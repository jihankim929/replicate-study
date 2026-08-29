#!/usr/bin/env python3
"""Emit a PBS script that runs a task list under xargs -P on one node.

usage: mkjob.py <name> <tasklist> <ppn> <nodeprop> [walltime_h] [runner]
runner = 'case' (default; each line is arguments to bin/run_case.sh)
       | 'raw'  (each line is a shell command)
"""
import sys, os

WS = '/home1/users/Bei/ws/rep04'
name, tasklist, ppn, prop = sys.argv[1:5]
wall = sys.argv[5] if len(sys.argv) > 5 else '48'
runner = sys.argv[6] if len(sys.argv) > 6 else 'case'

if runner == 'case':
    body = "xargs -P %s -L1 bash %s/bin/run_case.sh < %s" % (ppn, WS, os.path.abspath(tasklist))
else:
    body = "xargs -P %s -I@@ -d'\\n' bash -c '@@' < %s" % (ppn, os.path.abspath(tasklist))

jobfile = os.path.join(WS, 'jobs', name + '.pbs')
with open(jobfile, 'w') as f:
    f.write("""#!/bin/bash
#PBS -N rep04_%s
#PBS -q long
#PBS -l nodes=1:ppn=%s:%s
#PBS -l walltime=%s:00:00
#PBS -j oe
#PBS -o %s/logs/%s.pbslog

cd %s
export OMP_NUM_THREADS=1
export REP04_WS=%s
echo "START $(date +%%s) $(hostname) ppn=%s" > %s/logs/%s.stamp
%s
echo "END $(date +%%s)" >> %s/logs/%s.stamp
""" % (name, ppn, prop, wall, WS, name, WS, WS, ppn, WS, name, body, WS, name))
print(jobfile)
