#!/usr/bin/env python3
"""Passes 3153-3154: exact five/six-opcode affine ISA census.

The ten frozen generators split into six zero-translation symplectic maps and four
pure translations.  Universality is therefore certified exactly by

    |<linear parts>| = 51,840 and dim span(<linear parts> translations) = 4.

All 462 five- and six-generator subsets receive exact universality, collision,
81-frame distance, and spectral metrics.  Full 4,199,040-state BFS is run for every
non-dominated design by default and for all universal designs with --exhaustive-full.
"""
from __future__ import annotations
import argparse, itertools, json, math
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3153_BT3154_LARGER_ISA_CENSUS_results.json'
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

def key(A):return tuple(map(int,A.reshape(-1)))
def mm(A,B):return (A@B)%3

def linear_closure(names):
    gens=[MATS[n] for n in names if n in LIN]
    seen={key(I4):0};arr=[I4.copy()];q=deque([0])
    while q:
        A=arr[q.popleft()]
        for G in gens:
            B=mm(A,G);k=key(B)
            if k not in seen:seen[k]=len(arr);arr.append(B);q.append(len(arr)-1)
    return seen,arr

def rank3(vectors):
    a=[list(map(int,v)) for v in vectors];r=0
    for c in range(4):
        p=next((i for i in range(r,len(a)) if a[i][c]%3),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];inv=1 if a[r][c]%3==1 else 2
        a[r]=[(inv*x)%3 for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]%3:
                f=a[i][c]%3;a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[r])]
        r+=1
    return r

def subset_metrics(sub,closure):
    dest=np.empty((81,len(sub)),dtype=np.int16);coll=0
    for gi,n in enumerate(sub):
        ys=(VECS@MATS[n].T+TRANS[n])%3
        dest[:,gi]=[VID[tuple(map(int,y))] for y in ys]
    for i,row in enumerate(dest):
        seen=set()
        for j in row:
            if int(j)==i or int(j) in seen:coll+=1
            seen.add(int(j))
    dist=np.full(81,-1,dtype=np.int16);dist[0]=0;q=deque([0])
    while q:
        i=q.popleft()
        for j in dest[i]:
            if dist[j]<0:dist[j]=dist[i]+1;q.append(int(j))
    P=np.zeros((81,81),dtype=float)
    for i in range(81):
        for j in dest[i]:P[i,j]+=1/len(sub)
    eig=np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
    sv=np.linalg.svd(P,compute_uv=False)
    translations=[TRANS[n] for n in sub if n.startswith('Z')]
    orbit=[]
    if translations:
        for A in closure:
            orbit.extend((A@t)%3 for t in translations)
    return {'collisions':coll,'collision_probability':coll/(81*len(sub)),
            'frame_diameter':int(dist.max()) if np.all(dist>=0) else None,
            'frame_mean_distance':float(dist.mean()) if np.all(dist>=0) else None,
            'slem':float(eig[1]),'sigma2':float(sv[1]),
            'translation_span_rank':rank3(orbit) if orbit else 0,
            'decoder_operation_units':sum(OPS[n] for n in sub)}

def dominates(a,b):
    ks=('collision_probability','frame_mean_distance','slem','decoder_operation_units')
    return all(a[k]<=b[k]+1e-12 for k in ks) and any(a[k]<b[k]-1e-12 for k in ks)

def vcode(v):return int(v[0]+3*v[1]+9*v[2]+27*v[3])

def full_tables():
    seen,group=linear_closure(LIN)
    G=np.stack(group).astype(np.int8)
    nxt={n:np.array([seen[key(x)] for x in (G@MATS[n])%3],dtype=np.int32) for n in LIN}
    vec=np.array([[c%3,(c//3)%3,(c//9)%3,(c//27)%3] for c in range(81)],dtype=np.int8)
    add=np.empty((81,81),dtype=np.uint8)
    for a in range(81):add[a]=[vcode((vec[a]+vec[b])%3) for b in range(81)]
    shift={}
    for i in range(4):
        e=np.zeros(4,dtype=np.int8);e[i]=1
        shift[f'Z{i}']=np.array([vcode(x) for x in (G@e)%3],dtype=np.uint8)
    return nxt,add,shift

def full_bfs(sub,tables):
    nxt,add,shift=tables;N=51840*81
    vis=np.zeros(N,dtype=np.bool_);vis[0]=1;front=np.array([0],dtype=np.int32)
    growth=[1];total=0;d=0
    while front.size:
        li=front//81;ti=front-li*81;parts=[]
        for n in sub:
            if n in LIN:ns=nxt[n][li]*81+ti
            else:ns=li*81+add[ti,shift[n][li]]
            parts.append(ns.astype(np.int32,copy=False))
        cand=np.unique(np.concatenate(parts));new=cand[~vis[cand]]
        if not new.size:break
        d+=1;vis[new]=1;growth.append(int(new.size));total+=d*int(new.size);front=new
    return {'group_order_reached':int(vis.sum()),'diameter':d,
            'mean_distance':total/int(vis.sum()),'growth_series':growth}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--exhaustive-full',action='store_true');a=ap.parse_args()
    cache={};rows=[]
    for r in range(7):
        for s in itertools.combinations(LIN,r):cache[frozenset(s)]=linear_closure(s)
    for size in (5,6):
        for sub in itertools.combinations(NAMES,size):
            lkey=frozenset(n for n in sub if n in LIN);index,arr=cache[lkey]
            m=subset_metrics(sub,arr)
            m.update({'generators':list(sub),'size':size,'linear_order':len(index)})
            m['universal']=len(index)==51840 and m['translation_span_rank']==4
            rows.append(m)
    universal=[x for x in rows if x['universal']]
    pareto=[x for x in universal if not any(dominates(y,x) for y in universal)]
    tables=full_tables();targets=universal if a.exhaustive_full else pareto
    full={'+'.join(x['generators']):full_bfs(tuple(x['generators']),tables) for x in targets}
    out={'schema':'w33.pass3153_3154.larger_isa_census.v1','subsets':len(rows),
         'universal':len(universal),'universal_by_size':{str(s):sum(x['universal'] and x['size']==s for x in rows) for s in (5,6)},
         'minimum_collisions_by_size':{str(s):min(x['collisions'] for x in universal if x['size']==s) for s in (5,6)},
         'pareto_count':len(pareto),'pareto':[dict(x,full_group=full['+'.join(x['generators'])]) for x in pareto],
         'all_rows':rows if a.exhaustive_full else None,
         'full_bfs_mode':'all universal' if a.exhaustive_full else 'non-dominated only',
         'boundary':'Exact frozen-library census. Decoder operation units and any combined physical-cost scalar are explicit design proxies, not measured energy.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
