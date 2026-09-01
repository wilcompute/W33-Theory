#!/usr/bin/env python3
"""Exact representation audit of the new 1080 = 27 x 40 obstruction carrier.

The preceding product theorem gives a PSp(4,3)-equivariant bijection between
transversal-free depth-three triples and

    completion charts (27) x W33 lines (40).

This script asks the representation-theoretic question left open there.
It rebuilds the native PSp action, proves that the diagonal product is one
transitive orbit with stabilizer H of order 24, and computes the multiplicity
of the 81-dimensional Steinberg representation by the building trace formula.

For the rank-two spherical building (the 40-point/40-line incidence graph),
Steinberg is H_1.  Hence for every g

  chi_St(g) = #fixed flags - #fixed points - #fixed lines + 1.

Frobenius reciprocity then gives

  mult_St C[G/H] = dim St^H = (1/|H|) sum_{h in H} chi_St(h).

The result is 3.  The script also resolves all constituents visible from the
rank-three 40- and 27-point actions and records the exact residual boundary;
it does not pretend that those visible sectors are the full ordinary-character
decomposition.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260901_OBSTRUCTION_PRODUCT_REPRESENTATION.json"


def parts(H, n):
    rem=set(range(n)); out=[]
    while rem:
        s=min(rem); O={g[s] for g in H}; out.append(sorted(O)); rem-=O
    return sorted(out,key=lambda O:(-len(O),O))


def order_profile(p):
    return base.porder(p)


def main():
    pts,idx,lines,N=base.geometry()
    supports,_=base.supports_from_N(N)
    assert (len(pts),len(lines),len(supports))==(40,40,45)

    # The 27 completion charts are the maximal five-cliques in packet
    # disjointness, exactly as in the new E8 completion theorem.
    adj45=[set() for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):
            adj45[i].add(j); adj45[j].add(i)
    charts=[C for C in itertools.combinations(range(45),5)
            if all(b in adj45[a] for a,b in itertools.combinations(C,2))]
    assert len(charts)==27
    cidx={frozenset(C):i for i,C in enumerate(charts)}

    # Native projective symplectic group, using the same deterministic generator
    # choice as the 2026-08-29/31 frontier packets.
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
    chosen=(18,62,77,10)
    Gpaired=base.closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen])
    assert len(Gpaired)==25920

    lidx={frozenset(L):i for i,L in enumerate(lines)}
    actions=[]
    for p40,p45 in Gpaired:
        pl=tuple(lidx[frozenset(p40[x] for x in L)] for L in lines)
        pc=tuple(cidx[frozenset(p45[x] for x in C)] for C in charts)
        actions.append((p40,pl,p45,pc))

    # Diagonal 27 x 40 product is transitive; stabilizer has order 24.
    orbit={(pc[0],pl[0]) for _p40,pl,_p45,pc in actions}
    assert len(orbit)==1080
    H=[a for a in actions if a[1][0]==0 and a[3][0]==0]
    assert len(H)==24 and 25920//24==1080

    # Exact Steinberg trace from the building chain complex.
    flags=[(p,l) for l,L in enumerate(lines) for p in L]
    def st_trace(a):
        p40,pl,_p45,_pc=a
        fp=sum(p40[p]==p for p in range(40))
        fl=sum(pl[l]==l for l in range(40))
        ff=sum(p40[p]==p and pl[l]==l for p,l in flags)
        return ff-fp-fl+1
    traces=[st_trace(a) for a in H]
    trace_hist=Counter(traces)
    assert trace_hist==Counter({81:1,9:2,0:8,-1:6,-3:7})
    st_fixed=sum(traces)//24
    assert st_fixed==3

    # Orbital rank / character norm of the 1080 permutation action.
    Hprod=[tuple(pc[c]*40+pl[l] for c in range(27) for l in range(40))
           for _p40,pl,_p45,pc in H]
    sub=parts(Hprod,1080)
    assert len(sub)==59
    subdegrees=sorted(map(len,sub),reverse=True)
    assert Counter(subdegrees)==Counter({24:35,12:18,6:2,4:2,3:1,1:1})

    # Resolve the fixed multiplicities of the irreps visible in the rank-three
    # W33-line and 27-chart modules.  Projection rank on H-orbit indicators is
    # exactly dim(V^H).
    H40=[a[1] for a in H]; H27=[a[3] for a in H]
    o40=parts(H40,40); o27=parts(H27,27)
    assert sorted(map(len,o40))==[1,3,12,12,12]
    assert sorted(map(len,o27))==[1,4,4,6,12]

    A40=np.zeros((40,40),dtype=int)
    for i,j in itertools.combinations(range(40),2):
        if set(lines[i]) & set(lines[j]): A40[i,j]=A40[j,i]=1
    A27=np.zeros((27,27),dtype=int)
    for i,j in itertools.combinations(range(27),2):
        if set(charts[i]) & set(charts[j]): A27[i,j]=A27[j,i]=1
    assert set(map(int,A40.sum(1)))=={12} and set(map(int,A27.sum(1)))=={10}

    def indicators(orbs,n):
        V=np.zeros((n,len(orbs)),dtype=int)
        for j,O in enumerate(orbs): V[O,j]=1
        return V
    V40=indicators(o40,40); V27=indicators(o27,27)
    I40=np.eye(40,dtype=int); I27=np.eye(27,dtype=int)
    # scalar multiples of the spectral projectors
    Q24=(A40-12*I40)@(A40+4*I40)   # eigenvalue +2, dimension 24
    Q15=(A40-12*I40)@(A40-2*I40)   # eigenvalue -4, dimension 15
    Q20=(A27-10*I27)@(A27+5*I27)   # eigenvalue +1, dimension 20
    Q6 =(A27-10*I27)@(A27-I27)     # eigenvalue -5, dimension 6
    rank=lambda X:int(sp.Matrix(X.tolist()).rank())
    visible={
      '1':1,
      '15_W33':rank(Q15@V40),
      '24_W33':rank(Q24@V40),
      '6_Schlafli':rank(Q6@V27),
      '20_Schlafli':rank(Q20@V27),
      '81_Steinberg':st_fixed,
    }
    assert visible=={'1':1,'15_W33':2,'24_W33':2,'6_Schlafli':1,'20_Schlafli':3,'81_Steinberg':3}
    visible_dimension=1+15*2+24*2+6*1+20*3+81*3
    visible_norm=1+2*2+2*2+1+3*3+3*3
    assert (visible_dimension,visible_norm)==(388,28)

    out={
      'schema':'w33.20260901.obstruction-product-representation.v1',
      'status':'PASS',
      'group':'PSp(4,3)',
      'groupOrder':25920,
      'carrier':{'description':'27 completion charts x 40 W33 lines','degree':1080,'transitive':True},
      'stabilizer':{
        'order':24,
        'elementOrderHistogram':dict(sorted(Counter(order_profile(a[0]) for a in H).items())),
        'subdegrees':subdegrees,
        'orbitalRank':59,
      },
      'steinberg':{
        'dimension':81,
        'traceFormula':'fixedFlags - fixedPoints - fixedLines + 1',
        'traceHistogramOnStabilizer':dict(sorted(trace_hist.items())),
        'fixedDimension':3,
        'permutationMultiplicityByFrobeniusReciprocity':3,
      },
      'visibleOrdinaryConstituents':visible,
      'visibleDimension':visible_dimension,
      'visibleCharacterNormContribution':visible_norm,
      'residual':{
        'dimension':1080-visible_dimension,
        'characterNormContribution':59-visible_norm,
        'status':'not fully decomposed in this Python witness; exact GAP character-table decomposition remains a separate refinement',
      },
      'theorem':'The natural 1080 depth-three obstruction carrier is one transitive PSp(4,3) G-set with stabilizer 24, and its permutation module contains the unique 81-dimensional Steinberg representation with multiplicity exactly three. The same stabilizer fixes 2 copies of the W33 15, 2 copies of the W33 24, 1 Schlaefli 6 and 3 Schlaefli 20s.',
      'boundary':'The three Steinberg copies are representation-theoretic constituents of C[1080]. This does not identify the previously observed incidence multiplicity 81 with a particular copy, and the 692-dimensional residual ordinary character is not silently labelled.',
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','degree':1080,'H':24,'rank':59,'steinbergMultiplicity':3,'visible':visible,'residualDimension':692},sort_keys=True))

if __name__=='__main__': main()
