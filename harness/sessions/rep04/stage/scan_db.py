#!/usr/bin/env python3
"""Single pass over db/*.cif -> compact manifest CSV.

Extracts only cheap, exact quantities: cell parameters, volume, atom count,
element composition, framework mass, crystal density, and the perpendicular
cell widths needed to choose RASPA UnitCells at a 12.8 A cutoff.

Writes: manifest/structures.csv  (one row per structure)
        manifest/elements.txt    (element -> count of structures containing it)
Nothing large is ever printed; stdout is a few summary lines.
"""
import os, sys, math, csv, collections

DB = sys.argv[1] if len(sys.argv) > 1 else "db"
OUT = sys.argv[2] if len(sys.argv) > 2 else "manifest"

# IUPAC standard atomic weights, enough to cover any MOF element.
MASS = {
 'H':1.008,'He':4.0026,'Li':6.94,'Be':9.0122,'B':10.81,'C':12.011,'N':14.007,
 'O':15.999,'F':18.998,'Ne':20.180,'Na':22.990,'Mg':24.305,'Al':26.982,
 'Si':28.085,'P':30.974,'S':32.06,'Cl':35.45,'Ar':39.948,'K':39.098,
 'Ca':40.078,'Sc':44.956,'Ti':47.867,'V':50.942,'Cr':51.996,'Mn':54.938,
 'Fe':55.845,'Co':58.933,'Ni':58.693,'Cu':63.546,'Zn':65.38,'Ga':69.723,
 'Ge':72.630,'As':74.922,'Se':78.971,'Br':79.904,'Kr':83.798,'Rb':85.468,
 'Sr':87.62,'Y':88.906,'Zr':91.224,'Nb':92.906,'Mo':95.95,'Tc':98.0,
 'Ru':101.07,'Rh':102.91,'Pd':106.42,'Ag':107.87,'Cd':112.41,'In':114.82,
 'Sn':118.71,'Sb':121.76,'Te':127.60,'I':126.90,'Xe':131.29,'Cs':132.91,
 'Ba':137.33,'La':138.91,'Ce':140.12,'Pr':140.91,'Nd':144.24,'Pm':145.0,
 'Sm':150.36,'Eu':151.96,'Gd':157.25,'Tb':158.93,'Dy':162.50,'Ho':164.93,
 'Er':167.26,'Tm':168.93,'Yb':173.05,'Lu':174.97,'Hf':178.49,'Ta':180.95,
 'W':183.84,'Re':186.21,'Os':190.23,'Ir':192.22,'Pt':195.08,'Au':196.97,
 'Hg':200.59,'Tl':204.38,'Pb':207.2,'Bi':208.98,'Po':209.0,'At':210.0,
 'Rn':222.0,'Fr':223.0,'Ra':226.0,'Ac':227.0,'Th':232.04,'Pa':231.04,
 'U':238.03,'Np':237.0,'Pu':244.0,'Am':243.0,'Cm':247.0,
}


def cell_volume(a, b, c, al, be, ga):
    ra, rb, rg = math.radians(al), math.radians(be), math.radians(ga)
    ca, cb, cg = math.cos(ra), math.cos(rb), math.cos(rg)
    t = 1.0 - ca*ca - cb*cb - cg*cg + 2.0*ca*cb*cg
    return a*b*c*math.sqrt(max(t, 0.0))


def perp_widths(a, b, c, al, be, ga):
    """Perpendicular width of the cell along each axis = V / (area of opposite face)."""
    V = cell_volume(a, b, c, al, be, ga)
    ra, rb, rg = math.radians(al), math.radians(be), math.radians(ga)
    return (V/(b*c*math.sin(ra)), V/(a*c*math.sin(rb)), V/(a*b*math.sin(rg)))


