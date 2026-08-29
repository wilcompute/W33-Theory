#!/usr/bin/env python3
"""Combine the nonsplit central-C3 circuit cover with the exact 216->dark20 map.

We decompose the 216-dimensional circuit permutation module into the deck-C3
invariant fibre-sum sector and the two-dimensional-per-fibre deck-difference
sector, then measure exactly which parts of the right dark 20-dimensional
module are reached.  This answers whether the dark20 intertwiner descends to
the 72 quotient fibres or genuinely requires the three-sheeted lift.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260829_circuit_dark_intertwiner import mm,tr,add,eye,rank_mod

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_C3_COVER_DARK20_DESCENT.json'


def cycles(p):
    seen=set(); out=[]
    for i in range(len(p)):
        if i in seen: continue
        O=[];j=i
        while j not in seen:
            seen.add(j);O.append(j);j=p[j]
        out.append(tuple(O))
    return sorted(out,key=lambda O:(len(O),O))


def orbit_partition(G,n):
    rem=set(range(n));out=[]
    while rem:
        s=min(rem);O={g[s] for g in G};out.append(tuple(sorted(O)));rem-=O
    return sorted(out,key=lambda O:(len(O),O))


def main():
    pts,idx,_,N=base.geometry();supports,masks=base.supports_from_N(N)
    A45=[[0]*45 for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):A45[i][j]=A45[j][i]=1
    Q20=mm(add(eye(45),A45,12,-1),add(A45,eye(45),1,3))
    assert rank_mod(Q20)==20

    circuits=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C:w^=masks[i]
        if w==0:circuits.append(C)
    assert len(circuits)==216
    cidx={C:i for i,C in enumerate(circuits)}
    Cmat=[[int(m in C) for m in range(45)] for C in circuits]
    T20=mm(Q20,tr(Cmat));assert rank_mod(T20)==20

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen=(18,62,77,10)
    G=base.closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(G)==25920
    K={p45 for p40,p45 in G if p40[0]==0};assert len(K)==648
    kgens=base.deterministic_generators(K,45)
    Z=[z for z in K if all(base.compose(z,g)==base.compose(g,z) for g in kgens)];assert len(Z)==3
    e45=tuple(range(45));z=next(x for x in Z if x!=e45)
    Kderived=base.derived_subgroup(K,45);assert len(Kderived)==216 and set(Z).issubset(Kderived)

    def act_circuit(i,g):return cidx[tuple(sorted(g[x] for x in circuits[i]))]
    zperm=tuple(act_circuit(i,z) for i in range(216))
    zfibres=cycles(zperm);assert len(zfibres)==72 and {len(O) for O in zfibres}=={3}
    fibre_of={x:i for i,O in enumerate(zfibres) for x in O}

    # Equivariance of the explicit integer map under the chosen deck generator.
    assert all(T20[z[m]][zperm[c]]==T20[m][c] for m in range(45) for c in range(216))

    # S embeds the 72 quotient-fibre coordinate space by equal weights on each
    # C3 orbit. D spans the two independent zero-sum differences in each fibre.
    S=[[0]*72 for _ in range(216)]
    D=[[0]*144 for _ in range(216)]
    for f,O in enumerate(zfibres):
        a,b,c=O
        for x in O:S[x][f]=1
        D[b][2*f]=1;D[a][2*f]=-1
        D[c][2*f+1]=1;D[a][2*f+1]=-1
    Tinvar=mm(T20,S);Tdiff=mm(T20,D)
    rinv=rank_mod(Tinvar);rdiff=rank_mod(Tdiff)
    assert rank_mod([Tinvar[i]+Tdiff[i] for i in range(45)])==20

    # The fixed dimension of dark20 under Z must equal the quotient-fibre image.
    z45orbits=cycles(z)
    I45=[[int(i in O) for O in z45orbits] for i in range(45)]
    fixed20=rank_mod(mm(Q20,I45));assert fixed20==rinv
    assert rinv+rdiff==20

    # Quotient K/Z action and its two intrinsic 36-fibre orbits.
    def qperm(g):return tuple(fibre_of[act_circuit(O[0],g)] for O in zfibres)
    Q={qperm(g) for g in K};assert len(Q)==216
    qorbs=orbit_partition(Q,72);assert [len(O) for O in qorbs]==[36,36]
    qrecords=[]
    for O in qorbs:
        through={sum(0 in supports[m] for m in circuits[zfibres[f][0]]) for f in O};assert len(through)==1
        cols=[[S[r][f] for f in O] for r in range(216)]
        qrecords.append({'supportsThroughDistinguishedPoint':next(iter(through)),'fibres':36,
                         'dark20RankFromFibreSums':rank_mod(mm(T20,cols))})
    qrecords.sort(key=lambda r:r['supportsThroughDistinguishedPoint'])

    out={
      'schema':'w33.20260829.c3-cover-dark20-descent.v1','status':'PASS',
      'cover':{'circuitStates':216,'deckGroup':'C3','deckFibres':72,'fibreSize':3,
               'pointStabilizerOrder':648,'quotientOrder':216,'nonsplit':True},
      'dark20':{'fullMapRank':20,'deckFixedDimension':fixed20,
                'quotientFibreSumImageRank':rinv,'deckDifferenceImageRank':rdiff,
                'ranksAddToFullDark20':rinv+rdiff==20},
      'quotient36Plus36':qrecords,
      'descent':{'fullMapDescendsTo72Fibres':rdiff==0,
                 'statement':('T20 descends completely to the 72 central fibres' if rdiff==0 else
                              'Only the deck-invariant part of T20 descends to the 72 central fibres; the remaining dark modes require sheet-resolving C3 data.')},
      'theorem':'The exact circuit-to-dark20 intertwiner admits a canonical decomposition into central-C3 fibre-sum and fibre-difference images. Their exact ranks determine the quotient-visible and genuinely three-sheeted parts.',
      'boundary':'Exact finite representation theory for the W33 circuit permutation module. This does not identify the 216 circuit states with physical one-qutrit Clifford gates or assert a calibrated optical implementation.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
