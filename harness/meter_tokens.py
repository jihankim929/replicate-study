#!/usr/bin/env python3
"""Token metering — sum Claude Code's own usage records into <ws>/usage.json.

Basis (ratified): input + output + cache_creation. Cache reads excluded.

This reads the SAME source the 12 M budget was derived from — Claude Code's per-message
`usage` records — so the number the budget was set from is the number the meter reports.
Deriving the budget from one instrument and metering with another is how budgets quietly
stop meaning anything.
"""
import argparse, glob, json, os, sys
from pathlib import Path

FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens")


def per_day(session_dir: Path) -> dict:
    """Per-calendar-day usage, for pricing the main run from measured smoke burn.

    A campaign total cannot price a 14-day run: the prior campaign averaged 2.8 M/day across
    11 days but peaked at 5.73 M, and the difference decides whether a budget binds. Daily
    resolution is the thing that makes the smoke's burn usable as a forecast.
    """
    days = {}
    for f in sorted(glob.glob(str(session_dir / "*.jsonl"))):
        for line in open(f, errors="replace"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            u = (d.get("message") or {}).get("usage") or d.get("usage")
            if not isinstance(u, dict):
                continue
            day = (d.get("timestamp") or "")[:10] or "unknown"
            e = days.setdefault(day, {f2: 0 for f2 in FIELDS})
            e.setdefault("cache_read_input_tokens", 0)
            for k in list(e):
                e[k] += u.get(k) or 0
    for day, e in days.items():
        e["billable"] = sum(e[f2] for f2 in FIELDS)
    return days


def count(session_dir: Path) -> dict:
    total = {f: 0 for f in FIELDS}
    total["cache_read_input_tokens"] = 0
    for f in sorted(glob.glob(str(session_dir / "*.jsonl"))):
        for line in open(f, errors="replace"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            u = (d.get("message") or {}).get("usage") or d.get("usage")
            if not isinstance(u, dict):
                continue
            for k in list(total):
                total[k] += u.get(k) or 0
    total["billable"] = sum(total[f] for f in FIELDS)
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session-dir", required=True,
                    help="~/.claude/projects/<encoded-path> for this replicate")
    ap.add_argument("--remote-ws", required=True, help="workspace_root on the cluster")
    ap.add_argument("--ssh-alias", default="dirac-bei")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    sd = Path(os.path.expanduser(a.session_dir))
    t = count(sd)
    # daily ledger -- append-only, one line per (replicate, day), rewritten in place per day
    rep = a.remote_ws.rstrip("/").split("/")[-1]
    days = per_day(sd)
    led = Path(__file__).parent / "token_daily.jsonl"
    existing = []
    if led.exists():
        for line in open(led):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if not (r.get("replicate") == rep and r.get("day") in days):
                existing.append(r)
    with open(led, "w") as fh:
        for r in existing:
            fh.write(json.dumps(r) + "\n")
        for day in sorted(days):
            fh.write(json.dumps({"replicate": rep, "day": day, **days[day]}) + "\n")
    print(f"[meter] {rep} daily burn:")
    for day in sorted(days):
        d0 = days[day]
        print(f"    {day}  billable={d0['billable']:>12,}  "
              f"(in={d0['input_tokens']:,} out={d0['output_tokens']:,} "
              f"cc={d0['cache_creation_input_tokens']:,})  "
              f"cache_read={d0['cache_read_input_tokens']:,}")
    print(f"[meter] billable={t['billable']:,} "
          f"(in={t['input_tokens']:,} out={t['output_tokens']:,} "
          f"cache_create={t['cache_creation_input_tokens']:,}) "
          f"| cache_read={t['cache_read_input_tokens']:,} EXCLUDED")

    # merge into the remote usage.json without clobbering the compute figure
    payload = json.dumps({"tokens": t["billable"]})
    cmd = (f"python3 - <<'PY'\n"
           f"import json,os\n"
           f"p=os.path.join({a.remote_ws!r},'usage.json')\n"
           f"d=json.load(open(p)) if os.path.exists(p) else {{}}\n"
           f"d.update(json.loads({payload!r}))\n"
           f"json.dump(d,open(p,'w'))\n"
           f"print('usage.json ->',d)\n"
           f"PY")
    if a.dry_run:
        print("[meter] (dry-run) would push tokens to", a.remote_ws + "/usage.json")
        return
    os.execvp("ssh", ["ssh", "-o", "BatchMode=yes", a.ssh_alias, cmd])


if __name__ == "__main__":
    main()
