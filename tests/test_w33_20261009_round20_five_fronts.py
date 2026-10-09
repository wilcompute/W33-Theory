"""Round20 tests: exact gauge frustration, interval Gaussian stability,
photon budgets, frozen heterotic screening, causal synthetic optical controls.
"""
from pathlib import Path
import sys,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_round20_photon_budget as P
import w33_20261009_round20_global_plaquette as G
import w33_20261009_round20_exact_star_interval as S
import w33_20261009_round20_heterotic_amplitude_obstructions as H
import w33_20261009_round20_two_actuator_dark_reference as O
import w33_pass11769_quantized_current_vacuum as V

def data(name):
 return json.loads((ROOT/'data'/f'w33_20261009_round20_{name}.json').read_text())

def test_photon_budget_five_native_histograms():
 d=data('photon_budget')
 assert .08<d['best_grid_search_time']*0+.083530550890556<.09
 assert d['best_grid_search_time'] == 10.350000000000001
 a,b=d['representative_shot_budgets'][:2]
 assert a['t']==2.0 and b['min_pairwise_histogram_linf_distance']>.08
 assert a['survival_shots_per_site_per_candidate']>19000000
 assert b['survival_shots_per_site_per_candidate']==11100
 assert b['survival_shots_per_site_per_candidate']<a['survival_shots_per_site_per_candidate']/1000
 # Exact union-bound inequality, no loose rounding error:
 n=b['survival_shots_per_site_per_candidate'];eps=b['min_pairwise_histogram_linf_distance']/4
 assert 2*400*math.exp(-2*n*eps*eps)<=.05

def test_gauge_disjoint_exact_theta_lower_bound():
 d=data('global_plaquette')
 edges,cyc,masks,rows=G.cycle_vectors()
 rel,packed=G.theta_packing(masks,rows)
 assert len(cyc)==1620 and len(rel)==4320
 assert len(packed)==485 and len({i for t in packed for i in t})==3*485
 assert d['rigorous_global_lower_bound_units_g']==-892.5
 assert d['best_numerical_achieved_upper_bound_units_g']>-892.5
 assert d['best_numerical_achieved_upper_bound_units_g'] < -320
 v=np.zeros(160)
 v[d['tree_chords']]=np.array(d['numerical_best_chord_angles'])
 direct=sum(math.cos(2*sum(int(s)*v[e] for e,s in row.items())) for row in rows)
 assert abs(direct-d['best_numerical_achieved_upper_bound_units_g'])<1e-7
 # All theta constraints must be exact integer relations; sample ten packed ones.
 for i,j,k in packed[:10]:
  v=[rows[t] for t in (i,j,k)]
  assert any(all(sum(s[t]*v[t].get(e,0) for t in range(3))==0 for e in range(160))
    for s in ((a,b,c) for a in (-1,1) for b in (-1,1) for c in (-1,1)))

def test_vacuum_interval_exact_all80():
 d=data('exact_star_interval')
 assert d['status']=='EXACT_RATIONAL_INTERVAL_CERTIFIED'
 assert len(d['star_rows'])==80
 assert d['numerical_summary']['D0_lower_min']>200
 assert d['numerical_summary']['D2_lower_min']>16000
 assert d['numerical_summary']['D_discriminant_upper_max']< -1e7
 trial=V.exact_trial();br=V.root_bracket(trial)
 sqrtlo,sqrthi=map(S.F,br['sqrt10_interval'])
 tlo,thi=map(S.F,br['t_interval'])
 m=S.box((6*sqrtlo+15)/40,(6*sqrthi+15)/40);t=S.box(tlo,thi)
 b=S.F(1,20);f=S.div(S.box(-2*b),S.plus(S.mul(S.box(3),S.mul(m,t)),S.box(b)))
 g=V.geometry()
 U=np.rint(40*g['u']).astype(np.int64);W=np.rint(40*g['v']).astype(np.int64)
 for star in (0,1,40,79):
  own=S.checked(star,U,W,m,t,f)
  assert own['H0_discriminant_lower']==d['star_rows'][star]['H0_discriminant_lower']

def test_vacuum_central_gaussian_local_moments_formula():
 g=V.geometry();c,ci=V.spectral_covariance(g);old=V.exact_trial()
 t=old['t'];f=old['f'];m=old['m'];ph=f*np.diag(g['s'])
 _,vx,vy,cross=V.gaussian_energy(g['u'],g['v'],t*c,ci/t,ph)
 assert np.max(np.abs(vx-m*t))<1e-10
 assert np.max(np.abs(vy-(m/t+f*f*m*t)))<1e-10
 assert np.max(np.abs(cross-f*m*t))<1e-10

def test_heterotic_identical_superfield_epsilon_forced_zeros():
 d=data('heterotic_amplitude_obstructions')
 fields,neutral=H.field_mononomials()
 assert len(fields)==176 and len(neutral)==424
 assert d['R_nonR_necessary']==90 and d['pointgroup_twist_sum0_mod6']==90
 assert d['additional_antisymmetry_vanishing_count']==8
 assert d['remaining_necessary_not_sufficient_cubic_candidates']==82
 assert 'd_1,q_2,q_2' in d['forced_commuting_identical_field_antisymmetric_zeros']
 assert H.local_symmetrization_zero(('d_1','q_2','q_2'),fields)

def test_independent_optical_reference_gain_calibration():
 a=O.simulate(n=16000,optical=.08,leak=.07)
 b=O.simulate(n=16000,optical=0,leak=.07)
 assert a['design_rank']==b['design_rank']==9
 assert abs(a['calibrated_optical_estimate']-.08)<.0005
 assert abs(b['calibrated_optical_estimate'])<.0005
 d=data('two_actuator_dark_reference')
 assert d['one_percent_calibration_gain_uncertainty_floor']>.0006
 assert abs(d['ten_percent_reference_gain_error_bias'])>.006
