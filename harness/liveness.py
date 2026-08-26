#!/usr/bin/env python3
"""Death detection by TRANSCRIPT GROWTH (PI ruling 2026-08-27).

Supersedes heartbeat staleness as the liveness criterion everywhere in the harness.

Why the heartbeat was the wrong signal. It was a *proxy*: a wrapper touched a file on the
cluster when it believed the agent had done something. A proxy can fail on its own, and one
did -- a replicate's heartbeat went 14.5 hours stale while its agent was demonstrably working,
which under the old rule was one dead screen session away from restarting a healthy campaign.
Transcript growth is not a proxy. It is the agent's own record of its own work, written by
Claude Code, on the machine the harness already runs on, with no network hop and no wrapper in
between. If it grows, the agent acted; if it never grows, no signal elsewhere can make that
false.

The heartbeat file is still written and still reported, as evidence about the wrapper. It no
longer decides anything.
"""
import argparse, glob, json, os, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = HERE / ".transcript_growth.json"


def session_dir(rep: str) -> Path:
    cwd = HERE / "sessions" / rep
    return Path(os.path.expanduser("~/.claude/projects/" + str(cwd).replace("/", "-")))


def transcript_bytes(rep: str) -> int:
    total = 0
    for f in glob.glob(str(session_dir(rep) / "*.jsonl")):
        try:
            total += os.path.getsize(f)
        except OSError:
            pass
    return total


def check(rep: str, update: bool = True) -> dict:
    """Minutes since this replicate's transcript last GREW.

    First observation records a baseline and reports age 0 -- the harness has no evidence of
    death it has not yet had time to gather, and inventing some would restart live sessions.
    """
    now = time.time()
    try:
        st = json.loads(STATE.read_text()) if STATE.exists() else {}
    except Exception:
        st = {}
    size = transcript_bytes(rep)
    prev = st.get(rep)
    if prev is None:
        rec = {"size": size, "grew_at": now, "first_seen": now}
    elif size > prev.get("size", 0):
        rec = {"size": size, "grew_at": now, "first_seen": prev.get("first_seen", now)}
    else:
        rec = dict(prev)
        rec["size"] = size
    if update:
        st[rep] = rec
        try:
            STATE.write_text(json.dumps(st, indent=2))
        except Exception:
            pass
    return {"replicate": rep, "bytes": size,
            "age_min": round((now - rec["grew_at"]) / 60, 1),
            "transcripts_present": size > 0,
            "baseline_only": prev is None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rep")
    ap.add_argument("--age-min", action="store_true", help="print the age in minutes and exit")
    ap.add_argument("--no-update", action="store_true", help="read without recording an observation")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dead-after", type=float, metavar="MIN",
                    help="exit 0 only if the transcript has not grown for MIN minutes; "
                         "exit 1 in every other case, including every error")
    a = ap.parse_args()
    r = check(a.rep, update=not a.no_update)
    if a.dead_after is not None:
        # Fail safe, deliberately. This exit code authorises restarting a running campaign,
        # so anything short of positive evidence of death -- no transcripts, an unreadable
        # state file, a crash -- must exit non-zero and restart nothing. The old shell version
        # of this comparison defaulted the other way when its arithmetic failed.
        if not r["transcripts_present"] or r["baseline_only"]:
            print("[liveness] %s: no positive evidence of death (%s)"
                  % (a.rep, "no transcripts" if not r["transcripts_present"] else "baseline only"))
            return 1
        dead = r["age_min"] >= a.dead_after
        print("[liveness] %s: transcript last grew %.1f min ago, threshold %.0f -> %s"
              % (a.rep, r["age_min"], a.dead_after, "DEAD" if dead else "alive"))
        return 0 if dead else 1
    if a.age_min:
        # No transcripts at all is not "age 0" -- it is no evidence either way. Report a
        # sentinel the caller must decide about rather than a reassuring number.
        print(-1 if not r["transcripts_present"] else r["age_min"])
    elif a.json:
        print(json.dumps(r))
    else:
        print("[liveness] %s: transcript %d bytes, last grew %.1f min ago%s"
              % (a.rep, r["bytes"], r["age_min"], "  (baseline)" if r["baseline_only"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
