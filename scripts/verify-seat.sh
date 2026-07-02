#!/usr/bin/env bash
# Per-seat verification for the faircode-frappe plugin rollout.
# CFO ask: confirm CLI >= 2.1.38 and that the plugin actually landed on each
# seat — seats below the floor silently get nothing, no error, no plugin.
#
# Run this ON EACH SEAT (not centrally — there is no remote way to check an
# engineer's local Claude Code install). Copy/paste to Slack, or run:
#   curl -fsSL <raw-url-of-this-file> | bash
# once the repo is public/org-owned.

set -uo pipefail

MIN_VERSION="2.1.38"
PLUGIN_NAME="faircode"
FAIL=0

pass() { printf '  \xe2\x9c\x94 %s\n' "$1"; }
fail() { printf '  \xe2\x9c\x98 %s\n' "$1"; FAIL=1; }

version_ge() {
  # returns 0 if $1 >= $2
  [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

echo "== 1. CLI version >= ${MIN_VERSION} =="
if command -v claude >/dev/null 2>&1; then
  RAW_VERSION="$(claude --version 2>&1 | head -n1)"
  VERSION="$(echo "$RAW_VERSION" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n1)"
  if [ -n "$VERSION" ] && version_ge "$VERSION" "$MIN_VERSION"; then
    pass "claude CLI $VERSION (>= $MIN_VERSION)"
  else
    fail "claude CLI is $VERSION — below $MIN_VERSION. Plugin will silently NOT load. Run: claude update"
  fi
else
  fail "claude CLI not found on PATH"
fi

echo "== 2. Plugin installed and enabled =="
LIST_OUT="$(claude plugin list 2>&1)"
if echo "$LIST_OUT" | grep -q "${PLUGIN_NAME}@"; then
  if echo "$LIST_OUT" | grep -A2 "${PLUGIN_NAME}@" | grep -q "enabled"; then
    pass "plugin '${PLUGIN_NAME}' installed and enabled"
  else
    fail "plugin '${PLUGIN_NAME}' installed but NOT enabled — run: claude plugin enable ${PLUGIN_NAME}"
  fi
else
  fail "plugin '${PLUGIN_NAME}' not installed — run: /plugin marketplace add https://github.com/nipunFaircode/faircode-frappe && /plugin install faircode"
fi

echo "== 3. SessionStart reminder + /faircode-help + output style =="
cat <<'EOF'
  These three can only be checked interactively inside a real session:
    a. Start a new `claude` session in this repo (or any project) and
       confirm a faircode reminder line appears at session start.
    b. Type `/faircode-help` and confirm it resolves (lists the installed
       faircode-* skills) instead of erroring as an unknown command.
    c. Confirm the output style is answer-first with no em-dashes — ask
       Claude something and eyeball the reply format.
  Report pass/fail for a., b., c. alongside this script's output.
EOF

echo
if [ "$FAIL" -eq 0 ]; then
  echo "RESULT: PASS (automated checks) — still confirm 3a/3b/3c manually."
else
  echo "RESULT: FAIL — see items above."
fi
