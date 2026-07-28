from __future__ import annotations
from collections import deque, Counter
from functools import lru_cache
from itertools import combinations, product
import math
import numpy as np


def e8_roots():
    roots=[]
    for i,j in combinations(range(8),2):
        for si in (-2,2):
            for sj in (-2,2):
                v=[0]*8; v[i]=si; v[j]=sj; roots.append(tuple(v))
    for signs in product((-1,1), repeat=8):
        if sum(s==-1 for s in signs)%2==0:
            roots.append(tuple(signs))
    assert len(roots)==len(set(roots))==240
    return tuple(roots)

def dot(a,b): return sum(x*y for x,y in zip(a,b))

@lru_cache(None)
def base_data():
    roots=e8_roots(); idx={r:i for i,r in enumerate(roots)}
    chosen=None
    for i,a in enumerate(roots):
        for j in range(i+1,len(roots)):
            b=roots[j]
            if dot(a,b)!=-4: continue
            c=tuple(-x-y for x,y in zip(a,b))
            if c in idx:
                chosen=tuple(sorted((i,j,idx[c]))); break
        if chosen is not None: break
    assert chosen is not None
    a2=[roots[i] for i in chosen]
    orth=[i for i,r in enumerate(roots) if all(dot(r,a)==0 for a in a2)]
    assert len(orth)==72
    def d(i,j): return dot(roots[i],roots[j])
    adjacent={i:[j for j in orth if d(i,j)==-4] for i in orth}
    simple=None
    for center in orth:
        for leaf,left,right in combinations(adjacent[center],3):
            if any(d(x,y)!=0 for x,y in combinations((leaf,left,right),2)): continue
            for left_end in adjacent[left]:
                if left_end==center or any(d(left_end,x)!=0 for x in (center,leaf,right)): continue
                for right_end in adjacent[right]:
                    if right_end in (center,leaf,left,left_end): continue
                    if any(d(right_end,x)!=0 for x in (center,leaf,left,left_end)): continue
                    simple=(left_end,left,leaf,center,right,right_end); break
                if simple is not None: break
            if simple is not None: break
        if simple is not None: break
    assert simple is not None
    return {'roots':roots,'root_index':idx,'a2_triple':chosen,'e6_root_indices':tuple(orth),'e6_simple_indices':simple}

def reflection_permutation(root_index):
    data=base_data(); roots=data['roots']; idx=data['root_index']; r=np.asarray(roots[root_index],dtype=np.int16)
    out=np.empty(240,dtype=np.uint8)
    for i,v in enumerate(roots):
        vv=np.asarray(v,dtype=np.int16); coeff=int(vv.dot(r)//4); image=tuple((vv-coeff*r).tolist()); out[i]=idx[image]
    return out

def compose(a,b): return a[b]
def inverse(p):
    q=np.empty_like(p); q[p]=np.arange(len(p),dtype=p.dtype); return q

@lru_cache(None)
def e6_generators(): return tuple(reflection_permutation(i) for i in base_data()['e6_simple_indices'])


def enumerate_group(gens):
    gens=tuple(gens); I=np.arange(len(gens[0]),dtype=gens[0].dtype)
    seen={I.tobytes()}; els=[I]; q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x); k=y.tobytes()
            if k not in seen: seen.add(k); els.append(y); q.append(y)
    return tuple(els)

@lru_cache(None)
def we6_group():
    G=enumerate_group(e6_generators()); assert len(G)==51840; return G

@lru_cache(None)
def a2_triples():
    roots=base_data()['roots']; idx=base_data()['root_index']; triples=set()
    for i,a in enumerate(roots):
        for j in range(i+1,len(roots)):
            b=roots[j]
            if dot(a,b)!=-4: continue
            c=tuple(-x-y for x,y in zip(a,b)); triples.add(tuple(sorted((i,j,idx[c]))))
    assert len(triples)==2240
    return tuple(sorted(triples))

@lru_cache(None)
def a2_generator_actions():
    triples=a2_triples(); idx={t:i for i,t in enumerate(triples)}; acts=[]
    for g in e6_generators():
        acts.append(np.array([idx[tuple(sorted(int(g[x]) for x in t))] for t in triples],dtype=np.int16))
    return tuple(acts)

def orbit_partition(actions,degree):
    unseen=set(range(degree)); out=[]
    for seed in range(degree):
        if seed not in unseen: continue
        orb={seed}; q=deque([seed])
        while q:
            x=q.popleft()
            for g in actions:
                y=int(g[x])
                if y not in orb: orb.add(y); q.append(y)
        unseen-=orb; out.append(tuple(sorted(orb)))
    return tuple(sorted(out,key=lambda x:(len(x),x[0])))

@lru_cache(None)
def a2_orbits():
    o=orbit_partition(a2_generator_actions(),2240)
    assert [len(x) for x in o]==[1,1,27,27,27,27,27,27,240,270,270,432,432,432]
    return o

def induced_triple_action(root_perm):
    triples=a2_triples(); idx={t:i for i,t in enumerate(triples)}
    return np.array([idx[tuple(sorted(int(root_perm[x]) for x in t))] for t in triples],dtype=np.int16)

def permutation_order(p):
    seen=np.zeros(len(p),bool); o=1
    for i in range(len(p)):
        if seen[i]: continue
        j=i;l=0
        while not seen[j]: seen[j]=True;j=int(p[j]);l+=1
        o=math.lcm(o,l)
    return o

def generated_subgroup(gens):
    return enumerate_group(tuple(gens))

def greedy_generators(group):
    group=tuple(group); selected=[]; cur=(np.arange(len(group[0]),dtype=group[0].dtype),); keys={cur[0].tobytes()}
    for x in group:
        if x.tobytes() in keys: continue
        selected.append(x); cur=generated_subgroup(selected); keys={y.tobytes() for y in cur}
        if len(cur)==len(group): break
    return tuple(selected)

@lru_cache(None)
def cubic_supports():
    data=base_data(); roots=data['roots']; a2=[np.asarray(roots[i],dtype=int) for i in data['a2_triple']]
    shells={}
    for i,r in enumerate(roots): shells.setdefault(tuple(dot(r,x) for x in a2),[]).append(i)
    patterns=sorted(p for p,s in shells.items() if len(s)==27); assert len(patterns)==6
    shell=shells[patterns[-1]]; sums={}
    for triple in combinations(shell,3):
        total=tuple(sum(roots[i][k] for i in triple) for k in range(8)); sums.setdefault(total,[]).append(tuple(sorted(triple)))
    constant,supports=max(sums.items(),key=lambda kv:len(kv[1])); assert len(supports)==45
    return tuple(sorted(supports))
