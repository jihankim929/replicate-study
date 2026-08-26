#!/usr/bin/env bash
# Bridge the watchdog to a REMOTE workspace.
#
# Until now nothing ran the watchdog against a live replicate. poll.sh's own header claimed a
# watchdog step it did not have, watchdog.py was only ever exercised against local mock
# workspaces in dryrun_loop.sh, and the workspaces themselves live on the cluster. The
# campaign has therefore been running with no budget enforcement and no liveness enforcement
# of any kind. Charter section 4's caps and section 5's forced filing cannot fire from code
# that is never called.
#
# Same shape as escalate_remote.sh: pull the files the checker needs, run the tested logic
# unchanged, push INBOX.md back only if it actually changed.
set -uo pipefail
cd "$(dirname "$0")/.."
REP="${1:?usage: watchdog_remote.sh <repid>}"
WS="/home1/users/Bei/ws/$REP"
TMP="${TMPDIR:-/tmp}/bei-wd-$REP"
rm -rf "$TMP"; mkdir -p "$TMP"

for f in WORKSPACE.json usage.json INBOX.md; do
  scp -q "dirac-bei:$WS/$f" "$TMP/$f" 2>/dev/null || true
done
[ -s "$TMP/WORKSPACE.json" ] || { echo "[watchdog] $REP: workspace unreachable"; exit 1; }

BEFORE=$(wc -c < "$TMP/INBOX.md" 2>/dev/null | tr -d ' ')
python3 harness/watchdog.py "$TMP" --no-isolation
RC=$?
AFTER=$(wc -c < "$TMP/INBOX.md" 2>/dev/null | tr -d ' ')

if [ "${AFTER:-0}" != "${BEFORE:-0}" ]; then
  scp -q "$TMP/INBOX.md" "dirac-bei:$WS/INBOX.md" && echo "[watchdog] $REP: notice delivered to the cluster inbox"
fi
rm -rf "$TMP"
exit $RC
