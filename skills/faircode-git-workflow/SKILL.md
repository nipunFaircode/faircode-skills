---
name: faircode-git-workflow
description: >-
  Use when setting up or following git conventions on a Faircode Frappe app
  project. Triggers on "branch naming", "commit convention", "PR rules",
  "git workflow", "how to branch", "code review". Enforces the branch/commit/PR
  rules that keep the team's repos readable and CI-compatible.
---

# Faircode Git Workflow

One set of rules across all Faircode Frappe repos. Consistency makes reviews
faster and CI reliable.

## Branch naming
```
feat/<task-id>-<slug>     # new feature - task ID from ERPNext
fix/<task-id>-<slug>      # bug fix
chore/<slug>              # tooling, config, deps - no task ID needed
hotfix/<slug>             # urgent production fix - branch from main
```
Examples: `feat/1042-credit-limit-check`, `fix/1087-esi-ceiling`, `chore/update-ruff`

## Commit convention
Conventional Commits. Scope = doctype or module in snake_case.
```
feat(sales_order): add credit-limit validation on submit
fix(payroll_entry): cap ESI deduction at ₹21,000 wage ceiling
chore(deps): upgrade frappe to v15.32.1
docs(readme): add env var setup instructions
```
One commit per logical change. Squash before merge if the PR has noise commits.

## PR rules
- Title: imperative sentence matching the commit scope.
- Body must include:
  - **What**: 1-2 lines describing the change.
  - **Why**: the business reason or task link.
  - **Test Plan**: numbered steps to verify the change.
  - ERPNext task number (e.g. `Task: #1042`).
- Squash merge to `main`. No merge commits on main.
- Delete branch after merge.

## Branch protection on `main`
- CI must pass (all checks green).
- Minimum 1 review approval.
- No direct push to `main` - no exceptions.

## Hotfix flow
1. Branch from `main`: `git checkout -b hotfix/<slug> main`.
2. Fix, commit, open PR to `main`.
3. After merge, cherry-pick the commit to `develop` if it exists.

## Release tagging
Tag on `main` after go-live or major milestone. Semver: `v1.0.0`, `v1.1.2`.
```bash
git tag -a v1.2.0 -m "Release v1.2.0 - GST e-invoicing"
git push origin v1.2.0
```

## Stale branch policy
Delete merged branches immediately. Close and delete unmerged branches after 30
days of inactivity with a comment explaining why.

## STOP - red flags
| Thought | Reality |
| --- | --- |
| "I'll push directly to main, it's urgent" | Urgency is exactly when mistakes happen. Hotfix branch takes 2 minutes. |
| "No need for a PR description, the code is obvious" | The reviewer needs the why, not the what. |
| "I'll fix the branch name after" | CI naming checks run on push. Fix it before pushing. |
| "One PR for two unrelated features" | One PR per logical change. Easier to revert, easier to review. |

## Definition of Done
- Branch follows naming convention with ERPNext task ID.
- Commit message passes conventional commits format.
- PR has description: what, why, test plan, task link.
- CI green before merge request is approved.
- Branch deleted after merge.

> Next: `faircode-frappe-development` to write the code.
