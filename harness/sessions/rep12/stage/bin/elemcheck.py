"""G4(b)(i) mechanical check: does RASPA's auto-created pseudo atom for every
element in this database receive the PINNED UFF parameters?

The CIFs label atoms `Cu1`, `C3`; `RemoveAtomNumberCodeFromLabel yes` reduces
those to `Cu`, `C`, which do not match the pinned pseudo-atom names `Cu_`, `C_`.
RASPA silently creates new pseudo atoms from its own element table. This builds
a synthetic diagnostic framework holding one atom of every element the database
contains, runs it, and compares the printed `X - CH4_sp3` cross term against
Lorentz-Berthelot on the pinned mixing-rules file.

The diagnostic framework is a protocol probe, not a candidate structure; no
number from it enters the claim.

usage:  elemcheck.py build <elements...> <destdir>
        elemcheck.py check <outputfile>
"""
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mofcore as mc

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
UFFP = os.path.join(WS, "toolchain/raspa/share/raspa/forcefield/UFF/force_field_mixing_rules.def")

CIF_HEAD = """data_elemprobe
_cell_length_a       %(L).4f
_cell_length_b       %(L).4f
_cell_length_c       %(L).4f
_cell_angle_alpha    90
_cell_angle_beta     90
_cell_angle_gamma    90

_symmetry_space_group_name_H-M    "P 1"
_symmetry_Int_Tables_number       1

loop_
  _symmetry_equiv_pos_as_xyz
  'x, y, z'

loop_
  _atom_site_type_symbol
  _atom_site_label
  _atom_site_symmetry_multiplicity
  _atom_site_fract_x
  _atom_site_fract_y
  _atom_site_fract_z
  _atom_site_occupancy
  _atom_site_charge
"""

SIM = """SimulationType                MonteCarlo
NumberOfCycles                10
NumberOfInitializationCycles  0
PrintEvery                    10

Forcefield                    UFF
CutOffVDW                     12.8
ChargeMethod                  None

Framework                     0
FrameworkName                 elemprobe
UnitCells                     1 1 1
UseChargesFromCIFFile         no
RemoveAtomNumberCodeFromLabel yes

ExternalTemperature           298.0
ExternalPressure              100000

component 0 MoleculeName             methane
            MoleculeDefinition       TraPPE
            TranslationProbability   1.0
            SwapProbability          2.0
            CreateNumberOfMolecules  0
"""


def build(els, dest):
    n = len(els)
    k = int(math.ceil(n ** (1.0 / 3.0)))
    spacing = 9.0
    L = max(30.0, k * spacing)
    lines = [CIF_HEAD % dict(L=L)]
    for i, e in enumerate(els):
        ix, iy, iz = i % k, (i // k) % k, i // (k * k)
        f = [(ix + 0.5) * spacing / L, (iy + 0.5) * spacing / L,
             (iz + 0.5) * spacing / L]
        lines.append("%-3s %-8s 1.0  %.5f  %.5f  %.5f  1.0000 0.0\n"
                     % (e, e + "1", f[0], f[1], f[2]))
    if not os.path.isdir(dest):
        os.makedirs(dest)
    with open(os.path.join(dest, "elemprobe.cif"), "w") as f:
        f.write("".join(lines))
    with open(os.path.join(dest, "simulation.input"), "w") as f:
        f.write(SIM)
    print("built %d elements, L=%.1f" % (n, L))


PAIR = re.compile(r"^\s*(\S+)\s*-\s*(\S+)\s*\[LENNARD_JONES\]\s*p_0/k_B:\s*([\d.]+)\s*\[K\],\s*p_1:\s*([\d.]+)")


def check(path):
    uff = mc.load_uff(UFFP)
    epsC, sigC = mc.CH4_PARAMS
    got = {}
    with open(path) as f:
        for line in f:
            m = PAIR.match(line)
            if not m:
                continue
            a, b, e, s = m.group(1), m.group(2), float(m.group(3)), float(m.group(4))
            if a == "CH4_sp3":
                got[b] = (e, s)
            elif b == "CH4_sp3":
                got[a] = (e, s)
    rows = []
    for el, (eu, su) in sorted(uff.items()):
        if el not in got:
            continue
        e_ref = math.sqrt(eu * epsC)
        s_ref = 0.5 * (su + sigC)
        e_got, s_got = got[el]
        de = abs(e_got - e_ref) / max(e_ref, 1e-9)
        ds = abs(s_got - s_ref) / max(s_ref, 1e-9)
        ok = (de < 2e-4 and ds < 2e-4)
        rows.append((el, e_ref, e_got, s_ref, s_got, ok))
    bad = [r for r in rows if not r[5]]
    print("checked,%d,matching,%d,mismatched,%d" % (len(rows), len(rows) - len(bad), len(bad)))
    for r in bad:
        print("MISMATCH,%s,eps_pinned,%.5f,eps_used,%.5f,sig_pinned,%.5f,sig_used,%.5f" % r[:5])
    missing = [el for el in uff if el not in got]
    print("no_autopseudo_created,%s" % ("|".join(sorted(missing)) if missing else "none"))


if __name__ == "__main__":
    if sys.argv[1] == "build":
        build(sys.argv[2].split(","), sys.argv[3])
    else:
        check(sys.argv[2])
