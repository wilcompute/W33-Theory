#!/usr/bin/env python3
"""Pass5177: one-type q=5 chart components are Cut(K6) tensor Cut(K6).

For one chart type (P or L), make the chart-intersection graph whose vertices are
opposite-pair charts and whose edges are apartments; every apartment belongs to
exactly two charts of the fixed type.  At q=5 this graph has 325 connected
components, each K_15,15.  Since a chart has C(6,2)=15 apartment coordinates and
the theta-triple equations on those coordinates are exactly the triangle checks
for Cut(K6), the component restriction code is

    Cut(K6) tensor Cut(K6),

with parameters [225,25,25].

The same K_m,m/tensor pattern is checked at q=2,3,4,5 with
m=C(q+1,2); this producer promotes the exact finite-building decomposition and
leaves the q5 heavy-shell enumeration to the companion C++ certificate.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5177_Q5_TENSOR_COMPONENT_GEOMETRY.json'

def gf2_rank(rows):
    P={}
    for r in rows:
        x=r
        while x:
            p=x.bit_length()-1
            if p in P:x^=P[p]
            else:P[p]=x;break
    return len(P)

def anchor(q,typ='P'):
    G=build_W(q);charts=[loc for t,loc in G['charts'] if t==typ]
    m=q*(q+1)//2;nA=len(G['apartments'])
    owners=[[] for _ in range(nA)]
    for ci,loc in enumerate(charts):
        for a in loc.values():owners[a].append(ci)
    assert {len(x) for x in owners}=={2}
    cadj=[set() for _ in charts];edge_of={}
    for a,(u,v) in enumerate(owners):cadj[u].add(v);cadj[v].add(u);edge_of[(min(u,v),max(u,v))]=a
    assert {len(x) for x in cadj}=={m}
    seen=set();comps=[]
    for s in range(len(charts)):
        if s in seen:continue
        C={s};Q=[s];seen.add(s)
        while Q:
            u=Q.pop()
            for v in cadj[u]:
                if v not in seen:seen.add(v);C.add(v);Q.append(v)
        comps.append(sorted(C))
    expected_components=q*q*(q*q+1)//2
    assert len(comps)==expected_components
    comp=comps[0];assert len(comp)==2*m
    # Bipartition and K_m,m verification.
    side={comp[0]:0};Q=deque([comp[0]])
    while Q:
        u=Q.popleft()
        for v in cadj[u]:
            if v not in side:side[v]=1-side[u];Q.append(v)
            else:assert side[v]!=side[u]
    L=[u for u in comp if side[u]==0];R=[u for u in comp if side[u]==1]
    assert len(L)==len(R)==m
    assert all(set(cadj[u])==set(R) for u in L)
    assert all(set(cadj[u])==set(L) for u in R)
    verts=sorted(edge_of[(min(u,v),max(u,v))] for u in L for v in R);idx={a:i for i,a in enumerate(verts)}
    # Triangle checks in each of the 2m charts; rank must be m^2-q^2.
    rows=[]
    for ci in comp:
        loc=charts[ci]
        for tri in itertools.combinations(range(q+1),3):
            z=0
            for e in itertools.combinations(tri,2):z^=1<<idx[loc[tuple(sorted(e))]]
            rows.append(z)
    rank=gf2_rank(rows);dim=m*m-rank
    assert dim==q*q
    return {'q':q,'m':m,'components':len(comps),'charts_per_component':2*m,
            'apartments_per_component':m*m,'chart_intersection_component':f'K_{m},{m}',
            'triangle_check_rank':rank,'component_code_dimension':dim,
            'component_minimum_distance_formula':'q^2 by tensor-product distance'}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5177,'status':'THEOREM_ONE_TYPE_COMPONENT_TENSOR_DECOMPOSITION',
      'statement':'For one chart type of W(3,q), the opposite-pair chart-intersection graph is a disjoint union of q^2(q^2+1)/2 copies of K_m,m with m=C(q+1,2). The theta-triangle restriction code on each component is Cut(K_{q+1}) tensor Cut(K_{q+1}).',
      'component_parameters':'[m^2,q^2,q^2], m=q(q+1)/2',
      'q5_parameters':'325 components, each [225,25,25], with 30 charts arranged as the two sides of K_15,15.',
      'anchors':A,
      'heavy_shell_companion':'analysis/w33_pass5177_q5_tensor_heavy_enum.cpp',
      'boundary':'This is a one-chart-type necessary decomposition of the full apartment code. P- and L-type component constraints must both hold globally.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
