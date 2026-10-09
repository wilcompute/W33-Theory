"""Round15 six independent reproducible W33 research frontiers:
80 exact classical zero planes, generic full-rank quantized
curvature, original heterotic charge-twin rule distinction,
causal clipped optical effect confidence intervals, complete
five-orbit 3/4-body incidence Hamiltonian selectors, and
regression of single-photon full-band isospectrality.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_all_80_classical_flat_zero_planes():
 import w33_20261009_round15_eighty_classical_zero_planes as m
 d=m.certificate()
 assert d['exact_classical_zero_planes']==80
 assert d['affine_momentum_plane_dimension']==74
 assert d['point_orbit_planes']==40 and d['line_orbit_planes']==40
 assert len({tuple(x) for x in d['all_80_active_flag_sets']})==80
def test_generic_full_rank_quantum_curvature_over_Q():
 import w33_20261009_round15_magnetic_generic_fullrank as m
 d=m.certificate()
 rows=d['exact_modular_point_certificates']
 assert [x['modular_certificates'][0]['exact_Fp_curvature_rank'] for x in rows]==[0,16,22,78,78]
 assert d['generic_rank_over_Q']==78
 assert all(c['exact_Fp_det']!=0 for x in rows[-2:] for c in x['modular_certificates'])
 assert all(c['exact_T_det']!=0 for x in rows for c in x['modular_certificates'])
def test_exact_original_heterotic_charge_twin_discrete_veto():
 import w33_20261009_round15_heterotic_charge_twin_rule as m
 d=m.certificate()
 assert len(d['source_sha256'])==64
 a,b=d['discriminating_superpotential_triples']
 assert a['corrected_R_nonR_passes'] and not b['corrected_R_nonR_passes']
 assert a['point_twist_sum_mod6']==b['point_twist_sum_mod6']==0
 assert a['SO4_Z2xZ2_necessary_residues']==[0,0]
def test_randomized_paired_optical_signed_clipped_CI():
 import w33_20261009_round15_optical_causal_effect_CI as m
 d=m.certificate()
 assert 0.01<d['certified_conservative_two_sided_halfwidth']<0.02
 assert d['synthetic_sham_and_optical_effect_CIs']['optical']['intervals_excluding_zero']==30
 assert d['synthetic_sham_and_optical_effect_CIs']['null']['intervals_excluding_zero']==0
 assert d['synthetic_sham_and_optical_effect_CIs']['electronics_only']['intervals_excluding_zero']==0
def test_complete_five_orbit_multiway_correlation_invariants_and_Hamiltonians():
 import w33_20261009_round15_complete_five_orbit_interactions as m
 d=m.certificate()
 assert d['distinct_signature_count']==5
 assert sorted(x['orbit_size'] for x in d['complete_five_PSp_signatures'])==[4320,4320,25920,25920,25920]
 assert all(x['first_orbit_gap']>=1 and x['ground_degeneracy'] in (4320,25920) for x in d['engineered_linear_orbit_selection_Hamiltonians'])
def test_previous_full_band_single_photon_isospectral_no_go_preserved():
 import w33_20261009_round14_fullband_magnetic_isospectrality as m
 d=m.certificate()
 assert d['identical_restricted_moments_m0_to_m4']
 assert d['exact_magnetic_isospectrality_all_k'] and d['optimal_flag_triples']==86400
