"""Independent reproducible regression checks for 2026-11-22 round-five TOE frontiers."""
import sys
from functools import lru_cache
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261122_round5_hessian_stage4_compiler as C
import toe_20261122_round5_e6_grade_leakage as E
import toe_20261122_round5_higgs_spinor_selection as H
import toe_20261122_round5_lorentzian_nulls as L
import toe_20261122_round5_18effect_optical as O
import toe_20261122_round5_optical_19_pareto as P

@lru_cache(None)
def result(name):
    return {'compiler':C,'e6':E,'higgs':H,'causal':L,'optics':O,'pareto':P}[name].verify()

def test_compiler_complete_exact_fourth_stage_count():
    d=result('compiler'); assert d['stage4_exact_left_H_cosets']==236359
    assert d['stage4_matrices']==153160632

def test_compiler_three_seeded_targets_exhaustive():
    x=result('compiler')['three_Haar_target_exhaustive_benchmarks']
    assert [round(r['projective_Frobenius_distance'],4) for r in x]==[.3364,.3638,.3876]
    assert x[0]['projective_Frobenius_distance']>x[0]['previous_exact_stage3_distance']
    assert all(x[i]['projective_Frobenius_distance']<x[i]['previous_exact_stage3_distance'] for i in (1,2))

def test_compiler_metric_packing_negative_control():
    p=result('compiler')['compact_diagonal_SU4_torus_packing']
    assert [z['strict_packing_obstruction'] for z in p]==[True,True,False]

def test_e6_grade_wedge_span_all_conjugate_27():
    d=result('e6'); assert d['rank_bracket_g1_wedge_g1_to_g2']==27

def test_e6_grade_adjoint_24_leakage_is_unavoidable():
    d=result('e6'); assert d['rank_bracket_g1_tensor_g2_to_g0']==24
    assert d['total_generated_e6_adjoint_dimension']==78 and d['necessary_adjoint_extra_directions']==51

def test_higgs_u1_cubic_spinor_selection():
    d=result('higgs');assert d['U1_neutral_fundamental_cubic_sectors']==['16*16*10','10*10*1']
    assert d['singlet_VEV_only_cubic_lifts_spinors'] is False

def test_higgs_64_spinors_and_conditional_cartan_escape():
    d=result('higgs');assert d['residual_quadratic_spinor_modes']==64
    assert d['adjoint_Cartan_escape']['spinor_coefficient']=='-3*a*lam'
    assert d['adjoint_Cartan_escape']['ten_coefficient']=='-6*a*lam'

def test_lorentzian_diamond_ordering_fraction_vs_two_layer():
    for row in result('causal')['test_sizes']:
        assert abs(row['sprinkled_Minkowski_diamond_mean']['ordering_fraction']-.5)<.05
        assert row['layered_counterexample']['maximum_chain_length']==2
        assert row['sprinkled_Minkowski_diamond_mean']['maximum_chain_length']>5

def test_lorentzian_interval_invariant_detects_null():
    for row in result('causal')['test_sizes']:
        assert row['layered_counterexample']['intervals_with_positive_interior']==0
        assert row['sprinkled_Minkowski_diamond_mean']['intervals_with_positive_interior']>0

def test_w33_orientation_degree_matched_null():
    r=result('causal')['W33_degree_matched_orientation_null']
    assert .7<r['ordering_fraction']['W33']<.9
    assert .7<r['ordering_fraction']['random_12_regular']<.9

def test_exact_18_and_19_witting_normalized_tight_frames():
    d=result('optics');assert d['exact_cyclotomic_identities']
    assert len(d['final_ray_indices'])==18 and len(d['nineteen_ray_indices'])==19
    assert len(d['overlap_six_rays'])==6

def test_exact_18_witting_modular_informational_completeness():
    assert all(x['union18']==16 and x['A']==12 and x['B']==12 and x['union19']==16 and x['C']==12 and x['D']==12 for x in result('optics')['six_finite_field_projector_ranks'])

def test_19_effect_dominates_20_in_tested_hardware_model():
    d=result('optics');l={x['design']:x for x in d['optical_designs']}
    assert l['19-effect']['gate_count']<l['20-effect']['gate_count']
    assert l['19-effect']['source_photon_HS_risk_coefficient']<l['20-effect']['source_photon_HS_risk_coefficient']
    assert l['19-effect']['detected_probability']>l['20-effect']['detected_probability']

def test_19_effect_has_better_exact_Haar_pure_average_risk_than_18_and_20():
    d=result('optics'); l={x['design']:x for x in d['optical_designs']}
    p=lambda name:l[name]['exact_Haar_pure_average_source_photon_HS_risk_coefficient']
    assert p('19-effect')<p('18-effect') and p('19-effect')<p('20-effect')

def test_18_effect_does_not_dominate_19():
    l={x['design']:x for x in result('optics')['optical_designs']}
    assert l['18-effect']['gate_count']<l['19-effect']['gate_count']
    assert l['18-effect']['source_photon_HS_risk_coefficient']>l['19-effect']['source_photon_HS_risk_coefficient']

def test_optical_loss_is_normalized_by_explicit_no_click_outcome():
    for x in result('optics')['optical_designs']:
        assert abs(x['detected_probability']+x['no_click_probability']-1)<1e-10
        assert x['source_photon_HS_risk_coefficient']>0

def test_19_optimize_mixture_weight_and_output_order():
    d=result('pareto');assert d['tested_output_row_orders']==81
    assert .45<d['bounded_weight_optimum_t']<.55
    assert d['best_tested_order']['gate_count']<=66
    assert d['best_tested_order']['source_photon_HS_risk_coefficient']<d['reference_half_half']['source_photon_HS_risk_coefficient']
