# Faircode Skills Suite — Phase 1 Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working, installable Claude plugin (`faircode`) containing the pilot skills plus the shared ERPNext helper, proving the install/use loop before expanding to all 24 skills.

**Architecture:** A git repo laid out as a Claude plugin: `.claude-plugin/{plugin.json,marketplace.json}`, `skills/<name>/SKILL.md` per skill, and a `shared/` directory with a Python ERPNext client and markdown reference files that skills cite. Skills are markdown instructions (frontmatter + body); the ERPNext client is tested Python. A pytest-based structure validator keeps the plugin manifest and skills consistent.

**Tech Stack:** Markdown (SKILL.md), Python 3.11+ (`shared/erpnext_client`, stdlib `urllib` only — no new deps), pytest, GitHub Actions + GitLab CI YAML templates.

## Global Constraints

- Skill names are flat kebab-case with a `faircode-` prefix; each skill lives in `skills/<name>/SKILL.md` and the frontmatter `name:` MUST equal the folder name.
- No hardcoded secrets anywhere. The ERPNext token is read from the `FAIRCODE_ERP_TOKEN` env var. ERPNext base URL from `FAIRCODE_ERP_URL` (default `https://erp.faircode.co`).
- Every ERPNext write (POST/PUT) MUST print the exact payload and require interactive `y/N` confirmation before sending; default on empty/non-`y` is abort.
- Python: stdlib only (`urllib`, `json`, `os`), no third-party HTTP libs. Target Python 3.11+.
- Plugin `repository` URL: `https://github.com/faircode/faircode-skills` — repo owner adjusts to the real remote before publishing.
- Guard-rail skills (`faircode-frappe-development`, `faircode-test-driven-development`, `faircode-cicd-guardrails`) MUST contain: a mandatory checklist, a "STOP / red-flags" table, and a "Definition of Done" section.
- Frequent commits: one commit per task minimum.

---

### Task 1: Plugin scaffold + structure validator

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `README.md`
- Create: `.gitignore`
- Create: `tests/test_plugin_structure.py`

**Interfaces:**
- Produces: a valid plugin manifest and a `validate_plugin(root)` test helper that later skill tasks reuse to confirm each new skill folder is wired into `marketplace.json` and has a matching frontmatter `name`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_plugin_structure.py`:

```python
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def _read_frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    assert m, f"{skill_md} missing YAML frontmatter"
    block = m.group(1)
    nm = re.search(r"^name:\s*(.+?)\s*$", block, re.MULTILINE)
    assert nm, f"{skill_md} frontmatter missing name:"
    return nm.group(1).strip()

def test_plugin_json_valid():
    data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert data["name"] == "faircode"
    assert re.match(r"^\d+\.\d+\.\d+$", data["version"])
    assert data["skills"] == "skills"

def test_marketplace_lists_existing_skills():
    mkt = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    plugin = mkt["plugins"][0]
    assert plugin["name"] == "faircode"
    for rel in plugin["skills"]:
        skill_dir = ROOT / rel
        assert skill_dir.is_dir(), f"listed skill missing: {rel}"
        name = _read_frontmatter_name(skill_dir / "SKILL.md")
        assert name == skill_dir.name, f"name {name} != folder {skill_dir.name}"

def test_no_hardcoded_token():
    # crude secret scan across tracked python and yaml
    pattern = re.compile(r"token\s+[0-9a-f]{15}:[0-9a-f]{15}")
    for path in ROOT.rglob("*"):
        if path.suffix in {".py", ".yml", ".yaml", ".md"} and path.is_file():
            if "test_plugin_structure" in path.name:
                continue
            assert not pattern.search(path.read_text(encoding="utf-8", errors="ignore")), f"possible token in {path}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_plugin_structure.py -v`
Expected: FAIL (FileNotFoundError — `.claude-plugin/plugin.json` does not exist).

- [ ] **Step 3: Write minimal implementation**

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "faircode",
  "version": "0.1.0",
  "description": "Faircode ERPNext delivery skills — discovery, blueprint, task breakdown, Frappe-method development, TDD, dual GitHub/GitLab CI guard-rails, release and governance.",
  "author": { "name": "Faircode", "url": "https://faircode.co" },
  "repository": "https://github.com/faircode/faircode-skills",
  "license": "UNLICENSED",
  "keywords": ["erpnext", "frappe", "delivery", "tdd", "ci", "project-management"],
  "skills": "skills"
}
```

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "faircode-skills",
  "owner": { "name": "Faircode", "url": "https://faircode.co" },
  "metadata": { "description": "Faircode ERPNext delivery skill suite", "version": "0.1.0" },
  "plugins": [
    {
      "name": "faircode",
      "description": "ERPNext implementation & customisation delivery skills",
      "source": "./",
      "strict": false,
      "skills": []
    }
  ]
}
```

