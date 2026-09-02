#!/usr/bin/env python3
"""Leaderboard + search-completeness extraction. PI instruction 2026-09-02: mechanical and verbatim.

NO ASSESSMENT. Every cell is a verbatim string from the filed report, a structure id, or a
classification against the sealed exclusion set. Nothing is scored and nothing is judged.

LEADERBOARD LOCI ARE DECLARED, NOT GUESSED. A report's "final claim-grade leaderboard" is not
machine-identifiable -- reports carry between 0 and 6 pipe tables containing structure ids, and
several file none. Each locus below is the start line of the table read, with the reason. Reports
that filed NO ranked table get one row with rank=0 and status recorded, because dropping them
would make the file silently under-report 10 of 16 replicates.
"""
import re, csv, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"harness"))
import behavioral_extract as B

# rep -> (start line of the table, note). Line numbers are 1-based into REPORT.md.
LOCI = {
 "rep01": (105, "table headed `rank | structure | Claim grade | N(65 bar) | N(5.8 bar)`; 3 entries filed"),
 "rep02": (38,  "table headed `structure | wc | seeds | ... | origin`; 10 entries"),
 "rep06": (73,  "table headed `structure | WC | ± | N(65) | N(5.8)`; 10 entries"),
 "rep07": (38,  "table headed `# | structure | WC (cm³/cm³) | grade | tag`; 10 entries"),
 "rep08": (53,  "table headed `sid | structure | WC | ...`; 6 entries"),
 "rep10": (44,  "table headed `structure | working capacity | +/- | ... | tier`; mixed tiers, as filed"),
 "rep11": (23,  "table headed `structure | working capacity (cm³ STP/cm³) | ...`; 2 entries filed"),
 "rep16": (25,  "table explicitly labelled **Claim grade leaderboard**; 10 entries"),
}
NO_TABLE = {
 "rep03": "no pipe table with >=2 structure ids anywhere in REPORT.md",
 "rep04": "no pipe table with >=2 structure ids anywhere in REPORT.md",
 "rep05": "no ranked leaderboard filed; champion in prose, plus a lattice-scaling table",
 "rep09": "no pipe table with >=2 structure ids; champion in prose",
 "rep12": "no ranked leaderboard filed; champion + runner-up in prose",
 "rep13": "no ranked leaderboard filed; champion + runner-up in prose",
 "rep15": "no pipe table with >=2 structure ids; champion in prose",
 "rep17": "no ranked leaderboard filed; champion + runner-up in prose",
}
EXCL_REASON = {  # answer-key/exclusion_set_record.md, FINAL STATE -- SEALED
 "2021[Cu][sql]2": "capacity artifact; complete anion deletion, divalent (net +8, azolate 0)",
 "2020[Fe][hcb]2": "capacity artifact; complete deletion, trivalent (net +9)",
 "2010[Co][tbo]3": "capacity artifact; complete deletion, divalent (net +24)",
 "2017[Fe][nan]3": "capacity artifact; complete deletion, trivalent (net +12)",
 "2015[Cu][pcu]3": "capacity artifact; complete deletion, divalent (net +4)",
 "2009[Cd][nan]3": "capacity artifact; partial anion deficit (net +48, 75% compensated)",
}
AGENT = re.compile(r'__\d+of\d+|_DENET|\+DEAQ|@(f|me)\d+')
SID   = re.compile(r'(\d{4}\[[A-Za-z]{1,6}\]\[[a-z]{3}\]\d(?:\[(?:ASR|FSR|ION)\]\d+)?)')
NUM   = re.compile(r'(\d{2,3}\.\d{1,3})')
ERR   = re.compile(r'±\s*(\d+\.\d+)')

def classify(name):
    base = SID.search(B.normalize(name))
    base = base.group(1).split("[ASR]")[0].split("[FSR]")[0] if base else ""
    if AGENT.search(name):
        return "agent-built", "", re.sub(AGENT, "", name).strip("`_ ")
    if base in EXCL_REASON:
        return "database-excluded", EXCL_REASON[base], ""
    return "database-clean", "", ""

def parse(rep, start):
    L = (B.COLL/rep/"REPORT.md").read_text(errors="replace").split("\n")
    i = start-1
    hdr = [c.strip() for c in L[i].strip("|").split("|")]
    rows=[]
    for l in L[i+2:]:
        if not l.startswith("|"): break
        rows.append([c.strip() for c in l.strip("|").split("|")])
    # structure column = first cell containing a structure id; wc column = first numeric after it
    out=[]
    for n,cells in enumerate(rows[:5], start=1):
        sname=None; si=None
        for k,c in enumerate(cells):
            if SID.search(B.normalize(c)): sname=c.strip("`* "); si=k; break
        if sname is None: continue
        wc=err=""
        for c in cells[(si+1):]:
            m=NUM.search(c)
            if m and not wc:
                wc=m.group(1)
                e=ERR.search(c)
                if e: err=e.group(1)
            elif wc and not err:
                e=ERR.search(c) or re.fullmatch(r'\*?\*?(\d\.\d{1,3})\*?\*?', c.strip())
                if e: err=e.group(1); break
        cls,reason,parent = classify(sname)
        out.append(dict(rep=rep, arm=B.ARM[rep], rank=n, structure=sname, wc=wc, error=err,
                        entry_class=cls, excluded_reason=reason, parent=parent,
                        source_locus=f"REPORT.md line {start}"))
    return out

def main():
    rows=[]
    for r in B.REPS:
        if r in LOCI:
            rows += parse(r, LOCI[r][0])
        else:
            rows.append(dict(rep=r, arm=B.ARM[r], rank=0, structure="(no ranked leaderboard filed)",
                             wc="", error="", entry_class="not-filed",
                             excluded_reason=NO_TABLE[r], parent="", source_locus="REPORT.md"))
    cols=["rep","arm","rank","structure","wc","error","entry_class","excluded_reason","parent","source_locus"]
    p=ROOT/"analysis/leaderboards.csv"; p.parent.mkdir(exist_ok=True)
    with p.open("w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=cols); w.writeheader()
        for x in rows: w.writerow(x)
    print(f"wrote {p}  rows={len(rows)}")
    from collections import Counter
    c=Counter(x["entry_class"] for x in rows)
    for k,v in c.most_common(): print(f"  {k:<20} {v}")
    print(f"  replicates filing a ranked table: {len(LOCI)}/16")
    return 0
if __name__=="__main__": sys.exit(main())
