---
name: faircode-code-style
description: >-
  Use when writing or reviewing Python or JavaScript code in a Faircode Frappe
  app. Triggers on "code style", "linting", "ruff", "eslint", "code review",
  "naming convention", "how to format". Enforces Faircode's coding standards
  for Frappe v14-v16 apps.
---

# Faircode Code Style

Rules enforced by `ruff` (Python) and ESLint (JS). CI blocks merge on failure.
No manual exceptions without a comment explaining the override.

## Python rules (ruff, line length 120)

**Mandatory:**
- No `frappe.db.sql()` without a comment explaining why the ORM can't do it.
- No bare `except:` - catch a specific exception or `except Exception as e` minimum.
- Always wrap user-facing strings in `_()` for translation.
- Use `frappe.throw()` not `raise frappe.ValidationError()`.
- No `print()` in production code - use `frappe.logger().debug()`.
- No TODO without a linked ERPNext task ID: `# TODO task-1234: fix ESI ceiling`.
- No commented-out code in PRs. Delete it or keep it - not both.
- Docstrings only on public `@frappe.whitelist()` methods, one line max.

**Naming:**
- Functions and variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- DocType controller class must match the DocType name: `SalesOrder`, `PayrollEntry`.

## JavaScript rules (ESLint, Frappe config)

**Mandatory:**
- Use `frappe.call()` not `$.ajax()` or raw `fetch()`.
- No `console.log()` in production code.
- Prefer `async/await` over `.then()` chains.
- Never manipulate form fields via jQuery DOM - use `frm.set_value()`, `frm.set_df_property()`, `frm.toggle_display()`.
- No inline styles on form elements - use CSS classes.

**Client Script structure:**
```javascript
// Good: namespaced, uses frm API
frappe.ui.form.on("Sales Order", {
    customer(frm) {
        if (!frm.doc.customer) return;
        frappe.call({
            method: "myapp.api.get_credit_limit",
            args: { customer: frm.doc.customer },
            callback(r) {
                frm.set_value("credit_limit", r.message);
            }
        });
    }
});
```

## General rules
- No magic numbers - use a Settings DocType field or a named constant.
- Functions do one thing. If you need a comment to explain what it does, split it.
- No half-finished features behind a flag without a task to complete them.
- Remove unused imports.

## STOP - red flags
| Thought | Reality |
| --- | --- |
| "Ruff says it's wrong but I know better" | Read the error code first. Ruff has very few false positives. |
| "I'll clean up console.logs before merge" | Pre-commit catches it. Write clean code from the start. |
| "This SQL is faster, no comment needed" | Comment is mandatory - future reader doesn't have your benchmark. |
| "It's a small script, translation isn't needed" | Every user-facing string gets `_()`. No exceptions. |

## Definition of Done
- `ruff check` passes with zero errors.
- ESLint passes with zero errors.
- No `print()` or `console.log()` in the diff.
- All user-facing strings wrapped in `_()`.
- No commented-out code, no unexplained TODOs.

> Next: `faircode-cicd-guardrails` to enforce this automatically in CI.
