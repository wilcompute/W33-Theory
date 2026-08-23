#!/usr/bin/env python3
"""Pass9733-9740: full ordered transverse-glue stabilizer inside U(6,3).

Pass9465 proved only signed-coordinate monomial rigidity.  Here the ambient
unitary group itself is used.  For the glue-derived package (K,R,B=KR^T),
C_G and C_E=R C_G are transverse K-Lagrangians and B-orthogonal nondegenerate
minus-type six-spaces.  Restriction to C_G identifies the ordered-pair
stabilizer in C_Sp(K)(R) with O^-(6,3).
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9733_9740_FULL_GLUE_PAIR_UNITARY_STABILIZER.json'

def o_minus_6(q=3):return 2*q**6*(q**3+1)*(q**2-1)*(q**4-1)
def u6(q=3):
 o=q**15
 for i in range(1,7):o*=q**i-(-1)**i
 return o

def main():
 prev=json.loads((ROOT/'data/PART_W33_PASS9465_9472_F9_UNITARY_CENTRALIZER_RIGIDITY.json').read_text())
 pol=json.loads((ROOT/'data/PART_W33_PASS9505_9512_DOUBLE_MINUS_ORTHOGONAL_POLARIZATION.json').read_text())
 assert prev['status']=='PASS' and pol['status']=='PASS'
 U=u6();Om=o_minus_6();assert U==182699779456696320 and Om==26127360
 proj=Om//2;idx=U//Om;unordered=Om*2
 assert proj==13063680 and idx==6992661312 and unordered==52254720
 out={'schema':'w33.pass9733_9740.full_glue_pair_unitary_stabilizer.v1','status':'PASS','passes':'9733-9740',
 'ambient':{'group':'U(6,3)=C_Sp(12,3)(R)','order':U},
 'ordered_pair_stabilizer':{'group':'O^-(6,3)','order':Om,'projective_order':proj,'index_in_U':idx},
 'unordered_pair_stabilizer':{'description':'<O^-(6,3),R>; R swaps C_G,C_E and R^2=-I lies in the ordered stabilizer','order':unordered,'quotient_over_ordered':'C2'},
 'proof':'If u commutes with R and preserves C_G, it automatically preserves C_E=R C_G. Because B=K R^T, preserving K and commuting with R is equivalent to preserving B; restriction therefore lands in O(B|C_G)=O^-(6,3). Conversely every A in O^-(B|C_G) extends uniquely by u(Rg)=R A g. The extension preserves B, commutes with R, hence preserves K, giving an isomorphism of the ordered-pair stabilizer with O^-(6,3).',
 'correction_to_previous_scope':{'signed_coordinate_common_stabilizer_order':2,'full_unitary_ordered_pair_stabilizer_order':Om,'projective_signed_coordinate_order':1,'projective_full_order':proj,'interpretation':'The Pass9465 projective rigidity was coordinate-monomial rigidity only, exactly as scoped. It is not absolute rigidity inside U(6,3).'},
 'theorem':'The complete stabilizer of the ordered transverse Niemeier glue pair inside the F9 unitary centralizer is O^-(6,3), order 26,127,360 (projective order 13,063,680). Allowing the two glues to swap doubles it to 52,254,720. Thus the concrete pair is highly rigid in the signed-coordinate group but carries a large intrinsic orthogonal symmetry in the full unitary geometry.',
 'boundary':'Uses the standard finite classical-group stabilizer equivalence plus the exact Pass9465/9505 form package. It does not assert that every element of this abstract unitary stabilizer lifts to an integral Niemeier lattice automorphism.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','ordered':Om,'projective':proj,'unordered':unordered}));return 0
if __name__=='__main__':raise SystemExit(main())
