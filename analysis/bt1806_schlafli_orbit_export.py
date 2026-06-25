#!/usr/bin/env python3
"""BT1806: export Schlaefli graph/support data for GAP/Sage/nauty orbit work."""
from __future__ import annotations
import json
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
F=range(3)
BT1795_IMAGE=[5,7,10,12,15,18,20,22,29,30,34,36,37,38,40,41,42,44]
def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
def ppoints(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def pline(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)
def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    return (v[0],v[1],v[3])
def support():
    P=ppoints(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({pline(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        old.append(tuple(sorted(shell_coord(x) for x in L if x in shell)))
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [tuple(sorted(L)) for L in old+new]
def main():
    lines=support(); pts=sorted({p for L in lines for p in L}); ix={p:i+1 for i,p in enumerate(pts)}
    G=nx.Graph(); G.add_nodes_from(pts)
    for L in lines:
        for a,b in combinations(L,2): G.add_edge(a,b)
    S=nx.complement(G)
    edges=sorted((min(ix[a],ix[b]),max(ix[a],ix[b])) for a,b in S.edges())
    supports=[[ix[p] for p in L] for L in lines]
    dimacs=['c BT1806 Schlaefli graph SRG(27,16,10,8)']+[f'c v {ix[p]} {p}' for p in pts]+[f'p edge 27 {len(edges)}']+[f'e {u} {v}' for u,v in edges]
    (ROOT/'data'/'bt1806_schlafli_graph.dimacs').write_text('\n'.join(dimacs)+'\n')
    gap='SchlaefliEdges := '+json.dumps(edges)+';\nTritangentSupports := '+json.dumps(supports)+';\nBT1795Image := '+json.dumps(BT1795_IMAGE)+';\n'
    (ROOT/'analysis'/'bt1806_schlafli_orbit_export.gap').write_text(gap)
    sage='sch_edges = '+json.dumps([(u-1,v-1) for u,v in edges])+'\ntritangent_supports = '+json.dumps([[x-1 for x in L] for L in supports])+'\nbt1795_image = '+json.dumps(BT1795_IMAGE)+'\nG = Graph(sch_edges)\nprint(G.order(), G.size(), G.automorphism_group().order())\n'
    (ROOT/'analysis'/'bt1806_schlafli_orbit_export.sage').write_text(sage)
    payload={'bt':'BT1806','title':'Schlaefli orbit export','vertices':27,'edges':len(edges),'tritangent_supports':45,'bt1795_image':BT1795_IMAGE,'files':['data/bt1806_schlafli_graph.dimacs','analysis/bt1806_schlafli_orbit_export.gap','analysis/bt1806_schlafli_orbit_export.sage'],'expected_aut_order':51840,'conclusion':'BT1806 exports the exact Schlaefli graph, 45 tritangent supports, and BT1795 image in portable formats for the W(E6) orbit computation.'}
    (ROOT/'data'/'bt1806_schlafli_orbit_export.json').write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps(payload,indent=2,sort_keys=True))
if __name__=='__main__': main()
