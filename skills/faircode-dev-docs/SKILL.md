---
name: faircode-dev-docs
description: >-
  Use when a Faircode developer has finished building a feature or task and
  wants to generate a simple dev doc. Triggers on "generate dev docs",
  "document this", "I'm done, write the docs", "create dev docs", "document
  what I built". Collects requirement, what was built, files changed, test
  steps, limitations, and developer name. Writes a markdown file to
  apps/<app>/dev_docs/<feature-slug>.md, creating the folder if needed.
license: MIT
compatibility: "Claude Code. Frappe v14-v16."
---

# Faircode Dev Docs

Goal: one markdown file per feature, stored in the app, that tells a reviewer
or QA exactly what was built and how to verify it - written in under 5 minutes.

## Step 1 - collect info (one round, all at once)

Ask all questions in a single AskUserQuestion call. Do not ask in multiple
rounds.

Required fields:
- **Custom app name** - the Frappe app the work lives in (e.g. `greenbite`)
- **Feature slug** - short kebab-case name for the file (e.g. `credit-limit-check`). This becomes the filename.
- **Task ID** - the ERP task reference (e.g. `TASK-2026-00042`). Optional; write "N/A" if not provided.
- **Requirement** - one or two sentences: what the customer/consultant asked for.
- **Developed by** - developer's name or email.

## Step 2 - auto-detect changed files

After collecting the fields above, run this to get the list of changed files
automatically. Do not ask the developer to list them manually.

```bash
git diff --name-only HEAD
```

If the repo is clean (nothing staged or unstaged), fall back to:

```bash
git diff --name-only HEAD~1
```

Present the file list to the developer and ask them to confirm or remove
irrelevant entries (e.g. lock files, auto-generated). This is one quick
confirmation, not a new question round.

## Step 3 - gather detail (one round)

Ask in a single AskUserQuestion call:
- **What was built** - DocType(s), fields added/changed, business logic
  implemented. Be specific.
- **How to test** - numbered step-by-step manual test steps a QA can follow
  without asking questions. Include login role, navigation path, input values,
  and expected result for each step.
- **Known limitations / out of scope** - what was explicitly not built.
  Write "None" if nothing to note.

## Step 4 - write the doc

Target path: `apps/<app>/dev_docs/<feature-slug>.md`

Check if the folder exists:

```bash
ls apps/<app>/dev_docs 2>/dev/null || echo "MISSING"
```

If missing, create it:

```bash
mkdir -p apps/<app>/dev_docs
```

Then write the file using the Write tool with this exact template:

```markdown
# <Feature Title (humanised from slug)>

| | |
|---|---|
| **Task ID** | TASK-XXXX |
| **Requirement** | <one or two sentence requirement> |
| **Developed by** | <name> |
| **Date** | <YYYY-MM-DD> |
| **App** | `<app>` |

---

## What was built

<DocType(s), fields, business logic - specific, not generic>

---

## Files changed

<bullet list from git diff>

---

## How to test

<numbered steps - role, path, inputs, expected result>

---

## Known limitations / out of scope

<bullet list, or "None">
```

After writing, print the full path of the created file.

## Step 5 - confirm

Tell the developer the file was written and suggest:
```
git add apps/<app>/dev_docs/<feature-slug>.md
```

Do not commit - the developer decides when to include it.

## Quality bar

Reject vague entries before writing:
- "How to test" steps must include the navigation path and expected outcome, not just "open the form and check".
- "What was built" must name specific DocTypes, fields, or methods - not "implemented the feature".
- Each test step must be passable/failble by a QA who has never seen the code.

## STOP - red flags

| Thought | Reality |
|---|---|
| "Developer will fill in test steps later" | No. Write them now while the context is fresh. |
| "The requirement is obvious" | Write it in one sentence anyway. Future devs won't have this conversation. |
| "git diff shows 50 files, list them all" | Filter to relevant app files only. Skip lock files, node_modules, __pycache__. |

## Definition of Done

- `apps/<app>/dev_docs/<feature-slug>.md` exists.
- Doc has all six sections populated (no empty or "TBD" entries).
- Test steps are numbered and self-contained.
- File path printed to the developer after write.
