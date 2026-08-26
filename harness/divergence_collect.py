#!/usr/bin/env python3
"""Remote-side divergence collector. Runs ON THE CLUSTER, emits NUMBERS ONLY.

    ssh dirac-bei "python3 - s01" < divergence_collect.py

Design rule that matters more than any other here: **structure names never leave the
cluster.** Every quantity that is derived from a structure name (distinct-structure count,
batch-size distribution, resubmission count) is reduced to an integer on this side of the
wire. The local side therefore cannot leak what it never receives, and a bug in the renderer
cannot turn into a disclosure.

Cluster runs python 3.6: no subprocess.capture_output, no walrus, no dict|dict.
"""
import hashlib, json, os, re, subprocess, sys, time

REP = sys.argv[1]
WRITE_USAGE = "--write-usage" in sys.argv[2:]
WS  = "/home1/users/Bei/ws/" + REP

# A benchmark structure identifier, e.g. 2021[AlAg][fet]2[ION]2 / 2023[Cu][ctn]3[FSR]1.
# Anchored at the start of a path component: 'X__stripH' is a derived variant of X, and
# counts as its base structure rather than as a new one.
STEM = re.compile(r"^(\d{4}\[[A-Za-z]+\]\[[A-Za-z0-9]+\]\d+\[[A-Z]+\]\d+)")
# [ASR]/[FSR] twins are coordinate-identical under the chargeless protocol -- one structure
# under two filenames. Collapsing on the charge tag gives the physical-structure count.
TWIN = re.compile(r"\[(?:ASR|FSR|ION|NEU)\]")

PRUNE = {"db", "prep", "toolchain", ".git", "__pycache__", "Movies", "VTK", "Restart"}
JOB_EXT = (".pbs", ".qsub", ".job", ".cmd", ".sh")
OUTPUT_MARKERS = ("DONE", "loading.txt")
CPUSEC = re.compile(r"CPUSEC\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)")

CACHE_P = os.path.join(WS, ".divergence_cache.json")


def load_cache():
    try:
        with open(CACHE_P) as fh:
            return json.load(fh)
    except Exception:
        return {}


def stem_of(path):
    """Innermost path component that names a benchmark structure, or None."""
    found = None
    for part in path.split(os.sep):
        m = STEM.match(part)
        if m:
            found = m.group(1)
    return found


def walk():
    """One pass over the workspace. Returns raw facts, still name-bearing."""
    stems_any, stems_out = set(), set()
    job_scripts = []          # (path, text)
    stderr_files, csv_files = [], []
    for dirpath, dirnames, filenames in os.walk(WS):
        dirnames[:] = [d for d in dirnames if d not in PRUNE]
        for d in dirnames:
            m = STEM.match(d)
            if m:
                stems_any.add(m.group(1))
        here = stem_of(dirpath)
        if here:
            stems_any.add(here)
            for f in filenames:
                if f in OUTPUT_MARKERS or f.endswith(".data") or f.endswith(".data.gz"):
                    stems_out.add(here)
                    break
        for f in filenames:
            p = os.path.join(dirpath, f)
            if f == "raspa.stderr":
                stderr_files.append(p)
                continue
            if f.endswith(".csv"):
                csv_files.append(p)
                continue
            if f.endswith(JOB_EXT):
                try:
                    if os.path.getsize(p) > 512 * 1024:
                        continue
                    with open(p, errors="replace") as fh:
                        txt = fh.read()
                except Exception:
                    continue
                if "#PBS -N" in txt:
                    job_scripts.append((p, txt))
    return stems_any, stems_out, job_scripts, stderr_files, csv_files


