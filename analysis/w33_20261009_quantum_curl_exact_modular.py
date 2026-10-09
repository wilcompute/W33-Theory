"""Exact finite-field certificate of nonzero magnetic curvature of the
actual 160-current W33 quantum Hamiltonian at a rational position.

Use 78 independent configuration coordinates q=D*x, with each D
column a zero-sum point or line difference. Differential vector-field
coefficients use the DUAL basis: U_x=U_ambient*D*(D.T*D)^-1.
This distinction is essential: position gradients V transform by D,
whereas momentum/derivative vectors U transform contravariantly.

At x=(a/10,0,...), a=1/sqrt20, let u=(40 Uamb) D
[40*(D.T D)^-1], v=(40 Vamb)D, t=400+v[:,0].
The rational magnetic connection has curvature
C = 32000*T^-1*u.T diag(t*(1-u*T^-1*b)) v,
T=u.T diag(t²) u, b=u.T(t²).
Exact residues of C_ij-C_ji modulo TWO primes prove curvature !=0,
excluding a local scalar phase gauge of all first-order terms.
This does NOT prove quantum ground degeneracy or a numerical gap.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
def solve_mod(A,b,p):
 n=A.shape[0];rhs=np.asarray(b,dtype=np.int64)
 if rhs.ndim==1:rhs=rhs[:,None]
 X=np.concatenate([A%p,rhs%p],axis=1).astype(np.int64)
 for k in range(n):
  nz=np.flatnonzero(X[k:,k])
  if len(nz)==0:raise ValueError('singular modulo prime')
  j=k+int(nz[0])
  if k!=j:X[[k,j]]=X[[j,k]]
  X[k]=(X[k]*pow(int(X[k,k]),-1,p))%p
  for j in range(n):
   if j!=k and X[j,k]:
    X[j]=(X[j]-int(X[j,k])*X[k])%p
 assert np.array_equal(X[:,:n],np.eye(n,dtype=np.int64))
 return X[:,n:].squeeze()
def certificate():
 geo=H.geometry()
 U0=np.rint(40*geo['u']).astype(np.int64)
 V0=np.rint(40*geo['v']).astype(np.int64)
 D=np.zeros((80,78),dtype=np.int64)
 for j in range(39):D[j,j]=1;D[39,j]=-1
 for j in range(39):D[40+j,39+j]=1;D[79,39+j]=-1
 HinvNum=40*np.eye(78,dtype=np.int64)
 HinvNum[:39,:39]-=np.ones((39,39),dtype=np.int64)
 HinvNum[39:,39:]-=np.ones((39,39),dtype=np.int64)
 assert np.array_equal(D.T@D@HinvNum,40*np.eye(78,dtype=np.int64))
 # u /1600 gives actual derivative coefficients, v /40 gives
 # actual z-factor configuration slopes.
 u=U0@D@HinvNum
 v=V0@D
 t=400+v[:,0]
 uf=u.astype(float);tf=t.astype(float)
 T=uf.T@((tf*tf)[:,None]*uf)
 b=uf.T@(tf*tf)
 assert np.linalg.eigvalsh(T)[0]>1e-5
 y=np.linalg.solve(T,b)
 W=uf.T@((tf*(1-uf@y))[:,None]*v)
 C=32000*np.linalg.solve(T,W)
 anti=C-C.T
 i,j=np.unravel_index(np.argmax(abs(anti)),anti.shape)
 assert i!=j and abs(anti[i,j])>1e-6
 mod_results=[]
 for p in (10007,10009):
  up=u%p;tp=t%p;vp=v%p
  Tmod=(up.T@(((tp*tp)%p)[:,None]*up))%p
  bmod=(up.T@((tp*tp)%p))%p
  yy=solve_mod(Tmod,bmod,p)
  residue=(1-(up@yy))%p
  Wmod=(up.T@(((tp*residue)%p)[:,None]*vp))%p
  cols=solve_mod(Tmod,Wmod[:,[i,j]],p)
  assert cols.shape==(78,2)
  cij=(32000*int(cols[i,1]))%p
  cji=(32000*int(cols[j,0]))%p
  assert (cij-cji)%p!=0
  mod_results.append(dict(prime=p,Cij_mod=cij,Cji_mod=cji,
    antisym_nonzero_residue=(cij-cji)%p,det_T_nonzero_mod_p=True))
 return dict(status='PASS',
    configuration='q=a*(e_0-e_39)/10, a=1/sqrt20; q is on physical 78D sum-zero configuration slice',
    physical_dimension=78,dual_derivative_basis_verified_exactly=True,
    antisymmetric_curvature_entry=[int(i),int(j)],
    approximate_nonzero_curl=float(anti[i,j]),
    modular_certificates=mod_results,
    exact_formula='C=32000*T^-1*u.T*diag(t*(1-u*T^-1*b))*v where u=(40U)D[40(D.T D)^-1],v=(40V)D,t=400+v[:,0],T=u.T diag(t^2)u,b=u.T(t^2)',
    theorem='Curvature of the quantum Hamiltonian first-order connection is nonzero as an exact rational tensor (certified modulo two primes). Therefore no local scalar U(1) gauge can remove the connection around the specified point. Positivity-improving scalar Schr. theorems cannot be applied without a new argument.',
    boundary='No conclusion about actual quantum vacuum irrep or degeneracy, global spectral lower enclosure, experimental magnetism or the Theory of Everything.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_quantum_curl_exact_modular.json').write_text(json.dumps(d,indent=2)+'\n')
 print('EXACT CURVATURE',d['antisymmetric_curvature_entry'],d['approximate_nonzero_curl'],d['modular_certificates'])
