"""Finite-N symmetry-selection susceptibility (N=2 and N=3) for the
native 80-site attractive bosonic W33 Levi Hamiltonian.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe22_two_boson_quantum_selector import build as build2
from w33_20261009_toe23_three_boson_vacuum import build as build3
OUT=ROOT/'data/w33_20261009_toe24_quantum_order_parameter_susceptibility.json'
def eigen(H,guess=None):
 if guess is None:guess=np.ones(H.shape[0])/np.sqrt(H.shape[0])
 e,v=eigsh(H,k=1,which='SA',tol=2e-11,maxiter=3500,v0=guess)
 return float(e[0]),v[:,0]
def run():
 outcomes={}
 for N,creator,Us,h in ((2,build2,(0,3,8,16,32),.001),(3,build3,(0,4,8),.001)):
  T,pairs,basis=creator()
  occupation=np.array([sum(x==0 for x in state) for state in basis],dtype=float)
  trial={}
  for U in Us:
   H=T-diags(U*pairs,0)
   e0,psi=eigen(H)
   def meas(sign):
    E,p=eigen(H-diags(sign*h*occupation,0),psi)
    return E,float(np.dot(occupation,p*p))
   Ep,np_=meas(1);Em,nm=meas(-1)
   delta=(np_-nm)/(2*h)
   sec=-(Ep+Em-2*e0)/(h*h)
   assert delta>0 and sec>0
   assert abs(sec-delta)<.02*delta+2e-4,(N,U,delta,sec)
   rec=dict(U_over_t=U,energy0=e0,occupation_plus_h=np_,
     occupation_minus_h=nm,local_susceptibility=delta,
     energy_second_derivative_susceptibility=sec,
     zero_field_density_exact=N/80)
   trial[str(U)]=rec
   print('SUSCEPTIBILITY',N,U,'chi',round(delta,6),'energy_d2',round(sec,6),flush=True)
  outcomes[str(N)]=trial
 assert outcomes['2']['32']['local_susceptibility']>outcomes['2']['0']['local_susceptibility']
 assert outcomes['3']['8']['local_susceptibility']>outcomes['3']['0']['local_susceptibility']
 res=dict(status='PASS',native_graph_vertices=80,
  computational_Hilbert_dimensions={'2':3240,'3':88560},local_pin_field=h,
  quantum_H='H=-t sum_edges(b†_i b_j+b†_j b_i)-U sum_i n_i(n_i-1)/2-h n_0',
  pinned_density_and_susceptibility=outcomes,
  exact_PF_theorem='On finite connected W33 hopping configuration graphs with finite N and t>0 the zero-field ground state is unique and PSp-invariant. Therefore lim_{h->0} <n_0>=N/80 and at any fixed finite N the analytic local susceptibility cannot signify true spontaneous symmetry breaking.',
  physical_next='The response becomes sharply enhanced when attraction forms dimers or trimers; independent Feynman-Hellmann energy-curvature and occupation finite differences agree. A genuine spontaneously chosen vacuum would require a specified thermodynamic sequence, order of limits lim_{h->0}lim_{size->infty}, and a physically derived coupling.',
  provenance='Round22 proved N=2 uniqueness; Round23 did N=3 Hilbert diagonalization. New: external source-field density susceptibility N2,N3, independent curvature check across couplings.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 return res
if __name__=='__main__':run()
