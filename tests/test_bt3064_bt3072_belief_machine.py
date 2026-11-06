from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())

def test_generator_summary():
 d=load('PART_BT3064_BT3070_BELIEF_MACHINE_summary.json');assert d['status']=='COMPLETE_EXACT_AND_EXPLICIT_MODEL_GENERATOR';assert all(d['checks'].values())

def test_noisy_reference():
 d=load('PART_BT3064_NOISY_D4_BAYES_results.json');assert d['hypotheses']==48826 and d['collision_classes_after_exact_base']==1436;assert abs(d['profiles']['moderate']['conditional_residual_error']-.0007574986249606812)<2e-11

def test_sat_fail_closed():
 d=load('PART_BT3065_D4_FIXED_OPTIMUM_results.json');assert d['verified_28_full_d4_unique'];assert d['current_exact_bounds']==[23,28];assert d['status'] in {'SOURCE_COMPLETE_27_DECISION_PENDING','SAT_CENTRAL_ONLY_FULL_D4_REJECTED','SAT_FULL_D4_27_FOUND','UNSAT_REPORTED_PROOF_REQUIRES_INDEPENDENT_CHECK','COMPLETE_UNSAT_PROOF_VERIFIED_OPTIMUM_28'}

def test_edit_sync():
 d=load('PART_BT3066_EDIT_SYNC_PILOT_ORDER_results.json');assert d['cyclic_hamming_distance']==9;assert d['minimum_cyclic_levenshtein_distance']==2;assert d['pilot_order_synchronization_score']==.5;assert d['combined_omission_order_synchronization_score']==.6

def test_causal_states():
 d=load('PART_BT3068_PREDICTIVE_CAUSAL_STATES_results.json');assert (d['raw_collision_classes'],d['initial_future_action_causal_states'],d['all_recursive_controller_states_including_stop'])==(1436,457,470);assert abs(d['entropy_reduction_bits']-1.0782908546674506)<2e-11

def test_fourier():
 d=load('PART_BT3069_D4_FOURIER_BELIEF_results.json');assert d['physical_symbol_count']==8 and d['spectral_channel_count']==5 and d['two_dimensional_block_scalar']=='89/100'

def test_portfolio():
 d=load('PART_BT3070_MEASUREMENT_BASIS_PORTFOLIO_results.json');assert d['alphabets']['full_D4']['conditional_best_one_probe_error']<=d['alphabets']['conjugacy_class_5']['conditional_best_one_probe_error'];assert d['conjugacy_sensor_retains_fraction_of_full_risk_reduction']>.996

def test_source_boundaries():
 d=load('PART_BT3064_BT3070_BELIEF_MACHINE_source_summary.json');assert d['current_fixed_schedule_bounds']==[23,28];assert 'independently checked SAT/DRUP decision for size 27' in d['pending']
