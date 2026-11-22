"""Six independent constructive Witting / E6 / causal / optical falsifier fronts.

The previous 42 tests are independently executable; this module adds 16
source-specific regressions over algebraic and statistical results.
"""
from __future__ import annotations
import sys
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_further_two_D_exact as two
import toe_20261122_further_e6_cubic_pullback as cubic
import toe_20261122_further_quantum_causal_arrow as causal
import toe_20261122_further_e6_isolated_singlet as vacuum
import toe_20261122_further_photonic_quadrature_fisher as photons
import toe_20261122_further_control_observation_duality as tomography

@lru_cache(None)
def data(name):
    return dict(two=two,cubic=cubic,causal=causal,vacuum=vacuum,
                photons=photons,tomography=tomography)[name].verify()

def test_exact_two_D_integer_cyclotomic_census():
    d=data('two')['exact_cyclotomic_enumeration']
    assert d['first_D_stage_unique_matrices']==17496
    assert d['second_D_stage_raw_words']==472392
    assert d['second_D_stage_exact_unique_matrices']==385560
    assert d['same_word_collision_excess']==86832
    assert d['common_cyclotomic_denominator_second_stage']==243

def test_exact_two_D_set_hash_and_shortwords():
    d=data('two')['exact_cyclotomic_enumeration']
    assert d['exact_second_stage_matrix_set_sha256']=='e50c2d9c40d10e05a63b807f938a05443178b79c6963061c25ed4834f93bde42'
    assert d['H_inside_two_D'] is True

def test_two_D_haar_target_benchmarks_nonincreasing_distance():
    d=data('two')['benchmark_results']
    assert len(d)==3
    assert all(x['two_D_best_projective_Frobenius']<=x['one_D_best_projective_Frobenius'] for x in d)
    assert all(x['two_D_best_projective_Frobenius']<.56 for x in d)

def test_E6_pullback_9x27_exact_sparse_chart():
    d=data('cubic')
    assert len(d['output_chart_canonical_to_raw'])==27
    assert d['sparse_matrix_nonzeros']==243
    assert d['cubic_radical_dimension']==54
    assert d['exact_modular_cubic_checks'][0]['nonzero_determinant_witness']==1

def test_E6_cubic_H27_covariance_six_primes():
    d=data('cubic')
    assert len(d['exact_modular_cubic_checks'])==6
    assert all(c['H27_cubic_covariant'] and c['samples_checked']==40 for c in d['exact_modular_cubic_checks'])

def test_causal_quantization_stochastic_ground_state():
    d=data('causal')
    assert d['state_count']==24
    assert d['exact_detailed_balance']
    assert d['gap_positive'] and d['spectral_gap']>.17

def test_causal_time_reversal_arrow_obstruction():
    d=data('causal')
    assert d['graph_automorphism_group_order']==8
    assert d['reversal_commutator_norm']<1e-12
    assert d['reversal_odd_order_parameter_expectation']==0

def test_E6_isolated_singlet_jacobian_minors():
    d=data('vacuum')
    assert d['original_singlet_moduli']==4
    assert d['added_E6_singlet_H27_character_drivers']==4
    assert d['holomorphic_F_constraint_jacobian_rank']==5
    assert d['residual_local_complex_singlet_moduli']==0
    assert len(d['algebraic_certificates']['Jacobian_5x5_minors'])==6

def test_E6_H27_character_symmetry_Dflat_six_primes():
    d=data('vacuum')
    assert len(d['finite_field_certificates'])==6
    assert all(r['Jacobian_rank']==5 and r['H27_characters_verified'] for r in d['finite_field_certificates'])
    assert d['all_E6_D_terms_zero_at_vectorlike_conjugate_pair']

def test_E6_exotics_do_not_yet_give_3_distinct_masses():
    d=data('vacuum')
    assert d['algebraic_certificates']['mass_squared_eigenvalues']==[4,7,7]
    assert d['algebraic_certificates']['matter_10_mass_determinant_norm_sq']==196

def test_photon_quadrature_approaches_QFI():
    d=data('photons')
    assert .95<d['Fisher_information_per_detected_photon_at_zero']<1
    assert d['ideal_quantum_Fisher_information_per_photon']==1

def test_photon_readout_18fold_gain_with_calibrated_SPAM():
    d=data('photons')
    x=d['measured_shot_budget_rows'][0]
    assert x['X']['detected_photons']==20823
    assert x['Y']['detected_photons']==1151
    assert x['detected_shot_reduction_ratio']>18
    assert x['X']['actual_typeI_error']<=.05 and x['Y']['actual_statistical_power']>=.95

def test_photon_binomial_controls_every_phase_angle():
    d=data('photons')
    for q in d['measured_shot_budget_rows']:
        for setting in ('X','Y'):
            assert q[setting]['actual_typeI_error']<=.05+1e-12
            assert q[setting]['actual_statistical_power']>=.95
            assert q[setting]['input_pulses_lower_ceil']>=q[setting]['detected_photons']

def test_Witting_universal_control_projectors_not_IC():
    d=data('tomography')
    assert len(d['universal_phase_sites'])==27
    assert d['dimensions']['universal_orbit_span']==15
    assert d['affine_state_tomography_with_known_trace_is_complete'] is True
    assert d['dimensions']['universal_orbit_plus_trace_span']==16
    assert d['unnormalized_operators_half_trace_norm_distance']==5/16

def test_Witting_blocked_sites_complete_39_effect_IC_POVM():
    d=data('tomography')
    assert len(d['nonuniversal_orthogonal_sites'])==12
    assert d['dimensions']['all39_span']==16
    assert len(d['modular_certificates'])==6
    assert all(c['tight_POVM_in_normalized_field'] for c in d['modular_certificates'])

def test_any_single_blocked_ray_repairs_tomography_rank():
    d=data('tomography')
    assert all(c['each_blocked_ray_repairs_linear_observation'] for c in d['modular_certificates'])
