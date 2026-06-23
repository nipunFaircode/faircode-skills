---
name: faircode-bug-reporting
description: >-
  Use when reporting a bug on a Faircode ERPNext project, internal or from a
  customer. Triggers on "something is broken", "report a bug", "raise an issue",
  "bug template", "defect". Ensures every report has enough information to
  reproduce and fix without back-and-forth.
---

# Faircode Bug Reporting

A bug report without steps to reproduce is a complaint, not a report. Every
field below is required before the ticket is accepted.

## Severity definitions (use these, not gut feel)

| Severity | Definition |
| --- | --- |
| Critical | Data loss, production site down, financial posting wrong (wrong GL entries, wrong tax). |
| High | Core workflow blocked - can't submit an invoice, can't run payroll. No workaround. |
| Medium | Degraded behaviour, workaround exists (different browser, skip a step, use a different route). |
| Low | Cosmetic, typo, minor UX issue. Does not affect data or workflow. |

## Required fields in every bug report

Create as an ERPNext Task linked to the project. All fields mandatory before assignment.

1. **Summary** - one sentence: what breaks and in what context.
   - Bad: "Invoice is not working."
   - Good: "Sales Invoice fails to submit when 'Update Stock' is enabled and the delivery note has a batch item."
2. **Environment** - site URL, ERPNext version (`bench version` output), browser + version, user role used.
3. **Steps to reproduce** - numbered, exact, starting from login. A reviewer must follow them in a fresh browser without asking a question.
4. **Expected result** - what should happen according to the requirement or standard ERPNext behaviour.
5. **Actual result** - what actually happens. Paste the exact error message, not a paraphrase.
6. **Logs** - paste the relevant lines from ERPNext Error Log (desk → Menu → Error Log) or browser console. Screenshot for UI bugs.
7. **Reproducible in incognito?** - Yes / No. Rules out browser cache/extensions.
8. **Reproducible by another user/role?** - Yes / No. Rules out user-specific permissions.

## Where to report
ERPNext Task, linked to the project. Severity in the Priority field. Tag the assigned developer.

## STOP - red flags
| Thought | Reality |
| --- | --- |
| "The customer said it's broken, that's enough" | "It's broken" is not a bug report. Get the steps. |
| "I'll attach logs later" | Logs at report time, before the state changes. Do it now. |
| "Severity is Critical because the customer is angry" | Severity is based on impact, not emotion. Use the definitions. |
| "I reproduced it once, that's enough" | Confirm it's reproducible, not a one-off. Try incognito and a second user. |

## Definition of Done
- Bug report created in ERPNext with all 8 fields complete.
- Severity assigned using the definitions table - no escalation without matching definition.
- Logs and screenshot attached.
- Steps verified as reproducible by the reporter before assigning.
