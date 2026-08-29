"""Print how many points of jobs/<wave>_<k>.tasks are not yet recorded ok.

Used by the autopilot to decide whether a chunk is worth resubmitting.
"""
import sys, os, csv
WS = "/home1/users/Bei/ws/rep09"

wave, k = sys.argv[1], sys.argv[2]
tasks = set()
tp = os.path.join(WS, "jobs", "%s_%s.tasks" % (wave, k))
if os.path.exists(tp):
    for L in open(tp):
        L = L.strip()
        if L:
            p = L.split(",")
            tasks.add((int(p[0]), int(float(p[1])), int(p[2]), int(p[3]), int(p[4])))

done = set()
cp = os.path.join(WS, "tables", "%s_%s.csv" % (wave, k))
if os.path.exists(cp):
    for r in csv.DictReader(open(cp)):
        if r.get("status") == "ok":
            done.add((int(r["idx"]), int(float(r["pressure_Pa"])), int(r["ninit"]),
                      int(r["nprod"]), int(r["seed"])))
print(len(tasks - done))
