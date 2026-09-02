#!/usr/bin/env python3
"""fig2_jobs.csv -- A RECONSTRUCTION FROM RUN OUTPUTS, NOT AN EXTRACTION FROM A RECORD.

Authorised by the PI 2026-09-03 after REPORT 031 established that no replicate-authored record
carries the per-job association this table needs: `cput_finished.txt`, the metering source every
usage.json names, is two fields (cput-seconds, job id) with no structure, tier or timing; and the
collected JOBS.md is a batch ledger whose single rows cover hundreds of structures with no
completion timestamps. **Every row below is therefore inferred from RASPA's own output files, and
the file must be read as derived.** It is also outside the seal: the workspaces were never
collected. Line 1 is a `#` UNATTESTED header.

WHAT EACH FIELD IS, AND WHAT IT IS NOT
  t_submitted   RASPA's OWN simulation start, parsed from the output header ("Sat Aug 29 14:37:36
                2026"). It is NOT the PBS submit time -- a job may sit queued for hours before
                RASPA starts, and that queue wait is invisible here.
  t_completed   mtime of the output file. It is NOT a recorded completion time; a file touched
                after the run would move it, and a killed run keeps the mtime of its last write.
  job_id        EMPTY. RASPA output carries no PBS job id and the run trees do not record one, so
                there is nothing to put here. `output_path` identifies the row instead.
  accuracy_tier CYCLES-TO-TIER MAPPING, from config.RATIFIED: cycles_claim = 10,000 init +
                50,000 production; cycles_screen = 2,000 init + 10,000 production. A file is
                `high` iff init >= 10,000 AND production >= 50,000; every other cycle count is
                `low`. Runs used many intermediate counts (200+500, 2,000+10,000, 3,000) and all
                of those fall to `low` by this rule.

Both times are reported as hours since that run's own launched_at, per the standing convention.
"""
import csv, json, re, sys, pathlib, datetime as dt
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"harness")); import behavioral_extract as B

EXCLUDED = {"2020[Fe][hcb]2","2021[Cu][sql]2","2010[Co][tbo]3","2017[Fe][nan]3",
            "2015[Cu][pcu]3","2009[Cd][nan]3"}
AGENT  = re.compile(r'__\d+of\d+|_DENET|\+DEAQ|@(f|me)\d+|_mod\b')
BRACK  = re.compile(r'(\d{4}\[[A-Za-z]{1,6}\]\[[a-z]{3}\]\d(?:\[(?:ASR|FSR|ION)\]\d+)?)')
# Replicate-internal sids. rep03, rep04 and rep08 name their run directories `s08559`, `s10985`
# and never the structure -- the same scheme that hid rep04's leaderboard from the first pass in
# REPORT 026. The sid is recorded AS the structure identifier and is NOT resolved to a structure
# name: only rep04 states a mapping (for one sid), and borrowing rep08's sid table to fill the
# others would be a cross-replicate inference presented as a fact. structure_class is left empty
# for these, because class cannot be assigned to an unresolved id.
# FIVE distinct replicate-internal id schemes are in use across the sixteen and each had to be
# found by reading the paths that failed: lowercase `s08559` (rep03, rep08), UPPERCASE `S10985`
# (rep04), `m02778` (rep09) and hex-like `f141371e1` (rep05). Generalised to a short alpha prefix
# plus a hex-ish body, with the prefix recorded so the scheme is visible per row.
SIDNUM = re.compile(r'[/_]([A-Za-z]{1,2}[0-9a-f]{4,9})(?:[_/]|\.data)')
# Runs that are not a database structure at all: RASPA's own test frames, the calibration
# benchmarks, and the bulk-fluid boxes used for reference density. Distinguished from failures.
NONSTRUCT = re.compile(r'output_(s_test|sT|frame|Box|S|bench\d*)_|/bulk_|/smoke/|/bench|/diag/|'
                       r'/t0/|/dbg/|bench\d*/')
UNDER  = re.compile(r'(\d{4})_([A-Za-z]{1,6})_+([a-z]{3})_(\d)_(ASR|FSR|ION)_(\d+)')
GROUP  = {"gated":"C","ungated":"U"}
HDR = ("# UNATTESTED and DERIVED. Reconstructed from RASPA output trees in the replicate "
       "workspaces on bnode0, read-only, 2026-09-03. Not an extraction from any replicate-authored "
       "record; the per-job association does not exist in one. Outside the sealed 16/16 "
       "attestation. t_submitted is RASPA's own start, NOT the PBS submit time. Skip this line.\n")

