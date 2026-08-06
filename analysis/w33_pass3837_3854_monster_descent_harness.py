#!/usr/bin/env python3
"""Fail-closed Monster promotion harness for Passes 3837-3854."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEFAULT=ROOT/'data'/'PART_3837_3854_MONSTER_DESCENT_candidate.json'
REFERENCE=ROOT/'data'/'PART_3837_3854_OVOID_WEDDERBURN_CODE_LEECH_TRIALITY_results.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,default=DEFAULT);args=ap.parse_args()
 candidate=json.loads(args.candidate.read_text());reference=json.loads(REFERENCE.read_text())
 assert candidate['expected']['semantic_reference']==reference['semantic_sha256']
 if candidate['status']=='PENDING':
  assert not candidate['mmgroup_strings'] and not candidate['mmgroup_integers']
  assert candidate['class_fusion_artifact'] is None
  print('PENDING_3837_3854_NO_MONSTER_WORDS');return
 assert candidate['status']=='CANDIDATE'
 words=candidate['mmgroup_strings'];assert words and candidate['degree45_generators'] and candidate['degree200_generators']
 try:
  from mmgroup import MM
 except ImportError as exc:
  raise SystemExit('mmgroup is required for a populated candidate') from exc
 elements=[MM(word) for word in words]
 assert [str(MM(str(g))) for g in elements]==[str(g) for g in elements]
 # as_int is accepted only as a local hash key; strings remain the portable storage form.
 if candidate['mmgroup_integers']:
  assert [int(g.as_int()) for g in elements]==candidate['mmgroup_integers']
 fusion=Path(candidate['class_fusion_artifact']['path']);assert fusion.exists()
 assert hashlib.sha256(fusion.read_bytes()).hexdigest()==candidate['class_fusion_artifact']['sha256']
 carrier=candidate['carrier_certificate'];expected=candidate['expected']
 for key in ('full_group_order','even_subgroup_order','gq_points','gq_lines','plane_ovoids','tripods','norton_lines','d4_frames','ovoid_orbitals'):
  assert carrier[key]==expected[key]
 assert carrier['tripod_norton_orbits']==expected['tripod_norton_orbits']
 assert carrier['reference_semantic_sha256']==reference['semantic_sha256']
 print('PASS_3837_3854_MONSTER_CANDIDATE_GATE')
if __name__=='__main__':main()
