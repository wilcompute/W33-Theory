#!/usr/bin/env python3
"""Deterministic replay runner for Pass5619-5626 physics deck/bundle frontier."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5619_spinor_deck_module.py',
 'analysis/w33_pass5620_e6_horizontal_vertical_selector.py',
 'analysis/w33_pass5621_many_cell_magnetic_clt.py',
 'analysis/w33_pass5622_phs_dirac_mass_ratio.py',
 'analysis/w33_pass5623_cover_f4_fixed_vertex_physics_gate.py',
 'analysis/w33_pass5624_split_step_lightcone.py',
 'analysis/w33_pass5625_finite_eta_spectral_flow.py',
 'analysis/w33_pass5626_deck_superselection_symmetry_classes.py',
]
def main():
    for s in SCRIPTS:
        print('RUN',s,flush=True)
        subprocess.run([sys.executable,str(ROOT/s)],cwd=ROOT,check=True)
    print('PASS5619_5626_REPLAY_OK')
if __name__=='__main__': main()
