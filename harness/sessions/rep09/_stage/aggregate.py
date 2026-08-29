"""Fold a wave's per-job CSVs into one compact table and print a summary.

Usage: aggregate.py <wave> [more_waves...]
Writes tables/<wave>_all.csv (one row per (idx,pressure,ninit,nprod,seed)) and
prints only distribution summaries — never per-structure dumps.
"""
import sys, os, csv, glob, math

WS = "/home1/users/Bei/ws/rep09"
FIELDS = ["idx", "name", "pressure_Pa", "ninit", "nprod", "seed", "load_v",
          "err_v", "load_m", "err_m", "density", "nframeat", "wall_s", "status"]


def collect(wave):
    rows = {}
    dup = 0
    for p in sorted(glob.glob(os.path.join(WS, "tables", "%s_[0-9][0-9].csv" % wave))):
        for r in csv.DictReader(open(p)):
            k = (int(r["idx"]), int(float(r["pressure_Pa"])), int(r["ninit"]),
                 int(r["nprod"]), int(r["seed"]))
            if k in rows:
                dup += 1
            rows[k] = r
    return rows, dup


def main():
    for wave in sys.argv[1:]:
        rows, dup = collect(wave)
        out = os.path.join(WS, "tables", "%s_all.csv" % wave)
        with open(out, "w") as f:
            w = csv.DictWriter(f, FIELDS, extrasaction="ignore")
            w.writeheader()
            for k in sorted(rows):
                w.writerow(rows[k])
        ok = [r for r in rows.values() if r["status"] == "ok"]
        bad = [r for r in rows.values() if r["status"] != "ok"]
        cpu = sum(float(r["wall_s"]) for r in rows.values()) / 3600.0
        loads = sorted(float(r["load_v"]) for r in ok)
        print("WAVE %s: points=%d ok=%d nonok=%d dup=%d cpu_h=%.1f"
              % (wave, len(rows), len(ok), len(bad), dup, cpu))
        if bad:
            st = {}
            for r in bad:
                st[r["status"]] = st.get(r["status"], 0) + 1
            print("  nonok breakdown:", sorted(st.items(), key=lambda x: -x[1])[:6])
        if loads:
            n = len(loads)
            qs = [0, 25, 50, 75, 90, 95, 99, 99.9, 100]
            print("  load_v quantiles: " + "  ".join(
                "p%s=%.1f" % (q, loads[min(n - 1, int(n * q / 100.0))]) for q in qs))
            print("  count >150: %d  >180: %d  >200: %d  >220: %d"
                  % (sum(1 for x in loads if x > 150), sum(1 for x in loads if x > 180),
                     sum(1 for x in loads if x > 200), sum(1 for x in loads if x > 220)))


if __name__ == "__main__":
    main()
