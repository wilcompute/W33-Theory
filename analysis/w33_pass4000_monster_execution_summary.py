#!/usr/bin/env python3
"""Pass 4000: fail-closed summary of executed Monster maximal-overgroup acquisition."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_3993_MONSTER_OVERGROUP_ACQUISITION.json';OUT=ROOT/'data/PART_4000_MONSTER_EXECUTION_SUMMARY.json'
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
 if not SRC.exists():raise FileNotFoundError('Run Pass 3993 GAP/mmgroup acquisition first')
 x=json.loads(SRC.read_text());invent=x.get('matched_explicit_overgroups',[])
 pools=sum(int(r.get('bounded_search',{}).get('pool_size',0)) for r in invent)
 order3=sum(int(r.get('bounded_search',{}).get('order3_candidates',0)) for r in invent)
 tested=sum(int(r.get('bounded_search',{}).get('quadruples_tested',0)) for r in invent)
 payload={'schema':'w33.pass4000.monster_execution_summary.v1','status':'PASS_CONCRETE_MONSTER_U42_WORDS' if x.get('candidate') else 'PASS_EXECUTED_BOUNDED_SEARCH_NO_PROMOTED_WORDS','direct_class_fusions':x.get('direct_class_fusions'),'monster_maximal_tables':x.get('monster_maximal_tables'),'compatible_overgroups':x.get('compatible_overgroups',[]),'database_commit':x.get('database_commit'),'database_key_count':x.get('database_key_count'),'explicit_overgroup_records':len(invent),'aggregate_pool_elements':pools,'aggregate_order3_candidates':order3,'aggregate_quadruples_tested':tested,'candidate':x.get('candidate'),'promoted':bool(x.get('candidate')),'boundary':'A negative bounded search is not a proof that U4(2) is absent from the Monster. Promotion requires portable MM words plus the existing order, object-action, and class-fusion firewalls.'}
 payload['semantic_sha256']=sha(payload);OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print('PASS_MONSTER_EXECUTION_SUMMARY',payload['status'],tested,payload['semantic_sha256'])
if __name__=='__main__':main()
