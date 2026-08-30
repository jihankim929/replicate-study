#!/usr/bin/env bash
# MAIN-RUN session loop — headless (`-p`). Approved by the PI 2026-08-28.
#
# Identical in intent to session_loop.sh: a single `claude` invocation runs one turn and exits,
# so a campaign is a sequence of them, each resuming the previous with --continue.
#
# THE ONE DIFFERENCE, AND WHY. session_loop.sh runs Claude Code's interactive TUI. In that mode
# an interactive modal can be drawn and will block forever, because nobody is there to answer
# it -- SI-006, where a smoke replicate sat at "You've hit your monthly spend limit" for 38.6
# hours of a 72-hour campaign while its screen session, its heartbeat wrapper and every signal
# above the TUI reported health. Two earlier instances (permission dialog, settings dialog)
# were each fixed as specific dialogs; the class is not enumerable.
#
# In `-p` mode there is no TUI and therefore no modal. A condition that would have drawn one
# instead makes the process EXIT NON-ZERO, which this loop can see, log, escalate and act on.
# That is the structural fix: not detecting the dialog, making it unreachable -- the same shape
# as the permission allow-list.
#
# It is a DELIBERATE APPARATUS DIFFERENCE from the smoke, which ran in TUI mode. Stated as a
# limitation in SI_LEDGER.md SI-011: the smoke's behavioural observations were made under a
# different interaction mode than the main run's, and any smoke-to-main extrapolation of
# behaviour (not of budget arithmetic) inherits that difference.
#
# Runs inside screen. Stops on: deadline reached, stop-file present, repeated hard failure of the
# invocation itself, or a run of sub-minute turns that write NOTHING to the transcript. A run of
# sub-minute turns that DOES write is an agent waiting on the cluster, and backs the inter-turn
# sleep off to ten minutes instead of ending the campaign -- see the guard near the foot of this
# file, and REPORT 006 section 2(a).
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

# Strip every inherited Claude Code environment marker. A child inherits markers such as
# CLAUDE_CODE_CHILD_SESSION which TURN TRANSCRIPT SAVING OFF -- the agent then works perfectly
# and leaves no record, which for a study whose output IS the record is the worst failure
# available. (Same rationale as session_loop.sh; kept here because this script must stand alone.)
for v in $(env | sed -n 's/^\(CLAUDE[A-Za-z0-9_]*\)=.*/\1/p'); do unset "$v"; done

