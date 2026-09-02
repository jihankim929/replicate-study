#!/usr/bin/env python3
"""Per-run inventory of scripts each replicate authored. PI instruction 2026-09-02: verbatim,
mechanical, read-only.

PROVENANCE, STATED FIRST BECAUSE IT GOVERNS THE OUTPUT. `git-log.txt` in the sealed collection
records hash, date and subject only -- NO FILENAMES -- so the sealed record contains no script
inventory of any kind. This inventory is therefore built from a POST-SEAL READ-ONLY READ of the
replicate workspaces on bnode0, exactly like REPORT 025's tables: outside the sealed 16/16
attestation, nothing attests these bytes are unchanged since the campaign. Both outputs carry a
`#` UNATTESTED header line.

SCOPE. Authored tool directories only -- `bin/`, `scripts/`, `tools/`. Deliberately excluded, with
the count reported in the summary instead of as rows:
  * `pylib/`   -- VENDORED numpy/scipy, not authored by the run (rep02, rep12). Reported as an
                  external package with the directory as evidence.
  * `work/{pending,done,running,queue,hqueue,dqueue}` -- GENERATED per-task scripts, one per job.
                  rep13 has 2,038 and rep10 418; listing them would swamp the file with artifacts
                  rather than tools. Counted in the summary as `generated_job_scripts`.

LOC RULE, stated because "lines of code" is not self-defining: non-blank lines whose first
non-space character is not `#`. Python docstrings are NOT stripped -- doing so needs a parse, and a
regex that tries silently mis-counts any file using triple quotes for data. Stated, not hidden.
"""
import ast, csv, os, re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC  = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/tools")
REPS = "rep01 rep02 rep03 rep04 rep05 rep06 rep07 rep08 rep09 rep10 rep11 rep12 rep13 rep15 rep16 rep17".split()
ARM  = {"rep01":"gated","rep02":"ungated","rep03":"ungated","rep04":"ungated","rep05":"gated",
        "rep06":"gated","rep07":"gated","rep08":"gated","rep09":"ungated","rep10":"ungated",
        "rep11":"gated","rep12":"gated","rep13":"gated","rep15":"ungated","rep16":"ungated",
        "rep17":"ungated"}
PULLED = "2026-09-02T13:5xZ"
# Counted remotely by read-only listing on 2026-09-02, recorded here rather than recomputed,
# because the local pull deliberately excludes both directory classes (see the module docstring).
GENERATED = {"rep07": 8, "rep10": 418, "rep13": 2038, "rep16": 43}
VENDORED  = {"rep02": "numpy+scipy+sklearn (ws/rep02/pylib/)",
             "rep12": "numpy+scipy+sklearn (ws/rep12/pylib/)"}
HDR = ("# UNATTESTED. Post-seal read-only read of replicate workspaces on bnode0 {p}. The sealed "
       "collection contains NO script inventory (git-log.txt records no filenames), so nothing "
       "attests these bytes are unchanged since the campaign. Skip this line when parsing.\n")

STDLIB = set(sys.stdlib_module_names)
# The pinned toolchain, per harness/config.py RATIFIED: RASPA 2.0.37 `simulate`, plus the shell and
# PBS. Anything else invoked is reported.
PINNED_BIN = {"simulate", "qsub", "qstat", "qdel", "qas", "bash", "sh", "python3", "python"}
# A binary counts only where it is INVOKED, never where the word appears. The first draft matched
# the name anywhere in a non-comment line and reported Zeo++'s `network` from prose about "pore
# network", and `make` from English inside docstrings ("Two things make the..."). Fifth match in
# this analysis series that was true as written and false as meant.
BINS = (r'zeo\+\+|network|obabel|openbabel|mofid|julia|Rscript|matlab|gcc|gfortran|'
        r'make|cmake|conda|pip|curl|wget|git')
PY_CALL = re.compile(r'(?:subprocess\.(?:run|Popen|check_output|call|check_call)|os\.(?:system|popen))'
                     r'\s*\((.{0,250})', re.S)
SH_CMD  = re.compile(r'(?:^|[|;&]|\$\(|`)\s*(' + BINS + r')\b')
BIN_NAME= re.compile(r'\b(' + BINS + r')\b')

# Scored, not first-match-wins. A first-match-wins list silently hands everything to whichever
# category sits at the top: an earlier draft put `job submission` first and it captured a
# compute-budget meter and a 10-minute tick logger on the word "queue". Filename evidence outranks
# body evidence 2:1, and the whole list is scored before anything is assigned.
CAT = [  # (category, filename regex, docstring/body keyword regex)
 ("job submission",        r'(submit|dispatch|launch|mkqueue|qsub|worker|pbs|sched|runner|hardstop)',
                           r'(qsub\b|PBS -|submits? (the |a )?job|dispatch|job script)'),
 ("parsing",               r'(parse|read|extract|collect|scrape|load|ingest)',
                           r'(parse|read the|extract|Output/System_0|\.data\b)'),
 ("descriptors",           r'(descr|geom|zeo|pore|void|widom|surface|acc|probe)',
                           r'(descriptor|void fraction|pore|Widom|geometr|surface area)'),
 ("surrogate model",       r'(model|fit|pred|surrogate|regress|gbr|rf_|ml_|rank|refit|ceiling)',
                           r'(surrogate|regress|predict|model fit|GBR|random forest|ceiling bound)'),
 ("structure modification",r'(modif|methylat|fluorinat|mod_|mkmod|deinterp|denet|deaq|variant|build)',
                           r'(modif|methylat|fluorinat|de-?interpenetrat|variant|functionalis)'),
 ("audit or gate check",   r'(audit|gate|check|verify|valid|selftest|g[0-9]|chem_audit|seedcheck)',
                           r'(audit|gate|verify|validat|G[0-9]\b|check that|assert)'),
 ("bookkeeping",           r'(log|state|report|status|meter|usage|spend|track|curator|inventory|tick|mkreport)',
                           r'(LOG\.md|STATE\.md|report|bookkeep|usage|spend|meter|ledger)'),
]

