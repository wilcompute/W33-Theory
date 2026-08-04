#!/usr/bin/env python3
"""Pass 2970: weld full-S4 pilots to the parity-curvature decoder."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT2970_LAYERED_ROUTE_FAULT_ARCHITECTURE_results.json'

def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2

def agreeing_on(p,q,slots):return all(p[s]==q[s] for s in slots)

def main():
 perms=list(itertools.permutations(range(4)));identity=tuple(range(4));nonid=[p for p in perms if p!=identity]
 assert len(perms)==24 and len(nonid)==23
 odd=[p for p in nonid if parity(p)];even=[p for p in nonid if not parity(p)]
 assert len(odd)==12 and len(even)==11
 one=[any(p[s]!=s for s in (0,)) for p in nonid]
 two=[any(p[s]!=s for s in (0,1)) for p in nonid]
 three=[any(p[s]!=s for s in (0,1,2)) for p in nonid]
 assert sum(one)==18 and sum(two)==22 and sum(three)==23
 assert all(sum(agreeing_on(p,q,(0,1,2)) for q in perms)==1 for p in perms)
 assert all(sum(agreeing_on(p,q,(0,1)) for q in perms)==2 for p in perms)
 pilot=json.loads((ROOT/'data/PART_BT2965_CURVATURE_ROUTE_CODE_results.json').read_text())
 curvature=json.loads((ROOT/'data/PART_BT2968_CURVATURE_ROUTE_CODE_results.json').read_text())
 assert pilot['minimum_universal_pilot_slots']==3
 assert pilot['three_pilot_detected']==pilot['three_pilot_fault_cases']==8280
 assert curvature['code']['parameters']=='[45,9,9]_2'
 assert curvature['raw_registers']['independent_syndrome_bits']==36
 checks={
  's4_has_23_nonidentity_faults':len(nonid)==23,
  'nonidentity_split_12_odd_11_even':(len(odd),len(even))==(12,11),
  'one_pilot_detects_18_of_23':sum(one)==18,
  'two_pilots_detect_22_of_23':sum(two)==22,
  'three_pilots_detect_all_23':sum(three)==23,
  'three_point_images_uniquely_determine_s4_permutation':all(sum(agreeing_on(p,q,(0,1,2)) for q in perms)==1 for p in perms),
  'two_point_images_leave_exactly_two_permutations':all(sum(agreeing_on(p,q,(0,1)) for q in perms)==2 for p in perms),
  'master_pilot_certificate_covers_all_8280_single_fault_cases':pilot['three_pilot_detected']==8280,
  'parity_layer_is_45_9_9_code':curvature['code']['parameters']=='[45,9,9]_2',
  'parity_layer_corrects_four_odd_faults_modulo_gauge':curvature['code']['correctable_fault_weight_modulo_gauge']==4,
 }
 assert all(checks.values())
 result={
  'schema':'w33.pass2970.layered_route_fault_architecture.v1','status':'COMPLETE_EXACT_LAYERED_FAULT_MODEL','checks':checks,'check_count':len(checks),
  'layer_A':{'name':'three-slot full-S4 pilot audit','coverage':'all 23 nonidentity S4 faults on one route edge','cases':8280,'role':'detect and identify even or odd single-edge route permutations'},
  'layer_B':{'name':'triangle-parity curvature decoder','code':'[45,9,9]_2','independent_bits':36,'role':'locate/correct up to four odd-parity edge faults modulo vertex gauge; detect nongauge odd faults through weight eight'},
  'combined_single_fault_theorem':'For one arbitrary nonidentity S4 edge fault, three pilots identify the complete permutation. If it is odd, the curvature syndrome additionally identifies its edge and participates in multi-edge decoding; if it is even, the pilot layer is essential because sign curvature is silent.',
  'resource_summary':{'pilot_slot_alphabet':3,'raw_triangle_checks':120,'independent_parity_checks':36},
  'headline':'Three pilots and the [45,9,9]_2 curvature code form complementary route defenses: the pilot layer is complete for one arbitrary S4 error, while the parity layer adds exact multi-edge correction for odd faults.',
  'claim_boundary':'No theorem here extends three-pilot completeness to simultaneous arbitrary S4 faults. Multi-edge guarantees apply only to the odd-parity projection; loss, drift and detector erasure remain in the calibrated channel model.',
 }
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS',len(checks),'/',len(checks),result['headline'])
if __name__=='__main__':main()