def job_facts(job_scripts):
    """Per-job: PBS name, submit time, task count, and a target signature.

    Task count ("batch size") is the number of simulation tasks one submitted job carries.
    Both arms express that the same way once resolved: either the script names a task-list
    file (one task per line), or it inlines one run directory per task.
    """
    names, sizes, sigs, mtimes = [], [], [], []
    for path, txt in job_scripts:
        m = re.search(r"#PBS\s+-N\s+(\S+)", txt)
        names.append(m.group(1) if m else os.path.basename(path))
        try:
            mtimes.append(os.path.getmtime(path))
        except Exception:
            pass
        # (a) a task-list file the script hands to a runner
        tasks, stems = None, set()
        for cand in re.findall(r"[\w./\-\[\]]+\.txt", txt):
            cp = cand if cand.startswith("/") else os.path.join(os.path.dirname(path), cand)
            if not os.path.isfile(cp):
                continue
            try:
                with open(cp, errors="replace") as fh:
                    lines = [l for l in fh if l.strip() and not l.lstrip().startswith("#")]
            except Exception:
                continue
            tasks = len(lines)
            for l in lines:
                for fld in l.split():
                    mm = STEM.match(fld)
                    if mm:
                        stems.add(mm.group(1))
            break
        # (b) otherwise, one run directory per task, inlined in the script
        if tasks is None:
            rundirs = set()
            for mm in re.finditer(r"(\d{4}\[[A-Za-z]+\]\[[A-Za-z0-9]+\]\d+\[[A-Z]+\]\d+)"
                                  r"([\w.\-]*)/([\w.\-]+)", txt):
                rundirs.add(mm.group(0))
                stems.add(mm.group(1))
            tasks = len(rundirs)
        sizes.append(tasks if tasks > 0 else None)   # None = task count not resolvable
        sigs.append(hashlib.sha256((",".join(sorted(stems)) or "-").encode()).hexdigest()[:16])
    return names, sizes, sigs, mtimes


def qstat_live():
    env = dict(os.environ)
    env["PATH"] = env.get("PATH", "") + ":/usr/local/pbs/bin"
    try:
        out = subprocess.run(["qstat", "-f"], stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, env=env).stdout.decode("utf-8", "replace")
    except Exception:
        return {"running": 0, "queued": 0, "held": 0, "cpu_s": 0.0, "earliest_ctime": None,
                "names": [], "ids": [], "reachable": False}
    run_n = q_n = h_n = 0
    cpu_s = 0.0
    earliest = None
    names, ids = [], []
    for b in re.split(r"\nJob Id: ", out):
        # A job belongs to this replicate if its name is prefixed with the replicate id or it
        # writes into the replicate's workspace. Either alone would miss jobs.
        if (REP + "_") not in b and ("/ws/" + REP + "/") not in b:
            continue
        ids.append(b.split("\n", 1)[0].strip())
        nm = re.search(r"Job_Name\s*=\s*(\S+)", b)
        if nm:
            names.append(nm.group(1))
        st = re.search(r"job_state\s*=\s*(\w)", b)
        s = st.group(1) if st else "?"
        if s == "R":
            run_n += 1
        elif s == "H":
            h_n += 1
        else:
            q_n += 1
        cm = re.search(r"resources_used\.cput\s*=\s*(\d+):(\d+):(\d+)", b)
        if cm:
            hh, mi, ss = map(int, cm.groups())
            cpu_s += hh * 3600 + mi * 60 + ss
        ct = re.search(r"ctime\s*=\s*(.+)", b)
        if ct:
            try:
                t = time.mktime(time.strptime(ct.group(1).strip(), "%a %b %d %H:%M:%S %Y"))
                earliest = t if earliest is None else min(earliest, t)
            except Exception:
                pass
    return {"running": run_n, "queued": q_n, "held": h_n, "cpu_s": cpu_s,
            "earliest_ctime": earliest, "names": names, "ids": ids, "reachable": True}


def cpu_from_disk(stderr_files, csv_files, cache):
    """Single-core wall seconds per completed run -- the one CPU figure both arms express.

    PBS drops finished jobs from qstat and this account cannot read the accounting log, so
    the scheduler cannot account for a job that has already left. What each run leaves on
    disk can: an elapsed time written by /usr/bin/time, or a wall_s column in a results CSV.
    Both are single-core runs, so wall-hours are CPU-hours. Cached by path -- a finished run
    never changes.
    """
    new = {}
    stderr_s, stderr_n, csv_s, csv_n = 0.0, 0, 0.0, 0
    counted = set()
    for p in stderr_files:
        if p in cache:
            v = cache[p]
        else:
            v = None
            try:
                with open(p, "rb") as fh:
                    fh.seek(max(0, os.path.getsize(p) - 4096))
                    tail = fh.read().decode("utf-8", "replace")
                m = CPUSEC.search(tail)
                if m:
                    v = float(m.group(3))          # elapsed
            except Exception:
                v = None
            if v is not None:
                new[p] = v
        if v is not None:
            stderr_s += v
            stderr_n += 1
            counted.add(os.path.dirname(p))
    # A results CSV row and a raspa.stderr can describe the SAME run. Keying the CSV row back
    # to its run directory and skipping anything already counted is what keeps the two disk
    # sources from silently adding up to twice the real burn.
    for p in csv_files:
        try:
            with open(p, errors="replace") as fh:
                head = fh.readline().rstrip("\n").split(",")
                if "wall_s" not in head:
                    continue
                iw = head.index("wall_s")
                ir = head.index("runroot") if "runroot" in head else None
                inm = head.index("name") if "name" in head else None
                ip = head.index("pressure_Pa") if "pressure_Pa" in head else None
                for line in fh:
                    fld = line.rstrip("\n").split(",")
                    if len(fld) <= iw:
                        continue
                    key = None
                    if ir is not None and inm is not None and ip is not None and len(fld) > max(ir, inm, ip):
                        key = os.path.join(WS, fld[ir], fld[inm], "P" + fld[ip])
                    if key is not None and key in counted:
                        continue
                    try:
                        csv_s += float(fld[iw]); csv_n += 1
                    except ValueError:
                        continue
                    if key is not None:
                        counted.add(key)
        except Exception:
            continue
    cache.update(new)
    return stderr_s, stderr_n, csv_s, csv_n


