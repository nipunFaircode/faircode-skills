# Git conventions

## Branches
`<type>/<erpnext-task-id>-<slug>` — e.g. `feat/TASK-0042-customer-credit-limit`.
Types: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`.

## Commits
`<type>: <imperative summary>` and reference the task: `feat: add credit limit check (TASK-0042)`.
Small, focused commits. Tests committed with the code they cover.

## PR / MR
- Title references the ERPNext task ID.
- Description: what, why, how tested, screenshots for UI.
- Must be green in CI (lint + tests + coverage) before review.
- At least one reviewer approval before merge to `main`.
