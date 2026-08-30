"""Summarise the Tier-1 screen and emit candidate id lists for later tiers.

Usage:
  select.py summary
  select.py top <n> <outfile>          top n by screened N(65 bar)
  select.py above <value> <outfile>    every structure with N65 >= value

Prints distributions only, never per-structure dumps beyond a short head.
"""
import os, sys, csv, glob

WS = "/home1/users/Bei/ws/rep09"


def load():
    dens = {int(r["id"]): float(r["density_gcm3"])
            for r in csv.DictReader(open(os.path.join(WS, "manifests/density.csv")))}
    name = {int(r["id"]): r["cif"]
            for r in csv.DictReader(open(os.path.join(WS, "manifests/structures.csv")))}
    rows = {}
    for p in glob.glob(os.path.join(WS, "tables", "s1_[0-9][0-9].csv")):
        for r in csv.DictReader(open(p)):
            if r.get("status") == "ok" and int(float(r["pressure_Pa"])) == 6500000:
                rows[int(r["idx"])] = (float(r["load_v"]), float(r["err_v"]))
    return dens, name, rows


def summary(dens, name, rows):
    n = len(rows)
    v = sorted(x[0] for x in rows.values())
    print("screened %d of 12499 (%.1f%%)" % (n, 100.0 * n / 12499))
    if not n:
        return
    qs = [0, 10, 25, 50, 75, 90, 95, 99, 100]
    print("N65 quantiles: " + "  ".join(
        "p%d=%.1f" % (q, v[min(n - 1, int(n * q / 100.0))]) for q in qs))
    for t in (200, 220, 240, 250, 260, 270):
        print("  N65 >= %3d : %d structures" % (t, sum(1 for x in v if x >= t)))
    top = sorted(rows.items(), key=lambda kv: -kv[1][0])[:12]
    print("top 12 by screened N65:")
    for i, (ld, er) in top:
        print("  id=%-6d rho=%.3f  N65=%7.2f +/- %5.2f  %s"
              % (i, dens[i], ld, er, name[i]))


def main():
    dens, name, rows = load()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if cmd == "summary":
        summary(dens, name, rows)
        return
    if cmd == "top":
        k = int(sys.argv[2])
        sel = [i for i, _ in sorted(rows.items(), key=lambda kv: -kv[1][0])[:k]]
    elif cmd == "above":
        t = float(sys.argv[2])
        sel = [i for i, v in rows.items() if v[0] >= t]
    else:
        raise SystemExit("unknown command")
    with open(sys.argv[3], "w") as f:
        for i in sorted(sel):
            f.write("%d\n" % i)
    print("wrote %d ids to %s" % (len(sel), sys.argv[3]))


if __name__ == "__main__":
    main()
