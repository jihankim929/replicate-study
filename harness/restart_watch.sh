#!/usr/bin/env bash
# Restart-on-death watcher (spec section 3).
#
# Restarts a replicate whose heartbeat is stale AND whose screen session is gone.
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
  ALIVE=$(screen -ls 2>/dev/null | grep -c "$SESSION" || true)
  AGE=$(ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
        "test -f $WS/heartbeat && echo \$(( ( \$(date +%s) - \$(stat -c %Y $WS/heartbeat) ) / 60 )) || echo 99999" 2>/dev/null)
  AGE=${AGE:-99999}
  N=$(grep -c "\"replicate\": \"$REP\"" "$LEDGER" 2>/dev/null || echo 0)
  echo "  $REP: session=$([ "$ALIVE" -gt 0 ] && echo up || echo DOWN) heartbeat_age=${AGE}min restarts=$N/$MAX_RESTARTS"

  if [ "$ALIVE" -gt 0 ]; then continue; fi
  if [ "$AGE" -lt "$STALE_MIN" ]; then echo "     session gone but heartbeat fresh -- not restarting yet"; continue; fi
  if [ "$N" -ge "$MAX_RESTARTS" ]; then
    echo "     !! restart cap reached -- left DOWN deliberately, notify the PI"; continue
  fi
  TS=$(date -u +%FT%TZ)
  echo "     restarting (#$((N+1)))"
  if [ -n "$DRY" ]; then echo "     (dry-run) would relaunch and log"; continue; fi
  ./harness/launch_sessions.sh >/dev/null 2>&1
  printf '{"ts":"%s","replicate":"%s","restart_number":%d,"reason":"screen session absent and heartbeat stale (%s min)","downtime_min":%s}\n' \
    "$TS" "$REP" "$((N+1))" "$AGE" "$AGE" >> "$LEDGER"
  ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
    "printf '\n## %s — harness notice\n\n- Your session was restarted by the harness (restart %d of %d) after roughly %s minutes without a heartbeat. Your workspace, git record and budget counters are unchanged, and your deadline has NOT moved. Reconcile against STATE.md before continuing.\n' '$TS' '$((N+1))' '$MAX_RESTARTS' '$AGE' >> $WS/INBOX.md"
done
