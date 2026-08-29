#!/usr/bin/env python3
"""Re-render CHARTER.md and CHARTER_ADDENDUM.md into already-provisioned workspaces.

A charter amendment after provisioning does not justify rebuilding a workspace: the database is
12,499 files per replicate and re-copying it to change two documents would be 187,000 file
operations to move a few hundred bytes, on a cluster whose network already dropped once today.
This renders the two documents through the SAME pipeline provision.py uses -- split_charter after
render_phase_prose after render_phase_rows -- and replaces only those two files.

It verifies AFTER writing, on the cluster, that the arm split still holds: the gated copy carries
Appendix A and the ungated copy does not. A re-render that silently handed the wrong arm its
charter would destroy the treatment, and it would look like a successful copy.
"""
import subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import provision as P, config as C

MARKER = C.APPENDIX_MARKER


def render(arm, phase):
    src = C.SOURCE_ALLOWLIST["charter"].read_text()
    ch = P.split_charter(P.render_phase_prose(P.render_phase_rows(src, phase), phase), arm)
    ad = P.render_phase_prose(
        P.render_phase_rows(C.SOURCE_ALLOWLIST["addendum"].read_text(), phase), phase)
    return ch, ad


def push(rep, body, name):
    ws = f"/home1/users/Bei/ws/{rep}"
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=60",
                        "dirac-bei", f"cat > {ws}/{name}"], input=body, text=True)
    if r.returncode:
        sys.exit(f"FAILED writing {name} to {rep}")


def main():
    reps = sys.argv[1:]
    if not reps:
        reps = [i for i in C.RATIFIED["phases"]["main"]["ids"] if i != "rep01"]
    bad = 0
    for rep in reps:
        arm = C.arm_of(rep)                   # the sealed assignment, same source provision uses
        phase = C.phase_of(rep)
        ch, ad = render(arm, phase)
        assert (MARKER in ch) == (arm == "gated"), f"{rep}: appendix/arm mismatch BEFORE sending"
        push(rep, ch, "CHARTER.md")
        push(rep, ad, "CHARTER_ADDENDUM.md")
        chk = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "dirac-bei",
             f"grep -c '{MARKER}' /home1/users/Bei/ws/{rep}/CHARTER.md; "
             f"grep -c 'Pinned files, claims and descriptors' /home1/users/Bei/ws/{rep}/CHARTER.md; "
             # count the CLAUSE BULLET, not the string: the revision-record row quotes the
             # clause title too, and split_charter keeps that row for the gated arm and drops it
             # for the ungated one -- so a bare grep reports 2 vs 1 for an identical clause.
             f"grep -c '^- \\*\\*Cost mechanics and discipline' /home1/users/Bei/ws/{rep}/CHARTER.md"],
            capture_output=True, text=True).stdout.split()
        appx, pinned, cost = ((int(chk[0]), int(chk[1]), int(chk[2]))
                              if len(chk) == 3 else (-1, -1, -1))
        ok = (appx == (1 if arm == "gated" else 0)) and pinned == 1 and cost == 1
        print(f"  {rep:<7} arm={arm:<8} appendixA={appx} §3-pinned={pinned} §4-cost={cost}  "
              f"{'OK' if ok else 'MISMATCH'}")
        bad += 0 if ok else 1
    print(f"  re-rendered {len(reps)} workspace(s), {bad} mismatch(es)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
