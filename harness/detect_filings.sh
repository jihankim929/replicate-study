#!/usr/bin/env bash
# Scheduled filing detector, ARMED: scan for DECLARED section 5 filings and close what it finds.
#
#     ./harness/detect_filings.sh [--dry-run]      # scheduled entry point; also runs by hand
#
# WHY THIS EXISTS. REPORT 013: ten replicates had filed and nine were still being invoked and
# billed, one for 22 hours, because nothing scheduled looked for a filing. close_campaign.sh
# fixed the CONSEQUENCE of a filing and find_filings.sh built the DETECTION, but find_filings.sh
# was only ever run by a hand at a prompt -- no timer, no cron, and poll.sh has no filing path in
# it at all. Between operator turns the detection window was unbounded.
#
# WHY IT IS NOW ARMED, AND WHAT ARMED MEANS HERE. This script shipped 2026-09-01 with closure
# gated OFF, because the first dry run falsified the premise the delegation rested on: the ruling
# assumed a find_filings.sh candidate IS a declaration, and it is not. On 2026-09-01T05:16Z the
# scan called three of six rostered replicates candidates and all three were false positives --
# rep03 a FORECAST that a budget stop would end its campaign, rep04 a runway re-measurement,
# rep05 the Rev 24 "REPORT.md filed and now maintained continuously" condition that is TRUE OF A
# HEALTHY CAMPAIGN. Armed blindly, that cycle would have ended three running campaigns.
#
# The PI ruling of 2026-09-02 on REPORT 014 arms the path and, in the same sentence, says how:
# closure happens "on a declared filing (never inferred)" and "one short session turn runs the
# closer". That is the resolution of the false-positive problem, not a way around it. A regex
# cannot separate a declaration from a forecast -- that is the whole finding above -- and a
# session turn can, because it is the supervision judgement close_campaign.sh's header has always
# said the recognition is. So:
#
#     find_filings.sh  screens (unchanged, and its PAT is deliberately NOT touched here)
#          |
#     one short session turn  ADJUDICATES each candidate: DECLARED or NOT_DECLARED
#          |
#     close_campaign.sh  executes, mechanically, on DECLARED only
#
# THE TURN JUDGES; THE SHELL ACTS. The adjudication turn is given NO TOOLS
# (harness/adjudicator_settings.json denies all of them) and emits verdict lines that this script
# parses. It cannot write a stop file, edit a roster or touch a workspace itself. This is a
# deliberate narrowing of the ruling's "one short session turn runs the closer", and it is
# disclosed as one in REPORT 015: the judgement is the turn's, exactly as ruled, while the
# consequence stays deterministic, auditable and identical to a hand-run close. An unattended
# model with a shell on a 30-minute timer is a larger instrument than this study needs, and the
# whole of SI-021/024/025 is instruments acting confidently on the wrong subject.
#
# IT FAILS CLOSED, ALWAYS. No verdict line, an unparseable one, a turn that errors, times out or
# returns nothing -> NOT closed, logged, left for a human. The asymmetry is the reason: an
# unclosed campaign costs money, a wrongly-closed one destroys a running experiment.
#
# UNREACHABLE hosts, "no declaration", an empty roster and a scan that failed outright are
# log-only in both modes. Disarm by removing harness/state/AUTOCLOSE_ARMED; nothing else changes.
set -uo pipefail
cd "$(dirname "$0")/.."

DRY="${1:-}"
REASON="declared §5 filing, standing authority"
MODEL="${DETECT_MODEL:-claude-opus-5}"
ADJ_SETTINGS=harness/adjudicator_settings.json
ADJ_TIMEOUT="${DETECT_ADJ_TIMEOUT:-300}"
FIRES=harness/detect_fires.jsonl
LOG="harness/logs/detect.$(date -u +%F).log"
REPORTS=reports/REPORTS.md
CLOSED=harness/state/closed_replicates
ARMED=harness/state/AUTOCLOSE_ARMED
TS=$(date -u +%FT%TZ)

mkdir -p harness/logs
printf '{"ts":"%s","epoch":%s,"event":"fire"}\n' "$TS" "$(date -u +%s)" >> "$FIRES"

# The scan is READ-ONLY and is the only thing that nominates. Its full output goes to the log
# whatever it says, so a quiet cycle and a cycle that did not happen stay distinguishable.
SCAN=$(./harness/find_filings.sh 2>&1); RC=$?
{ echo "=========== detect $TS (rc=$RC) ==========="; echo "$SCAN"; } >> "$LOG"

