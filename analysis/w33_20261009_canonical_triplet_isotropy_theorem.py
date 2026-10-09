"""EXACT PSp-equivariant isotropic 3-direction selector theorem.

Native oriented W33 Levi graph 80 vertices, 160 flags, B
vertex-edge incidence, L=B B.T with eigenvalues
0,8,4,4+sqrt6,4-sqrt6.
The rational pseudoinverse polynomial is
12800 L+ = -47 L^4 +900 L^3 -5686 L^2+12152 L.
Thus Pi=I-B.T L+ B, the projector onto 81D cycle space,
has entries EXACTLY:
  160 Pi_ii=81, offdiag in {-27,-3,1,9}.
No arbitrary spanning tree or cycle-coordinate basis!

For ANY unordered triple of distinct native flags, the
3x3 principal matrix 160 K_3 has diagonal81 and offdiagonal
absolute value >=1. Its eigenvalue condition number >=83/80,
attained iff all three offdiagonal elements are +1.
Proof: traceless perturbation has squared Frobenius>=6;
spectral spread >=sqrt(3/2)||perturbation||_F>=3,
fixed trace=243 then lambda_min <=(243-spread)/3
=> kappa >= (243+2spread)/(243-spread)>=83/80.
Count optimal triples as triangles of the Pi_ij=+1/160
relation; that relation is PSp-invariant.

This is an equivariant FAMILY of nearly isotropic 3-mode
candidate selectors. A specific selected triple still
BREAKS symmetry; no dynamical selection or Einstein gravity.
"""
from pathlib import Path
from collections import Counter
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_5state_ritz as W
def certificate():
 edges,*_=W.geometry()
 B=np.zeros((80,160),dtype=np.int64)
 for j,(p,l) in enumerate(edges):B[p,j]=1;B[l,j]=-1
 L=B@B.T
 L2=L@L;L3=L2@L;L4=L3@L
 numerator=-47*L4+900*L3-5686*L2+12152*L
 N=12800*np.eye(160,dtype=np.int64)-B.T@numerator@B
 assert not np.any(N%80)
 P=N//80
 assert np.array_equal(P@P,160*P)
 assert np.array_equal(P,P.T)
 assert np.array_equal(B@P,np.zeros((80,160),dtype=np.int64))
 vals,cnt=np.unique(P,return_counts=True)
 assert set(vals.tolist())=={-27,-3,1,9,81}
 assert np.all(np.diag(P)==81)
 off=P[np.triu_indices(160,k=1)]
 freq={str(int(v)):int(np.sum(off==v)) for v in (-27,-3,1,9)}
 A=(P==1).astype(np.int64);np.fill_diagonal(A,0)
 assert np.all(A.sum(axis=1)==81)
 n_best=int(np.trace(A@A@A)//6)
 assert n_best>0
 ex=None
 for i in range(160):
  nei=np.flatnonzero(A[i])
  for j in nei:
   common=np.flatnonzero(A[i]*A[j])
   common=common[common>j]
   if len(common):
    ex=[i,int(j),int(common[0])];break
  if ex:break
 assert ex
 three=P[np.ix_(ex,ex)]
 assert np.array_equal(three,np.array([[81,1,1],[1,81,1],[1,1,81]],dtype=np.int64))
 eigen=[80,80,83];ratio=83/80
 return dict(status='PASS',projector_denominator=160,
   exact_rational_L_pseudoinverse_polynomial='12800 L+ = -47 L^4 + 900 L^3 - 5686 L^2 + 12152 L',
   exact_cycle_projector_rank=81,
   exact_cycle_projector_integer_levels={str(int(v)):int(c) for v,c in zip(vals,cnt)},
   offdiagonal_unordered_class_sizes=freq,
   relation_Pij_plus_1_graph_degree=81,
   exact_optimal_unordered_three_flag_selectors=n_best,
   concrete_optimal_three_flag_indices=ex,
   exact_example_3x3_integer_tensor=three.tolist(),
   exact_optimal_eigenvalues_divided_by_160=eigen,
   global_min_eigenvalue_ratio_for_all_160_choose_3_triples='83/80',
   all_unordered_flag_triplets='C(160,3)=669920',
   optimality_proof='Let G=160 K for any three distinct flags. G has diagonal81 and nonzero integer offdiagonal abs>=1, so ||G-81I||_F²>=6; for tracezero 3x3 real symmetric, lambda_max-lambda_min>=sqrt(3/2)*||G-81I||_F>=3. Trace G=243 gives lambda_min<=(243-spread)/3, hence kappa >=(243+2*spread)/(243-spread)>=83/80. Equality achieved when all three offdiagonals equal+1.',
   group_equivariance='PSp acts by permutation of 160 flags and commutes with Pi. Entire optimal set is G-invariant, not any specifically selected 3D subspace.',
   physical_boundary='A rigorously optimal symmetry-covariant combinatorial selector family, but choosing a member is an external symmetry breaking or requires unproven dynamics. No physical dimension, spacetime metric or Lorentz signature follows.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_canonical_triplet_isotropy_theorem.json').write_text(json.dumps(d,indent=2)+'\n')
 print('CANONICAL TRIPLET',d['exact_optimal_unordered_three_flag_selectors'],d['concrete_optimal_three_flag_indices'],d['exact_cycle_projector_integer_levels'])
