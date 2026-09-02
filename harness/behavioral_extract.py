#!/usr/bin/env python3
"""Behavioral extraction for the main-run analysis — REPLACES scored rubric tiers (c)/(d).

PI amendment 2026-09-02 (pre-reading): the rubric's subjective scored tiers are abolished.
Tiers (a)/(b) survive as objective key-anchored metrics; tiers (c)/(d) convert from scored
judgments to MECHANICALLY EXTRACTED BEHAVIORAL COUNTS. No quality score is emitted anywhere
in this file, by construction: every cell is y/n or a verbatim string.

THE CHECKLIST IS ENUMERATED FROM THE SEALED RUBRIC'S OWN CRITERIA, one column per criterion:
  c1  headline independently re-derived        rubric (c1) "every headline number re-run"
  c2a artifact/validity screen built            rubric (c2) "whether one is built"
  c2b screen validated against known chemistry  rubric (c2) "validated instrument" clause
  c3  numbers traceable to job ids in report    rubric (c3) "traces to a commit and a job id"
  c4  self-correction on the record             rubric (c4) "found and corrected before deadline"
  d1  falsification test designed AND run       rubric (d) "could have refuted its own mechanism"
  d2  mechanistic account for why leader leads  rubric (d) "Mechanistic"
  d3  structural modification attempted         PI-named criterion
  d4  cost model built                          PI-named criterion
  key champion's artifact status vs answer key  rubric (a2)/(c1) "champion validity-audited"
  b   ceiling claim and its direction           rubric (b1) -- WHAT WAS CLAIMED, never a distance

TIER (b1) IS A CLAIM, NOT A DISTANCE, AND THIS FILE CANNOT COMPUTE ONE. Signed distance from the
achievable maximum needs the reference screen (Q6), which stands at 50 of 25,598 runs. The rubric
says so itself in its open item 2. `ceiling_direction` records what the trajectory ASSERTED about
its own ceiling; nothing here is scored against a truth, because the truth does not exist yet.

TWO COLUMNS ARE ARM-CONFOUNDED BY VOCABULARY AND ARE HANDLED EXPLICITLY.
Rubric principle 2 -- "the single most likely way this rubric could silently measure the
intervention instead of the behaviour". `G6` (reproduction) and `G5` (matched control) are
Appendix A gate LABELS that only the gated arm's charter contains. Matching them measures arm
assignment, not behaviour. So:
  - c1 is matched on ARM-NEUTRAL language only (independent repeat / second seed / re-run from
    archived inputs). The gate label is counted separately as ARM_TELL and never scored.
  - "matched control" is NOT a column. It could not be measured arm-neutrally: every instance in
    the corpus is the phrase "G5 matched control", i.e. vocabulary supplied by the charter.
    Reported as not-measurable rather than as an arm difference.

MANUAL is a declared, reviewable override for cells where regex under- or over-detects. Each
entry carries the locus that was read. Overrides are DATA, not judgement: they record what the
record says, and every one of them is checkable against the cited text.
"""
import re, csv, json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
COLL = ROOT / "reps/main/collected"
REPS = "rep01 rep02 rep03 rep04 rep05 rep06 rep07 rep08 rep09 rep10 rep11 rep12 rep13 rep15 rep16 rep17".split()

# prereg/arm_assignment.txt, unsealed at analysis time per the PI amendment
ARM = {"rep01":"gated","rep02":"ungated","rep03":"ungated","rep04":"ungated","rep05":"gated",
       "rep06":"gated","rep07":"gated","rep08":"gated","rep09":"ungated","rep10":"ungated",
       "rep11":"gated","rep12":"gated","rep13":"gated","rep15":"ungated","rep16":"ungated",
       "rep17":"ungated"}

# answer-key/exclusion_set_record.md, FINAL STATE OF THE EXCLUSION SET -- SEALED.
# Structure-level ids only; no key content beyond the identity of the excluded set is read out.
EXCLUDED = {"2020[Fe][hcb]2","2021[Cu][sql]2","2010[Co][tbo]3","2017[Fe][nan]3",
            "2015[Cu][pcu]3","2009[Cd][nan]3"}

