---
name: faircode-change-request
description: >-
  Use when a customer asks to add, remove, or change scope AFTER the SOW is
  signed. Triggers on "scope change", "can we add this", "new requirement",
  "change request", "CR", "out of scope". Ensures no extra work starts without
  a written, approved change request.
---

# Faircode Change Request

Any request that adds, removes, or changes a deliverable described in the
signed SOW is a change request. No exceptions. No work starts without written
approval.

## Trigger
The following phrases from a customer mean a CR is required:
- "Can we also add...", "While you're at it...", "We need one more thing..."
- "Actually, we want it to work differently..."
- "Can you remove X and replace it with Y?"
- "We didn't realise we also needed..."

## Procedure
1. **Stop.** Do not start any work. Acknowledge receipt to the customer.
2. **Document** the change precisely: what is being asked, which SOW section or
   deliverable it affects.
3. **Assess impact**: additional hours, cost delta (from rate card), timeline
   shift, which in-progress tasks are blocked or affected.
4. **Classify**:
   - Minor: fits within project contingency, no timeline impact, no cost
     increase. Still requires sign-off - just no revised SOW needed.
   - Major: additional cost, timeline extension, or replaces a SOW deliverable.
     Requires revised SOW or a signed CR document.
5. **Internal sign-off** from the project lead before presenting to the customer.
6. **Present to customer**: change description, impact statement, revised
   cost/timeline if Major. Use the CR template below.
7. **Written customer approval** - email confirmation or signed CR document.
   Verbal approval does not count.
8. **Only after approval**: create ERPNext tasks, update project plan, notify
   dev team.

## CR document fields
| Field | Content |
| --- | --- |
| CR Number | Sequential, e.g. CR-001 |
| Date | Date of request |
| Project | Project name |
| Requested By | Customer contact name |
| Description | What is being requested |
| SOW Reference | Which section/deliverable this affects |
| Impact | Additional hours, cost delta, new delivery date |
| Classification | Minor / Major |
| Internal Approval | Lead consultant name and date |
| Customer Approval | Signature or email confirmation and date |

File the signed CR in the project folder in Google Drive.

## STOP - red flags
| Thought | Reality |
| --- | --- |
| "It's a small change, I'll just do it" | Small changes compound. Every change goes through CR. No size threshold. |
| "The customer mentioned it verbally, that counts" | Written approval only. Email is fine. Verbal is not. |
| "I'll log the hours and tell them at the end" | Surprise bills destroy trust. CR before work, always. |
| "We're already over budget, a CR makes it awkward" | A CR protects both sides. Doing free work sets a precedent. |

## Definition of Done
- CR document created, numbered, and saved to Google Drive.
- Impact assessed (hours, cost, timeline).
- Internal sign-off obtained.
- Written customer approval received and filed.
- ERPNext tasks created and linked to the CR.
- Project plan updated.

> Next: `faircode-task-breakdown` to create tasks from the approved CR.
