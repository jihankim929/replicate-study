#!/usr/bin/env python3
"""Extract the numbers we need from a RASPA .data file into one CSV line.

Emitted fields (no header; header is written once when the results file is
created):
  sid,P_Pa,ninit,nprod,seed,grid,wall_s,rc,uc,rho_kgm3,
  n_uc,n_uc_err,vol_cm3cm3,vol_err,molkg,molkg_err,henry,ok
"""
import sys, os, re, glob

case, sid, ppa, ninit, nprod, seed, grid, wall, rc = sys.argv[1:10]

def blank(reason):
    print(','.join([sid, ppa, ninit, nprod, seed, grid, wall, rc,
                    '', '', '', '', '', '', '', '', '', reason]))
    sys.exit(0)

f = glob.glob(os.path.join(case, 'Output', 'System_0', '*.data'))
if not f:
    blank('NOOUT')
txt = open(f[0], 'r', errors='replace').read()

def last(pat, n=2):
    m = re.findall(pat, txt)
    return m[-1] if m else None

uc = 'x'.join(os.path.basename(f[0]).split('_')[-3].split('.'))
rho = last(r'Framework Density:\s+([0-9.eE+-]+)\s+\[kg/m\^3\]')

nuc = last(r'Average loading absolute \[molecules/unit cell\]\s+([0-9.eE+-]+)\s+\+/-\s+([0-9.eE+-]+)')
vol = last(r'Average loading absolute \[cm\^3 \(STP\)/cm\^3 framework\]\s+([0-9.eE+-]+)\s+\+/-\s+([0-9.eE+-]+)')
mkg = last(r'Average loading absolute \[mol/kg framework\]\s+([0-9.eE+-]+)\s+\+/-\s+([0-9.eE+-]+)')
hen = last(r'\[K_H\]\s*:\s*([0-9.eE+-]+)')

if vol is None:
    blank('NOLOAD' if 'Simulation finished' not in txt else 'NOPARSE')

ok = 'OK' if ('Simulation finished' in txt) else 'UNFIN'
row = [sid, ppa, ninit, nprod, seed, grid, wall, rc, uc, rho or '',
       nuc[0] if nuc else '', nuc[1] if nuc else '',
       vol[0], vol[1],
       mkg[0] if mkg else '', mkg[1] if mkg else '',
       hen or '', ok]
print(','.join(row))
