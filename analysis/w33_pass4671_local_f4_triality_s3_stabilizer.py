#!/usr/bin/env python3
"""Pass 4671 bonkers -- the 216<648<1296 tower is a local S3 extension.

The triality plane pointwise stabilizer is H216=3^{1+2}:Q8 and is the derived
subgroup of the W33 point stabilizer H648=3^{1+2}:SL(2,3).  H648/H216=C3 is
exactly the cyclic action on the three nonzero vectors of the anisotropic plane.
The full PGSp point / semilinear F4 stabilizer has order 1296; its outer coset
reverses that cyclic order and exchanges J with J^2.  Hence H1296/H216=S3 and
H648 is the preimage of A3.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4671_LOCAL_F4_TRIALITY_S3_STABILIZER.json'

def main():
    g=json.loads((ROOT/'data/PART_W33_PASS4657_TRIALITY_INTERSECTION_GROUP.json').read_text())
    f=json.loads((ROOT/'data/PART_W33_PASS4628_F4_CHOICE_IS_W33_POINT_CARRIER.json').read_text())
    p=json.loads((ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json').read_text())
    o=json.loads((ROOT/'data/PART_W33_PASS4669_ORIENTED_F4_TRIALITY_DOUBLE_COVER.json').read_text())
    assert g['triality_pair_intersection']['order']==216 and g['triality_pair_intersection']['structure']=='3^{1+2}:Q8'
    assert g['W33_point_stabilizer']['order']==648 and g['W33_point_stabilizer']['structure']=='3^{1+2}:SL(2,3) = 3^{1+2}:2A4'
    assert g['triality_pair_intersection']['equals_W33_point_stabilizer_derived_subgroup']
    assert p['base_plane_pointwise_stabilizer_order']==216 and p['base_plane_setwise_stabilizer_order']==648
    assert f['compatible_F4_structures']['normalizer_order']==1296
    assert o['triality_plane_cover']['full_PGSp_plane_stabilizer_order']==1296
    out={
      'pass':4671,
      'tower':[
        {'order':216,'group':'H216=3^{1+2}:Q8','role':'pointwise stabilizer of the three nonzero anisotropic-plane vectors; derived subgroup of H648'},
        {'order':648,'group':'H648=3^{1+2}:SL(2,3)','role':'PSp W33-point / triality-plane stabilizer; quotient H648/H216=C3 gives cyclic orientation'},
        {'order':1296,'group':'H1296','role':'full PGSp W33-point / semilinear compatible-F4 stabilizer; outer coset reverses orientation'}],
      'quotients':{'H648_over_H216':'C3=A3','H1296_over_H648':'C2','H1296_over_H216':'S3'},
      'F4_action':'The C2 quotient exchanges J and J^2; the orientation-preserving index-two subgroup is H648.',
      'triality_plane_action':'The C3 quotient rotates the three nonzero plane vectors; adjoining the outer C2 gives all S3 permutations.',
      'exact_sequence':'1 -> (3^{1+2}:Q8)_216 -> H1296 -> S3 -> 1, with H648 the preimage of A3',
      'theorem':'The local stabilizer shared by the F4-choice and triality-plane descriptions has an exact S3 quotient. Its 216-kernel is the triality-conjugate PSp intersection, its 648 orientation-preserving layer is the W33 point stabilizer, and the 1296 semilinear layer adds the orientation-reversing outer involution.',
      'boundary':'Finite subgroup and local-orientation theorem only; S3 is not promoted to a physical family or chirality symmetry.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
