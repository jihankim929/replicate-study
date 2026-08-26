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
DRY=""
[ "${1:-}" = "--dry-run" ] && DRY=1

for REP in s01 s02; do
  WS="/home1/users/Bei/ws/$REP"
  SESSION="rep-$REP"
  LOG="harness/sessions/$REP.log"
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
    echo "    claude --model $MODEL --settings harness/replicate_settings.json <prompt>"
    echo "  workspace: $WS"
    echo "  local cwd: $CWD"
    echo "  transcripts: ~/.claude/projects/$(echo "$CWD" | sed 's|/|-|g')/"
    echo "  prompt bytes: $(printf '%s' "$PROMPT" | wc -c | tr -d ' ')"
    continue
  fi

  if screen -ls | grep -q "$SESSION"; then
    echo "  $REP: session already running, skipping"
    continue
  fi
  screen -dmS "$SESSION" -L -Logfile "$LOG" \
    bash -lc "cd '$CWD' && exec claude --model '$MODEL' --settings '$PWD/harness/replicate_settings.json' \"\$(cat '$PWD/harness/sessions/$REP.prompt')\""
  echo "  $REP: launched in screen session '$SESSION' (log: $LOG)"
done

echo
echo "sessions:"; screen -ls 2>/dev/null | grep -E 'rep-s0|Sockets' || echo "  (none)"
