#!/usr/bin/env python3
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# one left-handed Weyl16: (multiplicity, Y)
states=[(6,F(1,6)),(2,F(-1,2)),(3,F(-2,3)),(3,F(1,3)),(1,F(1)),(1,F(0))]
trY2=sum(m*y*y for m,y in states)
# Dynkin indices: Q has two color fundamentals; uc,dc one each.
T3=F(2)
# Q gives 3 weak doublets and L one: four fundamentals.
T2=F(2)
assert trY2==F(10,3)
ratio=trY2/T2
assert ratio==F(5,3)
# normalized U1 generator sqrt(3/5)Y has the same index 2.
sin2=F(3,8)
out={
 'status':'PASS_CANONICAL_SPIN10_HYPERCHARGE_NORMALIZATION',
 'Tr_Y2_on_Weyl16':str(trY2),
 'SU3_Dynkin_index':str(T3),
 'SU2L_Dynkin_index':str(T2),
 'TrY2_over_T2':str(ratio),
 'GUT_normalized_generator':'Y1=sqrt(3/5) Y',
 'coupling_relation':'g1=sqrt(5/3) gY; at Spin(10) unification gY^2=(3/5)gU^2',
 'tree_level_unification_sin2thetaW':str(sin2),
 'boundary':'3/8 is the unification-scale normalization prediction. Running and thresholds are required before comparison with low-energy data.'
}
(ROOT/'data/PART_W33_PASS11596_SPIN10_COUPLING_NORMALIZATION.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print(json.dumps(out,indent=2))
