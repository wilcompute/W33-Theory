#!/usr/bin/env python3
"""Deterministic replay runner for Passes 5691--5698."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5691_affine_su3_discrete_ym_complex.py',
 'analysis/w33_pass5692_deck16_flatray_duality.py',
 'analysis/w33_pass5693_explicit_ramanujan_levels23.py',
 'analysis/w33_pass5694_collision_jacobi_expansion_l3_no_go.py',
 'analysis/w33_pass5695_ramanujan_dirac_tensor_separation.py',
 'analysis/w33_pass5696_agl_orientation_twisted_su3.py',
 'analysis/w33_pass5697_ramanujan_adjoint_laplacian_gap.py',
 'analysis/w33_pass5698_vertical_z3_generation_falsifier.py',
]
def main():
  for s in SCRIPTS:
    print(f'=== {s} ===',flush=True)
    subprocess.run([sys.executable,str(ROOT/s)],cwd=ROOT,check=True)
if __name__=='__main__':main()
