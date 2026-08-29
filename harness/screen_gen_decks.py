#!/usr/bin/env python3
"""Pre-generate every RASPA input deck the reference screen will submit.

Generated this week so the screen's first wave can submit inside the hour after the final
collection, and generated LOCALLY from the frozen manifest's metadata so nothing touches the
cluster before the last bell.

The template is transcribed VERBATIM from an archived claim-grade deck
(`reps/smoke/s01/runs/s3/.../simulation.input`) rather than written fresh, so the screen runs the
same protocol the campaign ran. The only fields that vary are the ones that must: framework name,
unit cells, pressure, cycle counts and PrintEvery.

UnitCells come from the frozen metadata pass: the minimum replication making every perpendicular
box width at least 2 x the 12.8 A cutoff. That is the condition whose violation RASPA reports as
"Cutoff smaller than half of one of the perpendicular boxlengths" -- and then exits 0.
"""
import hashlib, json, os, sys
from pathlib import Path

TEMPLATE = """SimulationType                MonteCarlo
NumberOfCycles                {cycles}
NumberOfInitializationCycles  {init}
PrintEvery                    {print_every}
RestartFile                   no
Movies                        no
WriteBinaryRestartFileEvery   0

Forcefield                    UFF
CutOff                        12.8
ChargeMethod                  None
UseChargesFromCIFFile         no
RemoveAtomNumberCodeFromLabel no

Framework 0
FrameworkName                 {stem}
UnitCells                     {nx} {ny} {nz}
HeliumVoidFraction            1.0
ExternalTemperature           298.0
ExternalPressure              {pressure}

Component 0 MoleculeName                methane
            MoleculeDefinition          TraPPE
            TranslationProbability      1.0
            ReinsertionProbability      1.0
            SwapProbability             2.0
            CreateNumberOfMolecules     0
"""

PRESSURES = {"p05": "580000.0", "p65": "6500000.0"}
FLOOR = {"cycles": 10000, "init": 2000, "print_every": 2000}
CLAIM = {"cycles": 50000, "init": 10000, "print_every": 10000}


def write(root, stage, stem, pc, tier, meta, seed_tag="", print_every=None):
    nx, ny, nz = meta["cells"]
    body = TEMPLATE.format(stem=stem, nx=nx, ny=ny, nz=nz, pressure=PRESSURES[pc],
                           cycles=tier["cycles"], init=tier["init"],
                           print_every=print_every or tier["print_every"])
    d = Path(root) / stage / stem / (pc + seed_tag)
    d.mkdir(parents=True, exist_ok=True)
    (d / "simulation.input").write_text(body)
    return hashlib.sha256(body.encode()).hexdigest()


def main():
    meta = json.load(open("screen/screen_meta_12499.json"))
    s0 = json.load(open("prereg/stage0_sample.SEALED.json"))
    fine = set(s0["fine_checkpoint_subset"])
    root = "screen/decks"
    led = []

    for stem, m in sorted(meta.items()):
        if "error" in m:
            continue
        for pc in PRESSURES:
            led.append(("stage1", stem, pc, "", write(root, "stage1", stem, pc, FLOOR, m)))

    for stem in s0["sample"]:
        m = meta[stem]
        pe = s0["fine_print_every"] if stem in fine else None
        for pc in PRESSURES:
            led.append(("stage0", stem, pc, "", write(root, "stage0", stem, pc, CLAIM, m, "", pe)))

    Path("screen").mkdir(exist_ok=True)
    with open("screen/deck_manifest.sha256", "w") as f:
        for stage, stem, pc, tag, h in led:
            f.write(f"{h}  {stage}/{stem}/{pc}{tag}/simulation.input\n")
    agg = hashlib.sha256("".join(h for *_, h in led).encode()).hexdigest()
    print(f"  decks written : {len(led):,}")
    print(f"    stage1 (floor, 12,499 x 2 pressures) : {sum(1 for r in led if r[0]=='stage1'):,}")
    print(f"    stage0 (claim, 300 x 2 pressures)    : {sum(1 for r in led if r[0]=='stage0'):,}")
    print(f"    of which fine-checkpoint (PrintEvery 1,000): {len(fine)*2}")
    print(f"  aggregate deck sha256: {agg}")


if __name__ == "__main__":
    main()
