#!/usr/bin/env python3
"""Deterministic replay runner for Passes 5675-5682."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5675_deck16_equivariant_bdg_normal_form.py',
 'analysis/w33_pass5676_e6_fiber_collision_projector.py',
 'analysis/w33_pass5677_connected_levi_voltage_tower.py',
 'analysis/w33_pass5678_voltage_tower_spectrum_and_bottleneck.py',
 'analysis/w33_pass5679_section_parent_real_imag_feshbach.py',
 'analysis/w33_pass5680_deck16_classd_pfaffian_triviality.py',
 'analysis/w33_pass5681_agl23_vertical_1plus8_no_gluon_bracket.py',
 'analysis/w33_pass5682_cover_tower_causal_speed_scaling.py',
]
def main():
    for s in SCRIPTS:
        print(f'\n=== {s} ===',flush=True)
        subprocess.run([sys.executable,str(ROOT/s)],cwd=ROOT,check=True)
    print('\nPass5675-5682 deterministic replay complete.')
if __name__=='__main__':main()
