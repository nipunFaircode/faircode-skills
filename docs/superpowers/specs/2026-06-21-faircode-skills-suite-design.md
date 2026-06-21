# Faircode Skills Suite — Design

**Date:** 2026-06-21
**Status:** Approved (brainstorming complete; ready for implementation plan)
**Owner:** Nipun C P (Faircode)

## Problem

Faircode delivers ERPNext implementation and customisation projects. The
delivery pipeline leaks quality at predictable points:

- **Discovery:** consultants miss requirement points during customer
  interviews; communication is long written notes, so customer and team are not
  on the same page.
- **Handoff:** consultants assign tasks without clear acceptance criteria;
  developers misunderstand requirements.
- **Development:** relatively inexperienced, non-professional developers copy
  code from chat, do not follow Frappe framework methods, and over-engineer
  simple solutions.
- **Testing:** no consistent Frappe TDD or end-to-end tests; quality is not
  locked by CI/CD.

The goal is a **set of skill packages** that give the team a structured,
repeatable way to run projects and produce a **quality, predictable, market-
presentable delivery**, with guard-rails strong enough for an inexperienced
team.

## Context (existing assets)

- ERPNext instance at `https://erp.faircode.co` with API token access.
- A delivery tracker (`~/Work/management/tracker`) already pulls Projects,
  Tasks, ToDo assignments, Timesheets, and Sales Invoices via the API
  (`fetch.py`).
- Reference: `https://github.com/frappe/skills` ships `code-style`,
  `frappe-app-dev`, `ui-design` — covering code, not project delivery/process.
  This suite extends that universe into delivery and process, and reuses
  frappe's code skills where they fit.

### Known issue to fix during implementation
`tracker/fetch.py` contains a **hardcoded ERPNext API token**. It must be
rotated and moved to the `FAIRCODE_ERP_TOKEN` env var as part of building the
shared ERPNext helper. Treat the current token as compromised.

## Decisions (locked during brainstorming)

| Decision | Choice |
| --- | --- |
| Delivery model | **Hybrid** — some skills are AI-agent instructions (coding, testing), some are human playbooks (interviews, MoM); shared structure and vocabulary; quality enforced in CI regardless of who/what did the work. |
| Suite scope | **All 24 skills** named below, built in phased rollout order. |
| Naming convention | Flat kebab-case, `faircode-<name>`. |
| Packaging | **Claude plugin + marketplace** — a git repo the team installs via `/plugin`. |
| ERPNext linkage | **Read + safe write with confirmation** via one shared helper; never write without y/N confirmation. |
| Git/CI platform | **Both GitHub Actions and GitLab CI** — `faircode-cicd-guardrails` ships templates for both. |
| Repo location | `/home/nipun/Work/management/faircode-skills` |

## The 24 skills

Tags: **[AI]** agent-run · **[Human]** playbook · **[Both]** hybrid. 🔒 = backed
by a CI lock, not advisory only.

**Orchestrator**
- `faircode-delivery` — root/index skill; routes agent and person to the right
  `faircode-*` skill at each project phase. **[Both]**

**Sales → Delivery handoff**
- `faircode-project-kickoff` — signed quotation/SOW → ERPNext Project skeleton
  (scope, milestones, deliverables, timeline). **[Both]**
- `faircode-requirements-discovery` 🔒 — **interactive** finetuned customer
  interviews; questions the consultant one aspect at a time, module by module;
  fit-gap between business requirements and vanilla ERPNext. **Completeness-gated:
  cannot proceed to a solution until the full ERP Coverage Map is answered or
  explicitly marked N/A.** See "Interactive discovery & completeness gate" below.
  **[Both]**

**Design & alignment (visual cues, same page)**
- `faircode-solution-blueprint` 🔒 — requirements → visual solution design
  (process flow diagrams, data model, mockups, fit-gap matrix) for sign-off.
  **Gated: refuses to emit a blueprint while any ERP Coverage Map item the
  discovery phase left open is still unresolved.** **[Both]**
- `faircode-customer-communication` — customer-facing updates/confirmations with
  visual summaries; explicit sign-off protocol. **[Both]**
- `faircode-meeting-minutes` — MoM: decisions, action items, owners, due dates →
  auto-linked to ERPNext tasks. **[Both]**
- `faircode-change-request` — scope-change control: log, impact, re-quote,
  sign-off. **[Both]**