def sid(path):
    m = BRACK.search(path)
    if m: return m.group(1), "bracket form in path"
    m = UNDER.search(path)
    if m: return f"{m.group(1)}[{m.group(2)}][{m.group(3)}]{m.group(4)}[{m.group(5)}]{m.group(6)}", "underscore form in path"
    if NONSTRUCT.search(path): return "", "non-structure run (test / calibration / bulk fluid)"
    m = SIDNUM.search(path)
    if m: return m.group(1), f"replicate-internal id, scheme '{m.group(1)[0]}' (unresolved)"
    return "", ""

def klass(name, how=""):
    # An unresolved sid has NO class. The first draft returned "retained" for 9,768 of them, which
    # is a claim against the sealed exclusion set that the id cannot support -- an unresolved
    # identifier is not evidence that a structure is not on the list.
    if how.startswith("replicate-internal id"): return ""
    if not name: return ""
    if AGENT.search(name): return "agent_modified"
    b = re.sub(r'\[(ASR|FSR|ION)\]\d+$', '', name)
    return "excluded" if b in EXCLUDED else "retained"

def main(hdr_path, mt_path):
    launch = {r: dt.datetime.fromisoformat(json.load(open(B.COLL/r/"WORKSPACE.json"))["launched_at"])
              for r in B.REPS}
    mt = {}
    for l in open(mt_path):
        p, t = l.rstrip("\n").split("\t"); mt[p] = float(t)
    rows, unassoc, noheader = [], 0, 0
    seen = set()
    for l in open(hdr_path):
        f = l.rstrip("\n").split("\t")
        if len(f) != 4: continue
        path, start, init, prod = f
        seen.add(path)
        run = path.split("/")[0]
        if run not in launch: continue
        L0 = launch[run]
        try:
            st = dt.datetime.strptime(start, "%a %b %d %H:%M:%S %Y").replace(tzinfo=L0.tzinfo)
        except ValueError:
            continue
        en = dt.datetime.fromtimestamp(mt[path], L0.tzinfo) if path in mt else None
        s, how = sid(path)
        if not s: unassoc += 1
        tier = "high" if (int(init) >= 10000 and int(prod) >= 50000) else "low"
        rows.append(dict(run=run, job_id="", t_submitted=f"{(st-L0).total_seconds()/3600:.3f}",
            t_completed=f"{(en-L0).total_seconds()/3600:.3f}" if en else "",
            accuracy_tier=tier, structure_id=s, structure_class=klass(s, how),
            init_cycles=init, production_cycles=prod, id_source=how, output_path=path))
    noheader = len(mt) - len(seen)
    p = ROOT/"analysis/fig2_jobs.csv"
    cols = ["run","job_id","t_submitted","t_completed","accuracy_tier","structure_id",
            "structure_class","init_cycles","production_cycles","id_source","output_path"]
    with p.open("w", newline="") as fh:
        fh.write(HDR); w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
        for r in rows: w.writerow(r)
    import collections
    print(f"  wrote analysis/fig2_jobs.csv  rows={len(rows)}")
    print(f"  output files found            {len(mt)}")
    print(f"  header unparseable / skipped  {noheader}")
    ns = sum(1 for r in rows if r["id_source"].startswith("non-structure"))
    print(f"  rows with NO structure id     {unassoc}  (of which non-structure runs: {ns};"
          f" genuinely unassociated: {unassoc-ns})")
    print("  id_source:", dict(collections.Counter(r['id_source'] for r in rows)))
    print("  tier:", dict(collections.Counter(r['accuracy_tier'] for r in rows)))
    print("  class:", dict(collections.Counter(r['structure_class'] for r in rows)))
    # fallback table the PI asked for either way
    per = collections.defaultdict(lambda: collections.defaultdict(set))
    for r in rows:
        if r["structure_id"]: per[r["run"]][r["accuracy_tier"]].add(r["structure_id"])
    print("\n  distinct structures simulated, by tier:")
    for r in B.REPS:
        print(f"    {r:<6} low={len(per[r]['low']):>5}  high={len(per[r]['high']):>4}")
    return 0
if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
