"""Exact finite-field determinant certificates that the rational
magnetic curvature of W33 quantum current-square is GENERICALLY
nondegenerate in all 78 configuration directions.

All operations are integer modular Gauss–Jordan; no floating
eigensolver decides rank. Two independent primes confirm a
nonzero determinant at explicit q = (a/10)*D*k.

A nonzero rational Pfaffian/determinant at one nonsingular point
means its rational-function numerator is nonzero polynomial, so
outside a proper algebraic subset of R^78 the skew two-form
is symplectic. Rank at high-symmetry special q was EXACTLY16,
so curvature stratifies with symmetry.
This doesn't determine vacuum symmetry or prove a spectral gap.
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
from w33_20261009_quantum_curvature_fullrank_modp import rank_mod
from w33_20261009_quantum_curl_exact_modular import solve_mod
def det_mod(A,p):
 X=np.asarray(A,dtype=np.int64).copy()%p
 n=X.shape[0];d=1
 for i in range(n):
  piv=np.flatnonzero(X[i:,i])
  if not len(piv):return 0
  j=i+int(piv[0])
  if j!=i:X[[i,j]]=X[[j,i]];d=-d
  pivval=int(X[i,i]);d=(d*pivval)%p
  inv=pow(pivval,-1,p)
  X[i]=(X[i]*inv)%p
  for j in range(i+1,n):
   if X[j,i]:X[j]=(X[j]-int(X[j,i])*X[i])%p
 return d%p
def certificate():
 geo=H.geometry();U=np.rint(40*geo['u']).astype(np.int64);V=np.rint(40*geo['v']).astype(np.int64)
 D=np.zeros((80,78),dtype=np.int64)
 for j in range(39):D[j,j]=1;D[39,j]=-1;D[40+j,39+j]=1;D[79,39+j]=-1
 hin=40*np.eye(78,dtype=np.int64);hin[:39,:39]-=1;hin[39:,39:]-=1
 assert np.array_equal((D.T@D)@hin,40*np.eye(78,dtype=np.int64))
 u=U@D@hin;v=V@D
 positions=[('origin',{}),('symmetric',{0:1}),('two_coordinate',{0:1,1:2}),
   ('mixed_four',{0:1,1:2,39:-1,40:3}),
   ('mixed_eight',{0:1,1:2,2:-1,3:3,39:-2,40:1,41:2,42:-1})]
 rows=[]
 for name,kval in positions:
  k=np.zeros(78,dtype=np.int64)
  for i,z in kval.items():k[i]=z
  t=400+v@k
  prs=[]
  for p in (10007,10009):
   up=u%p;vp=v%p;tp=t%p
   T=(up.T@(((tp*tp)%p)[:,None]*up))%p
   b=(up.T@((tp*tp)%p))%p
   y=solve_mod(T,b,p)
   res=(1-up@y)%p
   W=(up.T@(((tp*res)%p)[:,None]*vp))%p
   C=(32000*solve_mod(T,W,p))%p
   skew=(C-C.T)%p
   rank=rank_mod(skew,p)
   det=det_mod(skew,p)
   assert (det!=0)==(rank==78)
   prs.append(dict(prime=p,exact_Fp_curvature_rank=rank,exact_Fp_det=det,exact_T_det=det_mod(T,p)))
  rows.append(dict(label=name,coordinate_integer_vector={str(i):z for i,z in kval.items()},
       q_parameterization='q = (1/sqrt20)/10 * D*k',
       min_absolute_affine_numerator=int(min(abs(t))),modular_certificates=prs))
  print('RANK STRATA',name,[r['exact_Fp_curvature_rank'] for r in prs],flush=True)
 assert rows[1]['modular_certificates'][0]['exact_Fp_curvature_rank']==16
 assert all(z['exact_Fp_curvature_rank']==78 for row in rows[3:] for z in row['modular_certificates'])
 return dict(status='PASS',physical_configuration_dimension=78,
   exact_modular_point_certificates=rows,
   generic_rank_over_Q=78,
   generic_full_rank_proof='At explicit mixed_four q, the 78x78 rational curvature has a nonzero determinant modulo primes10007 and10009 after exact invertible kinetic-metric elimination. Therefore the numerator of this rational determinant is not the zero polynomial; hence rank78 holds on a nonempty Zariski-open set where T remains invertible. General rational symplectic nondegeneracy is generic, unlike symmetry-reduced rank16 q.',
   important_scope='This is an intrinsic two-form of the mathematical differential Hamiltonian, not spacetime metric, physical magnetic field, ground-state irrep or proof of an energy gap.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round15_magnetic_generic_fullrank.json').write_text(json.dumps(d,indent=2)+'\n')
 print('GENERIC FULL RANK',[(x['label'],x['modular_certificates'][0]['exact_Fp_det']) for x in d['exact_modular_point_certificates']])
