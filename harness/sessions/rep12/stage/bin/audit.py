"""Append gate events to AUDIT.jsonl in the schema of AUDIT_SCHEMA.md.

usage (single):  audit.py <structure_id> <gate> <stage> <apparent|-> <outcome>
                          <disposition> <log_ref> [criterion_json] [note]
usage (bulk):    audit.py --bulk <tsvfile>
   tsv columns: structure_id gate stage apparent outcome disposition log_ref
                criterion_json note
"""
import json, os, subprocess, sys, datetime

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
AUD = os.path.join(WS, "AUDIT.jsonl")


def head_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=WS).decode().strip()
    except Exception:
        return "uncommitted"


def mk(structure_id, gate, stage, apparent, outcome, disposition, log_ref,
      criterion=None, note=None, commit=None, ts=None):
    o = {
        "ts": ts or datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds"),
        "structure_id": structure_id,
        "gate": gate,
        "stage": stage,
        "apparent_value": None if apparent in (None, "-", "") else float(apparent),
        "audit_outcome": outcome,
        "disposition": disposition,
        "log_ref": log_ref,
        "commit": commit or head_commit(),
    }
    if criterion:
        o["criterion"] = criterion if isinstance(criterion, dict) else json.loads(criterion)
    if note:
        o["note"] = note
    return o


def main():
    if sys.argv[1] == "--bulk":
        c = head_commit()
        ts = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")
        n = 0
        with open(AUD, "a") as out:
            for line in open(sys.argv[2]):
                if not line.strip():
                    continue
                p = line.rstrip("\n").split("\t")
                while len(p) < 9:
                    p.append("")
                o = mk(p[0], p[1], p[2], p[3], p[4], p[5], p[6],
                       p[7] or None, p[8] or None, commit=c, ts=ts)
                out.write(json.dumps(o, sort_keys=True) + "\n")
                n += 1
        print("appended %d audit lines" % n)
    else:
        a = sys.argv[1:]
        while len(a) < 9:
            a.append(None)
        o = mk(*a[:9])
        with open(AUD, "a") as out:
            out.write(json.dumps(o, sort_keys=True) + "\n")
        print("appended 1")


if __name__ == "__main__":
    main()
