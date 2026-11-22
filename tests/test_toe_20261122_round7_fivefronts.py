"""Independent round-seven mathematical and engineering regression tests."""
from functools import lru_cache
import json
from pathlib import Path
import numpy as np

import toe_20261122_round7_mic_orbits as A
import toe_20261122_round7_mic_optics_symmetry as O
import toe_20261122_round7_h27_subsystem_code as Q
import toe_20261122_round7_h27_mediator_vacuum as H
import toe_20261122_round7_w33_three_layer_hasse as C
import toe_20261122_round7_coordinate_compiler as G
import toe_20261122_round6_beam_compiler as B

ROOT=Path(__file__).resolve().parents[1]

def cert(name):return json.loads((ROOT/'data'/('toe_20261122_round7_'+name+'.json')).read_text())

@lru_cache(None)
def orbit():return A.verify()
@lru_cache(None)
def optic():return O.verify()
@lru_cache(None)
def code():return Q.verify()
@lru_cache(None)
def vac():return H.verify()
@lru_cache(None)
def causal():return C.verify()

def test_mic_group_648():
    d=orbit();assert d['hessian_group_order']==648
    assert d['support_orbit_size']==648 and d['weighted_povm_orbit_size']==648

def test_mic_stabilizers_and_exact_Gram():
    d=orbit();assert d['support_stabilizer_order']==d['weighted_povm_stabilizer_order']==1
    assert d['exact_seed_Gram_determinant']=='25/59049'
    assert d['support_composition_in_1_12_27_ray_orbits']=={'12':5,'27':11}

def test_all_orbit_supports_ic_and_normalized():
    d=orbit();assert d['all_transported_supports_rank16'] and d['all_transported_weighted_povms_normalized']
    assert d['max_floating_point_identity_error']<1e-12

def test_sparse_optic_51_gates():
    d=optic();assert d['tested_POVM_designs']==648
    assert d['minimize_gate_count_then_maximize_survival']['gates']==51
    assert d['baseline']['gates']==54

def test_optic_survival_and_risk_tradeoff():
    d=optic();b=d['baseline'];g=d['minimize_gate_count_then_maximize_survival']
    assert g['survival']>b['survival']
    assert g['Haar_average_source_photon_risk_coefficient']>b['Haar_average_source_photon_risk_coefficient']
    assert d['gate_histogram']=={'51':3,'52':8,'53':19,'54':618}

def test_h27_tensor_factorization():
    d=code();assert d['logical_code_dimension']==9 and d['physical_dimension']==27
    assert d['H27_projective_errors']==9
    assert max(d['tensor_residuals'].values())<1e-12

def test_h27_Knill_Laflamme_all_pairs():
    d=code();assert d['KL_max_abs_residual']<2e-12
    assert len(d['KL_coefficient_matrix'])==81
    assert d['nine_error_mixture_recovered_density_max_abs_residual']<2e-12

def test_e6_full_error_algebra_not_mistaken_for_H27_noise():
    d=code();assert 'full compact E6' in d['full_E6_no_go']
    assert 'not arbitrary E6' in d['restricted_error_scope']

def test_h27_mediator_F_flat_and_Hessian():
    d=vac();assert d['root_F_terms_zero']
    assert d['full_15x15_Hessian_rank']==14
    assert d['mediator_Hessian_rank']==8
    assert d['effective_7x7_Hessian_rank']==6

def test_higgs_only_gauge_zero_mode_in_singlet_slice():
    d=vac();assert d['residual_singlet_moduli_after_gauge_quotient']==0
    assert d['gauge_complex_zero_mode']==[1,0,0,-1,0,0,0]
    assert len(d['mediator_modes'])==8

def test_w33_sharp_80_edge_height_three():
    d=causal();assert d['minimum_deleted_edges_proven_prior']==80
    assert d['three_layer_poset']['longest_chain']==3
    assert d['three_layer_poset']['comparable_pairs']==260
    assert d['three_layer_poset']['interval_interior_histogram']=={'0':160,'2':40,'3':32,'4':28}

def test_w33_sharp_four_layer_BFS():
    d=causal();assert d['four_layer_vertex_distribution']==[1,8,19,12]
    assert d['four_layer_Hasse_covers']==160
    assert d['four_layer_poset']['longest_chain']==4
    assert d['four_layer_poset']['comparable_pairs']==287
    assert d['four_layer_poset']['interval_interior_histogram']=={'0':160,'2':49,'3':36,'4':30,'16':12}

def test_causal_Minkowski_negative_control():
    d=causal();m=d['seeded_40event_1plus1_Minkowski_diamond_control']
    assert m['longest_chain']==10 and m['comparable_pairs']==415
    assert m['ordering_fraction']>d['four_layer_poset']['ordering_fraction']

def test_compiler_constructed_two_stage_target():
    gates=B.build_gates();h,n,phase,*_=gates
    U=h[143]@phase@n[3]@phase@n[5]
    rows=B.compile(U,depth=2,width=128,gates=gates)
    assert rows[-1]['distance']<1e-7

def test_compiler_frozen_random_target_diagnostics():
    d=cert('coordinate_compiler');assert d['depth']==12 and d['known_two_stage_witness_error']<1e-7
    assert len(d['targets'])==3
    for t in d['targets']:
        assert t['refined']['distance']<=t['beam_initial_distance']+1e-11
        assert len(t['refined']['normal_indices'])==12
        assert t['refined']['primitive_word_length']>0
    assert any(t['refined']['distance']>.40 for t in d['targets'])

def test_all_producer_frozen_statuses():
    names=['mic_orbits','mic_optics_symmetry','h27_subsystem_code','h27_mediator_vacuum','w33_three_layer_hasse','coordinate_compiler']
    for name in names:
        obj=cert(name);assert obj['status'].startswith('PASS_')
