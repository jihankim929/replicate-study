#!/usr/bin/env bash
# Bridge the escalation router to a REMOTE workspace.
#
# escalate.py operates on a local directory, but under ruling (A) the workspace lives on the
# cluster. Without this bridge a replicate could file escalations forever and nothing would
# ever read them. Pull the two files the router needs, run the tested logic unchanged, push
# the inbox back.
set -uo pipefail
cd "$(dirname "$0")/.."
REP="${1:?usage: escalate_remote.sh <repid>}"
WS="/home1/users/Bei/ws/$REP"
TMP="${TMPDIR:-/tmp}/bei-esc-$REP"
rm -rf "$TMP"; mkdir -p "$TMP"

for f in ESCALATIONS.md WORKSPACE.json INBOX.md; do
  scp -q "dirac-bei:$WS/$f" "$TMP/$f" 2>/dev/null || touch "$TMP/$f"
done
[ -s "$TMP/WORKSPACE.json" ] || { echo "  [escalate] $REP: workspace unreachable"; exit 1; }

BEFORE=$(wc -c < "$TMP/INBOX.md" 2>/dev/null | tr -d ' ')
python3 harness/escalate.py "$TMP"
AFTER=$(wc -c < "$TMP/INBOX.md" 2>/dev/null | tr -d ' ')

if [ "$AFTER" != "$BEFORE" ]; then
  scp -q "$TMP/INBOX.md" "dirac-bei:$WS/INBOX.md" && echo "  [escalate] $REP: inbox updated on the cluster"
fi
rm -rf "$TMP"
