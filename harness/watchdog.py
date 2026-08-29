#!/usr/bin/env python3
"""(b) Watchdog — liveness, budget metering, workspace-isolation audit.

Enforces:
  charter section 4  -- "Usage warnings at 75%; hard stop at 100%" (compute and tokens)
  charter section 4  -- "you operate exclusively inside [workspace path] ... prohibited and audited"
  charter section 6  -- STATE.md "updated before any long wait" (staleness is reported, not punished)

The watchdog NEVER answers science and never edits a replicate's files except INBOX.md,
which is the one channel the harness owns. Charter section 8: Bei handles infrastructure.
"""
import os
import argparse, json, os, subprocess, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C
import liveness as L

KST = timezone(timedelta(hours=9))
# Minutes without the agent writing anything to its own transcript before the harness
# calls the record stale. No longer a heartbeat threshold (PI ruling 2026-08-27).
STALE_ACTIVITY_MIN = 30


def _read_usage(ws: Path) -> dict:
    """Usage ledger. `cpu_h` is the RECORDED meter and is now the job-record basis.

    PI ruling 2026-08-27: the recorded meter is the truthful one. The scheduler figure is kept
    alongside it as `cpu_h_scheduler`, because the size of the gap between them is itself the
    evidence for why the basis changed, and discarding it would erase the defect.
    """
    f = ws / "usage.json"
    if not f.exists():
        return {"cpu_h": 0.0, "cpu_h_scheduler": 0.0, "basis": "none",
                "tokens": 0, "queued_jobs": 0}
    d = json.loads(f.read_text())
    return {"cpu_h": float(d.get("cpu_h", 0)),
            "cpu_h_scheduler": float(d.get("cpu_h_scheduler", 0)),
            "basis": d.get("cpu_h_basis", "unknown"),
            "tokens": int(d.get("tokens", 0)),
            "queued_jobs": int(d.get("queued_jobs", 0))}


def check_liveness(ws: Path, rep: str) -> dict:
    """Liveness = the agent's transcript grew (PI ruling 2026-08-27).

    The heartbeat file is still read and still reported, because it is evidence about the
    wrapper that writes it -- one replicate's went 14.5 h stale while its agent was working.
    It decides nothing.
    """
    r = L.check(rep, update=True)
    hb = ws / "heartbeat"
    hb_age = round((time.time() - hb.stat().st_mtime) / 60, 1) if hb.exists() else None
    if not r["transcripts_present"]:
        state = "no-transcript"
    elif r["baseline_only"]:
        state = "baseline"
    else:
        state = "stale" if r["age_min"] > STALE_ACTIVITY_MIN else "alive"
    return {"state": state, "age_min": r["age_min"], "basis": "transcript-growth",
            "heartbeat_age_min": hb_age, "heartbeat_informational_only": True}


def enforcement(phase: str, resource: str) -> str:
    """Whether a budget event acts on the replicate, or is only written down.

    PI ruling 2026-08-27, smoke phase, compute only: LOG-ONLY. The charter's 75% warning was
    never delivered, because the meter that would have triggered it was undercounting by more
    than an order of magnitude. Delivering a warning now -- or firing a hard stop -- would mean
    enforcing a threshold retroactively, and enforcing it unequally between two arms that
    reached it at different times under a broken instrument. Either would breach the terms of
    the clause being enforced. The deadline in section 5 remains the sole terminator for the
    smoke phase.

    Tokens are unaffected: that meter was never broken, and its cap still ends a campaign
    through the section 5 forced-filing path.

    The main run seals truthful metering with working warnings and full enforcement, so this
    exception is scoped to the phase by name and expires with it.
    """
    if phase == "smoke" and resource == "compute":
        return "log-only"
    return "enforce"


def check_budget(ws: Path, meta: dict) -> list:
    """Returns a list of budget events. One per resource, worst level only."""
    u = _read_usage(ws)
    events = []
    for name, used, cap in (("compute", u["cpu_h"], meta["compute_cpu_h"]),
                            ("tokens", u["tokens"], meta["token_budget"])):
        frac = used / cap if cap else 0.0
        level = ("stop" if frac >= C.STOP_FRACTION else
                 "warn" if frac >= C.WARN_FRACTION else "ok")
        events.append({"resource": name, "used": used, "cap": cap,
                       "fraction": round(frac, 4), "level": level,
                       "enforcement": enforcement(meta["phase"], name)})
    if u["queued_jobs"] > meta["max_queued_jobs"]:
        events.append({"resource": "queued_jobs", "used": u["queued_jobs"],
                       "cap": meta["max_queued_jobs"], "fraction": None, "level": "warn",
                       "enforcement": enforcement(meta["phase"], "queued_jobs")})
    return events


