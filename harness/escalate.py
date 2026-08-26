#!/usr/bin/env python3
"""(c) Escalation router — implements the charter section 8 table, verbatim.

Charter section 8, transcribed:

    Escalations must be filed in the fixed format [ESC: category / one-line question].
    Categories: `infra` (mechanical failures -- will be repaired), `charter` (rule
    clarification -- answered from this document), `scientific` (will receive: "Proceed per
    your own judgment within the charter; log the ambiguity."). There is no other channel;
    plan accordingly.

THE ROUTER HOLDS NO DISCRETION. Exactly one category has a chartered reply text, and that is
the only category it answers. The other two are QUEUED, because:

  * `infra` promises a repair. A repair is an action, not a sentence. Auto-replying "will be
    repaired" while nothing is repaired would be a false statement by the harness.
  * `charter` promises an answer "from this document". Deciding WHICH clause answers a given
    question is interpretation, and interpretation is not Bei's to perform -- Bei is a
    harness, not a supervisor. Queued for the PI.

A malformed escalation gets the format back, not a guess at what was meant.
"""
import argparse, json, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as C

KST = timezone(timedelta(hours=9))
ESC_RE = re.compile(r"\[ESC:\s*([A-Za-z]+)\s*/\s*(.+?)\s*\]", re.S)
LEDGER = Path(__file__).parent / "escalations.jsonl"
QUEUE = Path(__file__).parent / "escalation_queue.jsonl"

MALFORMED_REPLY = (
    "Malformed escalation. The fixed format is `[ESC: category / one-line question]` and the "
    "categories are `infra`, `charter`, `scientific` (charter section 8). Re-file in that "
    "format. There is no other channel."
)


def parse(text: str):
    return [(m.group(1).lower(), " ".join(m.group(2).split()), m.group(0))
            for m in ESC_RE.finditer(text)]


def route(category: str, question: str) -> dict:
    """The whole of Bei's authority over escalations is this function."""
    if category not in C.ESC_TABLE:
        return {"category": category, "valid": False, "disposition": "malformed",
                "reply": MALFORMED_REPLY, "charter_text": None}
    row = C.ESC_TABLE[category]
    return {"category": category, "valid": True,
            "disposition": row["disposition"],
            "reply": row["auto_reply"],
            "charter_text": row["charter_text"]}


def process(ws_path, dry_run=False):
    ws = Path(ws_path).resolve()
    meta = json.loads((ws / "WORKSPACE.json").read_text())
    esc_file = ws / "ESCALATIONS.md"
    seen_file = Path(__file__).parent / f".seen-{meta['replicate_id']}"
    seen = set(seen_file.read_text().splitlines()) if seen_file.exists() else set()

    results = []
    for cat, q, raw in parse(esc_file.read_text() if esc_file.exists() else ""):
        key = f"{cat}|{q}"
        if key in seen:
            continue
        r = route(cat, q)
        stamp = datetime.now(KST).isoformat()
        # queued_at is stamped at ENTRY, so response latency is on the record whether or not
        # anyone answers promptly. PI ruling 2026-08-26: queued items are answered at
        # approximately 09:00 and 21:00 KST daily during the smoke.
        rec = {"ts": stamp, "queued_at": stamp if r["reply"] is None else None,
               "answered_at": stamp if r["reply"] is not None else None,
               "latency_h": 0.0 if r["reply"] is not None else None,
               "replicate": meta["replicate_id"], "phase": meta["phase"],
               "raw": raw, "question": q, **r}
        results.append(rec)
        seen.add(key)

        if r["reply"] is not None:
            block = (f"\n## {stamp} — escalation response\n\n"
                     f"> {raw}\n\n{r['reply']}\n")
        else:
            block = (f"\n## {stamp} — escalation received\n\n"
                     f"> {raw}\n\n"
                     f"Category `{cat}`: {r['charter_text']} (charter section 8).\n"
                     f"**Queued.** No response should be assumed pending; continue working.\n")
        if dry_run:
            print(f"[escalate] (dry-run) {cat} -> {r['disposition']}")
            print("    " + block.strip().replace("\n", "\n    "))
        else:
            with open(ws / "INBOX.md", "a") as fh:
                fh.write(block)

    if not dry_run:
        seen_file.write_text("\n".join(sorted(seen)) + "\n")
        with open(LEDGER, "a") as fh:
            for rec in results:
                fh.write(json.dumps(rec) + "\n")
        with open(QUEUE, "a") as fh:
            for rec in results:
                if rec["reply"] is None and rec["valid"]:
                    fh.write(json.dumps(rec) + "\n")

    print(f"[escalate] {meta['replicate_id']}: {len(results)} new escalation(s)")
    for r in results:
        print(f"    {r['category']:<11} -> {r['disposition']:<18} {r['question'][:60]}")
    queued = [r for r in results if r["reply"] is None and r["valid"]]
    if queued:
        print(f"    !! {len(queued)} awaiting a human action (repair or PI ruling)")
    return results


