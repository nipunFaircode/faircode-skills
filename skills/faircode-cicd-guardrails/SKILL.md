---
name: faircode-cicd-guardrails
description: >-
  Use when setting up or fixing CI/CD for a Faircode Frappe app repo, or when
  asked to "lock quality", "add CI", "require tests before merge", or enforce
  coverage. Ships ready GitHub Actions and GitLab CI templates and the branch-
  protection rules that stop unreviewed/untested code reaching main.
---

# Faircode CI/CD Guard-rails

This is the layer that makes quality non-optional. Skills advise; CI enforces.

## Setup checklist (make a todo per item)
- [ ] Pick the platform: GitHub → copy `templates/github/erpnext-ci.yml` to the
      app repo's `.github/workflows/`. GitLab → copy
      `templates/gitlab/.gitlab-ci.yml` to the repo root.
- [ ] Adjust `--frappe-branch` and the coverage threshold (default 70%) to the
      project. Never lower without sign-off.
- [ ] Turn on branch protection / merge-request rules on `main`:
      - require the CI job to pass,
      - require ≥1 review approval,
      - disallow direct pushes to `main`.
- [ ] Verify a failing test actually blocks the PR/MR (open a throwaway PR).

## What CI enforces
1. Lint (`ruff`).
2. Frappe tests (`bench run-tests`).
3. Coverage threshold (`--fail-under`).
(Browser/e2e smoke is added in Phase 3.)

## STOP — red flags
| Thought | Reality |
| --- | --- |
| "Merge now, CI is red but it's unrelated" | Red is red. Fix or revert. |
| "Lower the coverage gate to pass" | Needs sign-off. Add tests instead. |
| "Push straight to main, it's urgent" | Branch protection exists for urgent moments too. |

## Definition of Done
- CI file committed to the app repo and green on a real PR/MR.
- Branch protection active on `main`.
- A deliberately failing test was shown to block merge.
