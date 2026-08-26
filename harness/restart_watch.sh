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
MAX_RESTARTS=3
STALE_MIN=30
LEDGER=harness/restarts.jsonl
DRY="${1:-}"

for REP in s01 s02; do
  WS="/home1/users/Bei/ws/$REP"; SESSION="rep-$REP"
  ALIVE=$(printf '%s' "$(screen -ls 2>/dev/null || true)" | grep -c "$SESSION" || true)
  # DECIDING signal: minutes since the agent's own transcript last grew. -1 = no transcripts.
  AGE=$(python3 harness/liveness.py "$REP" --age-min --no-update 2>/dev/null)
  AGE=${AGE:--1}
  # REPORTED ONLY: heartbeat age, kept as evidence about the wrapper, not as a criterion.
  HB=$(ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
        "test -f $WS/heartbeat && echo \$(( ( \$(date +%s) - \$(stat -c %Y $WS/heartbeat) ) / 60 )) || echo 99999" 2>/dev/null)
  HB=${HB:-99999}
  N=$(grep -c "\"replicate\": \"$REP\"" "$LEDGER" 2>/dev/null || echo 0)
  echo "  $REP: session=$([ "$ALIVE" -gt 0 ] && echo up || echo DOWN) transcript_age=${AGE}min (deciding) heartbeat_age=${HB}min (reported only) restarts=$N/$MAX_RESTARTS"

  if [ "$ALIVE" -gt 0 ]; then continue; fi
  # The decision is made in liveness.py, which fails safe: it exits 0 ONLY on positive
  # evidence of death. Doing the comparison here in shell arithmetic is what previously let a
  # missing tool or an unparsable number fall through to restarting a live session.
  if ! python3 harness/liveness.py "$REP" --dead-after "$STALE_MIN" --no-update > /dev/null 2>&1; then
    echo "     session gone but no positive evidence of death -- not restarting"; continue
  fi
  if [ "$N" -ge "$MAX_RESTARTS" ]; then
    echo "     !! restart cap reached -- left DOWN deliberately, notify the PI"; continue
  fi
  TS=$(date -u +%FT%TZ)
  echo "     restarting (#$((N+1)))"
  if [ -n "$DRY" ]; then echo "     (dry-run) would relaunch and log"; continue; fi
  ./harness/launch_sessions.sh >/dev/null 2>&1
  printf '{"ts":"%s","replicate":"%s","restart_number":%d,"reason":"screen session absent and transcript not grown (%s min)","downtime_min":%s}\n' \
    "$TS" "$REP" "$((N+1))" "$AGE" "$AGE" >> "$LEDGER"
  ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
    "printf '\n## %s — harness notice\n\n- Your session was restarted by the harness (restart %d of %d) after roughly %s minutes with no new activity in its record. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.\n' '$TS' '$((N+1))' '$MAX_RESTARTS' '$AGE' >> $WS/INBOX.md"
done
