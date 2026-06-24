---
name: frappe-testing-browser
description: >-
  Use when writing or running end-to-end browser tests for a Frappe app.
  Triggers on "UI test", "browser test", "Cypress", "Playwright", "end-to-end
  test", "e2e", "bench run-ui-tests", "automated UI testing". Covers Cypress
  and Playwright setup for Frappe, form interaction patterns, list view
  assertions, and CI integration.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Browser Testing

Frappe has built-in Cypress support from v14. Playwright is a fully supported
alternative with better async ergonomics and faster parallel execution.

## Choose your framework

Ask the user which framework they want before writing any code:

| | Cypress | Playwright |
| --- | --- | --- |
| Frappe built-in support | Yes (`bench run-ui-tests`) | No - standalone only |
| Language | JavaScript only | JS/TS/Python/Java |
| Parallelism | Paid tier (Cypress Cloud) | Free, built-in |
| Async model | Chainable commands | `async/await` |
| Debugging | Time-travel UI, screenshots | Trace viewer, screenshots |
| Best for | Teams already using Frappe defaults | New setups, TypeScript, parallel CI |

Default recommendation: **Cypress** if the project already uses `bench run-ui-tests`.
**Playwright** if starting fresh or the team prefers `async/await`.

---

## Cypress

### Setup

Install Cypress in your app:
```bash
cd apps/myapp
yarn add --dev cypress
```

Or use bench's managed Cypress:
```bash
bench setup cypress
```

`apps/myapp/cypress.config.js`:
```javascript
const { defineConfig } = require('cypress');
module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://site1.localhost:8000',
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: 'cypress/support/e2e.js',
    viewportWidth: 1280,
    viewportHeight: 800,
    defaultCommandTimeout: 10000,
  },
});
```

`cypress/support/commands.js` - login helper:
```javascript
Cypress.Commands.add('login', (user = 'Administrator', password = 'admin') => {
  cy.request({
    method: 'POST',
    url: '/api/method/login',
    body: { usr: user, pwd: password },
  });
  cy.visit('/app');
});
```

### Common test patterns

```javascript
describe('Sales Order', () => {
  before(() => { cy.login(); });

  it('creates a draft sales order', () => {
    cy.visit('/app/sales-order/new-sales-order-1');

    // Fill a Link field
    cy.get('.frappe-control[data-fieldname="customer"] input')
      .type('Test Customer')
      .wait(500);
    cy.get('.dropdown-item').contains('Test Customer').click();

    // Fill a Date field
    cy.get('.frappe-control[data-fieldname="delivery_date"] input')
      .type('12-31-2025');

    // Add a child table row
    cy.get('[data-fieldname="items"] .grid-add-row').click();
    cy.get('[data-fieldname="items"] [data-fieldname="item_code"] input')
      .first().type('ITEM-001').wait(500);
    cy.get('.dropdown-item').contains('ITEM-001').click();

    cy.get('[data-fieldname="items"] [data-fieldname="qty"] input')
      .first().clear().type('5');

    // Save
    cy.get('.page-head .btn-primary').click();

    cy.get('.title-text').should('contain', 'SO-');
  });
});
```

### Key selectors (Frappe-specific)

| What | Selector |
| --- | --- |
| Any field input | `.frappe-control[data-fieldname="field_name"] input` |
| Read-only field value | `.frappe-control[data-fieldname="field_name"] .control-value` |
| Primary action button | `.page-head .btn-primary` |
| Secondary button by label | `.page-head .btn-secondary:contains("Label")` |
| Child table add row | `[data-fieldname="child_table"] .grid-add-row` |
| Child table field | `[data-fieldname="child_table"] [data-fieldname="field"] input` |
| Dialog confirm button | `.modal-footer .btn-primary` |
| Alert/toast | `.alert-message` |

### Assertions

```javascript
// Field has value
cy.get('.frappe-control[data-fieldname="status"] .control-value')
  .should('contain', 'Draft');

// Currency field is positive
cy.get('.frappe-control[data-fieldname="grand_total"] .control-value')
  .invoke('text')
  .then((text) => {
    const val = parseFloat(text.replace(/[^0-9.]/g, ''));
    expect(val).to.be.gt(0);
  });

// Toast alert appeared
cy.get('.alert-message').should('contain', 'Saved');
```

### Cleanup after tests

```javascript
afterEach(() => {
  cy.request({
    method: 'DELETE',
    url: '/api/resource/Sales Order/SO-TEST-001',
    failOnStatusCode: false,
  });
});
```

### Running tests

```bash
# Interactive (development)
cd apps/myapp && npx cypress open

# Headless (CI)
bench run-ui-tests --app myapp
# or directly:
cd apps/myapp && npx cypress run --headless --browser chrome
```

### GitHub Actions CI

```yaml
- name: Run browser tests
  run: |
    cd apps/myapp
    npx cypress run --headless --browser chrome
  env:
    CYPRESS_BASE_URL: http://site1.localhost:8000
```

---

## Playwright

### Setup

```bash
cd apps/myapp
yarn add --dev @playwright/test
npx playwright install chromium
```

