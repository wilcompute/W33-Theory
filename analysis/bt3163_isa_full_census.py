#!/usr/bin/env python3
"""Pass 3163: sharded exact full-affine BFS for all universal 5/6-opcode ISAs.

This is the completion layer for Pass 3153/3154.  It reuses the same frozen ten-opcode
library, exact universality criterion, and 4,199,040-state semidirect-product BFS, but makes
the exhaustive gate resumable and aggregation-safe.  No global optimum is promoted unless
all 194 records are present and every reached order is exactly 4,199,040.
"""
from __future__ import annotations
import argparse, itertools, json
from collections import deque
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
    MATS[f'Z{i}']=I4.copy(); v=np.zeros(4,dtype=np.int8); v[i]=1; TRANS[f'Z{i}']=v
OPS={'F_p':1,'F_f':1,'S_p':1,'S_f':1,'CX_pf':2,'CX_fp':2,
     'Z0':1,'Z1':1,'Z2':1,'Z3':1}
VECS=np.array(list(itertools.product(range(3),repeat=4)),dtype=np.int8)
VID={tuple(map(int,v)):i for i,v in enumerate(VECS)}

def key(A): return tuple(map(int,A.reshape(-1)))
def mm(A,B): return (A@B)%3

def linear_closure(names):
    gens=[MATS[n] for n in names if n in LIN]
    seen={key(I4):0}; arr=[I4.copy()]; q=deque([0])
    while q:
        A=arr[q.popleft()]
        for G in gens:
            B=mm(A,G); k=key(B)
            if k not in seen:
                seen[k]=len(arr); arr.append(B); q.append(len(arr)-1)
    return seen,arr

def rank3(vectors):
    a=[list(map(int,v)) for v in vectors]; r=0
    for c in range(4):
        p=next((i for i in range(r,len(a)) if a[i][c]%3),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]; inv=1 if a[r][c]%3==1 else 2
        a[r]=[(inv*x)%3 for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                f=a[i][c]%3; a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[r])]
        r+=1
    return r

def subset_metrics(sub,closure):
    dest=np.empty((81,len(sub)),dtype=np.int16); collisions=0
    for gi,n in enumerate(sub):
        ys=(VECS@MATS[n].T+TRANS[n])%3
        dest[:,gi]=[VID[tuple(map(int,y))] for y in ys]
    for i,row in enumerate(dest):
        seen=set()
        for j in row:
            if int(j)==i or int(j) in seen: collisions+=1
            seen.add(int(j))
    dist=np.full(81,-1,dtype=np.int16); dist[0]=0; q=deque([0])
    while q:
        i=q.popleft()
        for j in dest[i]:
            if dist[j]<0: dist[j]=dist[i]+1; q.append(int(j))
    translations=[TRANS[n] for n in sub if n.startswith('Z')]
    orbit=[]
    for A in closure:
        for t in translations: orbit.append((A@t)%3)
    return {
      'collisions':collisions,
      'collision_probability':collisions/(81*len(sub)),
      'frame_diameter':int(dist.max()) if np.all(dist>=0) else None,
      'frame_mean_distance':float(dist.mean()) if np.all(dist>=0) else None,
      'translation_span_rank':rank3(orbit) if orbit else 0,
      'decoder_operation_units':sum(OPS[n] for n in sub)}

def universal_rows():
    cache={}
    for r in range(7):
        for s in itertools.combinations(LIN,r): cache[frozenset(s)]=linear_closure(s)
    rows=[]
    for size in (5,6):
        for sub in itertools.combinations(NAMES,size):
            idx,arr=cache[frozenset(n for n in sub if n in LIN)]
            m=subset_metrics(sub,arr)
            if len(idx)==51840 and m['translation_span_rank']==4:
                rows.append(dict(m,generators=list(sub),size=size,linear_order=len(idx)))
    rows.sort(key=lambda r:(r['size'],r['generators']))
    assert len(rows)==194
    return rows

def vcode(v): return int(v[0]+3*v[1]+9*v[2]+27*v[3])

