#!/usr/bin/env python3
"""Calibrate and, more importantly, *test* the screening surrogate against GCMC.

The question is not "is the surrogate correlated with GCMC" — almost any porosity
descriptor is. The question is whether it ranks correctly **at the head**, because
that is the only place a screening error costs a candidate. So this reports
head-restricted diagnostics alongside the global ones, and it reports what a
given tier-1 cut would have recalled on the calibration set.

  fit.py report                 -> diagnostics for results/calib.csv
  fit.py apply <n> <outfile>    -> write the tier-1 sid list using the fitted model
"""
import sys, os, csv, math
import numpy as np

WS = os.environ.get('REP04_WS', '/home1/users/Bei/ws/rep04')

FEATS = ['hs_1', 'hs_1.6', 'hs_1.865', 'frac_U_lt0', 'frac_U_ltm500',
         'frac_U_ltm1000', 'frac_U_ltm1500', 'lda65_v', 'lda58_v', 'lda_dc_v']


def load_desc():
    d = {}
    for r in csv.DictReader(open(os.path.join(WS, 'manifest/desc_all.csv'))):
        d[r['sid']] = r
    return d


def load_gcmc(path):
    """-> {sid: (dc, err, n65, n58, cost_s)} from a results CSV at one cycle count."""
    by = {}
    for r in csv.DictReader(open(path)):
        if not r.get('vol_cm3cm3') or r.get('ok') != 'OK':
            continue
        p = round(float(r['P_Pa'])/1e5, 1)
        by.setdefault(r['sid'], {})[p] = (float(r['vol_cm3cm3']), float(r['vol_err']),
                                          int(r['wall_s']))
    out = {}
    for sid, d in by.items():
        if 65.0 in d and 5.8 in d:
            hi, lo = d[65.0], d[5.8]
            out[sid] = (hi[0]-lo[0], math.hypot(hi[1], lo[1]), hi[0], lo[0], hi[2]+lo[2])
    return out


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx*ry).sum()/math.sqrt((rx*rx).sum()*(ry*ry).sum()))


def design(desc, sids):
    X = np.array([[float(desc[s][f]) for f in FEATS] for s in sids])
    return np.hstack([np.ones((len(sids), 1)), X])


def fit_ridge(X, y, lam=1e-2):
    A = X.T @ X + lam*np.eye(X.shape[1])*np.trace(X.T @ X)/X.shape[1]
    return np.linalg.solve(A, X.T @ y)


def report():
    desc = load_desc()
    g = load_gcmc(os.path.join(WS, 'results/calib.csv'))
    sids = sorted(g)
    if len(sids) < 10:
        print('only %d complete calibration structures; too few to fit' % len(sids))
        return
    y = np.array([g[s][0] for s in sids])
    sur = np.array([float(desc[s]['lda_dc_v']) for s in sids])
    cost = np.array([g[s][4] for s in sids], dtype=float)

    print('calibration set: %d structures with both pressures' % len(sids))
    print('GCMC working capacity: min %.1f  median %.1f  max %.1f cm3/cm3'
          % (y.min(), np.median(y), y.max()))
    print('per-structure cost (both pressures, floor cycles): median %.0f s, '
          'mean %.0f s, max %.0f s  => mean %.3f CPU-h/structure'
          % (np.median(cost), cost.mean(), cost.max(), cost.mean()/3600))

    print('\n--- surrogate as-is ---')
    print('  Spearman (all)          = %+.3f' % spearman(sur, y))
    b = sur - y
    print('  bias (surrogate - GCMC) = %+.2f cm3/cm3, RMS %.2f' % (b.mean(), math.sqrt((b*b).mean())))
    k = max(len(sids)//4, 5)
    head = np.argsort(-sur)[:k]
    print('  Spearman within surrogate top-%d = %+.3f' % (k, spearman(sur[head], y[head])))

    # recall: if I had taken the surrogate's top-k, how much of the true top-k
    # would I have caught?
    for frac in (0.1, 0.2, 0.3):
        k = max(int(round(frac*len(sids))), 3)
        true_top = set(np.argsort(-y)[:k])
        sur_top = set(np.argsort(-sur)[:k])
        print('  top-%d%% recall = %d/%d' % (int(frac*100), len(true_top & sur_top), k))

    print('\n--- ridge on descriptors, leave-one-out ---')
    X = design(desc, sids)
    pred = np.zeros(len(sids))
    for i in range(len(sids)):
        m = np.ones(len(sids), bool); m[i] = False
        w = fit_ridge(X[m], y[m])
        pred[i] = X[i] @ w
    print('  Spearman (all)   = %+.3f' % spearman(pred, y))
    r = pred - y
    print('  LOO RMSE         = %.2f cm3/cm3' % math.sqrt((r*r).mean()))
    for frac in (0.1, 0.2, 0.3):
        k = max(int(round(frac*len(sids))), 3)
        print('  top-%d%% recall = %d/%d'
              % (int(frac*100), len(set(np.argsort(-y)[:k]) & set(np.argsort(-pred)[:k])), k))

    w = fit_ridge(X, y)
    np.save(os.path.join(WS, 'manifest/ridge_w.npy'), w)
    print('\nmodel saved. coefficients (intercept first):')
    print('  ' + '  '.join('%s=%+.3g' % (n, v) for n, v in
                           zip(['1'] + FEATS, w)))

    print('\n--- worst surrogate misses in the calibration set ---')
    for i in np.argsort(-(y - sur))[:5]:
        print('  %-8s GCMC %7.2f  surrogate %7.2f  (under by %.1f)'
              % (sids[i], y[i], sur[i], y[i]-sur[i]))
    for i in np.argsort(-(sur - y))[:5]:
        print('  %-8s GCMC %7.2f  surrogate %7.2f  (over by %.1f)'
              % (sids[i], y[i], sur[i], sur[i]-y[i]))


def apply_model(n, outfile):
    desc = load_desc()
    sids = sorted(desc)
    w = np.load(os.path.join(WS, 'manifest/ridge_w.npy'))
    X = design(desc, sids)
    pred = X @ w
    order = np.argsort(-pred)[:n]
    with open(outfile, 'w') as f:
        for i in order:
            f.write('%s\t%.3f\n' % (sids[i], pred[i]))
    print('wrote %d candidates, predicted DC from %.1f to %.1f'
          % (len(order), pred[order].max(), pred[order].min()))


if __name__ == '__main__':
    if sys.argv[1] == 'report':
        report()
    else:
        apply_model(int(sys.argv[2]), sys.argv[3])