`apps/myapp/playwright.config.js`:
```javascript
const { defineConfig, devices } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './playwright/e2e',
  use: {
    baseURL: 'http://site1.localhost:8000',
    viewport: { width: 1280, height: 800 },
    actionTimeout: 10000,
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
```

Login helper - use a shared fixture so auth happens once per test file:

`playwright/fixtures.js`:
```javascript
const { test: base, expect } = require('@playwright/test');

exports.test = base.extend({
  authedPage: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.request.post('/api/method/login', {
      data: { usr: 'Administrator', pwd: 'admin' },
    });
    await use(page);
    await context.close();
  },
});
exports.expect = expect;
```

### Common test patterns

```javascript
const { test, expect } = require('./fixtures');

test.describe('Sales Order', () => {
  test('creates a draft sales order', async ({ authedPage: page }) => {
    await page.goto('/app/sales-order/new-sales-order-1');

    // Fill a Link field
    await page.locator('.frappe-control[data-fieldname="customer"] input').fill('Test Customer');
    await page.waitForTimeout(300); // debounce for autocomplete
    await page.locator('.dropdown-item', { hasText: 'Test Customer' }).click();

    // Fill a Date field
    await page.locator('.frappe-control[data-fieldname="delivery_date"] input').fill('12-31-2025');

    // Add a child table row
    await page.locator('[data-fieldname="items"] .grid-add-row').click();
    await page.locator('[data-fieldname="items"] [data-fieldname="item_code"] input').first().fill('ITEM-001');
    await page.waitForTimeout(300);
    await page.locator('.dropdown-item', { hasText: 'ITEM-001' }).click();

    await page.locator('[data-fieldname="items"] [data-fieldname="qty"] input').first().fill('5');

    // Save
    await page.locator('.page-head .btn-primary').click();

    // Assert
    await expect(page.locator('.title-text')).toContainText('SO-');
  });
});
```

### Key selectors (Frappe-specific)

Same HTML structure as Cypress - the selectors are identical, only the API differs.

| What | Locator |
| --- | --- |
| Any field input | `page.locator('.frappe-control[data-fieldname="field_name"] input')` |
| Read-only field value | `page.locator('.frappe-control[data-fieldname="field_name"] .control-value')` |
| Primary action button | `page.locator('.page-head .btn-primary')` |
| Secondary button by label | `page.locator('.page-head .btn-secondary', { hasText: 'Label' })` |
| Child table add row | `page.locator('[data-fieldname="child_table"] .grid-add-row')` |
| Child table field | `page.locator('[data-fieldname="child_table"] [data-fieldname="field"] input')` |
| Dialog confirm button | `page.locator('.modal-footer .btn-primary')` |
| Alert/toast | `page.locator('.alert-message')` |

### Assertions

```javascript
// Field has value
await expect(page.locator('.frappe-control[data-fieldname="status"] .control-value'))
  .toContainText('Draft');

// Currency field is positive
const text = await page.locator('.frappe-control[data-fieldname="grand_total"] .control-value').innerText();
const val = parseFloat(text.replace(/[^0-9.]/g, ''));
expect(val).toBeGreaterThan(0);

// Toast appeared
await expect(page.locator('.alert-message')).toContainText('Saved');
```

### Cleanup after tests

```javascript
test.afterEach(async ({ request }) => {
  await request.delete('/api/resource/Sales Order/SO-TEST-001').catch(() => {});
});
```

### Running tests

```bash
# Interactive UI mode (development)
cd apps/myapp && npx playwright test --ui

# Headless (CI)
cd apps/myapp && npx playwright test

# Single browser
cd apps/myapp && npx playwright test --project=chromium

# Show trace on failure
cd apps/myapp && npx playwright show-trace test-results/.../trace.zip
```

### GitHub Actions CI

```yaml
- name: Install Playwright browsers
  run: cd apps/myapp && npx playwright install --with-deps chromium

- name: Run browser tests
  run: cd apps/myapp && npx playwright test
  env:
    PLAYWRIGHT_BASE_URL: http://site1.localhost:8000
```

---

## Anti-patterns (both frameworks)

| Do NOT | Do Instead |
| --- | --- |
| Arbitrary `cy.wait(3000)` / `waitForTimeout(3000)` | Assert on visibility - both frameworks retry automatically. Use `waitForTimeout` only for Frappe's autocomplete debounce (300ms max). |
| Leave test data after the test | Delete via API request in `afterEach` |
| Test against production site | Dedicated test site only |
| One massive test file for all features | One file per DocType or feature; each test independent |
| Assert on network request content | Assert on the UI result - test what the user sees |
| Playwright: skip `storageState` / fixtures | Reuse auth context via fixtures - logging in per test is slow |
| Cypress: `cy.login()` in `it()` blocks | Call `cy.login()` in `before()` or `beforeEach()` |

## Definition of Done

- Framework config in place and running against the dev site.
- At least one test covers the happy path for each custom DocType.
- Tests run headless in CI and pass on clean state.
- Test data cleaned up after each run.
- No arbitrary sleeps - all waits are assertion-based.
- Flaky tests fixed before merge.

## Related Skills

`faircode-test-driven-development`, `faircode-cicd-guardrails`, `frappe-testing-unit`
