#!/usr/bin/env bash
# analysis/fig4_interim.csv -- one row per Figure-4 structure that has BOTH pressure legs ok.
#
# WHAT IT TOUCHES. One ssh round trip that runs `awk` and `perl` on the login node, both reads.
# It SUBMITS NOTHING, KILLS NOTHING, and the only file it writes anywhere is its own output,
# analysis/fig4_interim.csv, plus a private mktemp directory removed on exit. Nothing on the
# cluster and nothing else in the repository is modified.
#
# SAFE WHILE THE SUBMITTER IS LIVE. Three things make that true rather than hoped for:
#   - it takes no lock and appends nothing, so it cannot block or corrupt the submitter's own
#     appends to screen/fig4_ledger.csv or to logs/fig4.runs;
#   - both of those files are read as one snapshot each. A row still being appended when we read
#     can arrive torn, so a short or unparseable trailing row is dropped rather than half-believed,
#     and the count of dropped rows is written into the header. A torn row is at worst one run's
#     absence from this export, which the next export picks up;
#   - the output is written to a temp file and renamed into place, so a reader of
#     analysis/fig4_interim.csv sees either the previous export or this one, never half of one.
# It is therefore an interim view of a moving campaign: two runs of it minutes apart will differ,
# and neither is wrong.
#
# WHERE EACH COLUMN COMES FROM. The join is deliberate, because no single source has all of it:
#   segment                 the submitter's own load_queue(), imported from harness/fig4_submit.py
#                           and not reimplemented, for the reason given in bin/fig4_status.sh: a
#                           private copy of that enumeration would drift from the submitter.
#   init_cycles,            screen/fig4_ledger.csv, the local record of what was actually
#   production_cycles       submitted, taken from the latest attempt of each leg. Where a run has
#                           no ledger row -- the reconcile gap of harness/fig4_submit.py -- these
#                           fall back to the grade's canonical CYCLES and the number of rows that
#                           needed the fallback is stated in the header.
#   N65, N5_8               `Average loading absolute [cm^3 (STP)/cm^3 framework]` from each leg's
#                           RASPA .data file on the cluster, read by seeking the last 20 kB (see
#                           bin/fig4_status.sh for why whole-file greps cost ~4 GB of network I/O).
#   working_capacity        N65 - N5_8, per harness/fig4_milestone.py. Both legs required: one leg
#   uncertainty             is not a capacity, so a half-finished structure is absent from this
#                           file, never present with a low value. Uncertainty is the two legs'
#                           quadrature sum -- separate runs, separate seeds, so independent.
#   agent_value, agent_run  the HIGHEST agent-reported deliverable_capacity for that structure in
#                           analysis/fig2_claims_long.csv, and the run that reported it, keyed on
#                           the resolved id. Empty for the overwhelming majority: no agent ever
#                           filed on most of these structures, and empty means unclaimed, NOT zero.
#                           A single agent value is the top of a band, not a number -- twelve of
#                           sixteen runs put one structure between 198.85 and 200.125 -- so any
#                           per-structure margin read off this column carries ~1.3 units of fleet
#                           spread that the column cannot show.
#
# WHAT IT IS NOT. Not a result and not a milestone: the segments are open, so the rows here are a
# subsample of each segment, and the top of a subsample is not the top of the segment.
# harness/fig4_milestone.py remains the tool of record for closing a segment.
#
# Usage: bin/fig4_export.sh [-o OUTPUT]     (default analysis/fig4_interim.csv)
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE=dirac-bei
OUT="$ROOT/analysis/fig4_interim.csv"

while getopts ":o:" opt; do
    case "$opt" in
        o) OUT="$OPTARG" ;;
        *) echo "usage: bin/fig4_export.sh [-o OUTPUT]" >&2; exit 2 ;;
    esac
done

TMP="$(mktemp -d)" || { echo "fig4_export: cannot create temp dir" >&2; exit 1; }
trap 'rm -rf "$TMP"' EXIT

