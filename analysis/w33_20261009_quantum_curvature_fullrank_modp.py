"""Finite-field magnetic-curvature RANK on the actual 78D
W33 quantum current-square Hamiltonian at the exact point
q=a*(e_0-e_39)/10.

Round12 proved one antisymmetric entry nonzero. This pass
computes the exact complete 78x78 rational 2-form rank using
finite-field matrix inverses and modular row reduction. The
ranks certify LOWER bounds over Q (bad characteristic can lower
rank), while real numeric singular values check upper candidate
and avoid claiming an exact Q-rank without rational minors or an
upper exact annihilator. The curvature is not the physical EM field.
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as Q
from w33_20261009_quantum_curl_exact_modular import solve_mod
def rank_mod(A,p):
 X=np.asarray(A,dtype=np.int64).copy()%p
 m,n=X.shape;rank=0
 for j in range(n):
  cand=np.flatnonzero(X[rank:,j]) if rank<m else []
  if len(cand)==0:continue
  k=rank+int(cand[0])
  X[[rank,k]]=X[[k,rank]]
  X[rank]=(X[rank]*pow(int(X[rank,j]),-1,p))%p
  for h in range(rank+1,m):
   if X[h,j]:X[h]=(X[h]-int(X[h,j])*X[rank])%p
  rank+=1
  if rank==m:break
 return rank
def certificate():
 geo=Q.geometry()
 u40=np.rint(40*geo['u']).astype(np.int64)
 v40=np.rint(40*geo['v']).astype(np.int64)
 D=np.zeros((80,78),dtype=np.int64)
 for j in range(39):
  D[j,j]=1;D[39,j]=-1
  D[40+j,39+j]=1;D[79,39+j]=-1
 Hinv=40*np.eye(78,dtype=np.int64)
 Hinv[:39,:39]-=1
 Hinv[39:,39:]-=1
 assert np.array_equal(D.T@D@Hinv,40*np.eye(78,dtype=np.int64))
 u=u40@D@Hinv;v=v40@D;t=400+v[:,0]
 results=[]
 for p in (10007,10009,10037):
  up=u%p;vp=v%p;tp=t%p
  T=(up.T@(((tp*tp)%p)[:,None]*up))%p
  b=(up.T@((tp*tp)%p))%p
  y=solve_mod(T,b,p)
  res=(1-up@y)%p
  W=(up.T@(((tp*res)%p)[:,None]*vp))%p
  C=(32000*solve_mod(T,W,p))%p
  skew=(C-C.T)%p
  assert not np.any(np.diag(skew))
  rk=rank_mod(skew,p)
  assert rk%2==0 and rk>0
  results.append(dict(prime=p,rank_skew2form_over_Fp=rk,nonzero_entries=int(np.count_nonzero(skew))))
 # Physical 78D real antisymmetric approximate rank, condition-number
 uf=u.astype(float);tf=t.astype(float)
 K=uf.T@((tf*tf)[:,None]*uf)
 y=np.linalg.solve(K,uf.T@(tf*tf))
 W=uf.T@((tf*(1-uf@y))[:,None]*v)
 C=32000*np.linalg.solve(K,W)
 A=C-C.T
 sing=np.linalg.svd(A,compute_uv=False)
 return dict(status='PASS',magnetic_curvature_2form_dimension=78,
   finite_field_rank_lower_bounds=results,
   real_singular_values_biggest=list(map(float,sing[:8])),
   real_singular_values_smallest=list(map(float,sing[-8:])),
   real_numerical_rank_tol_1e_minus_6=int(sum(sing>1e-6)),
   statement='A nonzero modular r-by-r minor yields rank over Q >=r. Equality requires separate exact upper rank certificate; none is asserted unless rank78 is established. Full 78 ranks yield exact maximal nondegenerate symplectic 2-form at this point.',
   interpretation='Nonzero effective magnetic curvature blocks naive scalar-gauge Perron-Frobenius ground-state uniqueness. It is a property of an artificial quantized model, not a physical magnetic field, a proof of vacuum degeneracy or measured curvature.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_quantum_curvature_fullrank_modp.json').write_text(json.dumps(d,indent=2)+'\n')
 print('MAGNETIC RANK',d['finite_field_rank_lower_bounds'],d['real_numerical_rank_tol_1e_minus_6'],d['real_singular_values_smallest'])
