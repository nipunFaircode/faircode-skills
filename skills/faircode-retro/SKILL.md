---
name: faircode-retro
description: >-
  Use at the end of each sprint or at project close for a retrospective.
  Triggers on "retro", "retrospective", "what went well", "lessons learned",
  "end of sprint", "post-mortem". Captures what to keep, stop, and try - and
  turns observations into tracked action items.
---

# Faircode Retrospective

The retro only works if it produces action items with owners. Notes without
owners are noise.

## When to run
- End of each sprint (2-week cadence minimum).
- At project close, before handover.

## Format: async-first, sync to decide
1. Team fills the board asynchronously before the meeting (15 min, no meeting).
2. 30-minute sync to discuss, deduplicate, and assign owners.
3. No sync longer than 45 minutes.

## Four sections

**1. What went well (keep doing)**
Specific practices that worked. Name the practice, not the person.
- Good: "Daily standups caught the GST template issue before the invoice run."
- Bad: "Nakul did a great job."

**2. What didn't go well (stop doing)**
Problems, blockers, friction points. No blame, no naming individuals.
Describe the situation and its impact.
- Good: "Requirements were unclear on the approval workflow - we had to redo
  the Work Order logic twice."
- Bad: "The customer was difficult."

**3. What to try next sprint (experiments)**
One or two new practices to test. Time-bound - evaluate at the next retro.
If it helped, move it to "what went well". If not, drop it.

**4. Action items**
Every item in "didn't go well" must have an action item or an explicit
"we accept this as unavoidable." No unresolved complaints.

| Owner | Action | Deadline | ERPNext Task |
| --- | --- | --- | --- |
| Name | Specific, actionable | Date | #task-id |

## Carry-forwards
Review unresolved action items from the previous retro FIRST, before opening
new items. If an action was not completed: re-assign with a new deadline, or
close it with a documented reason.

## Facilitation rules
- No blame, no naming individuals in "didn't go well."
- Every action item has exactly one owner - not "the team."
- An action item without a deadline is not an action item.
- No item gets closed without either an action or an explicit accept.

## Output
Retro notes saved to the project folder in Google Drive. Link shared with the
full project team within 24 hours of the session.

## STOP - red flags
| Thought | Reality |
| --- | --- |
| "We don't have time for a retro this sprint" | The sprints you skip are the ones where problems compound. |
| "We all know what went wrong, no need to write it" | Unwritten lessons don't transfer to the next project or team member. |
| "Action items without owners are fine" | No owner = no action. Assign one person, not "the team." |
| "We covered everything last retro" | Carry-forwards first. If they're all done, the retro is short. |

## Definition of Done
- All four sections completed.
- Every "didn't go well" item has an action item or an explicit accept.
- Action items created in ERPNext with owners and deadlines.
- Retro notes saved to Google Drive and linked in the project channel.
