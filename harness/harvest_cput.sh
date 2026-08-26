#!/usr/bin/env bash
# Harvest CPU time from jobs that have LEFT the queue.
#
# PBS drops a job from `qstat` shortly after it exits, so a poller that only reads qstat loses
# the burn of every job that finished between polls -- which, at the measured 338x run-cost
# spread, is most of it. This keeps a jobid -> last-seen-cput snapshot and, when a job
# disappears, appends its final cput to <ws>/cput_finished.txt.
set -uo pipefail
REP="${1:?usage: harvest_cput.sh <repid>}"

ssh -o BatchMode=yes -o ConnectTimeout=30 dirac-bei "REP='$REP' python3 - <<'PY'
import re, os, json, subprocess
rep = os.environ['REP']
ws  = '/home1/users/Bei/ws/' + rep
snap_p = os.path.join(ws, '.cput_snapshot.json')
fin_p  = os.path.join(ws, 'cput_finished.txt')
env = dict(os.environ); env['PATH'] = env.get('PATH','') + ':/usr/local/pbs/bin'
out = subprocess.run(['qstat','-f'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                     env=env).stdout.decode('utf-8','replace')
now = {}
for b in re.split(r'\nJob Id: ', out):
    if rep + '_' not in b:
        continue
    jid = b.split('\n',1)[0].strip()
    m = re.search(r'resources_used\.cput\s*=\s*(\d+):(\d+):(\d+)', b)
    secs = 0
    if m:
        h, mi, s = map(int, m.groups()); secs = h*3600 + mi*60 + s
    now[jid] = secs
prev = {}
if os.path.exists(snap_p):
    try: prev = json.load(open(snap_p))
    except Exception: prev = {}
gone = [j for j in prev if j not in now]
if gone:
    with open(fin_p, 'a') as fh:
        for j in gone:
            fh.write('%d %s\n' % (prev[j], j))
    print('[harvest] %s: %d job(s) left the queue, %.3f CPU-h banked'
          % (rep, len(gone), sum(prev[j] for j in gone)/3600.0))
else:
    print('[harvest] %s: nothing newly finished (%d tracked)' % (rep, len(now)))
json.dump(now, open(snap_p,'w'))
PY"
