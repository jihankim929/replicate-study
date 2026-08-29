#!/usr/bin/env python3
"""Merge the descriptor sweep with the structure manifest, rank, and select the
GCMC calibration sample.

  rank.py merge          -> manifest/desc_all.csv  (+ a short summary to stdout)
  rank.py select <n>     -> manifest/calib_sids.txt
"""
import sys, os, csv, math
import numpy as np

WS = os.environ.get('REP04_WS', '/home1/users/Bei/ws/rep04')
DESC = os.path.join(WS, 'results/desc')
OUT = os.path.join(WS, 'manifest/desc_all.csv')

KEEP = ['sid', 'V_A3', 'natoms', 'kh_boltz', 'umin_K', 'umean_neg_K', 'frac_U_lt0',
        'frac_U_ltm500', 'frac_U_ltm1000', 'frac_U_ltm1500', 'hs_1', 'hs_1.6',
        'hs_1.865', 'lda65_uc', 'lda58_uc', 'lda65_v', 'lda58_v', 'lda_dc_v']


def merge():
    man = {r['sid']: r for r in csv.DictReader(open(os.path.join(WS, 'manifest/structures.csv')))}
    rows, bad = [], 0
    for fn in sorted(os.listdir(DESC)):
        if not fn.endswith('.csv'):
            continue
        for r in csv.DictReader(open(os.path.join(DESC, fn))):
            if r.get('V_A3') in (None, 'ERR') or not r.get('lda_dc_v'):
                bad += 1
                continue
            rows.append(r)
    with open(OUT, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(KEEP + ['density_g_cm3', 'name'])
        for r in rows:
            m = man[r['sid']]
            w.writerow([r[k] for k in KEEP] + [m['density_g_cm3'], m['name']])
    dc = np.array([float(r['lda_dc_v']) for r in rows])
    print('merged %d structures (%d unusable)' % (len(rows), bad))
    for p in (50, 90, 99, 99.9):
        print('  surrogate DC p%-5s = %7.2f' % (p, np.percentile(dc, p)))
    print('  surrogate DC max     = %7.2f' % dc.max())
    order = np.argsort(-dc)
    print('  top 15 by surrogate:')
    for i in order[:15]:
        r = rows[i]
        print('    %-8s DC=%7.2f  65bar=%7.2f 5.8bar=%6.2f  hs1.865=%.3f  rho=%s  %s'
              % (r['sid'], float(r['lda_dc_v']), float(r['lda65_v']), float(r['lda58_v']),
                 float(r['hs_1.865']), man[r['sid']]['density_g_cm3'], r['name'][:34]))


def select(n):
    rows = list(csv.DictReader(open(OUT)))
    dc = np.array([float(r['lda_dc_v']) for r in rows])
    order = np.argsort(-dc)
    rng = np.random.RandomState(4)
    picked = []

    # Half the sample from the head of the ranking: that is where the surrogate
    # has to be trustworthy, and where a systematic error would actually cost a
    # candidate.  Take a spread of the top 600 rather than the top n, so the
    # calibration is not confined to a single corner of descriptor space.
    head = order[:600]
    picked += list(rng.choice(head, size=n//2, replace=False))

    # The other half stratified over the whole surrogate range, so the fit has
    # leverage away from the head and I can see if the ranking inverts anywhere.
    rest = order[600:]
    edges = np.linspace(0, len(rest), n - n//2 + 1).astype(int)
    for a, b in zip(edges[:-1], edges[1:]):
        if b > a:
            picked.append(rest[rng.randint(a, b)])

    picked = sorted(set(int(i) for i in picked))
    with open(os.path.join(WS, 'manifest/calib_sids.txt'), 'w') as f:
        for i in picked:
            f.write(rows[i]['sid'] + '\n')
    print('calibration sample: %d structures, surrogate DC from %.2f to %.2f'
          % (len(picked), min(dc[i] for i in picked), max(dc[i] for i in picked)))


if __name__ == '__main__':
    if sys.argv[1] == 'merge':
        merge()
    else:
        select(int(sys.argv[2]) if len(sys.argv) > 2 else 80)
