#!/usr/bin/env bash
# Close a replicate's campaign, mechanically and in one place.
#
#   ./harness/close_campaign.sh <rep> "<reason>" [--dry-run]
#
# WHAT A CLOSURE IS. Charter section 5 gives a replicate the right to file its final report early,
# and states that filing ENDS THE CAMPAIGN. Until 2026-08-31 nothing in the harness knew that.
# rep17 filed at 04:20 KST, recorded its campaign closed in its own workspace commit, and was
# re-invoked FOUR TIMES at roughly $5 a turn -- its spend moved 130.75 -> 149.82 with no work
# performed -- because restart_watch.sh saw a missing screen session, called it death, and
# relaunched it. A deliberately ended campaign looked exactly like a dead one.
#
# PI ruling 2026-08-31, ruled generally and not only for rep17: A SECTION 5 FILING DROPS THE
# REPLICATE FROM THE ACTIVE ROSTER MECHANICALLY -- stop-file PLUS roster removal. Two steps, and
# a closure that does one of them is the bug this script exists to make unavailable:
#
#   * stop file alone   -> the loop ends, but poll.sh keeps metering it, the watchdog keeps
#                          reporting a deadline it will never reach, and any hand relaunch
#                          re-adds it to the roster and re-opens the campaign.
#   * roster removal    -> the running loop never sees it and keeps invoking, at full context
#     alone                re-read cost, until the deadline.
#
# WHAT CLOSURE DOES NOT DO, deliberately:
#   * it does not touch the workspace, the git record, usage.json or the deadline stamp;
#   * it does not stop cluster jobs -- a replicate's queued work is its own and keeps running;
#   * it does not remove the replicate from the STUDY. N = 16 is the ratified figure and lives in
#     config.RATIFIED["phases"]["main"]["ids"]; the fleet spend meter reads that, not this roster,
#     so a closed campaign keeps counting toward the fleet cap exactly as its record requires.
#     `active_replicates` is an OPERATIONAL list -- who is still being invoked -- and nothing else.
#
# THE DETECTION IS NOT AUTOMATED, AND THAT IS DELIBERATE. Charter Rev 24 tells every replicate to
# keep REPORT.md continuously current, so "REPORT.md looks complete" is true of a healthy campaign
# and cannot be the trigger. A filing is an explicit declaration by the replicate (rep17's was in
# its escalation and in its commit message); recognising one is a supervision judgement. What is
# mechanical is what HAPPENS once it is recognised, which is this script and all of this script.
set -uo pipefail
cd "$(dirname "$0")/.."
REP="${1:?usage: close_campaign.sh <rep> \"<reason>\" [--dry-run]}"
REASON="${2:?a reason is required -- it goes on the record}"
DRY="${3:-}"
ROSTER=harness/state/active_replicates
CLOSED=harness/state/closed_replicates
LEDGER=harness/closures.jsonl
STOP="harness/sessions/$REP.stop"
TS=$(date -u +%FT%TZ)

grep -qx "$REP" "$ROSTER" 2>/dev/null; ON_ROSTER=$?
[ -f "$STOP" ] && HAD_STOP=yes || HAD_STOP=no
echo "  $REP: on_roster=$([ $ON_ROSTER -eq 0 ] && echo yes || echo no) stop_file=$HAD_STOP"

if [ -n "$DRY" ]; then
  echo "  (dry-run) would write $STOP, drop $REP from $ROSTER, and append to $LEDGER"
  exit 0
fi

# FINAL METER READ BEFORE THE ROSTER DROP. Once off the roster the replicate is no longer polled,
# so this is the last automatic reading its record will get. It is a snapshot, not a total: jobs
# still running at closure keep accruing cput that nothing will harvest afterwards. That gap is
# named in the ledger row rather than papered over -- a final sweep at collection closes it.
./harness/harvest_cput.sh "$REP" 2>&1 | sed 's/^/    /' || echo "    (harvest unreachable)"
./harness/meter_compute.sh "$REP" 2>&1 | sed 's/^/    /' || echo "    (meter unreachable)"
USAGE=$(ssh -o BatchMode=yes -o ConnectTimeout=25 dirac-bei \
        "cat /home1/users/Bei/ws/$REP/usage.json 2>/dev/null" || echo "{}")
USAGE=${USAGE:-\{\}}

printf '%s campaign closed on the record: %s\n' "$TS" "$REASON" >> "$STOP"
if [ $ON_ROSTER -eq 0 ]; then
  # SI-026. `grep -vx` EXITS 1 when it filters out every line, so `&& mv` silently did not run
  # when the replicate being closed was the LAST one on the roster: stop file written, ledger row
  # appended, closed_replicates updated -- and the roster still naming it. It bit exactly once,
  # on rep09, the sixteenth and final closure, 2026-09-02T16:29Z. rc 0 and rc 1 are both success
  # here; anything above 1 is a real grep failure and must NOT be allowed to empty the roster.
  grep -vx "$REP" "$ROSTER" > "$ROSTER.tmp"; GREP_RC=$?
  if [ "$GREP_RC" -le 1 ]; then
    mv "$ROSTER.tmp" "$ROSTER"
  else
    rm -f "$ROSTER.tmp"
    echo "  !! roster filter failed rc=$GREP_RC -- $REP left ON the roster, fix by hand" >&2
  fi
fi
grep -qx "$REP" "$CLOSED" 2>/dev/null || echo "$REP" >> "$CLOSED"

python3 - "$REP" "$TS" "$REASON" "$USAGE" "$HAD_STOP" <<'PY' >> "$LEDGER"
import json, sys
rep, ts, reason, usage, had_stop = sys.argv[1:6]
try: u = json.loads(usage)
except Exception: u = {}
print(json.dumps({
    "ts": ts, "event": "CAMPAIGN_CLOSED", "replicate": rep, "reason": reason,
    "basis": "charter section 5 -- early filing ends the campaign",
    "stop_file_already_present": had_stop == "yes",
    "usage_at_closure": u,
    "note": ("roster removal stops polling: cput still accruing on jobs alive at closure "
             "is not harvested after this row and needs a final sweep at collection"),
}))
PY
echo "  $REP CLOSED -- stop file written, dropped from the active roster, ledger row appended"
echo "  roster now: $(tr '\n' ' ' < "$ROSTER")"
