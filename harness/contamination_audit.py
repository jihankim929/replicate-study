#!/usr/bin/env python3
"""READ-ONLY audit of what crossed between replicates through the agent host's shared /tmp.

WHY. All sixteen sessions run as one user on one machine, so /tmp is shared between them. On
2026-08-30 rep01 reported that a sibling's REPORT.md overwrote its own at the same path AND was
surfaced into its session; rep03 reported that STATE.md in its workspace contained rep09's. Both
were verified from the harness end: /tmp/REPORT.md and /tmp/STATE.md exist unprefixed and both
are rep09's. REPORT 007 section 7(1); this audit ordered by the PI 2026-08-31.

WHAT IT DOES. For every replicate, over every transcript it has on this host, it finds every
reference to a /tmp path and classifies it:

    own          the path is namespaced to the replicate that touched it
    foreign      the path is namespaced to a DIFFERENT replicate -- an unambiguous crossing
    unprefixed   the path is in the shared namespace, where a crossing is possible and silent

and records the direction (read / write / ambiguous), the tool, and the timestamp.

WHAT IT DOES NOT DO. It changes nothing, it deletes nothing, and it does not decide anything
about scoring. Exposure is a fact to be recorded and disclosed; what follows from it is the
analysis plan's business and the PI's.

    ./harness/contamination_audit.py                     # writes the incident record
    ./harness/contamination_audit.py --print             # and prints the summary
"""
import json, glob, os, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "harness" / "state" / "incident_20260831_tmp_collision"
REPS = [f"rep{i:02d}" for i in list(range(1, 14)) + [15, 16, 17]]

TMP_PATH = re.compile(r"/tmp/[A-Za-z0-9._\-/]+")
REP_TAG = re.compile(r"\brep(\d{2})\b")
# Bash commands that read a path vs write one. Deliberately crude and deliberately conservative:
# an ambiguous command is reported as ambiguous rather than guessed into either column.
READS = re.compile(r"\b(cat|head|tail|less|more|grep|diff|wc|md5sum|sha\d*sum|cp|python3?|open)\b")
WRITES = re.compile(r"(>\s*/tmp/|>>\s*/tmp/|\b(tee|mv|cp)\b.*\s/tmp/)")


def session_dir(rep):
    cwd = ROOT / "harness" / "sessions" / rep
    return Path.home() / ".claude" / "projects" / str(cwd).replace("/", "-")


def classify(path, rep):
    """own | foreign:<repNN> | unprefixed"""
    tail = path[len("/tmp/"):]
    m = REP_TAG.match(tail) or re.match(r"rep(\d{2})", tail)
    if m:
        other = f"rep{m.group(1)}"
        return "own" if other == rep else f"foreign:{other}"
    return "unprefixed"