def audit_isolation(ws: Path, repo: Path) -> list:
    """charter section 4: reading/writing outside the workspace is prohibited AND AUDITED.

    What can be checked from the outside, honestly:
      - symlinks escaping the workspace          (a real escape route)
      - a git remote                              (a path back / exfiltration route)
      - absolute paths outside the workspace in the replicate's own files
      - sealed material present by content hash
    What CANNOT be checked from here, and is stated rather than implied:
      - reads that left no trace. Genuine read-auditing needs OS-level mediation
        (a bind-mounted read-only tree, or an audit subsystem). See README, "limits".
    """
    problems = []
    if not ws.exists():
        return [f"workspace missing: {ws}"]
    remotes = subprocess.run(["git", "remote"], cwd=ws, capture_output=True, text=True).stdout.strip()
    if remotes:
        problems.append(f"git remote configured ({remotes}) -- path back to outside")
    sealed = repo / "answer-key"
    sealed_hashes = set()
    if sealed.exists():
        import hashlib
        for p in sealed.rglob("*"):
            if p.is_file():
                sealed_hashes.add(hashlib.sha256(p.read_bytes()).hexdigest())
    import hashlib
    for p in ws.rglob("*"):
        rel = p.relative_to(ws)
        if ".git" in rel.parts:
            continue
        if p.is_symlink():
            tgt = Path(os.path.realpath(p))
            if not str(tgt).startswith(str(ws)):
                problems.append(f"symlink escapes workspace: {rel} -> {tgt}")
            continue
        if not p.is_file() or p.suffix in {".cif", ".sha256"}:
            continue
        if hashlib.sha256(p.read_bytes()).hexdigest() in sealed_hashes:
            problems.append(f"SEALED MATERIAL PRESENT: {rel}")
        try:
            txt = p.read_text(errors="replace")
        except Exception:
            continue
        if str(repo) in txt:
            problems.append(f"references the study repo path: {rel}")
    return problems


def fleet_check(dest_root: Path) -> dict:
    """Study-wide queue ceiling (PI ruling 2026-08-26).

    Independent of, and additional to, the per-replicate cap.

    RULED 160 -> 240 on 2026-08-28 (Flag I): 240 is 1.80x the fleet's 133.33 sustained
    requirement, the same invariant as the per-replicate cap and exactly 20 x 12. At 160 this
    ceiling bound BEFORE the per-replicate caps did, so replicates would have been throttled
    by a study-wide limit they cannot see, cannot attribute, and would experience as their own
    jobs mysteriously not starting -- a confound in the funnel decision the study measures.

    Crowding is now managed by what actually governs it: displacement is MEASURED every poll
    into queue_depth.jsonl, and the PI may lower this ceiling mid-run as a logged, uniform
    infrastructure event (config.fleet_max_queued_jobs / fleet_ceiling.json). Holding the
    number low was a proxy for that and cost reachability to buy it.

    Deliberately NOT a charter clause. A replicate cannot obey a limit defined over other
    replicates it cannot see, and stating it in the charter would disclose the fleet. It binds
    the harness, which is the only party that can enforce it.
    """
    root = Path(dest_root).resolve()
    per, total = {}, 0
    for wsj in sorted(root.glob("*/WORKSPACE.json")):
        ws = wsj.parent
        n = _read_usage(ws)["queued_jobs"]
        per[ws.name] = n
        total += n
    cap, provenance = C.fleet_max_queued_jobs()
    return {"total_queued": total, "cap": cap, "cap_provenance": provenance,
            "per_replicate": per,
            "level": "breach" if total > cap else "ok",
            "headroom": cap - total}


def notify(ws: Path, lines: list, dry_run: bool):
    stamp = datetime.now(KST).isoformat()
    block = f"\n## {stamp} — harness notice\n\n" + "\n".join(f"- {l}" for l in lines) + "\n"
    if dry_run:
        print("[watchdog] (dry-run) would append to INBOX.md:", *lines, sep="\n    ",
              file=sys.stderr)
    else:
        with open(ws / "INBOX.md", "a") as fh:
            fh.write(block)


def act_on_stop(ws: Path, resource: str, dry_run: bool):
    """charter section 4 hard stop. Compute stop holds the queue; token stop ends the session.

    The queue action is Dirac-specific and lives behind dirac.hold_all(); it is a stub until
    the account lands, and says so rather than pretending to have acted.
    """
    import dirac
    notify(ws, [f"**HARD STOP — {resource} budget at 100%.** Charter section 4. "
                f"No further submissions. A final report in the section 7 format remains "
                f"mandatory (section 5): file it from the state you are in."], dry_run)
    if resource == "compute":
        dirac.hold_all(ws.name, dry_run=dry_run)


