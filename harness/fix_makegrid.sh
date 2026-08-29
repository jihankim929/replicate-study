#!/usr/bin/env bash
# INFRA REPAIR (PI authorized 2026-08-29, rep01 escalation `infra`): give a workspace a writable
# RASPA_DIR so SimulationType MakeGrid can write grids.
#
# Diagnosis, measured rather than assumed. The pinned toolchain's share tree is read-only and
# contains NO grids/ directory, and RASPA writes grids to $RASPA_DIR/share/raspa/grids/... It
# therefore cannot create the path, and -- this is the part that matters -- it reports the failure
# by printing "ERROR:" to stdout and **exiting 0**. Reproduced twice on the provided 2.0.37 build:
# once failing (no grid file, exit 0) and once succeeding (2 grid files, exit 0). The exit code
# carries no information in either direction.
#
# The repair does NOT touch the pinned toolchain. It builds `raspa_home/` beside it, symlinking
# each pinned share subtree so the forcefield and molecule definitions remain the hash-pinned
# originals, and providing grids/ as a real writable directory pointed at the workspace's own
# grids_dir. Claim-grade inputs stay pinned; only the output path becomes writable.
#
#   ./harness/fix_makegrid.sh rep01
set -euo pipefail
REP="${1:?usage: fix_makegrid.sh <rep_id>}"
WS="/home1/users/Bei/ws/$REP"

ssh -o BatchMode=yes -o ConnectTimeout=60 dirac-bei "bash -s" -- "$WS" <<'REMOTE'
set -euo pipefail
export LC_ALL=C
WS="$1"
TC="$WS/toolchain/raspa"
H="$WS/raspa_home"
mkdir -p "$H/share/raspa" "$WS/grids"
for d in forcefield molecules structures framework; do
  [ -e "$TC/share/raspa/$d" ] && ln -sfn "$TC/share/raspa/$d" "$H/share/raspa/$d"
done
rm -rf "$H/share/raspa/grids"
ln -sfn "$WS/grids" "$H/share/raspa/grids"
echo "  raspa_home ready: $H"
ls -l "$H/share/raspa" | awk '{print "    ", $9, $10, $11}'
REMOTE
