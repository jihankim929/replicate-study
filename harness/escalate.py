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
        rec = {"ts": stamp, "replicate": meta["replicate_id"], "phase": meta["phase"],
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

    print(f"[escalate] {meta['replicate_id']}: {len(results)} new escalation(s)")
    for r in results:
        print(f"    {r['category']:<11} -> {r['disposition']:<18} {r['question'][:60]}")
    queued = [r for r in results if r["reply"] is None and r["valid"]]
    if queued:
        print(f"    !! {len(queued)} awaiting a human action (repair or PI ruling)")
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    process(a.workspace, a.dry_run)