# ---------------------------------------------------------------- one round trip
cat > "$TMP/remote.sh" <<'REMOTE_EOF'
cd /home1/users/Bei/screen || exit 1
echo '#NOW'
date -u +%s
echo '#RUNS'
cat logs/fig4.runs 2>/dev/null
echo '#LOAD'
# Absolute loading for every completed run, 32 readers wide, seeking to the last 20 kB.
# -d '\n' so xargs does not try to interpret the brackets in a structure id as quoting.
awk -F, '$2=="ok"{print $1}' logs/fig4.runs 2>/dev/null | sort -u |
xargs -d '\n' -P 32 -n 64 perl -e '
for my $rel (@ARGV) {
  my $d = "runs/$rel/Output/System_0";
  opendir(my $dh, $d) or next;
  my ($f) = grep { /\.data$/ } readdir($dh);
  closedir($dh);
  defined $f or next;
  my $p = "$d/$f";
  my $sz = -s $p;
  defined $sz or next;
  open(my $fh, "<", $p) or next;
  seek($fh, $sz > 20000 ? $sz - 20000 : 0, 0);
  local $/; my $buf = <$fh>; close($fh);
  print "$rel,$1,$2\n"
    if $buf =~ /Average loading absolute \[cm\^3 \(STP\)\/cm\^3 framework\]\s+(\S+)\s+\+\/-\s+(\S+)/;
}' 2>/dev/null
echo '#END'
REMOTE_EOF

if ! ssh -o BatchMode=yes -o ConnectTimeout=10 "$REMOTE" bash -s \
        < "$TMP/remote.sh" > "$TMP/payload" 2>"$TMP/err"; then
    echo "fig4_export: cluster query failed (nothing was submitted or changed;" \
         "$OUT is untouched)" >&2
    sed 's/^/  /' "$TMP/err" >&2
    exit 1
fi
grep -qx '#END' "$TMP/payload" || {
    echo "fig4_export: cluster query returned a truncated payload; refusing to write a" \
         "partial export ($OUT is untouched)" >&2
    exit 1
}

# ---------------------------------------------------------------- build
cat > "$TMP/build.py" <<'PY_EOF'
import sys, csv, math, pathlib, collections, datetime

payload, root, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
sys.path.insert(0, str(root / "harness"))
import fig4_submit as fs
import fig4_milestone as fm

LEGS = ("p05", "p65")
SECTIONS = ("NOW", "RUNS", "LOAD", "END")
sec, cur = collections.defaultdict(list), None
for line in payload.read_text(errors="replace").splitlines():
    if line.startswith("#") and line[1:] in SECTIONS:
        cur = line[1:]
    elif cur and line.strip():
        sec[cur].append(line.strip())

KST = datetime.timezone(datetime.timedelta(hours=9))
if sec["NOW"]:
    now, clock = int(sec["NOW"][0]), "cluster clock"
else:   # the nodes stamp fig4.runs, so the cluster clock is the right one; say so if it is missing
    now, clock = int(datetime.datetime.now(datetime.timezone.utc).timestamp()), "LOCAL clock"
