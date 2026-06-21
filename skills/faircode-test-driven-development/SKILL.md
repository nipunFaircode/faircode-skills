---
name: faircode-test-driven-development
description: >-
  Use before writing implementation code for any Faircode Frappe feature or bug
  fix. Triggers on "implement", "fix the bug", "add the feature", or starting an
  assigned ERPNext task. Enforces write-test-first using Frappe's test tooling.
---

# Faircode TDD (Frappe)

Write the test first. Watch it fail. Write minimal code to pass. No exceptions
on real work (throwaway spikes excepted — ask the consultant).

## The loop
1. **Write a failing test** in `<app>/<module>/test_<doctype>.py` using
   `FrappeTestCase`:
   ```python
   from frappe.tests.utils import FrappeTestCase
   import frappe

   class TestCreditLimit(FrappeTestCase):
       def test_blocks_over_limit_sales_order(self):
           so = frappe.get_doc({"doctype": "Sales Order", ...})
           with self.assertRaises(frappe.ValidationError):
               so.insert()
   ```
2. **Run it, watch it fail** for the RIGHT reason:
   `bench --site <site> run-tests --module <app>.<module>.test_<doctype>`
   Expected: fail (feature not implemented) — not an import/typo error.
3. **Write minimal code** in the controller/hook to pass. Nothing extra.
4. **Run tests, watch them pass.**
5. **Refactor** with tests green. **Commit** (test + code together).

## Each acceptance criterion = at least one test
Map every AC from the task to a named test. If an AC has no test, it is not done.

## STOP — red flags
| Thought | Reality |
| --- | --- |
| "I'll write the test after the code" | Then you're testing what you wrote, not the requirement. Test first. |
| "I didn't see it fail but it's fine" | If you didn't watch it fail, you don't know it tests anything. |
| "Too simple to test" | Write the one-line test. It takes seconds. |

## Definition of Done
- One+ test per acceptance criterion, all green.
- Tests committed alongside the code.
- Part of the CI gate (see `faircode-cicd-guardrails`).

> Next: `faircode-cicd-guardrails` ensures these tests run on every push.
