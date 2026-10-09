"""Engineered correlated-disorder W33 flat-band photonic couplers.

PREEXISTING BT548/Pass4019: Levi 160-edge LINE-GRAPH -2 H1 band.
PREVIOUS round8: degree30 triple-overlap coupler shares that H1 band.

NEW: any local positive diagonal weight per 80 parent Levi vertices
produces H(w)=B^T diag(w)B-2I, with EXACT protected 81-dimensional
ground band at -2 and robust quantitative gap
>= min(w)*(4-sqrt6), regardless of disorder amplitude variance.
Weights alter onsite energies in a correlated way; generic site
disorder is NOT protected (Pass4019 already showed rank1 splitting).

Also compare affine interpolations of degree6 and degree30 couplers:
the H1 invariant subspace persists, but need not stay the ground band.
"""
from itertools import combinations
from pathlib import Path
import json,sys
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
from w33_20261009_local_hormander_depth import rank_mod
def construct():
 lines=B.w33_lines(B.make_points())
 T=[];parents=[];missing=[]
 for li,L in enumerate(lines):
  for tri in combinations(L,3):
   T.append(tuple(tri));parents.append(li);missing.append(next(iter(set(L)-set(tri))))
 D=np.zeros((40,160),dtype=np.int64);M=D.copy()
 D[parents,np.arange(160)]=1;M[missing,np.arange(160)]=1
 Blevi=np.vstack([M,D])
 P=np.zeros((40,160),dtype=np.int64)
 for i,tri in enumerate(T):P[list(tri),i]=1
 I=np.eye(160,dtype=np.int64)
 A6=Blevi.T@Blevi-2*I
 A30=P.T@P-D.T@D-2*I
 assert np.all(A6.sum(axis=1)==6) and np.all(A30.sum(axis=1)==30)
 return Blevi,A6,A30,M,D,P
def certificate():
 B,A6,A30,M,D,P=construct();N=160
 assert rank_mod(np.vstack([M,D]))==79
 assert rank_mod(np.vstack([M,P]))==64
 assert rank_mod(B)==79
 I=np.eye(160,dtype=np.int64)
 assert np.array_equal(A6+A30+4*I,M.T@M+P.T@P)
 # At t=1/2, A(t)+2I=(M^T M+P^T P)/2 is PSD
 # and has rank 64 => exactly 96 lowest eigenstates at -2.
 # At t>1/2, a 15D complement to H1 in ker(M,P) has
 # nonzero D and negative quadratic form (1-2t)||Dx||².
 Lgap=4-np.sqrt(6)
 seeds=np.random.default_rng(2039)
 weights=[np.ones(80),seeds.uniform(.6,1.4,80),
          np.where(np.arange(80)%2==0,.5,1.5)]
 W=[]
 for w in weights:
  H=(B.T*w)@B-2*np.eye(N)
  e=np.linalg.eigvalsh(H)
  gap=float(e[81]-(-2))
  assert np.max(abs(e[:81]+2))<1e-9
  assert gap>=float(min(w)*Lgap)-1e-9
  assert np.max(abs(B@np.eye(160)[:,0]))>0
  W.append(dict(weight_min=float(min(w)),weight_max=float(max(w)),
       numerical_first_above_flat_band_gap=gap,
       rigorous_weighted_lower_gap=float(min(w)*Lgap),
       onsite_shift_range=[float(min(w[B[:,j].nonzero()[0]].sum()-2 for j in range(160))),
                           float(max(w[B[:,j].nonzero()[0]].sum()-2 for j in range(160)))],
       exact_H_on_cycles='-2*I'))
 # Compute generalized eigenvalue of (A30+2I) relative to (A6+2I)
 # on range(B.T) of dimension79. The shared 81 kernel is removed.
 gram=B@B.T
 ev,Q=np.linalg.eigh(gram.astype(float))
 assert sum(ev>1e-8)==79
 U=B.T@Q[:,ev>1e-8]@np.diag(ev[ev>1e-8]**(-.5))
 assert np.max(abs(U.T@U-np.eye(79)))<1e-10
 K6=U.T@(A6+2*np.eye(N))@U
 K30=U.T@(A30+2*np.eye(N))@U
 generalized=eigh(K30,K6,eigvals_only=True)
 lambdamin=float(generalized[0])
 transition=1/(1-lambdamin)
 assert lambdamin<0 and 0<transition<1
 samples=[]
 for t in (0.,.05,.1,.2,.25,transition-1e-5,transition+1e-5,.5,1.):
  K=(1-t)*K6+t*K30
  smallest=float(np.linalg.eigvalsh(K)[0])
  samples.append(dict(t=float(t),minimum_complement_energy_above_minus2=smallest,
       H1_is_ground=(smallest>=-1e-8)))
 assert samples[5]['H1_is_ground'] and not samples[6]['H1_is_ground']
 conservative=Lgap/(Lgap+4)
 assert abs(transition-.5)<1e-10
 assert transition>=conservative-1e-8
 return dict(status='PASS',existing_line_coupler_degree=6,second_triple_coupler_degree=30,
       protected_H1_dimension=81,local_weight_disorder= W,
       guaranteed_gap_bound='H(w)=B^T diag(w)B-2I has E0=-2 with multiplicity81, next energy >= -2+min(w)*(4-sqrt6), for ALL w_i>0. In particular all1620 BT4019 apartment states remain exact eigenvectors even after correlated disorder.',
       interpolation_min_generalized_eigenvalue=lambdamin,
       interpolation_numeric_H1_ground_phase_endpoint=transition,
       conservative_analytic_sufficient_endpoint=conservative,
       interpolation_samples=samples,
       exact_ground_transition='The interpolation A(t)=(1-t)A6+t*A30 has A(t)+2I=(1-t)M^TM+(1-2t)D^TD+tP^TP. For 0<=t<1/2 it is PSD and has kernel exactly ker[M;D] of dimension81 (t=0 follows directly too). At t=1/2 it equals (M^TM+P^TP)/2 and the kernel has exact rank-deficiency 160-64=96, hence 15 extra ground states. For t>1/2, choose x in ker(M,P) but Dx!=0; its Rayleigh form is (1-2t)||Dx||²<0, proving that the H1 -2 band is NO LONGER the ground band.',
       exact_midpoint_rank64=True,
       ground_crossing_exact_fraction='1/2',ground_degeneracy_at_crossing=96,
       additional_zero_modes_at_crossing=15,
       interpolation_exact_H1_identity='[(1-t)A6+t*A30]c=-2c for every c in H1, all real t. Ground-band status is lost after a computable positive critical t; continuity of flat band does NOT imply ground protection for all t.',
       critical_boundary='The critical interpolation is proved EXACTLY t=1/2 by factorization and rational rank. The 0.2793 gap bound is only a conservative separate estimate. Coupler onsite terms must covary with shared-vertex hopping weights; independent onsite disorder generically splits H1 (Pass4019 prior result).')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_correlated_disorder_dual_couplers.json').write_text(json.dumps(d,indent=2)+'\n')
 print('DUAL COUPLERS',d['interpolation_numeric_H1_ground_phase_endpoint'],d['conservative_analytic_sufficient_endpoint'],[(x['weight_min'],x['numerical_first_above_flat_band_gap']) for x in d['local_weight_disorder']])