def loc(text):
    return sum(1 for l in text.split("\n") if l.strip() and not l.strip().startswith("#"))

def purpose(path, text):
    if path.suffix == ".py":
        try:
            d = ast.get_docstring(ast.parse(text))
            if d: return " ".join(d.strip().split())[:200]
        except SyntaxError:
            pass
    for l in text.split("\n")[:12]:
        s = l.strip()
        if s.startswith("#") and not s.startswith("#!") and len(s) > 3 \
           and "coding:" not in s and "-*-" not in s:
            return s.lstrip("# ").strip()[:200]
    return ""

def categorise(name, text):
    body = text[:1500]
    best, score = "other", 0
    for cat, fre, kre in CAT:
        s = (2 if re.search(fre, name, re.I) else 0) + (1 if re.search(kre, body, re.I) else 0)
        if s > score: best, score = cat, s
    return best

def imports(text, own):
    """`own` is the set of module names the replicate itself authored. Sibling imports are NOT
    external packages -- an earlier draft reported cifutil, descr, gates and a dozen others as
    external, which would have made every run look like it pulled in third-party code."""
    out = set()
    try:
        for n in ast.walk(ast.parse(text)):
            if isinstance(n, ast.Import):
                out |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                out.add(n.module.split(".")[0])
    except SyntaxError:
        pass
    return {m for m in out if m not in STDLIB and m not in own}

def main():
    rows, summary = [], []
    for r in REPS:
        base = SRC / r
        files = sorted(p for p in base.rglob("*") if p.suffix in (".py", ".sh") and p.is_file())
        own = {p.stem for p in files if p.suffix == ".py"} | {p.parent.name for p in files}
        ext_pkg, ext_bin = collections.defaultdict(list), collections.defaultdict(list)
        tot = 0
        for p in files:
            try: text = p.read_text(errors="replace")
            except Exception: continue
            n = loc(text); tot += n
            rel = str(p.relative_to(base))
            for m in imports(text, own):
                ext_pkg[m].append(rel)
            if p.suffix == ".py":
                for m in PY_CALL.finditer(text):
                    line = text[:m.start()].count("\n") + 1
                    for b in BIN_NAME.finditer(m.group(1)):
                        if b.group(1) not in PINNED_BIN:
                            ext_bin[b.group(1)].append(f"{rel}:{line}")
            else:
                for i, l in enumerate(text.split("\n"), 1):
                    if l.strip().startswith("#"): continue
                    for b in SH_CMD.finditer(l):
                        if b.group(1) not in PINNED_BIN:
                            ext_bin[b.group(1)].append(f"{rel}:{i}")
            rows.append(dict(rep=r, arm=ARM[r], filename=rel,
                             language="python" if p.suffix == ".py" else "shell",
                             loc=n, purpose=purpose(p, text), category=categorise(p.name, text),
                             pulled_at=PULLED, attestation="none - post-seal workspace read"))
        pkgs = "; ".join(f"{k} (evidence: {v[0]}"
                         + (f" +{len(v)-1} more" if len(v) > 1 else "") + ")"
                         for k, v in sorted(ext_pkg.items()))
        bins = "; ".join(f"{k} (evidence: {v[0]}"
                         + (f" +{len(v)-1} more" if len(v) > 1 else "") + ")"
                         for k, v in sorted(ext_bin.items()))
        summary.append(dict(rep=r, arm=ARM[r], script_count=len(files), total_loc=tot,
                            external_packages=pkgs or "none detected",
                            external_binaries=bins or "none detected",
                            vendored_packages=VENDORED.get(r, "none"),
                            generated_job_scripts=GENERATED.get(r, 0),
                            pulled_at=PULLED, attestation="none - post-seal workspace read"))
    def write(path, cols, data):
        p = ROOT / "analysis" / path
        with p.open("w", newline="") as fh:
            fh.write(HDR.format(p=PULLED))
            w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
            for d in data: w.writerow(d)
        print(f"  wrote analysis/{path}  rows={len(data)}")
    write("tools.csv", ["rep","arm","filename","language","loc","purpose","category",
                        "pulled_at","attestation"], rows)
    write("tools_summary.csv", ["rep","arm","script_count","total_loc","external_packages",
                                "external_binaries","vendored_packages","generated_job_scripts",
                                "pulled_at","attestation"], summary)
    print(f"\n  {len(rows)} scripts, {sum(r['loc'] for r in rows):,} LOC")
    print("  categories:", dict(collections.Counter(r["category"] for r in rows).most_common()))
    return 0

if __name__ == "__main__":
    sys.exit(main())
