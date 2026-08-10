#!/usr/bin/env python3
"""Pass 4664 -- distinguish the packet S3 from the D4 sheet S3.

The two S3 actions both permute three objects, but their order-three directions
live in different ambient places.  The packet C3 is inside PSp(4,3), while the
D4 sheet C3 centralizes PSp in the type-preserving normalizer.  Hence they are
not the same ambient symmetry.  They commute and meet trivially, so together
with any outer reflection stabilizing a packet they generate (C3 x C3):C2.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4664_TWO_S3S_JOINT_STRUCTURE.json'

def main():
    p=json.loads((ROOT/'data/PART_W33_PASS4629_FULL_OUTER_PACKET_S3_FIBER.json').read_text())
    d=json.loads((ROOT/'data/PART_W33_PASS4649_FULL_TRIALITY_GROUP_INTERSECTIONS.json').read_text())
    assert p['PSp']['quotient']=='C3=A3' and p['PGSp']['quotient']=='S3'
    assert p['PSp']['kernel_H_order']==192 and p['PGSp']['support_stabilizer_order']==1152
    assert d['triality_closure']['PSp_order']==25920
    # Pass4641/4643 theorem: the type-preserving normalizer is (C3 x PSp):C2,
    # so the sheet-rotation C3 centralizes PSp and intersects it trivially.
    packet_C3_location='inside PSp support stabilizer'
    sheet_C3_location='centralizer C3 outside PSp in (C3 x PSp):C2'
    # Since the sheet C3 centralizes PSp, it commutes with the packet C3.
    # Their intersection is trivial because one lies in PSp and the other meets PSp trivially.
    # Any outer element is g*sigma with g in PSp; sigma inverts the sheet C3 and,
    # when chosen in the packet stabilizer, induces a transposition on the packet fiber.
    out={
      'pass':4664,
      'packet_S3':{'order3_location':packet_C3_location,'order3_subgroup':'C3_packet <= PSp','reflection':'outer PGSp coset element in support stabilizer'},
      'd4_sheet_S3':{'order3_location':sheet_C3_location,'order3_subgroup':'C3_sheet intersects PSp trivially','reflection':'W33 outer similitude coset','normalizer_order':155520,'quotient_over_PSp':'S3'},
      'separation':{'same_ambient_S3':False,'reason':'C3_packet is nontrivial inside PSp, whereas C3_sheet centralizes all of PSp and intersects PSp trivially; no automorphism preserving the distinguished PSp subgroup can identify them.'},
      'joint_group':{'C3s_commute':True,'C3_intersection_order':1,'rotation_subgroup':'C3 x C3','rotation_order':9,'common_outer_reflection_inverts_both':True,'generated_structure':'(C3 x C3):C2','generated_order':18},
      'fiber_reading':'The packet S3 acts locally on three maximal partial spreads over one 45-object; the D4 sheet S3 acts globally on the three degree-36 spread sheets. Their standard 3-point permutation representations are abstractly isomorphic but the ambient actions are transverse.',
      'boundary':'Finite group/action theorem only; abstract S3 isomorphism is not used as an intertwiner and no physical family symmetry is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
