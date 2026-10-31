#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from typing import Any
EXPECTED_SHARDS=495;EXPECTED_TOTAL=213_648_435
COUNT_KEYS=('subspaces_examined','distinct_general_subspaces_examined','rank4_isotropic_subspaces_in_shard','isotropic_subspaces','examined','count')
CANDIDATE_KEYS=('candidate_rows','candidates','hits','collinearity_projectors')
def walk_count(v:Any):
 if isinstance(v,dict):
  for k in COUNT_KEYS:
   x=v.get(k)
   if isinstance(x,int) and x>=0:return x
  for x in v.values():
   y=walk_count(x)
   if y is not None:return y
 return None
def walk_candidates(v:Any):
 if isinstance(v,dict):
  for k in CANDIDATE_KEYS:
   x=v.get(k)
   if isinstance(x,list):return x
  for x in v.values():
   y=walk_candidates(x)
   if y:return y
 return []
def log_count(p):
 text=p.read_text(errors='replace')
 for pat in (r'(?:subspaces_examined|examined|subspaces|count)\s*[=:]\s*(\d+)',r'PASS[^\n]*?\b(\d+)\s+(?:subspaces|isotropic)'):
  m=re.findall(pat,text,re.I)
  if m:return int(m[-1])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();rows=[];cands=[];missing=[];unparsed=[]
 for i in range(EXPECTED_SHARDS):
  js=sorted(a.root.rglob(f'shard_{i}.json'));logs=sorted(a.root.rglob(f'shard_{i}.log'));count=None;src=None;cc=[]
  if js:src=js[0];payload=json.loads(src.read_text());count=walk_count(payload);cc=walk_candidates(payload)
  elif logs:src=logs[0];count=log_count(src)
  else:missing.append(i);continue
  if count is None:unparsed.append(i);continue
  rows.append({'pivot_index':i,'subspaces_examined':count,'candidate_count':len(cc),'source':str(src.relative_to(a.root))})
  cands.extend(({'pivot_index':i,**x} if isinstance(x,dict) else {'pivot_index':i,'candidate':x}) for x in cc)
 total=sum(x['subspaces_examined'] for x in rows);complete=len(rows)==495 and not missing and not unparsed and total==EXPECTED_TOTAL
 out={'schema':'w33.pass3003.general_isotropic_m36_full.v1','status':'COMPLETE_EXHAUSTIVE' if complete else 'INCOMPLETE_FAIL_CLOSED','expected_shards':495,'parsed_shards':len(rows),'missing_shards':missing,'unparsed_shards':unparsed,'expected_subspaces':EXPECTED_TOTAL,'examined_subspaces':total,'candidate_count':len(cands),'candidate_rows':cands,'shard_rows':rows,'claim_boundary':'Complete only when all 495 duplicate-free RREF pivot shards parse and sum exactly to 213648435.'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'],len(rows),total,len(cands))
 if not complete:raise SystemExit(1)
if __name__=='__main__':main()
