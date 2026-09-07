#!/usr/bin/env python3
"""Pass7328: the 90-D4 scheme antipodal quotient is the 45-tritangent 1+20+24 scheme."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7182_d4_glue_spread_code as d

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7328_D4_ANTIPODAL_TRITANGENT_FUSION.json'

def srg(G):
    V=list(G);kset=set(dict(G.degree()).values());assert len(kset)==1;k=next(iter(kset));la=set();mu=set()
    for i,j in itertools.combinations(V,2):
        c=len(set(G[i])&set(G[j]));(la if G.has_edge(i,j) else mu).add(c)
    assert len(la)==len(mu)==1;return len(V),k,next(iter(la)),next(iter(mu))

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();Q,partner=d.cqs(adj);P=d.pairs(partner);assert len(P)==45
    pair_index={frozenset(x):i for i,x in enumerate(P)};support=[frozenset(Q[a]|Q[c]) for a,c in P]
    # On each quotient pair B, the two lifts of a fixed D4 see the share/cross7 relations once each,
    # while cross4 occurs in paired lifts. Verify objectwise.
    pattern=Counter();G32=nx.Graph();G12=nx.Graph();G32.add_nodes_from(range(45));G12.add_nodes_from(range(45))
    for x,y in itertools.combinations(range(45),2):
        rel=Counter(d.relation(Q,adj,a,c) for a in P[x] for c in P[y]);pattern[tuple(sorted(rel.items()))]+=1
        if rel==Counter({(1,3):2,(0,7):2}):G32.add_edge(x,y)
        elif rel==Counter({(0,4):4}):G12.add_edge(x,y)
        else:raise AssertionError(rel)
    assert srg(G32)==(45,32,22,24);assert srg(G12)==(45,12,3,3)
    assert set(G32.edges())|set(G12.edges())==set(itertools.combinations(range(45),2)) and not(set(G32.edges())&set(G12.edges()))
    # Support interpretation: disjoint 8-point supports are the degree-12 graph.
    assert all(G12.has_edge(i,j)==support[i].isdisjoint(support[j]) for i,j in itertools.combinations(range(45),2))
    # Spectral quotient from Pass7179 P matrix: partner-even rows are dimensions 1,20,24.
    quotient_P=[[1,32,12],[1,-4,3],[1,2,-3]];mult=[1,20,24]
    out={'schema':'w33.pass7328.d4_antipodal_tritangent_fusion.v1','status':'PASS','D4_vertices':90,'antipodal_pairs':45,
      'partner_even_dimensions':[1,20,24],'partner_odd_dimensions':[15,30],
      'quotient_relations':{'fused_share_plus_cross7':[45,32,22,24],'cross4':[45,12,3,3]},
      'quotient_eigenmatrix':quotient_P,'quotient_multiplicities':mult,
      'objectwise':'The degree-12 quotient relation is exactly disjointness of the 45 eight-point D4-pair/tritangent supports; its complement is the degree-32 overlap graph.',
      'theorem':'The 90-D4 rank-five scheme is an antipodal two-fold refinement of the 45-tritangent association scheme. Passing to partner-even functions deletes the 15+30 odd sectors and leaves exactly the canonical 1+20+24 tritangent permutation module.',
      'module_bridge':'This makes the Pass7184 [45,21,5]=1+V20 and [45,24,6]=V24 code split the two nontrivial even eigenspaces of the D4 antipodal quotient.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','quotient':'1+20+24','graphs':['45,32,22,24','45,12,3,3']}))
if __name__=='__main__':main()
