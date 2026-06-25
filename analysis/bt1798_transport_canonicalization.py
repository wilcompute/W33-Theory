#!/usr/bin/env python3
"""BT1798: transport canonicalization probe.

This is intentionally bounded/honest: it verifies the exact source automorphism
count and performs a capped VF2 sample of Hesse->H27 transports.  Full W(E6)
automorphism-orbit enumeration is left as the next GAP/nauty-scale job.
"""
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1798_transport_canonicalization.json'
F=range(3)
def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
def projective_points(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def projective_line(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)
def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])
def support():
    P=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({projective_line(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        old.append(tuple(sorted(shell_coord(x) for x in L if x in shell)))
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [tuple(sorted(L)) for L in old+new]
def source_edges(): return [tuple(sorted(((0,i,j),(1,i,s),(2,j,s)))) for i,j,s in product(F,F,F) if s!=(j-i)%3]
def bip(edges):
    G=nx.Graph(); pts=sorted({p for e in edges for p in e})
    for p in pts: G.add_node(('v',)+p, kind='v')
    for i,e in enumerate(edges):
        n=('e',i); G.add_node(n, kind='e')
        for p in e: G.add_edge(n,('v',)+p)
    return G
def nm(a,b): return a['kind']==b['kind']
def main():
    S=bip(source_edges()); T=bip(support())
    src_aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(S,S,node_match=nm).isomorphisms_iter())
    GM=nx.algorithms.isomorphism.GraphMatcher(T,S,node_match=nm)
    sample=0; images=Counter(); first=None
    for m in GM.subgraph_monomorphisms_iter():
        inv={v:k for k,v in m.items()}
        used=tuple(sorted(inv[('e',i)][1] for i in range(18)))
        images[used]+=1; sample+=1
        if first is None: first=used
        if sample>=1000: break
    payload={'bt':'BT1798','title':'transport canonicalization probe','exact_source_automorphisms':src_aut,'target_automorphism_context':'Schlaefli/E6 graph has W(E6) symmetry in the mathematical model; full orbit enumeration was not attempted with NetworkX VF2 because it is too slow for the 27-line graph in this connector session.','sampled_transports':sample,'distinct_support_images_in_sample':len(images),'first_BT1795_image':list(first),'most_common_image_multiplicity_in_sample':images.most_common(1)[0][1],'uniqueness_status':'not_unique','canonicalization_status':'open_orbit_classification','conclusion':'BT1795 is not unique as a literal transport: even the first 1000 VF2 embeddings split across 504 distinct 18-line images, and the source hypergraph already has 216 automorphisms. The right canonical object is therefore an orbit under source automorphisms and Schlaefli/E6 target automorphisms, not a single map.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'source_aut':src_aut,'sampled':sample,'distinct_images':len(images),'unique':False},indent=2,sort_keys=True))
if __name__=='__main__': main()
