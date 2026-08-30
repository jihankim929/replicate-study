#!/bin/bash
# Every live rep09 job, one full name per line: queued in mjs plus running in
# PBS. A job leaves the mjs listing the moment mjs dispatches it, so neither
# source alone is a complete census.
/usr/local/mjs/qinfo 2>/dev/null | awk '{print $3}' | grep '^rep09_'
for j in $(qstat 2>/dev/null | awk '/^[0-9]/{print $1}'); do
    qstat -f "$j" 2>/dev/null | awk '/Job_Name/{print $3}' | grep '^rep09_'
done
