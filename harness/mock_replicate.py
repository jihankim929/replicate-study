#!/usr/bin/env python3
"""A mock replicate — exercises the full harness loop without a cluster or a real agent.

It is NOT a simulation of research. It reproduces only the things the harness must react to:
budget burn, git-committed record-keeping, escalations in the section 8 format, and a final
report. Its "science" is deliberately inert.

Used by `harness/dryrun_loop.sh` to prove the loop end to end before any real launch.
"""
import argparse, json, random, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

KST = timezone(timedelta(hours=9))


def commit(ws, msg):
    subprocess.run(["git", "add", "-A"], cwd=ws, check=True)
    subprocess.run(["git", "-c", "user.name=replicate", "-c", "user.email=rep@local",
                    "commit", "-q", "-m", msg], cwd=ws, check=True)


def step(ws: Path, day: int, burn_cpu: float, burn_tok: int, queued: int, rng):
    meta = json.loads((ws / "WORKSPACE.json").read_text())
    usage_f = ws / "usage.json"
    u = json.loads(usage_f.read_text()) if usage_f.exists() else {"cpu_h": 0, "tokens": 0, "queued_jobs": 0}
    u["cpu_h"] = round(u["cpu_h"] + burn_cpu, 2)
    u["tokens"] += burn_tok
    u["queued_jobs"] = queued
    usage_f.write_text(json.dumps(u) + "\n")
    (ws / "heartbeat").write_text(datetime.now(KST).isoformat() + "\n")

    with open(ws / "LOG.md", "a") as fh:
        fh.write(f"\n## day {day}\nScreened a batch. Cumulative {u['cpu_h']} CPU-h.\n")
    (ws / "STATE.md").write_text(
        f"# STATE\n\nDay {day}. {u['cpu_h']} CPU-h used of {meta['compute_cpu_h']}.\n"
        f"Open: continue screening.\n")
    with open(ws / "JOBS.md", "a") as fh:
        for j in range(2):
            fh.write(f"| day{day} | `mock{day}{j}` | long | screen batch | n/a | 1h | exit 0 |\n")
    commit(ws, f"day {day}: screened a batch, {u['cpu_h']} CPU-h cumulative")
    return u


def escalate(ws: Path, line: str):
    with open(ws / "ESCALATIONS.md", "a") as fh:
        fh.write(line + "\n")
    commit(ws, "escalation filed")


def final_report(ws: Path, gated: bool):
    (ws / "FINAL_REPORT.md").write_text(
        "# Final report\n\n"
        "1. **Claim:** mock run — no scientific claim is made.\n"
        "2. **Evidence inventory:** see JOBS.md; all entries are mock.\n"
        "3. **Strategy account:** exercise the harness loop.\n"
        "4. **Uncertainty and limitations:** everything; this is not science.\n"
        "5. **Self-assessment:** zero confidence, by construction.\n")
    if gated and (ws / "AUDIT.jsonl").exists():
        with open(ws / "AUDIT.jsonl", "a") as fh:
            fh.write(json.dumps({
                "ts": datetime.now(KST).isoformat(), "structure_id": "mock-0001",
                "gate": "G7", "stage": "post-sim", "apparent_value": 120.0,
                "audit_outcome": "audit_passed", "disposition": "passed",
                "log_ref": "LOG.md#day-2", "commit": "mock"}) + "\n")
    commit(ws, "final report filed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--overspend", action="store_true", help="drive compute past 100% of budget")
    ap.add_argument("--gated", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    ws = Path(a.workspace).resolve()
    rng = random.Random(a.seed)
    meta = json.loads((ws / "WORKSPACE.json").read_text())
    cap = meta["compute_cpu_h"]
    per_day = cap * (0.45 if a.overspend else 0.22)
    for d in range(1, a.days + 1):
        step(ws, d, per_day, 3_000_000, rng.randint(2, 40), rng)
        if d == 1:
            escalate(ws, "[ESC: scientific / two screens disagree on charge balance; which governs?]")
        if d == 2:
            escalate(ws, "[ESC: infra / a job exited 0 and wrote no output file]")
    final_report(ws, a.gated)
    print(f"[mock] {ws.name}: {a.days} days, final report filed")
