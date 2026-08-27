#!/usr/bin/env bash
# Launch the two smoke replicate sessions.
#
# Host placement: this machine. The cluster head runs CentOS 7.6 / glibc 2.17 and cannot run
# Node 18+, which Claude Code requires; see prereg/replicate_runtime_spec.md section 1.
# Persistence: GNU screen (tmux is not installed here).
#
# The bootstrap prompt is IDENTICAL for both replicates. The only difference between arms is
# the charter each was provisioned with -- that is the whole treatment, and any difference in
# the prompt would confound it.
set -uo pipefail
cd "$(dirname "$0")/.."
MODEL="claude-opus-5"
ROOT="$PWD"
# Interaction mode is chosen BY PHASE, not globally (PI ruling 2026-08-28).
#   smoke -> session_loop.sh          (interactive TUI; the mode the smoke was measured in)
#   main  -> session_loop_headless.sh (`-p`; no TUI, so no modal can block -- SI-006/SI-011)
# The smoke is running as this is written, so session_loop.sh is deliberately left untouched:
# editing a bash script that a live process is still reading is its own way to lose a campaign.
PHASE="${PHASE:-smoke}"
case "$PHASE" in
  smoke) LOOP="$ROOT/harness/session_loop.sh" ;;
  main)  LOOP="$ROOT/harness/session_loop_headless.sh" ;;
  *) echo "unknown PHASE '$PHASE' (expected smoke|main)" >&2; exit 2 ;;
esac
[ -x "$LOOP" ] || { echo "session loop not executable: $LOOP" >&2; exit 2; }
echo "  phase=$PHASE  loop=$(basename "$LOOP")"
FAILED=0
DRY=""
[ "${1:-}" = "--dry-run" ] && DRY=1

for REP in s01 s02; do
  WS="/home1/users/Bei/ws/$REP"
  SESSION="rep-$REP"
  LOG="harness/sessions/$REP.loop.log"
  # Each session gets its OWN local working directory, so Claude Code writes its transcripts
  # to a distinct ~/.claude/projects/<encoded-cwd>/ per replicate. Sharing one cwd would put
  # both replicates' usage records in the same directory and make per-session token
  # attribution guesswork -- which is exactly the number the main-run budget is priced from.
  CWD="$PWD/harness/sessions/$REP"
  mkdir -p "$CWD"
  # Claude Code loads CLAUDE.md from its LOCAL cwd (and parents), not from the remote
  # workspace. The workspace copy is the governed record; this copy is the one that actually
  # reaches the model. Both are byte-identical and both arms get the same file.
  cp harness/replicate_CLAUDE.md "$CWD/CLAUDE.md"
  PROMPT="$(cat harness/replicate_prompt.md)
Your workspace_root is: $WS"
  printf '%s' "$PROMPT" > "harness/sessions/$REP.prompt"

  if [ -n "$DRY" ]; then
    echo "=== $REP (dry-run) ==="
    echo "  screen -dmS $SESSION -L -Logfile $LOG \\"
    if [ "$PHASE" = "main" ]; then
      echo "    claude --model $MODEL --settings harness/replicate_settings.json -p <prompt>   [headless]"
    else
      echo "    claude --model $MODEL --settings harness/replicate_settings.json <prompt>"
    fi
    echo "  workspace: $WS"
    echo "  local cwd: $CWD"
    echo "  transcripts: ~/.claude/projects/$(echo "$CWD" | sed 's|/|-|g')/"
    echo "  prompt bytes: $(printf '%s' "$PROMPT" | wc -c | tr -d ' ')"
    echo "  loop: $(basename "$LOOP") re-invokes with --continue until the deadline"
    continue
  fi

  if printf '%s' "$(screen -ls 2>/dev/null || true)" | grep -q "$SESSION"; then
    echo "  $REP: session already running, skipping"
    continue
  fi
  DEADLINE=$(python3 -c "import json;from datetime import datetime;print(int(datetime.fromisoformat(json.load(open('/dev/stdin'))['deadline_kst']).timestamp()))" < <(ssh -o BatchMode=yes -o ConnectTimeout=20 dirac-bei "cat $WS/WORKSPACE.json"))
  # macOS ships screen 4.00.03 (2006), which has no -Logfile. Start screen FROM the session
  # directory instead, so its `-L` log (screenlog.0) lands there and the two replicates do not
  # collide on one file in the repo root.
  ( cd "$CWD" && screen -dmS "$SESSION" -L \
      "$LOOP" "$REP" "$WS" "$MODEL" "$DEADLINE" )
  UP=0
  for i in $(seq 1 10); do
    sleep 1
    if printf '%s' "$(screen -ls 2>/dev/null || true)" | grep -q "$SESSION"; then UP=1; break; fi
  done
  if [ "$UP" -eq 0 ]; then
    echo "  $REP: LAUNCH FAILED -- no screen session '$SESSION'"; FAILED=1; continue
  fi
  # A live screen session proves nothing: the first launch sat blocked on an interactive
  # settings dialog for 40 minutes with the session "up". Proof of life is the agent WRITING
  # A TRANSCRIPT. Wait for one, and fail loudly if it never appears.
  TDIR="$HOME/.claude/projects/$(echo "$CWD" | sed 's|/|-|g')"
  # Proof of life is GROWTH, not existence. On a first launch the directory is empty so
  # "a transcript appeared" is proof; on a RESTART the previous transcript is already there,
  # and this check passed instantly against the dead session's own bytes -- it reported the
  # blocked replicate as "launched and WORKING" using the byte count of the file that proved
  # it was stuck. Baseline first, then require the total to exceed it. (SI-006)
  BASE=$(cat "$TDIR"/*.jsonl 2>/dev/null | wc -c | tr -d " "); BASE=${BASE:-0}
  OK=0
  for i in $(seq 1 30); do
    NOW_B=$(cat "$TDIR"/*.jsonl 2>/dev/null | wc -c | tr -d " "); NOW_B=${NOW_B:-0}
    if [ "$NOW_B" -gt "$BASE" ]; then OK=1; break; fi
    sleep 4
  done
  if [ "$OK" -eq 1 ]; then
    B=$(cat "$TDIR"/*.jsonl 2>/dev/null | wc -c | tr -d " ")
    echo "  $REP: launched and WORKING (screen '$SESSION', transcript $BASE -> $B bytes)"
  else
    echo "  $REP: LAUNCH FAILED -- session up but no transcript after 120s (blocked on a prompt?)"
    screen -S "$SESSION" -X hardcopy "/tmp/stuck_$REP.txt" 2>/dev/null
    echo "       screen contents captured to /tmp/stuck_$REP.txt"
    FAILED=1
  fi
done

echo
echo "sessions:"; printf '%s\n' "$(screen -ls 2>/dev/null || true)" | grep -E 'rep-s0' || echo "  (none)"
exit $FAILED
