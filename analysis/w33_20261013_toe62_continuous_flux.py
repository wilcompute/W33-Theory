"""TOE62 front1: continuous 3-holonomy U(1) fermionic flux potential.

Checks stationary Hessian, gradient, multistart minimizers; numerical
search is NOT a global optimization theorem.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import minimize
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,vs,look,octs,comm,*_=prep()
E=np.asarray(ed,int);V=np.asarray(vs,int)
P=np.rint(np.asarray([cycle_row(x,ed,vs,look,np.zeros(3)).real for x in octs+comm])).astype(int)
assert np.count_nonzero(P@V)==0
def data(theta,beta):
 ph=np.exp(1j*(V@theta))
 H=np.zeros((80,80),complex)
 for k,(a,b) in enumerate(E):
  H[a,b]=-ph[k];H[b,a]=-np.conj(ph[k])
 es,U=np.linalg.eigh(H)
 if beta==np.inf:
  F=float(-np.abs(es).sum()/2)
  t=np.sign(es)
 else:
  F=float(-np.logaddexp(beta*es/2,-beta*es/2).sum()/beta)
  t=np.tanh(beta*es/2)
 C=(U*t)@U.conj().T
 grad=np.zeros(3)
 for k,(a,b) in enumerate(E):
  grad+=-V[k]*np.imag(C[b,a]*ph[k])
 return F,grad
rng=np.random.default_rng(6201)
allrows=[]
for beta in (.5,2.,8.,np.inf):
 starts=[np.array([0.,0.,0.]),np.full(3,np.pi)]+[rng.uniform(-np.pi,np.pi,3) for _ in range(8)]
 fits=[]
 for start in starts:
  f=lambda q:data(q,beta)
  res=minimize(f,start,jac=True,method='BFGS',options={'gtol':3e-9,'maxiter':110})
  t=(res.x+np.pi)%(2*np.pi)-np.pi
  fits.append({'point':t.tolist(),'value':float(res.fun),'grad_inf':float(max(abs(data(t,beta)[1]))),
               'success':bool(res.success)})
 pi=np.full(3,np.pi);Fpi,gpi=data(pi,beta);Fzero,gzero=data(np.zeros(3),beta)
 h=.0004
 Hess=np.column_stack([(data(pi+np.eye(3)[i]*h,beta)[1]-data(pi-np.eye(3)[i]*h,beta)[1])/(2*h) for i in range(3)])
 Hmin=np.linalg.eigvalsh((Hess+Hess.T)/2)
 # independent finite difference gradient at generic configuration
 x=np.array([.31,.77,-1.12]);g=data(x,beta)[1]
 gn=np.array([(data(x+np.eye(3)[i]*1e-5,beta)[0]-data(x-np.eye(3)[i]*1e-5,beta)[0])/2e-5 for i in range(3)])
 assert max(abs(gn-g))<5e-7,(beta,g,gn)
 best=min(fits,key=lambda z:z['value'])
 print('U1',beta,'Fpi',Fpi,'best',best['value'],'theta',best['point'],'Hess',Hmin,flush=True)
 allrows.append({'beta':str(beta),'F_three_pi':Fpi,'F_zero':Fzero,
  'best_local_multistart_value':best['value'],'best_local_theta':best['point'],
  'found_better_than_three_pi':bool(best['value']<Fpi-2e-7),
  'three_pi_stationary_grad_norm_inf':float(max(abs(gpi))),
  'three_pi_Hessian_eigenvalues':Hmin.tolist(),
  'gradient_vs_finite_difference_max':float(max(abs(gn-g))),
  'number_search_starts':len(starts),'optimizer_outputs':fits})
out={'status':'TOE62_CONTINUOUS_U1_HARMONIC_THERMAL_SEARCH',
'bloch_deck_marking_flat_plaquette_PV_max':int(max(abs(P@V).ravel())),
'cases':allrows,
'model':"H_ab(theta)=-exp(i V_e dot theta), H_ba its conjugate. F_beta=-1/beta Tr log[2cosh(beta H/2)] at mu=0; gradient computed from exact spectral derivative; zeroT F=-Tr|H|/2.",
'limitation':"Multistart three-variable local optimization, numerical Hessian and Fermi free energy on a given 80-site free spinless model, NOT a certified continuous torus global minimum, dynamical gauge vacuum, interacting SM, physical CP or fitted fundamental parameter."}
(R/'data/w33_20261013_toe62_continuous_flux.json').write_text(json.dumps(out,indent=2)+'\n')
