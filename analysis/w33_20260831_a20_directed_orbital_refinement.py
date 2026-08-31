#!/usr/bin/env python3
"""Resolve the unsymmetrized orbital pair hidden by the symmetric A20 relation.

The all-five frontier audit shows that A30 is one C5xC5 PSp orbital whereas
A20 is a fusion of exactly two.  This audit reconstructs the two bicolour
incidence matrices and the complete 10-orbital C5 relation algebra, then reads
the exact orbital constants of M+ M-^T.  It also tests whether the resulting
directed operator commutes with the symmetric seven-sector generators.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base
from w33_20260830_sentinel_six_circuit_orbit import six_circuits
from w33_20260831_all5_frontier_audit import orbit_ids

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_A20_DIRECTED_ORBITAL_REFINEMENT.json'


def main():
    pts,idx,_lines,N=base.geometry(); supports,masks=base.supports_from_N(N)
    c5=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C: w^=masks[i]
        if w==0: c5.append(C)
    c6=six_circuits(masks)
    assert len(c5)==216 and len(c6)==540
    i5={C:i for i,C in enumerate(c5)}; i6={C:i for i,C in enumerate(c6)}

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
    assert len(O)==2160
    Mp=np.zeros_like(M)
    for z in O:
        a,b=divmod(z,540); Mp[a,b]=1
    Mm=M-Mp

    I=np.eye(216,dtype=np.int64)
    A30=Mp@Mp.T-10*I
    K=Mp@Mm.T
    assert np.array_equal(K+K.T,4*((K+K.T)//4))
    A20=(K+K.T)//4
    assert set(np.unique(A20)).issubset({0,1})

    rel55,reps55,sizes55=orbit_ids(act5,act5,216,216)
    assert len(reps55)==10
    rows=[]
    for rid,seed55 in enumerate(reps55):
        a,b=divmod(seed55,216)
        vals=np.unique(K[rel55==rid])
        assert len(vals)==1
        tr=int(rel55[b,a])
        rows.append({
            'id':rid,'size':sizes55[rid],'valency':sizes55[rid]//216,
            'transposeId':tr,'MplusMminusT':int(vals[0]),
            'A20':int(A20[a,b]),'A30':int(A30[a,b]),
        })
    a20=[r for r in rows if r['A20']==1]
    a30=[r for r in rows if r['A30']==1]
    assert len(a20)==2 and len(a30)==1
    assert a20[0]['transposeId']==a20[1]['id'] and a20[1]['transposeId']==a20[0]['id']

    comm20=K@A20-A20@K
    comm30=K@A30-A30@K
    out={
        'schema':'w33.20260831.a20-directed-orbital-refinement.v1','status':'PASS',
        'C5OrbitalRank':10,'orbitalRows':rows,
        'A20OrbitalIds':[r['id'] for r in a20],
        'A20TransposePaired':True,
        'A20Valencies':[r['valency'] for r in a20],
        'crossConstants':[r['MplusMminusT'] for r in a20],
        'A30OrbitalId':a30[0]['id'],'A30Valency':a30[0]['valency'],
        'commutators':{
            'MplusMminusT_with_A20_zero':bool(not np.any(comm20)),
            'MplusMminusT_with_A30_zero':bool(not np.any(comm30)),
            'maxAbsWithA20':int(np.max(np.abs(comm20))),
            'maxAbsWithA30':int(np.max(np.abs(comm30))),
        },
        'theorem':'The symmetric A20 relation is exactly the fusion of a transpose-paired directed PSp orbital pair.  The unsymmetrized colour-cross Gram M+M-^T has a constant integral weight on each member, exposing the orientation data erased by A20.',
        'boundary':'Directed orbital orientation is an exact finite-geometry datum; no physical chirality identification is asserted here.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','A20ids':out['A20OrbitalIds'],'A20valencies':out['A20Valencies'],'crossConstants':out['crossConstants'],'A30id':out['A30OrbitalId'],'comm20':out['commutators']['MplusMminusT_with_A20_zero'],'comm30':out['commutators']['MplusMminusT_with_A30_zero']},sort_keys=True))

if __name__=='__main__': main()
