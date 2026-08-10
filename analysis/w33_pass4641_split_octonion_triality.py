#!/usr/bin/env python3
"""Pass 4641 — explicit split-octonion triality on the W33-derived O+(8,2) quotient.

The proof is constructive.  It builds the protected plus-type V8 directly from W33,
puts it into a hyperbolic coordinate chart, identifies that chart with the split-octonion
Zorn norm over F2, and verifies the order-three point/left-annihilator/right-annihilator
triality on all incidences.  It does not use 135=135=135 as evidence.
"""
from __future__ import annotations
import json
from pathlib import Path
from itertools import product
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4641_SPLIT_OCTONION_TRIALITY_REGEN.json'


def cross(u,v):
    return (
        (u[1]*v[2]+u[2]*v[1])&1,
        (u[2]*v[0]+u[0]*v[2])&1,
        (u[0]*v[1]+u[1]*v[0])&1,
    )

def dot(u,v): return sum(a*b for a,b in zip(u,v))&1

def tup(m): return tuple((m>>i)&1 for i in range(8))
def mask(x): return sum((int(b)&1)<<i for i,b in enumerate(x))

def zmul(x,y):
    a,b,*r=x; u=tuple(r[:3]); v=tuple(r[3:])
    c,d,*s=y; X=tuple(s[:3]); Y=tuple(s[3:])
    vxY=cross(v,Y); uxX=cross(u,X)
    top=(a*c+dot(u,Y))&1
    bot=(b*d+dot(v,X))&1
    U=tuple((a*X[i]+d*u[i]+vxY[i])&1 for i in range(3))
    V=tuple((c*v[i]+b*Y[i]+uxX[i])&1 for i in range(3))
    return (top,bot,*U,*V)

def norm(x):
    a,b,*r=x; return (a*b+dot(tuple(r[:3]),tuple(r[3:])))&1

def idim(S,T): return (len(S&T)).bit_length()-1


def w33_v8():
    *_,Astar,_,_,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(n) for k in range(i+1,n) if Astar[i,k]]
    B9=rank_basis_int([cols[i]^cols[k] for i,k in edges]); V9=set(span(B9)); assert len(B9)==9 and j in V9
    rep=lambda x:min(int(x),int(x)^j)
    reps={rep(x) for x in V9}; assert len(reps)==256
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in reps if x and q(x)==0); assert len(singular)==135
    levels={0:{frozenset((0,))}}
    for d in range(4):
        nxt=set()
        for S in levels[d]:
            for v in singular:
                if v in S or any(polar(v,u) for u in S): continue
                T=frozenset(set(S)|{rep(u^v) for u in S})
                if len(T)==1<<(d+1) and all(q(u)==0 for u in T): nxt.add(T)
        levels[d+1]=nxt
    generators=set(levels[4]); assert len(generators)==270

    # Greedy hyperbolic basis e1,f1,...,e4,f4.
    hb=[]
    for _ in range(4):
        cand=[x for x in singular if x not in hb and all(polar(x,z)==0 for z in hb)]
        e=cand[0]
        f=next(y for y in singular if y!=e and all(polar(y,z)==0 for z in hb) and polar(e,y)==1)
        hb.extend([e,f])
    assert len(rank_basis_int(hb))==8
    coord_to_v={0:0}
    for c in range(256):
        x=0
        for i,b in enumerate(hb):
            if (c>>i)&1: x^=b
        coord_to_v[c]=rep(x)
        cq=tup(c); qcanon=(cq[0]*cq[1]+cq[2]*cq[3]+cq[4]*cq[5]+cq[6]*cq[7])&1
        assert q(coord_to_v[c])==qcanon
    return coord_to_v,generators


def main():
    elems=[tup(m) for m in range(256)]; zero=(0,)*8
    # Exhaustive composition-algebra law.
    checks=0
    for x in elems:
        nx=norm(x)
        for y in elems:
            assert norm(zmul(x,y))==(nx*norm(y))&1
            checks+=1
    singular=[x for x in elems if x!=zero and norm(x)==0]; assert len(singular)==135
    L={}; R={}
    for x in singular:
        la=frozenset(mask(y) for y in elems if zmul(x,y)==zero)
        ra=frozenset(mask(y) for y in elems if zmul(y,x)==zero)
        assert len(la)==len(ra)==16
        assert all(norm(tup(y))==0 for y in la|ra)
        L[mask(x)]=la; R[mask(x)]=ra
    assert len(set(L.values()))==len(set(R.values()))==135
    assert len(set(L.values())|set(R.values()))==270

    coord_to_v,wgens=w33_v8()
    Lw={frozenset(coord_to_v[c] for c in S) for S in L.values()}
    Rw={frozenset(coord_to_v[c] for c in S) for S in R.values()}
    assert Lw|Rw==wgens and len(Lw)==len(Rw)==135 and not (Lw&Rw)

    # Exhaustively verify the type cycle P(x)->L(x)->R(x)->P(x).
    fail_pa=fail_pb=fail_ab=0; edges_pa=edges_pb=edges_ab=0
    keys=sorted(L)
    for xi in keys:
        for yj in keys:
            pa = xi in L[yj]
            mapped_pa = idim(L[xi],R[yj])==3
            fail_pa += pa!=mapped_pa; edges_pa += pa
            pb = xi in R[yj]
            mapped_pb = yj in L[xi]
            fail_pb += pb!=mapped_pb; edges_pb += pb
            ab = idim(L[xi],R[yj])==3
            mapped_ab = yj in R[xi]
            fail_ab += ab!=mapped_ab; edges_ab += ab
    assert (fail_pa,fail_pb,fail_ab)==(0,0,0)
    assert (edges_pa,edges_pb,edges_ab)==(2025,2025,2025)

    out={
      'pass':4641,
      'norm_multiplicative_pairs':checks,
      'singular_points':135,
      'left_annihilators':135,
      'right_annihilators':135,
      'annihilator_size':16,
      'maximal_singular_spaces_exhausted':270,
      'w33_transport_matches_all_270_generators':True,
      'triality_order':3,
      'incidence_failures':[fail_pa,fail_pb,fail_ab],
      'cross_edges':[edges_pa,edges_pb,edges_ab],
      'theorem':'Split-octonion left/right annihilators give an explicit order-three D4 triality on the W33-derived plus-type V8.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
