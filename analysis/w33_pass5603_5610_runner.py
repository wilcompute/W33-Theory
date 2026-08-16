#!/usr/bin/env python3
"""Replay the Python portion of Pass5603-5610 fail-closed."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5603_psl2_fixedpoint_fusion_symbolic.py',
 'analysis/w33_pass5604_isodual_minimum_distance.py',
 'analysis/w33_pass5605_hodge_hashimoto_scaling_firewall.py',
 'analysis/w33_pass5607_segre_dalembertian_no_go.py',
 'analysis/w33_pass5608_s12_golay_weight12_m12_action.py',
 'analysis/w33_pass5609_s12_heisenberg_phase_segre_spectrum.py',
 'analysis/w33_pass5610_s12_w33_symplectic_embedding_firewall.py',
]
def main():
    for rel in SCRIPTS:
        print(f'==> {rel}',flush=True)
        subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,check=True)
if __name__=='__main__': main()
