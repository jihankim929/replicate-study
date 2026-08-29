#!/bin/bash
# Keeps the Tier-1 screen alive without a live session.
#
# Bounded on purpose: it only ever resubmits s1 chunks that (a) still have
# unfinished tasks and (b) are not currently in the mjs queue, and it never
# lets the rep09 queue exceed MAXQ. It submits nothing else, so it cannot
# start a tier I have not decided on.
WS=/home1/users/Bei/ws/rep09
MAXQ=11
LOGF=$WS/logs/autopilot.log
mkdir -p $WS/logs

while true; do
    NQ=$(/usr/local/mjs/qinfo 2>/dev/null | grep -c "rep09_")
    if [ "$NQ" -lt "$MAXQ" ]; then
        for k in 00 01 02 03 04 05 06 07 08 09 10; do
            NQ=$(/usr/local/mjs/qinfo 2>/dev/null | grep -c "rep09_")
            [ "$NQ" -ge "$MAXQ" ] && break
            /usr/local/mjs/qinfo 2>/dev/null | grep -q "rep09_s1_$k" && continue
            NEED=$(/bin/python3 $WS/bin/remaining.py s1 $k)
            if [ "$NEED" -gt 0 ]; then
                echo "$(date -Iseconds) resubmit s1_$k ($NEED points left)" >> $LOGF
                /usr/local/mjs/qas $WS/jobs/s1_$k.pbs >> $LOGF 2>&1
                sleep 5
            fi
        done
    fi
    sleep 300
done
