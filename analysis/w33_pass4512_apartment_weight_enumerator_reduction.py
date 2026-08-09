#!/usr/bin/env python3
"""Pass 4512 -- exact reduction of the complete apartment-code weight enumerator.

The requested complete numerical coefficient table is not silently claimed.
Instead this pass derives the exact weight of every codeword from four induced
subgraph statistics of the dual W33 graph and computes the exact symmetry-
reduced search size by Burnside.

For a coefficient subset S of the 40 line coordinates, let m=|S|, e(S) be the
number of dual-W33 edges induced by S, p3(S) the number of induced P3 triples,
and c4(S) the number of induced apartment C4s. Then

  wt(H^T 1_S) = 162 m - 12 C(m,2) - 42 e(S) + 12 p3(S) - 8 c4(S).

Thus the complete enumerator is exactly

  W_C(z) = (1/2) sum_{S subset V(W33)} z^wt(S),

where the factor 1/2 is the global-complement kernel.  This removes the 1,620-
coordinate hypergraph from the remaining enumeration problem, but does not by
itself evaluate all coefficients.

Aut(C)=PGSp(4,3) has 25 cycle types on the 40 coefficients. Burnside gives
21,578,952 subset orbits and 10,789,604 codeword orbits after adjoining global
complement. This is the exact size of a symmetry-complete orbit enumeration.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4511_4514_dual_even_prism_ihara import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS4512_APARTMENT_WEIGHT_ENUMERATOR_REDUCTION.json"
DIST=ROOT/"data"/"PART_W33_PASS4495_4502_DISTANCE_PRISM_RECONSTRUCTION.json"


def cycle_lengths(p):
    seen=[False]*len(p); out=[]
    for i in range(len(p)):
        if not seen[i]:
            j=i;n=0
            while not seen[j]: seen[j]=True;n+=1;j=p[j]
            out.append(n)
    return tuple(sorted(out))


def main()->int:
    pts,pidx,lines,A,apartments,apmasks,H=geometry()
    # Exact apartment-design incidence constants.
    row=Counter(int(H[i].sum()) for i in range(40)); assert row==Counter({162:40})
    pair=Counter()
    for i,j in itertools.combinations(range(40),2):
        pair[(int(A[i,j]),int(np.dot(H[i],H[j])))] += 1
    assert pair==Counter({(0,6):540,(1,27):240})
    triples=Counter()
    for ap in apartments:
        for t in itertools.combinations(ap,3): triples[tuple(sorted(t))]+=1
    assert len(triples)==2160 and set(triples.values())=={3}
    for t in triples:
        assert sum(int(A[i,j]) for i,j in itertools.combinations(t,2))==2

    # The Newton expansion of odd parity on j=0..4 is
    # 1_odd(j)=C(j,1)-2C(j,2)+4C(j,3)-8C(j,4).
    formula="wt=162*m-12*C(m,2)-42*e+12*p3-8*c4"
    apset=set(apmasks)
    # Exhaustively verify the specialization on every coefficient subset of size <=4.
    for m in range(5):
        for S in itertools.combinations(range(40),m):
            mask=sum(1<<i for i in S)
            e=sum(int(A[i,j]) for i,j in itertools.combinations(S,2))
            p3=sum(1 for t in itertools.combinations(S,3)
                   if sum(int(A[i,j]) for i,j in itertools.combinations(t,2))==2)
            c4=sum(1 for q in itertools.combinations(S,4) if sum(1<<i for i in q) in apset)
            w=162*m-12*math.comb(m,2)-42*e+12*p3-8*c4
            b=np.zeros(40,dtype=np.uint8);b[list(S)]=1
            assert w==int(((b@H)%2).sum())

    selected,psp,outer,pgsp=build_groups(pts,pidx,lines)
    assert len(pgsp)==51840
    ctype=Counter(cycle_lengths(p) for p in pgsp)
    assert len(ctype)==25
    fixed=sum(n*(1<<len(t)) for t,n in ctype.items())
    twisted=sum(n*(1<<len(t)) for t,n in ctype.items() if all(x%2==0 for x in t))
    subset_orbits=fixed//51840
    codeword_orbits=(fixed+twisted)//(2*51840)
    assert subset_orbits==21578952 and codeword_orbits==10789604
    assert twisted==13271040

    dist=json.loads(DIST.read_text(encoding="utf-8"))
    low=dist["4495_primal_distance"]["exact_low_weight_counts"]
    assert low=={"162":40,"270":240,"312":540,"324":200}

    out={
      "pass":4512,
      "code":{"length":1620,"dimension":39,"codewords":2**39,"global_kernel":"S~V\\S"},
      "exact_weight_formula":formula,
      "formula_statistics":{"m":"vertices of coefficient subset","e":"induced dual-W33 edges","p3":"induced P3 triples","c4":"induced apartment C4s"},
      "design_constants":{"row_apartments":162,"intersecting_pair_apartments":27,"disjoint_pair_apartments":6,"P3_triple_apartments":3},
      "proved_low_weight_enumerator":{"0":1,**low},
      "Burnside":{"AutC_order":51840,"cycle_types":25,"subset_orbits":subset_orbits,"codeword_orbits_mod_complement":codeword_orbits,"twisted_complement_fixed_sum":twisted},
      "exact_centered_weight_moments":{"mean":810,"variance":405,"third":-1620,"fourth":"1236465/2"},
      "complete_numerical_enumerator_status":"OPEN",
      "remaining_exact_task":"evaluate the four-statistic induced-subgraph polynomial on 10,789,604 PGSp+complement codeword orbits",
      "boundary":"The displayed sum is an exact reduction, not a completed coefficient table. The repository must not describe the full enumerator as closed until those orbit weights are actually accumulated."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=="__main__":raise SystemExit(main())
