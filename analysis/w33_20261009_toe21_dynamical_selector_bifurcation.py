"""An explicit symmetry-invariant normalized focusing DNLS energy on the
W33 80-node Levi graph, and a rigorous first-order-like coexistence window.
Finite quantum linear Perron Frobenius forbids exact spontaneous selection.
No claim that the focusing quartic or couplings follow from fundamental physics.
"""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain
def matrix():
 *_,flags,fi,E,T,D,M,L=chain()
 A=np.zeros((80,80))
 for p,l in flags:A[p,40+l]=A[40+l,p]=1.
 assert np.all(A.sum(0)==4)
 return A
def minimize_focusing(g,seed=2121):
 A=matrix();rng=np.random.default_rng(seed)
 u=np.ones(80)/math.sqrt(80)
 def f(y):
  norm=np.linalg.norm(y)
  x=y/norm
  energy=-float(x@A@x)-g*float((x**4).sum())
  d=-2*A@x-4*g*x**3
  return energy,(d-x*np.dot(x,d))/norm
 starts=[u]+[np.eye(80)[i]+.04*u for i in (0,1,40,41)]
 starts +=[rng.random(80) for j in range(3)]
 sols=[]
 for y in starts:
  r=minimize(f,y,method='L-BFGS-B',jac=True,
   options={'maxiter':500,'ftol':2e-13,'gtol':3e-8})
  x=r.x/np.linalg.norm(r.x)
  sols.append((float(r.fun),float(np.max(x*x)),float(np.sum(x*x)**2/np.sum(x**4)),float(np.max(np.abs(r.jac)))))
 return sorted(sols)
def run():
 A=matrix()
 eigen=np.linalg.eigvalsh(A)
 assert abs(eigen[-1]-4)<1e-10 and abs(eigen[-2]-math.sqrt(6))<1e-10
 g_trial=320/79
 g_hessian=20*(4-math.sqrt(6))
 assert g_trial<g_hessian
 # All PSp-invariant amplitudes have point-constant and line-constant
 # components. For 0<g<=160 their nonnegative-energy minimum is uniform.
 # Trial basis vector energy -g beats uniform -4-g/80 for g>320/79.
 for g in (5,8,16,25,30):
  assert g>g_trial and g<g_hessian and g<160
  assert -g<-4-g/80
 sims={}
 for g in (0,3,5,10,20,32):
  sol=minimize_focusing(g)
  sims[str(g)]=dict(best_energy=sol[0][0],
    max_site_probability=sol[0][1],participation_ratio=sol[0][2],
    uniform_energy=-4-g/80,basis_vector_trial_energy=-g,
    converged_gradient_inf=sol[0][3])
  print('SELECT',g,round(sol[0][0],7),round(sol[0][1],7),flush=True)
 assert abs(sims['0']['best_energy']+4)<1e-7
 assert sims['5']['best_energy'] < -4-5/80-0.01
 out=dict(status='PASS',finite_graph=80,Levi_degree=4,
   model='Normalized complex amplitude psi on the 80 Levi nodes, sum |psi_i|²=1; E=-t psi†A psi-g sum |psi_i|^4, real nonnegative phase representative suffices by graph connectedness and Perron-Frobenius. t=1 units.',
   exact_symmetry='The same A and quartic onsite term are invariant under ALL automorphisms of the uncolored Levi graph; in particular type-preserving PSp(4,3).',
   exact_uniform_energy='-4t-g/80',exact_basis_trial_energy='-g',
   trial_crossing_g_over_t=320/79,local_uniform_hessian_threshold_g_over_t=g_hessian,
   certified_coexistence_interval='320/79 < g/t < 20*(4-sqrt(6))',
   theorem='For g/t>320/79 (~4.050633), a normalized site-basis vector has strictly lower energy than uniform. For g/t<20*(4-sqrt6) (~31.010205), the uniform PSp-invariant state has strictly positive Hessian for ALL transverse tangent modes; hence it is a strict local minimum. Every PSp-invariant positive normalized state must be constant on the point and line fibers; for g/t<160, the minimum of the PSp-invariant family is uniform. Thus throughout the displayed interval all global minimizers BREAK PSp(4,3) while the symmetric state stays locally stable. This is a finite nonlinear mean-field symmetry-breaking bifurcation (metastability), NOT a quantum spontaneous-symmetry-breaking theorem.',
   local_stability_derivation='For x=sqrt(1-eps²)u+eps v, v perp u, ||v||=1 eigenvector of A with eigenvalue lambda, E(x)-E(u)=[t(4-lambda)-4g/80]eps²+O(eps³). Largest transverse eigenvalue sqrt6, so positive if g<20t(4-sqrt6).',
   quantum_nogo='For any finite 80-level single-particle Hermitian H=-tA (t>0) the Perron-Frobenius ground eigenvector is unique, positive, and fully symmetry invariant. Nonlinear focusing mean-field energy is a NEW assumption and cannot by itself establish exact finite-system quantum degenerate vacua; a thermodynamic limit and dynamical quartic origin are missing.',
   numerical_multistart=sims,
   physically_free_parameters=['t hopping energy overall scale','g focusing interaction magnitude','choice of state preparation and thermodynamic scaling'])
 (ROOT/'data/w33_20261009_toe21_dynamical_selector_bifurcation.json').write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
