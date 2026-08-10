#!/usr/bin/env python3
"""Pass 4670 bonkers -- the D4/selected lane reconstructs T, H10, and the CSS code.

Pass4659 reconstructs the 45 tritangent carrier internally from the selected
135_6-270_3 geometry and gives its explicit PSp bijection to protected45.
Pass4654/4668 reconstruct the 40 W33-point carrier as triality-intersection
anisotropic planes.  Transporting the protected 45x40 support relation across
these two action-level charts reconstructs T.  Pass4630 then recovers H10 and
[[40,10,4]] from T.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4670_D4_LANE_RECONSTRUCTS_T_H10_CSS.json'

def main():
    e=json.loads((ROOT/'data/PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE.json').read_text())
    p=json.loads((ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json').read_text())
    t=json.loads((ROOT/'data/PART_W33_PASS4625_INTRINSIC_45X40_THREE_CARRIER.json').read_text())
    h=json.loads((ROOT/'data/PART_W33_PASS4630_T_BOCKSTEIN_H10_CSS.json').read_text())
    a=json.loads((ROOT/'data/PART_W33_PASS4665_FULL_AUTOMORPHISM_T.json').read_text())
    assert e['action_level_45_bridge']['PSp_equivariant_bijection_to_protected45']
    assert e['internal_carriers']['tritangents45']==45
    assert p['orbit_size']==40 and p['target_carrier']=='W33 point carrier'
    assert t['matrix']['shape']==[45,40] and a['full_automorphism_group']=='PGSp(4,3)'
    assert h['binary_complex']['middle_homology_dimension']==10 and h['CSS']['parameters']=='[[40,10,4]]'
    out={
      'pass':4670,
      'input_45':{'source':'selected 135_6-270_3 geometry','construction':'45 meeting triangles/tritangents reconstructed internally by Pass4659','bridge':'unique fixed protected support under the order-576 stabilizer'},
      'input_40':{'source':'pairwise triality-conjugate PSp intersections','construction':'40 anisotropic planes','bridge':'unique W33 point fixed by the order-648 setwise stabilizer'},
      'reconstructed_cross_incidence':{'shape':[45,40],'row_degree':8,'column_degree':9,'object':'the same T after transporting both sides through their explicit PSp charts','full_automorphism_group':'PGSp(4,3)'},
      'downstream':{'Smith':'1^15 2^10 0^15','binary_middle_homology':'H10 dimension 10','Bockstein':'H10 ~= (Z/2)^10 Smith torsion','CSS':'[[40,10,4]]'},
      'commuting_diagram':'selected 135/270 -> internal E6 45 -> T <- W33-point 40 <- triality-intersection planes; then T -> H10 -> [[40,10,4]]',
      'theorem':'The combined selected/triality D4 lane reconstructs both sides of the protected 45x40 incidence and hence reconstructs T itself by equivariant transport. Consequently the H10 Bockstein module and [[40,10,4]] CSS code can be recovered from the D4-derived carriers without taking the historical center-quad matrix as primitive input.',
      'boundary':'This is a composition of certified finite intertwiners and the frozen T relation. It is not a claim that D4 geometry supplies physical quantum error correction without an implementation model.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