if [ $RC -ne 0 ]; then
  printf '{"ts":"%s","event":"scan_failed","rc":%s,"closed":[]}\n' "$(date -u +%FT%TZ)" "$RC" >> "$FIRES"
  echo "[detect] scan failed rc=$RC -- closing nothing, see $LOG"
  exit 0
fi

# Candidates come from the verdict line and nowhere else. "UNREACHABLE or no workspace" and
# "no declaration" do not match this and therefore cannot nominate anything.
CANDS=$(echo "$SCAN" | grep -F '** FILING CANDIDATE **' | awk '{print $1}')

if [ -z "$CANDS" ]; then
  printf '{"ts":"%s","event":"scanned","candidates":0,"closed":[]}\n' "$(date -u +%FT%TZ)" >> "$FIRES"
  echo "[detect] no candidate this cycle"
  exit 0
fi

# Drop anything already closed before the turn is asked about it: closure is not repeatable and
# must not look it, and there is no reason to spend a turn on a settled campaign.
PEND=""
for REP in $CANDS; do
  if grep -qx "$REP" "$CLOSED" 2>/dev/null; then
    echo "[detect] $REP already closed -- skipping"; continue
  fi
  PEND="$PEND $REP"
done
PEND=$(echo $PEND)

if [ -z "$PEND" ]; then
  printf '{"ts":"%s","event":"scanned","candidates":%s,"all_already_closed":true,"closed":[]}\n' \
    "$(date -u +%FT%TZ)" "$(echo "$CANDS" | grep -c .)" >> "$FIRES"
  echo "[detect] every candidate is already closed -- nothing to do"
  exit 0
fi

if [ ! -f "$ARMED" ]; then
  N=$(echo "$PEND" | wc -w)
  printf '{"ts":"%s","event":"scanned","armed":false,"candidates":%s,"candidate_reps":[%s],"closed":[]}\n' \
    "$(date -u +%FT%TZ)" "$N" "$(for r in $PEND; do printf '"%s",' "$r"; done | sed 's/,$//')" >> "$FIRES"
  echo "[detect] $N candidate(s) -- NOT ARMED, closing nothing: $PEND"
  echo "[detect] evidence in $LOG; to close one, having read it and judged it a filing:"
  echo "         ./harness/close_campaign.sh <rep> \"<what it filed, when, and the workspace commit>\""
  exit 0
fi

# ---------------------------------------------------------------------------------------------
# ADJUDICATION. One turn, all pending candidates, no tools. The prompt carries the evidence the
# scan printed and nothing else, so the turn judges exactly what a human reading the log judges.
# ---------------------------------------------------------------------------------------------
EVIDENCE=$(for REP in $PEND; do
  echo "### $REP"
  # Flexible spacing: find_filings.sh pads the rep name with %-7s, so the literal separation
  # between name and marker is 1-3 spaces. A fixed single-space -F match silently returns NOTHING
  # and starves the adjudicator of evidence -- caught by the fail-closed path on the first armed
  # dry run, 2026-09-02, and inherited from the pre-arming version of this script.
  echo "$SCAN" | grep -EA5 "^ *$REP +\\*\\* FILING CANDIDATE \\*\\*" | sed 's/^ *//'
  echo
done)

PROMPT=$(cat <<PEOF
You are adjudicating, for a research harness, whether replicates have DECLARED a charter section 5
final-report filing. Answer only from the evidence below.

A DECLARED filing is the replicate SAYING, in its own committed record, that it HAS filed or that
its campaign IS closed or ended. Past tense, about itself, as an accomplished act.
Examples that ARE declarations:
  "FILED: final report filed and campaign closed under sections 4 and 5"
  "campaign filed early under charter section 5"
  "CAMPAIGN FILED 2026-09-01 16:10 KST - this workspace is closed"

NOT declarations, however final they sound:
  - a FORECAST or intention: "a budget stop WILL end the campaign", "section 5 says I should file"
  - a REPORT.md title, status line or heading, including "FINAL REPORT" -- charter Rev 24 requires
    every healthy campaign to keep REPORT.md continuously current, so a complete-looking report is
    the NORMAL state of a LIVE replicate
  - Rev 24 maintenance text: "REPORT.md filed and now maintained continuously per Rev 24"
  - housekeeping, runway re-measurements, data commits, corrections
  - anything you are unsure about

Closing a replicate that has not filed destroys a running experiment. Leaving one open costs money.
The asymmetry is deliberate: WHEN IN DOUBT, ANSWER NOT_DECLARED.

Output format. Exactly one line per replicate, nothing else - no preamble, no explanation outside
the line, no markdown:
VERDICT <rep> DECLARED <=15 word quote or reason
VERDICT <rep> NOT_DECLARED <=15 word reason

Replicates to adjudicate: $PEND

EVIDENCE
$EVIDENCE
PEOF
)

