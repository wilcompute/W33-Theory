#!/usr/bin/env python3
"""Group-order obstruction to a fully W33-equivariant Conwell 8-label map.

Established group inputs: PSp(4,3) is nonabelian simple of order25920;
PGSp(4,3) is its index2 automorphism extension of order51840;
Conwell heptads carry natural A8 on eight labels.

This does not preclude restriction to a common subgroup or a linear,
non-permutation action on the eight-dimensional logical vector space.
"""
from math import factorial,gcd
import json

def certificate():
    H=25920;G=51840;A8=factorial(8)//2;S8=factorial(8)
    assert G==2*H and G%H==0
    assert S8==40320 and A8==20160
    assert S8%H!=0 and G%A8!=0
    assert gcd(H,S8)<H
    # Any homomorphism H -> S8 has kernel normal in simple H;
    # injectivity impossible by Lagrange, hence its image is trivial.
    # Thus any homomorphism G -> S8 factors through G/H = C2.
    return {
      "schema":"w33.conwell.eight_label.full_symmetry_nogo.v1",
      "PGSp4_3_order":G,"PSp4_3_order":H,
      "PSp4_3_is_simple":True,
      "S8_order":S8,"A8_order":A8,
      "PSp4_3_cannot_embed_S8":True,
      "A8_cannot_embed_PGSp4_3":True,
      "any_W33_full_group_8_label_permutation_image_order_at_most":2,
      "surjective_full_W33_equivariant_map_40_points_to_28_pairs_with_natural_A8_action":False,
      "reason":"Nonabelian simple normal subgroup PSp4(3) acts trivially on any eight labels; quotient of order two cannot act transitively on all 28 pairs.",
      "does_not_rule_out":"A specified common proper subgroup, independent encodings, non-permutation eight-dimensional GF2 representations, or nonfaithful geometry functors."
    }

if __name__=="__main__":print(json.dumps(certificate(),indent=2))
