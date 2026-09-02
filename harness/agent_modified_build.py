#!/usr/bin/env python3
"""Inventory of structure files present in a collected workspace and absent from the frozen manifest.

REBUILD, authorised 2026-09-03, correcting REPORT 036 section 4. The first build reported 6 runs and
2,037 files; the correct figures are 8 runs and 2,253 files. Two filter defects, both recorded in
REPORT 039 and fixed here:

  rep09, 209 files lost. Its products are named `m100080.cif`, and the old rule treated any
    `^[A-Za-z]{1,2}[0-9a-f]{4,9}\\.cif$` as a sid-renamed staged copy. rep09 uses `m`-prefixed ids
    for BOTH staged copies and modified products. FIX: a file living in a run's `mod/` or `mods/`
    directory is a product by construction and is never classed as a staged copy. (The id ranges
    also separate cleanly -- products 100080-112474, staged copies below 100000 -- but the
    directory is the rule, because it does not depend on a run's numbering habits.)
  rep12, 7 files lost. Its products are named `2016_Cu__pts_3_ASR_1__fluoro100.cif`, and the old
    underscore normaliser was UNANCHORED: it matched the stem, produced a valid manifest name and
    discarded the file. FIX: the normalised name must consume the WHOLE basename.

Columns and every other rule are unchanged from the first build.
"""
import csv, json, re, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"harness")); import behavioral_extract as B

EXCL = {"2020[Fe][hcb]2","2021[Cu][sql]2","2010[Co][tbo]3","2017[Fe][nan]3","2015[Cu][pcu]3","2009[Cd][nan]3"}
GROUP = {"gated":"C","ungated":"U"}
RASPA   = re.compile(r'^Framework_\d+_(initial|final)_')
GENERIC = re.compile(r'^(framework|framework_bench\d*|S|G|Box|input|struct\d*)\.cif$', re.I)
TESTY   = re.compile(r'^(struct|sT|s_test|bench\d*|f|frame|smoke|gt\d*|elemprobe)\.cif$', re.I)
SIDONLY = re.compile(r'^[A-Za-z]{1,2}[0-9a-f]{4,9}\.cif$')
UND     = re.compile(r'^S?(\d{4})_([A-Za-z]{1,6})_+([a-z]{3})_(\d)_(ASR|FSR|ION)_(\d+)\.cif$')  # ANCHORED
INMODS  = re.compile(r'(^|/)(mod|mods)/')
TR = {"rep02":'"interpenetration removal"',
      "rep05":'"Isotropic lattice scaling of the winner"',
      "rep06":'"de-interpenetration against matched pristine controls"',
      "rep09":'"defunctionalisation"; "every substitution is monovalent-for-monovalent, substituent -> H"',
      "rep10":'"Methylation of framework C-H, charge-balanced by construction" (bin/methylate.py)',
      "rep12":'"aromatic C-H -> C-CH3 and C-H -> C-F, both charge-neutral by construction" (bin/modify.py)',
      "rep15":'"+DEAQ"; "The section 3 terminal-aqua removal"',
      "rep17":'"the four-methyl variant of the same framework" (scripts/methylate.py, scripts/fluorinate.py)'}
PAT = [(re.compile(r'^(.*?)__\d+of\d+\.cif$'),"rep02"), (re.compile(r'^(.*?)_DENET\.cif$'),"rep06"),
       (re.compile(r'^(.*?)\+DEAQ\.cif$'),"rep15"), (re.compile(r'^(.*?)@(?:me|f)\d+\.cif$'),"rep17"),
       (re.compile(r'^M(.*?)_f\d+\.cif$'),"rep10"), (re.compile(r'^scale0p\d+_(.*?)\.cif$'),"rep05"),
       (re.compile(r'^(.*?)__(?:methyl|fluoro)\d+\.cif$'),"rep12")]
# rep12 reports a value for every one of its seven, "each against its pristine parent at identical
# settings, which is what G5 requires" -- so the matched-setting column is `yes` for all seven.
R12 = {"2021_Cu__sql_2_ASR_6__methyl25":("206.59","1.02"), "2021_Cu__sql_2_ASR_6__methyl50":("203.41",""),
       "2021_Cu__sql_2_ASR_6__methyl100":("197.07",""), "2021_Cu__sql_2_ASR_6__fluoro100":("180.23",""),
       "2016_Cu__pts_3_ASR_1__methyl50":("186.35",""), "2016_Cu__pts_3_ASR_1__methyl100":("179.15",""),
       "2016_Cu__pts_3_ASR_1__fluoro100":("175.33","")}
R6  = {"0000[Er][lcy]3[ASR]1":("165.75","","low"), "0000[Lu][lcy]3[ASR]1":("175.41","","low"),
       "2010[Zn][rtl]3[ASR]1":("153.57","","low"), "2021[Cu][sql]2[ASR]6":("132.04","","low")}
