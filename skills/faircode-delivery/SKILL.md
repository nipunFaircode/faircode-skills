---
name: faircode-delivery
description: >-
  Use at the start of any Faircode ERPNext/Frappe project task, or any time
  it's unclear which faircode-* skill applies, to route to the correct one.
  Triggers on: starting or resuming delivery work on a customer project;
  being mid-implementation and unsure what phase or skill comes next; asking
  which faircode skill to use for a given step (e.g. writing acceptance
  criteria, breaking down a blueprint); or mentioning project kickoff,
  requirements, blueprint, task breakdown, Frappe development, testing, CI,
  release, or handover for an ERPNext customisation project.
---

# Faircode Delivery — orchestrator

Pick the skill for the current phase. When unsure, start here.

## Phase → skill
- Kickoff (signed quote → project): `faircode-project-kickoff`
- Requirements interviews: `faircode-requirements-discovery`
- Visual solution design: `faircode-solution-blueprint`
- Customer updates & sign-off: `faircode-customer-communication`
- Minutes of meeting: `faircode-meeting-minutes`
- Scope change: `faircode-change-request`
- Break work into tasks: `faircode-task-breakdown`
- Write code (Frappe way): `faircode-frappe-development`
- Test first: `faircode-test-driven-development`
- Lock quality in CI: `faircode-cicd-guardrails`
- Manual/UAT: `faircode-manual-testing`
- Data migration: `faircode-data-migration`
- Release/go-live: `faircode-deployment-release`
- Docs/handover: `faircode-documentation-handover`
- Always-on: `faircode-project-tracking`, `faircode-estimation`,
  `faircode-bug-reporting`, `faircode-git-workflow`, `faircode-code-style`

## Default delivery flow
faircode-project-kickoff → faircode-requirements-discovery →
faircode-solution-blueprint →
{faircode-customer-communication, faircode-meeting-minutes} →
faircode-task-breakdown →
[per task] faircode-frappe-development → faircode-test-driven-development →
{unit,integration,browser}-testing → faircode-git-workflow →
faircode-cicd-guardrails → faircode-manual-testing → faircode-data-migration →
faircode-deployment-release → faircode-documentation-handover

> Pilot note: only a subset of these skills ship in v0.1 (faircode-delivery,
> faircode-requirements-discovery, faircode-task-breakdown,
> faircode-frappe-development, faircode-test-driven-development,
> faircode-cicd-guardrails, faircode-help). If a referenced skill is not
> installed yet, fall back to the closest available one and tell the user.
