"""2026-10-09 Round13 W33 TOE exact/conditional research regression.

Core proofs are reproduced from SOURCE, not only frozen JSON.
PSp orbit test enumerates all 25920 group elements on 86400 flags,
quantum curvature certifies modular rank lower bounds, heterotic
tadpoles remain ONLY necessary-rule integer witnesses.
"""
import json,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_all160_cycle_weighted_lower_bound():
 import w33_20261009_all160_single_factor_dual_bounds as m
 d=m.certificate()
 assert d['representative_count']==160
 assert d['exact_rational_values_with_edge_counts']=={'25600/77571':160}
 assert F(d['rational_bound_min'])>F(33,100)
def test_all16_true_integer_correctedR_Ftadpole_screen():
 import w33_20261009_all16_heterotic_F_tadpoles as m
 d=m.certificate()
 assert d['candidate_supports']==16
 assert d['histogram_num_tadpole_possible_outsiders']=={'13':2,'15':2,'19':6,'21':6}
 assert all(x['n_F_tadpole_necessary_candidates']>0 for x in d['full_results'])
 assert d['full_results'][2]['candidate_mononomials'][0]['outside']=='n_81'
def test_quantum_full_curvature_rank_exact_lower_modular():
 import w33_20261009_quantum_curvature_fullrank_modp as m
 d=m.certificate()
 assert len(d['finite_field_rank_lower_bounds'])==3
 assert all(x['rank_skew2form_over_Fp']==16 for x in d['finite_field_rank_lower_bounds'])
 assert d['real_numerical_rank_tol_1e_minus_6']==16
def test_photonic_sham_observational_indistinguishability():
 import w33_20261009_optical_threeway_identifiability_nogo as m
 d=m.certificate()
 assert d['identical_raw_samples'] and d['identical_shot_clipped_samples']
 assert d['shots']==240000
def test_native_cycle_projector_exact_optimal_three_flag_selectors():
 import w33_20261009_canonical_triplet_isotropy_theorem as m
 d=m.certificate()
 assert d['exact_cycle_projector_rank']==81
 assert d['exact_optimal_unordered_three_flag_selectors']==86400
 assert d['global_min_eigenvalue_ratio_for_all_160_choose_3_triples']=='83/80'
 assert d['exact_cycle_projector_integer_levels']=={'-27':960,'-3':8640,'1':12960,'9':2880,'81':160}
def test_86400_three_flag_selector_full_PSp_five_orbit_decomposition():
 import w33_20261009_PSp_orbits_isotropic_triplets as m
 d=m.certificate()
 assert d['number_of_orbits']==5
 assert sorted(x['orbit_size'] for x in d['orbits'])==[4320,4320,25920,25920,25920]
 assert sorted(x['stabilizer_order'] for x in d['orbits'])==[1,1,1,6,6]
 assert all(x['induced_permutation_image_order']==3 and x['pointwise_triple_stabilizer_order']==2 for x in d['orbits'] if x['stabilizer_order']==6)
def test_exact_pointline_polarization_spectrum():
 import w33_20261009_weighted_flag_polarization_spectrum as m
 d=m.certificate()
 assert d['universal_flatband_dimension']==81
 assert d['endpoint_flatband_dimensions']==[120,120]
 assert all(x['numerical_vs_formula_maxerror']<1e-8 for x in d['samples'])
