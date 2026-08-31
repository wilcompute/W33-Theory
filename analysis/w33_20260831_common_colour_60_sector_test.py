#!/usr/bin/env python3
"""Test whether the 60-dimensional common colour row space is the transported 60-sector.

The all-five audit proves dim(row M+ intersect row M-)=60.  The symmetric
bicolour algebra also has a distinguished joint sector of dimension 60 with
(A30,A20)=(0,2).  Equality of dimensions is not enough.  This script uses the
exact integer spectral projector and modular rank tests to measure the actual
intersection of M+^T(P_60 V) with row(M-), and conversely.
"""
from __future__ import annotations
import itertools, json
from collections import deque
from pathlib import Path
import numpy as np
import sympy as sp
import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits
from w33_20260831_all5_frontier_audit import rank_mod, lagrange_projector_numerators

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_COMMON_COLOUR_60_SECTOR_TEST.json'
P=1000003

def main():
    pts,idx,_lines,N=base.geometry(); supports,masks=base.supports_from_N(N)
    c5=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0: c5.append(C)
    c6=six_circuits(masks); i5={C:i for i,C in enumerate(c5)}; i6={C:i for i,C in enumerate(c6)}
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    gg=[gens45[i] for i in (18,62,77,10)]
    act5=[tuple(i5[tuple(sorted(g[x] for x in C))] for C in c5) for g in gg]
    act6=[tuple(i6[tuple(sorted(g[x] for x in C))] for C in c6) for g in gg]
    s5=[set(C) for C in c5]; s6=[set(C) for C in c6]
    M=np.zeros((216,540),dtype=np.int64)
    for a in range(216):
        for b in range(540):
            if len(s5[a]&s6[b])==3: M[a,b]=1
    seed=next(a*540+b for a in range(216) for b in range(540) if M[a,b])
    O={seed}; Q=deque([seed])
    while Q:
        z=Q.popleft(); a,b=divmod(z,540)
        for p5,p6 in zip(act5,act6):
            nz=p5[a]*540+p6[b]
            if nz not in O: O.add(nz); Q.append(nz)
    Mp=np.zeros_like(M)
    for z in O:
        a,b=divmod(z,540); Mp[a,b]=1
    Mm=M-Mp
    I=np.eye(216,dtype=np.int64)
    A30=Mp@Mp.T-10*I
    A20=(Mp@Mm.T+Mm@Mp.T)//4
    Csep=A30+7*A20
    roots=[-58,-22,-18,8,14,62,170]
    Q60,D60=lagrange_projector_numerators(Csep,roots)[14]
    assert int(np.trace(Q60))==60*D60
    assert rank_mod(Q60,P)==60

    Xp=Mp.T@Q60
    Xm=Mm.T@Q60
    rp=rank_mod(Xp,P); rm=rank_mod(Xm,P)
    assert rp==rm==60
    rMinus=rank_mod(Mm.T,P); rPlus=rank_mod(Mp.T,P)
    assert rMinus==rPlus==216
    join_pm=rank_mod(np.column_stack([Mm.T,Xp]),P)
    join_mp=rank_mod(np.column_stack([Mp.T,Xm]),P)
    int_pm=60+216-join_pm
    int_mp=60+216-join_mp

    # Common colour row space W has dimension 60.  Measure how much of W lies
    # in each transported joint sector image under M+^T.
    dims=[]
    sector_meta=[(-58,15),(-22,15),(-18,81),(8,20),(14,60),(62,24),(170,1)]
    projectors=lagrange_projector_numerators(Csep,roots)
    for lam,d in sector_meta:
        Qs,Ds=projectors[lam]
        X=Mp.T@Qs
        rx=rank_mod(X,P); assert rx==d
        join=rank_mod(np.column_stack([Mm.T,X]),P)
        inter=d+216-join
        dims.append({'separatorEigenvalue':lam,'sectorDimension':d,'intersectionWithOtherColourRowSpace':inter})
    assert sum(x['intersectionWithOtherColourRowSpace'] for x in dims) >= 60

    out={
      'schema':'w33.20260831.common-colour-60-sector-test.v1','status':'PASS',
      'commonColourRowSpaceDimension':60,
      'transported60SectorDimensions':[rp,rm],
      'Mplus60ImageIntersectionWithRowMminus':int_pm,
      'Mminus60ImageIntersectionWithRowMplus':int_mp,
      'sectorwiseMplusImageIntersectionsWithRowMminus':dims,
      'equalsTransported60Sector':bool(int_pm==60 and int_mp==60),
      'boundary':'Equality is asserted only if both containment tests attain dimension 60; otherwise the dimension-60 coincidence is explicitly rejected.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__': main()
