#!/usr/bin/env python3
"""Pass5177: P-chart components are Cut(K_{q+1}) tensor Cut(K_{q+1}).

For the P/opposite-point chart type, make the chart-intersection graph whose
vertices are opposite-point-pair charts and whose edges are apartments; every
apartment belongs to exactly two P charts.  For q=2,3,4,5 this graph splits into
q^2(q^2+1)/2 components, each K_m,m with m=C(q+1,2).  Since a P chart has m
apartment coordinates and its theta-triple equations are exactly the triangle
checks for Cut(K_{q+1}), the component restriction code is

    Cut(K_{q+1}) tensor Cut(K_{q+1}),

with parameters [m^2,q^2,q^2].

Important odd-q firewall: the canonical L/opposite-line chart-intersection graph
does NOT share this component decomposition (at q=3 and q=5 it is connected).
Therefore this producer promotes a P-side theorem only; no P/L symmetry is
silently assumed.
"""
from __future__ import annotations
import itertools,json
from collections import deque
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

def component_count(G,q,typ):
    charts=[loc for t,loc in G['charts'] if t==typ];nA=len(G['apartments'])
    owners=[[] for _ in range(nA)]
    for ci,loc in enumerate(charts):
        for a in loc.values():owners[a].append(ci)
    assert {len(x) for x in owners}=={2}
    cadj=[set() for _ in charts]
    for u,v in owners:cadj[u].add(v);cadj[v].add(u)
    seen=set();sizes=[]
    for s in range(len(charts)):
        if s in seen:continue
        C={s};Q=[s];seen.add(s)
        while Q:
            u=Q.pop()
            for v in cadj[u]:
                if v not in seen:seen.add(v);C.add(v);Q.append(v)
        sizes.append(len(C))
    return len(sizes),sorted(set(sizes))

def anchor(q):
    G=build_W(q);typ='P';charts=[loc for t,loc in G['charts'] if t==typ]
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
    expected=q*q*(q*q+1)//2;assert len(comps)==expected
    comp=comps[0];assert len(comp)==2*m
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
    rows=[]
    for ci in comp:
        loc=charts[ci]
        for tri in itertools.combinations(range(q+1),3):
            z=0
            for e in itertools.combinations(tri,2):z^=1<<idx[loc[tuple(sorted(e))]]
            rows.append(z)
    rank=gf2_rank(rows);dim=m*m-rank;assert dim==q*q
    lc,ls=component_count(G,q,'L')
    return {'q':q,'m':m,'P_components':len(comps),'P_charts_per_component':2*m,
            'P_apartments_per_component':m*m,'P_chart_intersection_component':f'K_{m},{m}',
            'P_triangle_check_rank':rank,'P_component_code_dimension':dim,
            'P_component_minimum_distance_formula':'q^2 by tensor-product distance',
            'L_chart_intersection_components':lc,'L_component_sizes':ls}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5177,'status':'THEOREM_P_TYPE_COMPONENT_TENSOR_DECOMPOSITION',
      'statement':'For P/opposite-point charts of W(3,q), the chart-intersection graph is a disjoint union of q^2(q^2+1)/2 copies of K_m,m with m=C(q+1,2). The theta-triangle restriction code on each P component is Cut(K_{q+1}) tensor Cut(K_{q+1}).',
      'component_parameters':'[m^2,q^2,q^2], m=q(q+1)/2',
      'q5_parameters':'325 P components, each [225,25,25], with 30 charts arranged as K_15,15.',
      'odd_q_asymmetry':'At q=3 and q=5 the L/opposite-line chart-intersection graph is connected in the canonical W(3,q) model; no L-side tensor decomposition is claimed.',
      'anchors':A,
      'heavy_shell_companion':'analysis/w33_pass5177_q5_tensor_heavy_enum.cpp',
      'boundary':'P-side necessary theorem only. A full apartment-code word must additionally satisfy the connected L-side theta constraints.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
