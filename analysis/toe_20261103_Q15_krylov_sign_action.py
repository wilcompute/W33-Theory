#!/usr/bin/env python3
"""Matrix-free Lanczos approximation to overlap-sign action at 40k Q15.

This is NOT a topological index: no sign trace or chiral measure computed.
For each input vector the Lanczos function action is checked at Krylov
dimensions. Also compute low Ritz estimates of H^2 via LOBPCG.
"""
from pathlib import Path
import sys,json,math,time
import numpy as np
from scipy.sparse.linalg import LinearOperator,lobpcg
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261103_sparse_exotic_chiral_q15 import kernel,grammas
def lanczos_sign(H,v,iterations=96):
 n=len(v);norm=np.linalg.norm(v);q=v/norm
 Q=np.zeros((n,iterations),complex)
 diag=[];off=[]
 prev=np.zeros(n,complex)
 beta=0.
 for j in range(iterations):
  Q[:,j]=q
  w=H@q
  a=np.vdot(q,w).real
  w-=a*q+beta*prev
  # full reorth to preserve spectral action in finite precision; 40k*128 ~82MB
  w-=Q[:,:j+1]@(Q[:,:j+1].conj().T@w)
  b=np.linalg.norm(w)
  diag.append(a)
  if j+1<iterations: off.append(b)
  if b<1e-13: break
  prev=q
  q=w/b
 m=len(diag)
 T=np.diag(diag)
 for k,z in enumerate(off[:m-1]):
  T[k,k+1]=T[k+1,k]=z
 vals,u=np.linalg.eigh(T)
 f=u@((np.sign(vals)*u[0].conj())*norm)
 return Q[:,:m]@f,{'iterations':m,'min_abs_Ritz':float(min(abs(vals))),'krylov_norm':float(np.linalg.norm(Q[:,:m]@f))}
def main():
 t=time.perf_counter()
 H,_=kernel(10,15)
 n=H.shape[0]
 A=LinearOperator((n,n),matvec=lambda v:H@(H@v),dtype=complex)
 rng=np.random.default_rng(20261103)
 X=rng.standard_normal((n,3))+1j*rng.standard_normal((n,3))
 low,vec,hist=lobpcg(A,X,largest=False,tol=1e-4,maxiter=90,
  retResidualNormsHistory=True)
 residuals=[float(np.linalg.norm(A@vec[:,j]-low[j]*vec[:,j])) for j in range(3)]
 print('LOBPCG',json.dumps({'lambda_H2_Ritz':low.tolist(),'residuals':residuals,'iterations':len(hist)}),flush=True)
 v=rng.standard_normal(n)+1j*rng.standard_normal(n)
 v/=np.linalg.norm(v)
 res=[]
 old=None
 for m in (24,48,72,96,128):
  out,info=lanczos_sign(H,v,m)
  diff=float(np.linalg.norm(out-old)) if old is not None else None
  old=out
  res.append({'m':m,'norm_sign_H_v':float(np.linalg.norm(out)),
    'change_from_previous_lanczos_m':diff,**info})
  print('LAN',json.dumps(res[-1]),flush=True)
 second,_=lanczos_sign(H,old,128)
 signed_sq_error=float(np.linalg.norm(second-v))
 twist=np.exp(1j*rng.uniform(-np.pi,np.pi,size=10**4))
 Hg,_=kernel(10,15,twist=twist)
 sitephase=np.repeat(twist,4)
 signed_g,_=lanczos_sign(Hg,sitephase*v,96)
 signed_ref,_=lanczos_sign(H,v,96)
 gauge_error=float(np.linalg.norm(signed_g-sitephase*signed_ref))
 print('SQUARED',signed_sq_error,'GAUGE_SIGN',gauge_error,flush=True)
 assert np.isfinite(signed_sq_error)
 assert abs(np.linalg.norm(old)-1)<.002
 assert gauge_error<1e-9
 out={'status':'PASS_MATRIX_FREE_Q15_L10_KRYLOV_OVERLAP_SIGN_VECTOR_DIAGNOSTIC',
  'L':10,'q':15,'dimension':n,'nonzeros':int(H.nnz),
  'H2_smallest_ritz_estimates':low.tolist(),'H2_ritz_residual_norms':residuals,
  'H2_Ritz_iterations':len(hist),'krylov_m_comparisons':res,
  'approx_sign_H_squared_on_single_vector_relative_error':signed_sq_error,
  'approx_sign_H_gauge_transform_vector_relative_defect':gauge_error,
  'wall_seconds':time.perf_counter()-t,
  'spectral_scope':'LOBPCG gives upper bounds to smallest H² eigenvalues (Ritz variational principle), NOT a rigorous gap lower bound. Lanczos sign action on ONE complex random vector plus its squared action, NOT full sign matrix, sign trace, large-Q index or proof of uniform locality or a Weyl measure. Potential tiny Ritz values make sign discontinuous, so finite Krylov convergence must be checked.',
  'index_scope':'The exact continuum charge-15 index magnitude for unit flux12 x unit flux34 is 225 if the admissible lattice background is in the corresponding index stable sector; not numerically established for this L10 kernel.',
  'prior_methods':['https://doi.org/10.1007/s11005-026-02080-w']}
 (ROOT/'data/toe_20261103_Q15_krylov_sign_action.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
