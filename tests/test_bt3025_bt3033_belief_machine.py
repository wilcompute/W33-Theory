from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))

from bt3025_3031_common import TRIANGLES, VERIFIED_28, frozen_collision_classes, hypotheses, syndrome_matrix
from bt3027_edit_sync_pilot_order import OMITTED, PILOT_ORDER, synchronization_score


def load(name):
    return json.loads((ROOT/'data'/name).read_text())


def test_exact_discrete_frontier():
    assert len(hypotheses())==48_826
    selected=[TRIANGLES.index(t) for t in VERIFIED_28]
    matrix=syndrome_matrix(selected)
    assert len({row.tobytes() for row in matrix})==48_826
    assert len(frozen_collision_classes(syndrome_matrix()))==1_436


def test_edit_sync_construction():
    pilot_score,_=synchronization_score(PILOT_ORDER)
    combined=tuple((OMITTED[i],PILOT_ORDER[i]) for i in range(12))
    combined_score,_=synchronization_score(combined)
    assert pilot_score==0.5
    assert combined_score==0.6


def test_noisy_reference():
    data=load('PART_BT3025_NOISY_D4_BAYES_results.json')
    assert data['collision_classes_after_exact_base']==1436
    assert abs(data['profiles']['moderate']['conditional_residual_error']-0.0007574986249606812)<2e-11


def test_sat_gate_is_fail_closed():
    data=load('PART_BT3026_D4_FIXED_OPTIMUM_results.json')
    assert data['verified_28_full_d4_unique'] is True
    assert data['status'] in {
        'SOURCE_COMPLETE_27_DECISION_PENDING',
        'SAT_CENTRAL_ONLY_FULL_D4_REJECTED',
        'SAT_FULL_D4_27_FOUND',
        'UNSAT_REPORTED_PROOF_REQUIRES_INDEPENDENT_CHECK',
        'COMPLETE_UNSAT_PROOF_VERIFIED_OPTIMUM_28',
    }


def test_causal_state_quotient():
    data=load('PART_BT3029_PREDICTIVE_CAUSAL_STATES_results.json')
    assert data['raw_collision_classes']==1436
    assert data['initial_future_action_causal_states']==457
    assert data['all_recursive_controller_states_including_stop']==470
    assert abs(data['entropy_reduction_bits']-1.0782908546674506)<2e-11


def test_fourier_engine():
    data=load('PART_BT3030_D4_FOURIER_BELIEF_results.json')
    assert data['physical_symbol_count']==8
    assert data['spectral_channel_count']==5
    assert data['two_dimensional_block_scalar']=='89/100'


def test_measurement_portfolio():
    data=load('PART_BT3031_MEASUREMENT_BASIS_PORTFOLIO_results.json')
    full=data['alphabets']['full_D4']['conditional_best_one_probe_error']
    coarse=data['alphabets']['conjugacy_class_5']['conditional_best_one_probe_error']
    assert full<=coarse
    assert data['conjugacy_sensor_retains_fraction_of_full_risk_reduction']>0.996


def test_summary_boundaries():
    data=load('PART_BT3025_BT3031_BELIEF_MACHINE_summary.json')
    assert data['current_fixed_schedule_bounds']==[23,28]
    assert 'independently checked SAT/DRUP decision for size 27' in data['pending']
