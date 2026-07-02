# Seat Rollout Verification

CFO ask: confirm all 40 seats are on CLI v2.1.38+ (seats below that silently
get nothing — no error, no plugin), and do a deep check on one test seat.

## What I could and couldn't verify from here

I have no remote access to the 40 engineers' machines — there is no central
registry of seat versions from this repo or this session. What I've done
instead is build `scripts/verify-seat.sh`, tested it on this machine (it
correctly self-reports: CLI 2.1.198 is fine, plugin isn't installed here
since this is the dev box, not a team seat).

## Rollout steps

1. Post `scripts/verify-seat.sh` to the team channel with:
   `curl -fsSL https://raw.githubusercontent.com/nipunFaircode/faircode-frappe/master/scripts/verify-seat.sh | bash`
2. Each of the 40 engineers runs it and reports back: automated pass/fail
   (CLI version + plugin install/enable) plus manual pass/fail on the three
   interactive checks (SessionStart reminder, `/faircode-help` resolves,
   output style).
3. Track results in a simple sheet: seat | CLI version | plugin installed |
   reminder seen | /faircode-help resolves | output style correct.
4. Anyone below v2.1.38 or failing plugin install: `claude update`, then
   re-run.

## Deep check on one test seat — what "pass" looks like

- `claude --version` >= 2.1.38.
- `claude plugin list` shows `faircode@faircode-frappe`, status enabled.
- New session in any project shows a SessionStart line referencing the
  faircode plugin/skills (confirms the reminder hook actually fires, not
  just that the plugin is present).
- `/faircode-help` resolves to the skill list (this only works now because
  `skills/faircode-help/SKILL.md` was added in this same change — it didn't
  exist before, so this check would have failed on every seat until this
  lands).
- Output style: answer-first, no em-dashes, on a real reply.

Until the org-owned repo / marketplace rename PR (#7) is merged and
`autoUpdate` picks it up, seats are still pointed at the old
`nipunFaircode/faircode-skills` marketplace entry — GitHub redirects that
URL to `faircode-frappe` automatically, so `/plugin marketplace add` with
the old URL still works, but seats should be repointed to the new URL once
convenient to avoid depending on GitHub's redirect indefinitely.
