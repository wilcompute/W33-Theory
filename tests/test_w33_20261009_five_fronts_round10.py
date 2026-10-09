"""W33 TOE round10: five independent physics/mathematics fronts.
Recreates all results from source or exact frozen metadata.
Tests no artificial missing tool assumptions and preserve prior ownership.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
def test_full_H_local_pointwise_form_lower_potential():
 import w33_20261009_pointwise_fullH_lower_potential as Q
 d=Q.certificate()
 assert d['exact_at_q_origin']=='V_C(0)=V_opt(0)=160*a^4=2/5'
 assert d['samples'][0]['optimal_barrier_numerical']>.399999999
 assert d['samples'][1]['optimal_barrier_numerical']<1e-8
 assert all(r['optimal_barrier_numerical']+1e-8>=r['naive_barrier'] for r in d['samples'])
def test_351_new_two_true_even_singlet_cones():
 import w33_20261009_two_even_singlets_mass_scan as Q
 d=Q.certificate()
 assert d['n_available_even_true_singlets']==27
 assert d['two_field_extensions']==351
 assert d['necessary_entry_tests']==27729
 assert d['rank_histogram']=={'(1, 5)':168,'(1, 6)':68,'(1, 7)':107,'(3, 7)':8}
def test_27729_independent_exact_rational_singlet_masks():
 import w33_20261009_two_even_singlets_exact_27729 as Q
 d=Q.certificate()
 assert d['all_HiGHS_masks_exactly_reproduced']
 assert d['exact_rational_entry_checks']==27729
 assert len(d['exact_double_rank_repair_pairs'])==8
def test_eight_pairs_integer_monomial_degree24():
 import w33_20261009_two_singlet_exact_degree24_integer_gate as Q
 d=Q.certificate()
 assert d['integer_rank_histogram']=={'(1, 7)':8}
 assert len(d['exact_integer_exponent_candidate_pairs'])==8
def test_eight_pairs_all_order_integer_gauge_semigroup():
 import w33_20261009_two_singlet_all_order_integer_semigroup as Q
 d=Q.certificate()
 assert d['rank_histogram_unbounded_integer_semigroup']=={'(1, 7)':8}
 assert all(len(p['integer_charged_gauge_mononomial_witnesses'])==31 for p in d['results'])
def test_trivial_PSp_symmetry_fullH_spectral_measure():
 import w33_20261009_PSp_trivial_spectral_measure as Q
 d=Q.certificate()
 assert d['gaussian_exact_eigenstate'] is False
 assert d['spectral_windows'][0]['approximate_lower']>95
 assert d['spectral_windows'][0]['approximate_upper']<163
 assert d['spectral_windows'][1]['guaranteed_spectral_weight_at_least']=='3/4'
def test_cluster_randomization_guard_against_burst_corruptions():
 import w33_20261009_frame_randomization_burst_guard as Q
 d=Q.certificate()
 assert d['total_shots']==240000 and d['independent_randomized_frames']==1200
 assert d['simulation']['null_adversarial_single_bad_frame']['rejects']<=3
 assert d['simulation']['quartic_proxy_single_bad_frame']['rejects']>=18
def test_exact_second_topology_band_crossing_at_sqrt10():
 import w33_20261009_exact_second_flatband_crossing as Q
 d=Q.certificate()
 assert d['generalized_eigenvalue_multiplicities']['3-sqrt10']==24
 assert d['generalized_eigenvalue_multiplicities']['-1']==15
 assert d['zero_eigenvalue_dimensions_at_critical']['t=(sqrt10+2)/6']==105
 assert d['negative_eigenvalue_counts_of_A_t_plus_2']['(sqrt10+2)/6<t<=1']==39
