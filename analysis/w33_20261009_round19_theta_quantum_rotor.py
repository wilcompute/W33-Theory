"""Quantum rotor toy reduction of a native W33 three-plaquette theta.
Full native 160-link U(1) gauge Hamiltonian is defined analytically by the
1620-cycle incidence C; this numerical truncation keeps only two loop fluxes
of a three-loop theta. Does NOT solve full 160-link dynamics.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
def rotor_matrix(cut,E=1.0,g=1.0):
  states=[(i,j) for i in range(-cut,cut+1) for j in range(-cut,cut+1)]
  where={p:k for k,p in enumerate(states)}
  rows=[];cols=[];v=[]
  steps=[(2,0),(-2,0),(0,2),(0,-2),(2,2),(-2,-2)]
  for i,(m,n) in enumerate(states):
    rows.append(i);cols.append(i);v.append(.5*E*(m*m+n*n))
    for a,b in steps:
      k=where.get((m+a,n+b))
      if k is not None:rows.append(k);cols.append(i);v.append(g/2)
  h=coo_matrix((v,(rows,cols)),shape=(len(states),len(states))).tocsr()
  assert np.linalg.norm((h-h.T).data)<1e-12
  return h,states
def main():
 out=[]
 for cut in (4,6,8):
   H,states=rotor_matrix(cut,E=.5,g=1.)
   vals,vec=eigsh(H,k=3,which='SA',tol=1e-11,maxiter=15000)
   perm=np.argsort(vals);vals=vals[perm];vec=vec[:,perm]
   flip=np.array([states.index((-m,-n)) for m,n in states])
   # Ground Fourier coefficients can be chosen real and inversion-even.
   tr=float(abs(np.vdot(vec[:,0],vec[flip,0])))
   assert tr>.999999
   assert vals[1]-vals[0]>1e-4
   out.append(dict(fourier_cut=cut,hilbert_dim=len(states),
      lowest_energy=float(vals[0]),first_gap=float(vals[1]-vals[0]),
      parity_mirror_absolute_overlap=tr))
 print('THETA ROTOR',out,flush=True)
 result=dict(status='PASS',native_theta_loop_relation='There are three W33 8-cycles with oriented fluxes F1+F2+F3=0; independent coordinates x,y give F3=-x-y.',
  full_formal_160_link_hamiltonian='H = (E/2) sum_e(-i d/dtheta_e)^2 + g sum_(c in 1620 eight_cycles) cos(2*(C theta)_c), with node gauge redundancy (79) and 81 cycle degrees. Its physical spectrum has NOT been computed.',
  truncated_theta_rotor='H_theta=(E/2)(-d_x^2-d_y^2)+g[cos(2x)+cos(2y)+cos(2(x+y))], E=1/2, g=1, 2D Fourier cutoff ±4,±6,±8.',
  samples=out,
  limitations='Fourier cutoffs approximate a 2D toy only; the chosen effective kinetic metric is not derived by projecting the full graph electric operator; the ground parity overlap is numerical and no thermodynamic symmetry breaking or physical chiral vacuum is established.')
 (ROOT/'data/w33_20261009_round19_theta_quantum_rotor.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
