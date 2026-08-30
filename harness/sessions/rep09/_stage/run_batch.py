"""Execute a task list of GCMC points with a process pool; append CSV results.

Task file lines: idx,pressure_Pa,init,prod,seed
Usage: run_batch.py <taskfile> <outcsv> <nproc> [keep|nokeep] [timeout_s]

Points already recorded `ok` in <outcsv> are skipped. Without that, a chunk
that is resubmitted after hitting a wall-time limit or a node failure would
redo from the beginning, and the watchdog would quietly burn the compute
budget re-running work that is already on disk.
"""
import sys, os, csv, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gcmc


def work(t):
    idx, press, init, prod, seed, rundir, keep, timeout = t
    try:
        return gcmc.run_point(idx, press, init, prod, rundir, seed=seed,
                              keep=keep, timeout=timeout)
    except Exception as e:
        return [idx, "?", int(press), init, prod, seed, "nan", "nan", "nan",
                "nan", "nan", -1, "0", "err:%s" % str(e)[:60]]


def already_done(outcsv):
    done = set()
    if os.path.exists(outcsv):
        try:
            for r in csv.DictReader(open(outcsv)):
                if r.get("status") == "ok":
                    done.add((int(r["idx"]), int(float(r["pressure_Pa"])),
                              int(r["ninit"]), int(r["nprod"]), int(r["seed"])))
        except Exception:
            pass
    return done


if __name__ == "__main__":
    taskfile, outcsv, nproc = sys.argv[1], sys.argv[2], int(sys.argv[3])
    keep = len(sys.argv) > 4 and sys.argv[4] == "keep"
    timeout = float(sys.argv[5]) if len(sys.argv) > 5 else None
    rundir = os.path.join(os.environ.get("SCRATCH",
                          "/home1/users/Bei/ws/rep09/scratch"),
                          "run_" + os.path.basename(taskfile).replace(".txt", "")
                          .replace(".tasks", ""))
    os.makedirs(rundir, exist_ok=True)

    done = already_done(outcsv)
    tasks, skipped = [], 0
    for L in open(taskfile):
        L = L.strip()
        if not L or L.startswith("#"):
            continue
        p = L.split(",")
        key = (int(p[0]), int(float(p[1])), int(p[2]), int(p[3]), int(p[4]))
        if key in done:
            skipped += 1
            continue
        tasks.append((key[0], float(p[1]), key[2], key[3], key[4],
                      rundir, keep, timeout))
    print("tasks", len(tasks), "skipped already ok", skipped, flush=True)

    new = not os.path.exists(outcsv)
    with open(outcsv, "a", 1) as f:
        if new:
            f.write(gcmc.HEADER + "\n")
        with mp.Pool(nproc) as pool:
            for row in pool.imap_unordered(work, tasks, chunksize=1):
                f.write(",".join(str(x) for x in row) + "\n")
    print("done", len(tasks))
