#!/usr/bin/env bash
# Scheduled filing detector: scan for DECLARED section 5 filings and close what it finds.
#
#     ./harness/detect_filings.sh [--dry-run]      # scheduled entry point; also runs by hand
#
# WHY THIS EXISTS. REPORT 013: ten replicates had filed and nine were still being invoked and
# billed, one for 22 hours, because nothing scheduled looked for a filing. close_campaign.sh
# fixed the CONSEQUENCE of a filing and find_filings.sh built the DETECTION, but find_filings.sh
# was only ever run by a hand at a prompt -- no timer, no cron, and poll.sh has no filing path in
# it at all. Between operator turns the detection window was unbounded. This closes it.
#
# WHAT AUTHORISES THE CLOSE, AND WHY IT IS GATED OFF. find_filings.sh's header states the
# standing position: recognising a filing is a supervision judgement, "a human runs the closer".
# The operator ruling of 2026-09-01 delegates that judgement to this script for a DECLARED filing
# -- no page, no per-case word, reason "declared section 5 filing, standing authority".
#
# That delegation is installed here but NOT ARMED, because the first dry run falsified the
# premise it rests on. The ruling assumes a find_filings.sh candidate IS a declaration. It is not.
# On 2026-09-01T05:16Z the scan called three of six rostered replicates candidates and all three
# were false positives:
#
#   rep03  "REPORT reframed from interim draft to FINAL, because spend passed 84 percent against
#          a hard stop at 100 and charter section 5 ..."   -- a FORECAST that a budget stop will
#          end the campaign. find_filings.sh names this exact commit in its own closing note as
#          the thing that is not a filing, and reports/REPORTS.md already records "rep03 not
#          closed -- it has not filed and the inference was refused".
#   rep04  a runway re-measurement from 2026-08-31 04:34, not a filing in any reading; last
#          commit 2026-09-01 13:53, mid-campaign.
#   rep05  "REPORT.md filed and now maintained continuously per Rev 24" -- the Rev 24
#          continuously-current condition, which is TRUE OF A HEALTHY CAMPAIGN and is the precise
#          case close_campaign.sh's header rules out as a trigger.
#
# All three were live, two had committed within the hour. Armed, this timer would have written
# three stop files at :15 and ended three running campaigns, one of them against a standing
# operator refusal. PAT is a SCREEN, not a verdict -- find_filings.sh says so in the line "A
# candidate is EVIDENCE, not a verdict", and a screen tuned to miss no filing necessarily admits
# forecasts and maintenance notes.
#
# So the detection runs unattended and the closing does not:
#
#     * every cycle scans, logs, and records candidates -- the 22-hour blind window REPORT 013
#       billed for is closed to 30 minutes whatever else is true;
#     * closure is ARMED ONLY by the presence of state/AUTOCLOSE_ARMED, which is absent, and
#       should stay absent until find_filings.sh separates a declaration from a forecast well
#       enough that a candidate can carry the ruling's word "declared";
#     * anything short of that is LOGGED AND NOTHING ELSE.
#
# The declaration test is NOT re-derived here. When armed, this script closes on find_filings.sh's
# own verdict line and no other signal, so the one place a filing is defined stays the one place
# it is defined. Widening OR tightening the trigger is a change to find_filings.sh, reviewed as
# such, never a change here. UNREACHABLE hosts, "no declaration", an empty roster and a scan that
# failed outright are log-only in both modes.
set -uo pipefail
cd "$(dirname "$0")/.."

DRY="${1:-}"
REASON="declared §5 filing, standing authority"
FIRES=harness/detect_fires.jsonl
LOG="harness/logs/detect.$(date -u +%F).log"
REPORTS=reports/REPORTS.md
CLOSED=harness/state/closed_replicates
ARMED=harness/state/AUTOCLOSE_ARMED
TS=$(date -u +%FT%TZ)

mkdir -p harness/logs
printf '{"ts":"%s","epoch":%s,"event":"fire"}\n' "$TS" "$(date -u +%s)" >> "$FIRES"

