"""A supplied classical-quantum mean-field rate action, with exact analytic limits in the companion report. Numerical stationary points are not global-optimum certificates."""
import sys,pathlib,itertools,json,math
import numpy as np
if hasattr(sys.stdout,'reconfigure'):
 sys.stdout.reconfigure(encoding='utf-8',errors='replace')
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_pass12055_microscopic_tick_model import HS,PROJ,ADJ
PI=np.eye(9)[None,:,:]-HS
def entropy(vals):
 a=np.asarray(vals);a=a[a>0];return -float(np.dot(a,np.log(a)))
def free(phi,T):
 e=np.linalg.eigvalsh(np.tensordot(phi,HS,axes=1));e0=e.min()
 return float(e0-T*np.log(np.exp(-(e-e0)/T).sum()))
def objective(phi,T,kappa=1):return free(phi,T)-kappa*T*entropy(phi)
def soft(x):
 a=np.exp(x-np.max(x));return a/a.sum()
def descent(rho,T):
 prev=float('inf')
 for n in range(2000):
  phi=soft(np.real(np.einsum('aij,ji->a',PI,rho))/T)
  Q=np.tensordot(phi,PI,axes=1);e,U=np.linalg.eigh(Q);prob=soft(e/T);rho=(U*prob)@U.conj().T
  value=objective(phi,T)
  assert value<=prev+1e-10
  if abs(prev-value)<1e-13:break
  prev=value
 return {'objective':value,'iterations':n+1,'rate_entropy':entropy(phi),'qutrit_entropy':entropy(prob),
         'rate_max':float(phi.max()),'rho_eigenvalues':prob.tolist(),'dominant_ticks':np.flatnonzero(phi>phi.max()*.05).tolist()}
def main():
 e0=np.zeros(120);e0[0]=1
 # The all-zero computational state is a common eigenstate of four diagonal Paulis.
 rho=np.zeros((9,9));rho[0,0]=1
 expected=np.real(np.einsum('aij,ji->a',PI,rho));context=np.flatnonzero(expected>1-1e-10)
 assert len(context)==4
 c=np.zeros(120);c[context]=.25
 print('context',context.tolist(),'Tc',1/math.sqrt(360),flush=True)
 out={'status':'SUPPLIED_MEAN_FIELD_MODEL_WITH_RATE_ENTROPY',
      'model':'H_N=(1/N) sum_ij h_{a_i}^{(j)}, with N classical tick labels and N two-qutrit copies',
      'effective_action':'Phi_T(phi)=F_T(phi)+T sum_a phi_a log(phi_a)',
      'rate_count_generalization':'With N classical labels and M quantum copies, kappa=N/M gives Phi=F+kappa*T*sum phi log phi. The low-temperature minimum divided by T is -max(log3,kappa*log4).',
      'low_T_event_context_boundary_kappa':math.log(3)/math.log(4),
      'event_phase_scope':'For 0<kappa<log3/log4 the zero-temperature accumulation points are single event ticks; above it they are four-tick contexts. The count ratio is supplied, not fixed by W33. No local rate kinetics or physical E8 vacuum coupling is derived.',
      'scope':'The action is derived for this specified all-to-all model. The coupling and ensemble are supplied, not selected by W33. Stationary points below are not global-minimum certificates.',
      'low_temperature_global_limit':'min Phi_T / T -> -log(4); zero-energy product states maximize total classical+quantum entropy at a four-tick stabilizer context, not a single event tick.',
      'global_disordering_transition_bounds':{'lower':2/(3*math.log(270)),'upper':math.sqrt(3)},
      'transition_proof':'A context product trial has E=0 and entropy log4; the uniform product has E=2/3 and entropy log1080, so uniform is not globally minimizing below 2/(3 log270). Pinsker plus ||delta Q||_F<=sqrt3||delta phi||_2 proves uniform uniquely global for T>sqrt3. Uniform is strictly locally stable for T>1/sqrt360, below the lower bound on the global transition; the global loss of order is therefore discontinuous in this mean-field model.',
      'context_ticks':context.tolist(),'uniform_hessian_spinodal_T':1/math.sqrt(360),'rows':[]}
 for T in [.005,.01,.02,.04,.052,.06,.08,.1,.2]:
  row={'T':T,'single_tick':objective(e0,T),'four_tick_context':objective(c,T),
       'uniform':objective(np.ones(120)/120,T),
       'stationary_from_context':descent(rho,T),'stationary_from_tick':descent(PI[0]/3,T),
       'uniform_hessian_contrast':120*T-1/(3*T)}
  out['rows'].append(row);print(json.dumps(row),flush=True)
 (R/'data/w33_20261031_tick_rate_entropy.json').write_text(json.dumps(out,indent=2))

if __name__=="__main__":main()
