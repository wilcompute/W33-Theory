#!/usr/bin/env python3
"""Pass7717-7724: ternary code carried by the Leech dual-40 incidence shell.

Pass7709 shows that the Leech order-9 top/socle pairing projectivizes to the
symmetric 2-(40,13,4) point-hyperplane design of PG(3,3).  This verifier builds
that design from a standard symplectic pairing, row-reduces its incidence matrix
over F3, exhausts all 3^11 row-code words, and proves the dual minimum distance
by a weighted-column meet-in-the-middle search.

The abstract [40,11,13]_3 design code and optimal [40,29,6]_3 dual are known in
the coding literature.  The new repo bridge is their canonical occurrence on
the Leech top-to-socle linking-incidence object from Pass7645/7709.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7717_7724_LEECH_DUAL40_TERNARY_CODE.json'

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%3 for y in v)
    raise ValueError
def omega(a,b):return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3

def rref(M,p=3):
    X=np.asarray(M,dtype=np.int64).copy()%p;m,n=X.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(X[r:,c])
        if len(nz)==0:continue
        z=r+int(nz[0]);X[[r,z]]=X[[z,r]];X[r]=(X[r]*pow(int(X[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and X[i,c]:X[i]=(X[i]-int(X[i,c])*X[r])%p
        r+=1
        if r==m:break
    return X[:r].astype(np.int8)

def main():
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});assert len(P)==40
    N=np.array([[int(omega(x,y)==0) for y in P] for x in P],dtype=np.int8)
    assert set(map(int,N.sum(1)))=={13}
    B=rref(N,3);assert B.shape==(11,40)

    weights=Counter()
    for n in range(3**11):
        q=n;c=np.zeros(11,dtype=np.int8)
        for i in range(11):c[i]=q%3;q//=3
        w=(c.astype(np.int16)@B.astype(np.int16))%3
        weights[int(np.count_nonzero(w))]+=1
    assert sum(weights.values())==3**11 and min(k for k in weights if k)>0==13
    expected={0:1,13:80,18:1560,22:20280,24:21060,25:33696,27:18800,28:42120,30:16848,31:21840,36:780,40:82}
    assert dict(sorted(weights.items()))==expected

    cols=[tuple(int(x) for x in B[:,j]) for j in range(40)];zero=(0,)*11
    def plus(a,b):return tuple((x+y)%3 for x,y in zip(a,b))
    def neg(a):return tuple((-x)%3 for x in a)
    def syn(supp,coef):
        z=zero
        for j,c in zip(supp,coef):z=plus(z,tuple((c*x)%3 for x in cols[j]))
        return z
    states={}
    for w in (1,2,3):
        D=defaultdict(list)
        for S in itertools.combinations(range(40),w):
            for c in itertools.product((1,2),repeat=w):D[syn(S,c)].append((S,c))
        states[w]=D
        assert zero not in D
    def disjoint_match(a,b):
        for L in states[a].values():
            pass
        for s,L in states[a].items():
            for x in L:
                X=set(x[0])
                for y in states[b].get(neg(s),[]):
                    if X.isdisjoint(y[0]):return x,y
        return None
    assert disjoint_match(2,2) is None and disjoint_match(2,3) is None
    w6=disjoint_match(3,3);assert w6 is not None

    # Count all projective weight-6 dual words from 3+3 decompositions.  Each
    # nonzero ternary word has two scalar representatives, so projective count
    # 3120 means 6240 actual weight-6 codewords.
    projective=set()
    for s,L in states[3].items():
        for x in L:
            X=set(x[0])
            for y in states[3].get(neg(s),[]):
                if not X.isdisjoint(y[0]):continue
                v=[0]*40
                for j,c in zip(x[0],x[1]):v[j]=c
                for j,c in zip(y[0],y[1]):v[j]=c
                if next(t for t in v if t)==2:v=[(2*t)%3 for t in v]
                projective.add(tuple(v))
    assert len(projective)==3120

    out={
      'schema':'w33.pass7717_7724.leech_dual40_ternary_code.v1','status':'PASS','passes':'7717-7724',
      'dependency':'Pass7709 dual PG(3,3) top/socle incidence from the Leech order-9 linking pairing',
      'design':'symmetric 2-(40,13,4)','incidence_rank_F3':11,
      'row_code':{'parameters':'[40,11,13]_3','weight_enumerator':{str(k):v for k,v in expected.items()}},
      'dual_code':{'parameters':'[40,29,6]_3','weight6_words':6240,'projective_weight6_words':3120,'minimum_distance_proved_by':'no weighted column dependency of support <=5; explicit support-6 dependency'},
      'literature_prior_art':['Some optimal codes and strongly regular graphs from the linear group L4(3)','Self-orthogonal designs and codes from the symplectic groups S4(3) and S4(4)'],
      'novelty_boundary':'The abstract design/code parameters are published prior art. New here is the exact transport onto the canonical Leech top-to-socle linking-incidence shell established in Pass7645/7709.',
      'theorem':'The Leech dual-40 projective linking incidence canonically carries the ternary [40,11,13]_3 PG(3,3) design code; its orthogonal code is [40,29,6]_3 with exactly 6240 minimum-weight words.',
      'claim_boundary':'Exact finite coding consequence of the Leech dual-40 incidence theorem; no physical decoder threshold is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','row_code':'[40,11,13]_3','dual':'[40,29,6]_3','A6_dual':6240}))
if __name__=='__main__':main()