# Heartbeat: a PROGRESS signal, not a liveness signal. It advances only when the agent's own
# transcript has grown -- i.e. when the agent did something. Liveness is decided by
# liveness.py against that same transcript; this is evidence about the wrapper only.
TDIR="$HOME/.claude/projects/$(echo "$CWD" | sed 's|/|-|g')"
ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei "touch $WS/heartbeat" >/dev/null 2>&1
( LAST=""
  while true; do
    SZ=$(cat "$TDIR"/*.jsonl 2>/dev/null | wc -c | tr -d " ")
    if [ "$SZ" != "$LAST" ] && [ -n "$SZ" ] && [ "$SZ" != "0" ]; then
      ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei "touch $WS/heartbeat" >/dev/null 2>&1
      LAST="$SZ"
    fi
    sleep 120
  done ) &
HB=$!
trap 'kill $HB 2>/dev/null' EXIT

# A non-zero exit in headless mode is the signal the TUI used to swallow. It is NOT always
# fatal -- a transient API error should be retried -- so it is backed off and counted, and only
# a run of them stops the campaign. The distinction matters: stopping on the first blip would
# throw away a campaign, and never stopping would spin silently for the whole term, which is
# the failure this mode exists to prevent.
MAX_HARD_FAILS=5
hard=0
i=0; fast=0
SLEEP=10          # inter-turn pause; backs off to IDLE_SLEEP while the agent is correctly idle
IDLE_SLEEP=600
while true; do
  NOW=$(date +%s)
  if [ "$NOW" -ge "$DEADLINE" ]; then
    echo "$(date -u +%FT%TZ) deadline reached, loop ending" >> "$LOG"; break
  fi
  if [ -f "$STOP" ]; then
    echo "$(date -u +%FT%TZ) stop file present, loop ending" >> "$LOG"; break
  fi
  i=$((i+1)); START=$(date +%s)
  BEFORE=$(cat "$TDIR"/*.jsonl 2>/dev/null | wc -c | tr -d " "); BEFORE=${BEFORE:-0}
  echo "$(date -u +%FT%TZ) iteration $i starting (headless)" >> "$LOG"
  if [ "$i" -eq 1 ]; then
    OUT=$(claude --model "$MODEL" --settings "$SETTINGS" -p "$(cat "$PROMPT_FILE")" 2>&1)
  else
    OUT=$(claude --model "$MODEL" --settings "$SETTINGS" --continue -p "$NUDGE" 2>&1)
  fi
  RC=$?; DUR=$(( $(date +%s) - START ))
  AFTER=$(cat "$TDIR"/*.jsonl 2>/dev/null | wc -c | tr -d " "); AFTER=${AFTER:-0}
  echo "$(date -u +%FT%TZ) iteration $i exited rc=$RC after ${DUR}s (transcript ${BEFORE} -> ${AFTER})" >> "$LOG"

  if [ "$RC" -ne 0 ]; then
    hard=$((hard+1))
    printf '%s iteration %d FAILED rc=%d (hard failure %d/%d). first 500 bytes of output:\n%s\n' \
      "$(date -u +%FT%TZ)" "$i" "$RC" "$hard" "$MAX_HARD_FAILS" "$(printf '%s' "$OUT" | head -c 500)" >> "$LOG"
    # A billing/usage limit is the specific condition this mode exists to surface. Say so in
    # the log by name, so the operator reads a cause and not just an exit code.
    if printf '%s' "$OUT" | grep -qiE "spend limit|usage limit|credit balance|upgrade your plan|rate limit"; then
      echo "$(date -u +%FT%TZ) !! ACCOUNT LIMIT REACHED -- see harness/preflight_billing.sh and SI-006" >> "$LOG"
      ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei \
        "printf '\n## %s — harness notice\n\n- The harness could not run your session: an account limit was reached. This is an infrastructure condition, not something you caused or can fix. Your workspace, record and deadline are unchanged.\n' '$(date -u +%FT%TZ)' >> $WS/INBOX.md" >/dev/null 2>&1
    fi
    if [ "$hard" -ge "$MAX_HARD_FAILS" ]; then
      echo "$(date -u +%FT%TZ) $MAX_HARD_FAILS consecutive hard failures, stopping -- this is a fact about the run, not a thing to hide" >> "$LOG"
      break
    fi
    sleep $(( 30 * hard ))       # linear backoff: 30s, 60s, 90s, ...
    continue
  fi
  hard=0

  # A run of sub-minute turns means one of two things, and they are opposites.
  #
  # It can mean the loop is spinning on something broken -- the case this guard was written for.
  # It can also mean the agent has correctly run out of work: everything is queued on the
  # cluster, the charter's own session rhythm says waiting is not working, and each turn is a
  # short honest "nothing has changed, holding". On 2026-08-30 the guard could not tell those
  # apart and ended TEN campaigns of the sixteen for the second one, 44 min to 2 h 23 min after
  # the fleet resumed, while the six that survived were merely the ones inside long turns.
  # rep02's last four turns were "Holding for the next results batch", "Holding.", "Holding."
  # REPORT 006 section 2(a); ruled 2026-08-31.
  #
  # The discriminator is the transcript. A turn that ends in seconds having WRITTEN something is
  # an agent doing its job briefly; a turn that ends in seconds having written nothing is a loop
  # spinning. So growth backs the inter-turn sleep off to ten minutes and says so; no growth
  # still breaks. Backing off rather than resetting the counter matters for cost as well as for
  # noise: five quick turns then a fresh ten seconds is ~24 turns an hour of full re-read
  # context against a spend cap, and ten minutes between turns is ~6.
  if [ "$DUR" -lt 60 ]; then fast=$((fast+1)); else fast=0; SLEEP=10; fi
  if [ "$fast" -ge 5 ]; then
    if [ "$AFTER" -gt "$BEFORE" ]; then
      if [ "$SLEEP" -ne "$IDLE_SLEEP" ]; then
        echo "$(date -u +%FT%TZ) 5 consecutive sub-minute turns WITH transcript growth -- the agent is working and waiting, not spinning; inter-turn sleep ${SLEEP}s -> ${IDLE_SLEEP}s" >> "$LOG"
      fi
      SLEEP="$IDLE_SLEEP"
      fast=4                      # hold the backed-off state; the next fast turn re-evaluates it
    else
      echo "$(date -u +%FT%TZ) 5 consecutive sub-minute turns with NO transcript growth, stopping to avoid a hot loop" >> "$LOG"
      break
    fi
  fi
  sleep "$SLEEP"
done
echo "$(date -u +%FT%TZ) headless session loop for $REP finished after $i iteration(s)" >> "$LOG"
