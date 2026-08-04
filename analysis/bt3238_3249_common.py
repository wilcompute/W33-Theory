#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, itertools, json, math
import numpy as np
import sympy as sp

def json_default(o):
    if isinstance(o,np.bool_): return bool(o)
    if isinstance(o,np.integer): return int(o)
    if isinstance(o,np.floating): return float(o)
    if o is sp.true: return True
    if o is sp.false: return False
    if isinstance(o,sp.Integer): return int(o)
    if isinstance(o,sp.Rational): return str(o)
    if isinstance(o,sp.Basic): return str(o)
    raise TypeError(type(o).__name__)

def semantic_hash(data):
    body=dict(data); body.pop("sha256_without_hash_field",None)
    return hashlib.sha256(json.dumps(body,sort_keys=True,separators=(",",":"),default=json_default).encode()).hexdigest()

def cells_of(h,blocks):
    out=[]; by=[]
    for block in blocks:
        local=h[np.ix_(block,block)]
        comp=np.ones((12,12),dtype=np.int8)-np.eye(12,dtype=np.int8)-local
        unseen=set(range(12)); cc=[]
        while unseen:
            s=min(unseen); unseen.remove(s); q=[s]; part={s}
            while q:
                x=q.pop()
                for y in list(unseen):
                    if comp[x,y]:
                        unseen.remove(y); part.add(y); q.append(y)
            cc.append(sorted(block[x] for x in part))
        cc.sort(); assert tuple(sorted(map(len,cc)))==(4,4,4)
        by.append(cc); out.extend(cc)
    return out,by

def compose(p,q):
    return tuple(p[q[i]] for i in range(len(q)))

def perm_order(p):
    seen=[False]*len(p); ans=1
    for i in range(len(p)):
        if seen[i]: continue
        j=i; n=0
        while not seen[j]:
            seen[j]=True; j=p[j]; n+=1
        ans=math.lcm(ans,n)
    return ans

def psp_group(point_generators):
    identity=tuple(range(40)); group=[identity]; index={identity:0}
    parent=[None]; used=[None]; q=collections.deque([0])
    while q:
        gi=q.popleft(); g=group[gi]
        for si,s in enumerate(point_generators):
            z=compose(s,g)
            if z not in index:
                index[z]=len(group); group.append(z); parent.append(gi); used.append(si); q.append(len(group)-1)
    assert len(group)==25920
    def word(gi):
        out=[]
        while gi:
            out.append(used[gi]); gi=parent[gi]
        return list(reversed(out))
    return group,word

def switch_family(m,h,cover):
    pos={v:i for i,v in enumerate(cover)}
    owner={}
    for v in cover:
        for e in np.where(m[v])[0]:
            assert int(e) not in owner
            owner[int(e)]=pos[v]
    assert len(owner)==240
    mult=collections.defaultdict(list)
    for v in range(540):
        if v in pos: continue
        sig=tuple(sorted(owner[int(e)] for e in np.where(m[v])[0]))
        assert len(sig)==4 and len(set(sig))==4
        mult[sig].append(v)
    loci=[]
    for sig,vs in sorted(mult.items()):
        if len(vs)!=8: continue
        parts=[tuple(c) for c in itertools.combinations(vs,4)
               if all(not h[u,w] for u,w in itertools.combinations(c,2))]
        assert len(parts)==2
        owners=tuple(cover[i] for i in sig)
        loci.append({"owner_indices":list(sig),"owner_frames":list(owners),
                     "outside_frames":list(vs),"parts":[list(x) for x in parts]})
    assert collections.Counter(map(len,mult.values()))==collections.Counter({1:440,8:5})
    assert len(loci)==5 and len(set().union(*(set(x["owner_frames"]) for x in loci)))==20
    family=[]; coords=[]
    for choice in itertools.product(range(3),repeat=5):
        new=set(cover)
        for i,ch in enumerate(choice):
            if ch:
                new-=set(loci[i]["owner_frames"]); new|=set(loci[i]["parts"][ch-1])
        t=tuple(sorted(new))
        assert len(t)==60 and all(not h[u,v] for u,v in itertools.combinations(t,2))
        assert len({int(e) for v in t for e in np.where(m[v])[0]})==240
        coords.append(choice); family.append(t)
    assert len(set(family))==243
    return loci,coords,family

def frame_permutations(group,points,lines,frames):
    lidx={line:i for i,line in enumerate(lines)}
    fidx={frame:i for i,frame in enumerate(frames)}
    fp=np.empty((len(group),540),dtype=np.uint16)
    for gi,p in enumerate(group):
        lp=[lidx[tuple(sorted(p[x] for x in line))] for line in lines]
        fp[gi]=[fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames]
    return fp
