"""Dirac/PBS glue — STUBBED until the cluster account lands.

Every function here prints exactly what it WOULD do and returns a sentinel. Nothing pretends
to have succeeded. The local mock path is the one exercised by selftest.sh.

Cluster facts already established (work/cluster/README.md, prior campaign):
  * scheduler PBS on bnode0; submit with `qas`, NOT `qsub`
  * a bare `nodes=1:ppn=1` is REJECTED with a bare AssertionError -- a node group is required
  * node groups: aa ab ac amd ax xeonphi ; queue `long` observed with 129 running slots
"""
import os, shutil, subprocess, sys

STUB = "DIRAC-STUB"

# MEASURED 2026-08-29, first real use of this module. Two facts the stub had wrong:
#
#  1. `qas` is NOT on a non-interactive PATH. It lives at /usr/local/mjs/qas and is picked up
#     only by an interactive profile, so `shutil.which("qas")` returned False over ssh and
#     `available()` silently reported the cluster unreachable.
#  2. `qas` takes the qsub FILE as its first positional argument and passes nothing through.
#     Flags are not accepted: `qas -q long -l nodes=... file` fails inside qas.py with
#     `AssertionError: -q does not exists`, because it treats "-q" as the script path.
#     Queue, node group and job name therefore belong in `#PBS` directives INSIDE the script.
#
# Both were found by submitting 40 real jobs. Neither would have surfaced in a dry run, and
# `launch.sh` calls nothing here, so the first main-run submission would have been the first
# time this path executed.
QAS_DIR = "/usr/local/mjs"


def _qas():
    return shutil.which("qas") or (os.path.join(QAS_DIR, "qas")
                                   if os.path.exists(os.path.join(QAS_DIR, "qas")) else None)


def available() -> bool:
    return _qas() is not None


def submit(script, rep_id, node_group="aa", queue="long", dry_run=True):
    # The script must already carry its own #PBS -N / -q / -l directives; qas passes no flags.
    cmd = [_qas() or "qas", script]
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
