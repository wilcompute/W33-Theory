from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def ledger(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_pass671_actual_h1_rigidity():
 p=ledger('w33_pass671_integral_h1_psp_rigidity.json');assert p['status']=='PASS';assert p['integral_homology']['H1_rank']==81;assert p['symmetry']['projective_action_order']==25920;assert p['commutant_rigidity']['centralizer_dimension_over_F2']==1

def test_pass672_compiled_gauge_register():
 p=ledger('w33_pass672_compiled_conductor_gauge_register.json');assert p['status']=='PASS';assert p['compiler']['canonical_frames']==5040;assert p['compiler']['gauge_states']==8;assert p['compression']['factor']>7.99

def test_pass673_noisy_optical_falsifier():
 p=ledger('w33_pass673_noisy_flat_probe_hardware_falsifier.json');assert p['status']=='PASS';assert p['monte_carlo_falsifier']['optimized']['maximum_channel_abs_error_q95']<.03;assert p['stress_envelope']['maximum_passing_stress']==5.0

def test_pass674_per_shot_martingale():
 p=ledger('w33_pass674_per_shot_propensity_martingale.json');assert p['status']=='PASS';assert p['e_process']['first_detection']['delay']<6000;assert p['covariance_replay']['dynamic_over_frozen_ratio']<.02;assert p['matrix_safety']['whitened_true_covariance_max_eigenvalue']<1

def test_pass675_multidimensional_atlas():
 p=ledger('w33_pass675_multidimensional_controller_atlas.json');assert p['status']=='PASS';assert p['parameterization']['cell_count']==7776;assert p['phase_atlas']['distinct_optimal_root_phases']==22;assert p['phase_atlas']['unique_tagged_pair_cells']==1308
