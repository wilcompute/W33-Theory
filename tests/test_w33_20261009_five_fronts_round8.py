"""Seven independently executable W33 TOE frontier checks, round 8."""
from pathlib import Path
from fractions import Fraction as F
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
def test_quantum_global_subelliptic_exponent_obstruction():
 import w33_20261009_sobolev_exponent_half_no_go as s
 d=s.certificate()
 assert d['all_s_strictly_greater_than_half_excluded']
 assert d['gaussian_packet_exact_H']==['1599/5','1681/10','39/5']
 assert len(d['powers'])==4
 assert d['powers'][-1]['samples'][-1]['upper_ratio_H_over_Sobolev_lower']<.01
def test_30_conjugate_pair_Su4_relaxed_masks():
 import w33_20261009_SU4_pair_meson_mass_masks as m
 d=m.certificate()
 assert d['candidates']==30
 assert d['best_relaxed_up_rank']==3 and d['best_relaxed_colored_rank']==5
 assert sum(x['up_relaxed_matching_rank']==3 for x in d['distinct_candidates'])==18
def test_independent_exact_rational_2370_cone_checks():
 import w33_20261009_SU4_pair_masks_exact_rational as r
 d=r.certificate()
 assert d['independent_exact_rational_entry_checks']==2370
 assert d['all_numerical_real_cone_masks_exactly_confirmed']
 assert d['candidates_rank3']==18 and d['max_colored_rank']==5
def test_actual_full_H_minmax_25th_55th_upper_bounds():
 import w33_20261009_fullH_minmax_25_55_bounds as m
 d=m.certificate()
 assert F(d['full_H_minmax_25th_eigenvalue_upper'])<F('142.435')
 assert F(d['full_H_minmax_55th_eigenvalue_upper'])<F('143.464')
 assert d['guaranteed_number_of_actual_eigenvalues_below_143_464']==55
def test_finiteN_adversarial_unbounded_spikes_but_bounded_count():
 import w33_20261009_bounded_sparse_glitch_optics as m
 d=m.certificate()
 assert d['max_unbounded_glitches']==40
 assert d['samples_per_trial']==240000
 assert d['simulation']['null_with_arbitrary_sign_glitches']['rejects']<=4
 assert d['simulation']['quartic_signal_with_glitches']['rejects']>=12
def test_native_line_and_triple_heat_spectral_dimension():
 import w33_20261009_native_selector_spectral_dimension as m
 d=m.certificate()
 assert d['line_context']['diameter']==2
 assert d['collinear_triples']['diameter']==3
 assert abs(d['line_context']['maximum_effective_spectral_dimension']-3.71848244)<1e-7
 assert abs(d['collinear_triples']['maximum_effective_spectral_dimension']-5.38953272)<1e-7
def test_distinct_degree30_coupler_shared_81_cycle_flatband():
 import w33_20261009_triple_flatband_cycle_space as m
 d=m.certificate()
 assert d['flat_band_exact_multiplicity']==81
 assert d['modular_exact_rank_witness']['rank_A_plus_2I']==79
 assert d['different_couplers']['new_triple_overlap_graph_degree']==30
 assert d['different_couplers']['shared_edges']==240
 assert d['full_laplacian_spectrum']['32']==81
 assert d['exact_trace_multiplicity_proof']['multiplicity_each_Galois_conjugate']==24
