"""Quantum 78D current-square Hamiltonian: test star displacement on the
low-energy *centered complex-Gaussian* 11769 trial (not the inferior
star-adapted real-Gaussian of Round18).
Uses exact Wick expectation for any coherent means and Gaussian covariance.
Variational upper bounds only.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
from w33_20261009_round18_classical_star_squeezed_trial import anchor

def main():
 g=H.geometry();trial=H.exact_trial()
 C0,C0i=H.spectral_covariance(g)
 u,v=g['u'],g['v']
 d=np.diag(g['s']);a=1/np.sqrt(20)
 U=np.rint(40*u).astype(np.int64);V=np.rint(40*v).astype(np.int64)
 samples=[]
 for star in (0,1,40,41):
  q0,p0=anchor(star,U,V)
  qlin=v@q0;plin=u@p0
  def energy(x):
   cq,cp,logt,f=x
   t=np.exp(logt)
   C=t*C0;Ci=C0i/t
   phase=f*d
   sx=np.einsum('ei,ei->e',v@C,v)/2
   sy=np.einsum('ei,ei->e',u@(Ci+phase@C@phase),u)/2
   cxy=np.einsum('ei,ei->e',v@C@phase,u)/2
   X=a+cq*qlin;Y=a+cp*plin
   return float(np.sum((X*X+sx)*(Y*Y+sy)+4*X*Y*cxy+2*cxy*cxy))
  base=np.array([0.,0.,np.log(trial['t']),trial['f']])
  ebase=energy(base)
  assert abs(ebase-trial['energy'])<1e-9
  optim=[minimize(energy,x,method='BFGS',options={'maxiter':300,'gtol':1e-8}) for x in [base,base+np.array([.5,.5,0,0]),base+np.array([1.,1.,0.,0]),base+np.array([-.5,-.5,0,0])]]
  best=min(optim,key=lambda x:x.fun)
  t0=trial['t'];f0=trial['f'];C=t0*C0;Ci=C0i/t0;phase=f0*d
  sx=np.einsum('ei,ei->e',v@C,v)/2
  sy=np.einsum('ei,ei->e',u@(Ci+phase@C@phase),u)/2
  cxy=np.einsum('ei,ei->e',v@C@phase,u)/2
  hessian=np.array([[2*np.sum(qlin**2*(a*a+sy)),4*np.sum(qlin*plin*(a*a+cxy))],
                    [4*np.sum(qlin*plin*(a*a+cxy)),2*np.sum(plin**2*(a*a+sx))]])
  eig=np.linalg.eigvalsh(hessian)
  assert min(eig)>0
  samples.append(dict(star=star,centered_energy=ebase,optimized_energy=float(best.fun),
    centered_displacement_hessian_eigenvalues=eig.tolist(),
    optimized_q_and_p_star_displacements=best.x[:2].tolist(),params_t_f=[float(np.exp(best.x[2])),float(best.x[3])],
    gradient_inf=float(max(abs(best.jac))),optimization_success=bool(best.success)))
 assert max(z['optimized_energy'] for z in samples)-min(z['optimized_energy'] for z in samples)<1e-4
 out=dict(status='PASS',samples=samples,
  ansatz='Complex centered 11769 invariant covariance t*C0 and phase f*diag(s), with qmean=s*qstar and pmean=r*pstar. Three Wick covariances and nonzero means retained exactly at double precision.',
  conclusion='Numerically optimized coherent displacement along four sampled star directions within this specified 4-parameter family; no global-minimum proof and no rigorous vacuum lower bound.',
  scope='Variational energy is an upper bound to infimum, not a proof of its location, uniqueness, or mass gap.')
 (ROOT/'data/w33_20261009_round19_vacuum_displaced_complex_gaussian.json').write_text(json.dumps(out,indent=2)+'\n')
 print('VACUUM',[(z['star'],z['optimized_energy'],z['optimized_q_and_p_star_displacements']) for z in samples], 'CENTERED',trial['energy'],flush=True)
if __name__=='__main__':main()
