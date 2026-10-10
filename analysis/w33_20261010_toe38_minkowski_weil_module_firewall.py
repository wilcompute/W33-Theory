"""TOE38: orthogonal-vs-symplectic four-dimensional module firewall.

The A6 finite Minkowski translations M=S/<ones> have no invariant
alternating form (Round37), whereas genus2 theta Heisenberg charges
E[3] have a nondegenerate symplectic Weil pairing (Pass11869).
Any equivariant linear isomorphism from M to a Weil module would
pull back its symplectic form to a nondegenerate A6-invariant
alternating form, impossible. A6 may act in other representations.
"""
import sys,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe37_finite_translation_form_obstruction import run as previous
from w33_20261010_toe37_finite_translation_form_obstruction import rank3
OUT=ROOT/'data/w33_20261010_toe38_minkowski_weil_module_firewall.json'
def run():
 base=previous(write=False)
 gens=[np.array(g,dtype=np.int64) for g in base['A6_generator_matrices_mod3']]
 J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],dtype=np.int64)%3
 assert rank3(J)==4
 witness=[int(np.count_nonzero((g.T@J@g-J)%3)) for g in gens]
 assert any(witness)
 forms=[]
 import itertools
 for a,b in itertools.combinations(range(4),2):
  K=np.zeros((4,4),dtype=np.int64);K[a,b]=1;K[b,a]=-1;forms.append(K)
 eqs=np.vstack([np.array([(g.T@K@g-K)%3 for K in forms]).reshape(6,16).T for g in gens])
 exactrank=rank3(eqs)
 assert exactrank==6
 out=dict(status='PASS',prime=3,translation_4d_module='A6 quotient M=S/<c> with invariant symmetric quadratic form I+J, prior Round37.',
  theta_4d_module='Level3 genus2 Pauli charge space A[3]=F3^4 with nondegenerate alternating Weil symplectic pairing, prior Pass11869.',
  standard_weil_J_mod3=J.tolist(),J_rank=rank3(J),
  broken_weil_pairing_constraint_nonzero_entries_by_generator=witness,
  invariant_alternating_linear_constraint_rank=exactrank,
  invariant_alternating_dimension=6-exactrank,
  theorem='No A6-equivariant invertible F3-linear identification of THIS orthogonal Minkowski 4D module with any 4D A6-module admitting a nondegenerate invariant alternating form. Otherwise pullback of symplectic Weil form would be a nonzero invariant alternating form on M; the computed invariant space is zero.',
  implications='W33 has at least TWO incompatible 4D roles: finite orthogonal momenta vs symplectic qutrit Pauli/Weil charges. They cannot be naively identified coordinate-for-coordinate equivariantly for the same A6 Lorentz action. An enlarged space, group extension, polarization choice or a non-equivariant map is additional structure.',
  boundary='Does not disprove existence of A6 subgroups inside Sp4(3) on other 4D modules, of complete E8 finite Poincare, or of genus2 modular physics. It is a module-specific precise no-go, not global spacetime or quantum mechanics obstruction.',
  source_priors=['analysis/w33_20261010_toe37_finite_translation_form_obstruction.py','analysis/w33_pass11869_11873_siegel_level3_two_qutrits.py'])
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('TOE38 Minkowski/Weil no-intertwiner rank',exactrank,'J defects',witness,flush=True)
 return out
if __name__=='__main__':run()