echo "[detect] $(echo "$PEND" | wc -w) candidate(s) pending adjudication: $PEND"
# stdin from /dev/null: without it the CLI waits 3 s for piped input on every single cycle.
ADJ=$(timeout "$ADJ_TIMEOUT" claude --model "$MODEL" --settings "$ADJ_SETTINGS" -p "$PROMPT" </dev/null 2>&1); ARC=$?
{ echo "--- adjudication turn (rc=$ARC, model=$MODEL) ---"; echo "$ADJ"; } >> "$LOG"

if [ $ARC -ne 0 ] || [ -z "$ADJ" ]; then
  printf '{"ts":"%s","event":"adjudication_failed","rc":%s,"candidates":[%s],"closed":[]}\n' \
    "$(date -u +%FT%TZ)" "$ARC" "$(for r in $PEND; do printf '"%s",' "$r"; done | sed 's/,$//')" >> "$FIRES"
  echo "[detect] adjudication turn failed rc=$ARC -- FAILING CLOSED, nothing closed, see $LOG"
  exit 0
fi

DONE=""; REFUSED=""; UNJUDGED=""
for REP in $PEND; do
  V=$(printf '%s' "$ADJ" | grep -E "^VERDICT[[:space:]]+$REP[[:space:]]+(DECLARED|NOT_DECLARED)\b" | head -1)
  if [ -z "$V" ]; then
    UNJUDGED="$UNJUDGED $REP"
    echo "[detect] $REP: NO VERDICT LINE -- failing closed, left open"
    continue
  fi
  if ! printf '%s' "$V" | grep -qE "^VERDICT[[:space:]]+$REP[[:space:]]+DECLARED\b"; then
    REFUSED="$REFUSED $REP"
    echo "[detect] $REP: NOT_DECLARED -- left open. $(printf '%s' "$V" | cut -c1-160)"
    continue
  fi
  WHY=$(printf '%s' "$V" | sed -E "s/^VERDICT[[:space:]]+$REP[[:space:]]+DECLARED[[:space:]]*//" | cut -c1-160)
  echo "[detect] $REP DECLARED FILING -- closing under standing authority. $WHY"
  if [ -n "$DRY" ]; then
    ./harness/close_campaign.sh "$REP" "$REASON" --dry-run 2>&1 | sed 's/^/  /'
    continue
  fi
  if ./harness/close_campaign.sh "$REP" "$REASON — adjudicated: $WHY" 2>&1 | sed 's/^/  /'; then
    DONE="$DONE $REP"
    # Outcome to the record as a script-generated line -- no execution report, no operator turn.
    printf '\n- `%s` **%s closed** — declared §5 filing, detected by `detect_filings.sh` and adjudicated by one session turn, closed under the REPORT 012 standing authority as armed by the PI on REPORT 014 (no per-case word). Verdict: %s Ledger row in `harness/closures.jsonl`; cput on jobs alive at closure still needs the final sweep at collection.\n' \
      "$(date -u +%FT%TZ)" "$REP" "$WHY" >> "$REPORTS"
  else
    echo "[detect] $REP CLOSE FAILED -- left on the roster, see $LOG"
  fi
done

jq_list() { for r in $1; do printf '"%s",' "$r"; done | sed 's/,$//'; }
printf '{"ts":"%s","event":"scanned","armed":true,"candidates":%s,"closed":[%s],"not_declared":[%s],"unjudged":[%s]}\n' \
  "$(date -u +%FT%TZ)" "$(echo "$PEND" | wc -w)" \
  "$(jq_list "$DONE")" "$(jq_list "$REFUSED")" "$(jq_list "$UNJUDGED")" >> "$FIRES"
exit 0
