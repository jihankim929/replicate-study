"""Emit claim-grade (10,000 + 50,000) and G6-reproduction task lists.

Charter s3 sets the Claim-grade cycle counts; Appendix A G6 requires every
number in the Claim to be reproduced in a fresh run from archived inputs before
filing.  A reproduction that reran the identical input with the identical RNG
stream would only test the plumbing, so the reproduction pass sets an explicit,
different `RandomSeed`: it is then a genuine independent estimate and the
agreement between the two is a statistical statement.

usage: claim.py <mode:claim|repro> <wave> <namesfile> <out.tasks> [seed]
"""
import os, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")

NCYC, NINIT = 50000, 10000


def main():
    mode, wave, namesfile, out = sys.argv[1:5]
    seed = sys.argv[5] if len(sys.argv) > 5 else "77001"
    names = [l.strip() for l in open(namesfile) if l.strip() and not l.startswith("#")]
    lines = []
    for n in names:
        safe = n.replace("[", "_").replace("]", "_")
        for p, tp in ((6500000, "65"), (580000, "58")):
            grid = "-" if mode == "claim" else ("seed:" + seed)
            lines.append("%s|%d|%d|%d|%s__%s__p%s|%s"
                         % (n, p, NCYC, NINIT, wave, safe, tp, grid))
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("mode=%s wave=%s structures=%d tasks=%d cycles=%d+%d"
          % (mode, wave, len(names), len(lines), NINIT, NCYC))


if __name__ == "__main__":
    main()
