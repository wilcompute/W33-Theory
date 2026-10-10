"""Round26: rigorous E8 SU(9)-embedded non-E6-factor route test.
Existing PSp4(3) Schlaefli 27 permutation module contains a 6D irrep.
Embed that six-dimensional representation plus three trivial lines into SL9.
The E8 sl9+Lambda3(9)+Lambda3(9)* realization admits a blockwise
decomposition with no 81-dimensional Steinberg irreducible constituent.
"""
from pathlib import Path
from collections import Counter
import itertools,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe26_e8_su9_embedding_obstruction.json'
def run():
 from importlib import import_module
 s=import_module('w33_pass7017_7024_schlafli_w33_equivariant_no_go')
 assert s.srg_spectrum(27,16,10,8)[1:] == [(4,6),(-2,20)]
 # V9=V6 + 1 + 1 +1, G acts nontrivially only on V6.
 # Wedge^3 decomposed by #basis from V6.
 wedge={r:0 for r in range(4)}
 for a in itertools.combinations(range(9),3):
  wedge[sum(i<6 for i in a)]+=1
 assert wedge=={0:1,1:18,2:45,3:20}
 # Invariant blocks refined using 3 trivial singlets:
 wedge_fine={
  'Lambda3(V6)':20,
  'three_Lambda2(V6)':3*15,
  'three_V6':3*6,
  'singlet':1}
 # sl9 = (End V6) + six V6 + (End 1^3) minus scalar
 adjoint_sl9={'End_V6':36,'six_copies_V6':6*6,'gl3_trivial_minus_one':8}
 assert sum(adjoint_sl9.values())==80
 # G-invariant direct summands of dimension <=36, hence no 81D
 # irreducible St81 can occur in either 80 or 84 gradings.
 block_dims=[36]+[6]*6+[1]*8+[20]+[15]*3+[6]*3+[1]
 assert sum(block_dims)==164 # sl9 (80) + Lambda3 (84)
 assert max(block_dims)==36
 E8_blocks=block_dims+[20]+[15]*3+[6]*3+[1]
 assert sum(E8_blocks)==248
 assert max(E8_blocks)==36
 # Native irreducible 81 must either lie inside an invariant block or
 # in a sum of constituents; direct sum over C is semisimple.
 rec=dict(status='PASS',
  subgroup='PSp(4,3), order 25920',
  candidate_SU9_representation='9=6_schlafli + 1 +1 +1, existing W33 27-permutation Schlaefli 6D eigenspace',
  origin='Pass7017-7024 proves 27 Schlaefli permutation decomposition 1+6+20; Pass11681 implements E8 sl9 + Lambda3(9) + dual.',
  E8_su9_grading=[80,84,84],
  wedge3_grade_by_six_basis={str(k):v for k,v in wedge.items()},
  wedge3_invariant_block_dimensions=[20,15,15,15,6,6,6,1],
  sl9_invariant_block_dimensions=[36,6,6,6,6,6,6,1,1,1,1,1,1,1,1],
  full_E8_invariant_block_max_dimension=max(E8_blocks),
  predicted_Steinberg81_multiplicity=0,
  proof='The fixed splitting 9=V6 + C^3 triv induces a PSp-invariant direct sum of sl9 into End(V6) (36), six copies V6 (6 each), eight singlets; and Lambda3(9) into Lambda3 V6(20), three copies Lambda2 V6(15 each), three copies V6(6 each), and one singlet, plus the complex dual. Each invariant summand has dimension at most36. By Maschke semisimplicity, the irreducible Steinberg81 cannot occur in any summand and hence has multiplicity ZERO in the 248-dimensional restricted E8 adjoint. The construction really embeds G in SL9 (simple G implies detV6 is a trivial 1D character).',
  boundary='Concrete SU9 non-E6-factor-preserving embedding using the SIX-dimensional Schlaefli G-module only. Does not exclude another embedding of PSp4(3) into E8, nor does it construct an E8 matter intertwiner. Statement remains conditional on prior Schlaefli 6D irreducible being complex over the chosen field.',
  next_diagnostic='Search SL9 embeddings from OTHER <=9-dimensional nontrivial G modules and search exceptional E8 embeddings not factoring through the SU9 maximal-rank subgroup.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('E8 SU9 obstruction',rec['predicted_Steinberg81_multiplicity'],'max block',max(E8_blocks),flush=True)
 return rec
if __name__=='__main__':run()
