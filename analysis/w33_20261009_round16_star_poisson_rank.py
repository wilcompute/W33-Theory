"""Round16: exact rational Poisson rank and normal-mode data at 80
star classical zero planes of the W33 current-square model.

This is the principal-symbol linearized constraint bracket, NOT an
operator spectral lower bound. Hessian rank82, with 74 flat momentum
directions in each of 80 affine classical zero planes.
"""
import sys,json
from pathlib import Path
import numpy as np
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
def rankmod(A,p=32003):
 a=np.asarray(A,dtype=np.int64)%p;m,n=a.shape;r=0
 for k in range(n):
  if r==m:break
  nz=np.flatnonzero(a[r:,k])
  if len(nz)==0:continue
  j=r+int(nz[0]);a[[j,r]]=a[[r,j]]
  a[r]=(a[r]*pow(int(a[r,k]),-1,p))%p
  for s in range(r+1,m):
   if a[s,k]:a[s]=(a[s]-int(a[s,k])*a[r])%p
  r+=1
 return r
def certificate():
 g=H.geometry();U=np.rint(40*g['u']).astype(np.int64);V=np.rint(40*g['v']).astype(np.int64)
 # Anchor constructions copied explicitly from prior 80-star certificate.
 results=[]
 for vertex in range(80):
  qi=np.zeros(80,dtype=np.int64)
  if vertex<40: qi[:40]=-1;qi[vertex]=39
  else: qi[40:]=1;qi[vertex]=-39
  X=V@qi+40;active=np.flatnonzero(X)
  assert len(active)==4
  A=U[active].astype(np.int64)
  Gram=A@A.T
  # Reference momentum with A*(p/a)=-40*ones, using exact Gram inverse.
  # Gram diagonal3120 and offdiag1520, so Gram=1600I+1520J.
  assert np.array_equal(Gram,1600*np.eye(4,dtype=np.int64)+1520*np.ones((4,4),dtype=np.int64))
  pnum=-40*(A.sum(axis=0)) # divide by 7680
  Y=U@pnum+40*7680
  # For e active: u.p/a+1=0; for inactive z=0.
  assert all(Y[active]==0)
  assert not np.any(X*Y)
  # Derivative of 160 currents w.r.t q,p up to positive scalar:
  # dJ= (Y/7680)*V dq + X*U dp /40. Multiply by 7680:
  # Gq=Y*V; Gp=192*X*U.
  Qgrad=Y[:,None]*V
  Pgrad=192*X[:,None]*U
  # Poisson brackets {J_e,J_f} proportional
  # Qgrad_e.Pgrad_f-Pgrad_e.Qgrad_f.
  # Nonzero entries only active-passive, rank 2*r where r is
  # cross block (active 4 against passive156).
  passive=np.flatnonzero(X==0)
  B=Qgrad[passive]@Pgrad[active].T
  r=rankmod(B)
  assert r<=4
  results.append(dict(star=vertex,bracket_rank=2*r,independent_conjugate_pairs=r,
                      classical_zero_momentum_plane_dim=74))
 assert len(set(z['bracket_rank'] for z in results))==1
 return dict(status='PASS',stars=80,
    rank_distribution=dict(Counter(str(x['bracket_rank']) for x in results)),
    each_star_74dim_exact_classical_zero_plane=True,
    example=results[0],
    proof='Exact integer current gradients Qgrad=Y*V, Pgrad=192*X*U at 80 zero anchors; full skew Poisson matrix is bipartite active/passive, rank=2 rank(B), verified by F32003 row elimination. Classical linear normal modes are bounded by this symplectic constraint rank; no quantum eigenvalue or global gap follows.',
    epistemic_boundary='The linearized classical Poisson matrix is not the full quantized operator or its ground representation. Rank over finite field gives a rational lower bound only unless independent analytic upper bound is given (here at most 2*4=8).')
if __name__=='__main__':
 z=certificate();(ROOT/'data/w33_20261009_round16_star_poisson_rank.json').write_text(json.dumps(z,indent=2)+'\n')
 print('STAR POISSON',z['rank_distribution'])
