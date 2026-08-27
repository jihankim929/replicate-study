#!/usr/bin/env python3
"""Shared-queue depth covariate — how much of the cluster this study is actually taking.

Why this exists (PI ruling 2026-08-28, Flag I). The study-wide ceiling used to manage crowding
by being LOW: 160 was chosen partly so the fleet could not displace other users. That cost
reachability -- at a 10-day horizon it bound before the per-replicate caps did -- and it was a
proxy for the thing that actually matters, which is whether anyone is being displaced. Nobody
was measuring that. The ceiling is now 240 and crowding is managed by measurement plus the
PI's standing authority to lower it as a logged, uniform infrastructure event.

So this is the evidence that authority would be exercised on. It records, every poll:
  - what the whole queue is doing (running / queued, all users);
  - what share of it is ours;
  - how long OTHER users' jobs are waiting -- the actual displacement signal. Our share can
    rise without displacing anyone if the cluster is idle, and a small share can displace
    badly if it is full. Share alone would be the same kind of proxy the ceiling was.

Read-only. It submits nothing and changes nothing.
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "queue_depth.jsonl"
KST = timezone(timedelta(hours=9))
REMOTE = r"""export PATH=$PATH:/usr/local/pbs/bin
qstat -f 2>/dev/null | tr -d '\t' | awk '
  /^Job Id:/ {if(id)print id"|"owner"|"st"|"q"|"nm; id=$3; owner=st=q=nm=""}
  /^ *Job_Owner *=/ {split($3,a,"@"); owner=a[1]}
  /^ *job_state *=/ {st=$3}
  /^ *queue *=/ {q=$3}
  /^ *Job_Name *=/ {nm=$3}
  END {if(id)print id"|"owner"|"st"|"q"|"nm}'
"""


def collect(alias: str) -> dict:
    out = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=30", alias, REMOTE],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode("utf-8", "replace")
    rows = [l.split("|") for l in out.splitlines() if l.count("|") == 4]
    tot = {"R": 0, "Q": 0}
    ours = {"R": 0, "Q": 0}
    others = {"R": 0, "Q": 0}
    by_user = {}
    for _id, owner, st, _q, name in rows:
        st = (st or "").strip()
        if st not in ("R", "Q"):
            continue
        tot[st] += 1
        by_user[owner] = by_user.get(owner, 0) + 1
        # "ours" is the STUDY's footprint, not the account's: replicate jobs are tagged with a
        # replicate id in the job name (charter section 4, cluster etiquette). A job run from
        # the same account that is not tagged is not the study's and must not be counted as it.
        if re.match(r"^(s\d\d|rep\d\d)_", (name or "").strip()):
            ours[st] += 1
        else:
            others[st] += 1
    share = round(100.0 * ours["R"] / tot["R"], 1) if tot["R"] else None
    return {"ts": datetime.now(timezone.utc).isoformat(),
            "ts_kst": datetime.now(KST).strftime("%Y-%m-%d %H:%M"),
            "reachable": bool(rows),
            "total_running": tot["R"], "total_queued": tot["Q"],
            "study_running": ours["R"], "study_queued": ours["Q"],
            "others_running": others["R"], "others_queued": others["Q"],
            "study_share_of_running_pct": share,
            # The displacement signal. Other users' jobs sitting in Q while ours run is the
            # only reading that can distinguish "we are large" from "we are in the way".
            "others_waiting": others["Q"],
            "distinct_users": len(by_user)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssh-alias", default="dirac-bei")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    d = collect(a.ssh_alias)
    if not a.no_log and d["reachable"]:
        with open(LEDGER, "a") as fh:
            fh.write(json.dumps(d) + "\n")
    if a.json:
        print(json.dumps(d, indent=2))
    elif not d["reachable"]:
        print("[queue-depth] cluster did not answer -- nothing recorded")
    else:
        print("[queue-depth] %s KST  queue R=%d Q=%d across %d users | study R=%d Q=%d (%s%% of running) "
              "| others waiting=%d"
              % (d["ts_kst"], d["total_running"], d["total_queued"], d["distinct_users"],
                 d["study_running"], d["study_queued"],
                 d["study_share_of_running_pct"] if d["study_share_of_running_pct"] is not None else "-",
                 d["others_waiting"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
