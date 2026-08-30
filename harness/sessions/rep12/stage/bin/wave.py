"""Choose the next GCMC wave and write its task list.

Selection has two arms and both are deliberate:

  exploit -- highest predicted working capacity not yet simulated.  The
             predictor is the physical Langmuir surrogate until enough GCMC
             pairs exist to fit a model on the descriptors, then a gradient
             boosting fit on residuals of that surrogate.
  explore -- a stratified random draw across surrogate deciles.  This is what
             makes the model honest (it is the only unbiased training set), and
             it is also the population G7's every-40th audit is drawn from.

usage: wave.py <wavename> <n_exploit> <n_explore> <ncyc> <ninit> <grid|-> <out.tasks>
"""
import csv, math, os, random, sys

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
sys.path.insert(0, os.path.join(WS, "pylib"))
import numpy as np

FEATS = ["density", "vf_he", "phi_geom", "qst", "lcd", "n_hi_pred",
         "n_lo_pred", "wc_pred", "log_phi_boltz", "natoms_per_v"]


def load_desc():
    p = os.path.join(WS, "tables", "descriptors.csv")
    rows = list(csv.DictReader(open(p)))
    for r in rows:
        r["log_phi_boltz"] = math.log10(max(float(r["phi_boltz"]), 1e-12))
        r["natoms_per_v"] = float(r["natoms"]) / max(float(r["density"]), 1e-6)
    return rows


def load_g3():
    p = os.path.join(WS, "tables", "g3_screen.csv")
    return dict((r["name"], r["g3"]) for r in csv.DictReader(open(p)))


def load_done():
    p = os.path.join(WS, "tables", "gcmc.csv")
    done = {}
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            if r["status"] == "OK":
                done.setdefault(r["name"], []).append(
                    (int(r["ncyc"]), r["grid"], float(r["wc"])))
            else:
                done.setdefault(r["name"], [])
    return done


def fit_model(rows, done):
    """Return name->predicted wc, and a report string."""
    X, y, names = [], [], []
    idx = dict((r["name"], r) for r in rows)
    for n, lst in done.items():
        if not lst or n not in idx:
            continue
        wc = max(v for _, _, v in lst)
        r = idx[n]
        X.append([float(r[f]) for f in FEATS])
        y.append(wc)
        names.append(n)
    if len(y) < 40:
        return None, "insufficient training data (%d)" % len(y)
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.model_selection import cross_val_predict, KFold
    X = np.array(X)
    y = np.array(y)
    m = GradientBoostingRegressor(n_estimators=400, max_depth=3,
                                  learning_rate=0.05, subsample=0.9,
                                  random_state=0)
    cv = cross_val_predict(m, X, y, cv=KFold(5, shuffle=True, random_state=0))
    r2 = 1 - ((y - cv) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    mae = float(np.abs(y - cv).mean())
    m.fit(X, y)
    Xa = np.array([[float(r[f]) for f in FEATS] for r in rows])
    pred = m.predict(Xa)
    return dict((r["name"], float(p)) for r, p in zip(rows, pred)), \
        "GBR n=%d cv_r2=%.3f cv_mae=%.2f" % (len(y), r2, mae)


def main():
    wave, nex, nrand, ncyc, ninit, grid, out = sys.argv[1:8]
    nex, nrand, ncyc, ninit = int(nex), int(nrand), int(ncyc), int(ninit)
    rows = load_desc()
    g3 = load_g3()
    done = load_done()
    elig = [r for r in rows if g3.get(r["name"], "PASS") == "PASS"]
    pred, rep = fit_model(rows, done)
    if pred is None:
        for r in elig:
            r["_p"] = float(r["wc_pred"])
    else:
        for r in elig:
            r["_p"] = pred[r["name"]]
    pool = [r for r in elig if r["name"] not in done]
    pool.sort(key=lambda r: -r["_p"])
    chosen = pool[:nex]
    rest = pool[nex:]
    # stratified explore draw over surrogate deciles of the eligible pool
    if nrand > 0 and rest:
        rnd = random.Random(20260829)
        vals = sorted(float(r["wc_pred"]) for r in rest)
        edges = [vals[int(k * (len(vals) - 1) / 10.0)] for k in range(11)]
        buckets = [[] for _ in range(10)]
        for r in rest:
            v = float(r["wc_pred"])
            k = min(9, max(0, sum(1 for e in edges[1:10] if v >= e)))
            buckets[k].append(r)
        per = nrand // 10
        for b in buckets:
            rnd.shuffle(b)
            chosen += b[:per]
        extra = nrand - per * 10
        pool2 = [r for b in buckets for r in b[per:]]
        rnd.shuffle(pool2)
        chosen += pool2[:extra]
    seen = set()
    lines = []
    for r in chosen:
        n = r["name"]
        if n in seen:
            continue
        seen.add(n)
        safe = n.replace("[", "_").replace("]", "_")
        for p, tagp in ((6500000, "65"), (580000, "58")):
            lines.append("%s|%d|%d|%d|%s__%s__p%s|%s"
                         % (n, p, ncyc, ninit, wave, safe, tagp, grid))
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wave=%s model=%s eligible=%d already_done=%d chosen=%d tasks=%d"
          % (wave, rep, len(elig), len(done), len(seen), len(lines)))
    print("chosen_pred_range=%.1f..%.1f"
          % (min(r["_p"] for r in chosen), max(r["_p"] for r in chosen)))


if __name__ == "__main__":
    main()