Create `.gitignore`:

```
__pycache__/
*.pyc
.venv/
.env
.pytest_cache/
```

Create `README.md`:

```markdown
# Faircode Skills

Claude plugin: a delivery-lifecycle skill suite for Faircode's ERPNext
implementation & customisation team.

## Install (team)

```bash
/plugin marketplace add https://github.com/faircode/faircode-skills
/plugin install faircode
```

## Configure ERPNext access

```bash
export FAIRCODE_ERP_URL="https://erp.faircode.co"
export FAIRCODE_ERP_TOKEN="<api-key>:<api-secret>"   # never commit this
```

## Layout

- `skills/faircode-*/SKILL.md` — the skills
- `shared/erpnext_client/` — read + safe-write ERPNext helper
- `shared/references/` — shared rules cited by skills

See `docs/superpowers/specs/` for the design and `docs/superpowers/plans/` for the build plan.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_plugin_structure.py -v`
Expected: PASS (3 tests; `test_marketplace_lists_existing_skills` passes vacuously — empty skills list).

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin README.md .gitignore tests/test_plugin_structure.py
git commit -m "feat: plugin scaffold and structure validator"
```

---

### Task 2: ERPNext client — read layer

**Files:**
- Create: `shared/erpnext_client/__init__.py`
- Create: `shared/erpnext_client/client.py`
- Test: `tests/test_erpnext_read.py`

**Interfaces:**
- Consumes: env vars `FAIRCODE_ERP_URL`, `FAIRCODE_ERP_TOKEN`.
- Produces:
  - `class ERPNextClient(base_url: str | None = None, token: str | None = None)` — falls back to env vars; raises `RuntimeError` if token unset.
  - `ERPNextClient.get_list(doctype: str, fields: list[str], filters: list | None = None, order_by: str | None = None) -> list[dict]` (paginated, 500/page).
  - `ERPNextClient._request(method: str, path: str, params: dict | None, body: dict | None) -> dict` (internal; injectable transport via `self._opener` for tests).

- [ ] **Step 1: Write the failing test**

Create `tests/test_erpnext_read.py`:

```python
import json
import pytest
from shared.erpnext_client.client import ERPNextClient

class FakeResp:
    def __init__(self, payload): self._p = json.dumps(payload).encode()
    def read(self): return self._p
    def __enter__(self): return self
    def __exit__(self, *a): return False

def make_client(pages):
    calls = []
    def opener(req, timeout=60):
        calls.append(req.full_url)
        return FakeResp(pages.pop(0))
    c = ERPNextClient(base_url="https://erp.test", token="k:s")
    c._opener = opener
    c._calls = calls
    return c

def test_requires_token(monkeypatch):
    monkeypatch.delenv("FAIRCODE_ERP_TOKEN", raising=False)
    with pytest.raises(RuntimeError):
        ERPNextClient(base_url="https://erp.test")

def test_get_list_paginates():
    page1 = {"message": [{"name": f"T{i}"} for i in range(500)]}
    page2 = {"message": [{"name": "T500"}]}
    c = make_client([page1, page2])
    rows = c.get_list("Task", ["name"])
    assert len(rows) == 501
    assert len(c._calls) == 2
    assert "Authorization" not in c._calls[0]  # token is a header, not in URL
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_erpnext_read.py -v`
Expected: FAIL (ModuleNotFoundError: `shared.erpnext_client.client`).

- [ ] **Step 3: Write minimal implementation**

Create `shared/erpnext_client/__init__.py`:

```python
from .client import ERPNextClient

__all__ = ["ERPNextClient"]
```

Create `shared/erpnext_client/client.py`:

```python
"""Read + safe-write ERPNext client for Faircode skills.

Token from FAIRCODE_ERP_TOKEN env var (format "<api-key>:<api-secret>").
Base URL from FAIRCODE_ERP_URL (default https://erp.faircode.co).
Stdlib only.
"""
import json
import os
import urllib.parse
import urllib.request

DEFAULT_URL = "https://erp.faircode.co"


