#!/usr/bin/env bash
# Archive the smoke workspaces off-cluster (PI ruling 2026-08-29, item 6) and remove them, so the
# fleet cannot read a previous campaign's record. Isolation is procedural under one Unix account;
# removing the material is the only mechanical part of it available this week.
#
# WHY THIS SCRIPT EXISTS RATHER THAN A COMMAND LINE. The first attempt was an ad-hoc pipeline that
# tarred, scp'd, and listed. The scp failed on a network outage, the trailing `ls` succeeded, and
# the whole thing **exited 0 while having copied nothing** -- the exact silent-success shape filed
# against RASPA the same hour. Every step here asserts, and the destructive step runs only after
# the non-destructive ones have proved their result.
#
# ORDER IS THE SAFETY PROPERTY: verify what is already held -> snapshot -> pull -> verify the pull
# -> and only then delete. Nothing is removed from the cluster until a verified local copy exists.
#
#   ./harness/archive_smoke.sh --verify-only    # steps 1-4, no deletion
#   ./harness/archive_smoke.sh --remove         # all steps, including deletion
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:---verify-only}"
ARCH="archive/smoke"; mkdir -p "$ARCH"
REPS="s01 s02"

say() { printf '%s\n' "  $*"; }

# --- 1. the copy already held, against the full pulled manifest -------------------------
say "1. verifying the local pulled copy against PULLED_MANIFEST.sha256"
TOT=$(grep -c . reps/smoke/PULLED_MANIFEST.sha256)
BAD=$(shasum -a 256 -c reps/smoke/PULLED_MANIFEST.sha256 2>/dev/null | grep -cv ": OK$" || true)
say "   verified $((TOT-BAD)) / $TOT"
[ "$BAD" -eq 0 ] || { echo "  ABORT: $BAD file(s) fail the pulled manifest" >&2; exit 4; }

# --- 2. the record files, against the 09:00 bell attestation ----------------------------
say "2. verifying record files against the 09:00 KST bell fingerprint"
N=0; F=0
while read -r h p; do
  [ "${#h}" -eq 64 ] || continue
  case "$h" in [0-9a-f]*) ;; *) continue ;; esac
  L="reps/smoke/${p#/home1/users/Bei/ws/}"
  N=$((N+1))
  [ -f "$L" ] || { echo "  MISSING $L" >&2; F=$((F+1)); continue; }
  [ "$(shasum -a 256 < "$L" | cut -d' ' -f1)" = "$h" ] || { echo "  MISMATCH $L" >&2; F=$((F+1)); }
done < reps/smoke/BELL_FINGERPRINT_0900KST.log
say "   $N record files checked, $F divergence(s)"
[ "$F" -eq 0 ] || { echo "  ABORT: the local copy diverges from the collection attestation" >&2; exit 5; }

# --- 3. raw snapshot of the cluster state, hashed ON the cluster -------------------------
say "3. tarring the cluster copy and hashing it there"
for R in $REPS; do
  ssh -o BatchMode=yes -o ConnectTimeout=60 dirac-bei "bash -s" -- "$R" <<'REMOTE' > "/tmp/$R.remote.sha"
set -euo pipefail
export LC_ALL=C
R="$1"
cd /home1/users/Bei/ws
mkdir -p /home1/users/Bei/tmp
tar czf "/home1/users/Bei/tmp/$R.tar.gz" "$R"
sha256sum "/home1/users/Bei/tmp/$R.tar.gz" | cut -d' ' -f1
REMOTE
  say "   $R remote sha256 $(cut -c1-16 < "/tmp/$R.remote.sha")..."
done

# --- 4. pull, and verify the pull actually arrived intact --------------------------------
say "4. pulling and verifying"
for R in $REPS; do
  scp -q "dirac-bei:/home1/users/Bei/tmp/$R.tar.gz" "$ARCH/$R.tar.gz"
  [ -s "$ARCH/$R.tar.gz" ] || { echo "  ABORT: $ARCH/$R.tar.gz absent or empty after scp" >&2; exit 6; }
  GOT=$(shasum -a 256 < "$ARCH/$R.tar.gz" | cut -d' ' -f1)
  WANT=$(tr -d '[:space:]' < "/tmp/$R.remote.sha")
  [ "$GOT" = "$WANT" ] || { echo "  ABORT: $R tar hash mismatch (remote $WANT, local $GOT)" >&2; exit 7; }
  tar tzf "$ARCH/$R.tar.gz" >/dev/null 2>&1 || { echo "  ABORT: $R tar is not readable" >&2; exit 8; }
  say "   $R $(du -h "$ARCH/$R.tar.gz" | cut -f1) verified, archive readable"
  cp "/tmp/$R.remote.sha" "$ARCH/$R.tar.gz.sha256"
done

if [ "$MODE" != "--remove" ]; then
  say "verify-only: nothing removed from the cluster. Re-run with --remove to delete."
  exit 0
fi

# --- 5. destructive step, last, and only now ---------------------------------------------
say "5. removing the smoke workspaces from the cluster"
for R in $REPS; do
  # The toolchain trees are provisioned read-only (dr-xr-xr-x), and rm cannot unlink inside a
  # directory it has no write bit on -- the first removal pass died on 494 permission-denied
  # files and left s01 stripped to its toolchain. Make the tree writable first, then remove.
  ssh -o BatchMode=yes -o ConnectTimeout=120 dirac-bei \
      "chmod -R u+w /home1/users/Bei/ws/$R 2>/dev/null; rm -rf /home1/users/Bei/ws/$R && rm -f /home1/users/Bei/tmp/$R.tar.gz && echo removed"
  ssh -o BatchMode=yes -o ConnectTimeout=60 dirac-bei "[ -d /home1/users/Bei/ws/$R ]" \
      && { echo "  ABORT: $R still present after removal" >&2; exit 9; }
  say "   $R removed and confirmed absent"
done
say "archive complete; the fleet can no longer reach a previous campaign's record"
