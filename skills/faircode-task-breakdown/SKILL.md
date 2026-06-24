---
name: faircode-task-breakdown
description: >-
  Use when a Faircode consultant turns a solution blueprint or a customer
  requirement into developer tasks in ERPNext. Triggers on "break this down",
  "assign to developer", "create tasks for", "acceptance criteria", or handing a
  requirement to the dev team. Ensures every task has clear acceptance criteria
  before a developer starts.
---

# Faircode Task Breakdown

Goal: no developer ever starts work without unambiguous acceptance criteria,
a task in erp.faircode.co, and a known custom app.

## Prerequisites - ERP credentials

Before starting, verify the token is available:

```bash
printenv FAIRCODE_ERP_TOKEN
```

If empty, the developer must export it from their shell profile:

```bash
export FAIRCODE_ERP_TOKEN=<api_key>:<api_secret>
```

The API key and secret come from ERPNext: erp.faircode.co > User > API Access.
Do not proceed until the token is confirmed non-empty.

## Collect dev environment info (ask once)

Before breaking down tasks, ask:

1. **ERPNext project ID** - the `PROJ-XXXX` ID from erp.faircode.co, not the project_name (e.g. `PROJ-0018`). To look it up: `curl -s "https://erp.faircode.co/api/resource/Project?fields=[\"name\",\"project_name\"]&limit_page_length=100" -H "Authorization: token $FAIRCODE_ERP_TOKEN"`
2. **Custom app name** - the Frappe app development will happen in (e.g. `greenbite`)
3. **Localhost site** - the developer's local bench site (e.g. `greenbite.local`)

Record these three values. They go on every task created in this session.

## Procedure

1. Restate the requirement in one sentence. Confirm with the consultant.
2. Split into the smallest independently shippable tasks. One outcome per task.
3. For EACH task write:
   - **Subject** - imperative, specific ("Add credit-limit check on Sales Order").
   - **Context** - the business reason, 1-2 lines.
   - **Acceptance criteria** - bullet list of observable, testable outcomes
     (Given/When/Then where useful). These become the test cases.
   - **Out of scope** - what this task does NOT cover.
   - **Estimate** - rough hours (see faircode-estimation when available).
4. Identify the ERPNext doctype(s) and whether it is config vs code.
5. For each task, show the full payload to the consultant (project, subject,
   description, AC, custom app) and ask for confirmation before writing.
   Once confirmed, create it with `--yes` (the `--yes` flag skips the
   interactive prompt because the consultant has already reviewed the payload
   in Claude):

   ```bash
   python3 ~/.claude/skills/faircode-task-breakdown/scripts/create_task.py \
     --project "PROJ-XXXX" \
     --subject "SUBJECT" \
     --description "CONTEXT (1-2 lines)" \
     --ac "- Given ...\n- When ...\n- Then ..." \
     --custom-app "APP_NAME" \
     --estimate 2.0 \
     --yes
   ```

   Required fields and their defaults (all sent by the script automatically):

   | Field | Flag | Default | Notes |
   | --- | --- | --- | --- |
   | `expected_time` | `--estimate` | 1.0 | Hours; must be > 0 or ERP rejects the task |
   | `exp_start_date` | `--start-date` | today | YYYY-MM-DD |
   | `exp_end_date` | `--end-date` | today + 7 days | YYYY-MM-DD |
   | `type` | `--type` | Task | Override for Bug, Feature, etc. |

   Always pass `--estimate` explicitly from the estimate agreed in step 3.
   The script prints the task name on success (e.g. `Created: TASK-2026-03954`).
   Record that ID.

6. After all tasks are created, output a summary table:

   | Task ID   | Subject | Branch |
   | --------- | ------- | ------ |
   | TASK-0042 | ...     | `feat/TASK-0042-<slug>` |

   Branch slug: lowercase, hyphen-separated, max 5 words from the subject.
   Full branch format: `feat/<task-id>-<slug>` (see references/git-conventions.md).

## Acceptance-criteria quality bar

Reject criteria that are vague ("works correctly", "looks good"). Each must be
something a tester can pass/fail without asking a question. See
`references/definition-of-done.md`.

## STOP - red flags

| Thought | Reality |
| --- | --- |
| "Developer will figure out the details" | That is how requirements get missed. Write the AC. |
| "It's obvious what done means" | Then it takes 20 seconds to write it down. Do it. |
| "I'll create the task without acceptance criteria, add later" | No. AC before assignment. |
| "FAIRCODE_ERP_TOKEN is probably set" | Check before creating - a failed API call mid-session wastes time. |
| "Project name is Faircode ERPNext" | ERP needs the ID (`PROJ-0018`), not the display name. Look it up first. |

## Definition of Done

- FAIRCODE_ERP_TOKEN confirmed set before any task is created.
- Custom app name collected and recorded on every task.
- Every created task has: subject, context, ≥1 testable AC, out-of-scope, estimate.
- All tasks exist in erp.faircode.co, linked to the project.
- Summary table with task IDs and branch names produced.

> Next: developer picks up the task → `faircode-frappe-development`.