def parse_cif(path):
    a=b=c=al=be=ga=None
    loop_tags = None
    in_loop = False
    counts = collections.Counter()
    natoms = 0
    with open(path, 'r', errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s:
                in_loop = False if loop_tags is None else in_loop
                continue
            low = s.lower()
            if low.startswith('_cell_length_a'):   a = float(s.split()[1])
            elif low.startswith('_cell_length_b'): b = float(s.split()[1])
            elif low.startswith('_cell_length_c'): c = float(s.split()[1])
            elif low.startswith('_cell_angle_alpha'): al = float(s.split()[1])
            elif low.startswith('_cell_angle_beta'):  be = float(s.split()[1])
            elif low.startswith('_cell_angle_gamma'): ga = float(s.split()[1])
            elif low == 'loop_':
                loop_tags = []
                in_loop = False
            elif loop_tags is not None and s.startswith('_'):
                loop_tags.append(low)
            elif loop_tags is not None:
                # first data line of the loop
                if '_atom_site_fract_x' in loop_tags:
                    in_loop = True
                    idx_sym = (loop_tags.index('_atom_site_type_symbol')
                               if '_atom_site_type_symbol' in loop_tags else None)
                    idx_lab = (loop_tags.index('_atom_site_label')
                               if '_atom_site_label' in loop_tags else None)
                    tags = loop_tags
                    loop_tags = None
                    # fall through to process this line below
                    tok = s.split()
                    if idx_sym is not None and len(tok) > idx_sym:
                        el = tok[idx_sym]
                    else:
                        el = ''.join(ch for ch in tok[idx_lab] if ch.isalpha())
                    counts[el] += 1; natoms += 1
                    continue
                else:
                    loop_tags = None
                    in_loop = False
                    continue
            elif in_loop:
                tok = s.split()
                if len(tok) < 4:
                    in_loop = False
                    continue
                if idx_sym is not None and len(tok) > idx_sym:
                    el = tok[idx_sym]
                else:
                    el = ''.join(ch for ch in tok[idx_lab] if ch.isalpha())
                counts[el] += 1; natoms += 1
    return a, b, c, al, be, ga, natoms, counts


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sorted(n for n in os.listdir(DB) if n.endswith('.cif'))
    elem_hist = collections.Counter()
    unknown = collections.Counter()
    rows = []
    bad = []
    for n in names:
        p = os.path.join(DB, n)
        try:
            a, b, c, al, be, ga, natoms, counts = parse_cif(p)
            if None in (a, b, c, al, be, ga) or natoms == 0:
                bad.append(n); continue
            V = cell_volume(a, b, c, al, be, ga)
            mass = sum(MASS.get(e, 0.0)*k for e, k in counts.items())
            for e in counts:
                elem_hist[e] += 1
                if e not in MASS:
                    unknown[e] += 1
            # density in g/cm3: mass[amu]/V[A^3] * 1.66053906660
            dens = mass / V * 1.66053906660
            wa, wb, wc = perp_widths(a, b, c, al, be, ga)
            comp = ''.join('%s%d' % (e, counts[e]) for e in sorted(counts))
            rows.append((n[:-4], a, b, c, al, be, ga, V, natoms, mass, dens,
                         wa, wb, wc, natoms/V, comp))
        except Exception as e:
            bad.append('%s:%s' % (n, type(e).__name__))
    with open(os.path.join(OUT, 'structures.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['name','a','b','c','alpha','beta','gamma','cell_vol_A3',
                    'natoms','mass_amu','density_g_cm3','wa','wb','wc',
                    'atom_density_A-3','composition'])
        for r in rows:
            w.writerow(['%s' % r[0]] + ['%.6g' % x if isinstance(x, float) else x
                                        for x in r[1:]])
    with open(os.path.join(OUT, 'elements.txt'), 'w') as f:
        for e, k in elem_hist.most_common():
            f.write('%s\t%d\t%s\n' % (e, k, 'KNOWN' if e in MASS else 'UNKNOWN'))
    with open(os.path.join(OUT, 'scan_bad.txt'), 'w') as f:
        for x in bad:
            f.write(x + '\n')
    print('parsed=%d bad=%d elements=%d unknown_elements=%s'
          % (len(rows), len(bad), len(elem_hist), sorted(unknown)))


if __name__ == '__main__':
    main()
