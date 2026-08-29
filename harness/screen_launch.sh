#!/usr/bin/env bash
# Reference-screen launcher. Pre-positioned 2026-08-29; executes only after the final collection.
#
# THE WRITE BARRIER IS THE FIRST THING THIS SCRIPT DOES, and it is a refusal rather than a check:
# the collection gate runs before any directory is created, any file is transferred, or any job is
# submitted, so the script cannot write a byte to the cluster until every replicate has been
# collected and attested. Sealed plan section 7.
#
#   ./harness/screen_launch.sh --check     # gate only, report readiness, touch nothing
#   ./harness/screen_launch.sh --go        # gate, then stage and submit wave 1
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:---check}"
SCREEN_ROOT="/home1/users/Bei/screen"
CONC_MAX=480          # PI revision 2026-08-29, post-collection
CONC_BACKOFF=240      # sustained third-party queueing

say() { printf '  %s\n' "$*"; }

# --- 1. collection gate ------------------------------------------------------------------
IDS=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(' '.join(C.RATIFIED['phases']['main']['ids']))")
MISSING=""
for R in $IDS; do
  [ -s "reps/main/collected/$R/REPORT.md" ] || MISSING="$MISSING $R"
done
[ -s "reps/main/collected/COLLECTION.md" ] || MISSING="$MISSING COLLECTION.md"
if [ -n "$MISSING" ]; then
  say "REFUSED — the screen may not run before the last collection completes."
  say "missing:$MISSING"
  say "Nothing was created, transferred or submitted."
  exit 3
fi
say "collection gate PASSED — all 16 replicates collected and attested"

# --- 2. deck integrity -------------------------------------------------------------------
BAD=$( (cd screen/decks && shasum -a 256 -c ../deck_manifest.sha256 2>/dev/null | grep -cv ': OK$') || true )
TOT=$(grep -c . screen/deck_manifest.sha256)
say "decks verified $((TOT-BAD)) / $TOT"
[ "$BAD" -eq 0 ] || { say "REFUSED — $BAD deck(s) fail their pre-registered hash"; exit 4; }

if [ "$MODE" != "--go" ]; then
  say "check-only: gate and decks verified, nothing touched. Re-run with --go to launch."
  exit 0
fi

# --- 3. stage and submit wave 1 ----------------------------------------------------------
say "staging to $SCREEN_ROOT"
ssh -o BatchMode=yes dirac-bei "mkdir -p $SCREEN_ROOT/decks $SCREEN_ROOT/runs $SCREEN_ROOT/logs"
rsync -a screen/decks/ "dirac-bei:$SCREEN_ROOT/decks/"
scp -q screen/deck_manifest.sha256 prereg/stage0_sample.SEALED.json "dirac-bei:$SCREEN_ROOT/"
say "submitting wave 1 at concurrency ceiling $CONC_MAX (back-off $CONC_BACKOFF)"
python3 harness/screen_submit.py --wave 1 --max-concurrent "$CONC_MAX" --backoff "$CONC_BACKOFF"
