#!/usr/bin/env python3
"""Pass5181 (bonkers): characteristic-parity point/line tensor firewall.

Pass5177 discovered that P/opposite-point chart intersections split into
K_m,m components with m=C(q+1,2).  It is tempting to dualize that statement to
L/opposite-line charts.  This is valid in even characteristic because W_3(q) is
self-dual, but it is false as a same-geometry statement in the odd-q canonical
model: W_3(q)^D is Q_4(q), not W_3(q).

This producer certifies the exact chart-intersection component structure at
q=2,3,4,5.  At q=2,4 the P and L decompositions agree componentwise, as forced
by self-duality.  At q=3,5 the P graph still has the tensor components while the
L graph is connected.  Thus the q5 equality-shell attack genuinely has a
factorized P side and a connected L side.
"""
from __future__ import annotations
import json
from collections import Counter,deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5181_POINT_LINE_DUALITY_FIREWALL.json'

def chart_graph(G,typ):
    charts=[loc for t,loc in G['charts'] if t==typ];nA=len(G['apartments'])
    o1=[-1]*nA;adj=[set() for _ in charts]
    for ci,loc in enumerate(charts):
        for a in loc.values():
            if o1[a]<0:o1[a]=ci
            else:
                u=o1[a];adj[u].add(ci);adj[ci].add(u)
    seen=set();comps=[]
    for s in range(len(charts)):
        if s in seen:continue
        C={s};Q=[s];seen.add(s)
        while Q:
            u=Q.pop()
            for v in adj[u]:
                if v not in seen:seen.add(v);C.add(v);Q.append(v)
        comps.append(sorted(C))
    return charts,adj,comps

def is_complete_bipartite_component(adj,C,m):
    side={C[0]:0};Q=deque([C[0]])
    while Q:
        u=Q.popleft()
        for v in adj[u]:
            if v not in C:continue
            if v not in side:side[v]=1-side[u];Q.append(v)
            elif side[v]==side[u]:return False
    L=[u for u in C if side[u]==0];R=[u for u in C if side[u]==1]
    return len(L)==len(R)==m and all((adj[u]&set(C))==set(R) for u in L) and all((adj[u]&set(C))==set(L) for u in R)

def anchor(q):
    G=build_W(q);m=q*(q+1)//2;row={'q':q,'m':m}
    for typ in ('P','L'):
        charts,adj,comps=chart_graph(G,typ)
        row[typ+'_charts']=len(charts);row[typ+'_degree_set']=sorted({len(x) for x in adj})
        row[typ+'_components']=len(comps);row[typ+'_component_size_set']=sorted({len(C) for C in comps})
        row[typ+'_first_component_Kmm']=is_complete_bipartite_component(adj,comps[0],m) if len(comps[0])==2*m else False
    if q%2==0:
        expected=q*q*(q*q+1)//2
        assert row['P_components']==row['L_components']==expected
        assert row['P_component_size_set']==row['L_component_size_set']==[2*m]
        assert row['P_first_component_Kmm'] and row['L_first_component_Kmm']
    else:
        assert row['P_components']==q*q*(q*q+1)//2 and row['P_component_size_set']==[2*m]
        assert row['P_first_component_Kmm']
        assert row['L_components']==1
    return row

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5181,'status':'THEOREM_EVEN_Q_DUAL_TENSOR_TRANSFER_WITH_ODD_Q_CONNECTED_ANCHORS',
      'P_side':'Pass5177 gives the P/opposite-point K_m,m tensor decomposition for all q, m=C(q+1,2).',
      'even_q_transfer':'For even q, classical W_3(q) is self-dual. Any point-line duality sends opposite-point charts to opposite-line charts and preserves apartment incidence, so the complete P tensor decomposition transfers to the L side.',
      'odd_q_firewall':'For odd q, the dual of W_3(q) is Q_4(q), not W_3(q); there is no same-geometry duality that licenses the transfer. Exact q=3 and q=5 anchors show the L chart-intersection graph is connected while P remains factorized.',
      'anchors':A,
      'q5_structure':'P: 325 copies of K_15,15 and [225,25,25] local tensor codes. L: one connected 9750-chart degree-15 graph. These are genuinely different constraint geometries on the same 73125 apartment coordinates.',
      'external_boundary':'Classical duality source: Crnkovic, Hawtin, Svob, arXiv:2105.05833, Sec.2 states W_3(q) is self-dual for q even and has dual Q_4(q) for q odd.',
      'consequence':'The remaining q5 equality-shell problem should be formulated as a factorized-P / connected-L gluing problem, not by copying P-component knapsack arguments to L.',
      'boundary':'The connected-L statement is certified here at q=3,5; no all-odd-q connectedness theorem is claimed. The all-even-q tensor transfer follows from self-duality plus Pass5177.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
