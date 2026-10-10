"""Round28 mathematically exact factor-screen for genuine exceptional E8
subgroups F4xG2, E7xA1, Spin16. Branching from literature.
No embedded PSp4(3) matrices were constructed. Reports necessary
locations for St81, rejects factor-only branches by block dimension.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe28_exceptional_e8_branch_screen.json'
def run():
 f4g2={'adjF4':52,'adjG2':14,'tensor26x7':26*7}
 e7a1={'adjE7':133,'adjA1':3,'tensor56x2':56*2}
 so16={'adjSO16':120,'halfspin':128}
 assert sum(f4g2.values())==sum(e7a1.values())==sum(so16.values())==248
 # For simple PSp4(3), any map to SL2(C) must be trivial:
 # finite simple subgroups PGL2(C) = A5, and |PSp|=25920.
 # Restriction via E7 factor leaves blocks 133, 56, 56, 1, 1, 1.
 e7blocks=[133,56,56,1,1,1]
 assert sum(e7blocks)==248
 # If G embedded wholly in F4 factor, G2 trivial, blocks
 # 52,14 trivial singlets, and seven invariant 26 modules.
 f4only=[52]+[1]*14+[26]*7
 g2only=[1]*52+[14]+[7]*26
 assert sum(f4only)==sum(g2only)==248
 assert max(f4only)<81 and max(g2only)<81
 # For both projections nontrivial, at most the (26,7)
 # factor has sufficient vector-space dimension to host St81.
 out=dict(status='PASS',G='PSp(4,3) order25920',
  branching={'F4xG2':f4g2,'E7xA1':e7a1,'Spin16':so16},
  no_go_F4_only=True,no_go_G2_only=True,
  F4_only_largest_G_invariant_block=52,
  G2_only_largest_G_invariant_block=14,
  E7_A1_trivial_A1_under_simple_G=True,
  E7_factor_only_invariant_block_dimensions=e7blocks,
  necessary_host_for_St81_in_E7xA1='E7 adjoint133 only; the 56x2 and A1 adjoint cannot contain 81 after SL2 projection is trivial.',
  necessary_host_for_St81_in_F4xG2='(26,7) 182D mixed tensor ONLY if PSp has nontrivial actions in both F4 and G2. Factor-only embeddings rigorously exclude St81.',
  necessary_host_for_St81_in_SO16='SO16 adjoint120 OR halfspin128; dimensional screening alone cannot decide either.',
  proof='For factor-only F4, the adjoint248 has invariant blocks 52, 14 scalar singlets, and seven copies of26, all strictly less than81; similarly for G2 alone, blocks14,52 scalar singlets,26 copies of7. For E7xA1, a nontrivial homomorphism of simple PSp4(3) to SL2(C) would be an injection up to finite center, impossible by the finite-subgroup classification of PGL2(C); hence A1 factor is trivial and two copies of 56 and three singlets exclude St81 except possibly in the adjoint133.',
  honest_boundary='These are exact conditional representation-theoretic screening statements, NOT actual exceptional-subgroup embeddings of PSp4(3), class fusions, Lie brackets, nor evidence an 81D constituent exists. Diagonal F4xG2, E7 adjoint133, SO16 120/128, and exceptional non-maximal embeddings remain open.',
  sources=['https://citeseerx.ist.psu.edu/document?doi=d31040221791fece0816c9adfa04522248c27456&repid=rep1&type=pdf','https://en.wikipedia.org/wiki/E8_(mathematics)'])
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('E8 screening: F4 alone & G2 alone impossible; E7 -> 133; F4xG2 -> mixed 182',flush=True)
 return out
if __name__=='__main__':run()
