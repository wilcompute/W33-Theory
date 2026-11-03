#!/usr/bin/env python3
"""Outside W33/Pascal: deterministic all-face Apollonian growth.

A local face-replacement rule without geometric coordinates produces
a connected planar triangular disk and high-degree hubs, not a four-dimensional
Lorentzian manifold. Control for overclaiming 'dimension from refinement'.
"""
from pathlib import Path
import json,networkx as nx,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_apollonian_growth_dimension_null.json"
def grow(level):
    G=nx.Graph()
    G.add_edges_from([(0,1),(1,2),(2,0)])
    faces=[(0,1,2)]
    nxt=3
    for step in range(level):
        new=[]
        for a,b,c in faces:
            m=nxt;nxt+=1
            G.add_edges_from(((a,m),(b,m),(c,m)))
            new.extend(((a,b,m),(b,c,m),(c,a,m)))
        faces=new
    return G,faces
def run():
    cases=[]
    for n in range(1,8):
        G,faces=grow(n)
        V=G.number_of_nodes();E=G.number_of_edges()
        assert V==(3**n+5)//2
        assert E==3*V-6
        assert len(faces)==3**n
        assert V-E+len(faces)==1
        assert nx.is_connected(G)
        planar,_=nx.check_planarity(G)
        assert planar
        sample=[min(G),V//3,2*V//3,V-1]
        low=max(nx.eccentricity(G,v) for v in sample)
        exact=nx.diameter(G) if V<=367 else None
        if exact is not None:assert exact>=low
        maxdeg=max(dict(G.degree()).values())
        assert maxdeg>3 if n>=2 else maxdeg>=3
        cases.append({"level":n,"vertices":V,"edges":E,"triangular_faces":len(faces),
           "planar":planar,"Euler_disk_chi":V-E+len(faces),
           "max_vertex_degree":maxdeg,
           "diameter_exact_if_small":exact,
           "diameter_sample_lower_bound":low,
           "coordinate_system_supplied":False})
    assert all(cases[i+1]['max_vertex_degree']>cases[i]['max_vertex_degree'] for i in range(6))
    out={"status":"PASS_ALTERNATIVE_LOCAL_GRAPH_GROWTH_TOPOLOGY_AND_HUB_NO_GO",
      "growth_rule":"Start a triangle disk. Synchronously replace each triangular face with three triangles by inserting one new center vertex and connecting it to all three corners; no embedding coordinates or 4D target are used in the update.",
      "exact_invariants":"After n iterations: faces=3^n, V=(3^n+5)/2, E=3V-6, Euler chi=V-E+F=1. Every graph is planar; topology remains a 2-dimensional triangulated disk.",
      "levels":cases,
      "dimension_selection_obstruction":"Self-similar, coordinate-free local refinement plus exponential vertex growth does not imply four Lorentzian dimensions. This specific rule stays a 2D simplicial disk at every finite level, generates increasing high-degree hub sites, and has no physical causal cone or massless spin-two constraint.",
      "comparison_to_causal_diamond":"Unlike sprinkling (which assumes Minkowski dimension), the rule takes only a starting triangle and combinatorial replacement. But it selects 2D triangular topology through its face rule. Neither candidate creates the intended 3+1 structure from no extra assumptions.",
      "scope":"A simple explicit growth-rule negative control, not an exhaustive classification of all coordinate-free graph or causal-set dynamics."
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("GROWTH",[(x["level"],x["vertices"],x["max_vertex_degree"],x["diameter_exact_if_small"]) for x in cases])
if __name__=="__main__":run()
