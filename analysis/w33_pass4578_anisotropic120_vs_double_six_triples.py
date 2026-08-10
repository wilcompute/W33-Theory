#!/usr/bin/env python3
"""Pass 4578 -- reject the tempting 120=120 protected/cubic count match.

Pass4559 gives 120 anisotropic protected classes in V8=O+(8,2). The cubic carrier
has 36 double-sixes. Under PSp(4,3), unordered triples of the 36 double-sixes split
into five orbits of sizes 120,540,1080,2160,3240. The unique 120-orbit is therefore
an obvious candidate for a hidden cross-carrier identification.

This pass tests equivariance rather than cardinality. Using the same five PSp
generators on the protected V8 and cubic U6 modules, the 120 protected anisotropic
points and the 120 double-six triples are both transitive G-sets with stabilizer
order 216. Nevertheless they are not isomorphic: stabilizer suborbit signatures
are respectively

  [1,1,1,27,27,27,36]  and  [1,2,27,36,54].

A direct generator-propagation search over every possible image of one base point
finds no equivariant bijection. Thus the count match is a genuine false friend.
"""
from __future__ import annotations

import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup

import w33_pass4522_4525_4527_dual_orthogonal_schlafli as p4522
import w33_pass4576_o8plus_o6minus_quadratic_no_go as p4576

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4578_ANISOTROPIC120_DOUBLE_SIX_TRIPLES.json'


def vecint(v):return sum(int(b)<<i for i,b in enumerate(v) if b)
def intvec(x,d):return np.array([(x>>i)&1 for i in range(d)],dtype=np.uint8)

def invariant_alt(gens,d):
    pairs=[(i,j) for i in range(d) for j in range(i+1,d)];basis=[];eq=[]
    for i,j in pairs:
        F=np.zeros((d,d),dtype=np.uint8);F[i,j]=F[j,i]=1;basis.append(F)
    for g in gens:
        ds=[((g.T@F@g)%2)^F for F in basis]
        for i in range(d):
            for j in range(d):eq.append([int(D[i,j]) for D in ds])
    ns=p4522.nullspace2(np.asarray(eq,dtype=np.uint8));assert len(ns)==1
    F=np.zeros((d,d),dtype=np.uint8)
    for bit,(i,j) in zip(ns[0],pairs):F[i,j]=F[j,i]=bit
    return F


def qbase(F,x):
    z=0;d=len(x)
    for i in range(d):
        for j in range(i+1,d):z^=int(F[i,j]&x[i]&x[j])
    return z


def invariant_q(gens,F,d,expected_anis):
    good=[]
    for ellm in range(1<<d):
        ell=intvec(ellm,d);ok=True
        for g in gens:
            for xm in range(1<<d):
                x=intvec(xm,d);y=(g@x)%2
                if (qbase(F,x)^int(ell@x%2))!=(qbase(F,y)^int(ell@y%2)):ok=False;break
            if not ok:break
        if ok:good.append(ell)
    assert len(good)==1;ell=good[0]
    q=lambda m:qbase(F,intvec(m,d))^int(ell@intvec(m,d)%2)
    anis=[m for m in range(1,1<<d) if q(m)==1];assert len(anis)==expected_anis
    return q,anis


def perms_on_vectors(gens,vals,d):
    idx={m:i for i,m in enumerate(vals)};out=[]
    for g in gens:
        p=[]
        for m in vals:p.append(idx[vecint((g@intvec(m,d))%2)])
        out.append(tuple(p))
    return out


def orbit_subset(seed,perms):
    seed=tuple(sorted(seed));seen={seed};q=deque([seed])
    while q:
        x=q.popleft()
        for p in perms:
            y=tuple(sorted(p[i] for i in x))
            if y not in seen:seen.add(y);q.append(y)
    return seen


def suborbit_signature(perms,n):
    G=PermutationGroup([Permutation(list(p)) for p in perms]);assert G.order()==25920
    H=G.stabilizer(0);rem=set(range(n));out=[]
    while rem:
        x=next(iter(rem));o=set(H.orbit(x));out.append(len(o));rem-=o
    return H.order(),sorted(out)


def equivariant_bijection_exists(P,Q):
    n=len(P[0]);assert len(Q[0])==n
    for y0 in range(n):
        f={0:y0};dq=deque([0]);ok=True
        while dq and ok:
            x=dq.popleft();y=f[x]
            for p,q in zip(P,Q):
                x2=p[x];y2=q[y]
                if x2 in f:
                    if f[x2]!=y2:ok=False;break
                else:f[x2]=y2;dq.append(x2)
        if ok and len(f)==n:return True
    return False


def main()->int:
    V8=p4576.protected_v8_generators();F8=invariant_alt(V8,8);q8,anis8=invariant_q(V8,F8,8,120)
    P8=perms_on_vectors(V8,anis8,8)

    d=p4522.build_module();U6=[np.asarray(g,dtype=np.uint8) for g in d['G6']];anis6=d['anis'];assert len(anis6)==36
    P36=perms_on_vectors(U6,anis6,6)
    rem=set(itertools.combinations(range(36),3));orbs=[]
    while rem:
        s=next(iter(rem));o=orbit_subset(s,P36);orbs.append(o);rem-=o
    sizes=sorted(map(len,orbs));assert sizes==[120,540,1080,2160,3240]
    O120=sorted(next(o for o in orbs if len(o)==120));oidx={x:i for i,x in enumerate(O120)}
    PT=[]
    for p in P36:PT.append(tuple(oidx[tuple(sorted(p[i] for i in t))] for t in O120))

    h8,s8=suborbit_signature(P8,120);ht,st=suborbit_signature(PT,120)
    assert (h8,s8)==(216,[1,1,1,27,27,27,36])
    assert (ht,st)==(216,[1,2,27,36,54])
    assert not equivariant_bijection_exists(P8,PT)
    out={'pass':4578,'candidate_count_match':{'protected_anisotropic_classes':120,'unique_double_six_triple_orbit':120},
      'double_six_triple_orbit_sizes':sizes,
      'protected_Gset':{'stabilizer_order':h8,'suborbits':s8},
      'double_six_triple_Gset':{'stabilizer_order':ht,'suborbits':st},
      'equivariant_bijection':False,
      'theorem':'The unique 120-orbit of cubic double-six triples is not PSp(4,3)-equivariantly isomorphic to the 120 protected anisotropic O+(8,2) classes.',
      'boundary':'Exact negative G-set result. Equal cardinality and equal stabilizer order are insufficient for identification.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
