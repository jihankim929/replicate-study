#!/usr/bin/env python3
"""Restore campaign time lost to a verified harness fault, per replicate, and record why.

WHAT THIS IS FOR. On 2026-08-30 ten of the sixteen main replicates stopped between 12:26 and
14:06 KST because `session_loop_headless.sh` ended a campaign after five consecutive sub-minute
turns -- a condition it read as a broken loop and which was in fact an agent correctly waiting on
cluster jobs. Every restart that followed was killed by systemd within about twenty seconds,
because `restart_watch.sh` runs inside `study.poll.service` (Type=oneshot, default
KillMode=control-group) and started the replacement `screen` in the poll's own cgroup. Thirty
restarts died that way, the counters reached their cap of 3, and the ten were left down for
10-12 h. REPORT 006 sections 2(a) and 2(b); both defects fixed and the restoration ruled by the
PI on 2026-08-31.

THE RULE IT GIVES EFFECT TO is the standing one already in `resume_fleet.py`:

    The 168-hour entitlement is LIVE-SESSION time. Campaign time lost to a VERIFIED HARNESS
    FAULT is restored to the affected replicate, with cause and measurement cited.

It is CAUSE-KEYED and therefore ARM-BLIND: the cause is one harness defect that struck whichever
replicates happened to be idle at the time, the entry written for each is identical in form, and
nothing here reads differently for one arm than for the other. Bei does not consult the arm map.

IT IS NOT THE UNIFORM PAUSE EXTENSION. That compensated an interval every replicate shared and
was uniform by design. This compensates an outage that ten replicates suffered and six did not,
and it is therefore PER-REPLICATE and measured individually -- a flat figure would over-restore
some and under-restore others, and the spread here is 10.0 h to 12.0 h.

MEASUREMENT. From the moment the replicate's session loop ended -- the timestamp of the guard's
own line in `harness/sessions/<rep>.loop.log`, which is in the repository and auditable -- to the
moment this script writes. Inside that window each replicate also had three restarts that lived
about twenty seconds each before being killed. They are NOT subtracted: ~1 min in total, they
advanced no campaign work, and the harness killed them. The rounding is in the replicate's favour
by under a minute and this sentence is the disclosure.

PASS 1 FIRST, ABORT AS A WHOLE. Every live deadline is read before anything is written, exactly
as the resume does. A deadline that cannot be read is an unexplained state and the right response
is to change nothing at all rather than to restore some replicates and not others.

    ./harness/restore_downtime.py --dry-run     # read, compute, print, write nothing
    ./harness/restore_downtime.py --apply
"""
import json, re, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KST = timezone(timedelta(hours=9))
WS = "/home1/users/Bei/ws"
LEDGER = Path(__file__).resolve().parent / "restorations.jsonl"

CAUSE = ("hot-loop guard ended the campaign on five consecutive sub-minute turns that were an "
         "agent correctly waiting on queued cluster jobs (REPORT 006 s2a), and all three "
         "restarts were killed by systemd within ~20 s because the replacement screen was "
         "started inside study.poll.service's control group (REPORT 006 s2b)")
RULING = "PI ruling 2026-08-31, on REPORT 006 section 7(4)"

GUARD_LINE = re.compile(r"^(\S+) 5 consecutive sub-minute turns, stopping to avoid a hot loop")

NOTE = """
## {stamp} — harness notice (infrastructure)

- **Your session stopped {down_h:.2f} h ago because of a harness defect, and it has been
  restarted.** This was not caused by anything you did, it is not a judgement about your work,
  and it carries no instruction about your science.
- **What happened.** The wrapper that runs your session ends it if five turns in a row finish in
  under a minute, on the assumption that means something is broken. It does not always mean that:
  when your work is all queued on the cluster, short turns are the correct behaviour and the
  charter asks for them. Your session was ended for waiting properly. The wrapper now backs off
  to a ten-minute pause between turns in that situation instead of stopping.
- **CORRECTION — the restart notices above are false.** Between them, three notices in this file
  say "Your session was restarted by the harness (restart N of 3)". No such restart ever ran: each
  one was killed about twenty seconds after it started, before it could do anything, by a second
  defect in how the harness launches sessions. Disregard all three. The repeated "No new activity
  in your session record" notices below them were written to a workspace whose session was not
  running and can also be disregarded.
- **Your deadline has been extended by {down_h:.4f} h**, the measured time your session was down,
  from **{before}** to **{after}**. Under the standing rule ratified 2026-08-30 -- the 168-hour
  entitlement is live-session time, and campaign time lost to a verified harness fault is
  restored to the affected replicate -- that time is owed to you rather than granted. Measured
  from {from_ts} (the moment your session loop ended, recorded in the harness log) to {to_ts}.
- **Your cluster jobs were never touched.** Nothing was cancelled. They kept running while your
  session was down and their outputs have been accumulating in your workspace. There is very
  likely finished work waiting for you: collect it before planning.
- Your compute, token and spend budgets are unchanged, and your workspace and git record are as
  you left them. Reconcile against `STATE.md`, then read `CHARTER.md` §5 -- it carries a new
  clause -- and `usage.json`, which now publishes your spend.
"""


def ssh(cmd, **kw):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30",
                           "dirac-bei", cmd], capture_output=True, text=True, **kw)


