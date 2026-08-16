#!/usr/bin/env python3
"""Deterministic replay runner for Passes 5683--5690."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5683_balanced_ramanujan_levi_lifts.py',
 'analysis/w33_pass5684_collision_linfinity_support_weld.py',
 'analysis/w33_pass5685_deck16_local_flatbond_ratio2.py',
 'analysis/w33_pass5686_asl23_su3_bracket.py',
 'analysis/w33_pass5687_metric_clock_expander_no_spacetime.py',
 'analysis/w33_pass5688_balanced_signing_search_vs_random.py',
 'analysis/w33_pass5689_fermionic_exterior_collision_boundary.py',
 'analysis/w33_pass5690_deck16_synthetic_berry_chern8.py',
]
def main():
    for s in SCRIPTS:
        print(f'=== {s} ===',flush=True)
        subprocess.run([sys.executable,str(ROOT/s)],cwd=ROOT,check=True)
    print('PASS5683_5690_REPLAY_OK')
if __name__=='__main__':main()