class ERPNextClient:
    def __init__(self, base_url=None, token=None):
        self.base_url = (base_url or os.environ.get("FAIRCODE_ERP_URL") or DEFAULT_URL).rstrip("/")
        self.token = token or os.environ.get("FAIRCODE_ERP_TOKEN")
        if not self.token:
            raise RuntimeError("FAIRCODE_ERP_TOKEN not set")
        self._opener = lambda req, timeout=60: urllib.request.urlopen(req, timeout=timeout)

    def _request(self, method, path, params=None, body=None):
        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"token {self.token}")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        with self._opener(req, timeout=60) as r:
            return json.loads(r.read().decode())

    def get_list(self, doctype, fields, filters=None, order_by=None):
        out, start = [], 0
        while True:
            params = {
                "doctype": doctype,
                "fields": json.dumps(fields),
                "limit_start": start,
                "limit_page_length": 500,
            }
            if filters:
                params["filters"] = json.dumps(filters)
            if order_by:
                params["order_by"] = order_by
            batch = self._request("GET", "/api/method/frappe.client.get_list", params=params)["message"]
            out.extend(batch)
            if len(batch) < 500:
                break
            start += 500
        return out
```

Create `tests/__init__.py` (empty) and `shared/__init__.py` (empty) if needed for imports; add `conftest.py` at repo root:

```python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_erpnext_read.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add shared/erpnext_client shared/__init__.py conftest.py tests/test_erpnext_read.py
git commit -m "feat: ERPNext client read layer with env-based auth"
```

---

### Task 3: ERPNext client — safe-write layer with confirmation

**Files:**
- Modify: `shared/erpnext_client/client.py`
- Test: `tests/test_erpnext_write.py`

**Interfaces:**
- Consumes: `ERPNextClient._request`, and a confirm hook `self._confirm` (defaults to interactive `input`; injectable in tests).
- Produces:
  - `ERPNextClient.create_task(project: str, subject: str, description: str, acceptance_criteria: str) -> dict | None` — returns created doc, or `None` if user declines.
  - `ERPNextClient.add_comment(doctype: str, name: str, text: str) -> dict | None`
  - `ERPNextClient.file_bug(project: str, subject: str, body: str) -> dict | None`
  - All three print the payload, call `self._confirm(summary) -> bool`, and only POST on `True`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_erpnext_write.py`:

```python
import json
from shared.erpnext_client.client import ERPNextClient

class FakeResp:
    def __init__(self, payload): self._p = json.dumps(payload).encode()
    def read(self): return self._p
    def __enter__(self): return self
    def __exit__(self, *a): return False

def client(confirm_value):
    posted = []
    def opener(req, timeout=60):
        posted.append((req.method, req.full_url, req.data))
        return FakeResp({"data": {"name": "TASK-0001"}})
    c = ERPNextClient(base_url="https://erp.test", token="k:s")
    c._opener = opener
    c._confirm = lambda summary: confirm_value
    c._posted = posted
    return c

def test_create_task_declined_does_not_post():
    c = client(confirm_value=False)
    result = c.create_task("PROJ-1", "Add field", "desc", "AC: field saves")
    assert result is None
    assert c._posted == []

def test_create_task_confirmed_posts():
    c = client(confirm_value=True)
    result = c.create_task("PROJ-1", "Add field", "desc", "AC: field saves")
    assert result["name"] == "TASK-0001"
    assert len(c._posted) == 1
    method, url, body = c._posted[0]
    assert method == "POST"
    assert "/api/resource/Task" in url
    sent = json.loads(body.decode())
    assert sent["project"] == "PROJ-1"
    assert "AC: field saves" in sent["description"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_erpnext_write.py -v`
Expected: FAIL (AttributeError: `ERPNextClient` has no attribute `create_task`).

- [ ] **Step 3: Write minimal implementation**

Append to `shared/erpnext_client/client.py` (add `import sys` at top):

```python
    def _confirm(self, summary):
        print(summary)
        return input("Proceed with this write to ERPNext? [y/N] ").strip().lower() == "y"

    def _safe_post(self, doctype, doc, summary):
        if not self._confirm(summary):
            print("Aborted — nothing written.")
            return None
        return self._request("POST", f"/api/resource/{urllib.parse.quote(doctype)}", body=doc)["data"]

    def create_task(self, project, subject, description, acceptance_criteria):
        full_desc = f"{description}\n\n## Acceptance Criteria\n{acceptance_criteria}"
        doc = {"project": project, "subject": subject, "description": full_desc}
        summary = f"CREATE Task in {project}: {subject!r}\n{full_desc}"
        return self._safe_post("Task", doc, summary)

    def add_comment(self, doctype, name, text):
        doc = {"reference_doctype": doctype, "reference_name": name,
               "content": text, "comment_type": "Comment"}
        summary = f"COMMENT on {doctype} {name}: {text!r}"
        return self._safe_post("Comment", doc, summary)

    def file_bug(self, project, subject, body):
        doc = {"project": project, "subject": subject, "description": body}
        summary = f"CREATE Issue in {project}: {subject!r}\n{body}"
        return self._safe_post("Issue", doc, summary)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_erpnext_write.py -v`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add shared/erpnext_client/client.py tests/test_erpnext_write.py
