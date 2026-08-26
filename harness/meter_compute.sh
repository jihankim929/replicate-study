#!/usr/bin/env bash
# Compute metering from the SCHEDULER, not from the replicate's self-report.
#
# Closes harness/README.md limit 2. PBS is authoritative: a replicate that under-reports its
# own burn does not thereby get a bigger budget.
#
# Running jobs: resources_used.cput from `qstat -f`.
# Finished jobs: accumulated into <ws>/cput_finished.txt by harvest_cput.sh as they exit,
# because PBS drops a job from qstat shortly after it completes.
# NOTE: the cluster runs python 3.6 -- no subprocess.capture_output, no f-string '=' specifier.
set -uo pipefail
REP="${1:?usage: meter_compute.sh <repid>}"

ssh -o BatchMode=yes -o ConnectTimeout=30 dirac-bei "REP='$REP' python3 - <<'PY'
import re, os, json, subprocess
rep = os.environ['REP']
ws  = '/home1/users/Bei/ws/' + rep
env = dict(os.environ); env['PATH'] = env.get('PATH','') + ':/usr/local/pbs/bin'
out = subprocess.run(['qstat','-f'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                     env=env).stdout.decode('utf-8','replace')
cpu_s, queued = 0.0, 0
for b in re.split(r'\nJob Id: ', out):
    if rep + '_' not in b:
        continue
    queued += 1
    m = re.search(r'resources_used\.cput\s*=\s*(\d+):(\d+):(\d+)', b)
    if m:
        h, mi, s = map(int, m.groups())
        cpu_s += h*3600 + mi*60 + s
fin = 0.0
led = os.path.join(ws, 'cput_finished.txt')
if os.path.exists(led):
    for line in open(led):
        try: fin += float(line.split()[0])
        except Exception: pass
total_h = round((cpu_s + fin)/3600.0, 3)
p = os.path.join(ws, 'usage.json')
d = json.load(open(p)) if os.path.exists(p) else {}
d['cpu_h'] = total_h
d['queued_jobs'] = queued
json.dump(d, open(p,'w'))
print('[meter-compute] %s: cpu_h=%s queued_jobs=%d (running=%.3fh finished=%.3fh)'
      % (rep, total_h, queued, cpu_s/3600.0, fin/3600.0))
PY"