def run(ws_path, repo, dry_run=False, once=True, json_out=False, isolation=True):
    ws = Path(ws_path).resolve()
    meta = json.loads((ws / "WORKSPACE.json").read_text())
    report = {"replicate": meta["replicate_id"], "ts": datetime.now(KST).isoformat(),
              "liveness": check_liveness(ws, meta["replicate_id"]),
              "budget": check_budget(ws, meta),
              # The isolation audit needs the whole workspace on local disk. When the watchdog
              # runs over the remote bridge it has only the three files the bridge pulls, so it
              # says so instead of reporting a clean audit it did not perform. Isolation is
              # covered on every poll by audit_transcript.py, which reads the local record.
              "isolation": audit_isolation(ws, Path(repo).resolve()) if isolation else [],
              "isolation_audited": bool(isolation)}
    report["overshoot_bound"] = C.overshoot_bound(meta["phase"])
    report["cpu_h_scheduler"] = _read_usage(ws)["cpu_h_scheduler"]
    report["cpu_h_basis"] = _read_usage(ws)["basis"]
    deadline = datetime.fromisoformat(meta["deadline_kst"])
    report["hours_to_deadline"] = round((deadline - datetime.now(KST)).total_seconds() / 3600, 1)

    msgs = []
    for e in report["budget"]:
        if e.get("enforcement") == "log-only" and e["level"] != "ok":
            # Written down, not delivered. Nothing reaches the replicate and no queue is held.
            # stderr: --json emits a machine-readable report on stdout and a diagnostic
            # written there would corrupt it.
            print("[watchdog] LOG-ONLY %s %s at %s / %s -- not delivered (smoke phase, "
                  "PI ruling 2026-08-27)" % (e["resource"], e["level"], e["used"], e["cap"]),
                  file=sys.stderr)
            continue
        if e["level"] == "warn":
            if e["fraction"] is None:          # non-fractional cap, e.g. queued-job count
                msgs.append(f"**Cap exceeded — {e['resource']} at {e['used']}, "
                            f"limit {e['cap']}.** Charter section 4, cluster etiquette.")
            else:
                msgs.append(f"**Usage warning — {e['resource']} at {e['fraction']:.0%} of budget** "
                            f"({e['used']} / {e['cap']}). Charter section 4.")
        elif e["level"] == "stop":
            act_on_stop(ws, e["resource"], dry_run)
    if report["isolation"]:
        msgs.append("**Workspace isolation audit raised findings** (charter section 4): "
                    + "; ".join(report["isolation"]))
    if report["liveness"]["state"] == "stale":
        msgs.append(f"No new activity in your session record for "
                    f"{report['liveness']['age_min']} min. "
                    f"If you are in a long wait, STATE.md should be current (charter section 6).")
    if msgs:
        notify(ws, msgs, dry_run)

    log = Path(os.environ.get("HARNESS_STATE_DIR", Path(__file__).parent)) / "watchdog.jsonl"
    if not dry_run:
        with open(log, "a") as fh:
            fh.write(json.dumps(report) + "\n")
    if json_out:
        print(json.dumps(report, indent=2))
    else:
        print(_fmt(report))
    return report


def _fmt(r):
    ob = r.get("overshoot_bound", {})
    out = [f"[watchdog] {r['replicate']}  T-{r['hours_to_deadline']}h  liveness={r['liveness']['state']}"
           + (f"  poll={ob.get('poll_minutes')}min bound=+{ob.get('overshoot_cpu_h')}CPU-h"
              f" ({ob.get('overshoot_pct_of_budget')}%)" if ob else "")]
    for e in r["budget"]:
        f = "n/a" if e["fraction"] is None else f"{e['fraction']:.1%}"
        out.append(f"    {e['resource']:<12} {e['used']} / {e['cap']}  ({f})  {e['level'].upper()}")
    if not r.get("isolation_audited", True):
        out.append("    isolation    NOT AUDITED HERE (remote bridge; see audit_transcript.py)")
    else:
        out.append(f"    isolation    {'CLEAN' if not r['isolation'] else str(len(r['isolation'])) + ' FINDING(S)'}")
    for p in r["isolation"]:
        out.append(f"      - {p}")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", nargs="?")
    ap.add_argument("--repo", default=str(C.REPO))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-isolation", action="store_true",
                    help="skip the workspace isolation audit (remote bridge: workspace not local)")
    ap.add_argument("--fleet", metavar="DEST_ROOT",
                    help="study-wide queue ceiling check across every workspace under DEST_ROOT")
    a = ap.parse_args()
    if a.fleet:
        f = fleet_check(Path(a.fleet))
        if a.json:
            print(json.dumps(f, indent=2))
        else:
            print(f"[fleet] queued {f['total_queued']} / {f['cap']}  "
                  f"headroom {f['headroom']}  {f['level'].upper()}   [{f['cap_provenance']}]")
            for k, v in sorted(f["per_replicate"].items()):
                print(f"    {k:<6} {v}")
            if f["level"] == "breach":
                print("    !! study-wide ceiling breached -- hold submissions before adding more")
        sys.exit(1 if f["level"] == "breach" else 0)
    if not a.workspace:
        ap.error("workspace is required unless --fleet is given")
    run(a.workspace, a.repo, a.dry_run, json_out=a.json, isolation=not a.no_isolation)
