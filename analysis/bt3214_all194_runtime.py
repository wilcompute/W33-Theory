#!/usr/bin/env python3
"""Pass 3214: proof-carrying exact BFS for all 194 universal larger ISAs.

The frozen ten-opcode affine library has 194 universal five/six-opcode subsets.
This engine creates one canonical plan, performs exact directed BFS on all
4,199,040 elements of ASp(4,3), and aggregates only a complete, plan-bound set
of records.  Frame information is recomputed exactly from destination
multiplicities; it is never substituted for full-group runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
LIN={
 'F_p':((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)),
 'F_f':((1,0,0,0),(0,1,0,0),(0,0,0,2),(0,0,1,0)),
 'S_p':((1,0,0,0),(1,1,0,0),(0,0,1,0),(0,0,0,1)),
 'S_f':((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1,1)),
 'CX_pf':((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1)),
 'CX_fp':((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,2,0,1))}
I4=np.eye(4,dtype=np.int8)
NAMES=list(LIN)+[f'Z{i}' for i in range(4)]
MATS={k:np.array(v,dtype=np.int8) for k,v in LIN.items()}
TRANS={k:np.zeros(4,dtype=np.int8) for k in LIN}
for i in range(4):
 MATS[f'Z{i}']=I4.copy();v=np.zeros(4,dtype=np.int8);v[i]=1;TRANS[f'Z{i}']=v
OPS={'F_p':1,'F_f':1,'S_p':1,'S_f':1,'CX_pf':2,'CX_fp':2,
     'Z0':1,'Z1':1,'Z2':1,'Z3':1}
VECS=np.array(list(itertools.product(range(3),repeat=4)),dtype=np.int8)
VID={tuple(map(int,v)):i for i,v in enumerate(VECS)}

def canonical_bytes(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
def sha(obj):return hashlib.sha256(canonical_bytes(obj)).hexdigest()
def key(a):return tuple(map(int,a.reshape(-1)))
def mm(a,b):return (a@b)%3

def linear_closure(names):
 gens=[MATS[n] for n in names if n in LIN]
 seen={key(I4):0};arr=[I4.copy()];q=deque([0])
 while q:
  a=arr[q.popleft()]
  for g in gens:
   b=mm(a,g);k=key(b)
   if k not in seen:seen[k]=len(arr);arr.append(b);q.append(len(arr)-1)
 return seen,arr

def rank3(vectors):
 a=[list(map(int,v)) for v in vectors];r=0
 for c in range(4):
  p=next((i for i in range(r,len(a)) if a[i][c]%3),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];inv=1 if a[r][c]%3==1 else 2
  a[r]=[(inv*x)%3 for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    f=a[i][c]%3;a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[r])]
  r+=1
 return r

def entropy(row):
 n=len(row);counts=Counter(map(int,row))
 return -sum((c/n)*math.log2(c/n) for c in counts.values())

def subset_metrics(sub,closure):
 dest=np.empty((81,len(sub)),dtype=np.int16);collisions=0
 for gi,n in enumerate(sub):
  ys=(VECS@MATS[n].T+TRANS[n])%3
  dest[:,gi]=[VID[tuple(map(int,y))] for y in ys]
 for i,row in enumerate(dest):
  seen=set()
  for j in row:
   if int(j)==i or int(j) in seen:collisions+=1
   seen.add(int(j))
 dist=np.full(81,-1,dtype=np.int16);dist[0]=0;q=deque([0])
 while q:
  i=q.popleft()
  for j in dest[i]:
   if dist[j]<0:dist[j]=dist[i]+1;q.append(int(j))
 translations=[TRANS[n] for n in sub if n.startswith('Z')]
 orbit=[(a@t)%3 for a in closure for t in translations]
 infos=[entropy(row) for row in dest]
 return {'collisions':collisions,'collision_probability':collisions/(81*len(sub)),
  'frame_diameter':int(dist.max()) if np.all(dist>=0) else None,
  'frame_mean_distance':float(dist.mean()) if np.all(dist>=0) else None,
  'translation_span_rank':rank3(orbit) if orbit else 0,
  'decoder_operation_units':sum(OPS[n] for n in sub),
  'information_average':float(np.mean(infos)),'information_minimum':float(min(infos)),
  'information_maximum':float(max(infos)),
  'information_normalized':float(np.mean(infos)/math.log2(len(sub)))}

def universal_rows():
 cache={}
 for r in range(7):
  for s in itertools.combinations(LIN,r):cache[frozenset(s)]=linear_closure(s)
 rows=[]
 for size in (5,6):
  for sub in itertools.combinations(NAMES,size):
   index,arr=cache[frozenset(n for n in sub if n in LIN)]
   metrics=subset_metrics(sub,arr)
   if len(index)==51840 and metrics['translation_span_rank']==4:
    rows.append(dict(metrics,generators=list(sub),size=size,linear_order=len(index)))
 rows.sort(key=lambda r:(r['size'],r['generators']))
 assert len(rows)==194
 return rows

def vcode(v):return int(v[0]+3*v[1]+9*v[2]+27*v[3])

def full_tables():
 seen,group=linear_closure(LIN);g=np.stack(group).astype(np.int8)
 assert len(seen)==51840
 nxt={n:np.array([seen[key(x)] for x in (g@MATS[n])%3],dtype=np.int32) for n in LIN}
 vec=np.array([[c%3,(c//3)%3,(c//9)%3,(c//27)%3] for c in range(81)],dtype=np.int8)
 add=np.empty((81,81),dtype=np.uint8)
 for a in range(81):add[a]=[vcode((vec[a]+vec[b])%3) for b in range(81)]
 shift={}
 for i in range(4):
  e=np.zeros(4,dtype=np.int8);e[i]=1
  shift[f'Z{i}']=np.array([vcode(x) for x in (g@e)%3],dtype=np.uint8)
 return nxt,add,shift

def full_bfs(sub,tables):
 nxt,add,shift=tables;n=51840*81
 visited=np.zeros(n,dtype=np.bool_);visited[0]=1;front=np.array([0],dtype=np.int32)
 growth=[1];total=0;depth=0
 while front.size:
  li=front//81;ti=front-li*81;parts=[]
  for name in sub:
   if name in LIN:next_states=nxt[name][li]*81+ti
   else:next_states=li*81+add[ti,shift[name][li]]
   parts.append(next_states.astype(np.int32,copy=False))
  candidates=np.unique(np.concatenate(parts));new=candidates[~visited[candidates]]
  if not new.size:break
  depth+=1;visited[new]=1;growth.append(int(new.size));total+=depth*int(new.size);front=new
 reached=int(visited.sum())
 assert sum(growth)==reached
 return {'group_order_reached':reached,'diameter':depth,'mean_distance':total/reached,
         'growth_series':growth,'growth_sha256':sha(growth)}

def write_plan(shards):
 rows=universal_rows()
 body={'library':NAMES,'universal_count':194,'shard_count':shards,
       'rows':[dict(row,global_index=i,shard=i%shards) for i,row in enumerate(rows)]}
 digest=sha(body)
 payload={'schema':'w33.pass3214.isa_plan.v1','status':'EXACT_PLAN','plan_sha256':digest,**body,
          'boundary':'Plan and frame information are exact; no full-group optimum exists until all shards aggregate.'}
 path=DATA/'PART_BT3214_ISA_PLAN.json';path.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'universal':194,'shards':shards,'plan_sha256':digest},sort_keys=True))

def load_plan(count):
 path=DATA/'PART_BT3214_ISA_PLAN.json'
 if not path.exists():raise FileNotFoundError('generate canonical plan first')
 plan=json.loads(path.read_text());assert plan['universal_count']==194 and plan['shard_count']==count
 body={k:plan[k] for k in ('library','universal_count','shard_count','rows')}
 assert sha(body)==plan['plan_sha256']
 return plan

def run_shard(index,count):
 plan=load_plan(count);selected=[r for r in plan['rows'] if int(r['shard'])==index]
 tables=full_tables();records=[]
 for raw in selected:
  row={k:v for k,v in raw.items() if k!='shard'}
  full=full_bfs(tuple(row['generators']),tables)
  record={**row,'full_group':full,'plan_sha256':plan['plan_sha256']}
  record['record_sha256']=sha({k:v for k,v in record.items() if k!='record_sha256'})
  records.append(record)
 payload={'schema':'w33.pass3214.isa_shard.v1','shard_index':index,'shard_count':count,
          'plan_sha256':plan['plan_sha256'],'record_count':len(records),'records':records}
 payload['shard_sha256']=sha({k:v for k,v in payload.items() if k!='shard_sha256'})
 path=DATA/f'PART_BT3214_ISA_SHARD_{index:03d}.json';path.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'shard':index,'records':len(records),'sha256':payload['shard_sha256']},sort_keys=True))

def dominates(a,b):
 weak=(a['full_group']['mean_distance']<=b['full_group']['mean_distance']+1e-12 and
       a['full_group']['diameter']<=b['full_group']['diameter'] and
       a['collision_probability']<=b['collision_probability']+1e-15 and
       a['decoder_operation_units']<=b['decoder_operation_units'] and
       a['information_average']>=b['information_average']-1e-12 and
       a['information_minimum']>=b['information_minimum']-1e-12)
 strict=(a['full_group']['mean_distance']<b['full_group']['mean_distance']-1e-12 or
         a['full_group']['diameter']<b['full_group']['diameter'] or
         a['collision_probability']<b['collision_probability']-1e-15 or
         a['decoder_operation_units']<b['decoder_operation_units'] or
         a['information_average']>b['information_average']+1e-12 or
         a['information_minimum']>b['information_minimum']+1e-12)
 return weak and strict

def aggregate(pattern,count):
 plan=load_plan(count);files=sorted(DATA.glob(pattern));assert len(files)==count
 shards={};records=[]
 for path in files:
  payload=json.loads(path.read_text());idx=int(payload['shard_index'])
  assert idx not in shards and payload['shard_count']==count and payload['plan_sha256']==plan['plan_sha256']
  assert sha({k:v for k,v in payload.items() if k!='shard_sha256'})==payload['shard_sha256']
  shards[idx]=payload
  for record in payload['records']:
   assert record['plan_sha256']==plan['plan_sha256']
   assert sha({k:v for k,v in record.items() if k!='record_sha256'})==record['record_sha256']
   assert record['full_group']['group_order_reached']==4199040
   assert sum(record['full_group']['growth_series'])==4199040
   records.append(record)
 assert sorted(shards)==list(range(count)) and len(records)==194
 by={int(r['global_index']):r for r in records};assert sorted(by)==list(range(194))
 rows=[by[i] for i in range(194)]
 frontier=[r for r in rows if not any(dominates(o,r) for o in rows)]
 best_runtime=min(rows,key=lambda r:(r['full_group']['mean_distance'],r['full_group']['diameter'],r['generators']))
 best_collision=min(rows,key=lambda r:(r['collision_probability'],r['full_group']['mean_distance'],r['generators']))
 best_info=max(rows,key=lambda r:(r['information_average'],r['information_minimum'],-r['collision_probability']))
 body={'schema':'w33.pass3214.isa_aggregate.v1','status':'COMPLETE_194_FULL_AFFINE_BFS',
       'plan_sha256':plan['plan_sha256'],'shard_count':count,'record_count':194,
       'global_runtime_optimum':best_runtime,'global_collision_optimum':best_collision,
       'global_information_optimum':best_info,'joint_pareto_count':len(frontier),
       'joint_pareto':frontier,'records':rows,
       'boundary':'Exact for the frozen ten-opcode library. Physical decoder area, timing, energy and calibration remain separate observed gates.'}
 body['aggregate_sha256']=sha({k:v for k,v in body.items() if k!='aggregate_sha256'})
 path=DATA/'PART_BT3214_ISA_FULL_BFS_AGGREGATE.json';path.write_text(json.dumps(body,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'records':194,'frontier':len(frontier),'runtime_best':best_runtime['generators'],'mean':best_runtime['full_group']['mean_distance']},sort_keys=True))

def selftest(shards):
 write_plan(shards);plan=load_plan(shards)
 assert sum(1 for r in plan['rows'] if r['size']==5)==80
 assert sum(1 for r in plan['rows'] if r['size']==6)==114
 assert min(r['collisions'] for r in plan['rows'] if r['size']==5)==45
 assert min(r['collisions'] for r in plan['rows'] if r['size']==6)==63
 print(json.dumps({'status':'PASS_PLAN_194','sha256':plan['plan_sha256']},sort_keys=True))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=('plan','selftest','shard','aggregate'),required=True)
 ap.add_argument('--shard-index',type=int,default=0);ap.add_argument('--shard-count',type=int,default=32)
 ap.add_argument('--pattern',default='PART_BT3214_ISA_SHARD_*.json');a=ap.parse_args()
 DATA.mkdir(exist_ok=True)
 if a.mode=='plan':write_plan(a.shard_count)
 elif a.mode=='selftest':selftest(a.shard_count)
 elif a.mode=='shard':run_shard(a.shard_index,a.shard_count)
 else:aggregate(a.pattern,a.shard_count)
if __name__=='__main__':main()