def answer(ws_path, question_substr, text, dry_run=False):
    """Deliver a human-authored answer to a QUEUED escalation and close out its latency.

    Bei does not author these. It transports them and records how long they took.
    """
    ws = Path(ws_path).resolve()
    meta = json.loads((ws / "WORKSPACE.json").read_text())
    pending = [json.loads(l) for l in QUEUE.read_text().splitlines()] if QUEUE.exists() else []
    hits = [r for r in pending
            if r["replicate"] == meta["replicate_id"] and question_substr.lower() in r["question"].lower()]
    if not hits:
        raise SystemExit(f"no queued escalation for {meta['replicate_id']} matching {question_substr!r}")
    rec = hits[-1]
    now = datetime.now(KST)
    latency = (now - datetime.fromisoformat(rec["queued_at"])).total_seconds() / 3600
    block = (f"\n## {now.isoformat()} — escalation response\n\n"
             f"> {rec['raw']}\n\n{text}\n")
    out = {**rec, "answered_at": now.isoformat(), "latency_h": round(latency, 2),
           "reply": text, "disposition": "answered"}
    if dry_run:
        print(f"[escalate] (dry-run) would answer {rec['category']} after {latency:.2f} h")
        print("    " + block.strip().replace("\n", "\n    "))
    else:
        with open(ws / "INBOX.md", "a") as fh:
            fh.write(block)
        with open(LEDGER, "a") as fh:
            fh.write(json.dumps(out) + "\n")
        remaining = [r for r in pending if r is not rec]
        QUEUE.write_text("".join(json.dumps(r) + "\n" for r in remaining))
    print(f"[escalate] answered {rec['category']} for {meta['replicate_id']}; "
          f"latency {latency:.2f} h")
    return out


def show_queue():
    pending = [json.loads(l) for l in QUEUE.read_text().splitlines()] if QUEUE.exists() else []
    now = datetime.now(KST)
    print(f"[escalate] {len(pending)} awaiting a human answer "
          f"(cadence: {', '.join(C.RATIFIED['escalation_answer_times_kst'])} KST)")
    for r in pending:
        age = (now - datetime.fromisoformat(r["queued_at"])).total_seconds() / 3600
        print(f"    {r['replicate']:<5} {r['category']:<9} waiting {age:6.2f} h  {r['question'][:56]}")
    return pending


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", nargs="?")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--queue", action="store_true", help="list escalations awaiting a human answer")
    ap.add_argument("--answer", metavar="SUBSTR", help="deliver an answer to a queued escalation")
    ap.add_argument("--text", help="the answer text (required with --answer)")
    a = ap.parse_args()
    if a.queue:
        show_queue()
    elif a.answer:
        if not (a.workspace and a.text):
            ap.error("--answer needs a workspace and --text")
        answer(a.workspace, a.answer, a.text, a.dry_run)
    else:
        if not a.workspace:
            ap.error("workspace is required")
        process(a.workspace, a.dry_run)