git commit -m "feat: ERPNext safe-write layer with confirmation gate"
```

---

### Task 4: Shared reference files

**Files:**
- Create: `shared/references/frappe-methods.md`
- Create: `shared/references/git-conventions.md`
- Create: `shared/references/definition-of-done.md`
- Create: `shared/references/severity-levels.md`
- Test: `tests/test_references_exist.py`

**Interfaces:**
- Produces: four markdown references cited by the pilot skills. Stable relative paths under `shared/references/`.

- [ ] **Step 1: Write the failing test**

Create `tests/test_references_exist.py`:

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def test_references_present_and_nonempty():
    for fn in ["frappe-methods.md", "git-conventions.md",
               "definition-of-done.md", "severity-levels.md"]:
        p = ROOT / "shared" / "references" / fn
        assert p.is_file(), f"missing {fn}"
        assert len(p.read_text().strip()) > 200, f"{fn} too thin"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_references_exist.py -v`
Expected: FAIL (missing files).

- [ ] **Step 3: Write minimal implementation**

Create `shared/references/frappe-methods.md`:

```markdown
# Frappe Methods — the Faircode way

Do it the framework's way. Never paste raw SQL or hand-rolled HTTP where a
framework method exists.

## Data access
- Read one: `frappe.get_doc(doctype, name)`. Read many: `frappe.get_all(doctype, filters=..., fields=...)`.
- Query builder for complex reads: `frappe.qb`. Raw `frappe.db.sql` only with a written reason in the PR.
- Single values: `frappe.db.get_value` / `set_value`. Never `UPDATE` by hand.

## Documents & lifecycle
- Create: `doc = frappe.new_doc(dt); doc.update({...}); doc.insert()`.
- Modify in controller hooks: `validate`, `before_save`, `on_submit`, `on_cancel` — declared in `hooks.py`, not monkey-patched.
- Never bypass permissions with `ignore_permissions=True` unless justified in the PR.

## APIs
- Expose with `@frappe.whitelist()`. Validate inputs. Return plain dicts/lists.

## Background work
- Long jobs: `frappe.enqueue`. Scheduled: `scheduler_events` in `hooks.py`.

## Anti-patterns (reject in review)
- Copy-pasted code from chat with no understanding of what it does.
- Re-implementing framework features (caching, permissions, naming series).
- Over-engineering: new abstraction layers for a one-off requirement (YAGNI).
```

Create `shared/references/git-conventions.md`:

```markdown
# Git conventions

## Branches
`<type>/<erpnext-task-id>-<slug>` — e.g. `feat/TASK-0042-customer-credit-limit`.
Types: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`.

## Commits
`<type>: <imperative summary>` and reference the task: `feat: add credit limit check (TASK-0042)`.
Small, focused commits. Tests committed with the code they cover.

## PR / MR
- Title references the ERPNext task ID.
- Description: what, why, how tested, screenshots for UI.
- Must be green in CI (lint + tests + coverage) before review.
- At least one reviewer approval before merge to `main`.
```

Create `shared/references/definition-of-done.md`:

```markdown
# Definition of Done

A task is DONE only when ALL hold:
1. Acceptance criteria from the ERPNext task are met and demonstrable.
2. Built with Frappe methods (see frappe-methods.md) — no raw SQL/HTTP shortcuts.
3. Failing test was written first (TDD), now passing.
4. Unit + relevant integration tests pass locally.
5. CI is green: lint + tests + coverage threshold.
6. Branch/commit/PR follow git-conventions.md and reference the task ID.
7. No hardcoded secrets or environment-specific values.
8. Reviewer approved.
```

Create `shared/references/severity-levels.md`:

```markdown
# Bug severity levels

- **S1 Blocker** — production down / data loss / no workaround. Fix now.
- **S2 Major** — core feature broken, workaround exists. Fix this sprint.
- **S3 Minor** — non-core defect or cosmetic-with-impact. Schedule.
- **S4 Trivial** — cosmetic / copy. Backlog.

