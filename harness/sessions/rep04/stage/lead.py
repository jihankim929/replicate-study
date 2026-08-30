#!/usr/bin/env python3
"""Leaderboard across every result file, keeping method provenance separate.

Grid-based and grid-free numbers are never mixed into one working capacity:
charter section 3 requires any grid-based number promoted to the report to say so,
and a difference taken across two methods would be untraceable to either.
"""
import sys, os, csv, math, collections

WS = os.environ.get('REP04_WS', '/home1/users/Bei/ws/rep04')
FILES = ['t1', 'calib', 'blogin', 'gridchk', 'bench', 'probe', 'tier1a', 'claim', 'tier2']


def load_all():
    """-> {(sid, grid, ninit, nprod, seed): {P: (vol, err, wall)}}"""
    by = collections.defaultdict(dict)
    for f in FILES:
        p = os.path.join(WS, 'results', f + '.csv')
        if not os.path.exists(p):
            continue
        for r in csv.DictReader(open(p)):
            if not r.get('vol_cm3cm3') or r.get('ok') != 'OK':
                continue
            k = (r['sid'], r['grid'], r['ninit'], r['nprod'], r['seed'])
            by[k][round(float(r['P_Pa'])/1e5, 1)] = (float(r['vol_cm3cm3']),
                                                     float(r['vol_err']), int(r['wall_s']), f)
    return by


def main():
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    by = load_all()
    desc = {r['sid']: r for r in csv.DictReader(open(os.path.join(WS, 'manifest/desc_all.csv')))}

    rows = []
    for (sid, grid, ninit, nprod, seed), d in by.items():
        if 65.0 in d and 5.8 in d:
            hi, lo = d[65.0], d[5.8]
            rows.append(dict(sid=sid, grid=grid, cycles='%s+%s' % (ninit, nprod), seed=seed,
                             dc=hi[0]-lo[0], err=math.hypot(hi[1], lo[1]),
                             n65=hi[0], n58=lo[0], cost=hi[2]+lo[2]))
    rows.sort(key=lambda r: -r['dc'])

    print('%-8s %8s %6s %8s %8s %4s %-11s %5s %7s  %s'
          % ('sid', 'DC', '+/-', 'N65', 'N5.8', 'grid', 'cycles', 'seed', 'sur', 'name'))
    for r in rows[:top]:
        print('%-8s %8.2f %6.2f %8.2f %8.2f %4s %-11s %5s %7.1f  %s'
              % (r['sid'], r['dc'], r['err'], r['n65'], r['n58'], r['grid'], r['cycles'],
                 r['seed'], float(desc[r['sid']]['lda_dc_v']), desc[r['sid']]['name']))

    npair = len(rows)
    nhalf = sum(1 for d in by.values() if len(d) == 1)
    cost = sum(v[2] for d in by.values() for v in d.values())
    print('\ncomplete pairs %d | half-done structures %d | measured cost %.1f CPU-h'
          % (npair, nhalf, cost/3600.0))

    # surrogate quality, measured only on grid-free floor-cycle pairs
    base = [r for r in rows if r['grid'] == 'no' and r['cycles'] == '2000+10000']
    if len(base) >= 8:
        import numpy as np
        y = np.array([r['dc'] for r in base])
        s = np.array([float(desc[r['sid']]['lda_dc_v']) for r in base])
        rx = np.argsort(np.argsort(s)).astype(float); ry = np.argsort(np.argsort(y)).astype(float)
        rx -= rx.mean(); ry -= ry.mean()
        rho = float((rx*ry).sum()/math.sqrt((rx*rx).sum()*(ry*ry).sum()))
        print('surrogate vs GCMC on %d grid-free floor pairs: Spearman %+.3f, '
              'mean ratio GCMC/surrogate %.2f' % (len(base), rho, float((y/s).mean())))


if __name__ == '__main__':
    main()
