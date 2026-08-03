#!/usr/bin/env python3
"""Pass 2970: weld full-S4 pilots to the parity-curvature decoder."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2970_LAYERED_ROUTE_FAULT_ARCHITECTURE_results.json'
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
def agree(p,q,s):return all(p[x]==q[x] for x in s)
def main():
 ps=list(itertools.permutations(range(4)));non=[p for p in ps if p!=tuple(range(4))];odd=[p for p in non if parity(p)];even=[p for p in non if not parity(p)];assert (len(non),len(odd),len(even))==(23,12,11)
 one=[any(p[s]!=s for s in(0,)) for p in non];two=[any(p[s]!=s for s in(0,1)) for p in non];three=[any(p[s]!=s for s in(0,1,2)) for p in non];assert (sum(one),sum(two),sum(three))==(18,22,23)
 assert all(sum(agree(p,q,(0,1,2)) for q in ps)==1 for p in ps) and all(sum(agree(p,q,(0,1)) for q in ps)==2 for p in ps)
 pilot=json.loads((ROOT/'data/PART_BT2965_CURVATURE_ROUTE_CODE_results.json').read_text());cur=json.loads((ROOT/'data/PART_BT2968_CURVATURE_ROUTE_CODE_results.json').read_text());assert pilot['minimum_universal_pilot_slots']==3 and pilot['three_pilot_detected']==pilot['three_pilot_fault_cases']==8280 and cur['code']['parameters']=='[45,9,9]_2'
 checks={'s4_has_23_nonidentity_faults':True,'nonidentity_split_12_odd_11_even':True,'one_pilot_detects_18_of_23':True,'two_pilots_detect_22_of_23':True,'three_pilots_detect_all_23':True,'three_point_images_uniquely_determine_s4_permutation':True,'two_point_images_leave_exactly_two_permutations':True,'master_pilot_certificate_covers_all_8280_single_fault_cases':True,'parity_layer_is_45_9_9_code':True,'parity_layer_corrects_four_odd_faults_modulo_gauge':cur['code']['correctable_fault_weight_modulo_gauge']==4};assert all(checks.values())
 result={'schema':'w33.pass2970.layered_route_fault_architecture.v1','status':'COMPLETE_EXACT_LAYERED_FAULT_MODEL','checks':checks,'check_count':10,'layer_A':{'name':'three-slot full-S4 pilot audit','coverage':'all 23 nonidentity S4 faults on one route edge','cases':8280,'role':'detect and identify even or odd single-edge route permutations'},'layer_B':{'name':'triangle-parity curvature decoder','code':'[45,9,9]_2','independent_bits':36,'role':'correct up to four odd edge faults modulo gauge and detect nongauge odd faults through weight eight'},'combined_single_fault_theorem':'Three pilots identify one arbitrary nonidentity S4 edge fault. Odd faults additionally enter the multi-edge curvature decoder; even faults require pilots because sign curvature is silent.','headline':'Three pilots and the [45,9,9]_2 curvature code form complementary route defenses.','claim_boundary':'No simultaneous arbitrary-S4 pilot theorem; multi-edge guarantees apply only to odd parity.'}
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS 10 / 10',result['headline'])
if __name__=='__main__':main()