def main():
    if not os.path.isdir(WS):
        print(json.dumps({"replicate": REP, "reachable": False}))
        return
    cache = load_cache()
    stems_any, stems_out, job_scripts, stderr_files, csv_files = walk()
    names, sizes, sigs, mtimes = job_facts(job_scripts)
    live = qstat_live()
    st_s, st_n, cs_s, cs_n = cpu_from_disk(stderr_files, csv_files, cache)
    try:
        with open(CACHE_P, "w") as fh:
            json.dump(cache, fh)
    except Exception:
        pass

    # finished-job CPU banked by harvest_cput.sh, for the scheduler-side figure
    fin_s = 0.0
    fp = os.path.join(WS, "cput_finished.txt")
    if os.path.exists(fp):
        for line in open(fp, errors="replace"):
            try:
                fin_s += float(line.split()[0])
            except Exception:
                pass

    submitted = len(job_scripts)
    live_n = live["running"] + live["queued"] + live["held"]
    first = min(mtimes) if mtimes else None
    if live["earliest_ctime"] is not None:
        first = live["earliest_ctime"] if first is None else min(first, live["earliest_ctime"])

    disk_h = (st_s + cs_s) / 3600.0

    hist = {}
    for s in sizes:
        k = "unresolved" if s is None else str(s)
        hist[k] = hist.get(k, 0) + 1
    resolved = [s for s in sizes if s is not None]

    # A resubmission is one PBS job name submitted more than once: duplicate -N across job
    # scripts, plus any name currently live more times than it has scripts.
    dup_scripts = len(names) - len(set(names))
    live_dup = 0
    for nm in set(live["names"]):
        live_dup += max(0, live["names"].count(nm) - 1)

    # PI ruling 2026-08-27: the RECORDED compute meter is the job-record basis. The scheduler
    # figure cannot see a job it has already dropped and undercounted by more than an order of
    # magnitude; it is kept beside the recorded meter, not as the recorded meter.
    if WRITE_USAGE:
        up = os.path.join(WS, "usage.json")
        try:
            d = json.load(open(up)) if os.path.exists(up) else {}
        except Exception:
            d = {}
        d["cpu_h"] = round(disk_h, 3)
        d["cpu_h_basis"] = "job-records (single-core elapsed per finished run)"
        d["cpu_h_scheduler"] = round((live["cpu_s"] + fin_s) / 3600.0, 3)
        d["cpu_h_runs_accounted"] = st_n + cs_n
        with open(up, "w") as fh:
            json.dump(d, fh)

    out = {
        "replicate": REP,
        "reachable": True,
        "pbs_reachable": live["reachable"],
        "first_submission_epoch": first,
        "jobs_submitted": submitted,
        "jobs_running": live["running"],
        "jobs_queued": live["queued"] + live["held"],
        "jobs_completed": max(0, submitted - live_n),
        "structures_distinct": len(stems_any),
        "structures_with_output": len(stems_out),
        "structures_collapsed": len(set(TWIN.sub("[*]", s) for s in stems_any)),
        "batch_hist": hist,
        "batch_tasks_total": sum(resolved),
        "batch_jobs_resolved": len(resolved),
        "cpu_h_scheduler": round((live["cpu_s"] + fin_s) / 3600.0, 3),
        "cpu_h_disk": round(disk_h, 3),
        "runs_accounted": st_n + cs_n,
        "resubmissions_scripts": dup_scripts + live_dup,
        # PBS job names + ids for the live set. Job names carry no structure identity; the
        # local side keeps a name -> ids ledger so a name resubmitted under a NEW id is
        # counted even though PBS has already dropped the old one.
        "live_jobs": list(zip(live["names"], live["ids"])) if len(live["names"]) == len(live["ids"]) else [],
    }
    print(json.dumps(out))


main()
