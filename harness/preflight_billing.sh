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

# --- leg 1c: spend headroom >= projected worst-case fleet remainder (S5, PI 2026-08-29) ---
# The spend limit is $3,000 with auto-reload on. This leg is now an ASSERTION, not a note.
#
# It exists because the charter's token cap does NOT bound spend. The ratified metering basis is
# input + output + cache_creation, with cache READS excluded -- and cache reads were 59.2% of the
# smoke's actual bill. A replicate can therefore sit far inside its 45 M cap while billing several
# times what the cap implies. Measured on the collected smoke at list price ($5/$25 per MTok,
# cache-create 1.25x input, cache-read 0.10x input): $20.54/M billable for one arm, $32.54/M for
# the other -- driven by cache-read ratios of 24.8x and 36.3x against billable.
echo "  [3/3] spend headroom >= projected worst-case fleet remainder"
python3 - "$BUDGET" "$REPS" <<'PYEOF'
import sys, json, os
budget, reps = int(sys.argv[1]), int(sys.argv[2])
LIMIT = float(os.environ.get("SPEND_LIMIT_USD", "3000"))
SPENT = float(os.environ.get("SPEND_TO_DATE_USD", "0"))
# $ per MILLION BILLABLE tokens, measured on the collected smoke. Low = the arm with the
# smaller cache-read ratio; high = the larger. Both are list-price, both are measured.
LO, HI = 20.54, 32.54
worst_lo = LO * (budget/1e6) * reps
worst_hi = HI * (budget/1e6) * reps
head = LIMIT - SPENT
print(f"        limit ${LIMIT:,.0f}  spent ${SPENT:,.0f}  headroom ${head:,.0f}")
print(f"        worst-case fleet remainder at N={reps}, each at {budget/1e6:.0f} M billable:")
print(f"          ${worst_lo:,.0f} (low-cache arm) .. ${worst_hi:,.0f} (high-cache arm)")
if head >= worst_hi:
    print("        PASS -- headroom covers the worst case"); sys.exit(0)
if head >= worst_lo:
    print("        FAIL -- headroom covers the low estimate but NOT the high one"); sys.exit(1)
print(f"        FAIL -- headroom is {worst_hi/head:.1f}x short of the worst case")
print(f"        the limit is reached at {100*head/worst_hi:.1f}%-{100*head/worst_lo:.1f}% of the ratified token budget")
print(f"        i.e. after roughly {head/(HI*budget/1e6):.1f}-{head/(LO*budget/1e6):.1f} replicates spend their full budget")
sys.exit(1)
PYEOF
[ $? -ne 0 ] && FAIL=1

echo
if [ "$FAIL" -eq 0 ]; then
  echo "== GATE PASSED (legs 1-2 automated; leg 3 requires the manual confirmation above) =="
else
  echo "== GATE FAILED -- do not launch =="
fi
exit "$FAIL"
