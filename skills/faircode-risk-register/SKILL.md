---
name: faircode-risk-register
description: >-
  Use at project kickoff and reviewed at each sprint retro to track project
  risks. Triggers on "risk", "risk register", "what could go wrong", "risk
  assessment", "identify risks", "project risks". Ensures risks are visible,
  owned, and mitigated before they become issues.
---

# Faircode Risk Register

A risk identified and mitigated is cheap. A risk that becomes an issue mid-project
is expensive. Create the register at kickoff; review it at every retro.

## When
- Create: project kickoff (before development starts).
- Review: every sprint retro.
- Close: project handover.

## Risk fields

| Field | Values / Notes |
| --- | --- |
| ID | R-001, R-002, ... |
| Description | One sentence: what could go wrong and why. |
| Category | Technical, Scope, Client, Resource, Compliance |
| Likelihood | High / Med / Low |
| Impact | High / Med / Low |
| Risk Score | See matrix below |
| Mitigation Plan | Specific action with owner and deadline |
| Owner | One person responsible for the mitigation |
| Status | Open / Mitigated / Closed |

## Risk score matrix

| | High Impact | Med Impact | Low Impact |
| --- | --- | --- | --- |
| **High Likelihood** | 9 - Critical | 6 - High | 3 - Medium |
| **Med Likelihood** | 6 - High | 4 - Medium | 2 - Low |
| **Low Likelihood** | 3 - Medium | 2 - Low | 1 - Low |

**Escalation rule:** any risk scored 6 or above must be flagged to the project
lead within 24 hours of identification.

## Categories to always check at kickoff

**Data migration**
- Source data completeness: has the customer confirmed what data exists?
- Data quality: known duplicates, missing fields, inconsistent formats?
- Cutover window: how long can the business be offline for migration?

**Integration**
- Third-party API availability: sandbox credentials available? Go-live timeline?
- Existing system decommission: who switches off the old system and when?

**Client**
- Approval turnaround: is the key decision-maker available for timely sign-offs?
- Requirement clarity: are there modules the customer hasn't fully defined yet?
- Testing resources: who does UAT and how much time have they committed?

**Resource**
- Developer availability: any planned leaves overlapping critical milestones?
- Skill gap: any module requiring expertise not currently on the team?

**Compliance**
- GST/payroll statutory changes mid-project: any upcoming notification deadlines?
- E-invoicing mandate: does the customer's turnover require IRN by go-live?
- State-specific PT/labour law: confirmed for the customer's operating states?

**Technical**
- ERPNext version compatibility: custom app tested against the target bench version?
- Customisation conflicts: any overlap with ERPNext's own code in the target area?

## Storage
Register saved as a spreadsheet in the project folder in Google Drive.
Link it from the ERPNext project record in the Notes field.

## STOP - red flags
| Thought | Reality |
| --- | --- |
| "We'll deal with risks if they happen" | By then they are issues, not risks. The register exists to prevent that. |
| "The customer always delivers data on time" | Record it as a medium risk. Past performance is not a guarantee. |
| "Mitigation: we'll monitor it" | Monitoring is not mitigation. A mitigation is a specific action with an owner. |
| "Score is 6 but I'll tell the lead at the next retro" | Escalation rule: 24 hours. Not next retro. |

## Definition of Done
- Register created at kickoff with at least one entry per category reviewed.
- All risks scored 6+ have owners and mitigation plans with deadlines.
- Register linked from ERPNext project record.
- Reviewed at every sprint retro; statuses updated.
- All risks Mitigated or Closed at project handover.
