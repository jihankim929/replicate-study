#!/usr/bin/env python3
"""Figure-2 extractions. Read-only, mechanical, no interpretation.

TWO OF THE THREE REQUESTED FILES ARE BUILT HERE. `fig2_jobs.csv` is NOT, and the reason is in
analysis/README.md: the per-completed-job records it specifies do not exist in the shape required,
in the collected record or in the workspace metering source.

DEFINITIONS ARE DECLARED HERE, NOT INHERITED. The request asks for "the same definitions already
used for the timing ranges in the manuscript". There is no manuscript in this repository -- the
rubric, seal_notes.md and STATE.md all record its absence -- so no definitions could be inherited
and every rule below is stated explicitly instead. If the manuscript's definitions differ, these
columns must be rebuilt against them; nothing here should be read as reproducing them.
"""
import csv, json, re, sys, pathlib, datetime as dt
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"harness")); import behavioral_extract as B

EXCLUDED = {"2020[Fe][hcb]2","2021[Cu][sql]2","2010[Co][tbo]3","2017[Fe][nan]3",
            "2015[Cu][pcu]3","2009[Cd][nan]3"}
AGENT = re.compile(r'__\d+of\d+|_DENET|\+DEAQ|@(f|me)\d+')
BASE  = re.compile(r'^(\d{4}\[[A-Za-z]{1,6}\]\[[a-z]{3}\]\d)')
GROUP = {"gated":"C","ungated":"U"}

def klass(name):
    if AGENT.search(name): return "agent_modified"
    m = BASE.match(name)
    return "excluded" if (m and m.group(1) in EXCLUDED) else "retained"

def launch(r): return dt.datetime.fromisoformat(json.load(open(B.COLL/r/"WORKSPACE.json"))["launched_at"])
def hrs(ts, L0): return f"{(ts-L0).total_seconds()/3600:.2f}"

def events():
    ms = {}
    for row in csv.DictReader(open(ROOT/"analysis/first_day.csv")):
        ms[(row["rep"], row["milestone"])] = row["t_plus_hours"]
    out=[]
    for r in B.REPS:
        L0 = launch(r); u = json.load(open(B.COLL/r/"usage.json"))
        mt = dt.datetime.fromtimestamp((B.COLL/r/"REPORT.md").stat().st_mtime,
                                       dt.timezone(dt.timedelta(hours=9)))
        gl = [l for l in (B.COLL/r/"git-log.txt").read_text(errors="replace").split("\n")
              if re.match(r'^[0-9a-f]{40}', l)]
        last = max(dt.datetime.strptime(l.split()[1]+" "+l.split()[2], "%Y-%m-%d %H:%M:%S")
                   .replace(tzinfo=dt.timezone(dt.timedelta(hours=9))) for l in gl)
        sf = u.get("spend_fraction", 0.0)
        end = "spend_cap" if u.get("spend_level") == "stop" or sf >= 1.0 else "filing"
        out.append(dict(run=r, group=GROUP[B.ARM[r]],
            strategy="",                                   # see README: no D/B/S/M taxonomy exists
            t_first_job_submitted=ms.get((r,"first_job_submitted"),""),
            t_first_declared_strategy=ms.get((r,"first_stated_strategy"),""),
            t_first_high_accuracy_calc=ms.get((r,"first_claim_grade"),""),
            t_first_encounter_cu_sql=ms.get((r,"first_mention_2021[Cu][sql]2"),""),
            t_final_filing=hrs(mt,L0), t_session_end=hrs(last,L0), end_reason=end,
            spend_fraction=f"{sf:.3f}"))
    return out

def claims():
    out=[]
    champ={}
    for row in csv.DictReader(open(ROOT/"analysis/claim_table.csv")):
        champ[row["rep"]]=row
        out.append(dict(run=row["rep"], group=GROUP[row["arm"]], structure_id=row["champion"],
            rank_in_run="1", reported_value=row["value"].split("±")[0].strip(),
            reported_uncertainty=(row["value"].split("±")[1].strip() if "±" in row["value"] else ""),
            accuracy_tier="high" if row["claim_grade"]=="y" else "low",
            structure_class=klass(row["champion"]),
            reported_how="ranked_list" if row["rep"] in RANKED else "prose"))
    for row in csv.DictReader(open(ROOT/"analysis/leaderboards.csv")):
        if row["entry_class"]=="not-filed" or row["rank"]=="1": continue
        out.append(dict(run=row["rep"], group=GROUP[row["arm"]], structure_id=row["structure"],
            rank_in_run=row["rank"], reported_value=row["wc"], reported_uncertainty=row["error"],
            accuracy_tier="", structure_class=klass(row["structure"]), reported_how="ranked_list"))
    for row in csv.DictReader(open(ROOT/"analysis/leaderboards_prose.csv")):
        if row["structure_as_named"].startswith("(") : continue
        if row["rep"] in champ and row["structure_as_named"]==champ[row["rep"]]["champion"]: continue
        out.append(dict(run=row["rep"], group=GROUP[row["arm"]],
            structure_id=row["structure_as_named"], rank_in_run="",
            reported_value=row["stated_value"],
            reported_uncertainty="" if row["stated_error"] in ("none stated","") else row["stated_error"],
            accuracy_tier="high" if "claim grade" in row["value_kind"] else
                          ("low" if "floor" in row["value_kind"] else ""),
            structure_class=klass(row["structure_as_named"]), reported_how="prose"))
    return out

RANKED={r["rep"] for r in csv.DictReader(open(ROOT/"analysis/leaderboards.csv"))
        if r["entry_class"]!="not-filed"}

def write(name, cols, rows):
    p=ROOT/"analysis"/name
    with p.open("w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=cols,extrasaction="ignore"); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"  wrote analysis/{name}  rows={len(rows)}")

if __name__=="__main__":
    e=events(); c=claims()
    write("fig2_events.csv",["run","group","strategy","t_first_job_submitted",
        "t_first_declared_strategy","t_first_high_accuracy_calc","t_first_encounter_cu_sql",
        "t_final_filing","t_session_end","end_reason","spend_fraction"], e)
    write("fig2_claims_long.csv",["run","group","structure_id","rank_in_run","reported_value",
        "reported_uncertainty","accuracy_tier","structure_class","reported_how"], c)
    import collections
    print("  end_reason:",dict(collections.Counter(x["end_reason"] for x in e)))
    print("  structure_class:",dict(collections.Counter(x["structure_class"] for x in c)))
    print("  reported_how:",dict(collections.Counter(x["reported_how"] for x in c)))
    print("  strategy column: empty for all 16 (no D/B/S/M taxonomy in the record)")