Every bug report states: severity, environment, steps to reproduce,
expected vs actual, and the linked ERPNext project.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_references_exist.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add shared/references tests/test_references_exist.py
git commit -m "docs: shared references (frappe methods, git, DoD, severity)"
```

---

### Task 5: `faircode-delivery` orchestrator skill

**Files:**
- Create: `skills/faircode-delivery/SKILL.md`
- Modify: `.claude-plugin/marketplace.json` (add to `skills` list)

**Interfaces:**
- Consumes: nothing.
- Produces: the router skill listing the phase→skill map. Other skills reference it as the entry point.

- [ ] **Step 1: Write SKILL.md**

Create `skills/faircode-delivery/SKILL.md` with this exact frontmatter, then the body below:

```markdown
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

> Pilot note: only a subset of these skills ship in v0.1. If a referenced skill
> is not installed yet, fall back to the closest available one and tell the user.
```

- [ ] **Step 2: Wire into marketplace.json**

Edit `.claude-plugin/marketplace.json` — set the plugin's `skills` array to:

```json
      "skills": [
        "./skills/faircode-delivery"
      ]
```

- [ ] **Step 3: Run the structure validator**

Run: `python -m pytest tests/test_plugin_structure.py -v`
Expected: PASS (validator confirms `faircode-delivery` folder exists and frontmatter name matches).

- [ ] **Step 4: Commit**

```bash
git add skills/faircode-delivery .claude-plugin/marketplace.json
git commit -m "feat: faircode-delivery orchestrator skill"
```

---

### Task 6: `faircode-task-breakdown` skill

**Files:**
- Create: `skills/faircode-task-breakdown/SKILL.md`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: `shared/erpnext_client` (`create_task`), `shared/references/definition-of-done.md`.
- Produces: a procedure that turns a blueprint item into ERPNext tasks with acceptance criteria.

- [ ] **Step 1: Write SKILL.md**

Create `skills/faircode-task-breakdown/SKILL.md`:

```markdown
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

Goal: no developer ever starts work without unambiguous acceptance criteria.

## Procedure
1. Restate the requirement in one sentence. Confirm with the consultant.
2. Split into the smallest independently shippable tasks. One outcome per task.
3. For EACH task write:
   - **Subject** — imperative, specific ("Add credit-limit check on Sales Order").
   - **Context** — the business reason, 1–2 lines.
   - **Acceptance criteria** — bullet list of observable, testable outcomes
     (Given/When/Then where useful). These become the test cases.
   - **Out of scope** — what this task does NOT cover.
   - **Estimate** — rough hours (see faircode-estimation when available).
4. Identify the ERPNext doctype(s) and whether it is config vs code.
5. Create the tasks in ERPNext (with confirmation):
   `from shared.erpnext_client import ERPNextClient`
   `ERPNextClient().create_task(project, subject, context, acceptance_criteria)`
   Review the printed payload, confirm `y` only when correct.
6. Record the branch name per git-conventions: `feat/<task-id>-<slug>`.

## Acceptance-criteria quality bar
Reject criteria that are vague ("works correctly", "looks good"). Each must be
something a tester can pass/fail without asking a question. See
`shared/references/definition-of-done.md`.

## STOP — red flags
| Thought | Reality |
| --- | --- |
| "Developer will figure out the details" | That is how requirements get missed. Write the AC. |
| "It's obvious what done means" | Then it takes 20 seconds to write it down. Do it. |
| "I'll create the task without acceptance criteria, add later" | No. AC before assignment. |

## Definition of Done (for this skill)
- Every created task has subject, context, ≥1 testable AC, out-of-scope, estimate.
- Tasks exist in ERPNext, linked to the project.
- Branch naming recorded.

> Next: developer picks up the task → `faircode-frappe-development`.
```

- [ ] **Step 2: Wire into marketplace.json** — append `"./skills/faircode-task-breakdown"` to the `skills` array.

- [ ] **Step 3: Run the structure validator**

Run: `python -m pytest tests/test_plugin_structure.py -v`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add skills/faircode-task-breakdown .claude-plugin/marketplace.json
git commit -m "feat: faircode-task-breakdown skill"
```

---

### Task 7: `faircode-frappe-development` skill

**Files:**
- Create: `skills/faircode-frappe-development/SKILL.md`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: `shared/references/frappe-methods.md`, `shared/references/definition-of-done.md`. Defers framework mechanics to frappe's `frappe-app-dev` skill (by reference, not vendored).
- Produces: the guard-rail development workflow.

- [ ] **Step 1: Write SKILL.md**

Create `skills/faircode-frappe-development/SKILL.md`:

```markdown
---
name: faircode-frappe-development
description: >-
  Use when writing or modifying code for a Faircode ERPNext/Frappe customisation
  — DocTypes, controllers, hooks, whitelisted APIs, reports, background jobs.
  Triggers on implementing an assigned task, "write the code for", "add a field",
  "hook into save", "create an endpoint". Enforces Frappe methods, no
  copy-paste-from-chat, and no over-engineering.
---

# Faircode Frappe Development

This is a guard-rail skill. Follow it exactly; it overrides the urge to ship fast.

## Before writing code (checklist — make a todo per item)
- [ ] Read the task's acceptance criteria. If missing, STOP → `faircode-task-breakdown`.
- [ ] Confirm the right Frappe mechanism for the job (see
      `shared/references/frappe-methods.md`). For framework mechanics, load the
      upstream `frappe-app-dev` skill.
- [ ] Confirm this is the simplest solution that meets the AC (YAGNI).
- [ ] Start a branch per `shared/references/git-conventions.md`.

## While writing code
- Use framework methods (`frappe.get_doc`, `frappe.qb`, hooks, `@frappe.whitelist`).
- No raw SQL or hand-rolled HTTP where a framework method exists.
- No abstractions for a single use case. Match surrounding code style.
- Pair with `faircode-test-driven-development`: failing test FIRST.

## STOP — red flags (you are rationalizing)
| Thought | Reality |
| --- | --- |
| "I'll paste this snippet from chat, it looks right" | You must understand every line. Re-derive it with framework methods or don't use it. |
| "Raw SQL is faster to write" | Use `frappe.qb`/`frappe.db.get_value`. Raw SQL needs a written reason in the PR. |
| "Let me add a service layer / generic engine" | YAGNI. Solve the actual task. |
| "I'll skip the test, it's simple" | Simple things break. Test first. |
| "ignore_permissions=True makes it work" | Justify it in the PR or fix the permission model. |

## Definition of Done
See `shared/references/definition-of-done.md`. All 8 items must hold before you
mark the task complete.

> Next: `faircode-test-driven-development` (in parallel), then
> `faircode-git-workflow` and `faircode-cicd-guardrails`.
```

- [ ] **Step 2: Wire into marketplace.json** — append `"./skills/faircode-frappe-development"`.

- [ ] **Step 3: Run the structure validator**

Run: `python -m pytest tests/test_plugin_structure.py -v`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add skills/faircode-frappe-development .claude-plugin/marketplace.json
git commit -m "feat: faircode-frappe-development guard-rail skill"
```

---

### Task 8: `faircode-test-driven-development` skill

**Files:**
- Create: `skills/faircode-test-driven-development/SKILL.md`
- Modify: `.claude-plugin/marketplace.json`

**Interfaces:**
- Consumes: `shared/references/definition-of-done.md`.
- Produces: the Frappe-specific TDD discipline.

- [ ] **Step 1: Write SKILL.md**

Create `skills/faircode-test-driven-development/SKILL.md`:

```markdown
---
name: faircode-test-driven-development
description: >-
  Use before writing implementation code for any Faircode Frappe feature or bug
  fix. Triggers on "implement", "fix the bug", "add the feature", or starting an
  assigned ERPNext task. Enforces write-test-first using Frappe's test tooling.
---

# Faircode TDD (Frappe)

Write the test first. Watch it fail. Write minimal code to pass. No exceptions
on real work (throwaway spikes excepted — ask the consultant).

## The loop
1. **Write a failing test** in `<app>/<module>/test_<doctype>.py` using
   `FrappeTestCase`:
   ```python
   from frappe.tests.utils import FrappeTestCase
   import frappe

   class TestCreditLimit(FrappeTestCase):
       def test_blocks_over_limit_sales_order(self):
           so = frappe.get_doc({"doctype": "Sales Order", ...})
           with self.assertRaises(frappe.ValidationError):
               so.insert()
   ```
2. **Run it, watch it fail** for the RIGHT reason:
   `bench --site <site> run-tests --module <app>.<module>.test_<doctype>`
   Expected: fail (feature not implemented) — not an import/typo error.
3. **Write minimal code** in the controller/hook to pass. Nothing extra.
4. **Run tests, watch them pass.**
5. **Refactor** with tests green. **Commit** (test + code together).

## Each acceptance criterion = at least one test
Map every AC from the task to a named test. If an AC has no test, it is not done.

## STOP — red flags
| Thought | Reality |
| --- | --- |
| "I'll write the test after the code" | Then you're testing what you wrote, not the requirement. Test first. |
| "I didn't see it fail but it's fine" | If you didn't watch it fail, you don't know it tests anything. |
| "Too simple to test" | Write the one-line test. It takes seconds. |