R17 = {"me004":("208.1526","0.3704","high"),"me008":("207.3989","1.1381","low"),
       "me012":("206.5920","0.2785","low"),"me017":("205.6064","1.1396","low"),
       "me025":("203.4985","0.9471","low"),"me100":("199.7268","0.5102","low"),
       "f025":("198.3658","0.7504","low"),"f050":("190.4478","0.7444","low")}

# rep05 names its products `scale0p960_2021Cusql2FSR6.cif` -- the parent with all brackets stripped.
COMPACT = re.compile(r'^(\d{4})([A-Z][a-z]?)([a-z]{3})(\d)(ASR|FSR|ION)(\d+)$')

def expand(pn):
    m = COMPACT.match(pn)
    return f"{m.group(1)}[{m.group(2)}][{m.group(3)}]{m.group(4)}[{m.group(5)}]{m.group(6)}" if m else pn

def norm(b):
    m = UND.match(b)
    return f"{m.group(1)}[{m.group(2)}][{m.group(3)}]{m.group(4)}[{m.group(5)}]{m.group(6)}.cif" if m else b

def main(pairs_tsv, manifest_txt, rep09_mods, rep09_ids):
    man = {l.strip() for l in open(manifest_txt)}
    ids = {r["id"]: r["cif"] for r in csv.DictReader(open(rep09_ids))}
    r09 = {r["cif"]: (ids.get(r["src"], ""), r["kinds"]) for r in csv.DictReader(open(rep09_mods))}
    rows, drop = [], collections.Counter()
    for l in open(pairs_tsv):
        b, p = l.rstrip("\n").split("\t", 1)
        run = p.split("/")[0]
        if RASPA.match(b): drop["RASPA restart/output dump"] += 1; continue
        if TESTY.match(b) or GENERIC.match(b): drop["test frame / generic staged copy"] += 1; continue
        inmods = bool(INMODS.search(p))
        if SIDONLY.match(b) and not inmods: drop["sid-renamed staged copy"] += 1; continue
        if norm(b) in man: drop["underscore-renamed staged copy"] += 1; continue
        par = who = None
        for rx, w in PAT:
            m = rx.match(b)
            if m: par, who = m.group(1), w; break
        if who is None and run == "rep09" and inmods:
            who = "rep09"; par = r09.get(b[:-4], ("",""))[0]
        if who is None: drop["unclassified"] += 1; continue
        pn = par
        if pn and not pn.startswith(("20","00")) or (pn and "_" in pn):
            n2 = norm(pn + ".cif")
            pn = n2[:-4] if n2.endswith(".cif") and n2 != pn + ".cif" else pn
        pn = expand(pn or "")
        base = re.sub(r'\[(ASR|FSR|ION)\]\d+$', '', pn)
        pc = "excluded" if base in EXCL else ("retained" if re.match(r'^\d{4}\[', pn or "") else "unknown")
        rv = ru = at = ""; same = "unknown"
        if who == "rep06" and b.endswith("_DENET.cif") and b[:-10] in R6:
            rv, ru, at = R6[b[:-10]]; same = "yes"
        elif who == "rep17":
            m = re.search(r'@((?:me|f)\d+)\.cif$', b)
            if m and m.group(1) in R17: rv, ru, at = R17[m.group(1)]; same = "yes"
        elif who == "rep12" and b[:-4] in R12:
            rv, ru = R12[b[:-4]]; same = "yes"
        rows.append(dict(run=run, group=GROUP[B.ARM[run]], file_path=p,
            parent_structure_id=pn if pc != "unknown" else "", parent_class=pc,
            transformation=TR[who], reported_value=rv, reported_uncertainty=ru,
            accuracy_tier=at, pristine_parent_measured_same_setting=same))
    # One row per distinct product file. rep12 stages each of its seven products into two run
    # directories as well as `mods/`, so a raw path count reports 21 where the run built 7. Dedupe
    # on (run, basename), keeping the `mod/`/`mods/` copy as the canonical path.
    best = {}
    for r in rows:
        k = (r["run"], r["file_path"].split("/")[-1])
        if k not in best or INMODS.search(r["file_path"]): best[k] = r
    rows = list(best.values())
    rows.sort(key=lambda r: (r["run"], r["file_path"]))
    out = ROOT/"analysis/agent_modified_structures.csv"
    with out.open("w", newline="") as fh:
        fh.write("# UNATTESTED. Workspace file inventory, post-seal read-only. REBUILT 2026-09-03 "
                 "correcting REPORT 036 section 4 (was 6 runs / 2,037 rows). Skip this line.\n")
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader()
        for r in rows: w.writerow(r)
    print(f"  rows={len(rows)}  runs={len(set(r['run'] for r in rows))}")
    print("  per run:", dict(collections.Counter(r["run"] for r in rows).most_common()))
    print("  parent_class:", dict(collections.Counter(r["parent_class"] for r in rows)))
    print("  no stated parent:", sum(1 for r in rows if not r["parent_structure_id"]))
    print("  with a reported value:", sum(1 for r in rows if r["reported_value"]))
    print("  dropped:", dict(drop))
    return 0
if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
