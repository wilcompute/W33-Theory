#!/usr/bin/env python3
"""Pass10797-10804: test the tempting 32 Hall-Janko C13 cycles against the order-2 defect.

The 416-point G2(4)/J2 action is free for C13 because 13 does not divide |J2|,
so it has exactly 32 C13-orbits.  Wilson's C13:6 lies inside the L2(13)
maximal subgroup.  ATLAS class fusion for that subgroup places the complement
powers in classes 2B,3B,6B.

For the 416 coset action, fixed-point counts follow exactly from centralizer
ratios because the corresponding J2 classes fuse to the same G2(4) classes:
  2B: |C_G(2B)|/|C_J2(2B)| = 3840/240 = 16,
  3B: 180/36 = 5,
  6B: 12/12 = 1.
Every element in a C13-coset of one complement power is conjugate inside the
Frobenius/dihedral normalizer, so these are also fixed counts on the 32 C13
orbit labels for n^3,n^2,n.

If the C6 permutation on 32 labels has a_d cycles of length d|6, the fixed
counts force
  a1=1, a2=2, a3=5, a6=2.
Hence the full 13:6 quotient has 10 states.  Under the involution n^3 the
32-label permutation module has invariant dimension 16+8=24, not 32, so it
cannot supply the Pass10789 order-2 defect.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10797_10804_HJ32_NORMALIZER_QUOTIENT.json'

def main():
    G2=251_596_800;J2=604_800
    assert G2//J2==416 and J2%13!=0
    cG={'2B':3840,'3B':180,'6B':12}
    cJ={'2B':240,'3B':36,'6B':12}
    fixed={k:cG[k]//cJ[k] for k in cG}
    assert fixed=={'2B':16,'3B':5,'6B':1}
    c13_cycles=416//13;assert c13_cycles==32

    # n order6; n^2 order3; n^3 order2.
    f1=fixed['6B'];f2=fixed['3B'];f3=fixed['2B']
    a1=f1
    a2=(f2-a1)//2
    a3=(f3-a1)//3
    a6=(32-a1-2*a2-3*a3)//6
    assert (a1,a2,a3,a6)==(1,2,5,2)
    assert a1+2*a2+3*a3+6*a6==32
    quotient_states=a1+a2+a3+a6;assert quotient_states==10

    # Involution action on 32 labels: 16 fixed labels + 8 transposed pairs.
    k_invariants=16+(32-16)//2;assert k_invariants==24
    order2_defect=32
    assert k_invariants!=order2_defect

    out={
      'schema':'w33.pass10797_10804.hj32_normalizer_quotient.v1','status':'PASS','passes':'10797-10804',
      'carrier':{'G_set':'G2(4)/J2','size':416,'C13_free':True,'C13_cycles':32},
      'class_fusion_input':{
        'normalizer_location':'C13:6 < L2(13) < G2(4)',
        'complement_classes':{'n^3':'2B','n^2':'3B','n':'6B'},
        'G2_centralizers':cG,'J2_centralizers':cJ,
        'source':'ATLAS G2(4) and J2 class tables; L2(13) maximal-subgroup fusion N(2B,3B,6B,7A,13AB)'},
      'fixed_points_on_416':fixed,
      'C6_on_32_C13_cycles':{
        'Fix_n':f1,'Fix_n2':f2,'Fix_n3':f3,
        'cycle_counts':{'1':a1,'2':a2,'3':a3,'6':a6},
        'orbit_count':quotient_states,
        'quotient_states':10},
      'order2_defect_test':{
        '32_label_module_k_invariant_dimension':k_invariants,
        'Pass10789_required_defect':order2_defect,
        'repairs_defect':False,
        'reason':'the involution fixes 16 labels and swaps the other 16 in eight pairs, so the permutation-module fixed dimension is only 24'},
      'new_selector_target':{'state_count':10,'arithmetic_coincidence':'10 = Phi_4(3) = 3^2+1','claim':'count recorded as a target only; no W33 Phi4 objectwise identification is made here'},
      'theorem':'The 32 Hall-Janko C13 cycles do not realize the characteristic-2 defect module. Their exact C6 normalizer action has cycle profile 1^1 2^2 3^5 6^2 and therefore a canonical ten-state 13:6 quotient. The involution-fixed dimension is 24, not the required 32. The surviving new object is the 10-state normalizer quotient.',
      'boundary':'Exact group-order/class-centralizer arithmetic conditional only on the standard ATLAS class fusion stated above. The 10=Phi4(3) comparison is not promoted beyond a selector target.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','C13_cycles':32,'C6_profile':{'1':1,'2':2,'3':5,'6':2},'quotient':10,'repairs_order2_defect':False}))
if __name__=='__main__':main()
