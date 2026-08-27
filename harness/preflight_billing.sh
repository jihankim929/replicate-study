#!/usr/bin/env bash
# LAUNCH GATE — billing/spend headroom must be proven before any replicate starts.
#
# Why this is a gate and not a check (PI ruling 2026-08-28, SI-006). One smoke replicate hit
# "You've hit your monthly spend limit", was shown an interactive modal, and sat at it for
# 38.6 hours of a 72-hour campaign. Nothing detected it: the screen session was up, the TUI
# kept repainting, and every liveness signal above the TUI reported health. The transcript
# stopped growing, but the restart path gates on the session being gone, so it never fired.
#
# The fix has two legs and this script is the first:
#   1. PRE-VERIFIED HEADROOM -- prove the account can complete a request, and prove the spend
#      limit cannot be reached inside a campaign, BEFORE launching. This script.
#   2. NON-INTERACTIVE INVOCATION -- so that if a limit is somehow reached, the process EXITS
#      rather than drawing a dialog nobody can answer. See prereg/seal_notes.md S5; that leg
#      changes how replicates run and is a PI decision, not a default.
#
# Same class as the permission allow-list: do not detect the dialog, make it unreachable.
#
#   ./harness/preflight_billing.sh              # gate: non-zero exit blocks launch
#   ./harness/preflight_billing.sh --budget 40000000 --replicates 20
set -uo pipefail
cd "$(dirname "$0")/.."

MODEL="claude-opus-5"
BUDGET=""; REPS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --budget) BUDGET="$2"; shift ;;
    --replicates) REPS="$2"; shift ;;
    --model) MODEL="$2"; shift ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

FAIL=0
PROBE_DIR=$(mktemp -d)
trap 'rm -rf "$PROBE_DIR"' EXIT

echo "== launch gate: billing headroom =="

# --- leg 1a: can the account complete a request AT ALL, right now? -----------------------
# The probe runs in a throwaway cwd so it cannot land in a replicate's transcript directory
# and be counted against that replicate's token budget.
echo -n "  [1/3] account can complete a request ... "
OUT=$(cd "$PROBE_DIR" && env -u CLAUDE_CODE_CHILD_SESSION -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT \
        claude --model "$MODEL" -p 'Reply with exactly: HEADROOM_OK' 2>&1 | tr -d '\r')
if printf '%s' "$OUT" | grep -q "HEADROOM_OK"; then
  echo "PASS"
else
  echo "FAIL"
  echo "      response: $(printf '%s' "$OUT" | head -3)"
  echo "      A launch now would put every replicate at the dialog SI-006 describes."
  FAIL=1
fi

# --- leg 1b: does any spend-limit language appear in the probe's own output? --------------
echo -n "  [2/3] no spend-limit language in response ... "
if printf '%s' "$OUT" | grep -qiE "spend limit|usage limit|upgrade your plan|limit to reset"; then
  echo "FAIL"; echo "      matched: $(printf '%s' "$OUT" | grep -ioE 'spend limit|usage limit|upgrade your plan|limit to reset' | head -1)"
  FAIL=1
else
  echo "PASS"
fi

# --- leg 1c: is the configured headroom larger than the campaign can possibly spend? ------
# This one cannot be automated end-to-end: Claude Code exposes no machine-readable spend
# limit. Stating that plainly is the point -- a gate that silently skips its hardest check is
# worse than one that says it needs a human.
echo "  [3/3] configured spend limit exceeds the campaign's maximum possible burn"
if [ -n "$BUDGET" ] && [ -n "$REPS" ]; then
  TOTAL=$(( BUDGET * REPS ))
  printf '        fleet ceiling: %s replicates x %s tokens = %s tokens billable\n' \
    "$REPS" "$(printf "%'d" "$BUDGET" 2>/dev/null || echo "$BUDGET")" \
    "$(printf "%'d" "$TOTAL" 2>/dev/null || echo "$TOTAL")"
else
  echo "        (pass --budget and --replicates to print the fleet ceiling)"
fi
cat <<'NOTE'
        MANUAL CONFIRMATION REQUIRED -- Claude Code exposes no machine-readable spend limit,
        so this leg cannot be asserted from here. Before launch, confirm in the account's
        billing settings that either no monthly spend limit is set, or the limit exceeds the
        figure above with margin. Record the confirmation in prereg/seal_notes.md S5.
NOTE

echo
if [ "$FAIL" -eq 0 ]; then
  echo "== GATE PASSED (legs 1-2 automated; leg 3 requires the manual confirmation above) =="
else
  echo "== GATE FAILED -- do not launch =="
fi
exit "$FAIL"