def full_tables():
    seen,group=linear_closure(LIN); G=np.stack(group).astype(np.int8)
    nxt={n:np.array([seen[key(x)] for x in (G@MATS[n])%3],dtype=np.int32) for n in LIN}
    vec=np.array([[c%3,(c//3)%3,(c//9)%3,(c//27)%3] for c in range(81)],dtype=np.int8)
    add=np.empty((81,81),dtype=np.uint8)
    for a in range(81): add[a]=[vcode((vec[a]+vec[b])%3) for b in range(81)]
    shift={}
    for i in range(4):
        e=np.zeros(4,dtype=np.int8); e[i]=1
        shift[f'Z{i}']=np.array([vcode(x) for x in (G@e)%3],dtype=np.uint8)
    return nxt,add,shift

def full_bfs(sub,tables):
    nxt,add,shift=tables; N=51840*81
    vis=np.zeros(N,dtype=np.bool_); vis[0]=1; front=np.array([0],dtype=np.int32)
    growth=[1]; total=0; depth=0
    while front.size:
        li=front//81; ti=front-li*81; parts=[]
        for n in sub:
            if n in LIN: ns=nxt[n][li]*81+ti
            else: ns=li*81+add[ti,shift[n][li]]
            parts.append(ns.astype(np.int32,copy=False))
        cand=np.unique(np.concatenate(parts)); new=cand[~vis[cand]]
        if not new.size: break
        depth+=1; vis[new]=1; growth.append(int(new.size)); total+=depth*int(new.size); front=new
    return {'group_order_reached':int(vis.sum()),'diameter':depth,
            'mean_distance':total/int(vis.sum()),'growth_series':growth}

def write_plan(shards):
    rows=universal_rows()
    plan={'schema':'w33.pass3163.isa_shard_plan.v1','universal_count':len(rows),
          'shard_count':shards,'rows':[dict(r,global_index=i,shard=i%shards) for i,r in enumerate(rows)]}
    p=DATA/'PART_BT3163_ISA_SHARD_PLAN.json'; p.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'universal_count':len(rows),'shard_count':shards},sort_keys=True))

def run_shard(index,count):
    plan_path=DATA/'PART_BT3163_ISA_SHARD_PLAN.json'
    if not plan_path.exists(): raise FileNotFoundError('run --mode plan once and distribute the plan artifact')
    plan=json.loads(plan_path.read_text()); rows=[{k:v for k,v in r.items() if k not in ('global_index','shard')} for r in plan['rows']]
    assert len(rows)==194 and int(plan['shard_count'])==count
    selected=[(i,r) for i,r in enumerate(rows) if i%count==index]
    tables=full_tables(); out=[]
    for i,r in selected:
        f=full_bfs(tuple(r['generators']),tables)
        out.append(dict(r,global_index=i,full_group=f))
    payload={'schema':'w33.pass3163.isa_full_bfs_shard.v1','shard_index':index,'shard_count':count,
             'records':out,'record_count':len(out)}
    p=DATA/f'PART_BT3163_ISA_FULL_BFS_SHARD_{index:03d}.json'
    p.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'shard':index,'records':len(out)},sort_keys=True))

def aggregate(pattern):
    files=sorted(DATA.glob(pattern)); records=[]
    for p in files:
        d=json.loads(p.read_text()); records.extend(d['records'])
    by={r['global_index']:r for r in records}
    assert len(by)==194 and sorted(by)==list(range(194))
    rows=[by[i] for i in range(194)]
    assert all(r['full_group']['group_order_reached']==4199040 for r in rows)
    best=min(rows,key=lambda r:(r['full_group']['mean_distance'],r['collision_probability'],r['generators']))
    lowcoll=min(rows,key=lambda r:(r['collision_probability'],r['full_group']['mean_distance']))
    payload={'schema':'w33.pass3163.isa_full_bfs_aggregate.v1','status':'COMPLETE_194_FULL_BFS',
             'record_count':194,'global_mean_distance_optimum':best,
             'global_collision_probability_optimum':lowcoll,'records':rows,
             'boundary':'Exact for the frozen ten-opcode library; physical decoder cost remains a separate placement gate.'}
    p=DATA/'PART_BT3163_ISA_FULL_BFS_AGGREGATE.json'; p.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'record_count':194,'best':best['generators'],'mean':best['full_group']['mean_distance']},sort_keys=True))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=('plan','shard','aggregate'),required=True)
    ap.add_argument('--shard-index',type=int,default=0); ap.add_argument('--shard-count',type=int,default=32)
    ap.add_argument('--pattern',default='PART_BT3163_ISA_FULL_BFS_SHARD_*.json'); a=ap.parse_args()
    if a.mode=='plan': write_plan(a.shard_count)
    elif a.mode=='shard': run_shard(a.shard_index,a.shard_count)
    else: aggregate(a.pattern)
if __name__=='__main__': main()
