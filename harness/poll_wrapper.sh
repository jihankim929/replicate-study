#!/usr/bin/env bash
# SI-012 fix: the scheduled entry point. `poll.sh` states a 10-minute cadence in its header and
# nothing ever ran it -- 2 cycles of an expected 393 across the whole smoke, silent for the last
# 49 h. This wrapper is what launchd invokes, and its first act is to record that it fired, so
# "the poll did not happen" becomes visible instead of indistinguishable from "the poll was quiet".
#
# launchd, NOT cron, and that choice is the fix for the sleep half of the problem: macOS runs a
# missed StartInterval on wake, cron silently drops it. Measured on this host during the smoke:
# 154 sleep transitions, 32.00 h suspended (48.8% of the campaign), 111 stretches longer than the
# poll interval. cron would have dropped 111 cycles.
set -uo pipefail
cd "$(dirname "$0")/.."
FIRES="${HARNESS_STATE_DIR:-harness}/poll_fires.jsonl"
TS="$(date -u +%FT%TZ)"
EPOCH="$(date -u +%s)"
printf '{"ts":"%s","epoch":%s,"event":"fire"}\n' "$TS" "$EPOCH" >> "$FIRES"
./harness/poll.sh >> "harness/logs/poll.$(date -u +%F).log" 2>&1
RC=$?
printf '{"ts":"%s","epoch":%s,"event":"done","rc":%s}\n' "$(date -u +%FT%TZ)" "$(date -u +%s)" "$RC" >> "$FIRES"
exit 0
