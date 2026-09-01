#!/usr/bin/env python3
"""Exact 1080 = 27 x 40 product factorization of the depth-3 obstruction.

The construction uses only PG(3,3), its symplectic polarity, and the already
certified GQ(4,2) disjointness relation on the 45 hyperbolic polar pairs.

For each of the 27 five-packet completion charts, its ten packet-pair edges
name ten all-isotropic reguli.  The new fact is that these ten reguli partition
all 40 totally isotropic W33 lines, four at a time.

Consequently every transversal-free triple has two canonical coordinates:
  (1) its unique one of 27 completion charts;
  (2) the unique W33 line omitted from its four-line isotropic regulus.

This gives a natural incidence/polarity-defined bijection

    BadTriples_1080  <->  CompletionCharts_27 x W33Lines_40.

No matching-integer inference is used: the inverse map is constructed and
checked on every one of the 27*40 pairs.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from bt810_completed_geography_schlafli import canon3

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260901_DEPTH3_PRODUCT_FACTORIZATION.json"


def geometry():
    pts = sorted({canon3(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    pidx = {p:i for i,p in enumerate(pts)}
    assert len(pts) == 40

    def symp(x,y):
        return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1]) % 3

    lines = set()
    for a,b in itertools.combinations(pts,2):
        L=set()
        for s,t in itertools.product(range(3), repeat=2):
            if s==t==0: continue
            L.add(canon3(tuple((s*x+t*y)%3 for x,y in zip(a,b))))
        lines.add(frozenset(L))
    assert len(lines)==130

    iso = sorted((L for L in lines if all(symp(a,b)==0 for a,b in itertools.combinations(sorted(L),2))),
                 key=lambda L:tuple(sorted(pidx[p] for p in L)))
    hyp = sorted(set(lines)-set(iso), key=lambda L:tuple(sorted(pidx[p] for p in L)))
    assert len(iso)==40 and len(hyp)==90
    iidx={L:i for i,L in enumerate(iso)}

    def perp(L):
        a,b=sorted(L)[:2]
        return frozenset(p for p in pts if symp(p,a)==0 and symp(p,b)==0)

    pairset={frozenset((L,perp(L))) for L in hyp}
    assert len(pairset)==45 and all(len(P)==2 for P in pairset)
    pairs=sorted(pairset, key=lambda P:tuple(sorted(tuple(sorted(pidx[x] for x in L)) for L in P)))
    supports=[frozenset().union(*P) for P in pairs]
    assert {len(S) for S in supports}=={8}
    return pts,iso,iidx,pairs,supports


def main():
    pts,iso,iidx,pairs,supports=geometry()

    # The 45-packet disjointness graph: SRG(45,12,3,3), whose 27 maximal
    # 5-cliques are the GQ(4,2) lines / E8 completion charts.
    adj=[set() for _ in range(45)]
    edges=[]
    for a,b in itertools.combinations(range(45),2):
        if supports[a].isdisjoint(supports[b]):
            adj[a].add(b);adj[b].add(a);edges.append(frozenset((a,b)))
    assert len(edges)==270 and {len(N) for N in adj}=={12}

    charts=[]
    for C in itertools.combinations(range(45),5):
        if all(b in adj[a] for a,b in itertools.combinations(C,2)):
            charts.append(tuple(C))
    assert len(charts)==27
    edge_chart={}
    for ci,C in enumerate(charts):
        for a,b in itertools.combinations(C,2):
            e=frozenset((a,b))
            assert e not in edge_chart
            edge_chart[e]=ci
    assert len(edge_chart)==270

    # Each obstruction edge names one all-isotropic regulus: the four W33
    # lines meeting all four hyperbolic lines in the two polar pairs.
    edge_regulus={}
    for e in edges:
        a,b=tuple(e)
        opposite=set(pairs[a])|set(pairs[b])
        assert len(opposite)==4
        R=tuple(sorted(iidx[L] for L in iso if all(L & H for H in opposite)))
        assert len(R)==4
        assert all(not (iso[x]&iso[y]) for x,y in itertools.combinations(R,2))
        edge_regulus[e]=R

    # NEW: on each chart the ten reguli partition all forty W33 lines.
    chart_partition=[]
    for ci,C in enumerate(charts):
        cnt=Counter()
        blocks=[]
        for a,b in itertools.combinations(C,2):
            R=edge_regulus[frozenset((a,b))]
            blocks.append(R)
            cnt.update(R)
        assert len(blocks)==10
        assert len(cnt)==40 and set(cnt.values())=={1}
        chart_partition.append(tuple(sorted(blocks)))

    # Every bad triple is a 3-subset of exactly one regulus.  Record its
    # unique coordinates (chart, omitted W33 line) and prove that every one of
    # the 27*40 coordinate pairs occurs exactly once.
    triple_coords={}
    coordinate_triples={}
    for e,R in edge_regulus.items():
        ci=edge_chart[e]
        for missing in R:
            T=tuple(sorted(x for x in R if x!=missing))
            assert len(T)==3
            # Pairwise skew / transversal-free family in W33.
            assert all(not (iso[x]&iso[y]) for x,y in itertools.combinations(T,2))
            coord=(ci,missing)
            assert T not in triple_coords and coord not in coordinate_triples
            triple_coords[T]=coord
            coordinate_triples[coord]=T
    assert len(triple_coords)==1080
    assert len(coordinate_triples)==27*40
    assert set(coordinate_triples)==set(itertools.product(range(27),range(40)))

    omitted=Counter(missing for _ci,missing in triple_coords.values())
    contained=Counter(x for T in triple_coords for x in T)
    assert set(omitted.values())=={27}
    assert set(contained.values())=={81}

    # Incidence check: every W33 line belongs to exactly one regulus in each
    # completion chart, hence to 27 reguli globally.  Each such regulus gives
    # one triple omitting it and three triples containing it.
    regulus_membership=Counter(x for R in edge_regulus.values() for x in R)
    assert set(regulus_membership.values())=={27}

    out={
      "schema":"w33.20260901.depth3-product-factorization.v1",
      "status":"PASS",
      "carriers":{
        "depth3TransversalFreeTriples":1080,
        "completionCharts":27,
        "w33Lines":40,
        "factorization":"1080 = 27 * 40"
      },
      "chartGeometry":{
        "packets":45,
        "obstructionEdges":270,
        "edgesPerChart":10,
        "reguliPerChart":10,
        "isotropicLinesPerRegulus":4,
        "eachChartPartitionsAll40W33Lines":True
      },
      "bijection":{
        "forward":"bad triple -> (unique completion chart of its regulus, omitted fourth W33 line)",
        "inverse":"(chart, W33 line ell) -> unique chart-regulus containing ell, with ell deleted",
        "allCoordinatePairsHitExactlyOnce":True,
        "naturalUnderIncidenceAndPolarity":True
      },
      "multiplicities":{
        "reguliThroughEachW33Line":27,
        "badTriplesOmittingEachW33Line":27,
        "badTriplesContainingEachW33Line":81
      },
      "representationReading":"The 1080 obstruction carrier is the natural diagonal product PSp-carrier 27 x 40. This supplies an explicit intermediate/product bridge where the direct characteristic-zero 27-to-40 linear intertwiner is known to be trivial beyond constants.",
      "boundary":"The product factorization is a finite incidence theorem. The number 81 here is a triple-containment multiplicity; it is not by itself an identification with the separate 81-dimensional Steinberg/H1 module."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,sort_keys=True))

if __name__=="__main__":
    main()
