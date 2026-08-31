#!/usr/bin/env python3
"""Exact 216-line hemisystem eigenframe in the W33 -4 eigenspace.

Holotrade's exact m-ovoid census supplies one size-20 2-ovoid T.  Its
PSp(4,3) orbit has 432 members and complement pairs them into 216 unoriented
objects.  This audit proves that these are not merely combinatorial halves:

  * every T meets every W33 line in 2 points;
  * every T meets every one of the 45 sentinel weight-8 supports in 4 points;
  * every characteristic word 1_T lies in the binary sentinel code C_S;
  * h_T = 2 1_T - 1 is a {+/-1} eigenvector Ah_T=-4 h_T;
  * complement sends h_T to -h_T, giving 216 projective eigenlines in the
    15-dimensional -4 eigenspace;
  * the 216 rank-one projectors form an exact tight frame with frame constant
    576:

      sum_[T]/complement h_T h_T^T = 576 E_{-4}
                                 = 192 I - 96 A + 24 J.

The script also freezes the complete projective angle distribution and tests
whether absolute inner product alone resolves the orbital relations.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

import w33_20260829_216_clifford_torsor_nogo as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_HEMISYSTEM_EIGENFRAME_576.json'
T0=frozenset([0,1,2,3,5,7,8,9,15,16,17,20,24,26,27,28,33,34,36,39])
ALL=frozenset(range(40))


def gf2_rank(rows, n=40):
    xs=[int(x) for x in rows if x]
    rank=0
    for bit in range(n-1,-1,-1):
        piv=next((i for i in range(rank,len(xs)) if (xs[i]>>bit)&1),None)
        if piv is None: continue
        xs[rank],xs[piv]=xs[piv],xs[rank]
        for i in range(len(xs)):
            if i!=rank and ((xs[i]>>bit)&1): xs[i]^=xs[rank]
        rank+=1
    return rank


def mask(S):
    z=0
    for x in S: z|=1<<x
    return z


def canon_pair(T):
    C=ALL-T
    a,b=tuple(sorted(T)),tuple(sorted(C))
    return (a,b) if a<b else (b,a)


def main():
    pts,idx,lines,N=base.geometry(); supports,masks=base.supports_from_N(N)
    assert len(lines)==40 and len(supports)==45

    # Native W33 adjacency matrix.
    A=np.zeros((40,40),dtype=np.int64)
    for L in lines:
        for a in L:
            for b in L:
                if a!=b: A[a,b]=1
    assert set(map(int,A.sum(axis=1)))=={12}

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    chosen=(18,62,77,10)
    # We need only the 40-point group here; pair with itself for closure helper.
    G=base.closure([gens40[i] for i in chosen],40) if hasattr(base,'closure') else None
    if G is None:
        # deterministic local closure fallback
        e=tuple(range(40)); Gset={e}; q=[e]
        gg=[gens40[i] for i in chosen]
        while q:
            a=q.pop()
            for g in gg:
                b=base.compose(g,a)
                if b not in Gset: Gset.add(b); q.append(b)
        G=Gset
    assert len(G)==25920

    orbit={frozenset(g[x] for x in T0) for g in G}
    assert len(orbit)==432
    pairs=sorted({canon_pair(T) for T in orbit})
    assert len(pairs)==216

    # Sentinel code C_S: span of the 45 weight-8 supports has binary rank 15.
    support_masks=[mask(S) for S in supports]
    assert gf2_rank(support_masks)==15

    line_intersections=Counter(); support_intersections=Counter(); code_fail=0
    signs=[]; chosen_halves=[]
    for P in pairs:
        T=frozenset(P[0]); chosen_halves.append(T)
        lint=tuple(sorted(len(T & set(L)) for L in lines))
        assert set(lint)=={2}
        line_intersections.update(lint)
        sint=tuple(sorted(len(T & S) for S in supports))
        assert set(sint)=={4}
        support_intersections.update(sint)
        if gf2_rank(support_masks+[mask(T)])!=15: code_fail+=1
        h=np.array([1 if i in T else -1 for i in range(40)],dtype=np.int64)
        assert int(h.sum())==0
        assert np.array_equal(A@h,-4*h)
        signs.append(h)
    assert code_fail==0
    H=np.stack(signs,axis=1) # 40 x 216
    assert np.linalg.matrix_rank(H.astype(float))==15

    # Exact frame operator.  Orientation choices cancel in h h^T.
    frame=H@H.T
    I=np.eye(40,dtype=np.int64); J=np.ones((40,40),dtype=np.int64)
    expected=192*I-96*A+24*J
    assert np.array_equal(frame,expected)
    # E_-4=(8I-4A+J)/24, hence expected=576 E_-4.
    projector_num=8*I-4*A+J
    assert np.array_equal(24*frame,576*projector_num)
    assert int(np.trace(frame))==216*40

    # BB^T identity explains why B^T h=0 and pins the rational rank at 25.
    B=np.zeros((40,45),dtype=np.int64)
    for j,S in enumerate(supports):
        for i in S: B[i,j]=1
    BB=B@B.T
    assert np.array_equal(BB,8*I+2*A+J)
    assert np.linalg.matrix_rank(B.astype(float))==25
    assert np.array_equal(B.T@H,np.zeros((45,216),dtype=np.int64))

    # Projective angle distribution.  Dot products are orientation-dependent,
    # absolute dots are line invariants.  Norm^2=40.
    abs_hist=Counter(); signed_hist=Counter()
    base_abs=Counter(); base_signed=Counter(); intersection_hist=Counter()
    for i in range(216):
        Ti=chosen_halves[i]
        for j in range(i+1,216):
            d=int(signs[i]@signs[j]); signed_hist[d]+=1; abs_hist[abs(d)]+=1
            intersection_hist[len(Ti & chosen_halves[j])]+=1
    for j in range(1,216):
        d=int(signs[0]@signs[j]); base_abs[abs(d)]+=1; base_signed[d]+=1
    # Transitivity on lines implies global undirected counts must be 216*k/2.
    for d,c in abs_hist.items():
        assert 2*c%216==0
    valencies={d:2*c//216 for d,c in sorted(abs_hist.items())}
    assert sum(valencies.values())==215

    # Stabilizer suborbits on the 216 projective lines and whether |dot|
    # distinguishes them.  Stabilize the first canonical pair.
    P0=pairs[0]; Tbase=frozenset(P0[0]); Cbase=ALL-Tbase
    Hp=[g for g in G if frozenset(g[x] for x in Tbase) in (Tbase,Cbase)]
    assert len(Hp)==120
    pidx={P:i for i,P in enumerate(pairs)}
    def act(g,i):
        T=frozenset(pairs[i][0]); return pidx[canon_pair(frozenset(g[x] for x in T))]
    rem=set(range(216)); sub=[]
    while rem:
        s=min(rem); O={act(g,s) for g in Hp}; sub.append(sorted(O)); rem-=O
    sub=sorted(sub,key=lambda O:(len(O),O))
    subrows=[]
    for O in sub:
        vals=sorted({abs(int(signs[0]@signs[j])) for j in O})
        subrows.append({'size':len(O),'absoluteDotsFromBase':vals})
    abs_resolves=(len(sub)==1+len(valencies) and all(len(r['absoluteDotsFromBase'])==1 for r in sub))

    # Entry counts of frame operator give a compact geometric checksum.
    frame_by_relation={
      'diagonal':sorted({int(frame[i,i]) for i in range(40)}),
      'adjacent':sorted({int(frame[i,j]) for i in range(40) for j in range(40) if A[i,j]}),
      'nonadjacent':sorted({int(frame[i,j]) for i in range(40) for j in range(40) if i!=j and not A[i,j]}),
    }
    assert frame_by_relation=={'diagonal':[216],'adjacent':[-72],'nonadjacent':[24]}

    out={
      'schema':'w33.20260831.hemisystem-eigenframe-576.v1','status':'PASS',
      'hemisystems':{'oriented':432,'complementPairs':216,'size':20,
        'lineIntersection':2,'sentinelSupportIntersection':4,
        'binarySentinelCodeMembershipAll216Representatives':True},
      'spectral':{'adjacencyEigenvalue':-4,'eigenspaceDimension':15,
        'projectiveEigenlines':216,'spanDimension':15,'normSquared':40},
      'sentinelIncidence':{'shape':[40,45],'rationalRank':25,
        'BBtIdentity':'B B^T = 8 I + 2 A + J','BtHZero':True},
      'tightFrame':{'frameConstant':576,
        'identity':'sum_[T]/complement h_T h_T^T = 576 E_-4 = 192 I - 96 A + 24 J',
        'entryValues':frame_by_relation},
      'projectiveAngles':{'absoluteDotHistogram':dict(sorted(abs_hist.items())),
        'absoluteDotValenciesFromEachLine':valencies,
        'signedDotHistogramForChosenOrientations':dict(sorted(signed_hist.items())),
        'chosenHalfIntersectionHistogram':dict(sorted(intersection_hist.items())),
        'baseAbsoluteDots':dict(sorted(base_abs.items())),
        'baseSignedDots':dict(sorted(base_signed.items()))},
      'hemisystemPairAction':{'stabilizerOrder':120,'subdegrees':sorted(map(len,sub)),
        'suborbits':subrows,'absoluteDotResolvesOrbitals':abs_resolves},
      'theorem':'The 432 W33 two-ovoids center to 432 antipodal +/-1 eigenvectors in the -4 adjacency eigenspace. Their 216 complement-pairs form a PSp(4,3)-transitive projective tight frame in dimension 15 with exact frame constant 576. Every half is a weight-20 sentinel-code word and is exactly 4-balanced against all 45 sentinel minima.',
      'boundary':'The number 576 here is an exact finite-frame constant. No identification with unrelated order-576 groups, Latin-square counts, or physical constants is asserted without an explicit equivariant construction.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({'status':'PASS','frame':576,'rankH':15,'rankB':25,
      'absDots':dict(sorted(abs_hist.items())),'valencies':valencies,
      'subdegrees':sorted(map(len,sub)),'absResolves':abs_resolves,
      'frameEntries':frame_by_relation},sort_keys=True))

if __name__=='__main__': main()
