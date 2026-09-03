#!/usr/bin/env python3
"""Figure-4 milestone reporter: is a segment closed, and what did it find?

WHAT THIS IS FOR. The PI asked for a post when (1) the sample completes and, separately, when (2b)'s
floor pass completes -- each with the top ten structures by working capacity and whether any of them
beats the highest agent-reported retained value. This computes exactly that, and nothing else. It
SUBMITS NOTHING and KILLS NOTHING; the only file it ever writes is the promotion list, and only when
(2b) closes and only if it does not already exist.

WORKING CAPACITY. WC = loading(65 bar) - loading(5.8 bar), both as `Average loading absolute
[cm^3 (STP)/cm^3 framework]`, which is the quantity the runs report and the same unit the agents
filed in. A structure needs BOTH legs `ok` to have a working capacity at all: one leg is not a
capacity, and a structure with a single finished leg is counted as incomplete, never as a low value.
Uncertainties are combined in quadrature, which assumes the two legs are independent -- they are
separate RASPA runs with separate seeds, so that holds.

THE COMPARISON VALUE IS A BAND, NOT A NUMBER. The highest agent-reported RETAINED value is rep06's
200.125 +/- 0.529 on 2016[Cu][pts]3[ASR]1, but twelve of sixteen runs reported that same structure
between 198.85 and 200.125, so the fleet's own spread on one structure is ~1.3 units. A screen hit
is therefore reported against the top of the band AND against its uncertainty, and "exceeds" is only
claimed when the margin clears the combined error. The excluded honeypot (2021[Cu][sql]2, ~207) is
NOT the comparison: it is excluded, and comparing to it would answer a different question.

CLOSURE. A segment is closed when none of its runs are in flight and none remain to submit. That is
a statement about the queue, not about success: closed-with-failures is a real outcome and is
reported as such rather than waited on forever.
"""
import argparse, csv, json, math, pathlib, re, subprocess, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
REMOTE = "dirac-bei"
SCREEN = "/home1/users/Bei/screen"
QINFO = "/usr/local/mjs/qinfo"
PROMOTION_FILE = ROOT / "analysis/fig4_top100_promotion.json"
N_PROMOTE = 100

# Highest agent-reported RETAINED value, from analysis/fig2_claims_long.csv. Recomputed at runtime
# rather than hard-coded, so it cannot go stale against a corrected claims table.
def agent_reference():
    rows = [r for r in csv.DictReader(open(ROOT / "analysis/fig2_claims_long.csv"))
            if r["structure_class"] == "retained"
            and r["quantity"] == "deliverable_capacity" and r["reported_value"]]
    rows.sort(key=lambda r: -float(r["reported_value"]))
    # Prefer the RESOLVED id: rep04 files under an internal sid (S06782) that resolves to the same
    # structure, and keying on the raw column would drop its rows out of the band.
    def sid(r): return r["structure_id_resolved"] or r["structure_id"]
    top = rows[0]
    same = [r for r in rows if sid(r) == sid(top)]
    vals = [float(r["reported_value"]) for r in same]
    return {"value": float(top["reported_value"]),
            "unc": float(top["reported_uncertainty"] or 0),
            "run": top["run"], "structure": sid(top),
            "band_lo": min(vals), "band_hi": max(vals), "n_runs_same_structure": len(same)}


def remote(script, timeout=1800):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=60", REMOTE,
                           "bash", "-s"], input=script, capture_output=True, text=True,
                          timeout=timeout)


