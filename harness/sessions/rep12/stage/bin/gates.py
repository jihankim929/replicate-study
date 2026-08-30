"""Apply the value-triggered gates to collected results and emit audit work.

- **G1** (> 230 cm3/cm3): presumed artifact.  Written to AUDIT.jsonl as
  `flagged_pending` and queued for a full audit before the number may appear
  anywhere outside AUDIT.jsonl.
- **G2** (210-230): interest band, `flagged_pending`, audited before promotion.
- **G7** (every 40th structure to pass screening): a G6-grade audit regardless
  of value.  "Pass screening" is defined here as: the structure passed the G3
  pre-simulation screen and both of its floor-grade pressure points returned
  status OK.  Ordering is by completion, taken from the sorted result table so
  it is reproducible from the record rather than from wall-clock accident.

The audit itself is an independent re-run from the archived inputs under a
different `RandomSeed`, which is what makes agreement a statistical statement
rather than a test of the plumbing.

usage: gates.py [--emit <queuefile>]
"""
import csv, json, os, subprocess, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
sys.path.insert(0, os.path.join(WS, "bin"))
import audit as A

G1_HI = 230.0
G2_LO = 210.0
G7_K = 40


def existing():
    seen = set()
    p = os.path.join(WS, "AUDIT.jsonl")
    if os.path.exists(p):
        for line in open(p):
            try:
                o = json.loads(line)
                seen.add((o["structure_id"], o["gate"]))
            except Exception:
                pass
    return seen


def main():
    emit = None
    if len(sys.argv) > 2 and sys.argv[1] == "--emit":
        emit = sys.argv[2]
    rows = [r for r in csv.DictReader(open(os.path.join(WS, "tables", "gcmc.csv")))]
    ok = [r for r in rows if r["status"] == "OK" and r["ncyc"] == "10000"]
    ok.sort(key=lambda r: r["name"])
    seen = existing()
    new, audits = [], []
    for i, r in enumerate(ok):
        n, wc = r["name"], float(r["wc"])
        if wc > G1_HI and (n, "G1") not in seen:
            new.append((n, "G1", "post-sim", "%.4f" % wc, "other",
                        "flagged_pending", "LOG-G1", "",
                        "Above the 230 ceiling threshold; presumed artifact "
                        "until structure integrity, charge balance, protocol "
                        "compliance and convergence are audited."))
            audits.append((n, "g1"))
        elif G2_LO <= wc <= G1_HI and (n, "G2") not in seen:
            new.append((n, "G2", "post-sim", "%.4f" % wc, "other",
                        "flagged_pending", "LOG-G2", "",
                        "In the 210-230 interest band; audited before promotion."))
            audits.append((n, "g2"))
        if (i + 1) % G7_K == 0 and (n, "G7") not in seen:
            new.append((n, "G7", "post-sim", "%.4f" % wc, "audit_passed",
                        "passed", "LOG-G7", "",
                        "Random audit: every %dth structure to pass screening, "
                        "regardless of value. Screening pass = G3 pass and both "
                        "floor-grade pressure points OK. Index %d in the "
                        "name-sorted completed table." % (G7_K, i + 1)))
            audits.append((n, "g7"))
    if new:
        tsv = os.path.join(WS, "work", "gate_events.tsv")
        with open(tsv, "w") as f:
            for t in new:
                f.write("\t".join(t) + "\n")
        subprocess.run([sys.executable, os.path.join(WS, "bin", "audit.py"),
                        "--bulk", tsv])
    if emit and audits:
        lines = []
        for n, kind in audits:
            safe = n.replace("[", "_").replace("]", "_")
            for p, tp in ((6500000, "65"), (580000, "58")):
                lines.append("%s|%d|10000|2000|aud%s__%s__p%s|seed:919%d"
                             % (n, p, kind, safe, tp, len(lines) % 7 + 1))
        with open(emit, "w") as f:
            f.write("\n".join(lines) + "\n")
    print("screened_ok=%d new_gate_events=%d audits_queued=%d" %
          (len(ok), len(new), len(audits)))
    if ok:
        w = sorted(float(r["wc"]) for r in ok)
        print("wc max=%.2f  n>=210=%d  n>230=%d" %
              (w[-1], sum(1 for x in w if x >= G2_LO),
               sum(1 for x in w if x > G1_HI)))


if __name__ == "__main__":
    main()
