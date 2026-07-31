#!/usr/bin/env python3
"""Exact structure of the order-432 selector stabilizer."""
from __future__ import annotations
import collections, hashlib, itertools, json, math, random
import numpy as np


def analyze(g):
    H=sorted(g['H']); n=120; identity=tuple(range(n))
    def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
    def inv(p):
        r=[0]*len(p)
        for i,j in enumerate(p): r[j]=i
        return tuple(r)
    def order(p):
        seen=[False]*len(p); out=1
        for i in range(len(p)):
            if not seen[i]:
                j=i; length=0
                while not seen[j]: seen[j]=True; length+=1; j=p[j]
                out=math.lcm(out,length)
        return out
    def comm(a,b): return compose(compose(compose(inv(a),inv(b)),a),b)
    def closure(gens):
        seen={identity}; queue=collections.deque([identity])
        while queue:
            x=queue.popleft()
            for a in gens:
                y=compose(a,x)
                if y not in seen: seen.add(y); queue.append(y)
        return seen

    orders=collections.Counter(order(h) for h in H)
    center=[h for h in H if all(compose(h,k)==compose(k,h) for k in H)]
    gens=[]; generated={identity}
    for h in H:
        if h not in generated:
            gens.append(h); generated=closure(gens)
        if len(generated)==len(H): break
    derived=closure([comm(a,b) for a in gens for b in gens])
    second=closure([comm(a,b) for a in derived for b in derived])
    normal3={h for h in H if order(h) in (1,3,9,27)}
    assert len(normal3)==27 and all(compose(a,b) in normal3 for a in normal3 for b in normal3)
    ncenter=[x for x in normal3 if all(compose(x,y)==compose(y,x) for y in normal3)]
    nderived=closure([comm(a,b) for a in normal3 for b in normal3])
    assert len(ncenter)==27 and len(nderived)==1

    unseen=set(H); cosets=[]
    while unseen:
        h=next(iter(unseen)); c={compose(h,x) for x in normal3}; cosets.append(c); unseen-=c
    cid={x:i for i,c in enumerate(cosets) for x in c}; qid=cid[identity]
    reps=[next(iter(c)) for c in cosets]
    qmul=[[cid[compose(a,b)] for b in reps] for a in reps]
    qinv=[next(b for b in range(16) if qmul[a][b]==qmul[b][a]==qid) for a in range(16)]
    def qcomm(a,b): return qmul[qmul[qmul[qinv[a]][qinv[b]]][a]][b]
    def qclosure(gs):
        seen={qid}; queue=collections.deque([qid])
        while queue:
            x=queue.popleft()
            for a in gs:
                y=qmul[a][x]
                if y not in seen: seen.add(y); queue.append(y)
        return seen
    qorders=[]
    for a in range(16):
        x=qid; k=0
        while True:
            k+=1; x=qmul[x][a]
            if x==qid: break
        qorders.append(k)
    qcenter=[a for a in range(16) if all(qmul[a][b]==qmul[b][a] for b in range(16))]
    qderived=qclosure([qcomm(a,b) for a in range(16) for b in range(16)])

    two_elements=[h for h in H if order(h) in (1,2,4,8,16) and h!=identity]
    complement=None
    rng=random.Random(1371)
    for _ in range(5000):
        c=closure(rng.sample(two_elements,3))
        if len(c)==16 and c & normal3 == {identity}: complement=c; break
    if complement is None:
        for a,b in itertools.combinations(two_elements,2):
            c=closure([a,b])
            if len(c)==16 and c & normal3 == {identity}: complement=c; break
    assert complement is not None

    ng=[]; generated={identity}
    for x in normal3:
        if x not in generated:
            ng.append(x); generated=closure(ng)
        if len(generated)==27: break
    assert len(ng)==3
    vec_to_elem={}; elem_to_vec={}
    for v in itertools.product(range(3),repeat=3):
        x=identity
        for exponent,basis in zip(v,ng):
            for _ in range(exponent): x=compose(basis,x)
        vec_to_elem[v]=x; elem_to_vec[x]=v
    matrices=[]
    for c in complement:
        ci=inv(c); cols=[]
        for b in ng: cols.append(elem_to_vec[compose(compose(c,b),ci)])
        matrices.append(np.array(cols,dtype=int).T%3)
    image={tuple(m.reshape(-1)) for m in matrices}; assert len(image)==16
    def canon(v):
        for x in v:
            if x%3:
                iv=1 if x%3==1 else 2
                return tuple((iv*y)%3 for y in v)
        raise ValueError
    lines=sorted({canon(v) for v in itertools.product(range(3),repeat=3) if any(v)})
    invariant_lines=[v for v in lines if all(canon(tuple((m@np.array(v))%3))==v for m in matrices)]
    invariant_planes=[]
    for cov in lines:
        plane={v for v in itertools.product(range(3),repeat=3) if sum(cov[i]*v[i] for i in range(3))%3==0}
        if all({tuple((m@np.array(v))%3) for v in plane}==plane for m in matrices): invariant_planes.append(cov)
    assert len(invariant_lines)==len(invariant_planes)==1

    result={
        'order':432,'element_orders':dict(sorted(orders.items())),'center_order':len(center),
        'derived_order':len(derived),'second_derived_order':len(second),
        'normal_3_subgroup_order':len(normal3),'normal_3_center_order':len(ncenter),
        'normal_3_derived_order':len(nderived),'normal_3_type':'elementary abelian C3^3',
        'quotient_order':16,'quotient_element_orders':dict(sorted(collections.Counter(qorders).items())),
        'quotient_center_order':len(qcenter),'quotient_derived_order':len(qderived),'quotient_type':'D8 x C2',
        'split_complement':True,'complement_action_image_order':len(image),
        'action_invariant_line_count':1,'action_invariant_plane_count':1,
        'action_decomposition':'1 + 2 over F3',
        'semidirect_product':'C3^3 : (D8 x C2), faithful 1+2 action over F3',
    }
    raw=json.dumps(result,sort_keys=True,separators=(',',':')); result['sha256']=hashlib.sha256(raw.encode()).hexdigest()
    return result
