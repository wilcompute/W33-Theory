#!/usr/bin/env python3
"""Passes 3217 and 3222: content-addressed shard/candidate evidence accumulator.

The accumulator binds every runtime or M36 shard to its schema, index, total,
engine/source identity, result digest, record count, and status.  It rejects
missing or duplicate indices before declaring completeness, builds domain-
separated Merkle roots, derives deterministic audit challenges, and verifies
inclusion proofs.  The construction is an integrity/provenance protocol, not a
claim of zero-knowledge, consensus, or cryptographic security beyond SHA-256.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=DATA/'PART_BT3217_BT3222_PROOF_ACCUMULATOR.json'

def enc(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def h(tag,payload):return hashlib.sha256(tag+b'\0'+payload).digest()
def hx(x):return x.hex()
def leaf_hash(leaf):return h(b'W33-SHARD-LEAF-V1',enc(leaf))
def parent(left,right):return h(b'W33-MERKLE-NODE-V1',left+right)

def merkle(leaves):
 if not leaves:return h(b'W33-MERKLE-EMPTY-V1',b''),[]
 level=list(leaves);levels=[level]
 while len(level)>1:
  if len(level)%2:level=level+[level[-1]]
  level=[parent(level[i],level[i+1]) for i in range(0,len(level),2)]
  levels.append(level)
 return level[0],levels

def proof(levels,index):
 out=[];i=index
 for level in levels[:-1]:
  padded=level if len(level)%2==0 else level+[level[-1]]
  sibling=i^1;out.append({'side':'left' if sibling<i else 'right','hash':hx(padded[sibling])});i//=2
 return out

def verify_inclusion(leaf,index,path,root):
 value=leaf_hash(leaf);i=index
 for step in path:
  sibling=bytes.fromhex(step['hash'])
  value=parent(sibling,value) if step['side']=='left' else parent(value,sibling);i//=2
 return value.hex()==root

def file_sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def normalize_runtime(path):
 d=json.loads(path.read_text());required={'schema','shard_index','shard_count','plan_sha256','records'}
 if not required<=set(d):raise ValueError(f'bad runtime shard {path}')
 records=d['records']
 return {'kind':'isa_runtime','schema':d['schema'],'index':int(d['shard_index']),'count':int(d['shard_count']),
  'engine_sha256':hashlib.sha256((ROOT/'analysis/bt3214_all194_runtime.py').read_bytes()).hexdigest(),
  'source_commit':d.get('source_commit','branch-source-unobserved'),'plan_sha256':d['plan_sha256'],
  'result_sha256':file_sha(path),'record_count':len(records),
  'candidate_count':0,'status':'COMPLETE_SHARD' if all(r.get('full_group',{}).get('group_order_reached')==4199040 for r in records) else 'INVALID_SHARD'}

def normalize_m36(path):
 d=json.loads(path.read_text());required={'schema','shard_index','shard_count','engine_sha256','candidates'}
 if not required<=set(d):raise ValueError(f'bad M36 shard {path}')
 candidates=d['candidates'];candidate_hashes=[hx(h(b'W33-M36-CANDIDATE-V1',enc(c))) for c in candidates]
 candidate_root,_=merkle([bytes.fromhex(x) for x in candidate_hashes])
 return {'kind':'m36_rank3','schema':d['schema'],'index':int(d['shard_index']),'count':int(d['shard_count']),
  'engine_sha256':d['engine_sha256'],'source_commit':d.get('source_commit','branch-source-unobserved'),
  'plan_sha256':d.get('plan_sha256','pass3125-materialized-contract'),
  'result_sha256':file_sha(path),'record_count':int(d.get('examined_count',d.get('record_count',0))),
  'candidate_count':len(candidates),'candidate_root':hx(candidate_root),
  'status':'COMPLETE_SHARD' if int(d['shard_count'])==256 else 'INVALID_SHARD'}

def deterministic_challenges(root,count,number):
 out=[];counter=0
 while len(out)<min(number,count):
  value=int.from_bytes(h(b'W33-AUDIT-CHALLENGE-V1',bytes.fromhex(root)+counter.to_bytes(8,'big')),'big')%count
  if value not in out:out.append(value)
  counter+=1
 return out

def accumulate(kind,paths,expected_count):
 normalizer=normalize_runtime if kind=='isa_runtime' else normalize_m36
 rows=[normalizer(p) for p in sorted(paths)]
 by={}
 for row in rows:
  if row['kind']!=kind:raise AssertionError('kind mismatch')
  if row['index'] in by:raise AssertionError(f'duplicate {kind} shard {row["index"]}')
  by[row['index']]=row
 present=sorted(by);missing=sorted(set(range(expected_count))-set(present))
 count_values=sorted({r['count'] for r in rows})
 plan_values=sorted({r['plan_sha256'] for r in rows})
 engine_values=sorted({r['engine_sha256'] for r in rows})
 valid=(not missing and present==list(range(expected_count)) and count_values==[expected_count]
        and len(plan_values)==1 and all(r['status']=='COMPLETE_SHARD' for r in rows))
 ordered=[by[i] for i in present];hashes=[leaf_hash(x) for x in ordered];root,levels=merkle(hashes)
 challenge_indices=deterministic_challenges(hx(root),len(ordered),max(4,(len(ordered).bit_length()+1))) if ordered else []
 challenge_rows=[]
 for i in challenge_indices:
  pr=proof(levels,i);assert verify_inclusion(ordered[i],i,pr,hx(root))
  challenge_rows.append({'position':i,'shard_index':ordered[i]['index'],'leaf_sha256':hx(hashes[i]),'proof':pr})
 return {'kind':kind,'expected_count':expected_count,'present_count':len(rows),'present_indices':present,
  'missing_indices':missing,'count_values':count_values,'plan_sha256_values':plan_values,
  'engine_sha256_values':engine_values,'complete':valid,'status':'COMPLETE' if valid else 'INCOMPLETE_FAIL_CLOSED',
  'merkle_root':hx(root),'total_records':sum(r['record_count'] for r in rows),
  'total_candidates':sum(r['candidate_count'] for r in rows),'audit_challenges':challenge_rows,'leaves':ordered}

def synthetic_selftest():
 leaves=[{'kind':'test','schema':'v1','index':i,'count':8,'engine_sha256':'11'*32,
          'source_commit':'test','plan_sha256':'22'*32,'result_sha256':hashlib.sha256(str(i).encode()).hexdigest(),
          'record_count':1,'candidate_count':0,'status':'COMPLETE_SHARD'} for i in range(8)]
 hashes=[leaf_hash(x) for x in leaves];root,levels=merkle(hashes)
 checks=[]
 for i,row in enumerate(leaves):checks.append(verify_inclusion(row,i,proof(levels,i),hx(root)))
 tampered=dict(leaves[3]);tampered['record_count']=2
 assert all(checks) and not verify_inclusion(tampered,3,proof(levels,3),hx(root))
 duplicate_rejected=False
 try:
  by={}
  for row in leaves+[leaves[0]]:
   if row['index'] in by:raise AssertionError('duplicate')
   by[row['index']]=row
 except AssertionError:duplicate_rejected=True
 assert duplicate_rejected
 return {'all_inclusion_proofs':True,'tampered_leaf_rejected':True,'duplicate_index_rejected':True,'root':hx(root)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runtime-pattern',default='data/PART_BT3214_ISA_SHARD_*.json')
 ap.add_argument('--m36-pattern',default='data/PART_BT3165_M36_NORMALIZED_SHARD_*.json');a=ap.parse_args()
 runtime=accumulate('isa_runtime',[Path(x) for x in glob.glob(str(ROOT/a.runtime_pattern))],32)
 m36=accumulate('m36_rank3',[Path(x) for x in glob.glob(str(ROOT/a.m36_pattern))],256)
 roots=[bytes.fromhex(runtime['merkle_root']),bytes.fromhex(m36['merkle_root'])]
 umbrella,_=merkle(roots)
 result={'schema':'w33.pass3217_3222.proof_accumulator.v1','status':'COMPLETE_BOTH' if runtime['complete'] and m36['complete'] else 'INCOMPLETE_FAIL_CLOSED',
  'runtime':runtime,'m36':m36,'umbrella_root':hx(umbrella),'selftest':synthetic_selftest(),
  'authorization_rule':'An M36 candidate may reach the independent authorizer only from a complete 256-shard root, a valid candidate inclusion proof, matching engine/source identities, and an independently accepted proof envelope.',
  'naysayer_rule':'A counterexample is actionable when it supplies an inclusion proof to a committed leaf plus a deterministic violation: bad group order, stale plan hash, malformed candidate, duplicate index, digest mismatch, or independent-certificate rejection.',
  'boundary':'SHA-256/Merkle integrity and deterministic challenges do not prove honest computation, zero knowledge, consensus, or cryptographic soundness. Full recomputation and independent certification remain authoritative.'}
 DATA.mkdir(exist_ok=True);OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'runtime':runtime['present_count'],'m36':m36['present_count'],'root':result['umbrella_root']},sort_keys=True))
if __name__=='__main__':main()
