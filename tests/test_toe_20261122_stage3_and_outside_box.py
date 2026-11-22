"""Independent 2026-11-22 six-front and KS negative-control regressions."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_stage3_hessian_exact as compiler
import toe_20261122_witting_qutrit_sic_mub30 as geometry
import toe_20261122_e6_higgs_tangent_and_center_gate as E6
import toe_20261122_causal_growth_finite_spectrum as causal
import toe_20261122_povm30_nai_mark_shot_cost as photonic
import toe_20261122_witting_KS_ovoid_firewall as contextuality

@lru_cache(None)
def c():return compiler.verify()
@lru_cache(None)
def g():return geometry.verify()
@lru_cache(None)
def e():return E6.verify()
@lru_cache(None)
def a():return causal.verify()
@lru_cache(None)
def p():return photonic.verify()
@lru_cache(None)
def ks():return contextuality.verify()


def test_third_stage_complete_exact_census():
    d=c();assert d['exact_third_stage_inequivalent_left_H_cosets']==12027
    assert d['exact_third_stage_distinct_complex_matrices']==7793496
    assert d['third_stage_raw_expressions']==12754584
    assert d['redundant_raw_expressions']==4961088


def test_third_stage_recovers_two_stage_and_no_bra_false_positives():
    d=c();assert d['stage2_recovery']['coset_count']==595
    assert d['stage2_recovery']['signature_bucket_count']==514
    assert d['stage3_coset_classification']['signature_bucket_count']==9478
    assert d['stage3_coset_classification']['coset_count']==12027


def test_third_stage_exhaustive_haar_benchmark():
    rows=c()['three_seeded_Haar_target_benchmarks']
    assert len(rows)==3
    for x,before in zip(rows,[.48196268,.55256014,.50925989]):
        assert x['projective_distance']<before
        assert x['primitive_word'].count('d')==3
        assert x['primitive_length']==len(x['primitive_word'])


def test_four_MUB_orthonormal_bases():
    d=g();assert d['blocked_qutrit_MUB_basis_partition']==[
       [1,5,33],[8,23,26],[11,14,24],[28,35,38]]
    assert d['exact_qutrit_MUB_cross_basis_squared_overlap']=='1/3'


def test_hesse_SIC_exact_projected_center_triples():
    d=g();assert len(d['H27_nine_center_fibers'])==9
    assert all(len(f)==3 for f in d['H27_nine_center_fibers'])
    assert d['exact_nine_SIC_projected_squared_overlap']=='1/4'


def test_MUB_SIC_affine_plane_parallel_classes():
    d=g();assert len(d['Hesse_affine_plane_MUB_zero_lines'])==12
    assert all(len(z)==3 for z in d['Hesse_affine_plane_MUB_zero_lines'].values())
    assert d['minimum_extra_blocked_orbit_sites_if_all27_positive']==3
    assert sorted(d['all_minimal_three_site_positive_supports'])==sorted(d['blocked_qutrit_MUB_basis_partition'])


def test_four_positive_30_outcome_30x4_isometries():
    d=g();assert d['reduced_effect_count']==30
    assert d['previous_effect_count']==39
    assert all(all(q==16 for q in z['all_four_30_effect_choices_rank']) for z in d['six_prime_rank_certificates'])
    assert len(d['Naimark_isometry_and_superoperator_spectra'])==5


def test_E6_Higgs_full_tangent_and_gauge_quotient():
    d=e();assert d['full_Higgs_complex_chiral_fields']==162
    assert d['driver_Fterm_Jacobian_rank']==5
    assert d['broken_complex_gauge_directions']==33
    assert d['unlifted_nonsinglet_Higgs_tangent_after_gauge_quotient']==124


def test_E6_charge_block_decomposition():
    d=e();assert d['components_left_unlifted_at_quadratic_order']=={
       '10_and_bar10':60,'spinors_after_goldstone_quotient':64}


def test_E6_81D_central_character_extension_no_go():
    d=e();assert d['center_eigenspace_dimensions']=={'1':27,'omega':27,'omega_squared':27}
    assert d['whole_source_H27_invariant_dimension']==3
    assert d['E6_81D_extension_with_identified_center_exists'] is False
    assert d['necessary_dimension_for_any_center_compatible_nontrivial_E6_supermodule']==132


def test_growing_W33_graphs_and_24_120_720_5040_causal_states():
    d=a();assert [x['number_of_total_order_states'] for x in d['nested_W33_induced_graphs']]==[24,120,720,5040]
    assert all(x['first_excitation_gap']>0 for x in d['nested_W33_induced_graphs'])


def test_growing_reversible_causality_no_arrow():
    d=a();assert all(abs(x['reversal_odd_ground_state_expectation'])<1e-11
                     for x in d['nested_W33_induced_graphs'])
    assert all(x['ground_state_residual_norm']<1e-10 for x in d['nested_W33_induced_graphs'])


def test_photonic_30_and_39_Naimark_full_unitary_completions():
    d=p();rows=d['design_comparison'];assert rows[0]['outcome_count']==39
    assert all(r['outcome_count']==30 for r in rows[1:])
    assert rows[0]['generic_full_mesh_two_mode_cells']==741
    assert all(r['generic_full_mesh_two_mode_cells']==435 for r in rows[1:])
    assert all(r['Naimark_isometry_deviation']<1e-11 for r in rows)


def test_photonic_statistical_risk_and_calibration_floor():
    d=p();rows=d['design_comparison']
    assert rows[0]['expected_linear_inversion_HS_MSE_times_detected_shot_count']['seeded_generic_pure']<rows[1]['expected_linear_inversion_HS_MSE_times_detected_shot_count']['seeded_generic_pure']
    assert abs(d['hypothetical_infinite_shot_pure_state_trace_distance_bias']-0.0075)<1e-12


def test_40_40_Witting_KS_full_context_uncolorable():
    d=ks();assert d['orthogonal_complete_bases']==40
    assert d['exact_cover_ovoid_exists'] is False
    assert d['exhaustive_dynamic_programming_distinct_states']==65


def test_KS_parity_only_no_go_and_explicit_parity_valuation():
    d=ks();assert d['GF2_context_point_incidence_rank']==25
    assert d['GF2_augmented_with_context_parity_rank']==25
    assert d['parity_only_context_proof_exists'] is False
    assert len(d['explicit_12_ray_parity_odd_transversal'])==12
