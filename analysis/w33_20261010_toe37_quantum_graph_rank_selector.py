"""TOE37 track3: Quantum rank-changing graph-sector toy selector.
Use SAME W33 Levi graph, p=3 and deck ranks1,2,3. Compute full
Gaussian massive scalar log determinant per vertex:
f_r(m)=1/(2 V_r) sum_j log(lambda_j + m²).
Construct rank-changing 3x3 Hermitian Hamiltonian with offdiag -g
between neighboring sectors and diagonal gamma*f_r + kappa*r.
These are externally chosen transitions and counterterms, NOT native
local graph moves or demonstrated dynamical dimensional selection.
"""
from pathlib import Path
import sys,json,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords,matrix
OUT=ROOT/'data/w33_20261010_toe37_quantum_graph_rank_selector.json'
def run(write=True):
 edges,D,C=wilson();cs=spanning_chords(edges);selected=[cs[i] for i in (5,30,65)]
 p=3
 spectra={}
 for rank in (1,2,3):
  volts=np.zeros((160,rank),dtype=int)
  for j,col in enumerate(selected[:rank]):volts[col,j]=1
  vals=[]
  for k in itertools.product(range(p),repeat=rank):
   theta=2*np.pi*np.array(k)/p
   vals.extend(np.linalg.eigvalsh(matrix(edges,volts,theta)))
  vals=np.sort(np.array(vals))
  assert len(vals)==80*p**rank and abs(vals[0])<1e-10 and vals[1]>0
  spectra[rank]=vals
 energies={}
 for mass in (.1,.5,2.,10.):
  energies[str(mass)]={str(r):float(.5*np.mean(np.log(spectra[r]+mass**2))) for r in (1,2,3)}
 cases=[]
 for mass,kappa,mixing in ((.1,0,.03),(.5,0,.03),(2.,0,.03),(10.,0,.03),(.5,.05,.03),(.5,-.05,.03),(.5,0,.2)):
  f=energies[str(mass)]
  diag=np.array([f[str(r)]+kappa*r for r in (1,2,3)])
  H=np.diag(diag)
  for i in range(2):H[i,i+1]=H[i+1,i]=-mixing
  z,V=np.linalg.eigh(H);prob=V[:,0]**2
  assert abs(float(np.sum(prob))-1)<1e-12
  cases.append(dict(mass=mass,rank_penalty=kappa,transition_amplitude=mixing,
    one_loop_effective_density_by_rank=[f[str(r)] for r in (1,2,3)],
    lowest_energy=float(z[0]),ground_rank_probabilities=[float(y) for y in prob],
    most_probable_rank=int(np.argmax(prob))+1))
  print('RANKTOY',mass,kappa,mixing,'probs',np.round(prob,4),flush=True)
 out=dict(status='PASS',base_W33_Levi_vertices=80,deck_p=3,
   total_vertices_by_rank={str(r):len(v) for r,v in spectra.items()},
   massive_scalar_one_loop_density='f_r(m)= 1/(2 |V_r|) sum_{lambda in spectrum(L_r)} ln(lambda + m²). Gaussian scalar determinant at normalized unit measure; physically requires specifying measure, scalar couplings, and meaningful size normalization.',
   exact_free_hopping_degeneracy='E_min(-t A)=-4t for every rank due to identical 4-regular covers, previously Round36.',
   one_loop_densities=energies,
   quantum_rank_hamiltonian='H_rank = diag(f_r(m)+kappa*r) - g*(|1><2|+|2><1|+|2><3|+|3><2|) on the abstract rank sector basis. The offdiagonal jumps between globally distinct covers, so it is NOT a derived local microscopic geometry move.',
   tested_ground_superpositions=cases,
   no_go='Rank selection depends on external masses, normalization, rank chemical potential and global transition amplitudes, none fixed by W33. Gaussian determinant depends on measure and counterterms. A three-sector Hilbert-space toy cannot establish spontaneous symmetry breaking, gravity, or stable thermodynamic 3D.',
   possible_use='Defines a repeatable effective-sector model and quantifies sensitivity to rank cost and scalar field mass rather than asserting unexplained 3D preference.')
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
