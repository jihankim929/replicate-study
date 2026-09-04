#!/usr/bin/env bash
# Figure-4 status in one screenful, in under five seconds. READ-ONLY.
#
# WHAT IT TOUCHES. One ssh round trip that runs `awk`, `qstat`, `qinfo`, `tail`-equivalent seeks and
# `perl` on the login node, all reads. It SUBMITS NOTHING, KILLS NOTHING, and writes nothing anywhere
# except a private mktemp directory removed on exit. Nothing in the repository and nothing in the
# campaign is modified, so it is safe to run at any time, including mid-campaign.
#
# WHY IT IS FAST. The obvious implementation -- what fig4_milestone.py does -- greps every RASPA
# .data file whole. Those files are 1.5-12 MB each and the loading line sits 4,203 bytes from EOF,
# so a whole-file grep reads ~4 GB across the network filesystem: measured at 2m19s for 1,647 runs.
# This seeks to the last 20 kB instead (one open + one 20 kB read per run) and fans the reads out 32
# ways, because the cost is filesystem latency and not CPU. The pattern occurs exactly once per
# file, so seeking cannot select a different occurrence than the whole-file grep does.
#
# WHERE THE DEFINITIONS COME FROM. The queue -- which structures are in which segment, and the `seq`
# that fixes every job NAME -- is built by importing harness/fig4_submit.py and calling its own
# load_queue(). It is deliberately not reimplemented here: a private copy of that enumeration would
# drift from the submitter and mis-name jobs. Working capacity and the agent reference band follow
# harness/fig4_milestone.py.
#
# VALIDATED against fig4_milestone.py --segment sample --force, run back to back on 2026-09-04:
# identical ok / failed / in flight counts once its "not yet done" is expanded into failed +
# unsubmitted, identical both-legs count, and the identical best structure 2013[Zn][pcu]3[ASR]6 at
# 190.157 +/- 0.839. 1m47.6s there, 0.66s here.
#
# WHAT IT IS NOT. A status view, not a milestone post: fig4_milestone.py remains the tool of record
# for closing a segment and is the only one that may write the promotion list.
#
# Usage: bin/fig4_status.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE=dirac-bei

TMP="$(mktemp -d)" || { echo "fig4_status: cannot create temp dir" >&2; exit 1; }
trap 'rm -rf "$TMP"' EXIT

# ---------------------------------------------------------------- one round trip
cat > "$TMP/remote.sh" <<'REMOTE_EOF'
cd /home1/users/Bei/screen || exit 1
echo '#NOW'
date -u +%s
echo '#RUNS'
cat logs/fig4.runs 2>/dev/null
echo '#QSTAT'
# Job NAME and state. The header is 5 lines; column 4 is the name, column 10 the state.
qstat -u Bei 2>/dev/null | awk 'NR>5 && NF>=10 {print $4, $10}'
echo '#MJS'
# Jobs the mjs daemon holds but has not dispatched to PBS yet: staged, not running. In flight is
# the UNION of this and qstat -- see the fig4_submit.py docstring on why either alone under-counts.
/usr/local/mjs/qinfo 2>/dev/null | awk '$4=="Bei"{print $3}'
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

if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE" bash -s \
        < "$TMP/remote.sh" > "$TMP/payload" 2>"$TMP/err"; then
    echo "fig4_status: cluster query failed (nothing was submitted or changed)" >&2
    sed 's/^/  /' "$TMP/err" >&2
    exit 1
fi
grep -qx '#END' "$TMP/payload" || {
    echo "fig4_status: cluster query returned a truncated payload;" \
         "refusing to report partial counts" >&2
    exit 1
}

# ---------------------------------------------------------------- report
cat > "$TMP/report.py" <<'PY_EOF'
import sys, math, collections, pathlib, datetime

payload, root = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
sys.path.insert(0, str(root / "harness"))
import fig4_submit as fs
import fig4_milestone as fm

SECTIONS = ("NOW", "RUNS", "QSTAT", "MJS", "LOAD", "END")
sec, cur = collections.defaultdict(list), None
for line in payload.read_text(errors="replace").splitlines():
    if line.startswith("#") and line[1:] in SECTIONS:
        cur = line[1:]
    elif cur and line.strip():
        sec[cur].append(line.strip())

if sec["NOW"]:
    now = int(sec["NOW"][0])
else:   # the nodes stamp fig4.runs, so the cluster clock is the right one; say so if it is missing
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    print("WARNING: no clock from the cluster; windows below use this machine's clock instead.")
KST = datetime.timezone(datetime.timedelta(hours=9))
def kst(ts):
    return datetime.datetime.fromtimestamp(ts, KST).strftime("%Y-%m-%d %H:%M KST")

