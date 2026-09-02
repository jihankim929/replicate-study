#!/usr/bin/env python3
"""Build the three figure tables from the POST-SEAL WORKSPACE PULL authorised 2026-09-02.

READ THIS BEFORE USING THE OUTPUT. These three files are the only analysis artifacts in this
repository that do NOT trace to the sealed 16/16 attestation. They were pulled read-only from
`bnode0` on 2026-09-02, after the seal, and nothing attests they are unchanged since the campaign.
Each output carries a `#`-prefixed UNATTESTED header line (so a strict CSV reader must skip line 1,
unlike every other file in analysis/) and per-row provenance columns.

THE ROW COUNTS DO NOT MATCH THE REPORTS' FILED TOTALS, AND THAT IS THE FINDING, NOT A DEFECT.
rep02's REPORT.md was written 2026-09-01 05:32; its `tables/t1_wc.csv` was last written
2026-09-02 02:13 -- 20 h 41 min later, and 44 min AFTER the campaign closed at 01:29. The workspace
therefore holds measurements the filed report never saw: 389 complete pairs against the 250 the
report states. These tables are the workspace's FINAL state, not the evidence behind the filed
report, and they cannot be used to reproduce a filed figure.
"""
import csv, glob, os, sys, pathlib, collections, statistics
ROOT = pathlib.Path(__file__).resolve().parent.parent
S = sys.argv[1] if len(sys.argv)>1 else "/tmp/pull"
PULLED = "2026-09-02T12:0xZ"
SHA = {"rep02/mod_rank.csv":"e4b33f443d529515a466ee329f94f451048e7959a5f77b2207c6ae93318f43a5",
       "rep02/t1_wc.csv":"67d64b40bc9a35cf9796f53cd74cf259f566df2e92c9d7da71a6d7e2c3e9bdbe",
       "rep15/mods.csv":"8e57441ee821c5f0519085b104eaa79a83ef31afbdd0d4971d6fee407ef0bb9f"}
HDR = ("# UNATTESTED. Post-seal read-only pull from bnode0 {p}. Outside the sealed 16/16 "
       "attestation; nothing attests these bytes are unchanged since the campaign. "
       "Workspace data postdates the filed REPORT.md, so row counts DO NOT match filed totals "
       "-- see the filed_total / count_matches_filed columns. Skip this line when parsing.\n")

def write(path, cols, rows):
    p = ROOT/"analysis"/path; p.parent.mkdir(exist_ok=True)
    with p.open("w", newline="") as fh:
        fh.write(HDR.format(p=PULLED))
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"  wrote analysis/{path}  rows={len(rows)}")

def rep02():
    mr=list(csv.DictReader(open(f"{S}/rep02/mod_rank.csv")))
    tw=list(csv.DictReader(open(f"{S}/rep02/t1_wc.csv")))
    by=collections.defaultdict(list)
    for r in tw: by[r["struct"]].append(r)
    pick=lambda n: sorted(by[n],key=lambda r:-int(r["prod"]))[0] if by.get(n) else None
    rows=[]
    for r in mr:
        c,p=pick(r["name"]),pick(r["parent"])
        if not(c and p): continue
        rows.append(dict(rep="rep02",arm="ungated",parent=r["parent"],child=r["name"],
            parent_wc=p["wc"],parent_sd=p["sd_wc"],child_wc=c["wc"],child_sd=c["sd_wc"],
            delta=f"{float(c['wc'])-float(p['wc']):+.3f}",
            parent_fidelity=f"{p['prod']} prod",child_fidelity=f"{c['prod']} prod",
            source_file="ws/rep02/tables/{mod_rank,t1_wc}.csv",
            source_sha256=SHA["rep02/t1_wc.csv"][:16]+"…",pulled_at=PULLED,
            attestation="none - post-seal pull",workspace_mtime="2026-09-02 02:13",
            filed_total="250 paired parents (REPORT.md 2026-09-01 05:32)",
            count_matches_filed="NO - 389 here; workspace postdates the report by 20h41m"))
    g=[float(x["child_wc"])-float(x["parent_wc"]) for x in rows]
    print(f"  rep02 pairs={len(rows)} mean delta {statistics.mean(g):+.2f} (filed: 250, +87.1)")
    return rows

