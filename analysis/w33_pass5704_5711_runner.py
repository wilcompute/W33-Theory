#!/usr/bin/env python3
"""Deterministic replay runner for Pass5704-5711."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5704_affine_su3_wilson_face_selection.py',
 'analysis/w33_pass5705_deck96_192_group_fingerprint.py',
 'analysis/w33_pass5706_ramanujan_levels45_and_color_gauge.py',
 'analysis/w33_pass5707_linfinity_l1_zero_no_go.py',
 'analysis/w33_pass5708_e8_27x3_generation_commutant.py',
 'analysis/w33_pass5709_z3_center_flux_su3_adjoint_no_go.py',
 'analysis/w33_pass5710_deck_DK_pfaffian_topology.py',
 'analysis/w33_pass5711_generation_hierarchy_symmetry_breaking.py',
]
def main():
  for s in SCRIPTS:
    print(f'=== {s} ===',flush=True)
    subprocess.run([sys.executable,str(ROOT/s)],cwd=ROOT,check=True)
if __name__=='__main__':main()
