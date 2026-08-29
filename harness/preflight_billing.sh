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
#   ./harness/preflight_billing.sh --budget 45000000 --replicates 20   # override the defaults
#
# --budget/--replicates DEFAULT to the ratified main-phase values read from harness/config.py.
# They used to be caller-supplied only, with 40000000 written into this comment: the Rev 16
# token revision (40 M -> 45 M) would have left the gate printing a stale 800,000,000 ceiling
# for a campaign that can now bill 900,000,000. A launch gate whose headline figure is a
# hand-copied literal is a gate that certifies the wrong number.
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

# Defaults come from the ratified config, never from a literal in this file.
if [ -z "$BUDGET" ] || [ -z "$REPS" ]; then
  DEFAULTS=$(python3 -c 'import sys; sys.path.insert(0,"harness"); import config as C; \
print(C.RATIFIED["token_budget"]["main"], len(C.RATIFIED["phases"]["main"]["ids"]))' 2>/dev/null) || DEFAULTS=""
  if [ -n "$DEFAULTS" ]; then
    [ -z "$BUDGET" ] && BUDGET=${DEFAULTS%% *}
    [ -z "$REPS" ]   && REPS=${DEFAULTS##* }
  fi
fi

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

# --- leg 1c: spend headroom >= worst-case fleet remainder, ABSORPTION-CHECKED (S5, 2026-08-29) ---
# Rewritten against the $4,500 limit and the ratified per-replicate spend cap. The assertion is
# not "N x cap <= limit" -- enforcement is POLLED, so the true fleet maximum is
#   N x (cap + peak_spend_rate x poll_interval)
# which is the same overshoot bound SI-012 showed the harness had been asserting falsely for
# compute. Ignoring it here would repeat that mistake with money.
echo "  [3/3] spend headroom >= worst-case fleet remainder (absorption-checked)"
python3 - <<'PYEOF'
import sys
sys.path.insert(0, "harness")
import config as C
R      = C.RATIFIED
N      = R["phases"]["main"]["replicates"]
CAP    = R["spend_usd"]["main"]
LIMIT  = R["monthly_spend_limit_usd"]
POLL   = R["spend_poll_minutes"]
PEAK   = R["spend_peak_usd_per_h"]
ideal  = N * CAP
over   = PEAK * POLL / 60.0
worst  = N * (CAP + over)
print(f"        limit ${LIMIT:,.0f}   cap ${CAP:.0f}/replicate x N={N}")
print(f"        ideal fleet max            : ${ideal:,.0f}  ({100*ideal/LIMIT:.1f}% of limit)")
print(f"        polled-enforcement overshoot: ${over:.2f}/replicate at a {POLL}-min spend poll")
print(f"        WORST CASE                 : ${worst:,.0f}  (headroom ${LIMIT-worst:,.0f})")
if worst <= LIMIT:
    print(f"        PASS -- the plan absorbs into the limit with ${LIMIT-worst:,.0f} to spare")
    sys.exit(0)
need = LIMIT/N - over
print(f"        FAIL -- over by ${worst-LIMIT:,.0f}")
print(f"        absorbs at a per-replicate cap of ${need:.2f}, or a faster spend poll")
sys.exit(1)
PYEOF
[ $? -ne 0 ] && FAIL=1

echo
if [ "$FAIL" -eq 0 ]; then
  echo "== GATE PASSED (all three legs asserted) =="
else
  echo "== GATE FAILED -- do not launch =="
fi
exit "$FAIL"