## Definition of Done
- One+ test per acceptance criterion, all green.
- Tests committed alongside the code.
- Part of the CI gate (see `faircode-cicd-guardrails`).

> Next: `faircode-cicd-guardrails` ensures these tests run on every push.
```

- [ ] **Step 2: Wire into marketplace.json** — append `"./skills/faircode-test-driven-development"`.

- [ ] **Step 3: Run the structure validator**

Run: `python -m pytest tests/test_plugin_structure.py -v`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add skills/faircode-test-driven-development .claude-plugin/marketplace.json
git commit -m "feat: faircode-test-driven-development skill"
```

---

### Task 9: `faircode-cicd-guardrails` skill + CI templates (GitHub + GitLab)

**Files:**
- Create: `skills/faircode-cicd-guardrails/SKILL.md`
- Create: `skills/faircode-cicd-guardrails/templates/github/erpnext-ci.yml`
- Create: `skills/faircode-cicd-guardrails/templates/gitlab/.gitlab-ci.yml`
- Modify: `.claude-plugin/marketplace.json`
- Test: `tests/test_ci_templates.py`

**Interfaces:**
- Consumes: nothing at runtime; templates are dropped into target app repos.
- Produces: ready-to-use CI for both platforms enforcing lint + tests + coverage.

- [ ] **Step 1: Write the failing test**

Create `tests/test_ci_templates.py`:

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "skills" / "faircode-cicd-guardrails" / "templates"

def test_github_template_runs_tests_and_coverage():
    y = (TPL / "github" / "erpnext-ci.yml").read_text()
    assert "run-tests" in y
    assert "coverage" in y.lower()
    assert "ruff" in y or "flake8" in y

def test_gitlab_template_runs_tests_and_coverage():
    y = (TPL / "gitlab" / ".gitlab-ci.yml").read_text()
    assert "run-tests" in y
    assert "coverage" in y.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_ci_templates.py -v`
Expected: FAIL (templates missing).

- [ ] **Step 3: Write the templates + SKILL.md**

Create `skills/faircode-cicd-guardrails/templates/github/erpnext-ci.yml`:

```yaml
name: erpnext-ci
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mariadb:
        image: mariadb:10.6
        env: { MYSQL_ROOT_PASSWORD: root }
        ports: ["3306:3306"]
      redis:
        image: redis:7
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - name: Lint
        run: pip install ruff && ruff check .
      - name: Bench init & install app
        run: |
          pip install frappe-bench
          bench init --skip-redis-config-generation --frappe-branch version-15 frappe-bench
          cd frappe-bench
          bench new-site test.localhost --admin-password admin --mariadb-root-password root --no-mariadb-socket
          bench get-app "$GITHUB_WORKSPACE" && bench --site test.localhost install-app "$(basename $GITHUB_WORKSPACE)"
      - name: Run tests with coverage
        run: |
          cd frappe-bench
          bench --site test.localhost run-tests --app "$(basename $GITHUB_WORKSPACE)" --coverage
      - name: Enforce coverage threshold
        run: |
          cd frappe-bench
          coverage report --fail-under=70
```

Create `skills/faircode-cicd-guardrails/templates/gitlab/.gitlab-ci.yml`:

```yaml
stages: [lint, test]
variables:
  MYSQL_ROOT_PASSWORD: root
lint:
  stage: lint
  image: python:3.11
  script:
    - pip install ruff
    - ruff check .
test:
  stage: test
  image: python:3.11
  services:
    - mariadb:10.6
    - redis:7
  script:
    - pip install frappe-bench
    - bench init --skip-redis-config-generation --frappe-branch version-15 frappe-bench
    - cd frappe-bench
    - bench new-site test.localhost --admin-password admin --mariadb-root-password root --no-mariadb-socket
    - bench get-app "$CI_PROJECT_DIR" && bench --site test.localhost install-app "$CI_PROJECT_NAME"
    - bench --site test.localhost run-tests --app "$CI_PROJECT_NAME" --coverage
    - coverage report --fail-under=70
  coverage: '/TOTAL.+?(\d+\%)/'
```

Create `skills/faircode-cicd-guardrails/SKILL.md`:

```markdown
---
name: faircode-cicd-guardrails
description: >-
  Use when setting up or fixing CI/CD for a Faircode Frappe app repo, or when
  asked to "lock quality", "add CI", "require tests before merge", or enforce
  coverage. Ships ready GitHub Actions and GitLab CI templates and the branch-
  protection rules that stop unreviewed/untested code reaching main.
---

# Faircode CI/CD Guard-rails

