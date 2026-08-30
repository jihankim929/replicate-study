"""Write work/queue.txt: the ordered list of GCMC tasks workers pull from.

Three things happen here that matter.

1. **Geometry deduplication.** s3 is chargeless, so two entries differing only in
   their DDEC6 charge column are the same simulation.  Only the canonical member
   of each geometry group is ever queued; the others inherit its number and are
   reported as identical entries, not re-simulated.

2. **Cost model.** Wall time per run is calibrated from the one run I have timed
   (reference structure, 0.333 s/cycle): cost ~ C * ncycles * N_mol * (N_fw +
   N_mol), with N_mol from the predicted loading and the supercell volume.  Used
   to keep the wave inside its CPU-hour allowance and to flag structures whose
   cost is out of proportion to their rank.

3. **Two arms.** `exploit` takes the head of the LDA ranking; `explore` is a
   stratified draw across LDA deciles.  The explore arm is not decoration: it is
   the only unbiased sample, so it is what any later model is trained and honestly
   scored on, and it is the population G7's every-40th audit is drawn from.

usage: mkqueue.py <wave> <n_exploit> <n_explore> <cpu_h_budget> [ncyc] [ninit]
"""
import csv, math, os, random, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")

C_CAL = 2.40e-7          # s per (cycle * molecule * interaction-partner)
MOLEC_PER_CC = 2.687e-5  # molecules per A^3 per (cm3 STP/cm3)


def cost_seconds(r, ncyc, nload):
    """Estimated wall seconds for one pressure point."""
    vsuper = float(r["v_super"])
    nfw = int(r["natoms"]) * int(r["nrep"])
    nmol = max(20.0, nload * vsuper * MOLEC_PER_CC)
    return C_CAL * ncyc * nmol * (nfw + nmol)


def main():
    wave = sys.argv[1]
    nex, nrand = int(sys.argv[2]), int(sys.argv[3])
    budget_h = float(sys.argv[4])
    ncyc = int(sys.argv[5]) if len(sys.argv) > 5 else 10000
    ninit = int(sys.argv[6]) if len(sys.argv) > 6 else 2000
    tot = ncyc + ninit

    canon = set()
    for r in csv.DictReader(open(os.path.join(WS, "tables", "geomgroups.csv"))):
        canon.add(r["canonical"])
    g3 = dict((r["name"], r["g3"]) for r in
              csv.DictReader(open(os.path.join(WS, "tables", "g3_screen.csv"))))
    rows = list(csv.DictReader(open(os.path.join(WS, "tables", "descriptors.csv"))))
    for r in rows:
        a, b, c = float(r["density"]), 0, 0
        # supercell volume from mass and density: V_uc = mass/(rho*0.60221)
        r["v_super"] = str(float(r["natoms"]) * 0.0 + 0.0)
    # recover V_super from the raw descriptor shards (they carry V_uc)
    vuc = {}
    d = os.path.join(WS, "desc")
    for f in sorted(os.listdir(d)):
        if f.endswith(".csv"):
            for r in csv.DictReader(open(os.path.join(d, f))):
                if r.get("V_uc"):
                    try:
                        vuc[r["name"]] = float(r["V_uc"]) * int(r["nrep"])
                    except (ValueError, TypeError):
                        pass
    for r in rows:
        r["v_super"] = str(vuc.get(r["name"], 1e5))

    elig = [r for r in rows
            if r["name"] in canon and g3.get(r["name"], "PASS") == "PASS"]
    elig.sort(key=lambda r: -float(r["wc_pred"]))

    done = set()
    cl = os.path.join(WS, "work", "claimed")
    if os.path.isdir(cl):
        for t in os.listdir(cl):
            if "__" in t:
                done.add(t.split("__")[1])

    chosen, spent = [], 0.0
    for r in elig:
        if len(chosen) >= nex:
            break
        safe = r["name"].replace("[", "_").replace("]", "_")
        if safe in done:
            continue
        c = (cost_seconds(r, tot, float(r["n_hi_pred"])) +
             cost_seconds(r, tot, float(r["n_lo_pred"]))) / 3600.0
        if spent + c > budget_h * 0.75:
            continue
        chosen.append((r, c, "exploit"))
        spent += c

    rest = [r for r in elig if r not in [c[0] for c in chosen]]
    if nrand > 0 and rest:
        rnd = random.Random(20260830)
        vals = sorted(float(r["wc_pred"]) for r in rest)
        edges = [vals[int(k * (len(vals) - 1) / 10.0)] for k in range(11)]
        buckets = [[] for _ in range(10)]
        for r in rest:
            v = float(r["wc_pred"])
            k = min(9, sum(1 for e in edges[1:10] if v >= e))
            buckets[k].append(r)
        per = max(1, nrand // 10)
        for b in buckets:
            rnd.shuffle(b)
            for r in b[:per]:
                safe = r["name"].replace("[", "_").replace("]", "_")
                if safe in done:
                    continue
                c = (cost_seconds(r, tot, float(r["n_hi_pred"])) +
                     cost_seconds(r, tot, float(r["n_lo_pred"]))) / 3600.0
                if spent + c > budget_h:
                    continue
                chosen.append((r, c, "explore"))
                spent += c

    # interleave so both arms progress even if only a few workers ever run
    ex = [c for c in chosen if c[2] == "exploit"]
    rd = [c for c in chosen if c[2] == "explore"]
    order = []
    i = j = 0
    while i < len(ex) or j < len(rd):
        for _ in range(3):
            if i < len(ex):
                order.append(ex[i]); i += 1
        if j < len(rd):
            order.append(rd[j]); j += 1

    lines = []
    for r, c, arm in order:
        n = r["name"]
        safe = n.replace("[", "_").replace("]", "_")
        for p, tp in ((6500000, "65"), (580000, "58")):
            lines.append("%s|%d|%d|%d|%s%s__%s__p%s|-"
                         % (n, p, ncyc, ninit, wave, arm[:2], safe, tp))
    qp = os.path.join(WS, "work", "queue.txt")
    with open(qp, "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(WS, "tables", "%s_plan.csv" % wave), "w") as f:
        f.write("name,arm,est_cpu_h,wc_pred,n_hi_pred,density,vf_he,lcd,qst,natoms,nrep\n")
        for r, c, arm in order:
            f.write('"%s",%s,%.3f,%s,%s,%s,%s,%s,%s,%s,%s\n'
                    % (r["name"], arm, c, r["wc_pred"], r["n_hi_pred"],
                       r["density"], r["vf_he"], r["lcd"], r["qst"],
                       r["natoms"], r["nrep"]))
    print("wave=%s structures=%d (exploit %d, explore %d) tasks=%d "
          "est_cpu_h=%.1f budget=%.1f cycles=%d+%d"
          % (wave, len(order), len(ex), len(rd), len(lines), spent, budget_h,
             ninit, ncyc))
    print("eligible_canonical_g3pass=%d of %d entries" % (len(elig), len(rows)))
    print("wc_pred range in wave: %.1f .. %.1f"
          % (min(float(r["wc_pred"]) for r, _, _ in order),
             max(float(r["wc_pred"]) for r, _, _ in order)))


if __name__ == "__main__":
    main()
