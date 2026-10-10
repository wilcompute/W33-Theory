"""Native 160-link qutrit gauge model: commuting vertex Gauss and
eight-cycle Wilson constraints; exact F3 ranks and logical-sector audit.
This exposes the overconstraint of simultaneously imposing flatness.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain,integer_cycle_basis
from w33_20261009_round19_gauge_cycle_frustration import modrank
from w33_20261009_round18_chirality_plaquette_audit import cycles_touching
from w33_pass1081_1086_core import rank_mod
OUT=ROOT/'data/w33_20261009_toe22_native_gauge_hamiltonian.json'
def run():
 pts,idx,lines,li,edges,tris,flags,fi,E,T,D,M,R=chain()
 Z,chords=integer_cycle_basis(flags)
 phys_edges=[(p,40+l) for p,l in flags]
 cycles=set()
 for j in range(160):cycles.update(cycles_touching(phys_edges,j))
 cycles=sorted(cycles)
 assert len(cycles)==1620
 # Compute the 1620 oriented 8-cycles in this EXACT native coordinate ordering.
 ei={tuple(sorted(e)):j for j,e in enumerate(phys_edges)}
 C=np.zeros((1620,160),dtype=np.int16)
 for i,cyc in enumerate(cycles):
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):
   C[i,ei[tuple(sorted((a,b)))]]=1 if a<b else -1
 assert np.count_nonzero(C,axis=1).min()==8
 assert np.all((D@C.T)%3==0)
 assert np.all((D@Z)%3==0)
 rank_C=modrank([{int(j):int(v) for j,v in enumerate(r) if v} for r in C],3)
 rank_D=rank_mod(D,3)
 assert (rank_C,rank_D)==(81,79)
 joint=rank_mod(np.r_[D[:-1],Z.T],3)
 assert joint==160
 # X vertex Gauss operators and Z 8-cycle Wilsons commute:
 # (X^a)(Z^b)=omega^(-a.b) Z^b X^a.
 # All X generators mutually commute; all Z generators mutually commute.
 # Neither flux nor Gauss constraints are logical operators when imposed as stabilizers.
 out=dict(status='PASS',n_physical_qutrit_edges=160,n_vertex_gauss_constraints=80,
  n_eightcycle_wilson_terms=1620,
  vertex_operator_weight=4,wilson_operator_weight=8,
  gauge_star_rank_over_F3=rank_D,independent_wilson_rank_over_F3=rank_C,
  full_stabilizer_rank=joint,
  gauge_only_code_parameters='[[160,81]]_3 before imposing flatness (no code distance claimed)',
  flatness_plus_gauss_code_parameters='[[160,0]]_3',
  unique_ground_state_dimension=1,
  Hamiltonian='H=-g sum_v (G_v+G_v†) -k sum_(1620 8cycles) (W_c+W_c†), g,k>0; choose G_v=X^(D_v), W_c=Z^(C_c), omega=e^(2pi i/3)',
  exact_all_commutators_zero=True,
  exact_logical_count_explanation='Gauss X checks rank79, leaving 160-79=81 encoded qutrits. The entire 8-cycle Z flatness stabilizer family has rank81 and is linearly independent of Gauss X in the symplectic Pauli check matrix; adding it uses all remaining stabilizer degrees and leaves zero encoded qutrits. Because rank79+rank81=160, the common +1 eigenspace has dimension 3^(160-160)=1. Flatness is a CHOICE of Hamiltonian, not automatically a required gauge condition.',
  gap_bound='Any violation of a stabilizer with nontrivial cube-root eigenvalue raises its -g(X+X†) energy by 3g or its -k(Z+Z†) energy by 3k. Because all 1620 and 80 terms commute, the spectral gap is at least 3*min(g,k), but potentially larger from syndrome redundancies.',
  boundary='An explicit local commuting 80+1620 term model and exact ground degeneracy count, not a derived fundamental interaction. Eight-cycle fluxes are all geometrically local on the Levi graph, but the model has no 4D continuum, Lorentzian propagation, matter or couplings.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('GAUGE 160',rank_D,rank_C,joint,'unique state',flush=True)
 return out
if __name__=='__main__':run()
