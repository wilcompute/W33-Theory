#!/usr/bin/env python3
"""A parameter-free S3 triangle Wilson-action on Pascal/W33 graphs.

Nontrivial holonomy is a *declared* microscopic edge connection, not physical
Yang-Mills dynamics. Unit Wilson deficit is normalized by the 40-point W33
permutation representation; no lattice coupling is inferred.
"""
from __future__ import annotations
import runpy,json
from pathlib import Path
from collections import Counter
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
A=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_w33_s3_holonomy.py"))
OUT=ROOT/"data"/"2026_11_03_pascal_w33_triangle_wilson.json"
def triangles(G):
    res=[]
    for a in G:
      for b in G[a]:
        if b<=a:continue
        for c in G[b]:
          if c<=b:continue
          if G.has_edge(a,c):res.append((a,b,c))
    return res

def run():
    assert len(A["S3"])==6
    trans=[x for x in A["S3"] if x!=A["ID"] and A["mul"](x,x)==A["ID"]]
    assert len(trans)==3
    fix={sum(i==p[i] for i in range(40)) for p in (A["Wperm"][t] for t in trans)}
    assert fix=={8}
    rows=[]
    for n in (1,2,3,4):
        G,lab=A["build"](n)
        T=triangles(G)
        assert len(T)==(21*6**(n-1)-1)//5
        census=Counter()
        for u,v,w in T:
            h=A["mul"](A["mul"](lab[frozenset((u,v))],lab[frozenset((v,w))]),
                         lab[frozenset((w,u))])
            assert h in trans
            census[str(h)]+=1
            # loop basepoint change conjugates; fixed-point trace invariant
            assert sum(i==A["Wperm"][h][i] for i in range(40))==8
        rows.append({"level":n,"triangles":len(T),
                    "flux_group_order":2,
                    "w33_wilson_trace_each_plaquette":8,
                    "normalized_wilson_action_sum":4*len(T)/5,
                    "conjugacy_histogram":dict(census)})
    bridges=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_schur_rg_exact.py"))["block_bridges"]()
    B=nx.Graph()
    B.add_edges_from(bridges)
    assert len(triangles(B))==1
    res={
     "status":"PASS_NONABELIAN_TRIANGLE_WILSON_CENSUS",
     "triangle_recursion":"T_(n+1)=6*T_n+1 with T_1=4; T_n=(21*6^(n-1)-1)/5",
     "recursion_proof":"At each scale six disjoint copies are connected by nine unit bonds. Their corner vertices are nonadjacent within every child level>=1; therefore any new triangle lies entirely within the bond graph, whose unique triangle is checked directly. Thus exactly one cross-block triangle is added.",
     "holonomy_law":"Every elementary triangular three-edge loop carries the product of three barycentric-coordinate transpositions; it is a transposition of order 2. All transpositions have W33 permutation trace 8 (32 nonfixed points), independent of local gauge.",
     "wilson_action_density":"Tr(I-U_triangle)/40=32/40=4/5; sum per level =4*T_n/5 with chosen standard dimensionless normalization.",
     "zero_mode_implication":"Full S3 holonomy gives 12 covariantly constant 40-fiber sections, versus 40 for trivial/pure-gauge transport; no physical mass or coupling follows.",
     "physical_scope":"A graph-connection Wilson observable and a gauge-invariant benchmark. A Yang-Mills field would require independent dynamical link variables, a coupling/action and observables; this construction specifies a background connection.",
     "checks":rows
    }
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS ELEMENTARY S3 FLUX / W33 TRACE",[(r["level"],r["triangles"],r["w33_wilson_trace_each_plaquette"]) for r in rows])
    return res
if __name__=="__main__":run()