**Work breakdown**
- `faircode-task-breakdown` — consultant decomposes blueprint into ERPNext Tasks
  with acceptance criteria; assigns developers; links git branch. **[Both]**

**Development**
- `faircode-frappe-development` 🔒 — "do it the Frappe way": framework methods,
  no copy-paste-from-chat, no over-engineering. Extends frappe `frappe-app-dev`.
  **[AI]**
- `faircode-code-style` 🔒 — house coding standards; wraps frappe `code-style`.
  **[AI]**
- `faircode-git-workflow` 🔒 — branch naming tied to ERPNext Task ID, commit/PR
  conventions, review gates. **[Both]**
- `faircode-bug-reporting` — structured repro/expected/actual/severity →
  ERPNext issue. **[Both]**

**Testing & CI locks**
- `faircode-test-driven-development` 🔒 — Frappe TDD: failing test first. **[AI]**
- `faircode-unit-testing` 🔒 — `FrappeTestCase` patterns. **[AI]**
- `faircode-integration-testing` 🔒 — server/API integration tests. **[AI]**
- `faircode-browser-testing` 🔒 — automated end-to-end UI (Playwright/Cypress).
  **[AI]**
- `faircode-manual-testing` — UAT scripts & acceptance checklists. **[Human]**
- `faircode-cicd-guardrails` 🔒 — CI wiring that locks all the above; templates
  for GitHub Actions and GitLab CI; branch protection. **[AI]**

**Release & operations**
- `faircode-data-migration` 🔒 — master/transaction migration: mapping,
  validation, dry-run, reconciliation. **[Both]**
- `faircode-deployment-release` 🔒 — staging→prod, bench migrate, go-live
  cutover checklist, rollback. **[Both]**
- `faircode-documentation-handover` 🔒 — user manuals, training, handover docs;
  **interactive — verifies every delivered module from the ERP Coverage Map is
  documented before sign-off.** **[Both]**

**Governance (continuous)**
- `faircode-project-tracking` — status, milestones, timesheet/%-complete/
  receivables (existing tracker). **[Both]**
- `faircode-estimation` — effort estimation + definition-of-done. **[Both]**

## Architecture

### Package layout
```
faircode-skills/                       git repo (GitHub primary; mirror GitLab)
├── .claude-plugin/
│   ├── plugin.json                    name "faircode", version, author
│   └── marketplace.json               /plugin marketplace add <repo>; /plugin install faircode
├── skills/
│   ├── faircode-delivery/SKILL.md     orchestrator
│   ├── faircode-task-breakdown/SKILL.md
│   ├── … 24 skill folders …
│   └── faircode-cicd-guardrails/
│       ├── SKILL.md
│       └── templates/
│           ├── github/erpnext-ci.yml
│           └── gitlab/.gitlab-ci.yml
├── shared/
│   ├── erpnext_client/                safe-write ERPNext helper (refactor of fetch.py)
│   └── references/                    frappe-methods.md, git-conventions.md,
│                                      definition-of-done.md, severity-levels.md,
│                                      erp-coverage-map.md  ← discovery completeness checklist
└── README.md
```

### Skill anatomy (one convention for all 24)
Each `SKILL.md` = YAML frontmatter (`name`, `description` containing a clear
trigger phrase) + body.

- **Guard-rail skills (🔒)** use a rigid template: a **mandatory checklist**
  (becomes todos), a **"STOP / red-flags" table** (superpowers style — catches
  rationalizations like "let me just copy this from chat"), and an explicit
  **Definition of Done** the agent must verify before claiming completion.
- **Flexible skills** (interviews, comms) are principle-based.
- All skills reference shared `references/` files rather than repeating content.

### Shared ERPNext helper (`shared/erpnext_client/`)
Refactor of `fetch.py`:
- Token from `FAIRCODE_ERP_TOKEN` env var (no hardcoding).
- **Read** functions: projects, tasks, todos, timesheets, invoices.
- **Safe-write** functions: `create_task`, `add_comment`, `log_action_item`,
  `file_bug` — each **prints the exact payload and requires y/N confirmation**
  before any POST.
- Consumed by `task-breakdown`, `meeting-minutes`, `bug-reporting`,
  `project-kickoff`.

### Interactive discovery & completeness gate (cross-cutting)
The discovery and documentation skills — `faircode-requirements-discovery`,
`faircode-solution-blueprint`, and `faircode-documentation-handover` — are
**interactive interviewers, not form generators**. This directly addresses the
core pain: *consultants miss many points during discussion*.

