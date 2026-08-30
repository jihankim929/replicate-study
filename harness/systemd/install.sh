#!/usr/bin/env bash
# Install and enable the study's schedulers on a Linux/systemd supervision host.
#
#     ./harness/systemd/install.sh              # render, enable, start, verify
#     ./harness/systemd/install.sh --verify     # report state only, change nothing
#
# WHY THIS EXISTS. The scheduling layer did not travel. harness/launchd/*.plist are macOS jobs
# with /Users/jihankim/replicate-study hardcoded; bronze4 is Ubuntu and has no launchctl, so on
# a resumed fleet nothing would have scheduled the spend meter and nothing would have scheduled
# poll.sh. That is SI-012 rebuilt on a new host -- the defect that let the watchdog run 2 cycles
# of an expected 393 and cost 2,452 CPU-h past a stop nobody read, and whose recorded fix
# ("launchd, not cron") is a macOS sentence with no referent here.
#
# The repository root is MEASURED, not typed. That is the whole lesson of the plists.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
UNIT_DIR="$HOME/.config/systemd/user"
SRC="$REPO/harness/systemd"
VERIFY=""; [ "${1:-}" = "--verify" ] && VERIFY=1

command -v systemctl >/dev/null 2>&1 || { echo "no systemctl -- this host is not systemd; do not use cron (see poll_wrapper.sh)" >&2; exit 2; }
systemctl --user show-environment >/dev/null 2>&1 || { echo "no systemd USER manager for $USER" >&2; exit 2; }

echo "=== study schedulers ==="
echo "  repo: $REPO"

if [ -z "$VERIFY" ]; then
  mkdir -p "$UNIT_DIR"
  for U in study.spend study.poll; do
    sed "s|@REPO@|$REPO|g" "$SRC/$U.service.in" > "$UNIT_DIR/$U.service"
    cp "$SRC/$U.timer" "$UNIT_DIR/$U.timer"
    echo "  rendered $U.service + $U.timer -> $UNIT_DIR"
  done
  systemctl --user daemon-reload
  systemctl --user enable --now study.spend.timer study.poll.timer >/dev/null 2>&1 \
    || { echo "!! enable failed" >&2; exit 1; }
  echo "  enabled and started"
fi

# LINGER. Without it the user manager stops at logout and both timers die with it -- an
# unattended fleet with no scheduler, which is the condition this file exists to prevent.
LING="$(loginctl show-user "$USER" -p Linger --value 2>/dev/null)"
if [ "$LING" = "yes" ]; then echo "  linger: ENABLED (timers survive logout)"
else echo "  !! linger: $LING -- run: loginctl enable-linger $USER"; fi

# SUSPEND. A host that sleeps is a fleet that stops; Persistent=true catches the missed fire up
# on wake, but not sleeping at all is better. Masking needs root, so this REPORTS rather than
# asserts -- an unverified claim about sleep is what made the launchd choice observed-pending.
echo "  suspend targets:"
for T in sleep.target suspend.target hibernate.target hybrid-sleep.target; do
  S="$(systemctl is-enabled "$T" 2>/dev/null || true)"
  A="$(systemctl is-active "$T" 2>/dev/null || true)"
  printf '    %-20s %s (%s)\n' "$T" "${S:-unknown}" "${A:-unknown}"
done
IDLE="$(systemctl --user show -p IdleAction 2>/dev/null)"
echo "    logind IdleAction: $(grep -E '^\s*IdleAction=' /etc/systemd/logind.conf 2>/dev/null || echo 'ignore (compiled default; not overridden in /etc/systemd/logind.conf)')"

echo "  timers:"
systemctl --user list-timers study.spend.timer study.poll.timer --all --no-pager 2>/dev/null | sed 's/^/    /'
echo
echo "  verify it actually FIRES (SI-012's lesson -- a scheduler nobody observed is not a scheduler):"
echo "    tail -f $REPO/harness/spend_fires.jsonl"
echo "    tail -f $REPO/harness/poll_fires.jsonl"
