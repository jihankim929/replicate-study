"""Fast reduced-precision descriptor pass, for seeding the first GCMC wave.

Same engine as descsweep.py but 2,000 Widom points instead of 12,000, which
costs ~0.9 s per structure instead of ~4.5 s.  The void fractions carry ~2 %
sampling noise at that setting -- useless for a reported number, entirely
adequate for deciding which few hundred structures to simulate first.  The full
12,000-point sweep runs on the queue and supersedes this for the real ranking.

usage: coarse.py <shard> <nshards> <out.csv>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import descsweep as d
import mofcore as mc

NPTS = 3000


def main():
    shard, nsh, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    uff = mc.load_uff(d.UFFP)
    files = sorted(f for f in os.listdir(d.DB) if f.endswith(".cif"))
    mine = files[shard::nsh]
    with open(out, "w") as fh:
        fh.write(",".join(d.COLS) + "\n")
        for i, f in enumerate(mine):
            try:
                row = d.describe(os.path.join(d.DB, f), uff, NPTS)
                fh.write(",".join(('"%s"' % v) if isinstance(v, str) else
                                  ("%.6g" % v if isinstance(v, float) else str(v))
                                  for v in row) + "\n")
            except Exception as e:
                fh.write('"%s",ERROR,,,,,,,,,,,,,,,"","%s",,,,,,,,,,,,,""\n'
                         % (f[:-4], str(e).replace(",", ";")[:100]))
            if i % 50 == 0:
                fh.flush()


if __name__ == "__main__":
    main()
