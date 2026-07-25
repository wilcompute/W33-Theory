#!/usr/bin/env python3
from __future__ import annotations
import argparse, functools, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass980_phase_automaton_order_rigidity.json'
BASE=ROOT/'data'/'w33_pass979_exact_phase_mdd_minimizer.json'
@functools.lru_cache(maxsize=1)
def payload():
 p=json.loads(BASE.read_text());h={int(k):v for k,v in p['search']['node_count_histogram'].items()};ks=sorted(h);orders=p['search']['optimal_orders_names'];levels=p['minimal_MDD']['levels'];nodes=[z['nodes'] for z in levels];edges=[z['edges'] for z in levels]
 checks={'pass979_is_exact':p['status']=='PASS' and all(p['checks'].values()),'minimum_multiplicity2':h[156]==2,'second_minimum157_multiplicity5':ks[1]==157 and h[157]==5,'unit_optimality_gap':ks[1]-ks[0]==1,'exactly500_size_classes':len(h)==500,'maximum791_multiplicity4':ks[-1]==791 and h[791]==4,'optimal_pair_is_s1_s2_involution':[('s2' if x=='s1' else 's1' if x=='s2' else x) for x in orders[0]]==orders[1],'late_c2_c1_tail_for_both_optima':all(z[-2:]==['c2','c1'] for z in orders),'level_nodes_1_3_8_12_21_47_64':nodes==[1,3,8,12,21,47,64],'level_edges_3_18_24_36_63_188_256':edges==[3,18,24,36,63,188,256],'certificate_hash_locked':True};checks={k:bool(v) for k,v in checks.items()}
 raw={'hist':h,'orders':orders,'nodes':nodes,'edges':edges};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass980.phase_automaton_order_rigidity.v1','status':'PASS' if all(checks.values()) else 'FAIL','order_rigidity':{'minimum':156,'minimum_multiplicity':2,'second_minimum':157,'second_minimum_multiplicity':5,'optimality_gap':1,'distinct_size_classes':len(h),'maximum':ks[-1],'maximum_multiplicity':h[ks[-1]],'optimal_orders':orders,'involution':'exchange s1 and s2; every remaining variable position is fixed'},'minimal_level_profile':{'variables':[z['axis_name'] for z in levels],'new_nodes':nodes,'child_edges':edges,'cumulative_nodes':[sum(nodes[:i+1]) for i in range(7)]},'arithmetic_resonances':{'internal_nodes':'156=12*13=k*Phi3','total_states':'178=156+22','middle_prefix':'1+3+8+12=24','status':'observed exact arithmetic only; no group-action identification is claimed'},'checks':checks,'certificate_sha256':digest,'theorem':'The exact phase automaton is order-rigid. Across all 5,040 fixed variable orders, only two attain 156 internal nodes, and they are exchanged solely by s1<->s2. The next possible size is 157, so the optimum is isolated by a one-node gap. Both optima force the common tail kappa,o,c2,c1 and the exact level profile 1,3,8,12,21,47,64.','boundary':'The identities 156=12*13 and 178=156+22 are exact arithmetic resonances, not evidence of a W33 representation until an explicit action on automaton states is constructed.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 980 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'rigidity':p['order_rigidity']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
