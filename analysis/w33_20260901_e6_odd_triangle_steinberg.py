#!/usr/bin/env python3
"""Geometrize the dark Steinberg 81 using the complementary E6 triangles.

The cubic/double-six graph H36 has 1200 triangles split by the invariant E6
switching parity into 1080 even and 120 odd triangles.  The 1080 even triangles
are explicitly the obstruction/C4 carrier: each C4 lies in three Schlaefli
K3,3s, those are three H36 edges, and those edges form its even triangle.

This script builds the three most intrinsic even<->odd incidence relations,
classified by intersection size 0,1,2 of the H36 vertex triples.  Their Gram
operators on the 1080 even carrier are pulled through the exact obstruction
crosswalk into the 59-orbital algebra and projected onto the Steinberg M3 block.
We then test exactly whether any relation selects P, R, Q, or the new dark S.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import sympy as sp

from w33_pass4992_4999_common import build_base
from w33_20260901_steinberg_frame_common import build, proportional_scalar
from w33_20260831_c5_wedderburn_kernel import mulvec

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_E6_ODD_TRIANGLE_STEINBERG.json'


def main():
    F=build(); b=build_base()
    q4=F['q4'];K33=F['K33'];kof=F['kof'];phi=F['phi'];q0=F['q0']
    rel,T,E,left=F['rel'],F['T'],F['E'],F['left_matrix']
    P,R,S,Q=F['Pvec'],F['Rvec'],F['Svec'],F['Qvec']
    frame=[P,R,S]; frame_names=['P','R','S']; frameM=[left(v) for v in frame]

    # Every H36 edge is exactly one of the 360 induced Schlaefli K3,3s: the
    # intersection of its two double-sixes is the six-line K3,3 support.
    DS,E36,ei,H36=b['DS'],b['E'],b['ei'],b['H36']
    edge_of_k={frozenset(DS[a]&DS[c]):e for e,(a,c) in enumerate(E36)}
    assert len(edge_of_k)==360 and set(edge_of_k)==set(K33)

    even=[]
    for i,C in enumerate(q4):
        es=[edge_of_k[K33[k]] for k in sorted(kof[i])]
        assert len(es)==3
        V=frozenset(x for e in es for x in E36[e]); assert len(V)==3
        assert all(H36.has_edge(*e) for e in __import__('itertools').combinations(V,2))
        assert sum(int(b['sigma'][e]) for e in es)%2==0
        even.append(V)
    assert len(even)==1080 and len(set(even))==1080

    odd=[]
    for tri in b['triangles']:
        es=[ei[tuple(sorted(e))] for e in __import__('itertools').combinations(tri,2)]
        if sum(int(b['sigma'][e]) for e in es)%2:odd.append(frozenset(tri))
    assert len(odd)==120 and set(odd)==set(map(frozenset,b['steiner']))

    results={}
    for s in (0,1,2):
        sets=[frozenset(j for j,U in enumerate(odd) if len(V&U)==s) for V in even]
        rowdeg=Counter(map(len,sets)); assert len(rowdeg)==1
        # Gram row in obstruction coordinates via phi: A_s A_s^T.
        base=sets[q0]
        row=[len(base & sets[phi[j]]) for j in range(1080)]
        oval=[None]*59
        for j,v in enumerate(row):
            r=int(rel[0,j])
            if oval[r] is None:oval[r]=v
            else:assert oval[r]==v
        assert all(v is not None for v in oval)
        Gvec=sp.Matrix(oval)
        GE=mulvec(E,Gvec,T); GM=left(GE)
        reg_rank=int(GM.rank()); actual_rank=27*reg_rank
        direct={name:(str(q) if (q:=proportional_scalar(GE,V)) is not None else None)
                for name,V in [('P',P),('R',R),('S',S),('Q',Q),('E',E)]}
        diagsc={}
        off={}
        for i in range(3):
            X=frameM[i]*GM*frameM[i]
            q=proportional_scalar(X,frameM[i]);diagsc[frame_names[i]]=str(q) if q is not None else None
        for i in range(3):
            for j in range(i+1,3):
                off[f'{frame_names[i]}{frame_names[j]}']=int((frameM[i]*GM*frameM[j]).rank())
                off[f'{frame_names[j]}{frame_names[i]}']=int((frameM[j]*GM*frameM[i]).rank())
        results[str(s)]={
          'evenRowDegree':next(iter(rowdeg)),
          'oddColumnDegreeHistogram':dict(Counter(sum(1 for V in even if len(V&U)==s) for U in odd)),
          'steinbergRegularCharpoly':str(sp.factor(GM.charpoly().as_expr())),
          'steinbergRegularRank':reg_rank,'steinbergActualRank':actual_rank,
          'directScalarMultipleOf':direct,'frameDiagonalSandwichScalars':diagsc,'frameOffDiagonalRanks':off,
        }

    dark_hits=[s for s,r in results.items() if r['directScalarMultipleOf']['S'] not in (None,'0')]
    out={
      'schema':'w33.20260901.e6-odd-triangle-steinberg.v1','status':'PASS',
      'carrierCrosswalk':{'evenTriangles':1080,'oddTriangles':120,'globalK33Edges':360,
                          'eachEvenTriangleFromThreeContainingK33Edges':True,
                          'oddTrianglesEqualSteiner120':True},
      'relationsByIntersectionSize':results,
      'darkProjectorDirectHits':dark_hits,
      'theorem':(
        'The 1080 obstruction carrier is explicitly identified with the E6-sign-even triangle orbit of H36. '
        'The complementary 120 sign-odd/Steiner triangles define three canonical intersection-incidence operators. '
        'Their exact Steinberg-block actions are listed, including whether any Gram is a scalar multiple of the dark rank-81 projector S.'),
      'boundary':(
        'A failure of these three coarse intersection relations to select S is a no-go only for this natural family, '
        'not for every equivariant operator from the 120-triangle permutation module.  No physical dark sector is inferred.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','darkHits':dark_hits,
                      'ranks':{s:r['steinbergActualRank'] for s,r in results.items()}},sort_keys=True))

if __name__=='__main__':main()
