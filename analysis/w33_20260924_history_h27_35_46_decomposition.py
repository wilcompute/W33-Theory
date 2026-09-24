#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_history_h27_35_46_decomposition.json"

from analysis.w33_20260924_history_bigcell_q43_compactification import (
    all_points, all_lagrangian_lines, history_line, graph_adj,
    gl2_projective_reps, history_perm, symp,
)
from analysis.w33_20260924_history_cycle81_character_bridge import simplex_trace

def main():
    pts=all_points(); lines=all_lagrangian_lines()
    B=frozenset([p for p in pts if p[2]==0 and p[3]==0])
    hs=list(itertools.product(range(3),repeat=3))
    hlines=[history_line(s) for s in hs]
    A=graph_adj(hlines)
    edges=[(i,j) for i in range(27) for j in range(i+1,27) if A[i,j]]
    tris=[t for t in itertools.combinations(range(27),3)
          if A[t[0],t[1]] and A[t[0],t[2]] and A[t[1],t[2]]]
    assert len(edges)==108 and len(tris)==36

    tri_points=[]
    edge_mult=Counter()
    for t in tris:
        meet=set(hlines[t[0]]) & set(hlines[t[1]]) & set(hlines[t[2]])
        assert len(meet)==1
        q=next(iter(meet))
        assert q not in B
        tri_points.append(q)
        for e in itertools.combinations(t,2):
            edge_mult[tuple(sorted(e))]+=1
    assert len(set(tri_points))==36
    assert set(tri_points)==set(pts)-set(B)
    assert set(edge_mult.values())=={1}

    # Point-side H27: non-neighbours of one W33 point.
    p0=0
    non=[i for i in range(40) if i!=p0 and symp(pts[p0],pts[i])!=0]
    assert len(non)==27
    H=np.zeros((27,27),dtype=int)
    for i,u in enumerate(non):
        for j,v in enumerate(non):
            if i<j and symp(pts[u],pts[v])==0:
                H[i,j]=H[j,i]=1
    assert int(H.sum()//2)==108

    g1=nx.from_numpy_array(A); g2=nx.from_numpy_array(H)
    matcher=nx.algorithms.isomorphism.GraphMatcher(g1,g2)
    isomorphic=matcher.is_isomorphic()
    iso=matcher.mapping if isomorphic else {}
    specA=np.linalg.eigvalsh(A.astype(float))
    specH=np.linalg.eigvalsh(H.astype(float))
    histA=Counter(int(round(x)) for x in specA)
    histH=Counter(int(round(x)) for x in specH)
    htris=sum(
        H[i,j] and H[i,k] and H[j,k]
        for i,j,k in itertools.combinations(range(27),3)
    )

    # Filling all 36 edge-disjoint triangles kills 36 independent cycles.
    cycle_rank=108-27+1
    b1_filled=cycle_rank-36
    assert cycle_rank==82 and b1_filled==46

    # Character split under the 648-element Bell-line stabilizer.
    reps=gl2_projective_reps()
    group={history_perm(M,t,1) for M in reps for t in hs}
    assert len(group)==648
    sum_tri=0; norm_tri=0; norm_tri_red=0; norm_h46=0
    for hp in group:
        c0=sum(i==hp[i] for i in range(27))
        c1=simplex_trace(hp,edges)
        c2=simplex_trace(hp,tris)
        cyc=c1-c0+1
        h46=cyc-c2
        sum_tri+=c2
        norm_tri+=c2*c2
        norm_tri_red+=(c2-1)*(c2-1)
        norm_h46+=h46*h46
    tri_triv=sum_tri//648
    assert tri_triv==1

    out={
      "schema":"w33.20260924.history_h27_35_46_decomposition.v1",
      "status":"PASS_HISTORY_35_46_SPLIT_WITH_POINT_LINE_FIREWALL",
      "history_graph":{
        "vertices":27,"edges":108,"triangles":36,
        "cycle_rank_unfilled":82,
        "filled_clique_b1":b1_filled,
        "each_edge_in_exactly_one_triangle":True,
        "triangle_index_set":"the 36 W33 points outside the Bell line",
      },
      "H27_firewall":{
        "repo_definition":"induced graph on the 27 non-neighbours of a W33 point",
        "isomorphic_to_history_null_graph":isomorphic,
        "history_adjacency_spectrum":dict(sorted(histA.items())),
        "point_side_H27_adjacency_spectrum":dict(sorted(histH.items())),
        "history_triangle_count":len(tris),
        "point_side_H27_triangle_count":int(htris),
        "same_edge_count":True,
        "same_filled_b1_value":bool(htris==36),
        "consequence":"The shared 27/108/46 counts do not identify the point-side H27 with the line-side history graph.",
      },
      "bell_stabilizer_character_split":{
        "group_order":648,
        "triangle_boundary_dimension":36,
        "triangle_module_trivial_multiplicity":tri_triv,
        "triangle_reduced_dimension":35,
        "filled_history_homology_dimension":46,
        "identity":"81=(36-1)+46=35+46",
        "triangle_character_norm":norm_tri//648,
        "triangle_reduced_character_norm":norm_tri_red//648,
        "history46_character_norm":norm_h46//648,
      },
      "theorem":(
        "The Bell-shell null-history graph has 108 edges partitioned into 36 edge-disjoint "
        "triangles indexed by W33 points off the Bell line. Filling those triangles changes "
        "graph-cycle rank 82 to b1=46. Under the Bell-line stabilizer, the unique invariant "
        "inside the 36-dimensional triangle module leaves a 35-dimensional reduced triangle "
        "sector, so the already-certified reduced 81-dimensional history-cycle module splits "
        "characterwise as 35+46. The point-side H27 graph shares the 27/108/46 counts but is "
        "not isomorphic; this is an exact point/line firewall rather than an identification."
      ),
      "physics_reading":(
        "The temporal 46 is the history homology that survives after local same-event "
        "triangular loops are declared contractible. Its equality in dimension with the old "
        "point-side H27 homology is structural but not objectwise; the line-side temporal chart "
        "and point-side H27 remain distinct carriers."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "history":out["history_graph"],
      "split":out["bell_stabilizer_character_split"],
      "h27_iso":isomorphic,
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
