from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())
def test_summary():
 d=load('PART_BT2960_BT2966_PHYSICAL_COMPILER_summary.json');assert d['check_count']==7 and all(d['checks'].values())
def test_factorized_observer():
 d=load('PART_BT2960_SPC15_PHYSICAL_FACTORIZATION_results.json');assert d['minimum_distance']==4 and d['incidence_reduction_factor']==3 and d['structured_reversible_decode']=={'not_gates':8,'cnot_gates':8,'decoded_trits':4,'fifth_triplet_role':'parity syndrome'}
def test_coherent_m36():
 d=load('PART_BT2961_M36_COHERENT_CORRELATED_LEAKAGE_results.json');assert sum(d['single_location_coherent_quadratic_histogram'].values())==189 and d['common_systematic_H_axis_coefficients']['Y']=='7/54'
def test_gauge_classification():
 d=load('PART_BT2962_SPREAD_GAUGE_CLASSIFICATION_results.json');assert d['spread_count']==36 and d['generated_holonomy_group']=='D4' and d['abelian_sign_curvature']['violations']==0
def test_optical_profiles():
 d=load('PART_BT2963_OAM_10X4_CHANNEL_MODEL_results.json');assert len(d['profiles'])==4
 for p in d['profiles']:assert abs(p['unconditional_correct_click']+p['unconditional_wrong_click']+p['erasure_or_multiclick']-1)<1e-12
def test_reversible_compiler():
 d=load('PART_BT2964_REVERSIBLE_COMPILER_SYNTHESIS_results.json');s=d['structured_protected_path'];assert (s['joint_rank_toffoli'],s['joint_rank_cnot'],s['exhaustive_valid_states'])==(120,79,3240)
 g=load('PART_BT2964_JOINT_RANK_GATE_LIST.json');assert g['gate_count']==199 and g['toffoli_count']==120 and g['cnot_count']==79
def test_bonkers_closures():
 a=load('PART_BT2965_CURVATURE_ROUTE_CODE_results.json');b=load('PART_BT2966_ANTISYMPLECTIC_PHASE_TRANSDUCER_results.json');assert a['pilot_detection']['3']['fraction']=='1' and b['global_phase_histogram']=={'0':1080,'1':1080,'2':1080}
