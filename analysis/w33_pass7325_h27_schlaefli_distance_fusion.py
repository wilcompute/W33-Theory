#!/usr/bin/env python3
"""Pass7325: Schlaefli as the distance-two fusion of the E8-derived H27 graph."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import w33_pass7186_e8_matter_h27_cayley as h

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7325_H27_SCHLAEFLI_DISTANCE_FUSION.json'

def srg_params(G):
    n=G.number_of_nodes();deg=set(dict(G.degree()).values());assert len(deg)==1;k=next(iter(deg));la=set();mu=set();V=list(G.nodes())
    for i,j in itertools.combinations(V,2):
        c=len(set(G[i])&set(G[j]));(la if G.has_edge(i,j) else mu).add(c)
    assert len(la)==len(mu)==1
    return n,k,next(iter(la)),next(iter(mu))

def main():
    V=[(u,z) for u in h.F for z in range(3)];G=nx.Graph();G.add_nodes_from(V)
    for x,y in itertools.combinations(V,2):
        u,z=x;v,w=y
        if u!=v and w==(z+h.coc(u,v))%3:G.add_edge(x,y)
    assert G.number_of_edges()==108 and set(dict(G.degree()).values())=={8}
    D={r:nx.Graph() for r in (1,2,3)}
    for r in D:D[r].add_nodes_from(V)
    for x in V:
        dx=nx.single_source_shortest_path_length(G,x)
        for y in V:
            if V.index(x)<V.index(y) and dx[y] in D:D[dx[y]].add_edge(x,y)
    assert set(dict(D[1].degree()).values())=={8};assert set(dict(D[2].degree()).values())=={16};assert set(dict(D[3].degree()).values())=={2}
    assert srg_params(D[2])==(27,16,10,8)
    H=nx.compose(D[1],D[3]);assert srg_params(H)==(27,10,1,5)
    # Distance-three relation is exactly the nine central cosets u x C3.
    comps=sorted(len(c) for c in nx.connected_components(D[3]));assert comps==[3]*9
    assert all(set(c)=={(u,z) for z in range(3)} for c in nx.connected_components(D[3]) for u in [next(iter(c))[0]])
    # Distance polynomial p2(lambda)=(lambda^2-lambda-8)/3 gives Schlaefli eigenvalues.
    ev={8:1,2:12,-1:8,-4:6};p2=Counter()
    for lam,m in ev.items():p2[(lam*lam-lam-8)//3]+=m
    assert p2==Counter({-2:20,4:6,16:1})
    out={'schema':'w33.pass7325.h27_schlaefli_distance_fusion.v1','status':'PASS',
      'H27_distance_graph':'intersection array {8,6,1;1,3,8}',
      'distance1':{'degree':8,'edges':108},
      'distance2':{'parameters':[27,16,10,8],'identification':'Schlaefli graph','spectrum':'16^1 + 4^6 + (-2)^20'},
      'distance3':{'graph':'9 K3','degree':2,'interpretation':'the nine central C3 cosets u x C3'},
      'distance1_plus_distance3':{'parameters':[27,10,1,5],'identification':'complement Schlaefli / GQ(2,4) point graph'},
      'theorem':'The E6 minuscule Schlaefli relation is exactly distance two in the E8-derived H27 matter graph. Equivalently, the H27 graph refines the complement-Schlaefli graph by deleting the nine central C3 triangles.',
      'index_hint':'Aut(Schlaefli) has order 51840 while the H27 refinement has order 1296; the index 40 motivates Pass7326.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','R2':'srg(27,16,10,8)','R3':'9K3'}))
if __name__=='__main__':main()
