"""Independent new five-front and binary tetrahedral coset compiler regressions."""
from __future__ import annotations
import sys
from functools import lru_cache
from pathlib import Path
import numpy as np
from sympy import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_next5_compiler_photonics as comp
import toe_20261122_next5_hessian_coset_compiler as coset
import toe_20261122_next5_h27_explicit_intertwiner as h27
import toe_20261122_next5_causal_dynamics as causal
import toe_20261122_next5_e6_susy_flat_branch as susy
import toe_20261122_next5_photonic_calibration_entangler as photon

@lru_cache(maxsize=None)
def corpus():return (comp.verify(),coset.verify(),h27.verify(),causal.verify(),susy.verify(),photon.verify())

def test_four_fixed_witting_units():
    for a,U in comp.gates().items():
        assert np.linalg.norm(U.conj().T@U-np.eye(4))<1e-12,(a,U)

def test_bounded_depth_compiler_dedup_corrected():
    d=corpus()[0]
    assert d['search_statistics'][-1]['cumulative_projective_words']==1675
    assert d['synthetic_target_shortest_up_to_depth']['projective_distance']<1e-10
    assert len(d['haar_target_projective_distances_by_depth'])==3

def test_bounded_depth_compiler_honest_negative_controls():
    d=corpus()[0]
    assert min(b[-1] for b in d['haar_target_projective_distances_by_depth'])>.7
    assert d['noise'][0]['mean_conditional_average_gate_fidelity']>1-1e-12
    assert d['noise'][-1]['mean_conditional_average_gate_fidelity']<.999

def test_exact_hessian_ray_stabilizer_is_24_binary_tetrahedral():
    d=corpus()[1]
    assert d['Hessian_mirror_subgroup_order']==648
    assert d['intersection_order']==24
    assert d['intersection_derived_subgroup_order']==8
    assert d['intersection_element_order_profile']=={1:1,2:1,3:8,4:6,6:8}
    assert d['H27_intersection_trivial'] is True

def test_six_prime_Hessian_double_coset_certificates():
    d=corpus()[1]
    assert d['double_coset_H_D_H_cardinality']==17496
    assert d['exact_search_work_reduction']==24
    assert len(d['exact_finite_field_certificates'])==6
    assert all(p['intersection_count']==24 for p in d['exact_finite_field_certificates'])

def test_optimized_coset_compiler_matches_bruteforce():
    d=corpus()[1]
    assert len(d['global_phase_insensitive_haar_benchmarks'])==3
    for i,b in enumerate(d['global_phase_insensitive_haar_benchmarks']):
        assert b['best_single_D_HDH_projective_distance']<=d['shallow_depth5_baseline'][i]
        assert b['searched_distinct_product_representatives']==17496

def test_H27_explicit_coisometry_and_generators():
    d,T=h27.build()
    assert T.shape==(27,81)
    assert d['maximal_intertwining_frobenius_error']<1e-10
    assert np.linalg.norm(T@T.conj().T-np.eye(27))<1e-10
    P=T.conj().T@T
    assert np.linalg.norm(P@P-P)<1e-10

def test_H27_27_to_27_no_go_minimal_regular_copy_lift():
    d=corpus()[2]
    assert d['one_regular_copy_max_equivariant_rank']==9
    assert d['minimal_source_dimension_in_uniform_regular_copy_class']==81
    assert d['kernel_dimension']==54

def test_causal_W33_nonuniqueness_and_automorphism_invariance():
    d=corpus()[3]
    assert d['canonical_initial_order']!=d['seeded_alternative_order']
    assert d['automorphism_relabel_invariant'] is True
    assert d['vertices']==40 and d['edges']==240

def test_causal_exact_detailed_balance_and_global_dag():
    d=corpus()[3]
    assert d['small_cycle_exact_partition_control']['total_orders']==24
    assert d['small_cycle_exact_partition_control']['exact_detailed_balance_verified']
    assert 0<d['metropolized_chain']['acceptance_rate']<1
    assert d['metropolized_chain']['final']['chain_height']<=40

def test_E6_F_D_flat_cubic_and_full_rank_exotic_masses():
    d=corpus()[4]
    assert d['U1_D']==0
    assert all(x=='0' for x in d['explicit_F_terms'])
    assert d['exotic_mass_determinant']==-66
    assert len(d['exotic_mass_singular_values'])==3
    assert d['matter_16_survivors']==3

def test_E6_family_breaks_without_fixing_moduli_or_hierarchy():
    d=corpus()[4]
    assert d['H27_broken_in_vacuum'] is True
    assert d['singlet_branch_unlifted_complex_moduli_dimension']==4
    assert susy.H_family()[0,0,0]==2
    assert susy.H_family()[0,1,2]==1
    assert susy.H_family()[0,0,1]==0

def test_photonic_intensity_only_incomplete_tomography():
    d=corpus()[5]
    assert d['intensity_measurement_identical_max_abs_error']<1e-12
    assert abs(d['channel_average_gate_fidelity']-.85)<1e-12
    assert abs(d['phase_referenced_superposition_test']['shifted_plus_probability']-.75)<1e-12

def test_photonic_dual_rail_no_deterministic_entangler():
    d=corpus()[5]
    p=[x['total_leakage'] for x in d['actual_witting_gate_dual_rail_leakage']]
    assert max(abs(p[i]-v) for i,v in enumerate((7/9,7/9,1/3,1/3)))<1e-12
    assert d['idealized_shot_budgets'][2]['shots_for_at_least_95pct_detection_ideal_SPAM']==1198

import toe_20261122_next5_h27_exact_matrix as h27exact
import toe_20261122_next5_phase_site_classification as sites

def test_exact_integer_pair_Witting_to_operator_H27_243_sparse_entries():
    d=h27exact.verify()
    assert d['exact_Eisenstein_integer_pair_checks'] is True
    e,_,_,orbit,*_=h27exact.exact_exponent_matrix()
    assert e.shape==(9,27)
    assert np.count_nonzero(e>=0)==81
    assert len(orbit)==27

def test_six_split_prime_sparse_H27_intertwiner_coisometry():
    d=h27exact.verify()
    assert len(d['six_finite_field_certificates'])==6
    assert all(x['T27x81_nonzeros']==243 and x['coisometry_rank']==27
               for x in d['six_finite_field_certificates'])

def test_all_Witting_pi_phase_sites_exhaustive_27_12_1():
    d=sites.verify()
    assert d['dense_site_count']==27
    assert d['block_site_count']==12
    assert d['fixed_site_count']==1
    assert d['dense_SU4_pi_sites']+d['block_preserving_nonuniversal_pi_sites']!=[]
    assert set(d['dense_SU4_pi_sites'])|set(d['block_preserving_nonuniversal_pi_sites'])|{d['finite_nonuniversal_pi_site']}==set(range(40))

def test_Witting_ray25_finite_phase_group_and_orthogonal_split():
    d=sites.verify()
    assert d['unique_fixed_orthogonal_line_ray']==25
    assert d['finite_ray25_group_order']==1296
    assert d['fixed_line_orthogonal_to_three_generators']
