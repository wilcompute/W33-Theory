from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'

def load(name):
    return json.loads((DATA/name).read_text())

def test_2996_adaptive_d4_dominates_fixed_29():
    d=load('PART_BT2996_D4_STATIC_ADAPTIVE_LOCALIZATION_results.json')
    assert all(d['checks'].values())
    assert d['global_fixed_schedule_bounds']=={'lower':23,'upper':29,'global_29_minimality':'open'}
    assert d['adaptive_depth_histogram']=={'23':44848,'24':3566,'25':412}
    assert d['adaptive_uniform_mean_triangles']<23.1

def test_2997_natural_equivariance_is_obstructed():
    d=load('PART_BT2997_CLOCK_FRAME_EQUIVARIANCE_results.json')
    assert all(d['checks'].values())
    assert d['skew_frame_character_at_transvection']==0
    assert d['clock_orbit_character_at_translation']==540

def test_2998_exact_route_diameter_two():
    d=load('PART_BT2998_LOCALITY_A40_ROUTING_results.json')
    assert all(d['checks'].values())
    assert d['distance_histogram']=={'0':40,'1':1080,'2':480}
    assert max(map(int,d['distance_histogram']))==2

def test_2999_exact_adaptive_policy():
    d=load('PART_BT2999_ADAPTIVE_BAYES_CONTROLLER_results.json')
    assert all(d['checks'].values())
    assert d['exact_policy_residual_error']==0
    assert d['prior_weighted_mean_triangles']<23.007
    assert d['next_action_alphabet_size']==14

def test_3000_fake_gate_rewrite_order():
    d=load('PART_BT3000_FAKE_GATE_AUDIT_results.json')
    assert all(d['checks'].values())
    assert d['optimization_order'][0]=='delete by relabeling'
    assert d['optimization_order'][-1]=='only then synthesize physically'

def test_3001_optimal_balanced_sync_word():
    d=load('PART_BT3001_SELF_SYNCHRONIZING_CURVATURE_results.json')
    assert all(d['checks'].values())
    assert d['slot_word']==[1,0,2,3,3,2,0,0,1,1,2,3]
    assert d['cyclic_shift_minimum_distance']==9
    assert d['correctable_arbitrary_slot_symbol_errors']==4

def test_3002_predictive_action_entropy():
    d=load('PART_BT3002_PREDICTIVE_THERMODYNAMIC_CONTROLLER_results.json')
    assert all(d['checks'].values())
    assert d['predictive_next_action_fixed_bits']==4
    assert d['predictive_next_action_entropy_bits']<0.052
    assert d['rate_distortion_endpoints'][1]['residual_bayes_error']==0

def test_shared_summary():
    d=load('PART_BT2996_BT3002_DEEP_OPTIMAL_INFORMATION_summary.json')
    assert d['check_count']==7
    assert all(d['checks'].values())
