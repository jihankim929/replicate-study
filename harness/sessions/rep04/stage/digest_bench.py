#!/usr/bin/env python3
"""Compact digest of the cost-model benchmark: one line per case, plus the
cost model the campaign will be planned against."""
import csv, os, sys, collections

WS = os.environ.get('REP04_WS', '/home1/users/Bei/ws/rep04')
rows = list(csv.DictReader(open(os.path.join(WS, 'results/bench.csv'))))
man = {r['sid']: r for r in csv.DictReader(open(os.path.join(WS, 'manifest/structures.csv')))}

print('%-8s %-6s %-4s %8s %9s %9s %8s %6s' %
      ('sid', 'P/bar', 'grid', 'wall_s', 'V_cm3cm3', '+/-', 'rho', 'natoms'))
by = {}
for r in rows:
    if not r.get('vol_cm3cm3'):
        print('%-8s %-6s %-4s %8s   FAILED rc=%s %s' %
              (r['sid'], float(r['P_Pa'])/1e5, r['grid'], r['wall_s'], r['rc'], r['ok']))
        continue
    p = float(r['P_Pa'])/1e5
    print('%-8s %-6g %-4s %8s %9.3f %9.3f %8.0f %6s' %
          (r['sid'], p, r['grid'], r['wall_s'], float(r['vol_cm3cm3']),
           float(r['vol_err']), float(r['rho_kgm3']), man[r['sid']]['natoms']))
    by[(r['sid'], p, r['grid'])] = r

print()
print('--- working capacity (65 - 5.8 bar), grid-free, floor cycles ---')
for sid in sorted({k[0] for k in by}):
    a = by.get((sid, 65.0, 'no')); b = by.get((sid, 5.8, 'no'))
    if a and b:
        dc = float(a['vol_cm3cm3']) - float(b['vol_cm3cm3'])
        err = (float(a['vol_err'])**2 + float(b['vol_err'])**2)**0.5
        print('%-8s DC=%7.2f +/- %5.2f   (65bar %7.2f, 5.8bar %6.2f)  cost=%s s'
              % (sid, dc, err, float(a['vol_cm3cm3']), float(b['vol_cm3cm3']),
                 int(a['wall_s']) + int(b['wall_s'])))

print()
print('--- grid vs grid-free at 65 bar ---')
for sid in sorted({k[0] for k in by}):
    a = by.get((sid, 65.0, 'no')); g = by.get((sid, 65.0, 'yes'))
    if a and g:
        va, vg = float(a['vol_cm3cm3']), float(g['vol_cm3cm3'])
        ea, eg = float(a['vol_err']), float(g['vol_err'])
        sp = int(a['wall_s'])/max(int(g['wall_s']), 1)
        print('%-8s direct %7.2f+/-%.2f  grid %7.2f+/-%.2f  diff %+6.2f (%+5.1f%%)  '
              'speedup x%.1f (%ss -> %ss)'
              % (sid, va, ea, vg, eg, vg-va, 100*(vg-va)/max(va, 1e-9), sp,
                 a['wall_s'], g['wall_s']))

tot = sum(int(r['wall_s']) for r in rows if r.get('wall_s'))
nok = sum(1 for r in rows if r.get('vol_cm3cm3'))
print('\ntotal benchmark cost %.2f CPU-h over %d completed cases' % (tot/3600.0, nok))
