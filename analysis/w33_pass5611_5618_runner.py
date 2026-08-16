#!/usr/bin/env python3
"""Replay Pass5611--5618 producers in deterministic order."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5611_general_q_heisenberg_magnetic_bulk.py',
 'analysis/w33_pass5612_projectivity_minwords_semilinear.py',
 'analysis/w33_pass5613_intrinsic_heisenberg_vector_lift.py',
 'analysis/w33_pass5614_q3_physics_selector.py',
 'analysis/w33_pass5615_cover_f4_object_dictionary_gate.py',
 'analysis/w33_pass5616_dirac_magnetic_dispersion.py',
 'analysis/w33_pass5617_z3_gauge_harper.py',
 'analysis/w33_pass5618_gauge_matter_phase_selection.py',
]
def main():
    for rel in SCRIPTS:
        print(f'==> {rel}',flush=True)
        subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,check=True)
if __name__=='__main__':main()
