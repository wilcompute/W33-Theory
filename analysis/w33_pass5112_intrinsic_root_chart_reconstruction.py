#!/usr/bin/env python3
"""Pass5112: intrinsic all-q root/chart reconstruction from theta minimum checks.

From the code, Pass5081 recovers theta checks as the complete dual weight-3 shell.
Two apartment variables are adjacent when they occur in one theta check; no pair
occurs in two checks.  For an adjacent pair a,b, define R(a,b) to contain a,b
and every common neighbor c for which the three pair-check labels are distinct.
By the all-q Tanner-six-cycle theorem (Pass5079), those triples are exactly the
apartments through one common length-four geodesic root.  Hence R(a,b) is the
q-apartment root block.

A theta check recovers three root blocks with common opposite endpoints.  A root
S belongs to the same opposite-pair chart iff it meets each of those three root
blocks in one apartment and the three intersections are distinct.  This recovers
all q+1 roots and therefore the C(q+1,2) apartment coordinates of the chart.
The proof is finite-GQ/girth-8 and works for every q; q=2,3,4 are rebuilt exactly.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5112_INTRINSIC_ROOT_CHART_RECONSTRUCTION.json'

def reconstruct(q):
    G=build_W(q);N=len(G['apartments'])
    checks=[]
    for _,loc in G['charts']:
        for tri in itertools.combinations(range(q+1),3):
            i,j,k=tri
            checks.append(tuple(sorted((loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]))))
    pair_check={};nbr=[set() for _ in range(N)]
    for ci,t in enumerate(checks):
        for a,b in itertools.combinations(t,2):
            e=(a,b)
            assert e not in pair_check
            pair_check[e]=ci;nbr[a].add(b);nbr[b].add(a)
    pair_root={};root_set={}
    for a,b in pair_check:
        common=nbr[a]&nbr[b];R={a,b}
        cab=pair_check[(a,b)]
        for c in common:
            cac=pair_check[tuple(sorted((a,c)))];cbc=pair_check[tuple(sorted((b,c)))]
            if len({cab,cac,cbc})==3:R.add(c)
        R=frozenset(R);assert len(R)==q
        root_set[R]=None;pair_root[(a,b)]=R
    roots=sorted(root_set,key=lambda z:tuple(sorted(z)));rid={R:i for i,R in enumerate(roots)}
    pair_rid={e:rid[R] for e,R in pair_root.items()};var_roots=[set() for _ in range(N)]
    for i,R in enumerate(roots):
        for a in R:var_roots[a].add(i)
    chart_fams=set()
    for t in checks:
        a,b,c=t
        base=[pair_rid[tuple(sorted(e))] for e in ((a,b),(a,c),(b,c))]
        assert len(set(base))==3
        R0,R1,R2=[roots[i] for i in base]
        cand=set()
        for x in R0:cand|=var_roots[x]
        fam=set(base)
        for s in cand:
            S=roots[s];ints=[S&R0,S&R1,S&R2]
            if all(len(z)==1 for z in ints) and len(set(next(iter(z)) for z in ints))==3:fam.add(s)
        assert len(fam)==q+1
        chart_fams.add(frozenset(fam))
    rec_support=set()
    for F in chart_fams:
        RR=[roots[i] for i in F];sup=set()
        for A,B in itertools.combinations(RR,2):
            z=A&B;assert len(z)==1;sup|=z
        assert len(sup)==q*(q+1)//2;rec_support.add(frozenset(sup))
    actual={frozenset(loc.values()) for _,loc in G['charts']}
    assert rec_support==actual
    exp_roots=q**3*(q+1)**2*(q**2+1);exp_charts=q**3*(q+1)*(q**2+1)
    assert len(roots)==exp_roots and len(chart_fams)==exp_charts
    return {'q':q,'apartments':N,'theta_checks':len(checks),'theta_adjacency_edges':len(pair_check),
            'recovered_roots':len(roots),'root_block_size':q,'recovered_charts':len(chart_fams),
            'roots_per_chart':q+1,'apartments_per_chart':q*(q+1)//2,'exact_support_match':True}

def main():
    out={'pass':5112,'status':'THEOREM_ALL_FINITE_GQ_INTRINSIC_ROOT_CHART_RECOVERY',
         'root_formula':'q^3 (q+1)^2 (q^2+1)','chart_formula':'q^3 (q+1)(q^2+1)',
         'algorithm':'dual weight-3 shell -> pair-labeled theta graph -> genuine Tanner-6 common-root blocks -> opposite-pair chart root families',
         'theorem_basis':'Pass5081 identifies all dual minima with theta; Pass5079 identifies genuine Tanner 6-cycles with common roots. GQ girth 8 gives uniqueness of the chart extension.',
         'anchors':{str(q):reconstruct(q) for q in (2,3,4)},
         'q5_predicted':{'roots':117000,'charts':19500,'theta_checks':390000,'apartments_per_chart':15},
         'consequence':'The local K_(q+1) cut-test/decoder placement is intrinsic to the apartment code and does not require external point/line labels.',
         'boundary':'Executable reconstruction is replayed at q=2,3,4; the all-q statement is the graph-theoretic theorem using the already-proved all-q root/Tanner characterization.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
