#!/bin/bash
# Keeps queued waves alive without a live session.
#
# Reads jobs/autopilot.plan: one "<wave> <chunk>" per line, highest priority
# first. For each entry that is not currently live and still has unfinished
# points, it submits the chunk. Never exceeds MAXJOBS live rep09 jobs.
#
# Bug fixed 2026-08-29 20:50: the first version judged "already submitted" from
# the mjs queue listing alone, but mjs drops a job from that listing the moment
# it dispatches it, so running chunks were duplicated and the live count hit 14
# against the charter cap of 12. bin/census.sh now unions queue and running.
WS=/home1/users/Bei/ws/rep09
PLAN=$WS/jobs/autopilot.plan
MAXJOBS=12
LOGF=$WS/logs/autopilot.log
mkdir -p "$WS/logs"

while true; do
    LIVE=$(bash "$WS/bin/census.sh")
    N=$(printf '%s\n' "$LIVE" | grep -c 'rep09_')
    while read -r WAVE K; do
        [ -z "$WAVE" ] && continue
        case "$WAVE" in \#*) continue;; esac
        [ "$N" -ge "$MAXJOBS" ] && break
        printf '%s\n' "$LIVE" | grep -qx "rep09_${WAVE}_${K}" && continue
        [ -f "$WS/jobs/${WAVE}_${K}.pbs" ] || continue
        NEED=$(/bin/python3 "$WS/bin/remaining.py" "$WAVE" "$K" 2>/dev/null)
        [ -z "$NEED" ] && continue
        if [ "$NEED" -gt 0 ]; then
            echo "$(date -Iseconds) submit ${WAVE}_${K} ($NEED left, live=$N)" >> "$LOGF"
            /usr/local/mjs/qas "$WS/jobs/${WAVE}_${K}.pbs" >> "$LOGF" 2>&1
            sleep 10
            LIVE=$(bash "$WS/bin/census.sh")
            N=$(printf '%s\n' "$LIVE" | grep -c 'rep09_')
        fi
    done < "$PLAN"
    sleep 300
done
