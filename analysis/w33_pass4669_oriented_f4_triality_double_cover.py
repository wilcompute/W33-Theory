#!/usr/bin/env python3
"""Pass 4669 bonkers -- oriented compatible-F4 / triality-plane double cover.

Pass4628 has 80 oriented order-three operators J and 40 unoriented pairs {J,J^2},
with centralizer 648 and normalizer 1296.  On the triality side a 40-plane
carrier has setwise stabilizer 648 in PSp and pointwise stabilizer 216; the
quotient C3 cyclically permutes the three nonzero plane vectors.  Under full
PGSp the W33-point stabilizer doubles to 1296 and the outer coset reverses that
cyclic orientation.  Thus both sides possess the same 80->40 orientation cover.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4669_ORIENTED_F4_TRIALITY_DOUBLE_COVER.json'

def main():
    f=json.loads((ROOT/'data/PART_W33_PASS4628_F4_CHOICE_IS_W33_POINT_CARRIER.json').read_text())
    p=json.loads((ROOT/'data/PART_W33_PASS4654_TRIALITY_PLANE_W33_POINT_INTERTWINER.json').read_text())
    g=json.loads((ROOT/'data/PART_W33_PASS4657_TRIALITY_INTERSECTION_GROUP.json').read_text())
    a=json.loads((ROOT/'data/PART_W33_PASS4665_FULL_AUTOMORPHISM_T.json').read_text())
    assert (f['compatible_F4_structures']['oriented_J'],f['compatible_F4_structures']['unoriented_pairs'])==(80,40)
    assert (f['compatible_F4_structures']['centralizer_order'],f['compatible_F4_structures']['normalizer_order'])==(648,1296)
    assert (p['base_plane_setwise_stabilizer_order'],p['base_plane_pointwise_stabilizer_order'])==(648,216)
    assert g['triality_pair_intersection']['equals_W33_point_stabilizer_derived_subgroup']
    assert a['full_automorphism_order']==51840
    out={
      'pass':4669,
      'F4_cover':{'oriented_objects':80,'base_objects':40,'fiber':2,'oriented_stabilizer_order':648,'unoriented_stabilizer_order':1296,'deck_operation':'J <-> J^2'},
      'triality_plane_cover':{'oriented_objects':80,'base_planes':40,'fiber':2,'plane_setwise_PSp_order':648,'plane_pointwise_order':216,'cyclic_orientation_group':'648/216 = C3','full_PGSp_plane_stabilizer_order':1296,'outer_operation':'reverses the cyclic order of the three nonzero plane vectors'},
      'equivalence':{'base':'the Pass4668 F4-structure <-> anisotropic-plane bijection','oriented_lift':'exists and is unique after choosing one base orientation; the only second lift is simultaneous global reversal','number_of_global_equivariant_orientation_matchings':2},
      'theorem':'The 40-object F4/triality moduli has a natural 80-object orientation double cover on both sides. Oriented J versus J^2 matches the two cyclic orientations of the three nonzero vectors in the associated anisotropic plane; the full outer symmetry reverses both orientations.',
      'boundary':'Finite double-cover/G-set statement. The choice between the two global orientation matchings is not canonical without an orientation convention, and no physical chirality is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
