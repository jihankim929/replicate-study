"""Dirac/PBS glue — STUBBED until the cluster account lands.

Every function here prints exactly what it WOULD do and returns a sentinel. Nothing pretends
to have succeeded. The local mock path is the one exercised by selftest.sh.

Cluster facts already established (work/cluster/README.md, prior campaign):
  * scheduler PBS on bnode0; submit with `qas`, NOT `qsub`
  * a bare `nodes=1:ppn=1` is REJECTED with a bare AssertionError -- a node group is required
  * node groups: aa ab ac amd ax xeonphi ; queue `long` observed with 129 running slots
"""
import shutil, subprocess, sys

STUB = "DIRAC-STUB"


def available() -> bool:
    return shutil.which("qas") is not None


def submit(script, rep_id, node_group="aa", queue="long", dry_run=True):
    cmd = ["qas", "-q", queue, "-l", f"nodes=1:ppn=1:{node_group}",
           "-N", f"{rep_id}_{script}", script]
    if dry_run or not available():
        print(f"[dirac:STUB] would submit: {' '.join(cmd)}", file=sys.stderr)
        return STUB
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def qstat(rep_id, dry_run=True):
    if dry_run or not available():
        print(f"[dirac:STUB] would poll qstat for jobs tagged {rep_id}_", file=sys.stderr)
        return []
    out = subprocess.run(["qstat", "-u", "$USER"], capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if f"{rep_id}_" in l]


def hold_all(rep_id, dry_run=True):
    """charter section 4 hard stop: stop further compute without destroying evidence.

    HOLD, never delete -- a killed job loses the partial output that a post-mortem needs.
    """
    if dry_run or not available():
        print(f"[dirac:STUB] would `qhold` every queued job tagged {rep_id}_ (hold, not delete)", file=sys.stderr)
        return STUB
    for line in qstat(rep_id, dry_run=False):
        subprocess.run(["qhold", line.split()[0]])
    return "held"


def tracejob(job_id, dry_run=True):
    if dry_run or not available():
        print(f"[dirac:STUB] would tracejob {job_id} for resources_used.cput / walltime", file=sys.stderr)
        return {"cput_h": None, "walltime_h": None, "source": STUB}
    out = subprocess.run(["tracejob", "-n", "5", job_id], capture_output=True, text=True).stdout
    return {"raw": out, "source": "tracejob"}
