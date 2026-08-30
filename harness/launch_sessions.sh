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
[ "${1:-}" = "--dry-run" ] && { DRY=1; shift; }

# Replicate list: explicit arguments win, otherwise the phase's roster from config.py. This was
# `s01 s02` inline, which cannot express a one-replicate gate or a wave.
REPS="$*"
if [ -z "$REPS" ]; then
  REPS=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(' '.join(C.RATIFIED['phases']['$PHASE']['ids']))")
fi
echo "  replicates:$REPS"

for REP in $REPS; do
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
  # Deadline is stamped HERE, at launch, not at provisioning -- "launch + N h exactly" (Rev 20).
  # Reading a provision-time deadline would silently shorten every wave by its own queue time.
  DEADLINE=$(python3 harness/stamp_deadline.py "$REP" | tail -1)
  # Register as ACTIVE before starting. poll.sh reads this file instead of a hardcoded list --
  # it was `s01 s02` inline, so after the smoke it would have polled two dead workspaces and
  # reported a healthy fleet while the live one ran unwatched. That is SI-012's failure wearing
  # different clothes: the watchdog running, on the wrong subject.
  grep -qx "$REP" harness/state/active_replicates 2>/dev/null || echo "$REP" >> harness/state/active_replicates
  # macOS ships screen 4.00.03 (2006), which has no -Logfile. Start screen FROM the session
  # directory instead, so its `-L` log (screenlog.0) lands there and the two replicates do not
  # collide on one file in the repo root.
  #
  # THE SESSION MUST OUTLIVE ITS LAUNCHER. restart_watch.sh runs inside study.poll.service, which
  # is Type=oneshot and therefore takes systemd's default KillMode=control-group: a screen started
  # from it lives in the POLL's cgroup and is killed the moment the poll finishes. That is how
  # thirty restarts died on 2026-08-30 -- each about twenty seconds after starting, each leaving a
  # transcript that stops mid-orientation and a loop log with no exit line, and each charged to a
  # restart counter that then hit its cap of 3 and left ten replicates down for twelve hours.
  # REPORT 006 section 2(b); `systemd-run --user --scope` ratified by the PI 2026-08-31.
  #
  # A transient scope is its OWN unit. It is not in the caller's cgroup and does not die with it.
  # Verified on this host both ways: a screen started through a scope from inside a oneshot unit
  # outlives that unit; started directly from the same place it does not.
  #
  # This lives here rather than in restart_watch.sh on purpose. Every launch path -- restart,
  # resume, first launch, a hand-run relaunch -- goes through this line, and the property wanted
  # is "a replicate session outlives whatever started it", which is a property of launching and
  # not of restarting. Guarded, not assumed: a host without a systemd user manager (the retired
  # macOS laptop) has no systemd-run, and this must not become the next thing that works on
  # exactly one machine.
  if command -v systemd-run >/dev/null 2>&1 && systemctl --user show-environment >/dev/null 2>&1; then
    ( cd "$CWD" && systemd-run --user --scope --quiet \
        --description="replicate session $REP" \
        screen -dmS "$SESSION" -L \
        "$LOOP" "$REP" "$WS" "$MODEL" "$DEADLINE" )
  else
    ( cd "$CWD" && screen -dmS "$SESSION" -L \
        "$LOOP" "$REP" "$WS" "$MODEL" "$DEADLINE" )
  fi
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
# The roster that was actually launched, never a phase literal. This read `rep-s0`, a smoke-era
# filter: launch sixteen main replicates successfully and the summary still printed "(none)".
# Third of the family the record has now fixed twice (collect.sh's two-workspace glob,
# restart_watch.sh's defaulted smoke roster) -- a smoke-era literal left in a main-phase path,
# reporting against the wrong subject while looking like it worked.
SESSION_RE="$(printf 'rep-%s|' $REPS | sed 's/|$//')"
echo "sessions:"; printf '%s\n' "$(screen -ls 2>/dev/null || true)" | grep -E "$SESSION_RE" || echo "  (none)"
exit $FAILED
