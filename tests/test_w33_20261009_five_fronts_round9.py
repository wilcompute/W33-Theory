"""Seven independent executable regressions for W33 TOE round9."""
import sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
def test_critical_half_sobolev_constant_optimized_upper_ceiling():
 import w33_20261009_critical_sobolev_ceiling as m
 d=m.certificate()
 assert abs(d['optimized_critical_halfSobolev_constant_upper_numeric']-43.43570974418893)<1e-8
 assert d['eigenspace_multiplicity']==24
 assert d['intersection_with_active_transport_null_dimension_at_least']>=20
 assert d['normV_square']==d['normU_square']
def test_pure_anti_baryon_five_alternative_hidden_SU4_Dflat():
 import w33_20261009_antibaryon_Dflat_mass_scan as m
 d=m.certificate()
 assert d['antibaryon_supports']==5
 assert d['exact_mass_entries_screened']==395
 assert d['best_up_rank']==1 and d['worst_colored_mass_rank']==5
def test_mixed_2mesons_antibaryon_60_Dflat_necessary_masks():
 import w33_20261009_SU4_mixed_baryon_mesons as m
 d=m.certificate()
 assert d['candidate_Dflat_supports']==60
 assert d['real_cone_masks']==4740
 assert d['maximum_up_rank']==3 and d['maximum_colored_rank']==5
 assert d['histogram_up_colored_rank']=={'(1, 5)':18,'(3, 5)':42}
def test_all_4740_lp_masks_reproduced_by_exact_rational_vertices():
 import w33_20261009_SU4_mixed_baryon_exact_4740 as m
 d=m.certificate()
 assert d['exact_fraction_vertex_checks']==4740
 assert d['complete_agreement_with_independent_scipy_masks']
 assert d['rank3_up_candidates']==42 and d['maximum_colored_rank']==5
def test_Gershgorin_interval_certified_fullH_235_eigenvalue_ladder():
 import w33_20261009_fullH_symmetry_minmax_ladder235 as m
 d=m.certificate()
 assert int(F(d['fullH_E235_upper']))==182
 assert d['fullH_minmax_ladder'][-1]['fullH_ordered_eigenvalue_index']==235
 assert len(d['fullH_minmax_ladder'])==13
 assert all(x['gershgorin_min_margin']>0 for a in d['exact_Gershgorin_certificates'].values() for x in a)
def test_optical_zero_glitch_calibration_count_and_union_error():
 import w33_20261009_photonic_glitch_calibration_plan as m
 d=m.certificate()
 assert d['minimum_zero_glitch_calibration_samples']==69021
 assert abs(d['combined_false_positive_limit']-.01)<1e-12
 assert d['independent_calibration_designs'][-1]['count_budget_approved']
 assert not d['independent_calibration_designs'][0]['count_budget_approved']
def test_dual_coupler_exact_half_ground_band_threshold_and_correlated_gap():
 import w33_20261009_correlated_disorder_dual_couplers as m
 d=m.certificate()
 assert d['exact_midpoint_rank64']
 assert d['ground_degeneracy_at_crossing']==96
 assert d['additional_zero_modes_at_crossing']==15
 assert d['ground_crossing_exact_fraction']=='1/2'
 assert d['protected_H1_dimension']==81
 assert all(x['numerical_first_above_flat_band_gap']>=x['rigorous_weighted_lower_gap']-1e-9 for x in d['local_weight_disorder'])
