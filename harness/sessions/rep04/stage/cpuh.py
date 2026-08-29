#!/usr/bin/env python3
"""Meter compute two ways and print one line.

busy  = sum of per-case wall seconds recorded in results/*.csv (cores actually
        doing work)
alloc = sum over jobs of (requested cores x job wall time), read from the
        START/END stamps in logs/*.pbslog; this is the conservative figure the
        campaign is metered against.
"""
import os, glob, csv, re

WS = os.environ.get('REP04_WS', '/home1/users/Bei/ws/rep04')
busy = 0.0
for f in glob.glob(os.path.join(WS, 'results', '*.csv')):
    try:
        for r in csv.DictReader(open(f)):
            if r.get('wall_s'):
                busy += float(r['wall_s'])
    except Exception:
        pass

alloc = 0.0
open_jobs = []
for f in glob.glob(os.path.join(WS, 'logs', '*.stamp')):
    txt = open(f, errors='replace').read()
    ms = re.search(r'START (\d+) (\S+) ppn=(\d+)', txt)
    me = re.search(r'END (\d+)', txt)
    if not ms:
        continue
    ppn = int(ms.group(3))
    if me:
        alloc += ppn*(int(me.group(1)) - int(ms.group(1)))
    else:
        import time
        alloc += ppn*(time.time() - int(ms.group(1)))
        open_jobs.append(os.path.basename(f))

print('busy=%.1f CPU-h  alloc=%.1f CPU-h of 1610 (%.1f%%)  open=%s'
      % (busy/3600.0, alloc/3600.0, 100*alloc/3600.0/1610.0, ','.join(open_jobs) or '-'))
