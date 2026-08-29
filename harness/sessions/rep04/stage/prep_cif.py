#!/usr/bin/env python3
"""Rewrite a db CIF into a RASPA-readable P1 CIF.

The pinned UFF set names its pseudo-atoms with a trailing underscore ('C_',
'Ag_'); the database CIFs label atoms 'C1', 'Ag3'.  This script relabels only:
positions, cell and composition are copied through unchanged.  The
_atom_site_charge column is dropped because the protocol is chargeless.
"""
import sys, os, math

def parse(path):
    cell = {}
    tags = None
    rows = []
    idx_sym = idx_lab = ix = iy = iz = None
    reading = False
    for line in open(path, 'r', errors='replace'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        low = s.lower()
        if low.startswith('_cell_length_') or low.startswith('_cell_angle_'):
            cell[low.split()[0]] = float(s.split()[1])
            continue
        if low == 'loop_':
            tags = []
            reading = False
            continue
        if tags is not None and s.startswith('_'):
            tags.append(low)
            continue
        if tags is not None:
            if '_atom_site_fract_x' in tags:
                idx_sym = tags.index('_atom_site_type_symbol') if '_atom_site_type_symbol' in tags else None
                idx_lab = tags.index('_atom_site_label') if '_atom_site_label' in tags else None
                ix = tags.index('_atom_site_fract_x')
                iy = tags.index('_atom_site_fract_y')
                iz = tags.index('_atom_site_fract_z')
                reading = True
            else:
                reading = False
            tags = None
        if reading:
            t = s.split()
            if len(t) <= max(ix, iy, iz):
                reading = False
                continue
            el = t[idx_sym] if idx_sym is not None else ''.join(ch for ch in t[idx_lab] if ch.isalpha())
            rows.append((el, float(t[ix]), float(t[iy]), float(t[iz])))
    return cell, rows


def write(dst, name, cell, rows):
    with open(dst, 'w') as f:
        f.write('data_%s\n' % name)
        f.write('_symmetry_space_group_name_H-M   \'P 1\'\n')
        f.write('_symmetry_Int_Tables_number      1\n')
        f.write('_symmetry_cell_setting           triclinic\n')
        for k in ('a', 'b', 'c'):
            f.write('_cell_length_%s   %.6f\n' % (k, cell['_cell_length_' + k]))
        for k in ('alpha', 'beta', 'gamma'):
            f.write('_cell_angle_%s   %.6f\n' % (k, cell['_cell_angle_' + k]))
        f.write('loop_\n_atom_site_label\n_atom_site_type_symbol\n'
                '_atom_site_fract_x\n_atom_site_fract_y\n_atom_site_fract_z\n')
        for el, x, y, z in rows:
            f.write('%-5s %-3s %10.6f %10.6f %10.6f\n' % (el + '_', el, x, y, z))


def cell_volume(c):
    a, b, cc = c['_cell_length_a'], c['_cell_length_b'], c['_cell_length_c']
    ra = math.radians(c['_cell_angle_alpha']); rb = math.radians(c['_cell_angle_beta'])
    rg = math.radians(c['_cell_angle_gamma'])
    ca, cb, cg = math.cos(ra), math.cos(rb), math.cos(rg)
    t = 1 - ca*ca - cb*cb - cg*cg + 2*ca*cb*cg
    return a*b*cc*math.sqrt(max(t, 0.0))


def unitcells(c, cutoff=12.8):
    a, b, cc = c['_cell_length_a'], c['_cell_length_b'], c['_cell_length_c']
    ra = math.radians(c['_cell_angle_alpha']); rb = math.radians(c['_cell_angle_beta'])
    rg = math.radians(c['_cell_angle_gamma'])
    V = cell_volume(c)
    w = (V/(b*cc*math.sin(ra)), V/(a*cc*math.sin(rb)), V/(a*b*math.sin(rg)))
    return tuple(max(1, int(math.ceil(2.0*cutoff/x))) for x in w)


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    name = os.path.basename(dst)[:-4]
    cell, rows = parse(src)
    write(dst, name, cell, rows)
    print('%d %d %d %.4f' % (unitcells(cell) + (cell_volume(cell),)))
