#!/usr/bin/env python3
"""Deliberate fleet pause (PI ruling, 2026-08-30). Deadline-neutral by construction.

The supervision host must go offline. Because the replicate PROCESS is local and only its
WORKSPACE is remote (prereg/replicate_runtime_spec.md section 1, PI reading (A)), an offline
host is an offline fleet -- there is no cluster-side executor that could carry the sessions.
So the fleet is stopped DELIBERATELY and on the record rather than dying unattended.

What this preserves, and how:
  * Cluster jobs are NOT touched. They keep running and their results accumulate in the
    workspaces for pickup at resume.
  * Deadlines are NOT moved here. This file records each replicate's deadline AS IT STANDS at
    pause. resume_fleet.py adds the MEASURED pause duration to every one of them, uniformly,
    so the pause costs no campaign time and costs the same campaign time in both arms.
  * Stop is GRACEFUL: it writes the loop's own stop-file and lets the turn in flight finish
    and write its transcript. Killing mid-turn would truncate the agent's own record, which
    for a study whose output IS the record is the failure worth avoiding.

Uniformity is the scientific requirement. The pause is one event with one timestamp applied
to all sixteen; it is not a per-replicate judgement and carries no arm-dependent content.
"""
import json, subprocess, sys
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
REPS = ["rep01","rep02","rep03","rep04","rep05","rep06","rep07","rep08",
        "rep09","rep10","rep11","rep12","rep13","rep15","rep16","rep17"]
REASON = "supervision host unavailable (planned operator absence, 24-48 h)"


def deadline_of(rep):
    out = subprocess.run(
        ["ssh","-o","BatchMode=yes","-o","ConnectTimeout=25","dirac-bei",
         f"grep deadline_kst /home1/users/Bei/ws/{rep}/WORKSPACE.json"],
        capture_output=True, text=True).stdout
    return out.split('"')[3] if '"' in out else None


def main():
    now = datetime.now(timezone.utc)
    rows = {}
    for r in REPS:
        d = deadline_of(r)
        if not d:
            sys.exit(f"pause aborted: could not read deadline for {r}")
        rows[r] = d
    rec = {
        "event": "FLEET_PAUSE",
        "paused_at_utc": now.isoformat(),
        "paused_at_kst": now.astimezone(KST).isoformat(),
        "reason": REASON,
        "uniform_across_arms": True,
        "arm_dependent_content": None,
        "replicates": REPS,
        "n": len(REPS),
        "deadlines_at_pause_kst": rows,
        "cluster_jobs": "left running; nothing qdel'd; outputs accumulate in-workspace for pickup at resume",
        "deadline_policy": "deadline-neutral: resume adds the measured pause duration to every deadline, uniformly",
        "resume_with": "harness/resume_fleet.sh",
        "smoke_arms_excluded": ["s01","s02"],
        "smoke_note": "s01/s02 were already down and are ARCHIVED, not paused; they are not part of this record",
    }
    with open("harness/state/PAUSE.json","w") as f:
        json.dump(rec, f, indent=2); f.write("\n")
    with open("harness/pause_events.jsonl","a") as f:
        f.write(json.dumps({"ts": now.isoformat(), "event": "FLEET_PAUSE",
                            "n": len(REPS), "reason": REASON}) + "\n")
    print(f"PAUSE record written: {now.astimezone(KST).isoformat()} KST, n={len(REPS)}")
    print(f"  reason: {REASON}")


if __name__ == "__main__":
    main()