stamp = (datetime.datetime.fromtimestamp(now, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
         + "  (" + datetime.datetime.fromtimestamp(now, KST).strftime("%Y-%m-%d %H:%M KST")
         + ", " + clock + ")")

# ---- the run log: rel,status,rc,start,end,host. A torn trailing row is dropped, not guessed. ----
ok, torn_runs = set(), 0
for line in sec["RUNS"]:
    p = line.split(",")
    if len(p) < 2 or not p[0] or p[1] not in ("ok", "failed"):
        torn_runs += 1
        continue
    if p[1] == "ok":
        ok.add(p[0])

load, unc = {}, {}
for line in sec["LOAD"]:
    try:
        rel, v, e = line.rsplit(",", 2)
        load[rel], unc[rel] = float(v), float(e)
    except ValueError:
        pass

# ---- the queue: segment and grade, from the submitter's own enumeration --------------------
# The queue is deduplicated on (structure, GRADE), not on structure: one structure can be in the
# sample at floor grade AND in the agent tail at claim grade, and those are two different
# measurements with different cycles, different decks and different `rel`s. So this iterates the
# queue rows and never keys on the structure id alone -- doing that silently replaces a finished
# floor row with an unfinished claim row and drops the finished work out of the export.
q = [r for r in fs.load_queue({})
     if (r["structure_id"], r["grade"]) not in fs.PRODUCED_ELSEWHERE]

def rel_of(r, leg):
    return f'{r["stage"]}/{r["structure_id"]}/{leg}'

queue_rels = {rel_of(r, leg) for r in q for leg in LEGS}
foreign_ok = len(ok - queue_rels)   # the Stage-0 ppn=1 requeue writes to the same log

# ---- the ledger: cycles as actually submitted, latest attempt of each leg -------------------
cycles, torn_ledger = {}, 0
lp = root / "screen/fig4_ledger.csv"
if lp.exists():
    with lp.open() as fh:
        rdr = csv.DictReader(l for l in fh if not l.startswith("#"))
        for row in rdr:
            try:
                stem, leg, grade = row["stem"], row["pressure"], row["grade"]
                init, prod = int(row["init_cycles"]), int(row["prod_cycles"])
            except (KeyError, TypeError, ValueError):
                torn_ledger += 1
                continue
            if not stem or leg not in LEGS:
                torn_ledger += 1
                continue
            # Keyed on grade as well as leg: the same structure can be submitted at both grades,
            # and a claim-grade run must not inherit a floor-grade run's cycles.
            cycles[(stem, grade, leg)] = (init, prod)   # later rows are later attempts; last wins

# ---- agent claims: highest reported deliverable_capacity per resolved structure --------------
agent = {}
with (root / "analysis/fig2_claims_long.csv").open() as fh:
    for row in csv.DictReader(fh):
        if row["quantity"] != "deliverable_capacity" or not row["reported_value"]:
            continue
        sid = row["structure_id_resolved"] or row["structure_id"]
        v = float(row["reported_value"])
        if sid not in agent or v > agent[sid][0]:
            agent[sid] = (v, row["run"], row["structure_class"])

# ---- rows: both legs ok AND both loadings parsed ---------------------------------------------
rows, both_ok, unparsed, fallback_cycles, nonretained = [], collections.Counter(), [], 0, []
for r in q:
    sid = r["structure_id"]
    rels = {leg: rel_of(r, leg) for leg in LEGS}
    if not all(rels[leg] in ok for leg in LEGS):
        continue
    both_ok[r["segment"]] += 1
    if not all(rels[leg] in load for leg in LEGS):
        unparsed.append(sid)         # legs finished, loading unreadable: a tooling gap, reported
        continue
    lo, hi = load[rels["p05"]], load[rels["p65"]]
    e = math.sqrt(unc[rels["p05"]] ** 2 + unc[rels["p65"]] ** 2)
    cyc = cycles.get((sid, r["grade"], "p65")) or cycles.get((sid, r["grade"], "p05"))
    if cyc is None:
        cyc = fs.CYCLES[r["grade"]]
        fallback_cycles += 1
    av, ar, cls = agent.get(sid, ("", "", ""))
    if cls and cls != "retained":
        nonretained.append(f"{sid} ({cls}, {ar})")
    rows.append(dict(structure_id=sid, segment=r["segment"],
                     init_cycles=cyc[0], production_cycles=cyc[1],
                     N65=f"{hi:.6f}", N5_8=f"{lo:.6f}",
                     working_capacity=f"{hi - lo:.6f}", uncertainty=f"{e:.6f}",
                     agent_value=(f"{av:.3f}" if av != "" else ""), agent_run=ar))

# Segment order is the submitter's; within a segment, descending working capacity.
order = {name: i for i, name in enumerate(fs.SUBMIT_ORDER)}
rows.sort(key=lambda d: (order.get(d["segment"], 99), -float(d["working_capacity"])))

_seen = collections.Counter(d["structure_id"] for d in rows)
dupes = sorted(k for k, n in _seen.items() if n > 1)
sizes = collections.Counter(r["segment"] for r in q)
exported = collections.Counter(d["segment"] for d in rows)
ref = fm.agent_reference()

COLS = ["structure_id", "segment", "init_cycles", "production_cycles", "N65", "N5_8",
        "working_capacity", "uncertainty", "agent_value", "agent_run"]

hdr = []
hdr.append("Figure-4 INTERIM export. One row per structure with BOTH pressure legs ok.")
hdr.append(f"exported            : {stamp}")
hdr.append("source              : logs/fig4.runs + RASPA .data on dirac-bei, joined to")
hdr.append("                      screen/fig4_ledger.csv (cycles) and harness/fig4_submit.py")
hdr.append("                      load_queue() (segment). Read-only; nothing was submitted.")
hdr.append("units               : N65, N5_8, working_capacity, uncertainty, agent_value are all")
hdr.append("                      cm^3 (STP)/cm^3 framework. N65 is 65 bar, N5_8 is 5.8 bar,")
hdr.append("                      working_capacity = N65 - N5_8, uncertainty = legs in quadrature.")
hdr.append("")
hdr.append("per-segment completion   both legs ok / structures in segment   ->  rows exported")
for name in fs.SUBMIT_ORDER:
    n = sizes.get(name, 0)
    if not n and not both_ok.get(name):
        continue
    pct = 100.0 * both_ok[name] / n if n else 0.0
    hdr.append(f"  {name:16s} {both_ok[name]:6d} / {n:6d}  ({pct:5.1f}%)"
               f"          {exported[name]:6d}")
hdr.append(f"  {'TOTAL':16s} {sum(both_ok.values()):6d} / {len(q):6d}"
           f"          {len(rows):6d}")
hdr.append("  Segments are OPEN. These rows are a subsample of each segment, so the top of this")
hdr.append("  file is not the top of the segment: an interim view, not a result.")
hdr.append("")
if dupes:
    hdr.append(f"note: {len(dupes)} structure(s) appear on MORE THAN ONE ROW because they are in")
    hdr.append("  the queue at two grades, which are two separate measurements at different cycle")
    hdr.append("  counts. Key on (structure_id, segment), not on structure_id: "
               + ", ".join(dupes[:5]) + (", ..." if len(dupes) > 5 else ""))
if unparsed:
    hdr.append(f"WARNING: {len(unparsed)} structure(s) have both legs ok but no parseable loading")
    hdr.append("  and are ABSENT below. That is a tooling gap, not an empty result: "
               + ", ".join(sorted(unparsed)[:5])
               + (", ..." if len(unparsed) > 5 else ""))
if torn_runs or torn_ledger:
    hdr.append(f"note: {torn_runs} row(s) of logs/fig4.runs and {torn_ledger} row(s) of the ledger")
    hdr.append("  were unparseable and were dropped rather than half-believed -- expected while the")
    hdr.append("  submitter is appending. Any run they cover reappears in the next export.")
if fallback_cycles:
    hdr.append(f"note: {fallback_cycles} row(s) had no ledger row and take init_cycles /")
    hdr.append("  production_cycles from the grade's canonical CYCLES instead of from the ledger.")
if foreign_ok:
    hdr.append(f"note: {foreign_ok} ok run(s) in logs/fig4.runs belong to no Figure-4 queue segment")
    hdr.append("  (the Stage-0 ppn=1 requeue writes to the same log) and are excluded.")
hdr.append("agent_value is the HIGHEST agent-reported deliverable_capacity for that structure in")
hdr.append("  analysis/fig2_claims_long.csv, and agent_run the run that reported it. EMPTY MEANS")
hdr.append("  UNCLAIMED, NOT ZERO. It is the top of a band, not a number: the highest retained")
hdr.append(f"  claim is {ref['value']:.3f} +/- {ref['unc']:.3f} ({ref['run']}, {ref['structure']}), yet "
           f"{ref['n_runs_same_structure']} runs on that one")
hdr.append(f"  structure span {ref['band_lo']:.2f}-{ref['band_hi']:.2f}, so the fleet's own spread "
           "there is ~%.1f units." % (ref["band_hi"] - ref["band_lo"]))
if nonretained:
    hdr.append("  Not every agent_value below is a RETAINED claim; these are not: "
               + "; ".join(sorted(nonretained)))
hdr.append("")
hdr.append("Every line above begins '#' and is header; the CSV header row follows. No structure id")
hdr.append("  contains '#', so pandas.read_csv(path, comment='#') reads this file as-is.")

tmp_out = out.with_name(out.name + ".tmp")
with tmp_out.open("w", newline="") as fh:
    for line in hdr:
        fh.write(("# " + line).rstrip() + "\n")
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
tmp_out.replace(out)     # atomic: a reader sees the old export or this one, never half of one

print(f"fig4_export: {len(rows)} rows -> {out}")
for name in fs.SUBMIT_ORDER:
    if sizes.get(name, 0) or both_ok.get(name):
        print(f"  {name:16s} {exported[name]:6d} exported of {both_ok[name]:6d} both-legs-ok "
              f"of {sizes.get(name, 0):6d} in segment")
if unparsed:
    print(f"  WARNING: {len(unparsed)} both-legs-ok structure(s) had no parseable loading")
PY_EOF

python3 "$TMP/build.py" "$TMP/payload" "$ROOT" "$OUT"
