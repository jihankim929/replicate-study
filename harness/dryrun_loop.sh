#!/usr/bin/env bash
# Full-loop dry run: provision -> run -> watchdog -> escalations -> fleet -> collect.
# No cluster, no real agent, no real budget. Proves the loop end to end.
set -uo pipefail
cd "$(dirname "$0")/.."
MOCK="${1:-${TMPDIR:-/tmp}/harness-dryrun.$$}"
rm -rf "$MOCK"; mkdir -p "$MOCK"
rm -f harness/.seen-s01 harness/.seen-s02 harness/escalation_queue.jsonl

echo "########## 1. PROVISION ##########"
./harness/launch.sh --dry-run --dest "$MOCK" --force 2>&1 | grep -Ev '^\[provision\] (DRY|receipt)'

echo; echo "########## 2. REPLICATES RUN (mock, 3 days) ##########"
python3 harness/mock_replicate.py "$MOCK/s01" --days 3 --gated --seed 1
python3 harness/mock_replicate.py "$MOCK/s02" --days 3 --overspend --seed 2

echo; echo "########## 3. WATCHDOG (live against the mock, so notices land in INBOX) ##########"
for R in s01 s02; do python3 harness/watchdog.py "$MOCK/$R" 2>/dev/null; done

echo; echo "########## 4. FLEET CEILING ##########"
python3 harness/watchdog.py --fleet "$MOCK" || echo "  (non-zero exit is the breach signal)"

echo; echo "########## 5. ESCALATIONS ##########"
for R in s01 s02; do python3 harness/escalate.py "$MOCK/$R" 2>/dev/null | grep -v '^\[escalate\] (dry'; done
python3 harness/escalate.py --queue
echo "-- PI delivers one answer --"
python3 harness/escalate.py "$MOCK/s01" --answer "exited 0" --text "Repaired: RASPA exits 0 on fatal input errors. Judge success on a non-empty expected output file, never on exit status."
python3 harness/escalate.py --queue

echo; echo "########## 6. COLLECT ##########"
./harness/collect.sh --dest "$MOCK" --out "$MOCK/collected"

echo; echo "########## 7. WHAT THE REPLICATE SAW ##########"
echo "-- s02 INBOX.md --"; sed -n '1,40p' "$MOCK/s02/INBOX.md"
echo; echo "workspace kept at: $MOCK"
