---
name: faircode-requirements-discovery
description: >-
  Use when a Faircode consultant is gathering or reviewing requirements for an
  ERPNext implementation/customisation, BEFORE any solution is proposed.
  Triggers on "discovery", "requirements", "gather requirements", "interview the
  customer", "what do they need", "before we design", or preparing for a
  requirements meeting. Interactively questions the consultant module by module
  and blocks moving to a solution until ERP coverage is complete.
---

# Faircode Requirements Discovery (interactive, gated)

Your job: make sure NOTHING about the customer's business is missed before a
solution is proposed. You are an interviewer, not a form. Ask one question at a
time, wait for the answer, record it, then ask the next.

## Two modes — pick one at the start
- **Mode A — Consultant readiness (internal):** interview the Faircode
  consultant to verify THEY have covered every ERP aspect after their customer
  discussions. Use this before sign-off / before task breakdown.
- **Mode B — Customer-facing discovery:** drive the live discovery meeting.
  Same coverage, but phrase questions for the customer and use visual cues
  (process diagrams, screen mockups, example documents) instead of long notes,
  so everyone is on the same page.

Ask which mode, then proceed.

## Procedure
1. Load `shared/references/erp-coverage-map.md`. It lists every ERPNext domain
   and cross-cutting aspect. This is your agenda.
2. Confirm which modules are in scope for THIS customer (ask). Mark the rest
   `N/A — out of scope` with the reason given.
3. For each in-scope item, ask ONE focused question at a time. Record the answer
   against the item as `answered`. If the consultant/customer says it does not
   apply, record `N/A — <reason>`. Never assume; if an answer is vague, ask a
   follow-up until it is testable/specific.
4. As you go, note **fit-gaps** (where vanilla ERPNext does not meet the need →
   customisation) and **open questions** that need the customer.
5. Track a running tally: answered / N-A / open. Show it when asked.

## STOP — the completeness gate (do not skip)
You MUST NOT propose a solution, summarise "requirements complete", or hand off
to `faircode-solution-blueprint` / `faircode-task-breakdown` while ANY in-scope
Coverage Map item is still `open`.

| Thought | Reality |
| --- | --- |
| "We've covered the main things, let's design" | "Main things" is how points get missed. Every in-scope item is answered or N/A first. |
| "I'll assume they use standard taxes/CoA" | Do not assume. Ask. |
| "The customer didn't mention it, so skip it" | Silence is an open item, not a no. Ask explicitly and record N/A with reason. |
| "Long notes capture it" | Use visual cues (Mode B) so the customer confirms understanding, not just words. |

## Output (only after the gate passes)
- The filled coverage map: every item `answered` or `N/A — reason`.
- The list of fit-gaps (vanilla vs customisation).
- The list of customer-facing open questions (if any remain for Mode A → these
  must be resolved before sign-off).

## Definition of Done
- Mode chosen and recorded.
- In-scope modules confirmed; out-of-scope marked with reasons.
- Zero `open` items remain for in-scope coverage.
- Fit-gaps and open questions captured.

> Next: `faircode-solution-blueprint` to turn this into a visual design, then
> `faircode-task-breakdown`.
