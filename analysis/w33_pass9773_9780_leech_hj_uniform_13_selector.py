#!/usr/bin/env python3
"""Pass9773-9780 outside-box: corrected Leech type-free generator vs HJ carrier.

Use only the corrected Pass9701 invariant: V2 has 4095 intrinsic type-8 frames and
zero type-4 classes (generic singular-generator baseline 48).  Ask what a uniform
common quotient with the 416 Hall-Janko vertices / 20,800 G2(4) edges could have.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9773_9780_LEECH_HJ_UNIFORM_13_SELECTOR.json'

def divisors(n):return [d for d in range(1,n+1) if n%d==0]
def main():
 corr=json.loads((ROOT/'data/PART_W33_PASS9701_9724_CORRECTIONS.json').read_text())
 hj=json.loads((ROOT/'data/PART_W33_PASS9085_9092_LEECH_G24_GRAPH_EDGES.json').read_text())
 assert corr['what_survives']['result']=='V_2 holds 0 type-4 classes; a generic generator holds 48'
 frames=4095;vertices=hj['G2(4)_graph']['vertices'];edges=hj['G2(4)_graph']['edges']
 assert (vertices,edges)==(416,20800)
 gv=math.gcd(frames,vertices);ge=math.gcd(frames,edges);gall=math.gcd(gv,edges)
 assert (gv,ge,gall)==(13,65,13)
 assert divisors(gall)==[1,13]
 q=3;phi3=q*q+q+1;assert phi3==13
 out={'schema':'w33.pass9773_9780.leech_hj_uniform_13_selector.v1','status':'PASS','passes':'9773-9780','outside_box':True,
 'corrected_Leech_input':{'type4_in_V2':0,'generic_generator_baseline':48,'intrinsic_type8_frames_in_V2':frames,'warning':'No frame-independent identification of V2 with one of the nine length-24 Type II code classes is used.'},
 'Hall_Janko_G24_input':{'HJ_vertices':vertices,'Leech_sixspace_edges':edges,'degree':100},
 'gcd_arithmetic':{'gcd_frames_HJ_vertices':gv,'gcd_frames_G24_edges':ge,'gcd_all_three':gall,'nontrivial_common_uniform_quotient_size':13,'Phi3_at_q3':phi3},
 'conditional_theorem':'Suppose the 4,095 intrinsic type-8 frames of V2, the 416 Hall-Janko copies, and the 20,800 G2(4) edges all admit surjections onto one common selector set S with constant fiber size on each source (the minimal regularity expected from a transitive/equivariant common quotient). Then |S| divides all three cardinalities, hence |S| divides gcd(4095,416,20800)=13. Therefore the only nontrivial possible uniform common quotient has exactly 13 states.',
 'interpretation':'The arithmetic does not construct the quotient, but it makes Phi_3(3)=13 the unique nontrivial size allowed by a uniform three-way Leech-frame/Hall-Janko/edge selector. This is substantially sharper than the raw shared-factor observation because all other quotient sizes are excluded under the stated regularity condition.',
 'boundary':'Conditional divisibility theorem only. Uniform fibers/equivariance are not yet proved, and no 13-state quotient is claimed to exist. The corrected Pass9701 type-4-free invariant is used; the retracted frame-independent Golay claim is not.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','common_gcd':gall,'only_nontrivial_uniform_size':13}));return 0
if __name__=='__main__':raise SystemExit(main())
