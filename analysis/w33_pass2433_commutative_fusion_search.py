#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, importlib.util, itertools, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'

def load_common():
    s=importlib.util.spec_from_file_location('w33_common',COMMON)
    m=importlib.util.module_from_spec(s); assert s.loader; s.loader.exec_module(m); return m

def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))

def actions():
    D=load_common().build_geometry(); ident=tuple(range(40)); seen={ident:tuple(range(540))}; q=collections.deque([ident])
    while q:
        pp=q.popleft(); fp=seen[pp]
        for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
            np_=compose(gp,pp)
            if np_ not in seen:
                seen[np_]=tuple(gf[fp[i]] for i in range(540)); q.append(np_)
    assert len(seen)==51840
    return list(seen.values())

def orbitals(group):
    rel=np.full((540,540),-1,dtype=np.int16); reps=[]
    for a in range(540):
        for b in range(540):
            if rel[a,b]>=0: continue
            orb={(p[a],p[b]) for p in group}; r=len(reps)
            for x,y in orb: rel[x,y]=r
            reps.append((a,b))
    assert len(reps)==22
    return rel,reps

def structure(rel,reps):
    r=len(reps); P=np.zeros((r,r,r),dtype=np.int64)
    for k,(a,b) in enumerate(reps):
        for x in range(540): P[int(rel[a,x]),int(rel[x,b]),k]+=1
    val=[int(np.sum(rel[a]==k)) for k,(a,b) in enumerate(reps)]
    tr=[int(rel[b,a]) for a,b in reps]
    return P,val,tr

def canon(blocks): return tuple(sorted((tuple(sorted(b)) for b in blocks),key=lambda b:(0 if 0 in b else 1,b)))

def refine(P,blocks):
    blocks=[tuple(sorted(b)) for b in blocks if b]
    while True:
        sigs=[]
        for k in range(P.shape[0]):
            sig=[]
            for A in blocks:
                for B in blocks:
                    sig.append(int(P[np.ix_(A,B,[k])].sum()))
            sigs.append(tuple(sig))
        nb=[]
        for C in blocks:
            groups=collections.defaultdict(list)
            for k in C: groups[sigs[k]].append(k)
            nb.extend(tuple(v) for _,v in sorted(groups.items(),key=lambda kv:(kv[0],kv[1])))
        nb=list(canon(nb))
        if canon(blocks)==canon(nb): return canon(nb)
        blocks=nb

def is_commutative(P,blocks):
    for A in blocks:
        for B in blocks:
            for k in range(P.shape[2]):
                if int(P[np.ix_(A,B,[k])].sum()) != int(P[np.ix_(B,A,[k])].sum()): return False
    return True

def fusion_constants(P,blocks):
    out=[]
    for a,A in enumerate(blocks):
        for b,B in enumerate(blocks):
            vals=[]
            for C in blocks:
                z={int(P[np.ix_(A,B,[k])].sum()) for k in C}; assert len(z)==1; vals.append(next(iter(z)))
            out.append((a,b,vals))
    return out

def main():
    rel,reps=orbitals(actions()); P,val,tr=structure(rel,reps)
    assert tr[0]==0 and val[0]==1
    unseen=set(range(1,22)); torbits=[]
    while unseen:
        i=min(unseen); o=tuple(sorted({i,tr[i]})); torbits.append(o); unseen-=set(o)
    m=len(torbits)
    closures={}; seeds=0
    # Binary symmetric seeds, modulo complement by forcing transpose-orbit 0 selected.
    for mask in range(1,1<<m):
        if not (mask&1): continue
        selected=set().union(*(set(torbits[i]) for i in range(m) if mask>>i&1))
        rest=set(range(1,22))-selected
        if not rest: continue
        c=refine(P,[{0},selected,rest]); seeds+=1
        closures.setdefault(c,0); closures[c]+=1
    comm=[]
    for blocks,count in closures.items():
        if not is_commutative(P,blocks): continue
        fc=fusion_constants(P,blocks)
        h=hashlib.sha256(json.dumps(fc,separators=(',',':')).encode()).hexdigest()
        comm.append({'rank':len(blocks),'blocks':[list(x) for x in blocks],
                     'valencies':[sum(val[i] for i in x) for x in blocks],
                     'seed_count':count,'constants_sha256':h})
    comm.sort(key=lambda z:(z['rank'],z['blocks']))
    out={'pgsp_rank':22,'transpose_orbits':[list(x) for x in torbits],
         'transpose_orbit_count':m,'binary_seeds_tested':seeds,
         'distinct_coherent_closures':len(closures),
         'commutative_fusions':comm,
         'commutative_rank_distribution':dict(sorted(collections.Counter(z['rank'] for z in comm).items())),
         'nontrivial_min_rank':min((z['rank'] for z in comm if z['rank']>2),default=None)}
    out['sha256_without_hash_field']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__': main()
