"""Round31 general Spin16 even-even orthogonal splitting obstruction.

For E8 D8 embedding e8 = so16(120) + halfspin16(128).
If G preserves a NONDEGENERATE orthogonal even-even split
V16=V_a+V_b (a,b even >=4), each invariant factor is <=66 for
so16 and each halfspin block has dim64. Thus no irreducible St81.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe31_E8_spin16_even_split_obstruction.json'
def run():
 cases=[]
 for a in (4,6,8,10,12):
  b=16-a
  adj=[a*(a-1)//2,b*(b-1)//2,a*b]
  half=[2**(a//2-1)*2**(b//2-1)]*2
  assert sum(adj)==120 and sum(half)==128
  assert max(adj+half)<81
  cases.append(dict(even_orthogonal_submodule_dimensions=[a,b],
     so16_G_invariant_blocks=adj,halfspin_G_invariant_blocks=half,
     largest_invariant_block=max(adj+half),
     St81_multiplicity=0))
 # ATLAS low-degree modules 5a, 5b dual + real6:
 # V16=(5a+5b)+6, nondegenerate orthogonal 10+6.
 candidate=next(x for x in cases if x['even_orthogonal_submodule_dimensions']==[6,10])
 assert candidate['so16_G_invariant_blocks']==[15,45,60]
 assert candidate['halfspin_G_invariant_blocks']==[64,64]
 rec=dict(status='PASS',source='Standard E8 maximal D8 branching 248=120_so16+128_halfspin, and standard complex halfspin factor branching.',
 theorem='Let G be a finite PERFECT group acting inside Spin16 (or its E8 HSpin16 image), whose 16D complex orthogonal vector representation decomposes as a direct sum of two nondegenerate G-invariant orthogonal even-dimensional subspaces of dimensions a and b=16-a, with 4<=a<=12. Then the restricted E8 adjoint is a direct sum of G-invariant modules of dimension at most66 from so16 and two 64D halfspin pieces. It contains NO irreducible 81-dimensional constituent, including the W33 Steinberg81.',
 proof='As G is perfect, its determinant characters on each invariant Va and Vb must be trivial, so its image preserves the oriented SO(a)×SO(b) factors and cannot exchange halfspin summands. Under Spin(a)×Spin(b), so16=Λ²Va⊕Λ²Vb⊕(Va⊗Vb), dimensions binom(a,2),binom(b,2),ab. The selected halfspin128 decomposes (S_a^+⊗S_b^+)⊕(S_a^-⊗S_b^-), each of dimension 2^(a/2-1+b/2-1)=64. Enumerate a=4,6,8,10,12: all adj pieces<=66 and spin pieces64. Over C finite-group representations are semisimple; an irrep of dimension81 cannot occur within any invariant summand <81.',
 cases=cases,
 concrete_PSp4_3_SO16_candidate='The ATLAS G=PSp4(3) complex 5a,5b=5a*,6_real gives a faithful real/orthogonal 16D representation 5a⊕5b⊕6, splitting into nondegenerate orthogonal 10D and 6D submodules. Every LIFT of this orthogonal action to E8 HSpin16 (if any exists) has St81 multiplicity0 by the dimension theorem.',
 candidate_SO16_blocks={'adjoint':[45,15,60],'halfspin':[64,64]},
 candidate_spin_lift_warning='An orthogonal G->SO16 homomorphism need not lift to the Spin16 central extension and need not define the relevant HSpin16 subgroup of E8. The theorem is conditional on such an E8 embedding existing; it nevertheless excludes Steinberg81 in any such lifted candidate.',
 surviving_spin16_cases='An irreducible 16D orthogonal PSp module, odd+odd decompositions and 2+14 splits are NOT excluded by this argument. Neither existence nor irreducible Steinberg81 character restriction in those cases was computed.',
 interpretation='A stronger subgroup-generic E8 no-go than the Round30 F4xG2 closure for this broad, explicitly stated class of reducible D8 embeddings. Does not prove an overall E8 embedding no-go or physical matter.',
 sources=['https://arxiv.org/abs/math/0607640','https://brauer.maths.qmul.ac.uk/Atlas/v3/clas/U42/'])
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('E8 SPIN16 EVEN SPLITS',[(r['even_orthogonal_submodule_dimensions'],r['largest_invariant_block']) for r in cases],flush=True)
 return rec
if __name__=='__main__':run()
