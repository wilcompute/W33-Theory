#!/usr/bin/env python3
"""Pass5726 addendum: identify the 14D Jacobiator complement with the canonical E8 A2 sector.

Consumes the exact rank/support certificate and the existing E8 root metadata.
The metadata already encodes the Z3 grading 78+81+81 and an su3_weight for each
root.  Among the 78 grade-zero roots, exactly six carry nonzero su3_weight; these
are the canonical A2 roots in the repository's E6 x A2 branching.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RANK=ROOT/'data/PART_W33_PASS5726_EXACT_FIREWALL_JACOBIATOR_RANK.json'
SC=ROOT/'extracted_v13/W33-Theory-master/artifacts/e8_structure_constants_w33_discrete.json'
META=ROOT/'extracted_v13/W33-Theory-master/artifacts/e8_root_metadata_table.json'
OUT=ROOT/'data/PART_W33_PASS5726_FAMILY_A2_COMPLEMENT_IDENTIFICATION.json'

def main():
 rank=json.loads(RANK.read_text());sc=json.loads(SC.read_text());meta=json.loads(META.read_text())
 assert rank['rank_over_Q']==234 and rank['untouched_complement_dimension']==14
 roots=[tuple(int(x) for x in r) for r in sc['basis']['roots']];cartan=int(sc['basis']['cartan_dim']);assert cartan==8
 rows={tuple(int(x) for x in r['root_orbit']):r for r in meta['rows']};assert len(rows)==240
 comp=set(int(i) for i in rank['untouched_complement_indices'])
 assert set(range(cartan)).issubset(comp)
 comp_roots={roots[i-cartan] for i in comp if i>=cartan};assert len(comp_roots)==6
 g0={r for r,row in rows.items() if row['grade']=='g0'}
 g1={r for r,row in rows.items() if row['grade']=='g1'}
 g2={r for r,row in rows.items() if row['grade']=='g2'}
 assert (len(g0),len(g1),len(g2))==(78,81,81)
 a2={r for r,row in rows.items() if row['grade']=='g0' and tuple(row.get('su3_weight',(0,0)))!=(0,0)}
 e6={r for r,row in rows.items() if row['grade']=='g0' and tuple(row.get('su3_weight',(0,0)))==(0,0)}
 assert (len(a2),len(e6))==(6,72)
 assert a2==comp_roots
 support=set(int(i) for i in rank['output_support_indices']);assert not any(i<cartan for i in support)
 support_roots={roots[i-cartan] for i in support};assert support_roots==e6|g1|g2
 assert len(support_roots)==72+81+81==234
 weights=Counter(tuple(rows[r]['su3_weight']) for r in a2)
 out={
  'pass':5726,
  'status':'JACOBIATOR_IMAGE_IS_EXACTLY_72_E6_PLUS_81_PLUS_81_ROOT_COORDINATES__COMPLEMENT_IS_CARTAN8_PLUS_CANONICAL_A2_ROOTS',
  'image_dimension':234,
  'image_root_decomposition':{'E6_grade0_roots':72,'g1_matter_roots':81,'g2_conjugate_matter_roots':81},
  'image_contains_cartan_coordinates':False,
  'complement_dimension':14,
  'complement_decomposition':{'Cartan_coordinates':8,'canonical_A2_roots':6},
  'canonical_A2_match':True,
  'A2_su3_weight_histogram':{str(k):v for k,v in sorted(weights.items(),key=lambda kv:str(kv[0]))},
  'historical_bridge':'Matches the repository E8 -> E6 x A2 root branching 240=72+6+81+81: the Jacobiator image occupies exactly the 72+81+81 part and misses exactly the six A2 roots plus all eight Cartan coordinates.',
  'reductive_complement_reading':'Together with the Pass5726 closure check, the untouched 14D coordinate subalgebra is A2 + T6: the canonical family A2 root subsystem with its rank-2 Cartan inside the full rank-8 Cartan, plus a six-dimensional central torus for this subalgebra.',
  'identification_boundary':'This is an exact match to the repository canonical E8 A2 factor. It does not identify that finite/algebraic family factor with QCD color or the separately constructed affine su3 without an explicit common action.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
