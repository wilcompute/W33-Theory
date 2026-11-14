#!/usr/bin/env python3
"""Pass 3217: plan-bound adapter for the merged Pass-3125 rank-three M36 engine.

The adapter never reimplements the 50,868,675-subspace search.  It materializes
and discovers the canonical engine, executes one logical shard, normalizes its
output, binds it to a plan and engine digest, and aggregates only all 256 unique
shards.  A zero-candidate no-go is available only when exact examined coverage
sums to 50,868,675 and independent certification remains a separate gate.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
EXPECTED=50_868_675
PLAN=DATA/'PART_BT3217_M36_SHARD_PLAN.json'

def enc(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def sha(obj):return hashlib.sha256(enc(obj)).hexdigest()
def file_sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def plan():
 body={'logical_shard_count':256,'workflow_bucket_count':32,'shards_per_bucket':8,
       'expected_isotropic_subspaces':EXPECTED,
       'mapping':{str(b):[b+32*k for k in range(8)] for b in range(32)},
       'engine_contract':'merged Pass-3125 duplicate-free rank-three M36 census'}
 payload={'schema':'w33.pass3217.m36_plan.v1','status':'EXACT_EXECUTION_PLAN',**body,
          'plan_sha256':sha(body),'boundary':'Execution plan only; no shard or candidate result.'}
 PLAN.parent.mkdir(exist_ok=True);PLAN.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'shards':256,'plan_sha256':payload['plan_sha256']},sort_keys=True))

def load_plan():
 if not PLAN.exists():plan()
 p=json.loads(PLAN.read_text());body={k:p[k] for k in ('logical_shard_count','workflow_bucket_count','shards_per_bucket','expected_isotropic_subspaces','mapping','engine_contract')}
 assert sha(body)==p['plan_sha256'] and p['logical_shard_count']==256
 return p

def materialize():
 candidates=[ROOT/'tools/materialize_bt3124_bt3132_bundle.py',ROOT/'tools/materialize_bt3124_3132_bundle.py']
 for path in candidates:
  if path.exists():
   subprocess.run([sys.executable,str(path)],cwd=ROOT,check=True);return str(path.relative_to(ROOT))
 return None

def discover_engine():
 patterns=['analysis/*3125*rank3*m36*.py','analysis/*3125*m36*.py','analysis/*3125*rank*three*.py','analysis/*3125*.py']
 files=[]
 for pattern in patterns:files.extend(ROOT.glob(pattern))
 unique={p.resolve():p for p in files if p.name!='bt3217_m36_sharded_census.py'}
 files=list(unique.values())
 if not files:raise FileNotFoundError('no materialized Pass-3125 engine')
 files.sort(key=lambda p:(('rank3' not in p.name.lower())+('m36' not in p.name.lower()),len(p.name),p.name))
 return files[0]

def cli_for(source,index,count,out):
 text=source.read_text(errors='replace')
 flags=set(re.findall(r"add_argument\(\s*['\"](--[A-Za-z0-9_-]+)",text))
 def pick(groups):return next((f for f in sorted(flags) if all(x in f.lower() for x in groups)),None)
 fi=pick(('shard','index')) or pick(('shard','id'))
 fc=pick(('shard','count')) or pick(('shard','total')) or pick(('num','shard'))
 fo=pick(('output',)) or pick(('out',))
 cmd=[sys.executable,str(source)]
 if fi:cmd += [fi,str(index)]
 if fc:cmd += [fc,str(count)]
 if fo:cmd += [fo,str(out)]
 return cmd,sorted(flags)

def recursive_candidates(obj):
 out=[]
 if isinstance(obj,dict):
  if isinstance(obj.get('generators'),list) or isinstance(obj.get('projector'),(list,dict)):
   if any(k in obj for k in ('accepted','success_probability','projector','logical_frame')):out.append(obj)
  for value in obj.values():out.extend(recursive_candidates(value))
 elif isinstance(obj,list):
  for value in obj:out.extend(recursive_candidates(value))
 return out

def recursive_counts(obj):
 values=[]
 keys={'examined_count','subspace_count','tested_count','tested','enumerated_count','processed_count','count_examined'}
 if isinstance(obj,dict):
  for key,value in obj.items():
   if key.lower() in keys and isinstance(value,int) and value>=0:values.append(value)
   values.extend(recursive_counts(value))
 elif isinstance(obj,list):
  for value in obj:values.extend(recursive_counts(value))
 return values

def run_shard(index,count):
 assert count==256 and 0<=index<count
 p=load_plan();materializer=materialize();engine=discover_engine()
 raw=DATA/f'PART_BT3217_M36_RAW_SHARD_{index:03d}.json'
 before={x.resolve() for x in DATA.glob('*.json')}
 cmd,flags=cli_for(engine,index,count,raw)
 env=os.environ.copy();env.update({'W33_SHARD_INDEX':str(index),'W33_SHARD_COUNT':str(count),'W33_SHARD_OUTPUT':str(raw)})
 start=time.time();cp=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True)
 if cp.returncode:
  raise RuntimeError(json.dumps({'engine':str(engine.relative_to(ROOT)),'command':cmd,'stdout_tail':cp.stdout[-4000:],'stderr_tail':cp.stderr[-4000:]},indent=2))
 payloads=[]
 if raw.exists():
  try:payloads.append(json.loads(raw.read_text()))
  except Exception:pass
 for path in DATA.glob('*.json'):
  if path.resolve() not in before and path!=raw and ('3125' in path.name or 'M36' in path.name.upper()):
   try:payloads.append(json.loads(path.read_text()))
   except Exception:pass
 try:payloads.append(json.loads(cp.stdout))
 except Exception:pass
 candidates=[];counts=[]
 for obj in payloads:candidates+=recursive_candidates(obj);counts+=recursive_counts(obj)
 # The maximum is used only when multiple nested summaries repeat the same coverage.
 examined=max(counts) if counts else None
 candidate_envelopes=[]
 for ordinal,candidate in enumerate(candidates):
  body={'shard_index':index,'ordinal':ordinal,'engine_sha256':file_sha(engine),
        'plan_sha256':p['plan_sha256'],'candidate':candidate}
  candidate_envelopes.append({**body,'candidate_sha256':sha(body)})
 status='COMPLETE_SHARD_COVERAGE_REPORTED' if examined is not None else 'COMPLETE_SHARD_COVERAGE_UNREPORTED'
 result={'schema':'w33.pass3217.m36_shard.v1','status':status,'shard_index':index,'shard_count':count,
  'plan_sha256':p['plan_sha256'],'engine':str(engine.relative_to(ROOT)),'engine_sha256':file_sha(engine),
  'materializer':materializer,'detected_cli_flags':flags,'elapsed_seconds':time.time()-start,
  'payload_count':len(payloads),'examined_count':examined,'candidate_count':len(candidate_envelopes),
  'candidates':candidate_envelopes,'source_commit':os.environ.get('GITHUB_SHA','local-source'),
  'stdout_tail':cp.stdout[-2000:],
  'boundary':'One completed shard is not a census. Candidate absence in one shard is not a no-go; every candidate still requires independent certification.'}
 result['shard_sha256']=sha({k:v for k,v in result.items() if k!='shard_sha256'})
 path=DATA/f'PART_BT3217_M36_NORMALIZED_SHARD_{index:03d}.json';path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'shard':index,'examined':examined,'candidates':len(candidate_envelopes),'sha256':result['shard_sha256']},sort_keys=True))

def aggregate(pattern):
 p=load_plan();files=sorted(DATA.glob(pattern));assert len(files)==256
 by={}
 for path in files:
  row=json.loads(path.read_text());idx=int(row['shard_index'])
  assert idx not in by and row['shard_count']==256 and row['plan_sha256']==p['plan_sha256']
  assert sha({k:v for k,v in row.items() if k!='shard_sha256'})==row['shard_sha256']
  by[idx]=row
 assert sorted(by)==list(range(256))
 engines=sorted({row['engine_sha256'] for row in by.values()});assert len(engines)==1
 coverage_known=all(isinstance(row.get('examined_count'),int) for row in by.values())
 examined=sum(row['examined_count'] for row in by.values()) if coverage_known else None
 coverage_exact=coverage_known and examined==EXPECTED
 candidates=[c for i in range(256) for c in by[i]['candidates']]
 if coverage_exact and not candidates:status='COMPLETE_ZERO_CANDIDATE_CENSUS'
 elif coverage_exact:status='COMPLETE_CENSUS_CANDIDATES_REQUIRE_CERTIFICATION'
 else:status='ALL_SHARDS_PRESENT_COVERAGE_NOT_CERTIFIED'
 result={'schema':'w33.pass3217.m36_aggregate.v1','status':status,'shard_count':256,
  'plan_sha256':p['plan_sha256'],'engine_sha256':engines[0],'coverage_known':coverage_known,
  'examined_subspaces':examined,'expected_isotropic_subspaces':EXPECTED,'coverage_exact':coverage_exact,
  'candidate_count':len(candidates),'candidates':candidates,
  'zero_candidate_no_go_under_frozen_engine':bool(coverage_exact and not candidates),
  'independent_certification_complete':False,
  'boundary':'A complete zero-candidate result is scoped only to the frozen Pass-3125 engine and requires exact coverage. Candidate existence is not authorization; independent projector/monotone certification remains mandatory.'}
 result['aggregate_sha256']=sha({k:v for k,v in result.items() if k!='aggregate_sha256'})
 path=DATA/'PART_BT3217_M36_CENSUS_AGGREGATE.json';path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':status,'examined':examined,'candidates':len(candidates)},sort_keys=True))

def selftest():
 plan();p=load_plan();assert len(p['mapping'])==32
 flat=sorted(i for values in p['mapping'].values() for i in values)
 assert flat==list(range(256)) and all(len(v)==8 for v in p['mapping'].values())
 print(json.dumps({'status':'PASS_M36_PLAN_256','sha256':p['plan_sha256']},sort_keys=True))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=('plan','selftest','shard','aggregate'),required=True)
 ap.add_argument('--shard-index',type=int,default=0);ap.add_argument('--shard-count',type=int,default=256)
 ap.add_argument('--pattern',default='PART_BT3217_M36_NORMALIZED_SHARD_*.json');a=ap.parse_args()
 DATA.mkdir(exist_ok=True)
 if a.mode=='plan':plan()
 elif a.mode=='selftest':selftest()
 elif a.mode=='shard':run_shard(a.shard_index,a.shard_count)
 else:aggregate(a.pattern)
if __name__=='__main__':main()
