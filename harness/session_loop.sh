#!/usr/bin/env bash
# Keeps one replicate's campaign alive for its full term.
#
# A single `claude` invocation runs ONE turn and exits. A 3-day campaign is therefore not one
# invocation but a sequence of them, each resuming the previous with --continue so context and
# history carry forward. Without this the "campaign" would end the first time the model
# finished a turn.
#
# Runs inside screen. Stops on: deadline reached, stop-file present, or repeated fast failure.
set -uo pipefail
REP="${1:?rep}"; WS="${2:?workspace}"; MODEL="${3:?model}"; DEADLINE="${4:?deadline epoch}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CWD="$ROOT/harness/sessions/$REP"
SETTINGS="$ROOT/harness/replicate_settings.json"
PROMPT_FILE="$ROOT/harness/sessions/$REP.prompt"
STOP="$ROOT/harness/sessions/$REP.stop"
LOG="$ROOT/harness/sessions/$REP.loop.log"
NUDGE="Continue your campaign. Check INBOX.md for any notices, bring STATE.md up to date, and carry on with your work. Your deadline is unchanged."

cd "$CWD" || exit 1

# Heartbeat: touched every 5 minutes for as long as this loop lives, so a long turn is not
# mistaken for a dead session by the watchdog's 30-minute staleness threshold.
( while true; do
    ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei "touch $WS/heartbeat" >/dev/null 2>&1
    sleep 300
  done ) &
HB=$!
trap 'kill $HB 2>/dev/null' EXIT

i=0; fast=0
while true; do
  NOW=$(date +%s)
  if [ "$NOW" -ge "$DEADLINE" ]; then
    echo "$(date -u +%FT%TZ) deadline reached, loop ending" >> "$LOG"; break
  fi
  if [ -f "$STOP" ]; then
    echo "$(date -u +%FT%TZ) stop file present, loop ending" >> "$LOG"; break
  fi
  i=$((i+1)); START=$(date +%s)
  echo "$(date -u +%FT%TZ) iteration $i starting" >> "$LOG"
  if [ "$i" -eq 1 ]; then
    claude --model "$MODEL" --settings "$SETTINGS" "$(cat "$PROMPT_FILE")"
  else
    claude --model "$MODEL" --settings "$SETTINGS" --continue "$NUDGE"
  fi
  RC=$?; DUR=$(( $(date +%s) - START ))
  echo "$(date -u +%FT%TZ) iteration $i exited rc=$RC after ${DUR}s" >> "$LOG"
  # A turn that ends in seconds, repeatedly, means something is broken -- do not hot-loop.
  if [ "$DUR" -lt 60 ]; then fast=$((fast+1)); else fast=0; fi
  if [ "$fast" -ge 5 ]; then
    echo "$(date -u +%FT%TZ) 5 consecutive sub-minute turns, stopping to avoid a hot loop" >> "$LOG"
    break
  fi
  sleep 10
done
echo "$(date -u +%FT%TZ) session loop for $REP finished after $i iteration(s)" >> "$LOG"
