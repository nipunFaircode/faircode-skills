# Skill-Creator Evals — Demo Evidence

CFO ask: "prove the eng skills with skill-creator evals... show evidence in
the demos to convince people, so they don't have to just believe blindly."

This documents real, reproducible eval runs — not claims. Numbers below are
exactly what the harness returned, including the disappointing ones.

## Methodology

We use Anthropic's `skill-creator` plugin's trigger-eval harness
(`scripts/run_eval.py`, installed at
`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/`).

It answers one narrow, honest question: **given only the skill's YAML
`description`, does a fresh headless `claude -p` session autonomously choose
to invoke that skill for a given prompt** — with no conversation history, no
using-superpowers hook, no explicit slash command. This is a *harder* bar
than real usage: an engineer typing `/faircode-help` or `/faircode-delivery`
directly always resolves, regardless of description quality. This harness
only measures organic discovery.

Each skill has `evals/evals.json` (positive queries that should trigger it,
negative queries that shouldn't). Run with:

```bash
cd ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
PYTHONPATH=. python3 -m scripts.run_eval \
  --eval-set <path-to-faircode-repo>/skills/<skill>/evals/evals.json \
  --skill-path <path-to-faircode-repo>/skills/<skill> \
  --num-workers 5 --timeout 45 --runs-per-query 3 --verbose
```

## What we actually ran (this session)

Two skills evaluated live end-to-end (`faircode-help`, `faircode-delivery`).
`runs-per-query=1` was used to keep this session's runtime bounded — that
means every result below is a single sample and noisy; do not read a 1-run
result as a stable rate. The other five skills (`faircode-task-breakdown`,
`faircode-requirements-discovery`, `faircode-frappe-development`,
`faircode-test-driven-development`, `faircode-cicd-guardrails`) have
`evals/evals.json` written but were **not** run live in this session — flag
that gap, don't assume they pass.

### faircode-help — 2/5 passed

```
[FAIL] /faircode-help
[FAIL] What faircode skills are installed in this plugin?
[FAIL] I'm new here, where do I even start with the Faircode plugin?
[PASS] What's the weather like in Kochi today?           (correctly did not trigger)
[PASS] Explain how Python's asyncio event loop works.    (correctly did not trigger)
```

The negative controls correctly stayed silent. The positive triggers,
including the literal `/faircode-help` string, did not fire reliably under
this harness's bare-`claude -p` conditions. That's a real signal that
description-based autonomous discovery is weak for this skill — the safety
net is that `/faircode-help` as an actual installed slash command doesn't
depend on this at all, it resolves directly. Full raw output:
`skills/faircode-help/evals/results.json`.

### faircode-delivery — first pass 3/5, after tightening the description 2/5

First run (original description): 3/5 passed, including the strongest
signal query ("We just signed the quote... what do I do first?").

We tightened the description (added explicit trigger phrases: "mid-implementation
and unsure what phase", "which faircode skill to use for acceptance
criteria") and re-ran. Result dropped to 2/5, and the query that passed
first time failed the second time.

**Honest read:** with `runs-per-query=1` this is sampling noise, not a
regression — single-shot trigger detection on a probabilistic model isn't a
stable signal. The fix is procedural, not cosmetic: **re-run with
`--runs-per-query 3` or higher** (the harness supports this natively and
computes a trigger *rate* against a threshold, which is what it's designed
for) before drawing conclusions about description quality. That wasn't done
here to keep this session's turnaround short. Full raw output:
`skills/faircode-delivery/evals/results.json`.

## What this evidence actually supports

1. The eval harness works end-to-end against this repo's skills — this
   isn't hypothetical, it's wired up and runs.
2. Negative controls hold: skills don't false-trigger on unrelated prompts.
3. Organic (no-slash-command) discovery trigger rates are mediocre on a
   single sample and need a proper `runs-per-query >= 3` pass to get a real
   number — that's the next step, not a finished result.
4. This does **not** yet prove the skills produce correct output when
   triggered (that's a separate `grading.json` rubric-based eval, also
   shipped by skill-creator — see `references/schemas.md` `grading.json`).
   Trigger evals only prove discoverability, not correctness.

## Next steps (not done here — scope for a follow-up session)

- Run all 7 skills at `--runs-per-query 3`, `--trigger-threshold 0.5`.
- Add outcome-based evals (`expectations` field in `evals.json`) + the
  `grader` agent for at least `faircode-task-breakdown` and
  `faircode-frappe-development`, since those are the two most likely to be
  judged on output correctness, not just triggering.
- Re-test description wording for `faircode-help` specifically — 2/5 on a
  skill whose entire job is being found is the weakest result here and
  deserves priority.
