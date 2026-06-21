---
name: faircode-delivery
description: >-
  Use at the start of any Faircode ERPNext project task to route to the correct
  faircode-* skill. Triggers when the user mentions a Faircode delivery, an
  ERPNext implementation/customisation project, "which skill do I use", project
  kickoff, requirements, blueprint, task breakdown, development, testing, CI,
  release, or handover for a customer project.
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
kickoff → requirements-discovery → solution-blueprint →
{customer-communication, meeting-minutes} → task-breakdown →
[per task] frappe-development → test-driven-development →
{unit,integration,browser}-testing → git-workflow → cicd-guardrails →
manual-testing → data-migration → deployment-release → documentation-handover

> Pilot note: only a subset of these skills ship in v0.1 (delivery,
> requirements-discovery, task-breakdown, frappe-development,
> test-driven-development, cicd-guardrails). If a referenced skill is not
> installed yet, fall back to the closest available one and tell the user.
