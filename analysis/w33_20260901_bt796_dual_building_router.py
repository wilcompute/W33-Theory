#!/usr/bin/env python3
"""Test one 2160 carrier as a simultaneous router for both building Steinbergs.

The exact building-homology audit proves that BT796/packet48-2160 contains
multiplicity 9 of H1(W33), degree 81, and multiplicity 5 of H1(GQ(4,2)), degree
64.  The 1080 obstruction carrier contains three copies of each.

This script reuses the complete 113-dimensional Hom_G(1080,2160) orbital basis
and projects its cross-Grams onto both central blocks.  It asks whether the
projected operators span all of End_G(81^3)=M3(Q) and End_G(64^3)=M3(Q), and,
when they do, solves exactly for all six primitive rank-81/rank-64 projectors.
"""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import sympy as sp

import w33_20260901_packet48_bt796_crossid as cross
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_double_steinberg_64_81 as dual
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_c5_wedderburn_kernel import mulvec, center_equations, generic_center

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_BT796_DUAL_BUILDING_ROUTER.json'


def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))

def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m))); G={I}; Q=deque([I])
    while Q:
        a,b=Q.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in G: G.add(z); Q.append(z)
    assert len(G)==25920
    return list(G)


def main():
    F=build_frame(); D=cross.build()
    acts,rel,reps,T,diag=F['acts'],F['rel'],F['reps'],F['T'],F['diag']
    E81=F['E']; frame81=list(F['frame']); left81=F['left_matrix']

    # Recover and split the degree-64 central isotypic block in the same 59-D
    # orbital algebra used for the 81 block.
    Z=center_equations(T).nullspace(); one=sp.zeros(59,1); one[diag]=1
    z,_L,_cp,factors,_coeff=generic_center(Z,T)
    records,idempotents=obs.central_records(z,factors,T,one,diag)
    i64=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==64)
    E64=idempotents[i64]
    split_label,split_vals,frame64,left64=dual.split_three_copies(E64,rel,reps,T,64,diag)

    slots=D['slots']; sli={x:i for i,x in enumerate(slots)}; wlines=D['wlines']
    li={frozenset(L):i for i,L in enumerate(wlines)}
    line_sets=[set(L) for L in wlines]
    import itertools
    skew=[(i,j) for i,j in itertools.combinations(range(40),2) if not (line_sets[i]&line_sets[j])]
    skidx={frozenset(x):i for i,x in enumerate(skew)}

    def line_perm(p): return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    def slot_perm(p):
        lp=line_perm(p); out=[]
        for s,t in slots:
            a,b=skew[s]
            ns=skidx[frozenset((lp[a],lp[b]))]
            out.append(sli[(ns,lp[t])])
        return tuple(out)

    target_gens=[slot_perm(p) for p in D['g40']]
    src_line=[tuple(acts[k][ell]%40 for ell in range(40)) for k in range(4)]
    assert src_line==[line_perm(p) for p in D['g40']]
    G=paired_closure(acts,target_gens,1080,2160)
    H=[z for z in G if z[0][0]==0]; assert len(H)==24

    unseen=set(range(2160)); orbits=[]
    while unseen:
        o=min(unseen); O={gt[o] for _gs,gt in H}; unseen-=O; orbits.append(sorted(O))
    orbits=sorted(orbits,key=lambda O:(len(O),O[0]))
    assert len(orbits)==113

    tr=[None]*1080
    for gs,gt in G:
        y=gs[0]
        if tr[y] is None: tr[y]=gt
    assert all(x is not None for x in tr)

    zero=sp.zeros(59,1)
    def raw_cross(i,j):
        Oi=set(orbits[i]); Oj=orbits[j]
        row=[]
        for y in range(1080):
            row.append(sum(1 for x in Oj if tr[y][x] in Oi))
        oval=[None]*59
        for y,v in enumerate(row):
            r=int(rel[0,y])
            if oval[r] is None: oval[r]=v
            else: assert oval[r]==v
        return sp.Matrix(oval)

    def project(E,V): return mulvec(E,mulvec(V,E,T),T)

    # Find independent projected cross-Grams simultaneously.  Cache raw
    # cross-operators because both blocks use the same complete orbital Hom basis.
    bases={64:sp.zeros(59,0),81:sp.zeros(59,0)}
    indep={64:[],81:[]}; ranks={64:0,81:0}; cache={}
    for i in range(len(orbits)):
        if ranks[64]==9 and ranks[81]==9: break
        for j in range(len(orbits)):
            key=(i,j)
            V=cache.setdefault(key,raw_cross(i,j))
            for deg,E in ((64,E64),(81,E81)):
                if ranks[deg]==9: continue
                X=project(E,V)
                if X==zero: continue
                C=sp.Matrix.hstack(bases[deg],X)
                r=C.rank()
                if r>ranks[deg]:
                    indep[deg].append((i,j,X)); bases[deg]=C; ranks[deg]=r
            if ranks[64]==9 and ranks[81]==9: break

    assert ranks[81]==9  # independently known from the prior 2160 scan

    solutions={}
    for deg,frame in ((64,frame64),(81,frame81)):
        if ranks[deg]!=9: continue
        B=bases[deg]
        for k,P in enumerate(frame):
            sol,_=B.gauss_jordan_solve(P); assert B*sol==P
            terms=[]
            for q,c in enumerate(sol):
                if c!=0:
                    a,b,_X=indep[deg][q]
                    terms.append({'crossOrbitPair':[a,b],'coefficient':str(sp.factor(c))})
            solutions[f'H1_{deg}_primitive_{k}']=terms

    # Rank diagnostics for the self-Grams in both blocks.
    hits={64:[],81:[]}
    for i in range(len(orbits)):
        V=raw_cross(i,i)
        for deg,E,left,actual in ((64,E64,left64,64),(81,E81,left81,81)):
            X=project(E,V); rr=left(X).rank(); assert rr%3==0
            ar=int(rr//3*actual)
            if ar: hits[deg].append([i,ar])

    out={
      'schema':'w33.20260901.bt796-dual-building-router.v1','status':'PASS',
      'groupOrder':25920,'sourceCarrier':1080,'targetCarrier':2160,
      'equivariantHomDimension':len(orbits),'sourceStabilizerOrder':24,
      'targetBuildingHomologyMultiplicities':{'H1_W33_81':9,'H1_GQ42_64':5},
      'sourceBuildingHomologyMultiplicities':{'H1_W33_81':3,'H1_GQ42_64':3},
      'H1_81':{'crossGramSpanDimension':ranks[81],'fullM3':ranks[81]==9,
               'independentCrossOrbitPairs':[[a,b] for a,b,_ in indep[81]],
               'selfGramHits':hits[81]},
      'H1_64':{'crossGramSpanDimension':ranks[64],'fullM3':ranks[64]==9,
               'independentCrossOrbitPairs':[[a,b] for a,b,_ in indep[64]],
               'selfGramHits':hits[64],
               'splitOperator':split_label,'splitEigenvalues':[str(v) for v in split_vals]},
      'exactPrimitiveProjectorExpansions':solutions,
      'simultaneousFullRouter':bool(ranks[64]==9 and ranks[81]==9),
      'theorem':('The same complete 113-dimensional PSp-equivariant incidence Hom space between the obstruction-1080 and BT796/packet48-2160 carriers is projected onto both building-homology isotypic blocks. If both recorded spans equal nine, one geometric 2160 carrier realizes the complete M3(Q) multiplicity algebra on both H1(W33)^3 and H1(GQ(4,2))^3, with exact rational formulas for all six primitive projectors.'),
      'boundary':('This is finite building homology and characteristic-zero representation theory. Simultaneous routing does not identify either block with a physical field or observable.')
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','span64':ranks[64],'span81':ranks[81],'simultaneous':out['simultaneousFullRouter'],'hits64':len(hits[64]),'hits81':len(hits[81])},sort_keys=True))

if __name__=='__main__': main()
