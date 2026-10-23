"""Regression for timed pair census, classical link reservations and F3 drift."""
import os,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_timing_optimal_interference_20261023 import census
from w33_fractal_multiuser_linebus_capacity_20261023 import allocate,report
from w33_fractal_qutrit_F3_tile_drift_20261023 import reconstruct,noise_sweep
def test_all_3240_two_path_pairs_and_best_equal_arrival():
    c=census()
    assert c['all_path_pair_comparisons']==3240
    assert c['same_start_same_arrival_nontrivial_phase_pairs']==192
    assert c['no_wait_nontrivial_phase_pairs']==0
    w=c['minimum_same_arrival_witness']
    assert w['path_a']==[4,5,19] and w['path_b']==[4,11,19]
    assert w['arrival_slots']==4 and w['waits_a']==w['waits_b']==2
    assert w['relative_i_exponent']==1
def test_exact_90_request_capacity_and_no_colliding_links():
    q=allocate()
    assert q['demands']==q['delivered']==90
    links=[]
    for trace in q['traces']:
        links.extend(tuple(x) for x in trace['links'])
    assert len(links)==len(set(links))
    assert q['total_optical_storage_waits_unimplemented']>0
def test_failure_and_phase_constrained_capacity():
    d=report()['cases']
    assert set(d)=={'normal','bus0_fault','phase_zero','fault_and_phase'}
    assert all(x['delivered']==90 for x in d.values())
    assert d['phase_zero']['mean_release_delay_slots']>=d['normal']['mean_release_delay_slots']
    assert d['bus0_fault']['mean_release_delay_slots']>=d['normal']['mean_release_delay_slots']
    for x in d['fault_and_phase']['traces']:
        assert x['frame']==0
        assert all(edge[1:]!=[0,0] for edge in x['links'])
def test_qutrit_exact_and_noise_sensitivity():
    o=noise_sweep(samples=18)
    assert o['active_two_mode_gates']==3
    assert o['phase_bank']==4
    assert o['ideal_reconstruction_error']<1e-12
    scores=[r['mean_unconditional_process_overlap'] for r in o['noise_sweep']]
    assert scores[0]==pytest.approx(1)
    assert scores[0]>scores[1]>scores[2]>scores[3]
def test_fourth_mode_undisturbed_in_perfect_compiler():
    U=reconstruct()
    assert abs(U[3,3]-1)<1e-12
    assert np.linalg.norm(U[3,:3])<1e-12
    assert np.linalg.norm(U[:3,3])<1e-12
