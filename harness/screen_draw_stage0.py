#!/usr/bin/env python3
"""Draw and seal Stage 0's calibration sample before the screen can run.

STRATIFICATION CONFLICT, RESOLVED EXPLICITLY. The sealed plan stratifies Stage 0 "by floor-value
decile" -- and floor values do not exist until Stage 1 has run. Drawing the list this week, as
ordered, means stratifying on something computable from the frozen manifest alone. This uses
DENSITY DECILE, which is the strongest pre-computable proxy for capacity in this database, and
pre-registers a top-up rule so the plan's intent survives contact with the real floor values:

    After Stage 1 completes, the realized FLOOR-VALUE decile coverage of this sample is reported.
    Any floor decile holding fewer than 10 of the 300 receives a top-up draw from that decile,
    using the same seed stream continued, until it holds 10. Top-ups are reported separately and
    never replace a drawn structure.

The seed is derived from the frozen manifest's own SHA-256, so the draw is reproducible by anyone
holding the manifest and could not have been chosen after seeing an outcome.
"""
import hashlib, json, random, sys
from pathlib import Path

MANIFEST_SHA = "4777fc4f5b7647d0e129f75978833698d3546d01d0b79d427b5d1ee28cd1a520"
N_TOTAL, N_DECILE = 300, 30
N_FINE = 25


def main():
    meta = json.load(open("screen/screen_meta_12499.json"))
    stems = sorted(k for k, v in meta.items() if "error" not in v)
    assert len(stems) == 12499, f"expected 12,499, got {len(stems)}"
    seed = int(MANIFEST_SHA[:16], 16)
    rng = random.Random(seed)

    ordered = sorted(stems, key=lambda s: meta[s]["density"])
    n = len(ordered)
    deciles = [ordered[round(i * n / 10):round((i + 1) * n / 10)] for i in range(10)]

    sample, per = [], {}
    for i, d in enumerate(deciles):
        pick = rng.sample(d, N_DECILE)
        per[i] = sorted(pick)
        sample += pick
    sample = sorted(sample)
    assert len(sample) == N_TOTAL and len(set(sample)) == N_TOTAL

    # the 25 fine-checkpoint structures are a SUBSET of Stage 0, not an addition:
    # PrintEvery=1,000 instead of 10,000, same cycles, same cost.
    fine = sorted(rng.sample(sample, N_FINE))

    out = {"seed_source": "sha256 of frozen/MANIFEST.sha256, first 16 hex digits",
           "manifest_sha256": MANIFEST_SHA, "seed": seed,
           "stratification": "density decile (pre-computable proxy for floor value)",
           "n_total": N_TOTAL, "per_decile": N_DECILE,
           "decile_bounds": [round(meta[d[0]]["density"], 4) for d in deciles] +
                            [round(meta[deciles[-1][-1]]["density"], 4)],
           "sample": sample, "by_decile": per,
           "fine_checkpoint_subset": fine,
           "fine_print_every": 1000,
           "topup_rule": ("after Stage 1, any FLOOR-VALUE decile holding <10 of the 300 receives a "
                          "top-up draw from that decile on the same seed stream until it holds 10; "
                          "top-ups are reported separately and never replace a drawn structure")}
    Path("prereg/stage0_sample.SEALED.json").write_text(json.dumps(out, indent=2) + "\n")
    body = json.dumps(out, sort_keys=True).encode()
    print(f"  drawn {len(sample)} structures, 30 per density decile")
    print(f"  fine-checkpoint subset: {len(fine)} (PrintEvery 1,000)")
    print(f"  density range covered: {out['decile_bounds'][0]} - {out['decile_bounds'][-1]} g/cm3")
    print(f"  sample sha256: {hashlib.sha256(body).hexdigest()}")


if __name__ == "__main__":
    main()
