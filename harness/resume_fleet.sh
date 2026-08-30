#!/usr/bin/env bash
# ONE COMMAND to bring the paused fleet back. Run it and nothing else.
#
#     ./harness/resume_fleet.sh              # resume
#     ./harness/resume_fleet.sh --dry-run    # show what would happen, change nothing
#
# Order matters and is enforced here, not left to the operator:
#   1. extend every deadline by the MEASURED pause duration, uniformly, and record it
#   2. deliver one identical INBOX note per replicate
#   3. reset the restart counters (append-only marker)
#   4. clear the stop files -- until this happens a relaunched loop exits immediately
#   4b. deliver the prepared escalation answers (fleet-uniform + rep01 Rev 21) and close the rows
#   5. relaunch each replicate THROUGH THE CORRECTED PATH: its own id, its own phase,
#      and stamp_deadline.py now idempotent so the launch PRESERVES the extended deadline
#   6. clear the pause record LAST, and only on full success, so a partial resume leaves the
#      restart watcher stood down rather than half-arming it against a half-up fleet
set -uo pipefail
cd "$(dirname "$0")/.."
DRY=""; [ "${1:-}" = "--dry-run" ] && DRY=1

[ -f harness/state/PAUSE.json ] || { echo "not paused (no harness/state/PAUSE.json) -- nothing to resume"; exit 1; }
REPS=$(python3 -c "import json;print(' '.join(json.load(open('harness/state/PAUSE.json'))['replicates']))")
echo "=== RESUME: $(echo "$REPS" | wc -w | tr -d ' ') replicates ==="

if [ -n "$DRY" ]; then
  echo "  (dry-run) would extend deadlines, notify, reset counters, clear stops, relaunch:"
  echo "    $REPS"
  python3 - <<'PY'
import json, sys
from datetime import datetime, timezone, timedelta
sys.path.insert(0, 'harness')
from resume_fleet import FAULT_RESTORATION
r=json.load(open('harness/state/PAUSE.json'))
p=datetime.fromisoformat(r['paused_at_utc'])
now=datetime.now(timezone.utc)
secs=(now-p).total_seconds(); h=secs/3600
print(f"    paused at:    {p.isoformat()}")
print(f"    now:          {now.isoformat()}")
print(f"    pause so far: {h:.4f} h -- this is what every deadline would gain, uniformly")
if FAULT_RESTORATION:
    print()
    print("    PLUS verified-harness-fault restoration (PI standing rule 2026-08-30),")
    print("    which is NOT uniform because the rule keys on cause, not on identity:")
    for rep, fr in FAULT_RESTORATION.items():
        print(f"      {rep}: +{fr['hours']:.4f} h  [{fr['ruling']}]")
        print(f"        measurement: {fr['measured']}")
print()
print("    projected deadlines (KST):")
for rep in r['replicates']:
    fr = FAULT_RESTORATION.get(rep)
    extra = 3600.0*fr['hours'] if fr else 0.0
    nd = datetime.fromisoformat(r['deadlines_at_pause_kst'][rep]) + timedelta(seconds=secs+extra)
    tail = f"   (+{fr['hours']:.2f} h restored)" if fr else ""
    print(f"      {rep}: {r['deadlines_at_pause_kst'][rep][:19]} -> {nd.isoformat()[:19]}{tail}")
PY
  exit 0
fi

# 1-3. deadline extension, INBOX notes, counter reset. Aborts as a whole if anything mismatches.
python3 harness/resume_fleet.py || { echo "!! resume aborted -- fleet left PAUSED, nothing relaunched"; exit 1; }

# 4. clear the stop files.
for R in $REPS; do rm -f "harness/sessions/$R.stop"; done
echo "  stop files cleared"

# 4b. deliver the prepared escalation answers BEFORE relaunching, so the notices are already in
#     INBOX.md when each agent boots and reads it, rather than arriving mid-turn.
python3 harness/deliver_escalation_answers.py || echo "  !! escalation delivery reported errors -- see above"

# 5. relaunch, per replicate, in its own phase.
FAILED=""
for R in $REPS; do
  PH=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(C.phase_of('$R'))")
  PHASE="$PH" ./harness/launch_sessions.sh "$R" >/dev/null 2>&1
  if screen -ls 2>/dev/null | grep -q "rep-$R"; then echo "  $R: up"; else echo "  $R: LAUNCH FAILED"; FAILED="$FAILED $R"; fi
done

# 6. clear the pause record only if every replicate came back.
if [ -n "$FAILED" ]; then
  echo "!! not resumed cleanly:$FAILED"
  echo "   harness/state/PAUSE.json LEFT IN PLACE -- restart watcher stays stood down. Investigate."
  exit 1
fi
mv harness/state/PAUSE.json "harness/state/PAUSE.resumed.$(date -u +%Y%m%dT%H%M%SZ).json"
echo "  pause record retired; restart watcher re-armed"
echo "=== RESUMED CLEANLY ==="