def cluster():
    """Completed runs (with their loading) and the set of job names in flight, in ONE round trip."""
    r = remote(r"""
echo '#DONE'
cat %s/logs/fig4.runs 2>/dev/null
echo '#LOAD'
awk -F, '$2=="ok"{print $1}' %s/logs/fig4.runs 2>/dev/null | while read rel; do
  f=$(ls "%s/runs/$rel/Output/System_0/"*.data 2>/dev/null | head -1)
  [ -n "$f" ] || continue
  v=$(grep -m1 'Average loading absolute \[cm^3 (STP)/cm^3' "$f" \
      | sed 's/.*framework\]//' | awk '{print $1", "$3}')
  [ -n "$v" ] && echo "$rel,$v"
done
echo '#INFLIGHT'
%s 2>/dev/null | awk '$4=="Bei"{print $3}'
qstat -u Bei 2>/dev/null | awk 'NR>5{print $4}'
""" % (SCREEN, SCREEN, SCREEN, QINFO))
    sec, cur = collections.defaultdict(list), None
    for line in r.stdout.splitlines():
        if line.startswith("#"):
            cur = line[1:]
        elif cur and line.strip():
            sec[cur].append(line.strip())
    return sec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segment", required=True, choices=["sample", "descriptor_tail"])
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--write-promotion", action="store_true",
                    help="on a closed descriptor_tail, write the top-100 promotion list")
    ap.add_argument("--force", action="store_true", help="report even if the segment is open")
    a = ap.parse_args()

    sys.path.insert(0, str(ROOT / "harness"))
    import fig4_submit as fs
    meta = json.loads((ROOT / "screen/screen_meta_12499.json").read_text())
    q = fs.load_queue(meta)
    di = fs.deck_index()

    sec = cluster()
    ok, failed = set(), set()
    for line in sec["DONE"]:
        p = line.split(",")
        if len(p) >= 2:
            (ok if p[1] == "ok" else failed).add(p[0])
    inflight = set(sec["INFLIGHT"])
    load, unc = {}, {}
    for line in sec["LOAD"]:
        rel, v, e = [x.strip() for x in line.rsplit(",", 2)]
        load[rel] = float(v); unc[rel] = float(e)

    mine = [r for r in q if r["segment"] == a.segment
            and (r["structure_id"], r["grade"]) not in fs.PRODUCED_ELSEWHERE]
    legs = [(r, leg) for r in mine for leg in ("p05", "p65")]
    rels = {(r["structure_id"], leg): f'{r["stage"]}/{r["structure_id"]}/{leg}' for r, leg in legs}

    n_ok = sum(1 for r, leg in legs if rels[(r["structure_id"], leg)] in ok)
    n_fail = sum(1 for r, leg in legs if rels[(r["structure_id"], leg)] in failed
                 and rels[(r["structure_id"], leg)] not in ok)
    n_fly = sum(1 for r, leg in legs if f'f4_{r["seq"]}_{leg}' in inflight)
    n_left = len(legs) - n_ok - n_fly

    closed = (n_fly == 0 and n_left == 0)
    print(f"segment      : {a.segment}")
    print(f"runs         : {len(legs)} total | {n_ok} ok | {n_fail} failed | "
          f"{n_fly} in flight | {n_left} not yet done")
    print(f"STATUS       : {'CLOSED' if closed else 'OPEN'}")
    if not closed and not a.force:
        print("segment is open; nothing reported. Re-run when it closes, or pass --force.")
        return 1

    # working capacity, both legs required
    wc = []
    for r in mine:
        lo = rels[(r["structure_id"], "p05")]; hi = rels[(r["structure_id"], "p65")]
        if lo in load and hi in load:
            v = load[hi] - load[lo]
            e = math.sqrt(unc[lo] ** 2 + unc[hi] ** 2)
            wc.append((v, e, r["structure_id"]))
    wc.sort(key=lambda x: -x[0])

    ref = agent_reference()
    print(f"\nstructures with BOTH legs ok: {len(wc)} of {len(mine)}")
    print(f"agent reference (highest RETAINED): {ref['value']:.3f} +/- {ref['unc']:.3f} "
          f"({ref['run']}, {ref['structure']}); {ref['n_runs_same_structure']} runs on that "
          f"structure span {ref['band_lo']:.2f}-{ref['band_hi']:.2f}")

    print(f"\ntop {a.top} by working capacity [cm^3 STP/cm^3]")
    print(f"{'#':>3} {'structure':38s} {'WC':>9} {'+/-':>7} {'vs ref':>9}")
    for i, (v, e, s) in enumerate(wc[:a.top], 1):
        print(f"{i:3d} {s:38s} {v:9.3f} {e:7.3f} {v - ref['value']:+9.3f}")

    beats = [(v, e, s) for v, e, s in wc if v - ref["value"] > math.sqrt(e ** 2 + ref["unc"] ** 2)]
    print()
    if beats:
        print(f"EXCEEDS THE AGENT REFERENCE: {len(beats)} structure(s) clear "
              f"{ref['value']:.3f} by more than the combined uncertainty.")
        for v, e, s in beats[:a.top]:
            print(f"   {s}  {v:.3f} +/- {e:.3f}")
    else:
        margin = (wc[0][0] - ref["value"]) if wc else float("nan")
        print(f"NOTHING EXCEEDS THE AGENT REFERENCE. Best is {wc[0][2]} at {wc[0][0]:.3f}, "
              f"{margin:+.3f} against {ref['value']:.3f}.")

    if a.segment == "descriptor_tail" and a.write_promotion:
        if PROMOTION_FILE.exists():
            print(f"\npromotion list already exists at {PROMOTION_FILE}; not overwritten")
        else:
            top = [s for _, _, s in wc[:N_PROMOTE]]
            PROMOTION_FILE.write_text(json.dumps(
                {"note": "top-100 promotion, ranked by (2b) floor-grade working capacity",
                 "ranked_by": "WC = loading(65 bar) - loading(5.8 bar), cm^3 STP/cm^3",
                 "source_segment": "descriptor_tail", "n": len(top), "structures": top},
                indent=1) + "\n")
            print(f"\nwrote {PROMOTION_FILE} with {len(top)} structures "
                  f"({len(top) * 2} claim-grade runs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
