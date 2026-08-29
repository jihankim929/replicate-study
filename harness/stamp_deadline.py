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