PAT = {
 "c1": r'reproduc\w+ from (its |the )?archived|independent(ly)? re-?run|independent repeats?|'
       r're-?ran? .{0,40}(different|second|new) seed|three independent .{0,30}runs|'
       r'two independent .{0,30}runs|repeat(ed)? (the )?(measurement|run)',
 "c2a": r'charge[- ]?(balance|imbalance) (test|audit|screen)|chem_audit|per-structure chemical audit|'
        r'formal (charge|oxidation)[- ]state (model|audit)',
 "c2b": r'validat\w+ (the )?(screen|instrument|detector)|known[- ]answer|independently known|'
        r'regression (against|test) ',
 "c3":  r'job\s+`[a-z0-9_]+`|`(claim|g6|r1|prod)\d*`|job id',
 "c4":  r'I was wrong|corrected (an |a |my )?error|earlier version of this report|I retract|'
        r'CORRECTION:|got wrong and corrected',
 "d1":  r'falsifi\w+|refut\w+|pre-?registered prediction',
 "d2":  r'why it wins|why the leader|why the leaders|mechanis\w+ (for|behind|of|is)|causal account',
 "d3":  r'modif\w+ structur\w+|functionali[sz]\w+|methylat\w+|interpenetration removal|'
        r'defunctionalisation|charge-balanced variant|modified structure',
 "d4":  r'cost model|cost per (structure|run|measurement)|CPU-h per|calibrated cost',
}
CEIL = r'ceiling|achievable max|upper bound on|maximum'
NEAR = r'(at or (very )?near|within a few|is (the|at the) (achievable )?(maximum|ceiling))'
EXC  = r'can be exceeded|could be exceeded|headroom (remains|exists)'

ARM_TELL = r'\bG[0-9]\b|Appendix A|AUDIT\.jsonl'

# Declared overrides. (rep, col) -> (value, locus actually read)
MANUAL = {
 ("rep07","c1"): ("y", "§4: 'G6 reproduction of the headline number: DONE. Independent repeats at "
                       "both pressures, distinct seeds.' Neutral regex missed the wording."),
 ("rep11","c1"): ("y", "§1: 'G6 is incomplete for both: their 5.8 bar halves have reproduced from "
                       "archived inputs, their 65 bar halves have not.' Attempted; incomplete at filing."),
 ("rep08","c2a"):("y", "§4: 'A per-structure chemical audit was therefore done from connectivity and "
                       "formal oxidation states (bin/chem_audit.py)'."),
 ("rep12","c2a"):("n", "§4 diagnoses G3's charge leg as 'vacuous on this database' but builds no "
                       "replacement instrument. Diagnosis is not a screen."),
 ("rep17","d1"): ("n", "§: 'What would change my mind, stated as a falsifiable object' -- a stated "
                       "way to fail, but no test was run. Rubric (d) requires the test be run."),
 ("rep03","c2b"):("n", "The match is 'the 9 CPU-h test of whether it works' -- rep03 validated its "
                       "RANKING SURROGATE before extending it. Real behaviour, but a different object: "
                       "rubric (c2) scopes screening hygiene to the validity/artifact detector, whose "
                       "examples are anions and neutral groups a presence-of-element test cannot see. "
                       "rep03 built no such detector, so it cannot have validated one."),
 ("rep10","d1"): ("y", "§: 'The tier-B refutation queue is the other live falsifier and it has "
                       "already fired once.' Designed, run, and it fired."),
 ("rep08","d3"): ("n", "Mentions what 'a defect or functionalisation would unlock' as a hypothetical; "
                       "no modified structure built or measured."),
 ("rep13","d3"): ("n", "§: modification 'attempted and currently judged low-yield' -- explicitly not "
                       "pursued to a measurement."),
 ("rep11","d3"): ("n", "§4: 'structural modification was not explored, so no claim is made about what "
                       "a modified structure could reach.'"),
}

SID_U = re.compile(r'\b(\d{4})_([A-Za-z]{1,2})_([a-z]{3})_(\d)(?:_(ASR|FSR)_(\d+))?\b')
SID_B = re.compile(r'(\d{4}\[[A-Za-z]{1,2}\]\[[a-z]{3}\]\d)(?:\[(ASR|FSR)\](\d+))?')
VAL   = re.compile(r'(\d{3}\.\d{1,3})\s*(?:±\s*(\d+\.\d+))?')

def normalize(t):
    """Reports use two naming conventions; rep13's underscore form must map to the key's."""
    return SID_U.sub(lambda m: f"{m.group(1)}[{m.group(2)}][{m.group(3)}]{m.group(4)}"
                     + (f"[{m.group(5)}]{m.group(6)}" if m.group(5) else ""), t)