def scan(rep):
    d = session_dir(rep)
    events = []
    for f in sorted(glob.glob(str(d / "*.jsonl"))):
        for line in open(f, errors="replace"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            ts = r.get("timestamp", "")
            if r.get("type") != "assistant":
                continue
            for c in r.get("message", {}).get("content", []):
                if c.get("type") != "tool_use":
                    continue
                tool = c.get("name", "?")
                inp = c.get("input") or {}
                if not isinstance(inp, dict):
                    inp = {}
                # THE PATH MUST COME FROM THE ARGUMENT, NOT FROM THE PAYLOAD. Scanning the whole
                # input blob counts a /tmp path that merely APPEARS IN FILE CONTENT as a touch of
                # that file -- and agents write about their own paths constantly. The first run of
                # this audit did that and reported rep01 writing /tmp/REPORT.md twice at times
                # when the file on disk demonstrably did not change. Only file_path (for the file
                # tools) and command (for Bash) say what was actually touched.
                if tool in ("Read", "Write", "Edit", "NotebookEdit"):
                    src = str(inp.get("file_path") or "")
                    direction = "read" if tool == "Read" else "write"
                elif tool in ("Glob", "Grep"):
                    src = str(inp.get("path") or "")
                    direction = "read"
                elif tool == "Bash":
                    src = str(inp.get("command") or "")
                    w, rd = bool(WRITES.search(src)), bool(READS.search(src))
                    direction = "write" if w and not rd else "read" if rd and not w else "ambiguous"
                else:
                    src = ""
                    direction = "ambiguous"
                paths = {q.rstrip(".,'\")") for q in TMP_PATH.findall(src)}
                for p in paths:
                    events.append({"ts": ts, "tool": tool, "path": p,
                                   "class": classify(p, rep), "direction": direction})
    return events


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    per_rep, summary = {}, []
    for rep in REPS:
        ev = scan(rep)
        per_rep[rep] = ev
        foreign = [e for e in ev if e["class"].startswith("foreign")]
        unpre = [e for e in ev if e["class"] == "unprefixed"]
        foreign_read = [e for e in foreign if e["direction"] in ("read", "ambiguous")]
        unpre_read = [e for e in unpre if e["direction"] in ("read", "ambiguous")]
        others = sorted({e["class"].split(":")[1] for e in foreign})
        summary.append({
            "replicate": rep, "tmp_events": len(ev),
            "own": sum(1 for e in ev if e["class"] == "own"),
            "unprefixed": len(unpre), "unprefixed_read_or_ambiguous": len(unpre_read),
            "foreign": len(foreign), "foreign_read_or_ambiguous": len(foreign_read),
            "foreign_replicates_touched": others,
            "first_tmp_use": min((e["ts"] for e in ev), default=None),
            "last_tmp_use": max((e["ts"] for e in ev), default=None),
        })

    (OUT / "tmp_events_per_replicate.json").write_text(json.dumps(per_rep, indent=1))
    (OUT / "tmp_audit_summary.json").write_text(json.dumps(summary, indent=1))

    # --- THE CROSSING ITSELF ------------------------------------------------------------
    # The per-replicate columns above are the exposure SURFACE. A crossing is narrower and has to
    # be argued from the order of events, so three classes are separated rather than merged:
    #
    #   A  READ WITHOUT OWN WRITE. R read a shared path it never wrote, and someone else had
    #      written it earlier. Whatever R read was another replicate's.
    #
    #   B  INTERLEAVED OVERWRITE. R wrote the path, ANOTHER replicate wrote it afterwards, and
    #      then R read it back. R believed it was reading its own file and was not. This is the
    #      shape rep01 described -- "a sibling's REPORT.md overwrote mine at the same path and
    #      was surfaced into my session" -- and class A structurally cannot see it, because R is
    #      a writer of that path. It is the most consequential class and the least visible.
    #
    #   C  SHARED PATH. More than one replicate touched it. Not evidence of a crossing on its
    #      own; it is the surface on which A and B become possible.
    #
    # A Bash command that neither clearly reads nor clearly writes is "ambiguous", and ambiguity
    # is always resolved AGAINST claiming a crossing: an ambiguous event counts as a possible
    # write when that would EXCUSE a replicate from class A, and does not count as a write when
    # claiming one in class B.
    touch = defaultdict(lambda: defaultdict(list))
    for rep, ev in per_rep.items():
        for e in ev:
            if e["class"] == "unprefixed":
                touch[e["path"]][rep].append(e)

    def wrote_definitely(es):  return [e for e in es if e["direction"] == "write"]
    def wrote_possibly(es):    return [e for e in es if e["direction"] in ("write", "ambiguous")]
    def read_events(es):       return [e for e in es if e["direction"] in ("read", "ambiguous")]

    collisions, class_a, class_b = [], [], []
    for path, reps in sorted(touch.items()):
        first = min(e["ts"] for es in reps.values() for e in es)
        last = max(e["ts"] for es in reps.values() for e in es)
        collisions.append({"path": path, "replicates": sorted(reps),
                           "first_touch": first, "last_touch": last,
                           "events": {r: len(es) for r, es in reps.items()}})
        if len(reps) < 2:
            continue
        for r, es in reps.items():
            others_def = sorted({o for o, oes in reps.items() if o != r and wrote_definitely(oes)})
            if not others_def:
                continue
            # A: r read it and never even possibly wrote it
            if read_events(es) and not wrote_possibly(es):
                first_read = min(e["ts"] for e in read_events(es))
                prior = sorted({o for o in others_def
                                if min(e["ts"] for e in wrote_definitely(reps[o])) < first_read})
                if prior:
                    class_a.append({"path": path, "replicate": r, "read_at": first_read,
                                    "written_earlier_by": prior})
            # B: r wrote, another definitely wrote later, r read after that
            for w in wrote_definitely(es):
                for o in others_def:
                    for ow in wrote_definitely(reps[o]):
                        if not (w["ts"] < ow["ts"]):
                            continue
                        after = [e for e in read_events(es) if e["ts"] > ow["ts"]]
                        if after:
                            class_b.append({"path": path, "replicate": r,
                                            "own_write": w["ts"],
                                            "overwritten_by": o, "overwritten_at": ow["ts"],
                                            "read_back_at": min(e["ts"] for e in after)})
    # de-duplicate class B to one row per (path, replicate, overwriter)
    seen, dedup = set(), []
    for b in sorted(class_b, key=lambda x: x["read_back_at"]):
        k = (b["path"], b["replicate"], b["overwritten_by"])
        if k not in seen:
            seen.add(k); dedup.append(b)
    class_b = dedup

    exposed = defaultdict(set)
    for a in class_a:
        exposed[a["replicate"]].update(a["written_earlier_by"])
    for b in class_b:
        exposed[b["replicate"]].add(b["overwritten_by"])

    (OUT / "tmp_collisions.json").write_text(json.dumps(collisions, indent=1))
    (OUT / "crossings_classA_read_without_own_write.json").write_text(json.dumps(class_a, indent=1))
    (OUT / "crossings_classB_interleaved_overwrite.json").write_text(json.dumps(class_b, indent=1))
    (OUT / "contamination_exposed.json").write_text(json.dumps(
        {r: sorted(v) for r, v in sorted(exposed.items())}, indent=1))

    lines = [f"{'rep':7} {'/tmp uses':>9} {'own':>5} {'unpref':>7} {'unpref r/a':>11} "
             f"{'foreign':>8} {'foreign r/a':>12}  touched"]
    for s in summary:
        lines.append(f"{s['replicate']:7} {s['tmp_events']:9} {s['own']:5} {s['unprefixed']:7} "
                     f"{s['unprefixed_read_or_ambiguous']:11} {s['foreign']:8} "
                     f"{s['foreign_read_or_ambiguous']:12}  {' '.join(s['foreign_replicates_touched']) or '-'}")
    shared = [c for c in collisions if len(c["replicates"]) > 1]
    lines += ["", f"C. SHARED-NAMESPACE PATHS TOUCHED BY MORE THAN ONE REPLICATE: {len(shared)}"]
    for c in shared:
        lines.append(f"  {c['path']:32} {' '.join(c['replicates'])}"
                     f"   {c['first_touch'][:19]} .. {c['last_touch'][:19]}")
    lines += ["", f"A. READ WITHOUT OWN WRITE ({len(class_a)}) -- read a shared path it never wrote,"
                  " written earlier by another"]
    for a_ in class_a:
        lines.append(f"  {a_['replicate']} read {a_['path']} at {a_['read_at'][:19]}"
                     f"   written earlier by: {' '.join(a_['written_earlier_by'])}")
    lines += ["", f"B. INTERLEAVED OVERWRITE ({len(class_b)}) -- wrote it, another overwrote it,"
                  " then read it back"]
    for b_ in class_b:
        lines.append(f"  {b_['replicate']} wrote {b_['path']} at {b_['own_write'][:19]};"
                     f" {b_['overwritten_by']} overwrote at {b_['overwritten_at'][:19]};"
                     f" {b_['replicate']} read back at {b_['read_back_at'][:19]}")
    lines += ["", "CONTAMINATION-EXPOSED (evidenced from transcripts, classes A and B):"]
    if exposed:
        for r, ws in sorted(exposed.items()):
            lines.append(f"  {r}  <- {' '.join(sorted(ws))}")
    else:
        lines.append("  none evidenced from transcripts alone")
    text = "\n".join(lines)
    (OUT / "tmp_audit_summary.txt").write_text(text + "\n")
    if "--print" in sys.argv:
        print(text)


if __name__ == "__main__":
    main()
