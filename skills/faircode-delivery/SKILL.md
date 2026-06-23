---
name: faircode-delivery
description: >-
  Use at the start of any Faircode ERPNext project task to route to the correct
  faircode-* skill. Triggers when the user mentions a Faircode delivery, an
  ERPNext implementation/customisation project, "which skill do I use", project
  kickoff, requirements, blueprint, task breakdown, development, testing, CI,
  release, or handover for a customer project.
---

# Faircode Delivery - orchestrator

Pick the skill for the current phase. When unsure, start here.

## Phase → skill

### Delivery lifecycle
- Kickoff (signed quote → project): `faircode-project-kickoff`
- Requirements interviews: `faircode-requirements-discovery`
- Visual solution design: `faircode-solution-blueprint`
- Customer updates & sign-off: `faircode-customer-communication`
- Minutes of meeting: `faircode-meeting-minutes`
- Scope change: `faircode-change-request`
- Break work into tasks: `faircode-task-breakdown`
- Write code (Frappe way): `faircode-frappe-development`
- Test first: `faircode-test-driven-development`
- Browser/UI tests: `frappe-testing-browser`
- Lock quality in CI: `faircode-cicd-guardrails`
- Manual/UAT: `faircode-manual-testing`
- Data migration: `faircode-data-migration`
- Release/go-live: `faircode-deployment-release`
- Docs/handover: `faircode-documentation-handover`

### Always-on (any phase)
- Bug reports: `faircode-bug-reporting`
- Git conventions: `faircode-git-workflow`
- Code style: `faircode-code-style`
- Scope changes: `faircode-change-request`
- Sprint retrospective: `faircode-retro`
- Risk tracking: `faircode-risk-register`
- Estimation: `faircode-estimation`
- Project tracking: `faircode-project-tracking`

### ERPNext module configuration
Use these when configuring a specific module for a customer.
- Accounts & GST (India): `erpnext-accounts-gst`
- Payroll (India): `erpnext-payroll-india`
- Selling / quote-to-cash: `erpnext-selling`
- Buying / purchase-to-pay: `erpnext-buying`
- Stock & inventory: `erpnext-stock`
- Manufacturing & BOM: `erpnext-manufacturing`
- CRM & pipeline: `erpnext-crm`
- Fixed assets: `erpnext-assets`
- Point of sale: `erpnext-pos`

### Frappe technical reference
Use these when implementing specific framework features.
- Print formats & PDF: `frappe-impl-print-format`
- Email (SMTP, IMAP, sendmail): `frappe-impl-email`
- Payment gateway integration: `frappe-impl-payment`
- Real-time events (Socket.io): `frappe-core-realtime`
- Dev environment setup: `frappe-devenv-setup`
- Production monitoring: `frappe-ops-monitoring`

### AI features
- Claude API in Frappe (API call, caching, cost): `faircode-ai-copilot`
- AI integration patterns (where/how to wire): `frappe-impl-ai-integration`

## Default delivery flow
kickoff → requirements-discovery → solution-blueprint →
{customer-communication, meeting-minutes} → task-breakdown →
[per task] frappe-development → test-driven-development →
{unit,integration,browser-testing} → git-workflow → cicd-guardrails →
manual-testing → data-migration → deployment-release → documentation-handover

> Skills marked as not installed yet (kickoff, solution-blueprint,
> customer-communication, meeting-minutes, manual-testing, data-migration,
> deployment-release, documentation-handover, project-tracking): fall back to
> the closest available skill and tell the user.
