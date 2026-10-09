"""Round16 five independent scientific tracks and two follow-up
certificates: source-recomputed exact maths, model-specific heterotic
necessary selection and numerical two-photon Bose-Hubbard comparisons.
"""
import sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
def test_80_classical_star_poisson_bracket_rank_exact():
 import w33_20261009_round16_star_poisson_rank as m
 z=m.certificate()
 assert z['stars']==80 and z['rank_distribution']=={'8':80}
 assert z['each_star_74dim_exact_classical_zero_plane']
def test_80_star_isotropic_gaussian_optimum():
 import w33_20261009_round16_star_gaussian_uncertainty as m
 z=m.certificate()
 assert z['classical_zero_stars']==80
 assert z['coefficient_A']=='312' and z['coefficient_B']=='1027/128'
 assert 252.16<z['optimum_gaussian_energy']<252.17
 assert z['isotropic_centered_origin_gaussian_energy']=='1681/10'
def test_all_176_heterotic_complete_charge_twin_groups():
 import w33_20261009_round16_charge_twins_all176 as m
 z=m.certificate()
 assert z['total_fields']==176 and z['groups_with_twins']==4
 assert z['twin_pairs']==4
 assert z['complete_twin_groups']==[['n_81','n_83'],['n_82','n_84'],['n_88','n_90'],['n_89','n_91']]
 assert z['benchmark_cubic_contrast']['n_81']['necessary_corrected_R_nonR']
 assert not z['benchmark_cubic_contrast']['n_83']['necessary_corrected_R_nonR']
def test_independent_dual_detector_optical_negative_control():
 import w33_20261009_round16_dual_sensor_did_optics as m
 z=m.certificate()
 assert z['synthetic']['null']['rejections']==0
 assert z['synthetic']['electronics_sham']['rejections']==0
 assert z['synthetic']['optical']['rejections']==18
 assert z['maximum_arbitrarily_corrupted_raw_readings']==14
def test_two_boson_native_onsite_operator_Hermitian_and_U0_band():
 import w33_20261009_round16_two_boson_hubbard_orbits as m
 z=m.certificate()
 assert z['two_boson_sector_dimension']==3240
 assert z['data']['flux']['0.0']['max_ground_spread']<1e-7
 assert z['data']['flux']['2.0']['max_excited_spread']>1e-6
def test_two_boson_high_precision_orbit_splitting_exceeds_residual():
 import w33_20261009_round16_two_boson_verified_splitting as m
 z=m.certificate()
 assert len(z['results'])==3
 assert all(r['excited_spread']>100*r['maximum_eigenpair_residual'] for r in z['results'])
 assert all(r['ground_spread']>100*r['maximum_eigenpair_residual'] for r in z['results'])
