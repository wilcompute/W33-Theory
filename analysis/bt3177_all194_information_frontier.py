#!/usr/bin/env python3
"""Pass 3177: exact frame-local information frontier for all 194 larger universal ISAs."""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3177_ALL194_INFORMATION_FRONTIER_results.json'
LIN={'F_p':((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)),'F_f':((1,0,0,0),(0,1,0,0),(0,0,0,2),(0,0,1,0)),'S_p':((1,0,0,0),(1,1,0,0),(0,0,1,0),(0,0,0,1)),'S_f':((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1,1)),'CX_pf':((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1)),'CX_fp':((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,2,0,1))}
I=np.eye(4,dtype=np.int8);NAMES=list(LIN)+[f'Z{i}' for i in range(4)]
M={k:np.array(v,dtype=np.int8) for k,v in LIN.items()};T={k:np.zeros(4,dtype=np.int8) for k in LIN}
for i in range(4):M[f'Z{i}']=I.copy();v=np.zeros(4,dtype=np.int8);v[i]=1;T[f'Z{i}']=v
OPS={n:(2 if n.startswith('CX') else 1) for n in NAMES};V=np.array(list(itertools.product(range(3),repeat=4)),dtype=np.int8);VID={tuple(map(int,v)):i for i,v in enumerate(V)}
def key(a):return bytes((a%3).astype(np.uint8).ravel())
def closure(names):
    gens=[M[n] for n in names];seen={key(I)};arr=[I.copy()];q=deque([I.copy()])
    while q:
        a=q.popleft()
        for g in gens:
            b=(a@g)%3;k=key(b)
            if k not in seen:seen.add(k);arr.append(b);q.append(b)
    return arr
def rank_stream(vecs):
    basis=[];piv=[]
    for vv in vecs:
        v=np.array(vv,dtype=np.int8)%3
        for b,p in zip(basis,piv):
            if v[p]:v=(v-v[p]*b)%3
        nz=np.flatnonzero(v)
        if nz.size:
            p=int(nz[0]);v=(v*(1 if v[p]==1 else 2))%3
            for i,b in enumerate(basis):
                if b[p]:basis[i]=(b-b[p]*v)%3
            j=sum(x<p for x in piv);piv.insert(j,p);basis.insert(j,v)
            if len(basis)==4:return 4
    return len(basis)
def dominates(a,b):
    ge=a['average']>=b['average']-1e-12 and a['minimum']>=b['minimum']-1e-12 and a['normalized']>=b['normalized']-1e-12
    le=a['variance']<=b['variance']+1e-12 and a['collision_probability']<=b['collision_probability']+1e-12 and a['decoder_units']<=b['decoder_units']
    strict=(a['average']>b['average']+1e-12 or a['minimum']>b['minimum']+1e-12 or a['normalized']>b['normalized']+1e-12 or a['variance']<b['variance']-1e-12 or a['collision_probability']<b['collision_probability']-1e-12 or a['decoder_units']<b['decoder_units'])
    return ge and le and strict
def main():
    cache={}
    for r in range(7):
        for s in itertools.combinations(LIN,r):cache[frozenset(s)]=closure(s)
    rows=[]
    for size in (5,6):
        for sub in itertools.combinations(NAMES,size):
            c=cache[frozenset(n for n in sub if n in LIN)]
            if len(c)!=51840:continue
            ts=[T[n] for n in sub if n.startswith('Z')]
            if rank_stream((a@t)%3 for a in c for t in ts)!=4:continue
            ent=[];coll=0
            for i,x in enumerate(V):
                dst=[];seen=set()
                for n in sub:
                    j=VID[tuple(map(int,(M[n]@x+T[n])%3))];dst.append(j)
                    if j==i or j in seen:coll+=1
                    seen.add(j)
                counts=Counter(dst);ps=[v/size for v in counts.values()];ent.append(-sum(p*math.log2(p) for p in ps))
            avg=float(np.mean(ent));rows.append({'generators':list(sub),'size':size,'average':avg,'minimum':min(ent),'maximum':max(ent),'variance':float(np.var(ent)),'normalized':avg/math.log2(size),'collision_probability':coll/(81*size),'decoder_units':sum(OPS[n] for n in sub)})
    assert len(rows)==194 and sum(r['size']==5 for r in rows)==80
    front=[r for r in rows if not any(dominates(s,r) for s in rows)];assert len(front)==8
    defs={'maximum_average':('average',max),'maximum_minimum':('minimum',max),'maximum_normalized':('normalized',max),'minimum_variance':('variance',min),'minimum_collision':('collision_probability',min)};extrema={}
    for label,(field,fn) in defs.items():
        value=fn(r[field] for r in rows);extrema[label]={'value':value,'attainers':sum(abs(r[field]-value)<1e-12 for r in rows)}
    out={'schema':'w33.pass3177.all194_information_frontier.v1','universal_designs':len(rows),'by_size':{'5':80,'6':114},'pareto_count':len(front),'pareto':front,'extrema':extrema,'all_rows':rows,'boundary':'Exact for uniform frame and opcode averaging. It is a control-channel metric, not physical bitrate or energy.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'universal_designs':len(rows),'pareto_count':len(front),'extrema':extrema},sort_keys=True))
if __name__=='__main__':main()
