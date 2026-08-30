#!/usr/bin/env bash
# Restart-on-death watcher (spec section 3).
#
# Restarts a replicate whose TRANSCRIPT HAS STOPPED GROWING and whose screen session is gone.
#
# PI ruling 2026-08-27: death detection moved off heartbeat staleness. The heartbeat is a
# proxy written by a wrapper and it failed on its own -- 14.5 hours stale on a replicate whose
# agent was working the whole time. Under the old rule that replicate was one dead screen
# session away from being restarted while healthy. Transcript growth is the agent's own record
# of its own work and cannot go stale while the agent acts. The heartbeat is still reported
# below as evidence about the wrapper; it no longer decides anything.
# Capped at 3 restarts per replicate per campaign: repeated death is a fact about the run,
# and unlimited restarts would hide it. The workspace is NEVER reset -- git record, usage
# counters and running jobs all survive, and the deadline does not move.
set -uo pipefail
cd "$(dirname "$0")/.."
MARKER=harness/.launched
if [ ! -f "$MARKER" ]; then
  echo "  campaign not launched yet (no $MARKER) -- restart watcher idle"
  exit 0
fi
# A DELIBERATE PAUSE IS NOT A DEATH. During a fleet pause every session is down by intent, and
# after STALE_MIN the transcripts go stale too -- which is exactly the signature this watcher
# restarts on. Without this guard the first poll cycle 30 minutes into a pause would relaunch
# all sixteen sessions on an unattended host, against the ruling that stopped them, and the
# deadline extension the pause is owed would then be computed against a fleet that never
# actually paused. The pause record is removed by resume_fleet.sh, not by hand.
if [ -f harness/state/PAUSE.json ]; then
  echo "  FLEET PAUSED (harness/state/PAUSE.json present) -- restart watcher stood down."
  echo "  Sessions are down by ruling, not by failure. Resume with harness/resume_fleet.sh."
  exit 0
fi
MAX_RESTARTS=3
STALE_MIN=30
LEDGER=harness/restarts.jsonl
DRY="${1:-}"

ACTIVE=$(cat harness/state/active_replicates 2>/dev/null | tr '\n' ' ')
[ -n "$ACTIVE" ] || { echo "  no active replicates registered"; exit 0; }
for REP in $ACTIVE; do
  WS="/home1/users/Bei/ws/$REP"; SESSION="rep-$REP"
  ALIVE=$(printf '%s' "$(screen -ls 2>/dev/null || true)" | grep -c "$SESSION" || true)
  # DECIDING signal: minutes since the agent's own transcript last grew. -1 = no transcripts.
  AGE=$(python3 harness/liveness.py "$REP" --age-min --no-update 2>/dev/null)
  AGE=${AGE:--1}
  # REPORTED ONLY: heartbeat age, kept as evidence about the wrapper, not as a criterion.
  HB=$(ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
        "test -f $WS/heartbeat && echo \$(( ( \$(date +%s) - \$(stat -c %Y $WS/heartbeat) ) / 60 )) || echo 99999" 2>/dev/null)
  HB=${HB:-99999}
  # SI-007: this counter was broken two ways and both pushed toward restarting MORE.
  # (1) the ledger is written by printf as "replicate":"s01" -- no space -- and this grep
  #     looked for "replicate": "s01" WITH one, so it never matched and a real restart counted
  #     as zero; (2) `grep -c || echo 0` appends a second 0 on no-match, yielding "0\n0", and
  #     `[ "$N" -ge 3 ]` then EXITS 2 rather than returning false -- which, with no `set -e`,
  #     falls through as though the cap were clear. Tolerate both spacings, swallow grep's
  #     exit status without adding to the value, and force a single integer.
  # SI-022: the cap is counted since the last COUNTER_RESET marker, not over all time. A
  # deliberate fleet pause is not a replicate failure, and a campaign that is resumed must not
  # inherit a cap that was spent before it. The ledger stays APPEND-ONLY -- the reset is a row
  # in it, not a deletion -- so the full restart history is still readable above the marker.
  # SPACING, again. This grep required "event":"COUNTER_RESET" with no space, while json.dumps
  # writes "event": "COUNTER_RESET" with one -- so a reset row written by any Python tool was
  # invisible here and the cap it was meant to clear stayed spent. Same family as SI-007's two
  # counter bugs and as the `"replicate": ?` tolerance three lines below, which is why the fix is
  # the same one: tolerate both spacings rather than dictate a writer. Found while giving effect
  # to the PI's COUNTER_RESET ruling of 2026-08-31, whose row this grep did not match.
  RESET_LN=$(grep -nE '"event": ?"COUNTER_RESET"' "$LEDGER" 2>/dev/null | tail -1 | cut -d: -f1)
  RESET_LN=${RESET_LN:-0}
  N=$(tail -n +$((RESET_LN+1)) "$LEDGER" 2>/dev/null | grep -cE "\"replicate\": ?\"$REP\"" | head -1)
  N=${N:-0}
  case "$N" in (*[!0-9]*|"") N=0 ;; esac
  echo "  $REP: session=$([ "$ALIVE" -gt 0 ] && echo up || echo DOWN) transcript_age=${AGE}min (deciding) heartbeat_age=${HB}min (reported only) restarts=$N/$MAX_RESTARTS"

  if [ "$ALIVE" -gt 0 ]; then continue; fi

  # A DELIBERATELY STOPPED REPLICATE IS NOT A DEAD ONE. session_loop*.sh ends cleanly when
  # harness/sessions/<rep>.stop exists, and that file is how a campaign is ended on purpose --
  # including by the replicate's own right under charter section 5 to file early, which states
  # that early filing ends the campaign. Without this guard the watchdog sees a missing screen,
  # calls it death and relaunches it, so the harness re-opens a campaign the charter says is
  # closed and bills the replicate's spend cap for turns it did not ask for. rep17 filed at
  # 04:20 KST on 2026-08-31 and was re-invoked four times at roughly $5 a turn before this was
  # noticed. Same shape as the PAUSE.json guard above: the watcher must not undo a deliberate
  # stop. Added 2026-08-31.
  if [ -f "harness/sessions/$REP.stop" ]; then
    echo "     stop file present -- campaign deliberately ended, NOT restarting"; continue
  fi
  # The decision is made in liveness.py, which fails safe: it exits 0 ONLY on positive
  # evidence of death. Doing the comparison here in shell arithmetic is what previously let a
  # missing tool or an unparsable number fall through to restarting a live session.
  if ! python3 harness/liveness.py "$REP" --dead-after "$STALE_MIN" --no-update > /dev/null 2>&1; then
    echo "     session gone but no positive evidence of death -- not restarting"; continue
  fi
  if [ "$N" -ge "$MAX_RESTARTS" ]; then
    echo "     !! restart cap reached -- left DOWN deliberately, notify the PI"
    # "notify the PI" is now something this line DOES, not something it says. It printed that
    # instruction 221 times into a log on an unattended host while ten replicates stayed down
    # for twelve hours. The pager exits 0 whatever happens and records its own outcome, so a
    # poll cannot be broken by it and a pager that is not working cannot look like one that is.
    # PI ruling 2026-08-31; REPORT 006 section 7(5).
    ./harness/page_pi.sh "restart-cap-$REP" "$REP is DOWN and out of restarts" <<PAGE || true
