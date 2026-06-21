---
name: faircode-frappe-development
description: >-
  Use when writing or modifying code for a Faircode ERPNext/Frappe customisation
  — DocTypes, controllers, hooks, whitelisted APIs, reports, background jobs.
  Triggers on implementing an assigned task, "write the code for", "add a field",
  "hook into save", "create an endpoint". Enforces Frappe methods, no
  copy-paste-from-chat, and no over-engineering.
---

# Faircode Frappe Development

This is a guard-rail skill. Follow it exactly; it overrides the urge to ship fast.

## Before writing code (checklist — make a todo per item)
- [ ] Read the task's acceptance criteria. If missing, STOP → `faircode-task-breakdown`.
- [ ] Confirm the right Frappe mechanism for the job (see
      `shared/references/frappe-methods.md`). For framework mechanics, load the
      upstream `frappe-app-dev` skill.
- [ ] Confirm this is the simplest solution that meets the AC (YAGNI).
- [ ] Start a branch per `shared/references/git-conventions.md`.

## While writing code
- Use framework methods (`frappe.get_doc`, `frappe.qb`, hooks, `@frappe.whitelist`).
- No raw SQL or hand-rolled HTTP where a framework method exists.
- No abstractions for a single use case. Match surrounding code style.
- Pair with `faircode-test-driven-development`: failing test FIRST.

## STOP — red flags (you are rationalizing)
| Thought | Reality |
| --- | --- |
| "I'll paste this snippet from chat, it looks right" | You must understand every line. Re-derive it with framework methods or don't use it. |
| "Raw SQL is faster to write" | Use `frappe.qb`/`frappe.db.get_value`. Raw SQL needs a written reason in the PR. |
| "Let me add a service layer / generic engine" | YAGNI. Solve the actual task. |
| "I'll skip the test, it's simple" | Simple things break. Test first. |
| "ignore_permissions=True makes it work" | Justify it in the PR or fix the permission model. |

## Definition of Done
See `shared/references/definition-of-done.md`. All 8 items must hold before you
mark the task complete.

> Next: `faircode-test-driven-development` (in parallel), then
> `faircode-git-workflow` and `faircode-cicd-guardrails`.
