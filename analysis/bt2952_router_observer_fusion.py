#!/usr/bin/env python3
"""Pass 2952: fuse corrected frame telemetry with the 10x4 route address reversibly."""
from __future__ import annotations
import itertools,json,math,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2952_ROUTER_OBSERVER_FUSION_results.json'
valid=[]
for xp,zp,xf,zf in itertools.product(range(3),repeat=4):
 frame=27*xp+9*zp+3*xf+zf
 for line in range(10):
  for slot in range(4):
   address=4*line+slot;joint=40*frame+address;valid.append((frame,address,joint))
assert len(valid)==3240 and {r[-1] for r in valid}==set(range(3240))
raw_valid={(frame<<6)|address:joint for frame,address,joint in valid};invalid_in=sorted(set(range(8192))-set(raw_valid));P=[None]*8192
for i,o in raw_valid.items():P[i]=o
for i,o in zip(invalid_in,range(3240,8192)):P[i]=o
assert sorted(P)==list(range(8192));Pinv=[0]*8192
for i,o in enumerate(P):Pinv[o]=i
Hframe=math.log2(81);Haddr=math.log2(40);Hjoint=math.log2(3240)
strategies=[{'name':'fast_static_observer_plus_address','raw_bits':14,'correctable_bits':0,'compressed_fixed_bits':12},{'name':'optimal_affine_d4_observer_plus_address','raw_bits':21,'correctable_bits':1,'compressed_fixed_bits':12},{'name':'internal_rank_plus_address','raw_bits':13,'correctable_bits':0,'compressed_fixed_bits':12}]
for s in strategies:s['fixed_bit_saving']=s['raw_bits']-12;s['entropy_redundancy_bits']=s['raw_bits']-Hjoint
def h2(p):return 0 if p in (0,1) else -p*math.log2(p)-(1-p)*math.log2(1-p)
error_rows=[{'block_error_probability':p,'minimum_error_record_entropy_bits':h2(p)+p*math.log2(15)} for p in [1e-6,1e-4,1e-3,1e-2,.05]]
seen=set();hist=collections.Counter()
for i in range(8192):
 if i in seen:continue
 j=i;n=0
 while j not in seen:seen.add(j);n+=1;j=P[j]
 hist[n]+=1
checks={'3240_valid_joint_states':len(valid)==3240,'joint_rank_bijection':{r[-1] for r in valid}==set(range(3240)),'twelve_bits_suffice':2**11<3240<=2**12,'thirteen_to_twelve_reversible_extension':sorted(P)==list(range(8192)),'inverse_exact':all(Pinv[P[i]]==i for i in range(8192)),'entropy_adds':abs(Hjoint-Hframe-Haddr)<1e-12,'protected_pipeline_saves_nine_fixed_bits':strategies[1]['fixed_bit_saving']==9}
out={'schema':'w33.pass2952.router_observer_fusion.v1','status':'COMPLETE_EXACT_LOGICAL_COMPILER','checks':checks,'check_count':len(checks),'valid_joint_states':3240,'joint_rank_formula':'joint_rank = 40*(27*xp+9*zp+3*xf+zf) + (4*oam_line+slot)','raw_word_formula':'raw = (frame_rank << 6) | address','joint_entropy_bits':Hjoint,'frame_entropy_bits':Hframe,'address_entropy_bits':Haddr,'fixed_width_joint_bits':12,'invalid_joint_words':856,'permutation_size':8192,'permutation_cycle_histogram':{str(k):v for k,v in sorted(hist.items())},'strategies':strategies,'corrected_error_record_entropy':'h2(p)+p*log2(15) for no error versus one of fifteen probe-bit locations','error_record_rows':error_rows,'interpretation':'Correct the 15-probe distance-four observer, reversibly uncompute its redundancy, fuse the 7-bit frame rank with the 6-bit 10x4 route address, and retain one 12-bit joint rank. Only the sparse error record must eventually be erased.','claim_boundary':'Exact logical permutation and entropy ledger; no transistor/optical implementation or finite-time energy measurement is claimed.'};assert all(checks.values());OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"PASS {len(checks)}/{len(checks)} joint entropy={Hjoint}")