$REP has reached the restart cap ($N/$MAX_RESTARTS) and has been left DOWN deliberately.

- transcript age at detection: ${AGE} min
- screen session: absent
- workspace: $WS

The harness will not restart it again without a COUNTER_RESET row in harness/restarts.jsonl.
Its cluster jobs are unaffected and keep running. Its deadline is still moving.

Raised automatically by harness/restart_watch.sh.
PAGE
    continue
  fi
  TS=$(date -u +%FT%TZ)
  echo "     restarting (#$((N+1)))"
  if [ -n "$DRY" ]; then echo "     (dry-run) would relaunch and log"; continue; fi
  # SI-022, the defect this line WAS. It read `./harness/launch_sessions.sh` -- no argument and
  # no PHASE. launch_sessions.sh then defaulted to PHASE=smoke and, with no argument, to the
  # smoke roster `s01 s02`. So a dead MAIN replicate caused s01/s02 to be relaunched, in the
  # interactive TUI mode that SI-006/SI-011 bars from the main run, while this loop charged the
  # restart to the dead replicate's counter and sent it an INBOX notice saying it had been
  # restarted. rep06 died once and was never restarted at all: three cap-consuming "restarts"
  # went to two other replicates. Restart the replicate that actually died, in its own phase.
  REP_PHASE=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(C.phase_of('$REP'))" 2>/dev/null)
  if [ -z "$REP_PHASE" ]; then
    echo "     !! cannot resolve phase for $REP -- NOT restarting"; continue
  fi
  PHASE="$REP_PHASE" ./harness/launch_sessions.sh "$REP" >/dev/null 2>&1
  printf '{"ts":"%s","replicate":"%s","restart_number":%d,"reason":"screen session absent and transcript not grown (%s min)","downtime_min":%s}\n' \
    "$TS" "$REP" "$((N+1))" "$AGE" "$AGE" >> "$LEDGER"
  ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
    "printf '\n## %s — harness notice\n\n- Your session was restarted by the harness (restart %d of %d) after roughly %s minutes with no new activity in its record. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.\n' '$TS' '$((N+1))' '$MAX_RESTARTS' '$AGE' >> $WS/INBOX.md"
done
