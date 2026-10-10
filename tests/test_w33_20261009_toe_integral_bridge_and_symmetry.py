"""Regression tests for the native W33 integral homology/gauge correspondence
and symmetry-breaking harmonic mass shells. No physical TOE inference.
"""
from pathlib import Path
import sys,json
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe_integral_clique_levi_bridge as B
import w33_20261009_toe_q4_family_theorem as F
import w33_20261009_toe_star_defect_spectra as S
import w33_20261009_toe_c3_clock_phase_nogo as C
from w33_pass1081_1086_core import build_w33,transvection_perm,line_perm,rank_mod

def cert(stem):
 return json.loads((ROOT/'data'/('w33_20261009_toe_'+stem+'.json')).read_text())

def test_integral_81_hodge_levi_chain_and_metric_iso():
 pts,ix,lines,li,edges,tris,flags,fi,E,T,D,M,L=B.chain()
 Z,chords=B.integer_cycle_basis(flags)
 assert len(chords)==81 and np.array_equal(D@M[:,:],np.r_[E,np.zeros((40,240),dtype=np.int64)])
 assert np.array_equal(M@T,np.zeros((160,160),dtype=np.int64))
 assert np.array_equal(M@L@Z,Z)
 assert np.array_equal(E@L@Z,np.zeros((40,81),dtype=np.int64))
 assert np.array_equal(M@M.T@Z,4*Z)
 H=E.T@E+T@T.T
 assert np.array_equal(H@M.T@Z,np.zeros((240,81),dtype=np.int64))
 assert np.array_equal((M.T@Z).T@(M.T@Z),4*(Z.T@Z))
 assert rank_mod(Z.T@Z,3)==81
 assert B.equivariance(pts,ix,lines,li,edges,flags,fi,M)==[240]*6
 c=cert('integral_clique_levi_bridge')
 assert c['exact_identities']['Psi_equals_M_transpose']
 assert c['cycles']['Gram_mod_prime_ranks']=={'2':52,'3':81,'5':58,'7':81,'11':81}

def test_q4_symplectic_gq_prime_family():
 c=cert('q4_family_theorem')
 for q in (2,3,5):
  d=c['prime_field_cases'][str(q)]
  assert d['Levi_first_homology_rank']==q**4
  assert d['points']==(q+1)*(q*q+1)
  assert int(d['critical_group_order'])%q
 assert c['prime_field_cases']['2']['explicit_q2_identity']['exact_chain_identity']
 assert c['prime_field_cases']['2']['explicit_q2_identity']['transpose_image_euclidean_scale_squared']==3

def test_all_six_star_orbit_pair_spectra_rigorous_polynomials():
 c=cert('star_defect_spectra')
 assert c['all80_single_stars']['nonzero_eigenvalue_of_P Pstar P']=='27/40 repeated 3'
 rows=c['all3160_distinct_vertex_pairs']
 assert sum(v['count'] for v in rows.values())==3160
 assert {k:v['count'] for k,v in rows.items()}=={
  'line_line_intersect':240,'line_line_skew':540,
  'point_line_incident':160,'point_line_nonincident':1440,
  'point_point_collinear':240,'point_point_far':540}
 pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33()
 K,_=S.levi_cycle_kernel(flags)
 assert np.array_equal(K@K,160*K)
 for typ,rec in rows.items():
  a,b=rec['representative']
  stars=[[i for i,(p,l) in enumerate(flags) if p==v] for v in range(40)]
  stars += [[i for i,(p,l) in enumerate(flags) if l==v] for v in range(40)]
  ids=sorted(set(stars[a]+stars[b]))
  pol=sp.factor(sp.Matrix(K[np.ix_(ids,ids)].tolist()).charpoly(sp.Symbol('z')).as_expr())
  assert sp.sstr(pol)==rec['characteristic_polynomial_of_integer_K_union']

def test_exact_transvection_f3_jordan_clocks():
 c=cert('c3_clock_phase_nogo')
 assert len(c['order3_transvection_witnesses'])==5
 for v in c['order3_transvection_witnesses']:
  assert v['char_order3']==[81,0,0]
  assert v['char3_nilpotent_ranks']==[54,27]
  assert v['mod3_jordan_three_blocks']==27
 # Recompute first transvection directly in an unrelated test.
 pts,pidx,lines,lidx,edges,tris,flags,fi,E,T,D,M,L=B.chain()
 Z,chords=B.integer_cycle_basis(flags)
 g=transvection_perm(pts[0],pts,pidx)
 lp=line_perm(g,lines,lidx)
 perm=[fi[(g[p],lp[l])] for p,l in flags]
 acted=np.zeros_like(Z);acted[perm,:]=Z
 X=acted[chords]
 assert np.array_equal(Z@X,acted)
 N=X-np.eye(81,dtype=np.int64)
 assert rank_mod(N%3,3)==54
 assert rank_mod((N@N)%3,3)==27
 assert not np.any((N@N@N)%3)
