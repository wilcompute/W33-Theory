from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'data/PART_4005_4007_4010_4012_EXACT_PHOTON_REVIVAL.json'

def load(): return json.loads(RESULT.read_text())

def test_exact_finite_detuning_revival():
    x=load(); r=x['pass4005_exact_nondispersive_revival']
    assert x['status']=='PASS_EXACT_NONDISPERSIVE_REVIVAL_TOMOGRAPHY_MEMORY_AND_THREE_CONSTRUCTIONS'
    assert x['semantic_sha256']=='3e4561f56a0719c85a3b1e9b56f3c79d5d3e0bc4e9a21707a30abd26bb6a5cf2'
    assert r['exact_ratio_Delta_over_g']=='2*sqrt(2)'
    assert r['exact_interaction_g_t']=='pi/sqrt(2)'
    assert r['half_angle_windings']=={'detuning':1,'sigma_4':3,'sigma_sqrt6':2}
    assert r['off_block_leakage_operator_norm']<1e-12
    assert r['full_unitary_operator_error']<1e-12

def test_quadratic_form_tomography():
    x=load()['pass4006_quadratic_form_wigner_smith_tomography']
    assert x['general_hermitian_quadratic_probe_count']==1600
    assert x['reciprocal_real_symmetric_probe_count']==820
    assert x['recovered_w33_edges']==240
    assert x['ideal_reconstruction_max_error']<1e-12
    ratios=x['three_frequency_central_difference']['successive_richardson_error_ratios']
    assert min(ratios)>14

def test_write_hold_read_gate():
    x=load()['pass4007_exact_bright_dark_write_hold_read']
    assert x['identities']==['T^T T=E16+E6','T T^T=F16+F6']
    assert x['arbitrary_phase_test_operator_error']<1e-12
    assert x['arbitrary_phase_test_line_leakage']<1e-12
    assert x['w33_reflection_sequence_error']<1e-12

def test_three_bonkers():
    x=load()
    a=x['pass4010_bonkers_revival_arithmetic']
    assert a['smallest_positive_solution']['n16']==3
    assert a['smallest_positive_solution']['n6']==2
    assert a['smallest_positive_solution']['k']==1
    c=x['pass4011_bonkers_spectral_checksum_and_geometry_oracle']
    assert c['checksum_operator_norm_at_theta_prime_1']==0.0
    rows=c['synchronized_tensor_clock']['point_plus_minus_multiplicities']
    assert rows[0]=={'m':1,'minus_multiplicity':24,'plus_multiplicity':16,'point_dimension':40}
    assert rows[-1]['point_dimension']==40**8
