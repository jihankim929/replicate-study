#!/usr/bin/env bash
# Amendment 2026-09-04, report 3: has the descriptor tail's top 200 by helium void fraction
# finished both pressure legs, and what is the best working capacity in that cohort? READ-ONLY.
#
# THIS IS NOT THE PROMOTION LIST, and under this amendment that distinction is easy to lose. The
# tail is now submitted in descending vf_he, so this cohort is exactly the 200 structures chosen to
# run FIRST, and void fraction correlates with working capacity -- so it will complete early and it
# will look like a plausible promotion set. It is not one. The promotion is the top 100 BY WORKING
# CAPACITY over the CLOSED 858, drawn once by harness/fig4_milestone.py, which refuses to draw it
# from an open segment and refuses to overwrite a list it has already written. Ranking the 200
# structures that were selected to run first, by the quantity that selected them, is a subsample
# ranking; reading it as the promotion would replace a pre-registered rule with a selection.
# This script writes NOTHING -- not the promotion list, not the ledger, nothing.
#
# DELIVERY IS ON REQUEST, NOT ON A TIMER, per the PI ruling of 2026-09-03 that this amendment leaves
# standing. No watcher is built. Run it when you look. The accepted consequence is that the
# milestone can pass unnoticed.
#
# Exit status: 0 when all 200 have both legs ok, 1 when the cohort is still incomplete, 2 on error.
#
# Usage: bin/fig4_top200.sh [N]      (N defaults to 200)
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE=dirac-bei
N="${1:-200}"

TMP="$(mktemp -d)" || { echo "fig4_top200: cannot create temp dir" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT

# ---------------------------------------------------------------- the cohort, built locally
cat > "$TMP/cohort.py" <<'PY_EOF'
import sys, pathlib
root, n, out = pathlib.Path(sys.argv[1]), int(sys.argv[2]), pathlib.Path(sys.argv[3])
sys.path.insert(0, str(root / "harness"))
import fig4_submit as fs
vf = fs.tail_void_fractions()
q = [r for r in fs.load_queue({})
     if r["segment"] == "descriptor_tail"
     and (r["structure_id"], r["grade"]) not in fs.PRODUCED_ELSEWHERE]
# load_queue already emits the tail in descending vf_he; rank here from the key itself rather than
# trusting position, so this report does not silently follow a future reorder of the submitter.
q.sort(key=lambda r: (-vf.get(r["structure_id"], 0.0), r["structure_id"]))
rows = []
for i, r in enumerate(q[:n], 1):
    rows.append("\t".join([str(i), r["structure_id"], f'{vf.get(r["structure_id"], 0.0):.6f}',
                           str(r["seq"]), r["stage"]]))
out.write_text("\n".join(rows) + "\n")
(out.parent / "rels.txt").write_text("".join(
    f'{r["stage"]}/{r["structure_id"]}/{leg}\n' for r in q[:n] for leg in ("p05", "p65")))
print(f"cohort: top {len(rows)} of {len(q)} by vf_he, "
      f"{float(rows[0].split(chr(9))[2]):.4f} down to {float(rows[-1].split(chr(9))[2]):.4f}")
PY_EOF
python3 "$TMP/cohort.py" "$ROOT" "$N" "$TMP/cohort.tsv" || { echo "fig4_top200: cohort failed" >&2; exit 2; }

# ---------------------------------------------------------------- one round trip
{
cat <<'REMOTE_EOF'
cd /home1/users/Bei/screen || exit 1
echo '#NOW'
date -u +%s
echo '#RUNS'
cat logs/fig4.runs 2>/dev/null
echo '#QSTAT'
qstat -u Bei 2>/dev/null | awk 'NR>5 && NF>=10 {print $4, $10}'
echo '#MJS'
/usr/local/mjs/qinfo 2>/dev/null | awk '$4=="Bei"{print $3}'
echo '#LOAD'
xargs -d '\n' -P 32 -n 64 perl -e '
for my $rel (@ARGV) {
  my $d = "runs/$rel/Output/System_0";
  opendir(my $dh, $d) or next;
  my ($f) = grep { /\.data$/ } readdir($dh);
  closedir($dh);
  defined $f or next;
  my $p = "$d/$f"; my $sz = -s $p; defined $sz or next;
  open(my $fh, "<", $p) or next;
  seek($fh, $sz > 20000 ? $sz - 20000 : 0, 0);
  local $/; my $buf = <$fh>; close($fh);
  print "$rel,$1,$2\n"
    if $buf =~ /Average loading absolute \[cm\^3 \(STP\)\/cm\^3 framework\]\s+(\S+)\s+\+\/-\s+(\S+)/;
}' 2>/dev/null <<'RELS'
REMOTE_EOF
cat "$TMP/rels.txt"
cat <<'REMOTE_TAIL'
RELS
echo '#END'
REMOTE_TAIL
} > "$TMP/remote.sh"

if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE" bash -s \
        < "$TMP/remote.sh" > "$TMP/payload" 2>"$TMP/err"; then
    echo "fig4_top200: cluster query failed (nothing was submitted or changed)" >&2
    sed 's/^/  /' "$TMP/err" >&2
    exit 2
fi
grep -qx '#END' "$TMP/payload" || {
    echo "fig4_top200: truncated payload; refusing to report partial counts" >&2; exit 2; }

# ---------------------------------------------------------------- report
cat > "$TMP/report.py" <<'PY_EOF'
import sys, math, collections, pathlib, datetime
payload, root, cohort_f = (pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]),
                           pathlib.Path(sys.argv[3]))
