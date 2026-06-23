---
name: frappe-testing-browser
description: >-
  Use when writing or running end-to-end browser tests for a Frappe app.
  Triggers on "UI test", "browser test", "Cypress", "end-to-end test", "e2e",
  "bench run-ui-tests", "automated UI testing". Covers Cypress setup for
  Frappe, form interaction patterns, list view assertions, and CI integration.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
---

# Frappe Browser Testing - Cypress

Frappe uses Cypress for browser tests (built-in from v14). Playwright is an
alternative but has no Frappe-specific helpers - use Cypress unless you have
a strong reason not to.

## Setup

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

## Common test patterns

```javascript
// Basic form test
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

    // Set quantity
    cy.get('[data-fieldname="items"] [data-fieldname="qty"] input')
      .first().clear().type('5');

    // Save
    cy.get('.page-head .btn-primary').click();

    // Assert saved
    cy.get('.frappe-control[data-fieldname="docstatus"]')
      .should('not.exist'); // draft has no docstatus badge
    cy.get('.title-text').should('contain', 'SO-');
  });
});
```

## Key selectors (Frappe-specific)

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

## Assertions

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

## Cleanup after tests

```javascript
afterEach(() => {
  // Delete test documents via API
  cy.request({
    method: 'DELETE',
    url: '/api/resource/Sales Order/SO-TEST-001',
    failOnStatusCode: false,
  });
});
```

## Running tests

```bash
# Interactive (development)
cd apps/myapp && npx cypress open

# Headless (CI)
bench run-ui-tests --app myapp
# or directly:
cd apps/myapp && npx cypress run --headless --browser chrome
```

## GitHub Actions CI

```yaml
- name: Run browser tests
  run: |
    cd apps/myapp
    npx cypress run --headless --browser chrome
  env:
    CYPRESS_BASE_URL: http://site1.localhost:8000
```

## Anti-patterns

| Do NOT | Do Instead |
| --- | --- |
| `cy.wait(3000)` arbitrary sleep | `cy.get(selector).should('be.visible')` - Cypress retries automatically |
| Leave test data after the test | Delete via `cy.request(DELETE)` in `afterEach` |
| Test against production site | Dedicated test site only; never run Cypress on production |
| One massive test file for all features | One file per DocType or feature; each test independent |
| Assert on network request content | Assert on the UI result - test what the user sees |

## Definition of Done
- Cypress config in place and running against the dev site.
- At least one test covers the happy path for each custom DocType.
- Tests run headless in CI and pass on clean state.
- Test data cleaned up after each run.
- Flaky tests fixed before merge (no `cy.wait` without a reason).

## Related Skills
`faircode-test-driven-development`, `faircode-cicd-guardrails`, `frappe-testing-unit`