def rep15():
    md=list(csv.DictReader(open(f"{S}/rep15/mods.csv")))
    rows=[dict(rep="rep15",arm="ungated",parent=r["parent"],child=r["name"],
        ligands_removed=r["n_h2o_removed"],parent_natoms=r["parent_natoms"],child_natoms=r["natoms"],
        density=r["density"],volume=r["volume"],
        parent_wc="NOT IN AUTHORISED PULL",child_wc="NOT IN AUTHORISED PULL",delta="",
        fidelity="screening cycles only (REPORT.md)",
        source_file="ws/rep15/manifests/mods.csv",source_sha256=SHA["rep15/mods.csv"][:16]+"…",
        pulled_at=PULLED,attestation="none - post-seal pull",workspace_mtime="2026-08-30 12:42",
        filed_total="42 measured pairs, 41 of 42 children beat parent, mean +18.6, max +74.8",
        count_matches_filed="N/A - mods.csv is the BUILD manifest (206 rows), carries no WC column")
        for r in md]
    print(f"  rep15 rows={len(rows)} (build manifest; NO working-capacity column exists in it)")
    return rows

def rep17():
    sel={}
    for f in glob.glob(f"{S}/rep17/*_selection.csv"):
        for r in csv.DictReader(open(f)): sel[r["name"]]=(r.get("init",""),r.get("prod",""))
    rows=[]
    for f in sorted(glob.glob(f"{S}/rep17/*.csv")):
        b=os.path.basename(f)
        if b.endswith("_selection.csv"): continue
        for r in csv.DictReader(open(f)):
            n=r.get("name","")
            if "@" not in n or "wc" not in r: continue
            series="fluorination" if "@f" in n else "methylation"
            init,prod=sel.get(n,("",""))
            rows.append(dict(rep="rep17",arm="ungated",series=series,parent="2021[Cu][sql]2[ASR]6",
                variant=n.split("@")[1],wc=r["wc"],error=r["ewc"],n58=r.get("n58",""),n65=r.get("n65",""),
                cycles_from_selection=f"{init}+{prod}" if init else "",
                cycles_note="e-series identified as claim grade (10,000+50,000) in REPORT.md §1; "
                            "selection files are per-wave and may not attribute across waves",
                source_file=f"ws/rep17/analysis/{b}",source_sha256="(45-file set, not individually hashed)",
                pulled_at=PULLED,attestation="none - post-seal pull",workspace_mtime="various",
                filed_total="me004 = 208.15 ± 0.37 in REPORT.md §1",
                count_matches_filed="YES for me004 - e3.csv gives 208.1526 ± 0.3704"))
    print(f"  rep17 rows={len(rows)} distinct variants={len(set(r['variant'] for r in rows))}")
    return rows

PROV=["source_file","source_sha256","pulled_at","attestation","workspace_mtime",
      "filed_total","count_matches_filed"]
r2,r15,r17=rep02(),rep15(),rep17()
write("rep02_deinterpenetration_pairs.csv",
      ["rep","arm","parent","child","parent_wc","parent_sd","child_wc","child_sd","delta",
       "parent_fidelity","child_fidelity"]+PROV, r2)
write("rep15_aqua_removal_pairs.csv",
      ["rep","arm","parent","child","ligands_removed","parent_natoms","child_natoms","density",
       "volume","parent_wc","child_wc","delta","fidelity"]+PROV, r15)
write("rep17_methylation_fluorination.csv",
      ["rep","arm","series","parent","variant","wc","error","n58","n65",
       "cycles_from_selection","cycles_note"]+PROV, r17)