# The scan is READ-ONLY and is the only thing that decides. Its full output goes to the log
# whatever it says, so a quiet cycle and a cycle that did not happen stay distinguishable.
SCAN=$(./harness/find_filings.sh 2>&1); RC=$?
{ echo "=========== detect $TS (rc=$RC) ==========="; echo "$SCAN"; } >> "$LOG"

if [ $RC -ne 0 ]; then
  printf '{"ts":"%s","event":"scan_failed","rc":%s,"closed":[]}\n' "$(date -u +%FT%TZ)" "$RC" >> "$FIRES"
  echo "[detect] scan failed rc=$RC -- closing nothing, see $LOG"
  exit 0
fi

# Candidates come from the verdict line and nowhere else. "UNREACHABLE or no workspace" and
# "no declaration" do not match this and therefore cannot close anything.
CANDS=$(echo "$SCAN" | grep -F '** FILING CANDIDATE **' | awk '{print $1}')

if [ -z "$CANDS" ]; then
  printf '{"ts":"%s","event":"scanned","candidates":0,"closed":[]}\n' "$(date -u +%FT%TZ)" >> "$FIRES"
  echo "[detect] no declared filing this cycle"
  exit 0
fi

if [ ! -f "$ARMED" ]; then
  # Detection without closure. This is the default and the reason is in the header.
  N=$(echo "$CANDS" | grep -c .)
  printf '{"ts":"%s","event":"scanned","armed":false,"candidates":%s,"candidate_reps":[%s],"closed":[]}\n' \
    "$(date -u +%FT%TZ)" "$N" "$(for r in $CANDS; do printf '"%s",' "$r"; done | sed 's/,$//')" >> "$FIRES"
  echo "[detect] $N candidate(s) -- NOT ARMED, closing nothing: $(echo "$CANDS" | tr '\n' ' ')"
  echo "[detect] evidence in $LOG; to close one, having read it and judged it a filing:"
  echo "         ./harness/close_campaign.sh <rep> \"<what it filed, when, and the workspace commit>\""
  exit 0
fi

DONE=""
for REP in $CANDS; do
  # Belt and braces on top of the roster drop: closure is not repeatable and must not look it.
  if grep -qx "$REP" "$CLOSED" 2>/dev/null; then
    echo "[detect] $REP already closed -- skipping"; continue
  fi
  EV=$(echo "$SCAN" | grep -A4 -F "$REP ** FILING CANDIDATE **" | tail -n +2 | sed 's/^ *//' | head -4 | tr '\n' ' ')
  echo "[detect] $REP DECLARED FILING -- closing under standing authority"
  if [ -n "$DRY" ]; then
    ./harness/close_campaign.sh "$REP" "$REASON" --dry-run 2>&1 | sed 's/^/  /'
    continue
  fi
  if ./harness/close_campaign.sh "$REP" "$REASON" 2>&1 | sed 's/^/  /'; then
    DONE="$DONE $REP"
    # Outcome to the record as a script-generated line -- no execution report, no session turn.
    printf '\n- `%s` **%s closed** — declared §5 filing detected by `detect_filings.sh`, closed under the REPORT 012 standing authority (no per-case word). Evidence: %s Ledger row in `harness/closures.jsonl`; cput on jobs alive at closure still needs the final sweep at collection.\n' \
      "$(date -u +%FT%TZ)" "$REP" "${EV:-see $LOG}" >> "$REPORTS"
  else
    echo "[detect] $REP CLOSE FAILED -- left on the roster, see $LOG"
  fi
done

printf '{"ts":"%s","event":"scanned","candidates":%s,"closed":[%s]}\n' \
  "$(date -u +%FT%TZ)" "$(echo "$CANDS" | grep -c .)" \
  "$(for r in $DONE; do printf '"%s",' "$r"; done | sed 's/,$//')" >> "$FIRES"
exit 0
