# Definition of Done

A task is DONE only when ALL hold:
1. Acceptance criteria from the ERPNext task are met and demonstrable.
2. Built with Frappe methods (see frappe-methods.md) — no raw SQL/HTTP shortcuts.
3. Failing test was written first (TDD), now passing.
4. Unit + relevant integration tests pass locally.
5. CI is green: lint + tests + coverage threshold.
6. Branch/commit/PR follow git-conventions.md and reference the task ID.
7. No hardcoded secrets or environment-specific values.
8. Reviewer approved.
