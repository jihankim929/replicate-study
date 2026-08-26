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

    t = count(Path(os.path.expanduser(a.session_dir)))
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
