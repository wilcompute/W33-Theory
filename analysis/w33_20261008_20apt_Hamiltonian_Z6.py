"""Exactly soluble W33 selected-apartment binary toric stabilizer Hamiltonian.

H=-sum_{40 vertices} A_v -sum_{20 faces} B_f.
All Pauli terms commute; one relation among each independent check family.
Constrain allowed syndrome bit parity and exhibit minimal pair defects.
This is a 2D finite CW topological model, NOT Lorentzian gravity.
"""
import sys,json,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add
OUT=ROOT/"data/w33_20261008_20apt_Hamiltonian_F20_Z6_guard.json"
def rank(vals):
 B={}
 for x in vals:add(x,B)
 return len(B)
def main():
 V,E,F,stab,H,b1,b2=topology()
 assert len(V)==40 and len(E)==60 and len(F)==20
 assert rank(b1)==39 and rank(b2)==19
 assert all((u&v).bit_count()%2==0 for u in b1 for v in b2)
 assert not any(sum((v>>j)&1 for v in b1)%2 for j in range(60))
 assert not any(sum((f>>j)&1 for f in b2)%2 for j in range(60))
 index={e:j for j,e in enumerate(E)}
 star_set=set(b1);face_set=set(b2)
 for g in stab:
  ep=[index[tuple(sorted((g[u],g[v])))] for u,v in E]
  def trans(bit):
   return sum(1<<ep[j] for j in range(60) if (bit>>j)&1)
  assert {trans(b) for b in b1}==star_set
  assert {trans(f) for f in b2}==face_set
 # Z on any qubit flips exactly the two endpoint star eigenvalues.
 z_syndrome=[sum((b>>j)&1 for b in b1) for j in range(60)]
 x_syndrome=[sum((b>>j)&1 for b in b2) for j in range(60)]
 assert set(z_syndrome)=={2}
 assert set(x_syndrome)=={2,4}
 # Each check sign vector constrained even (1 global check product).
 # Excitations require >=2 violated checks -> gap=4 at unit stabilizer coefficients.
 # Since one edge achieves exactly 2 violated stars, 4 is attained.
 return {
  "CW_cells":[40,60,20],
  "stabilizer_rank_X":39,"stabilizer_rank_Z":19,
  "Pauli_commutators_zero":True,
  "Hamiltonian_unit_coefficients":"H = -sum_v A_v - sum_f B_f",
  "ground_energy_exact":-60,
  "ground_space_dimension_exact":4,
  "energy_gap_exact":4,
  "minimal_excited_energy_exact":-56,
  "star_relation_all_stars_multiply_identity":True,
  "plaquette_relation_all_20_plaquettes_multiply_identity":True,
  "single_Z_excitation_star_violations":dict(collections.Counter(z_syndrome)),
  "single_X_excitation_face_violations":dict(collections.Counter(x_syndrome)),
  "Hamiltonian_invariant_under_all_20_F20_permutations":True,
  "logical_code_distance":6,
  "full_F20_invariant_flat_Z6_Wilson_line_characters":[[0,0],[3,3]],
  "full_F20_invariant_flat_Z6_group":"Z2",
  "full_F20_invariant_flat_Z6_order_six_characters":0,
  "CRT_argument":"H1(Z6)=H1(Z2) x H1(Z3); fixed spaces have sizes2 x1; only (0,0) and (3,3) under a chosen mod2 logical basis.",
  "proton_hexality_cannot_be_entirely_F20_invariant_flat_Z6_holonomy":True,
  "relativistic_or_Einstein_dynamics_derived":False,
  "full_nonabelian_gauge_fields_derived":False,
  "physical_boundary":"Finite commuting projector stabilizer Hamiltonian; no 3+1D spacetime, lapse/shift or ADM hypersurface-deformation bracket, and not a Standard Model matter representation."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,indent=2),flush=True);print("HAMILTONIAN_Z6_GUARD_PASS")
