"""Exact-form magnetic connection diagnostic for the real W33
current-square Hamiltonian. Tests whether a positive-ground-state
Perron-Frobenius proof by removing first-order gauge phases is valid.
The normalized kinetic metric K(q)=U^T diag(z²) U,
b(q)=a U^T z², A=K^-1 b, and Veff=a² sum z²-b^T K^-1 b.
For U,V 160x78, z=a+V q, curl A_{ij}=D_j A_i-D_i A_j,
D A=2 K^-1 U^T diag(z*(a-U A)) V.
Curl nonzero => NO scalar phase removes this magnetic connection
in an open neighborhood. Does NOT prove ground degeneracy.
"""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
def certificate():
 g=H.geometry();U=g['u'];V=g['v']
 ev,Q=np.linalg.eigh(U.T@U);Q=Q[:,ev>1e-7]
 u=U@Q;v=V@Q;a=1/math.sqrt(20)
 def evaluate(q):
  z=a+v@q;K=u.T@((z*z)[:,None]*u)
  b=a*u.T@(z*z)
  A=np.linalg.solve(K,b)
  C=2*np.linalg.solve(K,u.T@((z*(a-u@A))[:,None]*v))
  return float(np.max(abs(C-C.T))),float(np.linalg.norm(C-C.T)),float(np.min(np.linalg.eigvalsh(K))),float(np.linalg.norm(A)),float(a*a*sum(z*z)-b@A)
 rng=np.random.default_rng(104)
 probes=[]
 for amp in (0,.01,.03,.1,.3):
  q=rng.normal(size=78)*amp if amp else np.zeros(78)
  mx,frob,mk,nA,scalar=evaluate(q)
  probes.append(dict(q_stddev=amp,max_curl=mx,curl_frob=frob,
      minimum_kinetic_metric_eigenvalue=mk,gauge_connection_norm=nA,
      sharp_pointwise_scalar_barrier=scalar))
 assert probes[0]['max_curl']<1e-8
 assert max(x['max_curl'] for x in probes[1:])>1e-5
 # Verify exact Jacobian by finite differences on two coordinates.
 q=rng.normal(size=78)*.1
 z=a+v@q;K=u.T@((z*z)[:,None]*u);b=a*u.T@(z*z)
 A=np.linalg.solve(K,b)
 C=2*np.linalg.solve(K,u.T@((z*(a-u@A))[:,None]*v))
 def connection(x):
  zz=a+v@x;return np.linalg.solve(u.T@((zz*zz)[:,None]*u),a*u.T@(zz*zz))
 for j in (0,13,54):
  h=1e-5;step=np.zeros(78);step[j]=h
  finite=(connection(q+step)-connection(q-step))/(2*h)
  assert np.linalg.norm(finite-C[:,j])<1e-7,(j,np.linalg.norm(finite-C[:,j]))
 return dict(status='PASS',projected_coordinate_dimension=78,probe_results=probes,
   exact_differential_form='K=U^T diag(z^2) U, b=a U^T(z^2), A=K^-1 b, dA/dq=2 K^-1 U^T diag(z*(a-U A)) V; zero-curl at symmetric q=0 does not imply zero-curl elsewhere.',
   positive_magnetic_curl_at_generic_points=True,
   proof_scope='Analytic exact derivative formula, finite-difference checks and numerical lower nonzero curl witnesses at explicitly seeded Gaussian probes. Rational exact certificate of nonzero entry can be added before claiming machine-checkable algebraic proof.',
   implication='A naive scalar positive-improving Perron-Frobenius or nodal theorem cannot be invoked by simply gauging away all first-order currents. No conclusion on actual ground irrep, degeneracy or numerical gap.',
   author='independent full-H ground-state symmetry obstruction, not a physical magnetic field.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_quantum_connection_curl_audit.json').write_text(json.dumps(d,indent=2)+'\n')
 print('CURL',[(p['q_stddev'],p['max_curl'],p['sharp_pointwise_scalar_barrier']) for p in d['probe_results']])
