#!/usr/bin/env python3
"""Resolve the 60-dimensional common colour row space against all seven sectors.

The previous audit proved dim(row M+ intersect row M-)=60.  A first follow-up
correctly tested the distinguished left 60-sector, but its final assertion
incorrectly assumed that diagonal sector intersections had to add to the whole
common space.  That is precisely what can fail when equivalent irreducibles
sit in different spectral sectors.

This version keeps the direct containment test, computes every 7x7 transported
sector intersection, and records the result as either an equality theorem or a
no-go.  No diagonal-additivity assumption is made.
"""
from __future__ import annotations
import itertools, json
from collections import deque
from pathlib import Path
import numpy as np
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
    sector_meta=[(-58,15),(-22,15),(-18,81),(8,20),(14,60),(62,24),(170,1)]
    projectors=lagrange_projector_numerators(Csep,roots)

    images_plus=[]; images_minus=[]
    for lam,d in sector_meta:
        Qs,Ds=projectors[lam]
        assert int(np.trace(Qs))==d*Ds
        Xp=Mp.T@Qs; Xm=Mm.T@Qs
        assert rank_mod(Xp,P)==d and rank_mod(Xm,P)==d
        images_plus.append(Xp); images_minus.append(Xm)

    rMinus=rank_mod(Mm.T,P); rPlus=rank_mod(Mp.T,P)
    assert rMinus==rPlus==216
    stack_rank=rank_mod(np.column_stack([Mp.T,Mm.T]),P)
    common_dim=216+216-stack_rank
    assert common_dim==60

    # Direct test of the distinguished 60-sector.
    s60=4
    Xp60=images_plus[s60]; Xm60=images_minus[s60]
    int_pm=60+216-rank_mod(np.column_stack([Mm.T,Xp60]),P)
    int_mp=60+216-rank_mod(np.column_stack([Mp.T,Xm60]),P)
    equals60=bool(int_pm==60 and int_mp==60)

    # Full transported-sector overlap matrix.  Off-diagonal entries are allowed
    # and are the expected signature when equivalent irreducibles occupy
    # different symmetric spectral sectors.
    cross=[]
    for i,(li,di) in enumerate(sector_meta):
        row=[]
        for j,(lj,dj) in enumerate(sector_meta):
            join=rank_mod(np.column_stack([images_plus[i],images_minus[j]]),P)
            inter=di+dj-join
            row.append(int(inter))
        cross.append(row)

    diagonal=[cross[i][i] for i in range(7)]
    offdiag=[
        {'plusSector':sector_meta[i][0],'minusSector':sector_meta[j][0],'dimension':cross[i][j]}
        for i in range(7) for j in range(7) if i!=j and cross[i][j]
    ]

    out={
      'schema':'w33.20260831.common-colour-60-sector-test.v2','status':'PASS',
      'commonColourRowSpaceDimension':common_dim,
      'sectorOrder':[{'separatorEigenvalue':l,'dimension':d} for l,d in sector_meta],
      'crossSectorIntersectionMatrix':cross,
      'diagonalSectorIntersectionDimensions':diagonal,
      'nonzeroOffDiagonalIntersections':offdiag,
      'Mplus60ImageIntersectionWithRowMminus':int_pm,
      'Mminus60ImageIntersectionWithRowMplus':int_mp,
      'equalsTransported60Sector':equals60,
      'reading':('The common colour row space is exactly the transported 60-sector.' if equals60 else
                 'The dimension-60 coincidence is not an equality; the full 7x7 matrix records the actual cross-sector intertwining pattern.'),
      'boundary':'This is an exact modular-rank certificate at a generic prime, with all source projectors integral and independently rank-certified.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','common':common_dim,'equals60':equals60,'direct':[int_pm,int_mp],
                      'diag':diagonal,'offdiag':offdiag},sort_keys=True))
if __name__=='__main__': main()
