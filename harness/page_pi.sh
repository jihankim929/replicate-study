#!/usr/bin/env bash
# Page the PI by opening a GitHub issue titled URGENT. Adopted by PI ruling 2026-08-31.
#
# WHY THIS EXISTS. On 2026-08-30 ten of sixteen replicates went down and stayed down for twelve
# hours. The harness detected it correctly and printed
#     !! restart cap reached -- left DOWN deliberately, notify the PI
# 221 times across the polls that followed, into a log file, on an unattended host. There was no
# channel by which it could notify anyone, so a correct detection and a correct instruction sat
# unread for half a day. REPORT 006 sections 0 and 7(5).
#
#   ./harness/page_pi.sh <dedupe-key> <title>          # body on stdin
#
# PROPERTIES IT HAS TO HAVE, and why each one is here rather than assumed:
#
#   NEVER BREAKS THE CALLER. Always exits 0. This is called from inside poll.sh; a pager that
#   can fail a poll would be a monitoring tool that takes down the thing it monitors.
#
#   NEVER PRINTS OR STORES THE CREDENTIAL. The token is read at runtime out of the git remote
#   URL and never written to a file, a log or the console -- the standing rule is that a
#   credential enters neither the repository nor a workspace, and this script is inside the
#   repository. curl gets it on stdin via --config, not on a command line where `ps` would show
#   it. Every response is scrubbed before it is logged.
#
#   DEDUPES, because the condition that pages is usually a condition that persists. One page per
#   key per COOLDOWN_H; the ledger harness/pages.jsonl is the record of what was sent and what
#   was suppressed, so a quiet pager can be told apart from a broken one.
#
#   RECORDS ITS OWN FAILURE AS A FACT. `issues:write` is not on the token as this is written, so
#   the expected result today is a 403 recorded in the ledger. That is the honest state: the
#   pager is installed, wired and inert, and the ledger says so at every fire rather than the
#   harness believing it has a pager it does not have.
set -uo pipefail
cd "$(dirname "$0")/.."
KEY="${1:?dedupe key}"; TITLE="${2:?title}"
LEDGER="${HARNESS_STATE_DIR:-harness}/pages.jsonl"
COOLDOWN_H=6
REPO_SLUG="jihankim929/replicate-study"
TS=$(date -u +%FT%TZ)
BODY=$(cat)

log() { printf '{"ts":"%s","key":"%s","title":%s,"outcome":"%s","detail":%s}\n' \
          "$TS" "$KEY" "$(printf '%s' "$TITLE" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
          "$1" "$(printf '%s' "${2:-}" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()[:400]))')" \
          >> "$LEDGER"; }

# --- dedupe ------------------------------------------------------------------------------
if [ -f "$LEDGER" ]; then
  LAST=$(python3 - "$LEDGER" "$KEY" <<'PY'
import json,sys
from datetime import datetime,timezone
last=None
for line in open(sys.argv[1],errors="replace"):
    try: d=json.loads(line)
    except Exception: continue
    if d.get("key")==sys.argv[2] and d.get("outcome")=="sent":
        last=d.get("ts")
print(last or "")
PY
)
  if [ -n "$LAST" ]; then
    AGE_H=$(python3 -c "
from datetime import datetime,timezone
import sys
t=datetime.fromisoformat('$LAST'.replace('Z','+00:00'))
print((datetime.now(timezone.utc)-t).total_seconds()/3600)")
    if python3 -c "import sys; sys.exit(0 if float('$AGE_H') < $COOLDOWN_H else 1)"; then
      log "suppressed" "last page for this key was ${AGE_H}h ago, inside the ${COOLDOWN_H}h cooldown"
      exit 0
    fi
  fi
fi

# --- credential, at runtime, never stored -------------------------------------------------
URL=$(git config --get remote.origin.url 2>/dev/null || true)
TOKEN=$(printf '%s' "$URL" | sed -n 's|https://\([^@]*\)@github.com/.*|\1|p')
if [ -z "$TOKEN" ]; then
  log "no-credential" "no token in the git remote; cannot page. Falls back to REPORTS.md."
  exit 0
fi

export T="$TITLE" B="$BODY"
PAYLOAD=$(python3 -c 'import json,os;print(json.dumps({"title":"URGENT: "+os.environ["T"],"body":os.environ["B"]}))')
RESP=$(printf 'header = "Authorization: Bearer %s"\n' "$TOKEN" | \
       curl --config - -sS -w '\n%{http_code}' -X POST \
         -H "Accept: application/vnd.github+json" \
         -H "X-GitHub-Api-Version: 2022-11-28" \
         --max-time 30 \
         -d "$PAYLOAD" \
         "https://api.github.com/repos/$REPO_SLUG/issues" 2>&1)
CODE=$(printf '%s' "$RESP" | tail -1)
SCRUB=$(printf '%s' "$RESP" | head -c 400 | sed 's/gh[pous]_[A-Za-z0-9_]*/[redacted]/g; s/github_pat_[A-Za-z0-9_]*/[redacted]/g')
case "$CODE" in
  201) log "sent" "issue created"; echo "  [page] URGENT issue opened: $TITLE" ;;
  403|404) log "forbidden" "HTTP $CODE -- the token lacks issues:write. $SCRUB"
           echo "  [page] NOT SENT (HTTP $CODE, token lacks issues:write): $TITLE" ;;
  *)   log "failed" "HTTP $CODE. $SCRUB"
       echo "  [page] NOT SENT (HTTP $CODE): $TITLE" ;;
esac
exit 0
