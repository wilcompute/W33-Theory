"""W33 2026-10-09 round11 exact five-front research regressions."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_quantum_current_critical_ims_local_enclosure():
 import w33_20261009_local_coercivity_IMS_packet as m
 d=m.certificate()
 assert d['exact_energy_bound_at_radius_half']=='1/10'
 assert d['U_Gram_max']=='4+sqrt6'
 assert len(d['samples'])==4
def test_three_even_singlets_integer_gauge_charge_witness_scan():
 import w33_20261009_three_even_singlets_integer_search as m
 d=m.certificate()
 assert d['checked_distinct_triplets']==184
 assert len(d['triple_up_rank3_integer_witnesses'])==16
 assert d['total_solver_undecided']==0
 assert d['rank_histogram_from_positive_integer_witnesses']=={'1':168,'3':16}
def test_three_even_singlets_actual_corrected_R_nonR_necessary_filter():
 import w33_20261009_three_singlet_corrected_R_screen as m
 d=m.certificate()
 assert d['tested_triples']==16
 assert len(d['candidates_with_up_rank3_after_R'])==16
 assert d['unresolved_MILP']==0
 assert all(r['colored_rank_after_R_when_up_rank2plus']==7 for r in d['results'])
def test_PSp_full_group_irrep_characters_first15_and_second24_crossing():
 import w33_20261009_PSp_crossing_irreducibility as m
 d=m.certificate()
 assert d['projective_symplectic_group_order']==25920
 assert d['point_line_15_character_inner_product']=='0/25920'
 assert d['point_line_24_character_inner_product']=='25920/25920'
 assert d['first_15_crossing_character_equal_to_line15_for_checked_actions']==80
 assert d['both_irreducible_over_complex']
def test_burst_glitch_sampling_watchdog_information_bound():
 import w33_20261009_sentinel_watchdog_limits as m
 d=m.certificate()
 assert d['single_unbounded_corrupt_shot_requires_full_audit_at_0p1pct']
 assert d['one_unbounded_corrupt_shot_sentinel199_miss']==.005
 assert next(r for r in d['calibration_sentinel_requirements'] if r['corruptions_per_frame']==40 and r['coverage_model']=='all_frames_union')['minimum_independent_random_sentinels']==54
def test_topological_coupler_two_critical_points_onsite_tolerances():
 import w33_20261009_flatband_fabrication_tolerance as m
 d=m.certificate()
 assert d['exact_offcritical_band_dimension']==81
 assert d['critical_points']['first_kernel_dimension']==96
 assert d['critical_points']['second_kernel_dimension']==105
 assert len(d['samples'])==13
 assert d['correlated_vertex_weights_exact_81_band']
