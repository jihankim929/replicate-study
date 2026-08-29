#!/usr/bin/env bash
# The spend meter runs on its OWN fast cadence, separate from poll.sh's cluster cycle.
# It reads transcripts on this machine -- no ssh, no cluster load -- so a 2-minute tick is free.
# That cadence is load-bearing, not cosmetic: enforcement is polled, so the fleet maximum is
# N x (cap + peak_rate x interval). At the 30-minute cluster cadence the overshoot alone is
# $168 fleet-wide and the $280 cap does NOT fit under the $4,500 limit; at 2 minutes it does.
set -uo pipefail
cd "$(dirname "$0")/.."
FIRES="${HARNESS_STATE_DIR:-harness}/spend_fires.jsonl"
printf '{"ts":"%s","epoch":%s,"event":"fire"}\n' "$(date -u +%FT%TZ)" "$(date -u +%s)" >> "$FIRES"
./harness/meter_spend.py --all >> "harness/logs/spend.$(date -u +%F).log" 2>&1
exit 0