This is the layer that makes quality non-optional. Skills advise; CI enforces.

## Setup checklist (make a todo per item)
- [ ] Pick the platform: GitHub → copy `templates/github/erpnext-ci.yml` to the
      app repo's `.github/workflows/`. GitLab → copy
      `templates/gitlab/.gitlab-ci.yml` to the repo root.
- [ ] Adjust `--frappe-branch` and the coverage threshold (default 70%) to the
      project. Never lower without sign-off.
- [ ] Turn on branch protection / merge-request rules on `main`:
      - require the CI job to pass,
      - require ≥1 review approval,
      - disallow direct pushes to `main`.
- [ ] Verify a failing test actually blocks the PR/MR (open a throwaway PR).

## What CI enforces
1. Lint (`ruff`).
2. Frappe tests (`bench run-tests`).
3. Coverage threshold (`--fail-under`).
(Browser/e2e smoke is added in Phase 3.)

## STOP — red flags
| Thought | Reality |
| --- | --- |
| "Merge now, CI is red but it's unrelated" | Red is red. Fix or revert. |
| "Lower the coverage gate to pass" | Needs sign-off. Add tests instead. |
| "Push straight to main, it's urgent" | Branch protection exists for urgent moments too. |

## Definition of Done
- CI file committed to the app repo and green on a real PR/MR.
- Branch protection active on `main`.
- A deliberately failing test was shown to block merge.
```

- [ ] **Step 4: Wire into marketplace.json** — append `"./skills/faircode-cicd-guardrails"`.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_ci_templates.py tests/test_plugin_structure.py -v`
Expected: PASS (CI template assertions + structure validator).

- [ ] **Step 6: Commit**

```bash
git add skills/faircode-cicd-guardrails .claude-plugin/marketplace.json tests/test_ci_templates.py
git commit -m "feat: faircode-cicd-guardrails skill with GitHub+GitLab templates"
```

---

### Task 10: Secret hygiene, env example, and full-suite validation

**Files:**
- Create: `.env.example`
- Modify: `README.md` (add token-rotation note)
- Test: full suite run

**Interfaces:**
- Produces: a clean, fully-green pilot ready to publish.

- [ ] **Step 1: Create `.env.example`**

```
# Copy to .env (gitignored) and fill in. Never commit real values.
FAIRCODE_ERP_URL=https://erp.faircode.co
FAIRCODE_ERP_TOKEN=your_api_key:your_api_secret
```

- [ ] **Step 2: Add rotation note to README.md**

Append:

```markdown
## Security note

The legacy `tracker/fetch.py` had a hardcoded ERPNext API token. That token must
be **rotated** in ERPNext (deactivate the old key/secret, issue a new one) and
supplied only via `FAIRCODE_ERP_TOKEN`. Treat the old token as compromised.
```

- [ ] **Step 3: Run the full test suite**

Run: `python -m pytest -v`
Expected: PASS — all tests across structure, references, ERPNext read/write, and CI templates green.

- [ ] **Step 4: Verify no secret leaked**

Run: `python -m pytest tests/test_plugin_structure.py::test_no_hardcoded_token -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .env.example README.md
git commit -m "chore: env example and token-rotation note; pilot complete"
```

---

## Self-Review

**Spec coverage (pilot scope):**
- Plugin + marketplace packaging → Task 1. ✓
- Shared read+safe-write ERPNext helper, token from env → Tasks 2–3. ✓
- Shared references → Task 4. ✓
- Orchestrator + pilot skills (task-breakdown, frappe-development, TDD, cicd-guardrails) → Tasks 5–9. ✓
- Dual GitHub/GitLab CI → Task 9. ✓
- Guard-rail skills carry checklist + red-flags + DoD → Tasks 7, 8, 9 (and task-breakdown). ✓
- Token rotation / no hardcoded secrets → Tasks 1 (scan), 3 (env auth), 10. ✓
- Phases 2–4 skills (discovery, blueprint, comms, full testing, release, governance) are intentionally OUT of this pilot plan per the spec's rollout section.

**Placeholder scan:** No TBD/TODO left in steps; all code and markdown content is concrete. The `repository` URL and coverage threshold (70%) are real defaults flagged in Global Constraints for the owner to confirm.

**Type consistency:** `ERPNextClient` constructor, `get_list`, `_request`, `_opener`, `_confirm`, `_safe_post`, `create_task`/`add_comment`/`file_bug` signatures are consistent between Tasks 2, 3 and their tests. Frontmatter `name:` equals folder name for all five skills, enforced by `tests/test_plugin_structure.py`.