sys.path.insert(0, str(root / "harness"))
import fig4_milestone as fm

SECTIONS = ("NOW", "RUNS", "QSTAT", "MJS", "LOAD", "END")
sec, cur = collections.defaultdict(list), None
for line in payload.read_text(errors="replace").splitlines():
    if line.startswith("#") and line[1:] in SECTIONS:
        cur = line[1:]
    elif cur and line.strip():
        sec[cur].append(line.strip())

now = int(sec["NOW"][0]) if sec["NOW"] else 0
KST = datetime.timezone(datetime.timedelta(hours=9))
stamp = datetime.datetime.fromtimestamp(now, KST).strftime("%Y-%m-%d %H:%M KST") if now else "?"

ok, failed = set(), set()
for line in sec["RUNS"]:
    p = line.split(",")
    if len(p) >= 2:
        (ok if p[1] == "ok" else failed).add(p[0])
failed -= ok
inflight = {l.split()[0] for l in sec["QSTAT"] if l.split()} | set(sec["MJS"])
load, unc = {}, {}
for line in sec["LOAD"]:
    try:
        rel, v, e = line.rsplit(",", 2)
        load[rel], unc[rel] = float(v), float(e)
    except ValueError:
        pass

cohort = []
for line in cohort_f.read_text().splitlines():
    if not line.strip():
        continue
    rank, sid, vf, seq, stage = line.split("\t")
    cohort.append((int(rank), sid, float(vf), int(seq), stage))

n = len(cohort)
both, part, fly, unsub, fail = 0, 0, 0, 0, 0
wc = []
for rank, sid, vf, seq, stage in cohort:
    lo, hi = f"{stage}/{sid}/p05", f"{stage}/{sid}/p65"
    d = sum(1 for r in (lo, hi) if r in ok)
    if d == 2:
        both += 1
    elif d == 1:
        part += 1
    elif any(f"f4_{seq}_{leg}" in inflight for leg in ("p05", "p65")):
        fly += 1
    elif lo in failed or hi in failed:
        fail += 1
    else:
        unsub += 1
    if lo in load and hi in load:
        wc.append((load[hi] - load[lo], math.sqrt(unc[lo] ** 2 + unc[hi] ** 2), sid, vf))
wc.sort(key=lambda x: -x[0])

print()
print(f"Figure 4 - descriptor tail, TOP {n} BY HELIUM VOID FRACTION   {stamp}   read-only")
print(f"  cohort vf_he {cohort[0][2]:.4f} (rank 1) down to {cohort[-1][2]:.4f} (rank {n})")
print()
print(f"  both legs ok        : {both:4d} of {n}")
print(f"  one leg ok          : {part:4d}")
print(f"  neither, in flight  : {fly:4d}")
print(f"  neither, failed     : {fail:4d}")
print(f"  neither, unsubmitted: {unsub:4d}")
complete = (both == n)
print()
print(f"  STATUS: {'COHORT COMPLETE - all ' + str(n) + ' have both legs ok' if complete else 'INCOMPLETE'}")

ref = fm.agent_reference()
print()
if not wc:
    print("  No structure in the cohort has both legs ok yet; no working capacity to report.")
else:
    v, e, s, vfb = wc[0]
    comb = math.sqrt(e ** 2 + ref["unc"] ** 2)
    label = "BEST IN THE COHORT" if complete else "BEST SO FAR (cohort incomplete)"
    print(f"  {label}, working capacity = loading(65 bar) - loading(5.8 bar) [cm^3 STP/cm^3]")
    print(f"    best      : {s:26s} {v:9.3f} +/- {e:5.3f}   vf_he {vfb:.4f}")
    print(f"    reference : {ref['structure']:26s} {ref['value']:9.3f} +/- {ref['unc']:5.3f}"
          f"   {ref['run']}, highest agent-reported RETAINED")
    print(f"    margin    : {v - ref['value']:+9.3f}   combined sigma {comb:.3f}   -> "
          f"{'EXCEEDS' if v - ref['value'] > comb else 'DOES NOT EXCEED'}")
    print(f"    ranked over {len(wc)} of {n} cohort structures with both legs ok.")
    if abs(ref["value"] - 200.125) > 1e-9:
        print(f"    NOTE: reference recomputed as {ref['value']:.3f}, not 200.125.")
print()
print("  NOT THE PROMOTION LIST. The promotion is the top 100 by working capacity over the CLOSED")
print("  858-structure tail, drawn once by harness/fig4_milestone.py. This cohort is the 200")
print("  structures selected to run first, ranked by the quantity that selected them.")
print()
sys.exit(0 if complete else 1)
PY_EOF

python3 "$TMP/report.py" "$TMP/payload" "$ROOT" "$TMP/cohort.tsv"
