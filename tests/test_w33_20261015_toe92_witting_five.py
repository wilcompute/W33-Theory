"""TOE92 five Witting physical/security fronts with frozen certificate checks."""
from functools import lru_cache
import json, math
from pathlib import Path
import numpy as np
import pytest
from analysis import w33_20261015_toe92_full_symplectic_4mode as G
from analysis import w33_20261015_toe92_iid_cq_privacy as K
from analysis import w33_20261015_toe92_optical_givens_mesh as O
from analysis import w33_20261015_toe92_herald_h27_nogo as A

ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def fresh(key):
    return {'symp':G.calculate,'key':K.certificate,'optics':O.certificate,'adversary':A.certificate}[key]()

def test_full_projective_psp43_group_order_and_cayley_closure():
    r=fresh('symp')
    assert r['full_projective_group_order']==25920
    assert r['four_plane_local_generators_projective_subgroup_order']==288
    assert r['all_Cayley_edges_verified']==5*25920
    assert r['maximum_projective_unitary_closure_residual']==0
    assert all(x==3 for x in r['generator_orders_in_projective_permutation_group'].values())

def test_explicit_projective_cocycle_holonomy_witness():
    r=fresh('symp')['explicit_scalar_projective_cocycle_relation']
    assert r['projective_loop_identity'] is True
    z=complex(r['scalar_phase_real'],r['scalar_phase_imag'])
    assert abs(abs(z)-1)<1e-9
    assert abs(z-1)>1
    assert all(0<=j<5 for j in r['left_word_generators'])

def test_quantum_collision_entropy_sanity_extreme_states():
    assert K.collision_entropy(0)[0]==pytest.approx(0,abs=1e-11)
    assert K.collision_entropy(1)[0]==pytest.approx(2,abs=1e-11)
    for v in [.2,.25,.5,.7,.8,.9,.95]:
        h2,g=K.collision_entropy(v)
        assert 0<h2<2 and g==pytest.approx(2**(-h2),abs=1e-10)

def test_iid_purifying_eve_privacy_only_conditional_bound():
    r=fresh('key')
    v={x['visibility']:x for x in r['rows']}
    assert r['N']==8192
    assert r['target_quantum_secrecy_trace_distance_bound']==1e-8
    assert v[.8]['quantum_leftover_hash_secrecy_only_bits']==7398
    assert v[.25]['optimistic_privacy_minus_asymptotic_leak_margin_bits']<0
    assert v[1]['quantum_leftover_hash_secrecy_only_bits']==16332

def test_optical_40_four_mode_ideal_mesh_reconstruction():
    r=fresh('optics')
    assert r['basis_count']==40
    assert sum(r['Givens_coupler_counts'].values())==40
    assert r['Givens_coupler_counts']['0']==1
    assert r['maximum_two_mode_couplers_per_setting']==6
    assert r['maximum_per_path_coupler_depth']==5
    assert r['shared_reconfigurable_mesh_upper_bound_couplers']==6
    assert r['max_unitary_reconstruction_residual']==0
    for row in r['circuits']:
        assert row['two_mode_couplers']==len(row['coupler_operations'])<=6
        assert len(row['outgoing_diagonal_phase_rad'])==4
        assert row['max_U4_reconstruction_error']==0

def test_explicit_loss_budget_assumptions_not_hardware():
    r=fresh('optics')
    assert r['per_side_loss_assumptions']=={
       'each_coupler_intensity_transmission':.98,
       'photon_detector_efficiency':.85}
    assert r['pessimistic_pair_coincidence_survival_ignoring_source_and_switch']==pytest.approx((.85*.98**5)**2,abs=1e-11)

def test_per_setting_balanced_herald_can_falsely_certify_product_state():
    r=fresh('adversary')
    assert r['unconditioned_uniform_basis_match']=='2/5'
    a=r['uniform_per_basis_acceptance_outcome_attack']
    assert a['accepted_fraction_each_of_40_bases']=='1/3'
    assert a['conditioned_match']=='1'
    assert a['accept_probability_if_mismatch']=='0'

def test_efficiency_limited_product_attack_and_universal_upper():
    r=fresh('adversary')
    from fractions import Fraction
    val=Fraction(r['constructive_basis_efficiency_attack_conditional_match'])
    upper=Fraction(r['setting_efficiency_ratio_universal_separable_upper_bound'])
    assert Fraction(2,5)<val<=upper

def test_H27_regular_set_equivariance_impossible_from_40_and_480():
    x=fresh('adversary')['equivariant_total_set_map_no_go']
    assert x['source_mod_27']==[13,21]
    assert x['target_cardinalities']['Schlaefli_directed_edges']==270
    assert x['minimum_discarded_points_for_free_subset_at_cardinality_level']==13
    assert x['minimum_discarded_directed_events_for_free_subset_at_cardinality_level']==21

@pytest.mark.parametrize('k,path',[
 ('symp','w33_20261015_toe92_full_symplectic_4mode.json'),
 ('key','w33_20261015_toe92_iid_cq_privacy.json'),
 ('optics','w33_20261015_toe92_optical_givens_mesh.json'),
 ('adversary','w33_20261015_toe92_herald_h27_nogo.json')
])
def test_frozen_certificate_roundtrip(k,path):
    assert fresh(k)==json.loads((ROOT/'data'/path).read_text(encoding='utf8'))