Behaviour required of these skills:
1. **One question at a time.** Walk the consultant through ERPNext **module by
   module**, asking a single focused question per turn and recording the answer.
   Never dump a long questionnaire; never assume an answer.
2. **Drive from the ERP Coverage Map.** `shared/references/erp-coverage-map.md`
   enumerates every ERPNext domain (Selling, Buying, Stock, Manufacturing,
   Accounts, HR & Payroll, Projects, CRM, Assets, Quality, Support,
   Website/Portal) and the cross-cutting aspects (company/org structure, chart of
   accounts, taxes, naming series, roles & permissions, print formats,
   workflows & approvals, integrations, data-migration sources, reporting/KPIs,
   multi-company/multi-currency). The skill tracks each item as
   **answered / N-A-with-reason / open**.
3. **Hard completeness gate.** The skill **MUST NOT propose a solution, produce
   a blueprint, or write final documentation while any applicable Coverage Map
   item is still `open`.** Each open item is either answered or explicitly marked
   `N/A` with a stated reason first. This gate uses the same STOP-table /
   Definition-of-Done discipline as the development guard-rails (hence these
   skills are marked 🔒).
4. **Surface gaps explicitly.** Output includes the filled coverage map, a list
   of customer-facing open questions, and the identified fit-gaps — so nothing
   is silently skipped.

### Quality lock — two layers
1. **Skill layer (advisory):** rigid skills + Definition-of-Done self-checks
   guide developer/agent behaviour.
2. **CI layer (the real lock):** `faircode-cicd-guardrails` ships ready-to-drop
   templates for **both** GitHub Actions and GitLab CI running:
   Frappe lint → unit + integration tests → coverage threshold → browser/e2e
   smoke. Branch-protection / merge-request rules mean **nothing reaches `main`
   without green checks**, regardless of who or what wrote the code.

### Skill chaining (`faircode-delivery` orchestrator)
```
kickoff → requirements-discovery → solution-blueprint
  → {customer-communication, meeting-minutes}
  → task-breakdown
  → [per task] frappe-development → TDD → {unit, integration, browser}-testing
  → git-workflow → cicd-guardrails → manual-testing/UAT
  → data-migration → deployment-release → documentation-handover

Continuous: project-tracking · estimation · change-request · bug-reporting · code-style
```
Each skill ends with a **"Next: invoke faircode-X"** pointer so an inexperienced
user is never guessing the next step.

## Rollout plan (do not ship all 24 at once)

- **Phase 1 — Pilot:** `faircode-delivery` (router), shared `erpnext_client`,
  `faircode-task-breakdown`, `faircode-frappe-development`,
  `faircode-test-driven-development`, `faircode-cicd-guardrails`.
  Rationale: hits the four sharpest pain points (missed requirements, copy-paste
  code, no TDD, no CI lock) and proves the plugin install/usage loop.
- **Phase 2 — Design & comms:** `requirements-discovery`, `solution-blueprint`,
  `customer-communication`, `meeting-minutes`.
- **Phase 3 — Full testing & dev hygiene:** `unit-testing`,
  `integration-testing`, `browser-testing`, `manual-testing`, `git-workflow`,
  `bug-reporting`, `code-style`.
- **Phase 4 — Release & governance:** `project-kickoff`, `change-request`,
  `data-migration`, `deployment-release`, `documentation-handover`,
  `project-tracking`, `estimation`.

## Success criteria

- Team installs the suite with one `/plugin install faircode`.
- A developer working a task is guided through frappe-method development + TDD,
  and **cannot** merge to `main` without green CI (lint + tests + coverage).
- A consultant runs a discovery interview and produces a visual blueprint and
  task list with acceptance criteria, linked to ERPNext.
- MoM action items and bug reports flow back into ERPNext (with confirmation).
- No hardcoded secrets; ERPNext token in env.

## Out of scope (for now)

- Full ERPNext write automation without confirmation.
- Replacing the existing tracker (it is integrated via `project-tracking`, not
  rebuilt).
- Unrelated refactoring of the tracker beyond the token fix.

## Open items for the implementation plan

- Exact frontmatter `description` trigger wording per skill (so Claude activates
  the right one).
- Whether `code-style` / `frappe-development` re-export frappe's skills by
  reference or vendor a copy.
- Coverage threshold value and which test layers are required vs advisory in CI.
- Playwright vs Cypress for `browser-testing`.
