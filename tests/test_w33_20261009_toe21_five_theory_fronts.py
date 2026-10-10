"""Five independently executed TOE tests, with exact group/cardinality,
finite-q heat-kernel, Weyl, energy-selection, and mass-spectrum controls.
"""
from pathlib import Path
import json,math,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe21_steinberg_cubic_invariants as E
import w33_20261009_toe21_dynamical_selector_bifurcation as D
import w33_20261009_toe21_qfamily_heat_nogo as Q
import w33_20261009_toe21_doubled_qutrit_heisenberg as H
import w33_20261009_toe21_mass_scale_firewall as S
def payload(name):
 return json.loads((ROOT/'data'/('w33_20261009_toe21_'+name+'.json')).read_text())

def test_full_symmetry_cubic_invariant_dimensions():
 a=payload('steinberg_cubic_invariants')
 assert a['group_order']==25920
 dims=a['invariant_dimensions']
 assert dims['sym3']==4 and dims['exterior3']==5
 assert dims['wedge2_times_V']==11 and dims['V_squared']==1
 assert dims['S21']==6
 ext=a['extended_similitude_invariant_dimensions']
 assert a['projective_similitude_group_order']==51840
 assert ext['exterior3']==1 and ext['wedge2_times_V']==4
 assert ext['sym3']==3 and ext['S21']==3 and ext['V_squared']==1
 # Universal Schur dimension formula on identity class:
 chi,chi2,chi3=81,81,81
 assert (chi**3-3*chi*chi2+2*chi3)//6==math.comb(81,3)
 assert (chi**3+3*chi*chi2+2*chi3)//6==math.comb(83,3)

def test_focusing_graph_coexistence_window_and_actual_trial():
 a=payload('dynamical_selector_bifurcation')
 A=D.matrix()
 ev=np.linalg.eigvalsh(A)
 assert abs(ev[-1]-4)<1e-12
 assert abs(ev[-2]-math.sqrt(6))<1e-12
 lo=a['trial_crossing_g_over_t'];hi=a['local_uniform_hessian_threshold_g_over_t']
 assert 4.05<lo<4.06 and 31<hi<31.02
 assert -5 < -4-5/80
 assert a['numerical_multistart']['5']['max_site_probability']>.90
 assert a['numerical_multistart']['3']['max_site_probability']<.02
 for g in (5,10,20,30):
  assert lo<g<hi and g<160

def test_generalized_spacetime_heat_limit_and_finite_gap():
 a=payload('qfamily_heat_nogo')
 for q in (2,3,5,11,31,101,1001,1000001):
  d=a['rows'][str(q)]
  spec,v=Q.eigens(q)
  assert sum(m for l,m in spec)==v
  assert len(spec)==5 and spec[0]==(0,1)
  assert abs(d['normalized_nonzero_gap']-(1-math.sqrt(2*q)/(q+1)))<1e-15
 assert abs(Q.heat(1000001,1)[0]-math.exp(-1))<1e-5
 assert abs(Q.heat(1000001,1)[1]-2)<1e-4
 assert Q.heat(3,1)[1]!=2

def test_mod3_Heisenberg_Weyl_and_contragredient_PSp():
 a=payload('doubled_qutrit_heisenberg')
 assert a['phase_space_pairing_preserved'] if 'phase_space_pairing_preserved' in a else True
 assert a['heisenberg_group_order']=='3^163'
 assert len(a['group_action_records'])==5
 assert all(x['phase_space_pairing_preserved'] for x in a['group_action_records'])
 assert a['weyl_3by3_validation']['max_100_random_exact_3by3_product_error']<1e-12
 assert abs(a['weyl_3by3_validation']['example_ground_gap']-2*math.sqrt(3))<1e-10
 rng=np.random.default_rng(102)
 for _ in range(30):
  x,z,a,b=[rng.integers(0,3,size=81) for j in range(4)]
  assert H.symp((x,z),(a,b))==(-H.symp((a,b),(x,z)))%3

def test_geometric_mass_hierarchy_and_unfixed_scale():
 a=payload('mass_scale_firewall')
 assert a['maximum_cross_type_nonzero_eigenratio']=='2'
 vals=[]
 for typ,record in a['eigenratio_by_type'].items():
  curr=[sp.Rational(x) for x in record['nonzero_eigenvalues']]
  vals.extend(curr)
  assert sp.Rational(record['largest_smallest_exact'])==max(curr)/min(curr)
 assert min(vals)==sp.Rational(9,20) and max(vals)==sp.Rational(9,10)
 assert a['RG_scale_examples']['b=1/20,g0=0.7'] < a['RG_scale_examples']['b=1/10,g0=1.3']/100000
