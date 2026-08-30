#!/usr/bin/env python3
"""Resume the paused fleet, deadline-neutrally. Called by harness/resume_fleet.sh.

THE ONE THING THIS FILE EXISTS TO GET RIGHT. A pause the campaign did not choose must cost the
campaign no time, and must cost BOTH ARMS THE SAME TIME. So the extension is not per-replicate
judgement and not a round number: it is the single measured wall-clock interval between the
pause stamp and this run, added to all sixteen deadlines identically.

  new_deadline[r] = deadline_at_pause[r] + (resumed_at - paused_at)

`deadline_at_pause` is read from the PAUSE record, not from the live workspace, because the
record is what was true when the fleet stopped. The live value is still checked against it and a
mismatch ABORTS: a deadline that moved while the fleet was down is an unexplained edit, and
extending it would silently ratify whatever did it.

Nothing here re-derives a deadline from `now + campaign_hours`. That is what stamp_deadline.py
does at first launch only, and its unconditional form is the defect that moved rep06's deadline
by 11.3 h on 2026-08-30.
"""
import json, subprocess, sys
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
PAUSE_FILE = "harness/state/PAUSE.json"
NOTE = """
## {stamp} — harness notice (infrastructure)

- Your session was **paused and resumed** by the harness. The pause was an infrastructure
  event: the machine that hosts the agent sessions was unavailable. It was not caused by
  anything you did, it is not a judgement about your work, and it carries no instruction.
- The pause was **uniform across the study**: every replicate was stopped by the same ruling at
  the same time, for the same measured duration, and resumed together.
- **Your deadline has been extended by exactly the pause duration** ({pause_h:.4f} h), so the
  pause costs you no campaign time. Your new deadline is **{new_deadline}**. Your compute,
  token and spend budgets are unchanged.
- **Your cluster jobs were never touched.** Nothing was cancelled. Jobs continued running
  while your session was down and their outputs accumulated in your workspace; results that
  landed during the pause are waiting for you to collect.
- Your workspace, git record and budget counters are unchanged. Reconcile against `STATE.md`
  and check for finished jobs before continuing.
"""


def ssh(cmd, **kw):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30",
                           "dirac-bei", cmd], capture_output=True, text=True, **kw)


def main():
    try:
        rec = json.load(open(PAUSE_FILE))
    except FileNotFoundError:
        sys.exit(f"resume: no pause record at {PAUSE_FILE} -- the fleet is not paused.")

    paused_at = datetime.fromisoformat(rec["paused_at_utc"])
    resumed_at = datetime.now(timezone.utc)
    pause_s = (resumed_at - paused_at).total_seconds()
    if pause_s <= 0:
        sys.exit("resume: pause duration is not positive -- refusing.")
    pause_h = pause_s / 3600.0
    reps = rec["replicates"]
    at_pause = rec["deadlines_at_pause_kst"]

    print(f"  paused  {paused_at.astimezone(KST).isoformat()[:19]} KST")
    print(f"  resumed {resumed_at.astimezone(KST).isoformat()[:19]} KST")
    print(f"  measured pause: {pause_h:.4f} h ({pause_s:.0f} s) -- applied to all {len(reps)} identically\n")

    # PASS 1: verify every live deadline still equals the recorded one. Abort as a whole.
    live = {}
    for r in reps:
        out = ssh(f"grep deadline_kst /home1/users/Bei/ws/{r}/WORKSPACE.json").stdout
        if '"' not in out:
            sys.exit(f"resume: cannot read deadline for {r} -- aborting before any change.")
        live[r] = out.split('"')[3]
        if live[r] != at_pause[r]:
            sys.exit(f"resume: {r} deadline moved during the pause\n"
                     f"    recorded at pause: {at_pause[r]}\n"
                     f"    live now:          {live[r]}\n"
                     f"  Refusing to extend an unexplained edit. Investigate, then rerun.")
    print(f"  verified: all {len(reps)} live deadlines match the pause record\n")

    # PASS 2: extend. Only after every replicate has been verified.
    new_deadlines = {}
    for r in reps:
        new = (datetime.fromisoformat(at_pause[r]) + timedelta(seconds=pause_s))
        new_deadlines[r] = new.isoformat()
        payload = json.dumps({
            "deadline_kst": new.isoformat(),
            "deadline_basis": (f"launch + 168 h, "
                               f"plus {pause_h:.4f} h of recorded fleet pause "
                               f"(harness/state/PAUSE.json, uniform across arms)"),
            "paused_at_kst": paused_at.astimezone(KST).isoformat(),
            "resumed_at_kst": resumed_at.astimezone(KST).isoformat(),
            "pause_seconds": round(pause_s, 3),
        })
        p = ssh(f"cd /home1/users/Bei/ws/{r} && python3 -c \"import json,sys; "
                f"m=json.load(open('WORKSPACE.json')); m.update(json.loads(sys.argv[1])); "
                f"open('WORKSPACE.json','w').write(json.dumps(m,indent=2)+chr(10))\" "
                f"{json.dumps(payload)}")
        if p.returncode:
            sys.exit(f"resume: failed to extend {r}: {p.stderr[:300]}")
        print(f"  {r}: {at_pause[r][:19]} -> {new.isoformat()[:19]}")

    # PASS 3: one uniform INBOX note each.
    stamp = resumed_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    for r in reps:
        note = NOTE.format(stamp=stamp, pause_h=pause_h, new_deadline=new_deadlines[r][:19])
        p = subprocess.run(["ssh", "-o", "BatchMode=yes", "dirac-bei",
                            f"cat >> /home1/users/Bei/ws/{r}/INBOX.md"],
                           input=note, text=True, capture_output=True)
        if p.returncode:
            print(f"  !! {r}: INBOX note FAILED: {p.stderr[:200]}")
    print(f"\n  INBOX note delivered to {len(reps)} replicates (identical text, no arm-dependent content)")

    # PASS 4: reset the restart counters by appending a marker. Append-only; nothing deleted.
    with open("harness/restarts.jsonl", "a") as f:
        f.write(json.dumps({"event": "COUNTER_RESET", "ts": stamp,
                            "reason": "deliberate fleet pause/resume, not replicate failure",
                            "scope": reps}, separators=(",", ":")) + "\n")
    print("  restart counters reset (COUNTER_RESET marker appended to harness/restarts.jsonl)")

    rec.update({"resumed_at_utc": resumed_at.isoformat(), "pause_seconds": round(pause_s, 3),
                "pause_hours": round(pause_h, 4), "new_deadlines_kst": new_deadlines})
    with open("harness/pause_events.jsonl", "a") as f:
        f.write(json.dumps({"ts": resumed_at.isoformat(), "event": "FLEET_RESUME",
                            "pause_hours": round(pause_h, 4), "n": len(reps)}) + "\n")
    with open("harness/state/LAST_RESUME.json", "w") as f:
        json.dump(rec, f, indent=2); f.write("\n")
    print("  resume recorded in harness/pause_events.jsonl and harness/state/LAST_RESUME.json")


if __name__ == "__main__":
    main()