# ---- the run log: rel,status,rc,start,end,host -----------------------------------
ok, failed, ends = set(), set(), []
for line in sec["RUNS"]:
    p = line.split(",")
    if len(p) < 2:
        continue
    (ok if p[1] == "ok" else failed).add(p[0])
    if len(p) >= 5:
        try:
            ends.append((int(p[4]), p[1]))
        except ValueError:
            pass
failed -= ok           # a run that failed and was re-run to ok is ok, not failed

# ---- what is in flight: PBS union mjs, keyed on job NAME -------------------------
qs = [l.split() for l in sec["QSTAT"]]
pbs_state = collections.Counter(p[1] for p in qs if len(p) >= 2)
pbs_names = {p[0] for p in qs if len(p) >= 2}
mjs_names = set(sec["MJS"])
inflight = pbs_names | mjs_names

# ---- loadings --------------------------------------------------------------------
load, unc = {}, {}
for line in sec["LOAD"]:
    try:
        rel, v, e = line.rsplit(",", 2)
        load[rel], unc[rel] = float(v), float(e)
    except ValueError:
        pass

# ---- the queue, from the submitter's own enumeration -----------------------------
LEGS = ("p05", "p65")
q = [r for r in fs.load_queue({})
     if (r["structure_id"], r["grade"]) not in fs.PRODUCED_ELSEWHERE]
seg_rows = collections.OrderedDict()
for name in fs.SUBMIT_ORDER:
    rs = [r for r in q if r["segment"] == name]
    if rs:
        seg_rows[name] = rs

def rel_of(r, leg):
    return f'{r["stage"]}/{r["structure_id"]}/{leg}'

# Exclusive categories, precedence ok > in flight > failed > unsubmitted, so the four
# columns partition the segment instead of double-counting a failed-then-requeued run.
stat = collections.OrderedDict()
queue_rels = set()
for name, rs in seg_rows.items():
    c = dict(runs=0, ok=0, failed=0, fly=0, unsub=0, structs=len(rs), both=0)
    for r in rs:
        done = 0
        for leg in LEGS:
            rel = rel_of(r, leg)
            queue_rels.add(rel)
            c["runs"] += 1
            if rel in ok:
                c["ok"] += 1
                done += 1
            elif f'f4_{r["seq"]}_{leg}' in inflight:
                c["fly"] += 1
            elif rel in failed:
                c["failed"] += 1
            else:
                c["unsub"] += 1
        if done == 2:
            c["both"] += 1
    stat[name] = c

print()
print(f"Figure 4 status   {kst(now)}   (cluster clock)   read-only")
print()
print(f"{'segment':16s} {'runs':>6} {'ok':>6} {'failed':>7} {'in flight':>10} "
      f"{'unsub':>7}   structures with both legs ok")
for name, c in stat.items():
    pct = 100.0 * c["both"] / c["structs"] if c["structs"] else 0.0
    print(f"{name:16s} {c['runs']:6d} {c['ok']:6d} {c['failed']:7d} {c['fly']:10d} "
          f"{c['unsub']:7d}   {c['both']:5d} of {c['structs']:5d}  ({pct:4.1f}%)")
tot = {k: sum(c[k] for c in stat.values()) for k in ("runs", "ok", "failed", "fly", "unsub")}
print(f"{'TOTAL':16s} {tot['runs']:6d} {tot['ok']:6d} {tot['failed']:7d} {tot['fly']:10d} "
      f"{tot['unsub']:7d}")
print("  categories are exclusive: ok > in flight > failed > unsubmitted. A failed run is")
print("  re-submittable, so work remaining is failed + in flight + unsubmitted.")
extra = len((ok | failed) - queue_rels)
if extra:
    print(f"  {extra} of the {len(ok | failed)} runs in logs/fig4.runs belong to no Figure-4 queue")
    print("  segment (the Stage-0 ppn=1 requeue writes to the same log) and are excluded above.")

# ---- the queue as the schedulers see it ------------------------------------------
running = pbs_state.get("R", 0)
print()
print("QUEUE")
print(f"  PBS running under this account (qstat -u Bei, state R) : {running}")
other = {s: n for s, n in pbs_state.items() if s != "R"}
if other:
    print(f"  PBS other states                                       : "
          f"{', '.join(f'{n} {s}' for s, n in sorted(other.items()))}")
print(f"  staged in mjs, not yet dispatched to PBS (qinfo)        : {len(mjs_names)}")
print(f"  in flight = union of both listings                      : {len(inflight)}")
print(f"  At ppn=1 one running job is one core, so throughput is set by the {running} running,")
print(f"  not by the {len(inflight)} in flight.")

# ---- completions -----------------------------------------------------------------
print()
print("COMPLETIONS  (logs/fig4.runs, by end time)")
rates = {}
for h in (1, 6, 12):
    cut = now - h * 3600
    w = [st for e, st in ends if e >= cut]
    n_ok = sum(1 for st in w if st == "ok")
    rates[h] = n_ok / h
    print(f"  last {h:2d} h : {len(w):5d} runs  ({n_ok} ok, {len(w) - n_ok} failed)"
          f"   {rates[h]:7.1f} ok/h")
