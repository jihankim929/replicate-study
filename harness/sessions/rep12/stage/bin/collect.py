"""Collapse per-worker GCMC result CSVs into one structure-level table.

Tags are `<wave>__<safe_structure>__p65` / `__p58`; the two pressures of one
structure at one fidelity are joined into a working capacity.  Nothing here
reads a RASPA output file -- bin/extract.py did that once, at run time.

usage: collect.py [outfile]
"""
import csv, math, os, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
COLS = ["tag", "cif", "press", "ncyc", "ninit", "grid", "v", "ve", "m", "me",
        "nmol", "sec", "status"]


def load_all():
    recs = []
    tdir = os.path.join(WS, "tables")
    for root, dirs, files in os.walk(tdir):
        for fn in files:
            if not fn.endswith(".csv") or "shard" in fn:
                continue
            if os.path.basename(root) == "tables":
                continue
            with open(os.path.join(root, fn)) as fh:
                for r in csv.reader(fh):
                    if len(r) != len(COLS):
                        continue
                    d = dict(zip(COLS, r))
                    d["_src"] = os.path.join(os.path.basename(root), fn)
                    recs.append(d)
    return recs


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WS, "tables", "gcmc.csv")
    recs = load_all()
    byk = {}
    for d in recs:
        tag = d["tag"]
        if "__p" not in tag:
            continue
        base, p = tag.rsplit("__p", 1)
        key = (base, d["ncyc"], d["ninit"], d["grid"])
        byk.setdefault(key, {})[p] = d
    rows = []
    for (base, ncyc, ninit, grid), pr in sorted(byk.items()):
        hi = pr.get("65")
        lo = pr.get("58")
        if not hi or not lo:
            continue
        if hi["status"] != "OK" or lo["status"] != "OK":
            st = "%s/%s" % (hi["status"], lo["status"])
            rows.append((base, hi["cif"].strip('"'), ncyc, ninit, grid,
                         "", "", "", "", "", "", st,
                         hi["sec"], lo["sec"]))
            continue
        v65, e65 = float(hi["v"]), float(hi["ve"])
        v58, e58 = float(lo["v"]), float(lo["ve"])
        wc = v65 - v58
        we = math.sqrt(e65 * e65 + e58 * e58)
        rows.append((base, hi["cif"].strip('"'), ncyc, ninit, grid,
                     "%.4f" % v65, "%.4f" % e65, "%.4f" % v58, "%.4f" % e58,
                     "%.4f" % wc, "%.4f" % we, "OK", hi["sec"], lo["sec"]))
    hdr = ("run,name,ncyc,ninit,grid,n65,n65_err,n58,n58_err,wc,wc_err,status,"
           "sec65,sec58")
    with open(out, "w") as f:
        f.write(hdr + "\n")
        for r in rows:
            f.write('"%s","%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % r)
    ok = [r for r in rows if r[11] == "OK"]
    tot = sum(int(r[12]) + int(r[13]) for r in rows if r[12] and r[13])
    print("pairs=%d ok=%d failed=%d cpu_h=%.2f" % (len(rows), len(ok),
                                                   len(rows) - len(ok), tot / 3600.0))
    if ok:
        w = sorted(float(r[9]) for r in ok)
        print("wc: max=%.1f p99=%.1f median=%.1f min=%.1f"
              % (w[-1], w[int(0.99 * (len(w) - 1))], w[len(w) // 2], w[0]))
    with open(os.path.join(WS, "tables", "cpu_used.txt"), "w") as f:
        f.write("%.2f\n" % (tot / 3600.0))


if __name__ == "__main__":
    main()
