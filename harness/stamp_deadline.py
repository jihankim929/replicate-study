#!/usr/bin/env python3
"""Re-stamp a workspace's deadline to LAUNCH + campaign_hours, at the moment of launch.

The ruled definition is "deadline = launch + 168 h exactly" (PI, Rev 20). provision.py stamps it
at PROVISION time, which is the same instant only when a workspace is launched the moment it is
built. It is not: the gate replicate is provisioned, verified and only then started, and the waves
are provisioned before a wave that starts an hour later. Every minute of that gap is a minute
taken off a campaign whose length is pre-registered.

This is the same defect class the section-5 day-count fix already closed once -- there the campaign
lost the gap between launch time and a 09:00 snap; here it loses the gap between provisioning and
launch. Fixing it in one place and not the other would have left the ruling half-implemented.

The change is recorded in the workspace's own record, not applied silently.

IDEMPOTENCY (PI ruling, 2026-08-30). This script re-stamped UNCONDITIONALLY, so every call
moved the deadline to now + campaign_hours. That is correct exactly once -- at first launch --
and wrong every other time. A RESTART goes through launch_sessions.sh, which calls this, so the
restart path silently extended the campaign of any replicate it restarted, while
restart_watch.sh's own INBOX notice told that replicate "your deadline has NOT moved". The two
disagreed and the notice was the one that was wrong.

The stamp is therefore taken ONCE and only once. A workspace that already carries `launched_at`
is already stamped: this reports its existing deadline and writes nothing. `--force` re-stamps
deliberately and says so on stdout, for the case where a workspace really is being launched
afresh. Deadline arithmetic that is SUPPOSED to move a deadline -- the pause extension -- lives
in resume_fleet.py, where it is measured, uniform across arms, and recorded.
"""
import json, subprocess, sys
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def main():
    rep = sys.argv[1]
    ws = f"/home1/users/Bei/ws/{rep}"
    raw = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30",
                          "dirac-bei", f"cat {ws}/WORKSPACE.json"],
                         capture_output=True, text=True, check=True).stdout
    meta = json.loads(raw)
    hours = meta["campaign_hours"]
    before = meta["deadline_kst"]

    # Already stamped -> report, do not move. This is the whole of the idempotency fix.
    force = "--force" in sys.argv[2:]
    if meta.get("launched_at") and not force:
        print(f"  deadline already stamped at launch ({meta['launched_at'][:19]}); "
              f"unchanged at {before[:19]}")
        print(int(datetime.fromisoformat(before).timestamp()))
        return
    if force and meta.get("launched_at"):
        print(f"  --force: RE-STAMPING a workspace already launched at {meta['launched_at'][:19]}")

    launch = datetime.now(KST)
    meta["deadline_kst"] = (launch + timedelta(hours=hours)).isoformat()
    meta["deadline_basis"] = f"launch + {hours} h exactly (stamped at launch)"
    meta["launched_at"] = launch.isoformat()

    body = json.dumps(meta, indent=2) + "\n"
    p = subprocess.run(["ssh", "-o", "BatchMode=yes", "dirac-bei",
                        f"cat > {ws}/WORKSPACE.json"], input=body, text=True)
    if p.returncode:
        sys.exit(f"stamp_deadline: failed to write {ws}/WORKSPACE.json")
    gained = (datetime.fromisoformat(meta["deadline_kst"]) - datetime.fromisoformat(before))
    print(f"  deadline re-stamped at launch: {before[:19]} -> {meta['deadline_kst'][:19]} "
          f"({gained.total_seconds()/60:.1f} min recovered)")
    print(int(datetime.fromisoformat(meta["deadline_kst"]).timestamp()))


if __name__ == "__main__":
    main()
