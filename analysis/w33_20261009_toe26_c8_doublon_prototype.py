"""Round26 minimal nontrivial 8-site W33 apartment/Levi cycle
Bose-Hubbard spectroscopy prototype: exact 36-state two-boson
diagonalization, weak-coupling failure checks and graph-specific fingerprint.
No physical experimental device is built.
"""
from pathlib import Path
import json,itertools,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe26_c8_doublon_prototype.json'
def build(n=8):
 basis=list(itertools.combinations_with_replacement(range(n),2))
 indices={a:i for i,a in enumerate(basis)}
 A=np.zeros((n,n),dtype=float)
 for i in range(n):A[i,(i+1)%n]=A[(i+1)%n,i]=1
 H=np.zeros((len(basis),len(basis)))
 doublon=np.zeros(len(basis))
 for j,state in enumerate(basis):
  occ={a:state.count(a) for a in set(state)}
  if state[0]==state[1]:doublon[j]=1
  for a,num in occ.items():
   for b in np.flatnonzero(A[a]):
    dst=list(state);dst.remove(a);dst.append(int(b))
    k=indices[tuple(sorted(dst))]
    H[k,j]-=math.sqrt(num*(occ.get(int(b),0)+1))
 assert np.allclose(H,H.T)
 pair=np.flatnonzero(doublon)
 assert len(pair)==n
 K=H[pair,:]@H[:,pair]
 assert np.allclose(K,4*np.eye(n)+2*A)
 return H,doublon,pair,A
def run():
 H,D,I,A=build()
 eigen=np.linalg.eigvalsh(A)
 spectral=[2,math.sqrt(2),0,-math.sqrt(2),-2]
 multiplicity=[1,2,2,2,1]
 assert all(sum(abs(eigen-l)<1e-10)==m for l,m in zip(spectral,multiplicity))
 tMHz=5.
 vals={}
 for UoverT in (8,16,32,64):
  mat=H-UoverT*np.diag(D)
  eig,V=np.linalg.eigh(mat)
  # eight lowest states = doublon band (for U>>t); sign convention
  bound=eig[:8]
  # aggregate split E's into groups by C8 degeneracy; each group can
  # have tiny finite-U differences but translation/reflection enforce them.
  groups=[(0,1),(1,3),(3,5),(5,7),(7,8)]
  centers=[float(np.mean(bound[a:b])) for a,b in groups]
  exact_gap=centers[1]-centers[0]
  leading=(2/UoverT)*(2-math.sqrt(2))
  assert exact_gap>0
  weights=[float(np.sum(V[0,a:b]**2)) for a,b in groups]
  # V[0] corresponds to |0,0>, and band weights include leakage
  leakage=float(1-sum(weights))
  vals[str(UoverT)]=dict(bound_band_centers_over_t=centers,
   first_gap_over_t=exact_gap,leading_first_gap_over_t=leading,
   finite_U_gap_relative_error=exact_gap/leading-1,
   doublon_initial_state_band_probabilities=weights,
   probability_leaked_to_scattering_bands=leakage,
   first_gap_hypothetical_MHz=exact_gap*tMHz,
   ten_gap_cycles_hypothetical_us=10/(exact_gap*tMHz))
  print('C8 PROTOTYPE',UoverT,'gap/t',exact_gap,'leading',leading,'leakage',leakage,flush=True)
 assert abs(vals['64']['finite_U_gap_relative_error'])<abs(vals['8']['finite_U_gap_relative_error'])
 first=2-math.sqrt(2)
 ratios=[(2-l)/first for l in spectral]
 assert abs(ratios[2]-(2+math.sqrt(2)))<1e-10
 rec=dict(status='PASS',prototype='8-site 8-link native W33 Levi apartment C8',
  native_graph_girth=8,two_boson_fock_dimension=36,
  two_boson_bosonic_site_capacity=2,
  exact_pair_perturbation_numerator='4 I_8+2 A_C8',
  five_pair_band_multiplicities=multiplicity,
  exact_asymptotic_local_spectral_weights=[m/8 for m in multiplicity],
  exact_leading_gap_ratios=ratios,
  W33_full_80_comparison='Full Levi W33 has five bands multiplicities [1,24,30,24,1]/80 and second-to-first normalized gap 4/(4-sqrt6)=2.5797959. C8 alone has five bands [1,2,2,2,1]/8, second-to-first ratio 2/(2-sqrt2)=3.41421356. C8 is a primitive interaction/readout prototype, not evidence of full W33 five-band spectrum.',
  modeled_U_over_t_cases=vals,
  illustrative_hopping_t_over_h_MHz=tMHz,
  experimental_minimum='Eight sites arranged in a single length-eight bipartite ring, attractive onsite bosonic two-particle U, pair loading on one site, coherent return/correlation spectroscopy, independent calibration of t and U, measured loss/dephasing/disorder. Full 80-site/160-link W33 design only after this primitive test.',
  no_hardware_claim='All spectra are computed for a specified toy Hamiltonian, not experimental data. This prototype does not test an E8 embedding or gravity.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
