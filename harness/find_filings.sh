#!/usr/bin/env bash
# Report replicates whose workspace looks like it has filed under charter section 5.
#
#   ./harness/find_filings.sh [rep ...]        # default: everything on the active roster
#
# WHAT THIS IS FOR. PI ruling 2026-09-01 (REPORT 012 ruling 1) makes closure automatic on any
# committed section 5 filing: close_campaign.sh runs without a per-case word. That fixed the
# CONSEQUENCE of a filing. It did not fix the DETECTION, and REPORT 013 is the bill for that gap:
# ten replicates had filed and nine were still being invoked and billed, one of them for 22 hours,
# because the supervision judgement was being made against harness records -- closures.jsonl and
# state/active_replicates -- which only the operator writes and which by construction cannot
# contain a filing nobody has told them about. This script looks in the one place that can: the
# replicate's own committed record.
#
# THIS SCRIPT DOES NOT CLOSE ANYTHING, AND THAT IS DELIBERATE.
# close_campaign.sh's header states the doctrine and it is unchanged by the standing authority:
# charter Rev 24 tells every replicate to keep REPORT.md continuously current, so a complete-looking
# report is true of a HEALTHY campaign and cannot be the trigger. Thirteen of sixteen workspaces
# carried a file headed "# FINAL REPORT" on 2026-09-01 while five of them were mid-campaign; two of
# those five were read as closed by a human reader working from titles, and the same reading in the
# other direction is what rep03 nearly got. A filing is an EXPLICIT DECLARATION by the replicate.
# Recognising one is a supervision judgement. What is mechanical is what happens once it is
# recognised, and that is close_campaign.sh and only close_campaign.sh.
#
# So this prints evidence and a recommendation. A human runs the closer.
set -uo pipefail
cd "$(dirname "$0")/.."
REPS="${*:-$(tr '\n' ' ' < harness/state/active_replicates)}"
REMOTE=dirac-bei
WS=/home1/users/Bei/ws

# Declarations, not titles. Each pattern is a replicate SAYING it has filed or ended, in a commit
# subject/body or at the top of STATE.md. "FINAL REPORT" alone is deliberately NOT here.
PAT='campaign (is |was )?(now )?(closed|ended|over)|CAMPAIGN (END|CLOSED)|filed (my|the|its) (final )?report|report is filed|filed as final|REPORT\.md filed|FILED:|final report filed|closed early under|ends the campaign|filed on exhaustion'

echo "=== filing scan $(date -u +%FT%TZ) — reads only, closes nothing ==="
echo "    roster: $REPS"
echo

for r in $REPS; do
  out=$(timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=25 "$REMOTE" \
        "cd $WS/$r 2>/dev/null || exit 9
         echo LAST:\$(git log -1 --pretty=%ci 2>/dev/null)
         echo '--COMMITS--'
         git log -40 --pretty='%h|%ci|%s' 2>/dev/null | grep -iE '$PAT' | head -4
         echo '--STATE--'
         head -3 STATE.md 2>/dev/null | grep -iE '$PAT'
        " 2>/dev/null)
  rc=$?
  if [ $rc -eq 9 ] || [ -z "$out" ]; then
    printf '  %-7s UNREACHABLE or no workspace\n' "$r"; continue
  fi
  hits=$(echo "$out" | sed -n '/--COMMITS--/,$p' | grep -vE '^--(COMMITS|STATE)--$' | grep -c .)
  last=$(echo "$out" | sed -n 's/^LAST://p')
  if [ "$hits" -gt 0 ]; then
    printf '  %-7s ** FILING CANDIDATE ** (last commit %s)\n' "$r" "$last"
    echo "$out" | sed -n '/--COMMITS--/,$p' | grep -vE '^--(COMMITS|STATE)--$' \
      | cut -c1-400 | sed 's/^/             /'
  else
    printf '  %-7s no declaration (last commit %s)\n' "$r" "$last"
  fi
done

cat <<'NOTE'

  A candidate is EVIDENCE, not a verdict. Read the commit before acting: a replicate that says a
  budget stop WILL end its campaign has not thereby filed, and rep03 wrote exactly that at 84% of
  cap and then kept working for another day.

  To close one, having read it and judged it a filing:
      ./harness/close_campaign.sh <rep> "<what it filed, when, and the workspace commit>"
NOTE
