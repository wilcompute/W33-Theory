"""Rigorous/falsifying certificates for 2026-11-22 Witting/W33/E6 round six."""
from pathlib import Path
import sys
from functools import lru_cache
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261122_round6_16effect_optimal as IC
import toe_20261122_round6_optical16 as OPT
import toe_20261122_round6_causal_graph_no_go as CAUS
import toe_20261122_round6_e6_twirl_noiseless as TWI
import toe_20261122_round6_e6_higgs_flat_branch as HIG
import toe_20261122_round6_beam_compiler as BEAM
import toe_20261122_round6_local_refine as LOCAL

@lru_cache(None)
def ic():return IC.proof()
@lru_cache(None)
def optical():return OPT.verify(ntries=12)
@lru_cache(None)
def causal():return CAUS.verify()
@lru_cache(None)
def twirl():return TWI.verify()
@lru_cache(None)
def higgs():return HIG.verify()
@lru_cache(None)
def refined():return LOCAL.verify()

def test_sixteen_exact_positive_normalized_povm():
    d=ic();assert len(d['indices'])==16 and len(d['heavy_indices'])==4
    assert sorted(set(d['weights'].values()))==['1/5','2/5'] and d['exact_normalization']

def test_sixteen_exact_nonzero_rational_gram_determinant():
    d=ic(); assert d['exact_projector_Gram_determinant']=='25/59049'
    assert d['exact_Gram_entry_histogram']=={'1':16,'0':90,'1/3':150}

def test_sixteen_six_independent_modular_ranks():
    assert [r for p,r in ic()['finite_field_ranks']]==[16]*6

def test_sixteen_dimension_is_global_ic_lower_bound():
    assert len(ic()['indices'])==4**2
    assert 40>len(ic()['indices']) and ic()['condition']<49

def test_sixteen_nai_mark_isometry_and_calibrated_no_click():
    d=optical();x=d['baseline'];assert x['gate_count']==54
    assert abs(x['detected_probability']+x['no_click_probability']-1)<1e-10
    assert .93<x['detected_probability']<.98

def test_sixteen_optical_hardware_vs_estimation_tradeoff():
    d=optical();assert 45<d['baseline']['haar_pure_average_source_photon_HS_risk_coefficient']<48
    assert d['best']['haar_pure_average_source_photon_HS_risk_coefficient']<=d['baseline']['haar_pure_average_source_photon_HS_risk_coefficient']

def test_w33_triangle_obstruction_and_srg_identity():
    d=causal();assert (d['vertices'],d['edges'],d['triangles'])==(40,240,160)
    assert d['triangles_per_edge']==2 and d['exact_adjacency_identity']=='A^2=8I-2A+4J'

def test_w33_optimal_maxcut_and_rank_two_hasse_repair():
    d=causal();assert d['spectral_max_cut_upper_bound']==160
    assert d['crossing_edges']==160 and d['deleted_edges']==80
    assert d['crossing_degree_per_vertex']==8 and d['cut_parts']==[20,20]
    assert d['minimum_deleted_edges_for_Hasse_realization']==80

def test_full_e6_twirl_schur_irrep_count_and_zero_address_information():
    d=twirl();assert d['twirl_fixed_operator_complex_dimension']==3
    assert d['address_basis_state_count']==81 and d['twirled_basis_outputs_identical']
    assert abs(sum(d['each_address_basis_block_populations'])-1)<1e-12

def test_e6_flat_adjoint_singlet_F_D_conditions():
    d=higgs();assert d['F_gradient_all_zero'] and d['D_terms_zero_on_conjugate_singlet_ansatz']
    assert d['trace_Q_squared']==72 and d['holomorphic_pairing_s']=='9*M*m/(2*lam**2)'

def test_e6_family_symmetry_leaves_four_complex_moduli():
    d=higgs();assert d['F_jacobian_rank']==2
    assert d['complex_ungauged_flat_tangent']==5
    assert d['remaining_complex_flat_moduli']==4

def test_beam_first_two_stages_against_previous_exact_census():
    import scipy.stats
    G=BEAM.build_gates(); rng=np.random.default_rng(20261122)
    U=scipy.stats.unitary_group.rvs(4,random_state=rng)
    rows=BEAM.compile(U,depth=2,width=81,gates=G)
    assert abs(rows[0]['distance']-.6572693468903162)<1e-8
    assert abs(rows[1]['distance']-.4819626758729542)<1e-8
    assert rows[0]['tested']==27 and rows[1]['tested']==729

def test_refined_compiler_reconstructs_better_target_specific_words():
    d=refined();assert len(d['targets'])==3
    for row in d['targets']:
        assert row['refined8']<=row['beam8']+1e-9
        assert row['tested_initial_paths']==81
    assert d['targets'][2]['refined8']<.38
