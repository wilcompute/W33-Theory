"""TOE38 independent theta-null perturbation proof and modular frame
warning. Independently reproduces prior 11872 slopes, then derives
the exact moment-determinant leading coefficient and measures
the effect of an ENTANGLING modular CZ shear on Schmidt entropy.
"""
from pathlib import Path
import sys,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2
OUT=ROOT/'data/w33_20261010_toe38_theta_moment_modular_frame.json'
def moments(tau,N=24):
 n=np.arange(-N,N+1)
 out=np.empty((3,3),dtype=complex)
 for a in range(3):
  x=n+a/3
  w=np.exp(3j*np.pi*tau*x*x)
  for r in range(3):out[a,r]=np.sum((x**r)*w)
 return out
def analyze():
 tau1=.173+1.07j;tau2=.286+1.29j
 eps0=.024*np.exp(.37j)
 def m(eps):
  O=np.array([[tau1,eps],[eps,tau2]],dtype=complex)
  return theta_null_2(O,N=24).reshape(3,3)
 U,V=moments(tau1),moments(tau2)
 # det expansion selects r=0,1,2 exactly, other order>=4
 analytic=(6j*np.pi)**3/2*np.linalg.det(U)*np.linalg.det(V)
 epslist=[eps0,eps0/2,eps0/4]
 svs=[];det_ratio=[]
 for e in epslist:
  M=m(e);sv=np.linalg.svd(M,compute_uv=False)
  svs.append([float(x) for x in sv])
  det_ratio.append(float(abs(np.linalg.det(M)/(analytic*e**3)-1)))
 assert det_ratio[-1]<.04,det_ratio
 slopes=[float(np.log((svs[0][j]/svs[1][j]))/np.log(2)) for j in (1,2)]
 assert abs(slopes[0]-1)<.03 and abs(slopes[1]-2)<.03,slopes
 # CP: O->-conj O is complex conjugation on coefficients,
 # hence Schmidt invariance. (existing Pass11869)
 O=np.array([[tau1,eps0],[eps0,tau2]],dtype=complex)
 cp=theta_null_2(-O.conj(),N=24).reshape(3,3)
 ss_cp=np.linalg.svd(cp,compute_uv=False)
 assert np.allclose(ss_cp,svs[0],atol=1e-11)
 # modular shear changes marking but acts on psi by CZ;
 # on an exactly product theta matrix, CZ turns it into rank3.
 M0=m(0);omega=np.exp(2j*np.pi/3)
 CZ=np.array([[omega**(a*b) for b in range(3)] for a in range(3)])
 M1=m(1)
 shear_error=float(np.max(abs(M1-CZ*M0)))
 assert shear_error<1e-11,shear_error
 s0=np.linalg.svd(M0,compute_uv=False)
 s1=np.linalg.svd(M1,compute_uv=False)
 assert s0[1]/s0[0]<1e-10
 assert s1[2]/s1[0]>1e-10,s1
 def entropy(mat):
  s=np.linalg.svd(mat,compute_uv=False);p=(s*s)/sum(s*s)
  return float(-sum(x*np.log(x) for x in p if x>1e-16))
 result=dict(status='PASS',base_moduli=[str(tau1),str(tau2)],
  moment_series='Theta_ab(eps)=Σ_{r≥0}(6π i eps)^r u_r(a)v_r(b)/r!, with u_r(a)=Σ_n(n+a/3)^r exp(3πi τ1(n+a/3)^2). Each order-r coefficient has matrix rank1.',
  determinant_first_nonzero_term='det Theta(eps)=((6πi)^3/2) det[u0,u1,u2] det[v0,v1,v2] eps^3+O(eps^4).',
  determinant_leading_coefficient_magnitude=float(abs(analytic)),
  eps_magnitudes=[float(abs(e)) for e in epslist],
  singular_values=svs,log2_halfsize_slopes_sigma2_sigma3=slopes,
  leading_determinant_relative_errors=det_ratio,
  CP_schmidt_invariance_max_abs_difference=float(max(abs(np.array(svs[0])-ss_cp))),
  modular_shear_CZ_coefficient_error=shear_error,
  product_original_normalized_small_singular_values=(s0/s0[0]).tolist(),
  product_after_integral_omega12_shear_normalized_singular_values=(s1/s1[0]).tolist(),
  entropy_before_shear_nats=entropy(M0),
  entropy_after_shear_nats=entropy(M1),
  interpretation='The 1:eps:eps² hierarchy of Pass11872 arises from a rank1 moment expansion, not a free mass prediction. The modular transformation Omega12→Omega12+1 acts via ENTANGLING CZ on a marked two-qutrit tensor factorization and generally maps a rank1 theta matrix to rank3, although the principally polarised torus is modularly equivalent. Therefore Schmidt entropy in a fixed marking is NOT a physical modular-invariant observable. By contrast generalised CP complex conjugates the state and preserves its Schmidt singular values.',
  source_priority='Pass11869–11873 already established the theta-Clifford transform and observed Schmidt scaling. New here: explicit determinant leading coefficient, cross-checked singular slopes, and modular-frame/gauge noninvariance of two-qutrit entanglement under shear.',
  physics_boundary='No Yukawa map, chiral fermions, fixed modulus, dynamical CP breaking, or physical generations obtained.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('TOE38 THETA eps slopes',slopes,'det rel errors',det_ratio,'shear entanglement',result['entropy_before_shear_nats'],result['entropy_after_shear_nats'],flush=True)
 return result
if __name__=='__main__':analyze()
