"""Build a RASPA GCMC job directory for one (structure, pressure).

usage: mkinput.py <cifname> <pressure_Pa> <ncycles> <ninit> <destdir> [grid]

Writes destdir/{<safe>.cif, simulation.input}.  The CIF is copied verbatim from
db/ under a bracket-free name (RASPA framework names cannot contain '[').  The
simulation.input reproduces the pinned protocol of charter s3 exactly:
UFF forcefield dir (truncated / tailcorrections no live in that file), 12.8 A
cutoff, ChargeMethod None, TraPPE united-atom methane, 298 K, rigid framework.
UnitCells is the smallest replication with all perpendicular widths >= 2*12.8 A.
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mofcore as mc

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
DB = os.path.join(WS, "db")

TEMPLATE = """SimulationType                MonteCarlo
NumberOfCycles                %(ncyc)d
NumberOfInitializationCycles  %(ninit)d
PrintEvery                    %(printevery)d

Forcefield                    UFF
CutOffVDW                     12.8
ChargeMethod                  None

Framework                     0
FrameworkName                 %(safe)s
UnitCells                     %(nx)d %(ny)d %(nz)d
UseChargesFromCIFFile         no
RemoveAtomNumberCodeFromLabel yes
%(gridblock)s
ExternalTemperature           298.0
ExternalPressure              %(press)s

component 0 MoleculeName             methane
            MoleculeDefinition       TraPPE
            TranslationProbability   1.0
            SwapProbability          2.0
            CreateNumberOfMolecules  0
"""

GRIDBLOCK = """NumberOfGrids                 1
GridTypes                     CH4_sp3
SpacingVDWGrid                %s
UseTabularGrid                yes
"""

MAKEGRID = """SimulationType                MakeGrid
Forcefield                    UFF
CutOffVDW                     12.8
ChargeMethod                  None

Framework                     0
FrameworkName                 %(safe)s
UnitCells                     %(nx)d %(ny)d %(nz)d
UseChargesFromCIFFile         no
RemoveAtomNumberCodeFromLabel yes

NumberOfGrids                 1
GridTypes                     CH4_sp3
SpacingVDWGrid                %(spc)s
"""


def safe_name(name):
    return name.replace("[", "_").replace("]", "_")


def build(cifname, press, ncyc, ninit, dest, grid=None):
    """`grid` is either a VDW grid spacing in A, or "seed:<n>" to set an
    explicit RASPA RandomSeed (used by the G6 reproduction pass), or None."""
    if cifname.endswith(".cif"):
        cifname = cifname[:-4]
    src = os.path.join(DB, cifname + ".cif")
    safe = safe_name(cifname)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    shutil.copyfile(src, os.path.join(dest, safe + ".cif"))
    cell, syms, fr = mc.parse_cif(src)
    M = mc.cell_matrix(cell)
    n, V, w = mc.supercell_counts(M)
    if not grid or grid == "-":
        gb = ""
    elif str(grid).startswith("seed:"):
        gb = "RandomSeed                    %s\n" % str(grid)[5:]
    else:
        gb = GRIDBLOCK % grid
    d = dict(ncyc=ncyc, ninit=ninit, printevery=max(1000, ncyc // 10),
             safe=safe, nx=n[0], ny=n[1], nz=n[2], gridblock=gb,
             press=("%g" % press))
    with open(os.path.join(dest, "simulation.input"), "w") as f:
        f.write(TEMPLATE % d)
    if gb.startswith("NumberOfGrids"):
        with open(os.path.join(dest, "makegrid.input"), "w") as f:
            f.write(MAKEGRID % dict(safe=safe, nx=n[0], ny=n[1], nz=n[2],
                                    spc=grid))
    return safe, tuple(int(x) for x in n)


if __name__ == "__main__":
    a = sys.argv[1:]
    grid = a[5] if len(a) > 5 else None
    s, n = build(a[0], float(a[1]), int(a[2]), int(a[3]), a[4], grid)
    print("%s %d %d %d" % (s, n[0], n[1], n[2]))
