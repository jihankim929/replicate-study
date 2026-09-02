#!/usr/bin/env python3
"""Generate the claim-grade decks the Figure-4 tail needs and the sealed screen never built.

WHY THIS EXISTS. `screen/decks/stage0` holds exactly the 300 pre-registered calibration structures
(600 decks). The Figure-4 agent tail is 572 structures and only 11 of them are among those 300, so
561 structures - 1,122 decks - have no claim-grade deck anywhere. Step (3)'s two remaining claims
have none either, which is 2 more structures and 4 more decks. Reported as REPORT 045's blocker on
segment (2a); built here under the PI's order of 2026-09-03.

THE CONSTRUCTION IS NOT REIMPLEMENTED. This module IMPORTS `screen_gen_decks` and calls its own
TEMPLATE, PRESSURES, CLAIM tier and `write()`. Transcribing them would create a second copy that can
drift silently; importing makes drift impossible. If the sealed generator changes, this changes with
it or fails loudly.

WHERE THEY GO, AND WHY NOT INTO stage0. `screen/decks/stage0` is a SEALED tree: it is what
`deck_manifest.sha256` covers and what section 7.1's gate counts as 25,598/25,598. Writing 1,126 new
decks into it would break that count and retroactively change what the seal describes. So the new
decks go to a NEW stage, `stage2`, with its OWN manifest `screen/fig4_deck_manifest.sha256`. The
sealed tree and the sealed manifest are not touched, read-only, and still verify at 25,598.
The 11 agent-tail structures that ARE in stage0 are NOT regenerated - the sealed deck is used.

HOW THE HASH RULE IS VERIFIED RATHER THAN ASSERTED. Those same 11 structures are regenerated in
memory through this exact code path and their hashes compared against the sealed
`deck_manifest.sha256` entries. If this file's construction differs from stage0's in any byte, those
22 hashes disagree and the build refuses. That is a measurement of the rule, not a claim about it.
"""
import hashlib, json, sys, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
import screen_gen_decks as sealed          # the sealed construction, imported not copied

STAGE = "stage2"
DECKS = ROOT / "screen/decks"
MANIFEST = ROOT / "screen/fig4_deck_manifest.sha256"
SEALED_MANIFEST = ROOT / "screen/deck_manifest.sha256"


def sealed_hashes():
    h = {}
    for line in SEALED_MANIFEST.read_text().splitlines():
        d, rel = line.split("  ", 1)
        h[rel] = d
    return h


def needed():
    """The claim-grade structures the fig4 queue asks for, in queue order, that stage0 lacks."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("f4", ROOT / "harness/fig4_submit.py")
    f4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f4)
    meta = json.loads((ROOT / "screen/screen_meta_12499.json").read_text())
    q = f4.load_queue(meta)
    have = {p.name for p in (DECKS / "stage0").iterdir() if p.is_dir()}
    miss, present = [], []
    for r in q:
        if r["grade"] != "claim":
            continue
        (present if r["structure_id"] in have else miss).append((r["structure_id"], r["segment"]))
    return miss, present, meta


def main():
    miss, present, meta = needed()
    s0 = json.loads((ROOT / "prereg/stage0_sample.SEALED.json").read_text())
    fine = set(s0["fine_checkpoint_subset"])
    sh = sealed_hashes()

    # -- verification first: the 11 stage0-resident claim structures, rebuilt through THIS path --
    tmp = Path(tempfile.mkdtemp())
    bad = []
    for stem, _ in present:
        pe = s0["fine_print_every"] if stem in fine else None
        for pc in sealed.PRESSURES:
            got = sealed.write(tmp, "stage0", stem, pc, sealed.CLAIM, meta[stem], "", pe)
            want = sh.get(f"stage0/{stem}/{pc}/simulation.input")
            if got != want:
                bad.append((stem, pc, got, want))
    shutil.rmtree(tmp)
    print(f"hash-rule check: {len(present)*2} decks rebuilt through this path vs sealed manifest -> "
          f"{'ALL MATCH' if not bad else str(len(bad)) + ' MISMATCH'}")
    if bad:
        for b in bad[:5]:
            print("  MISMATCH", b)
        print("REFUSING to build: this path does not reproduce the sealed construction.")
        return 2

    # -- none of the new structures may be in the sealed fine-checkpoint subset --
    overlap = [s for s, _ in miss if s in fine]
    if overlap:
        print(f"REFUSING: {len(overlap)} new structures are in fine_checkpoint_subset: {overlap[:5]}")
        return 3

    # -- build --
    led, by_seg = [], {}
    for stem, seg in miss:
        by_seg[seg] = by_seg.get(seg, 0) + 1
        for pc in sealed.PRESSURES:
            h = sealed.write(DECKS, STAGE, stem, pc, sealed.CLAIM, meta[stem])
            led.append((stem, pc, h))
    with open(MANIFEST, "w") as f:
        for stem, pc, h in led:
            f.write(f"{h}  {STAGE}/{stem}/{pc}/simulation.input\n")
    agg = hashlib.sha256("".join(h for *_, h in led).encode()).hexdigest()
    print(f"  structures : {len(miss):,}  ({', '.join(f'{k} {v}' for k, v in by_seg.items())})")
    print(f"  decks      : {len(led):,}  -> screen/decks/{STAGE}/")
    print(f"  manifest   : {MANIFEST.relative_to(ROOT)}")
    print(f"  aggregate sha256: {agg}")
    print(f"  sealed tree untouched: stage0={len(list((DECKS/'stage0').iterdir())):,} "
          f"stage1={len(list((DECKS/'stage1').iterdir())):,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