def loop_end(rep: str):
    """The timestamp of the guard line that ended this replicate's campaign, from the repo log."""
    log = ROOT / "harness" / "sessions" / f"{rep}.loop.log"
    stamp = None
    for line in log.read_text(errors="replace").splitlines():
        m = GUARD_LINE.match(line)
        if m:
            stamp = m.group(1)
    if not stamp:
        return None
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def main():
    apply = "--apply" in sys.argv[1:]
    dry = "--dry-run" in sys.argv[1:]
    if apply == dry:
        sys.exit("pass exactly one of --dry-run or --apply")
    reps = [a for a in sys.argv[1:] if a.startswith("rep")]
    if not reps:
        sys.exit("name the replicates to restore, e.g. --apply rep02 rep03 ...")

    now = datetime.now(KST)

    # --- evidence: when did each campaign actually stop -------------------------------------
    downtime = {}
    for r in reps:
        end = loop_end(r)
        if end is None:
            sys.exit(f"restore: no hot-loop guard line in {r}.loop.log -- refusing to restore a "
                     f"replicate whose stop this script cannot evidence.")
        downtime[r] = (end, (now - end).total_seconds() / 3600.0)

    # --- PASS 1: read every live deadline before writing anything ----------------------------
    print(f"  PASS 1 (read-only): {len(reps)} live deadline reads over ssh dirac-bei")
    live, problems = {}, []
    for r in reps:
        out = ssh(f"cat {WS}/{r}/WORKSPACE.json")
        if out.returncode:
            problems.append(f"{r}: workspace unreadable"); continue
        try:
            live[r] = json.loads(out.stdout)
        except ValueError:
            problems.append(f"{r}: WORKSPACE.json does not parse")
    if problems:
        print("  ABORTING -- nothing has been written:")
        for p in problems:
            print("   ", p)
        sys.exit(1)
    print(f"  verified: all {len(reps)} workspaces read\n")

    print(f"  {'rep':7} {'down since (UTC)':22} {'hours':>7}  {'deadline before':19} -> "
          f"{'deadline after':19}")
    records = []
    for r in reps:
        end, hours = downtime[r]
        meta = live[r]
        before = datetime.fromisoformat(meta["deadline_kst"])
        after = before + timedelta(hours=hours)
        print(f"  {r:7} {end.astimezone(timezone.utc).isoformat()[:19]:22} {hours:7.4f}  "
              f"{before.isoformat()[:19]} -> {after.isoformat()[:19]}")
        records.append({"replicate": r, "hours": round(hours, 4),
                        "from_ts": end.astimezone(timezone.utc).isoformat(),
                        "to_ts": now.isoformat(),
                        "deadline_before_kst": meta["deadline_kst"],
                        "deadline_after_kst": after.isoformat(),
                        "cause": CAUSE, "ruling": RULING})

    if dry:
        print(f"\n  (dry-run) {len(records)} deadline(s) would move; nothing written.")
        return

    # --- apply -------------------------------------------------------------------------------
    stamp = now.isoformat()
    for rec in records:
        r = rec["replicate"]
        meta = live[r]
        prior = float(meta.get("fault_restoration_hours") or 0.0)
        meta["deadline_kst"] = rec["deadline_after_kst"]
        meta["deadline_basis"] = (
            f"{meta.get('deadline_basis','')} + {rec['hours']:.4f} h restored for harness-fault "
            f"downtime {rec['from_ts'][:19]}Z to {rec['to_ts'][:19]} ({RULING})").strip()
        meta["fault_restoration_hours"] = round(prior + rec["hours"], 4)
        body = json.dumps(meta, indent=2) + "\n"
        if ssh(f"cat > {WS}/{r}/WORKSPACE.json", input=body).returncode:
            sys.exit(f"restore: FAILED writing WORKSPACE.json for {r} -- stop and inspect")
        note = NOTE.format(stamp=stamp, down_h=rec["hours"],
                           before=rec["deadline_before_kst"][:19],
                           after=rec["deadline_after_kst"][:19],
                           from_ts=rec["from_ts"][:19] + "Z", to_ts=rec["to_ts"][:19])
        if ssh(f"cat >> {WS}/{r}/INBOX.md", input=note).returncode:
            sys.exit(f"restore: FAILED writing INBOX.md for {r} -- stop and inspect")
        with open(LEDGER, "a") as fh:
            fh.write(json.dumps({"ts": stamp, "event": "FAULT_RESTORATION", **rec}) + "\n")
        print(f"  {r}: +{rec['hours']:.4f} h, notice delivered")

    # --- verify: re-read every deadline and match it against what we wrote --------------------
    print("\n  PASS 2 (read-back): confirming every deadline is the extended value")
    bad = 0
    for rec in records:
        out = ssh(f"cat {WS}/{rec['replicate']}/WORKSPACE.json")
        got = json.loads(out.stdout).get("deadline_kst") if out.returncode == 0 else None
        ok = got == rec["deadline_after_kst"]
        bad += 0 if ok else 1
        print(f"  {rec['replicate']:7} {'OK' if ok else 'MISMATCH: ' + str(got)}")
    print(f"\n  {len(records)} restored, {bad} mismatch(es)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