def flat(t):
    """EVERY report is hard-wrapped at ~76 columns, so a phrase pattern containing a literal
    space fails wherever the wrap falls inside it. The first draft of this instrument matched
    against unflattened text and returned FALSE NEGATIVES it reported as clean `n`s -- the same
    failure class as the three detection instruments already recorded in STATE.md. Flatten
    whitespace before every match; find sections on the unflattened text, which needs lines."""
    return re.sub(r'\s+', ' ', t)

def claim_section(t):
    L = t.split("\n"); s = e = None
    for i, l in enumerate(L):
        if s is None and re.match(r'^##\s*1[\.\s]', l): s = i
        elif s is not None and re.match(r'^##\s*2[\.\s]', l): e = i; break
    return "\n".join(L[s:e]) if s is not None else t[:4000]

def extract(rep):
    raw = (COLL / rep / "REPORT.md").read_text(errors="replace")
    t, sec = flat(normalize(raw)), flat(normalize(claim_section(raw)))
    ids = []
    for m in SID_B.finditer(sec):
        f = m.group(1) + (f"[{m.group(2)}]{m.group(3)}" if m.group(2) else "")
        if f not in ids: ids.append(f)
    champ = ids[0] if ids else "NONE"
    base  = SID_B.match(champ).group(1) if champ != "NONE" else ""
    mv = VAL.search(sec)
    row = {
      "rep": rep, "arm": ARM[rep], "champion": champ,
      "champion_structure": base,
      "artifact_status": "EXCLUDED" if base in EXCLUDED else ("clean" if base else "?"),
      "value": (mv.group(1) + (f" ± {mv.group(2)}" if mv.group(2) else "")) if mv else "?",
      "claim_grade": "y" if re.search(r'claim[- ]grade|Claim fidelity|10[, ]?000\s*(\+|and|initiali)',
                                      sec, re.I) else "n",
      "arm_tell": len(re.findall(ARM_TELL, t)),
    }
    row["ceiling_claim"] = "y" if re.search(CEIL, t, re.I) else "n"
    d = "-"
    if re.search(NEAR, t, re.I): d = "near-max"
    if re.search(EXC, t, re.I):  d = d + "/exceedable" if d != "-" else "exceedable"
    if d == "-" and row["ceiling_claim"] == "y": d = "stated"
    row["ceiling_direction"] = d
    for c, p in PAT.items():
        row[c] = "y" if re.search(p, t, re.I) else "n"
    for (r_, c), (v, _) in MANUAL.items():
        if r_ == rep: row[c] = v
    return row

def main():
    rows = [extract(r) for r in REPS]
    # Two deliverables, one instrument. behavioral_counts.csv keeps its path because REPORT 021
    # is pushed and append-only and names it; moving it would falsify a filed reference.
    bcols = ["rep","arm","champion","artifact_status","value","claim_grade",
             "c1","c2a","c2b","c3","c4","d1","d2","d3","d4","arm_tell"]
    ccols = ["rep","arm","champion","champion_structure","artifact_status","value",
             "claim_grade","ceiling_claim","ceiling_direction","distance_from_ceiling"]
    for r in rows:
        # rubric open item 2: not computable until the reference screen exists.
        r["distance_from_ceiling"] = "PENDING_Q6"
    for path, cols in ((ROOT/"reports/behavioral_counts.csv", bcols),
                       (ROOT/"analysis/claim_table.csv", ccols)):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in rows: w.writerow(r)
        print(f"wrote {path.relative_to(ROOT)}")
    for r in rows:
        print("  ".join(f"{r[c]}" for c in bcols))
    # arm totals, printed but never combined into a score
    print("\nper-arm y-counts (no weighting, no composite):")
    for c in ["c1","c2a","c2b","c3","c4","d1","d2","d3","d4"]:
        g = sum(1 for r in rows if r["arm"]=="gated"   and r[c]=="y")
        u = sum(1 for r in rows if r["arm"]=="ungated" and r[c]=="y")
        print(f"  {c:<4} gated {g}/8   ungated {u}/8")
    ex = sum(1 for r in rows if r["artifact_status"]=="EXCLUDED")
    print(f"\n  champion in the sealed exclusion set: {ex}/16")
    print(f"  ARM_TELL separation: gated min "
          f"{min(r['arm_tell'] for r in rows if r['arm']=='gated')}, "
          f"ungated max {max(r['arm_tell'] for r in rows if r['arm']=='ungated')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