rate6 = rates[6]

# ---- projection ------------------------------------------------------------------
print()
sample_left = stat["sample"]["runs"] - stat["sample"]["ok"] if "sample" in stat else 0
tail_left = (stat["descriptor_tail"]["runs"] - stat["descriptor_tail"]["ok"]
             if "descriptor_tail" in stat else 0)
if not rate6:
    print("PROJECTION: no completions in the last 6 h; no rate, so no projection.")
    print(f"  sample {sample_left} runs left, descriptor tail {tail_left} runs left.")
else:
    hs = sample_left / rate6
    ht = (sample_left + tail_left) / rate6
    print(f"PROJECTION at the 6 h rate ({rate6:.1f} ok/h)")
    print(f"  sample            : {sample_left:5d} runs left {hs:8.1f} h  -> {kst(now + hs * 3600)}")
    print(f"  + descriptor tail : {tail_left:5d} runs left {ht:8.1f} h  -> {kst(now + ht * 3600)}")
    print("  Cumulative: the tail is sequential behind the sample, so its hours include the")
    print("  sample's. Both assume the rate holds and that nothing ahead of the tail is inserted.")
    # A projection off one window is a point estimate of a moving quantity. When the windows
    # disagree the honest answer is the range, so say so and price the disagreement.
    spread = max(rates.values()) / min(rates.values()) if min(rates.values()) > 0 else float("inf")
    if spread > 1.5:
        alt = max((h for h in rates if rates[h] > 0), key=lambda h: rates[h])
        ra = rates[alt]
        print(f"  NOT IN STEADY STATE: 1 h {rates[1]:.1f}/h, 6 h {rates[6]:.1f}/h, "
              f"12 h {rates[12]:.1f}/h. At the fastest of the three")
        print(f"  ({alt} h, {ra:.1f} ok/h) the sample closes in {sample_left / ra:.1f} h "
              f"({kst(now + sample_left / ra * 3600)}) and the tail in")
        print(f"  {(sample_left + tail_left) / ra:.1f} h. Read the range, not the point: "
              f"the 6 h figure above is one end of it.")

# ---- best in the sample ----------------------------------------------------------
ref = fm.agent_reference()
wc = []
for r in seg_rows.get("sample", []):
    lo, hi = rel_of(r, "p05"), rel_of(r, "p65")
    if lo in load and hi in load:
        wc.append((load[hi] - load[lo],
                   math.sqrt(unc[lo] ** 2 + unc[hi] ** 2), r["structure_id"]))
wc.sort(key=lambda x: -x[0])

print()
print("BEST IN THE SAMPLE  by working capacity = loading(65 bar) - loading(5.8 bar)"
      "  [cm^3 STP/cm^3]")
expect = stat["sample"]["both"] if "sample" in stat else 0
if not wc and expect:
    print(f"  NO LOADINGS PARSED, though {expect} sample structures have both legs ok. The")
    print("  extraction returned nothing -- this is a tooling failure, NOT an empty result.")
elif not wc:
    print("  No sample structure has both legs ok yet; there is no working capacity to report.")
else:
    v, e, s = wc[0]
    comb = math.sqrt(e ** 2 + ref["unc"] ** 2)
    print(f"  best      : {s:26s} {v:9.3f} +/- {e:5.3f}")
    print(f"  reference : {ref['structure']:26s} {ref['value']:9.3f} +/- {ref['unc']:5.3f}"
          f"   {ref['run']}, highest agent-reported RETAINED")
    print(f"  margin    : {v - ref['value']:+9.3f}   combined sigma {comb:.3f}   -> "
          f"{'EXCEEDS' if v - ref['value'] > comb else 'DOES NOT EXCEED'}")
    print(f"  The reference is the top of a band, not a number: "
          f"{ref['n_runs_same_structure']} runs on that one structure")
    print(f"  span {ref['band_lo']:.3f}-{ref['band_hi']:.3f}, so the fleet's own spread on it is "
          f"~{ref['band_hi'] - ref['band_lo']:.1f} units.")
    if len(wc) < expect:
        print(f"  WARNING: {expect - len(wc)} of {expect} both-legs structures had no parseable")
        print("  loading and are missing from this ranking.")
    b = stat["sample"]
    print(f"  Basis: {len(wc)} of {b['structs']} sample structures have both legs ok "
          f"({100.0 * len(wc) / b['structs']:.0f}%). The top of a")
    print("  subsample is not the top of the sample: this is a progress note, not a result.")
if abs(ref["value"] - 200.125) > 1e-9:
    print(f"  NOTE: the reference recomputed from analysis/fig2_claims_long.csv is "
          f"{ref['value']:.3f}, not 200.125.")
print()
PY_EOF

python3 "$TMP/report.py" "$TMP/payload" "$ROOT"
