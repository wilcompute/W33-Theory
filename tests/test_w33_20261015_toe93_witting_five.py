"""TOE93 five continuation audit: exact algebra and conditional optical/QKD models."""
from functools import lru_cache
from pathlib import Path
import json
import pytest
from analysis import w33_20261015_toe93_central_extension as C
from analysis import w33_20261015_toe93_conditional_key_ledger as K
from analysis import w33_20261015_toe93_mzi_bill as M
from analysis import w33_20261015_toe93_event_ready_herald as E
from analysis import w33_20261015_toe93_affine_H27_chain as H
ROOT=Path(__file__).resolve().parents[1]
@lru_cache(None)
def calc(t):
    return {'central':C.certificate,'key':K.certificate,'mzi':M.certificate,
            'herald':E.certificate,'H27':H.certificate}[t]()

def test_order_two_central_extension_witness_is_phase_gauge_invariant():
    d=calc('central')
    assert d['projective_40_ray_permutation_order']==25920
    assert d['projective_involutions_count']>100
    v=d['gauge_invariant_nontrivial_multiplier_witness']
    assert v['projective_permutations_commute']
    assert v['ququart_U4_lifts_anticommute']
    assert v['scalar_commutator']=='-1'
    assert v['commutator_max_numerical_residual_rounded']==0
    assert v['commutator_phase_rounded']==[-1.,0.]

def test_conservative_conditional_qkd_ledger():
    d=calc('key')
    assert d['block_length']==196
    assert d['single_error_Hamming_decoder_cases_verified']==896
    assert d['privacy_epsilon_used']==1e-6
    byv={v['visibility']:v for v in d['audit']}
    assert byv[.995]['illustrative_conditional_key_length_bits']==113
    assert byv[1.]['illustrative_conditional_key_length_bits']==169
    assert byv[.995]['public_hamming_syndrome_bits']==168
    assert byv[.995]['public_transcript_leak_upper']==185

def test_single_error_hamming_corrects_all_896_cases():
    assert K.test_single_error_decoder()==896
    for j in range(7):
        b=[int(i==j) for i in range(7)]
        s=K.xor_columns(b)
        for k in range(7):
            c=b[:];c[k]^=1
            assert K.correct_one_block(c,s)==b

def test_all_40_mzi_analyzers_have_verified_fourmode_factorizations():
    d=calc('mzi')
    assert d['setting_count']==40
    assert d['basis_MZI_counts']=={'0':1,'3':3,'4':3,'5':10,'6':23}
    assert d['MZI_upper_per_setting']==6
    assert d['balanced_50_50_couplers_upper_per_setting']==12
    assert d['worst_balanced_couplers_per_photon_path']==10
    assert d['all_40_reconstruction_error_max_rounded']==0
    assert d['pessimistic_two_photon_survival']==pytest.approx(.453840066101,abs=1e-11)
    assert all(row['balanced_couplers_count']==2*row['MZI_count'] for row in d['basis_circuits'])

def test_event_ready_all_herald_denominator_protects_against_balanced_attack():
    d=calc('herald')
    e=d['simulated_physical_channel']
    assert e['heralds_committed_before_basis_choice']==8192
    assert e['null_separable_per_herald_match_upper']==.4
    assert e['rejection_count_or_higher']==3415
    assert e['conditional_adaptive_separable_false_alarm_at_most']<=.001
    assert e['synthetic_independent_alternative_power']>.999
    control=d['selected_attacker_control']
    assert control['attacker_matched_fraction_given_acceptance']==1
    assert control['fraction_of_all_precommitted_heralds_accepted_and_matching']==pytest.approx(1/3)

def test_exact_parabolic_phi_is_Heisenberg_isomorphism():
    d=calc('H27')
    assert d['affine_points_not_perpendicular_to_polar_point']==27
    assert d['polar_hyperplane_points_perpendicular_to_polar_point']==13
    assert d['symplectic_Heisenberg_parabolic_subgroup_order']==27
    assert len(d['affine_ray_to_native_address'])==27
    assert set(tuple(x['H27_address']) for x in d['affine_ray_to_native_address'])==set(H.H)

def test_affine_W33_schlaefli_chain_boundary_and_H27_equivariance():
    d=calc('H27')
    assert d['W33_edge_partition']=={'affine_affine':108,'affine_polar':108,'polar_polar':24}
    assert d['directed_detector_substitution_admitted_affine_edges']==216
    assert d['directed_detector_substitution_erasure_outside_affine_edges']==264
    assert d['Schlaefli_edges']==135
    assert d['native_path_length_census_per_relative_generator']=={'1':2,'2':6}
    assert len(d['eight_relative_affine_graph_generators'])==8

@pytest.mark.parametrize('key,path',[
 ('central','w33_20261015_toe93_central_extension.json'),
 ('key','w33_20261015_toe93_conditional_key_ledger.json'),
 ('mzi','w33_20261015_toe93_mzi_bill.json'),
 ('herald','w33_20261015_toe93_event_ready_herald.json'),
 ('H27','w33_20261015_toe93_affine_H27_chain.json'),
])
def test_regenerate_frozen_certificates(key,path):
    assert calc(key)==json.loads((ROOT/'data'/path).read_text(encoding='utf8'))
