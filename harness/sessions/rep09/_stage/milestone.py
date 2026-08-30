"""Print a status line only when something notable changed; else print nothing.

State is kept in logs/milestone.state so the caller can be a dumb poll loop.
"""
import os, csv, glob, json

WS = "/home1/users/Bei/ws/rep09"
STATE = os.path.join(WS, "logs/milestone.state")
STEP = 1000

n_ok = n_bad = 0
for p in glob.glob(os.path.join(WS, "tables", "s1_[0-9][0-9].csv")):
    for r in csv.DictReader(open(p)):
        if r.get("status") == "ok":
            n_ok += 1
        else:
            n_bad += 1
cal = 0
cp = os.path.join(WS, "tables", "cal_00.csv")
if os.path.exists(cp):
    cal = sum(1 for r in csv.DictReader(open(cp)) if r.get("status") == "ok")
live = len([x for x in os.popen("bash %s/bin/census.sh 2>/dev/null" % WS).read().split() if x.startswith("rep09_")])

prev = {"milestone": -1, "bad": 0, "warned_live": 0}
if os.path.exists(STATE):
    try:
        prev.update(json.load(open(STATE)))
    except Exception:
        pass

msgs = []
m = n_ok // STEP
if m > prev["milestone"]:
    msgs.append("s1 screen %d/12499 (%.1f%%)  cal=%d  live_jobs=%d  nonok=%d"
                % (n_ok, 100.0 * n_ok / 12499, cal, live, n_bad))
    prev["milestone"] = m
if n_bad > prev["bad"] + 5:
    msgs.append("WARN s1 nonok rows rose to %d (n_ok=%d)" % (n_bad, n_ok))
    prev["bad"] = n_bad
if live < 3 and prev["warned_live"] != live:
    msgs.append("WARN only %d live rep09 jobs (n_ok=%d)" % (live, n_ok))
    prev["warned_live"] = live
if live >= 3:
    prev["warned_live"] = 0
if n_ok >= 12499:
    msgs.append("S1_COMPLETE %d points" % n_ok)

os.makedirs(os.path.dirname(STATE), exist_ok=True)
json.dump(prev, open(STATE, "w"))
for x in msgs:
    print(x)
