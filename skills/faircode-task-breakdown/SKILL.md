---
name: faircode-task-breakdown
description: >-
  Use when a Faircode consultant turns a solution blueprint or a customer
  requirement into developer tasks in ERPNext. Triggers on "break this down",
  "assign to developer", "create tasks for", "acceptance criteria", or handing a
  requirement to the dev team. Ensures every task has clear acceptance criteria
  before a developer starts.
---

# Faircode Task Breakdown

Goal: no developer ever starts work without unambiguous acceptance criteria.

## Procedure
1. Restate the requirement in one sentence. Confirm with the consultant.
2. Split into the smallest independently shippable tasks. One outcome per task.
3. For EACH task write:
   - **Subject** — imperative, specific ("Add credit-limit check on Sales Order").
   - **Context** — the business reason, 1–2 lines.
   - **Acceptance criteria** — bullet list of observable, testable outcomes
     (Given/When/Then where useful). These become the test cases.
   - **Out of scope** — what this task does NOT cover.
   - **Estimate** — rough hours (see faircode-estimation when available).
4. Identify the ERPNext doctype(s) and whether it is config vs code.
5. Create the tasks in ERPNext (with confirmation):
   `from shared.erpnext_client import ERPNextClient`
   `ERPNextClient().create_task(project, subject, context, acceptance_criteria)`
   Review the printed payload, confirm `y` only when correct.
6. Record the branch name per git-conventions: `feat/<task-id>-<slug>`.

## Acceptance-criteria quality bar
Reject criteria that are vague ("works correctly", "looks good"). Each must be
something a tester can pass/fail without asking a question. See
`shared/references/definition-of-done.md`.

## STOP — red flags
| Thought | Reality |
| --- | --- |
| "Developer will figure out the details" | That is how requirements get missed. Write the AC. |
| "It's obvious what done means" | Then it takes 20 seconds to write it down. Do it. |
| "I'll create the task without acceptance criteria, add later" | No. AC before assignment. |

## Definition of Done (for this skill)
- Every created task has subject, context, ≥1 testable AC, out-of-scope, estimate.
- Tasks exist in ERPNext, linked to the project.
- Branch naming recorded.

> Next: developer picks up the task → `faircode-frappe-development`.
