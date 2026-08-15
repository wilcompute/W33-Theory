#!/usr/bin/env python3
"""Pass5348c: identify the q=5 footprint hull with the binary adjacency code of NO_5^+(5).

The 325 q5 P-components are polar pairs H union H^perp of non-isotropic lines.
Join two carriers when their 12-point W-supports meet in two points. The resulting
carrier graph is the strongly regular graph with parameters (325,144,68,60),
the standard NO_5^+(5) graph.

Let C_F be the q5 point-footprint row code [325,65,25] and H=C_F cap C_F^perp
its 64-dimensional doubly-even hull. This producer proves
  H = Row_F2(A_NO5),
by independently building both spaces and comparing ranks. Since all three SRG
parameters k,lambda,mu are even, A^2=0 over F2, so the graph adjacency code is
self-orthogonal. This gives a graph-code model for the Hoffman shortening, which
Pass5243 embeds into H.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5348C_Q5_HULL_NO5_GRAPH_CODE.json'

def rank(rows):
    piv={}
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def main():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    assert {len(B) for B in blocks}=={12}
    # Point-footprint rows.
    F=[]
    for p in range(156):
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        F.append(z)
    assert rank(F)==65 and {x.bit_count() for x in F}=={25}
    hull=[]
    for p in range(1,156):hull.append(F[0]^F[p])
    assert rank(hull)==64
    # Carrier graph: intersection two.
    adj=[]
    for i,A in enumerate(blocks):
        z=0
        for j,B in enumerate(blocks):
            if i!=j and len(A&B)==2:z|=1<<j
        adj.append(z)
    assert {x.bit_count() for x in adj}=={144}
    # Full SRG check via bit intersections.
    pair_hist={True:set(),False:set()}
    for i in range(325):
        for j in range(i+1,325):
            pair_hist[bool((adj[i]>>j)&1)].add((adj[i]&adj[j]).bit_count())
    assert pair_hist[True]=={68} and pair_hist[False]=={60}
    rA=rank(adj);rH=rank(hull);rU=rank(adj+hull)
    assert (rA,rH,rU)==(64,64,64)
    # Direct A^2=0 check: all row pair dot products, including diagonal, are even.
    assert all((adj[i]&adj[j]).bit_count()%2==0 for i in range(325) for j in range(i,325))
    out={'pass':'5348c','status':'THEOREM_Q5_FOOTPRINT_HULL_EQUALS_NO5PLUS5_BINARY_ADJACENCY_CODE',
      'carrier_graph':{'vertices':325,'degree':144,'lambda':68,'mu':60,'standard_name':'NO_5^+(5)'},
      'footprint_code':'C_F=[325,65,25]_2','hull_dimension':64,
      'adjacency_code_dimension':rA,'combined_span_dimension':rU,
      'identity':'Hull(C_F)=Row_F2(A_NO5+5)',
      'self_orthogonality':'A^2=0 over F2 because k=144, lambda=68, mu=60 are all even; verified directly from all row dot products.',
      'hoffman_bridge':'Pass5243 proves every [312,52,d] Hoffman-13 shortened word lies in the footprint hull, hence in this NO_5^+(5) adjacency code.',
      'boundary':'This identifies the ambient 64-dimensional graph code. It does not by itself prove its minimum distance or the Hoffman shortened distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
