#!/usr/bin/env python3
"""Deterministic replay runner for Passes 5627-5634."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass5627_deck_stabilizer_spinor_no_go.py',
 'analysis/w33_pass5628_e6_gauge_action_two_coupling_no_go.py',
 'analysis/w33_pass5629_connected_cover_tower_obstruction.py',
 'analysis/w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected.py',
 'analysis/w33_pass5631_q5_fixed_line_crossq_module_gate.py',
 'analysis/w33_pass5632_pin_bdg_spin_statistics_no_go.py',
 'analysis/w33_pass5633_bad9_gauge_generator_not_boson.py',
 'analysis/w33_pass5634_sheet_decimation_resolvent_rg.py',
]
def main():
    for s in SCRIPTS:
        print('REPLAY',s,flush=True)
        subprocess.run([sys.executable,s],cwd=ROOT,check=True)
    print('PASS5627_5634_REPLAY_OK')
if __name__=='__main__':main()
