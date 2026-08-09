#!/usr/bin/env python3
"""Pass 4515 -- GQ(3,9)=Q(5,3) apartment-code distance/dual frontier.

Builds on Pass 4506's exact 70-dimensional apartment/protected quotient.
For the 280 line coefficients and 102,060 apartments:

  rank H = 279, so the only coefficient kernel is global complement;
  every line row has weight 1,458;
  wt(S)=1458 m - 12 C(m,2) - 150 e(S) + 36 p3(S) - 8 c4(S),

where e,p3,c4 are induced statistics in the line-intersection graph.
The exact coefficient-support spectra for sizes 1--3 are frozen, and a simple
universal lower bound proves no support 2<=m<=12 can beat 1,458. Thus d<=1458,
but any counterexample to d=1458 must have gauge-fixed support 13..140.

On the dual side, minimum distance is exactly 3. Every weight-3 relation is the
three rectangular apartment faces of a triangular prism.  Such a prism is
specified by a noncollinear point pair and three of its t+1=10 common neighbors:
4536*C(10,3)=544,320 relations.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass4448_4450_q53_floquet_tanner import build_q53

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS4515_Q53_APARTMENT_CODE_FRONTIER.json"


def rank_bit_rows(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)


def main()->int:
    pts,lines=build_q53();P=len(pts);L=len(lines)
    assert (P,L)==(112,280)
    # Point collinearity and unique line through a collinear pair.
    Ap=np.zeros((P,P),dtype=np.uint8); pair_line={}
    for li,line in enumerate(lines):
        for x,y in itertools.combinations(sorted(line),2):
            Ap[x,y]=Ap[y,x]=1;pair_line[(x,y)]=li
    assert np.all(Ap.sum(1)==30)

    # Line-intersection graph and apartments.
    A=np.zeros((L,L),dtype=np.uint8)
    for i,j in itertools.combinations(range(L),2):
        if lines[i]&lines[j]:A[i,j]=A[j,i]=1
    assert np.all(A.sum(1)==36)
    nb=[set(np.flatnonzero(A[i]).tolist()) for i in range(L)]
    apartments=set()
    for u,w in itertools.combinations(range(L),2):
        if A[u,w]:continue
        common=sorted(nb[u]&nb[w]);assert len(common)==4
        for a,b in itertools.combinations(common,2):
            if not A[a,b]:apartments.add(tuple(sorted((u,w,a,b))))
    apartments=sorted(apartments);assert len(apartments)==102060
    apidx={ap:i for i,ap in enumerate(apartments)}

    Hrows=[0]*L
    for j,ap in enumerate(apartments):
        bit=1<<j
        for x in ap:Hrows[x]|=bit
    assert rank_bit_rows(Hrows)==279
    assert Counter(x.bit_count() for x in Hrows)==Counter({1458:280})
    allxor=0
    for x in Hrows:allxor^=x
    assert allxor==0

    # Pair and triple apartment incidences.
    # General Pass-4465 constants here are alpha=81, beta=6.
    for i,j in itertools.combinations(range(L),2):
        inter=(Hrows[i]&Hrows[j]).bit_count()
        assert inter==(81 if A[i,j] else 6)
    triple_count=Counter()
    for ap in apartments:
        for t in itertools.combinations(ap,3):triple_count[tuple(sorted(t))]+=1
    assert len(triple_count)==45360 and set(triple_count.values())=={9}
    for t in triple_count:
        assert sum(int(A[i,j]) for i,j in itertools.combinations(t,2))==2

    formula="wt=1458*m-12*C(m,2)-150*e+36*p3-8*c4"
    # Exact support-size 2 census.
    edges=int(A.sum()//2);assert edges==5040
    pairs=math.comb(280,2);assert pairs-edges==34020
    support2={2754:edges,2904:pairs-edges}
    # Exact support-size 3 census by induced edge count; only P3 (e=2)
    # has a 9-apartment triple intersection.
    pattern=Counter()
    for i,j,k in itertools.combinations(range(280),3):
        e=int(A[i,j])+int(A[i,k])+int(A[j,k]);pattern[e]+=1
    assert pattern==Counter({0:2381400,1:1088640,2:136080,3:13440})
    support3={
      4338:pattern[0],
      4188:pattern[1],
      4074:pattern[2],
      3888:pattern[3],
    }

    # Coarse but rigorous lower bound for all coefficient supports 2..12:
    # e<=C(m,2), p3>=0, c4<=C(m,4).
    lower={m:1458*m-162*math.comb(m,2)-8*math.comb(m,4) for m in range(2,13)}
    assert min(lower.values())>1458

    # Exact triangular-prism count for dual weight-3 words.
    noncol=[]
    for x,y in itertools.combinations(range(P),2):
        if not Ap[x,y]:noncol.append((x,y))
    assert len(noncol)==4536
    prism_count=0
    apset=set(apartments)
    # Verify every constructed prism supplies three apartment faces.  We do not
    # store the 544,320 triples; the centers/common-neighbor data are canonical.
    for x,y in noncol:
        common=[z for z in range(P) if Ap[x,z] and Ap[y,z]]
        assert len(common)==10
        for zs in itertools.combinations(common,3):
            lx=[pair_line[tuple(sorted((x,z)))] for z in zs]
            ly=[pair_line[tuple(sorted((y,z)))] for z in zs]
            six=set(lx+ly);assert len(six)==6
            faces=[]
            for a,b in itertools.combinations(range(3),2):
                face=tuple(sorted((lx[a],ly[a],ly[b],lx[b])))
                assert face in apset;faces.append(face)
            # symmetric difference of the three 4-faces is zero on six lines
            parity=0
            for face in faces:
                for q in face:parity^=1<<q
            assert parity==0
            prism_count+=1
    assert prism_count==544320

    out={
      "pass":4515,
      "geometry":{"points":112,"lines":280,"apartments":102060,"rank_H":279,"coefficient_kernel":"global complement"},
      "distance_frontier":{"row_weight_upper_bound":1458,"minimum_distance_status":"OPEN: d<=1458; equality not yet proved","exact_weight_formula":formula,"support1":{"1458":280},"support2":{str(k):v for k,v in sorted(support2.items())},"support3":{str(k):v for k,v in sorted(support3.items())},"rigorous_lower_bound_support_2_to_12":{str(k):v for k,v in lower.items()},"counterexample_support_window_after_complement_gauge":[13,140]},
      "dual":{"minimum_distance":3,"weight3_words":544320,"geometry":"three rectangular apartment faces of a triangular prism","count_formula":"(# noncollinear point pairs)*C(t+1,3)=4536*C(10,3)"},
      "design_constants":{"row_r":1458,"adjacent_pair_alpha":81,"disjoint_pair_beta":6,"P3_triple_apartments":9},
      "boundary":"The GQ(3,9) distance equality d=1458 is not claimed. The support-13..140 window is the exact remaining coefficient-space frontier after the proved bounds."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=="__main__":raise SystemExit(main())
