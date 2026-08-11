#!/usr/bin/env python3
"""Pass 4831 bonkers — falsify the tempting 12 deep-hole orbits = 12 residue orbitals match.

Pass4812 classifies the H10 deep holes into twelve PSp(4,3) orbits. Pass4737
classifies ordered pairs in the transitive 270-residue action into twelve
orbitals with subdegrees 1,12,16,48,16,6,24,96,12,12,24,3.

A genuine component-by-component PSp G-set identification would preserve the
homogeneous orbit sizes and stabilizer orders. They do not match. This pass
freezes that obstruction explicitly so the shared number 12 cannot be reused as
an identification later.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4831_DEEPHOLE_RESIDUE_12X12_FALSIFIER.json'

def main():
    H=json.loads((ROOT/'data/PART_W33_PASS4812_H10_DEEP_HOLE_ORBITS.json').read_text())
    deep_sizes=sorted(int(o['PSp_cosets']) for o in H['orbits'])
    deep_stabs=sorted(int(o['PSp_stabilizer']) for o in H['orbits'])
    assert len(deep_sizes)==12 and sum(deep_sizes)==82080
    sub=[1,12,16,48,16,6,24,96,12,12,24,3]
    G=25920;point_stab=96;carrier=270
    residue_sizes=sorted(carrier*d for d in sub)
    residue_stabs=sorted(point_stab//d for d in sub)
    assert all(point_stab%d==0 for d in sub)
    assert residue_sizes!=deep_sizes and residue_stabs!=deep_stabs
    out={'pass':4831,
      'H10_deep_hole_orbits':{'count':12,'orbit_size_multiset':dict(sorted(Counter(deep_sizes).items())),'stabilizer_order_multiset':dict(sorted(Counter(deep_stabs).items()))},
      'residue_ordered_pair_orbitals':{'count':12,'subdegrees':sub,'orbit_size_multiset':dict(sorted(Counter(residue_sizes).items())),'ordered_pair_stabilizer_order_multiset':dict(sorted(Counter(residue_stabs).items()))},
      'componentwise_PSp_Gset_identification_exists':False,
      'obstruction':'homogeneous PSp orbit sizes and stabilizer-order multisets differ; e.g. residue orbitals include sizes 270, 810, 1620 and 25920, while H10 deep-hole orbits include sizes 1080 and 2160 and have no components of those residue sizes',
      'theorem':'The equality 12=12 between the Pass4812 H10 deep-hole orbit count and the Pass4737 residue-action orbital rank is numerology, not an equivariant identification. No componentwise PSp-homogeneous G-set bijection can match the two twelve-part decompositions.',
      'boundary':'This falsifies the direct twelve-component G-set identification. It does not forbid more indirect incidence maps between the H10 coset geometry and residue-pair geometry.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
