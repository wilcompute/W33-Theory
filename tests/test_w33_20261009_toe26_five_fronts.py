"""Round26: replay exact code, character, E6 dynamics, scaled tower and
C8 pair spectroscopy. Every new calculation is independently executable.
"""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe26_css_matching_family as css
import w33_20261009_toe26_css_milp_distance as ilp
import w33_20261009_toe26_q2_css_transport as q2
import w33_20261009_toe26_e8_su9_embedding_obstruction as e8
import w33_20261009_toe26_e6_sector_charge_dynamics as e6
import w33_20261009_toe26_scaled_tower_competing_vacua as scaled
import w33_20261009_toe26_c8_doublon_prototype as c8
def frozen(name):
 return json.loads((ROOT/'data'/f'w33_20261009_toe26_{name}.json').read_text())
def test_w33_ternary_css_distance_three_through_eight_exact_hyperplanes():
 r=css.run()
 assert r==frozen('css_matching_family')
 assert r['highest_verified_code']=='[[160,1,8]]_3'
 assert r['rank_Gauss_X']==79
 for d in range(3,9):
  c=r['matching_css_codes'][str(d)]
  assert c['X_distance']==d and c['Z_distance']==8
  assert c['Wilson_rank']==80 and c['independent_weight_eight_checks']==80
  assert c['code_parameters']==f'[[160,1,{d}]]_3'
 assert r['matching_css_codes']['8']['selected_eight_cycles']==1074
def test_independent_full_binary_integer_program_coset_optima():
 r=ilp.run()
 assert r['status']=='PASS'
 for d in range(3,9):
  c=r['cases'][str(d)]
  assert c['certified_optimal'] and c['status']==0
  assert abs(c['objective']-d)<1e-7 and abs(c['dual_bound']-d)<1e-7
  assert abs(c['mip_gap'])<1e-7
def test_small_q2_ternary_css_transport_three_four_five():
 r=q2.run()
 assert r['q']==2 and r['physical_qutrit_links']==45
 assert r['full_eightcycle_count']==90 and r['full_eightcycle_rank']==16
 for d in (3,4,5):
  a=r['matching_trials'][str(d)]
  assert a['qutrit_CSS_code']==f'[[45,1,{d}]]_3'
  assert a['cycle_rank']==15 and a['logical_qutrits']==1
  assert a['numerical_MILP_gap']<1e-8
def test_e8_su9_6plus3_adjoint_has_no_steinberg81():
 r=e8.run()
 assert r==frozen('e8_su9_embedding_obstruction')
 assert r['E8_su9_grading']==[80,84,84]
 assert r['full_E8_invariant_block_max_dimension']==36
 assert r['predicted_Steinberg81_multiplicity']==0
 assert sum(r['wedge3_invariant_block_dimensions'])==84
def test_transitive_e6_charge_forbidden_only_with_added_conservation():
 r=e6.run()
 assert r['sector_count']==45 and r['states_per_sector']==36
 assert r['sector_projectors_commute_with_A3']
 assert not r['sector_projectors_commute_with_A2']
 assert r['exact_projected_tunneling_eigenspectrum']=={'9.0':20,'22.5':24,'90.0':1}
 assert abs(r['finite_tunneling_gap'][0]['relative_correction'])<.01
def test_scaled_q_tower_variational_first_order_only_conditional():
 r=scaled.run()
 assert len(r['q_examples'])==7
 assert r['q_examples'][-1]['sites']==2081208
 assert r['variational_scan_across_u']['2.0']['best_alpha_limit']==0
 assert r['variational_scan_across_u']['6.0']['best_alpha_limit']==1
 for row in r['q_examples']:
  assert row['rigorous_E0_over_v_lower']<=row['rigorous_E0_over_v_upper']
  assert row['rigorous_E0_over_v_lower']<=row['min_101_family_trial_E_per_site']+1e-9
def test_8site_C8_exact_36dim_doublon_prototype():
 r=c8.run()
 assert r['two_boson_fock_dimension']==36
 assert r['five_pair_band_multiplicities']==[1,2,2,2,1]
 assert math.isclose(r['exact_leading_gap_ratios'][2],2+math.sqrt(2))
 assert abs(sum(r['exact_asymptotic_local_spectral_weights'])-1)<1e-12
 assert r['modeled_U_over_t_cases']['64']['probability_leaked_to_scattering_bands']<.002
 assert abs(r['modeled_U_over_t_cases']['64']['finite_U_gap_relative_error'])<.002
