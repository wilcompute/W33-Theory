"""Round30 full F4 x G2 exclusion for W33 simple PSp4(3).

External exact inputs: ATLAS U4(2) complex low-degree irreps 5a,5b
non-real conjugate and unique real orthogonal 6; no 2,3,4,7.
G2(C) fundamental 7 is orthogonal, and stabilizer of a
non-isotropic nonzero vector is SL3(C) with 7=1+3+3*.

Proof: Any faithful action G->G2(C) would give selfdual 7, hence
1+6 (since 5 is non-real); its fixed line is non-isotropic.
Stabilizer SL3 would split the 6 as 3+3*, contradict irred6.
"""
import json,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe30_G2_full_subgroup_nogo.json'
def decompositions(total,parts=(1,5,6)):
 def rec(left,lower):
  if left==0:yield lower;return
  for v in parts:
   if v>= (lower[-1] if lower else 0) and v<=left:
    yield from rec(left-v,lower+(v,))
 return list(rec(total,()))
def run():
 parts=decompositions(7)
 assert parts==[(1,1,1,1,1,1,1),(1,1,5),(1,6)]
 # 5a and 5b are distinct complex-conjugate nonselfdual irreps. No
 # 7 self-dual if 5 with two one-dimensional constituents.
 # A trivial 1^7 cannot be faithful for simple nonabelian G.
 admissible=[(1,6)]
 assert len(admissible)==1
 f4g2_blocks={'adjoint_F4':52,'adjoint_G2':14,'mixed_F4_26_times_G2_7':26*7}
 assert sum(f4g2_blocks.values())==248
 # With G2 projection trivial, mixed block consists of seven
 # independent copies of the F4 26D module, and G2 adjoint 14
 # copies of the trivial group rep.
 invariant_blocks=[52]+[1]*14+[26]*7
 assert sum(invariant_blocks)==248 and max(invariant_blocks)==52
 rec=dict(status='PASS',group='PSp(4,3) ≅ PSU4(2), simple order25920',
  ATLAS_complex_irreducible_degrees_at_most_seven={'trivial':1,'5a':5,'5b':5,'6':6},
  ATLAS_low_degree_reality={'5a':'complex, 5b conjugate','5b':'complex, 5a conjugate','6':'real orthogonal and irreducible'},
  all_seven_dimension_sum_candidates=[list(p) for p in parts],
  selfdual_nontrivial_seven_dimension_candidate=[1,6],
  G2_seven_dimensional_fundamental='faithful, orthogonal, invariant nonsingular 3-form; nonisotropic fixed-vector stabilizer SL3(C) and restriction 7=1⊕3⊕3*',
  no_nontrivial_G_homomorphism_to_G2C=True,
  F4xG2_branching=f4g2_blocks,
  full_E8_G_invariant_max_block_via_F4xG2=52,
  Steinberg81_multiplicity_through_any_F4xG2_embedding=0,
  theorem='Any PSp4(3)->G2(C) homomorphism is trivial. By simplicity a nontrivial homomorphism would be injective. Restrict the orthogonal faithful 7D G2 module to G: from the ATLAS irreducible degrees and Schur/self-duality only 1+6 is possible, since 5a and 5b are nonselfdual and cannot pair within dimension7. The G-fixed line is nonisotropic because 1 and irreducible6 are orthogonal and the whole form is nondegenerate. Thus G lies in its SL3(C) stabilizer, where 7=1+3+3*. This forces irreducible6 to decompose, contradiction. Therefore the G2 projection of any G->F4(C)xG2(C) is trivial. E8 adjoint 248=(52,1)+(1,14)+(26,7) restricts to G invariant blocks 52, 14 trivial lines, seven 26D modules. Hence irreducible Steinberg81 multiplicity0.',
  proof_scope='Uses external authoritative ATLAS ordinary character-table low degree and standard complex G2 stabilizer theorem as INPUTS; the Python checks only enumerated seven-dimensional partitions and E8 branching arithmetic. This is NOT an independently computed full PSp4(3) character table, an exhaustive enumeration of G2 group elements, or a physical E8 matter theorem. Does not cover E7xA1 or Spin16 embeddings or other E8 subgroups.',
  external_sources=[
   'https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U42/',
   'https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Ar5aB0',
   'https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Ar5bB0',
   'https://brauer.maths.qmul.ac.uk/Atlas/v3/matrep/U42G1-Zr6B0',
   'https://math.univ-cotedazur.fr/~pauly/G2Theta.pdf'
  ],prior='Round28 excluded factor-only F4/G2; Round29 excluded three E7 maximal-rank routes. This calculation closes ALL embeddings into F4xG2, including formerly open mixed actions.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('G2 FULL NO-GO: low-degree 7D candidates',parts,'only orthogonal nontrivial',admissible,flush=True)
 return rec
if __name__=='__main__':run()
