#!/usr/bin/env bash
# Transfer a provisioned workspace to the cluster and populate its database THERE.
#
# Why the database is populated on the cluster and not copied from here: the main phase's world
# is 12,499 structures and the fleet is 16 workspaces. Pulling 12,499 files down and pushing
# 200,000 back up is not a sane operation, and it would put a second copy of the frozen world on
# a laptop that has no business holding one. The manifest travels; the structures do not.
#
# What this asserts, on the cluster, before it reports success:
#   * every manifest entry exists in the workspace db/
#   * every one of them matches its frozen SHA-256
#   * the count equals the manifest's count, stated as N/N rather than "OK"
# A partial copy that merely did not error is exactly the failure this exists to prevent.
#
#   ./harness/transfer.sh rep01 [--dest reps/main]
set -euo pipefail
cd "$(dirname "$0")/.."

REP="${1:?usage: transfer.sh <rep_id> [--dest DIR]}"; shift || true
DEST="reps/main"
[ "${1:-}" = "--dest" ] && { DEST="$2"; shift 2; }
LOCAL="$DEST/$REP"
WS="/home1/users/Bei/ws/$REP"
[ -d "$LOCAL" ] || { echo "no such workspace: $LOCAL" >&2; exit 2; }

PHASE=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(C.phase_of('$REP'))")
FROZEN=$(python3 -c "import sys;sys.path.insert(0,'harness');import config as C;print(C.db_source('$PHASE')['dir'])")

echo "=== transfer $REP ($PHASE) -> $WS ==="

# 1. refuse to overwrite a workspace that already has a record in it -----------------------
# "Non-empty" is the wrong test: provision.py writes a LOG.md header, so a transfer that failed
# part-way leaves one behind and the retry refuses itself. The question is not whether LOG.md has
# bytes in it, but whether a REPLICATE has written to it — so compare against the local copy.
REMOTE_LOG=$(ssh -o BatchMode=yes -o ConnectTimeout=30 dirac-bei "cat $WS/LOG.md 2>/dev/null" | shasum -a 256 | cut -d' ' -f1)
LOCAL_LOG=$(shasum -a 256 < "$LOCAL/LOG.md" | cut -d' ' -f1)
EMPTY_LOG=$(printf '' | shasum -a 256 | cut -d' ' -f1)
if [ "$REMOTE_LOG" != "$EMPTY_LOG" ] && [ "$REMOTE_LOG" != "$LOCAL_LOG" ]; then
  echo "  REFUSED: $WS holds a LOG.md a replicate has written to." >&2
  echo "  Remove it deliberately if that is what you mean; this script will not." >&2
  exit 3
fi

# 2. workspace record files (db/ carries only MANIFEST.sha256 and the marker at this point) --
ssh -o BatchMode=yes -o ConnectTimeout=30 dirac-bei "mkdir -p $WS/db"
rsync -a --delete-excluded --exclude '.git/' "$LOCAL/" "dirac-bei:$WS/"
echo "  record files transferred"

# 3. source map: flat workspace name -> path under the frozen world. Kept OUT of the
#    workspace -- it is Bei's routing detail, not the replicate's data.
MAP=$(mktemp)
python3 - "$PHASE" > "$MAP" <<'PY'
import sys; sys.path.insert(0, "harness")
import config as C
src = C.db_source(sys.argv[1])
for line in open(src["manifest"]):
    if line.strip():
        _, rel = line.split(None, 1)
        rel = rel.strip()
        print(f"{rel.split('/')[-1]}\t{rel}")
PY
REMOTE_MAP="/home1/users/Bei/tmp/${REP}.dbmap"
ssh -o BatchMode=yes dirac-bei "mkdir -p /home1/users/Bei/tmp"
scp -q "$MAP" "dirac-bei:$REMOTE_MAP"; rm -f "$MAP"

# 4. populate + verify ON THE CLUSTER -------------------------------------------------------
ssh -o BatchMode=yes -o ConnectTimeout=60 dirac-bei "bash -s" <<REMOTE
set -euo pipefail
# The cluster runs a Korean locale: sha256sum -c prints "<file>: 성공", not "<file>: OK", so a
# tally that greps for OK counts zero on a perfectly good copy. Caught because this script asserts
# N/N and refuses anything less -- a looser check would have reported success either way.
export LC_ALL=C
cd "$WS/db"
n=0
while IFS=\$'\t' read -r flat rel; do
  cp -f "$FROZEN/\$rel" "./\$flat"
  n=\$((n+1))
done < "$REMOTE_MAP"
rm -f "$REMOTE_MAP" POPULATE_REMOTELY
want=\$(grep -c . MANIFEST.sha256)
echo "  populated \$n files (manifest lists \$want)"
[ "\$n" = "\$want" ] || { echo "  COUNT MISMATCH: copied \$n, manifest \$want" >&2; exit 4; }
ok=\$(sha256sum -c MANIFEST.sha256 2>/dev/null | grep -c ': OK\$' || true)
echo "  checksums verified \$ok/\$want"
[ "\$ok" = "\$want" ] || { echo "  CHECKSUM FAILURE: \$ok of \$want verified" >&2; exit 5; }
REMOTE

# 5. toolchain: a Bei-owned pristine copy, verified against its attestation, then read-only ----
# The two smoke workspaces held the only copies; they were confirmed byte-identical over the whole
# campaign (aggregate over RELATIVE paths -- an earlier check hashed absolute paths too and made
# two identical trees look modified), and one was frozen to /home1/users/Bei/toolchain_frozen.
# Main workspaces provision from the frozen copy, never from a sealed replicate workspace.
TC_EXPECT="d79c1ba040dadf095901f3ebfb458af07df9e2404b0fe66ccfb2726b543d5fc1"
# Quoted heredoc + positional args: an unquoted one expanded $(...) on THIS machine, where
# sha256sum does not exist (macOS ships shasum), so the verification ran locally and died.
ssh -o BatchMode=yes -o ConnectTimeout=60 dirac-bei "bash -s" -- "$WS" "$TC_EXPECT" <<'REMOTE'
set -euo pipefail
export LC_ALL=C
WS="$1"; TC_EXPECT="$2"
rm -rf "$WS/toolchain"
mkdir -p "$WS/toolchain"
cp -a /home1/users/Bei/toolchain_frozen/. "$WS/toolchain/"
cd "$WS/toolchain"
got=$(find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -c1-64)
echo "  toolchain aggregate $got"
[ "$got" = "$TC_EXPECT" ] || { echo "  TOOLCHAIN MISMATCH (expected $TC_EXPECT)" >&2; exit 6; }
chmod -R a-w "$WS/toolchain"
echo "  toolchain verified against its attestation and set read-only"
REMOTE

echo "=== $REP transferred and verified ==="
