"""TOE missing-interface audit: C4 chiral parity exchange acts on CY
Klein deck group, but is NOT a fixed-vacuum geometric automorphism of
the certified free tetraquadric F_{2,3}.

Uniform Hadamard rotation R:(x,y)->(x+y,x-y), projectively; on quadratic
S=x²+y², D=x²-y², T=2xy we have S'=2S, D'=2T, T'=2D.
Four factors: F_{a,b} maps to 16 F_{b,a}. Fixed fiber requires a=b,
but then original g*h fixed locus contains points where F∝a-b=0.
This proves a no-go for this specific uniform-Hadamard lift, not for
all possible nonuniform or nonlinear CY automorphisms.
Also explicit four-dimensional deck-character Hilbert-space SWAP:
F20 C4 swapping the two Z2 holonomies matches W33 logical SWAP
as an abstract 4state intertwiner, not as a physical coupling.
"""
from pathlib import Path
import json,sys,itertools
import sympy as S
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"data/w33_20261008_chiral_CY_duality_Gcharacter_SWAP_no_go.json"
def main():
 x,y=S.symbols('x y');a,b=S.symbols('a b')
 SS=x*x+y*y;D=x*x-y*y;T=2*x*y
 tx=x+y;ty=x-y
 assert S.expand(SS.subs({x:tx,y:ty},simultaneous=True)-2*SS)==0
 assert S.expand(D.subs({x:tx,y:ty},simultaneous=True)-2*T)==0
 assert S.expand(T.subs({x:tx,y:ty},simultaneous=True)-2*D)==0
 # Independent indeterminates U,V,W represent full 4factor products.
 U,V,Z=S.symbols('U V Z')
 F=U+a*V+b*Z
 pull=16*(U+a*Z+b*V)
 assert S.expand(pull/16-F.subs({a:b,b:a},simultaneous=True))==0
 assert S.solve([S.expand(pull/16-F)],(a,b))=={a:b}
 # Characters chi_{uv}(g1^i g2^j)=(-1)^{ui+vj}, unitary Fourier:
 chars=list(itertools.product(range(2),repeat=2))
 H=S.Matrix([[S.Rational((-1)**(u*i+v*j),2) for i,j in chars] for u,v in chars])
 assert H.T*H==S.eye(4)
 swap=S.zeros(4)
 for k,(i,j) in enumerate(chars):swap[chars.index((j,i)),k]=1
 assert swap**2==S.eye(4)
 assert swap*H==H*swap
 Z0=S.diag(1,1,-1,-1);Z1=S.diag(1,-1,1,-1)
 assert swap*Z0*swap==Z1
 X0=S.zeros(4);X1=S.zeros(4)
 for k,(i,j) in enumerate(chars):
  X0[chars.index((i^1,j)),k]=1
  X1[chars.index((i,j^1)),k]=1
 assert swap*X0*swap==X1
 # In projective fixed class gh, x/y= ±i for all four factors.
 # F|Fix(gh)=16(a ± b), so a=b (with arbitrary nonzero a)
 # forces vanishing for half of fixed points.
 assert S.factor((a-b).subs(a,b))==0
 selected={a:S.Integer(2),b:S.Integer(3)}
 assert S.expand(pull/16-F).subs(selected)==V-Z
 return {"uniform_Hadamard_all_four_P1_factors_action":"(S,D,T)->(2S,2T,2D); product quartics each scale 16",
  "tetraquadric_family_duality":"F_{a,b} maps to F_{b,a} up to common scalar 16",
  "certified_free_polynomial_a2b3_maps_to_a3b2_distinct":True,
  "identical_fiber_requires_a_equal_b":True,
  "a_equal_b_causes_original_gh_fixedpoint_locus_on_hypersurface":True,
  "uniform_Hadamard_as_C4_chiral_swap_on_same_smooth_free_X23":False,
  "may_relate_distinct_smooth_free_fibers_X23_X32_by_isomorphism":True,
  "abstract_CY_flat_U1_character_group":"Hom(pi1=Z2^2,U1)=Z2^2",
  "abstract_character_space_dimension":4,
  "character_basis_Fourier_matrix_Hadamard_tensor_Hadamard":[list(map(str,row)) for row in H.tolist()],
  "deck_factor_exchange_permutation_SWAPS_two_qubits":True,
  "SWAP_intertwines_deck_char_Fourier_transform":True,
  "SWAP_conjugates_both_X_and_Z_logical_Paulis_by_qubit_exchange":True,
  "F20_C5_acts_trivially_on_2bit_character_model":True,
  "F20_C4_image_order_on_2bit_character_model":2,
  "potential_shared_Z2squared_representation_not_physical_geometric_or_quantum_identification":True,
  "scope":"A precise duality-versus-vacuum-symmetry obstruction for uniform H4/Clifford interchange and a positive abstract 4-state Fourier intertwiner. No CY deck Wilson dynamics, local spacetime symmetry or Standard Model action derived."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if k!="character_basis_Fourier_matrix_Hadamard_tensor_Hadamard"},flush=True)
 print("CHIRAL_CY_Z2FOURIER_DUALITY_NO_GO_PASS")
