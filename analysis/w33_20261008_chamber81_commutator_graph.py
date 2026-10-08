#!/usr/bin/env python3
"""The 81 apartments through a chamber as a candidate rank-81 commutator Cayley graph.

Exact adjacency/common-neighbor/spectrum checks. This does not infer a
group isomorphism merely from the numbers 81 and 32.
"""
import sys,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_global_cycle_center_census import cycles
from w33_20261008_six_toe_frontier_followthrough import levi_graph
OUT=ROOT/"data"/"w33_20261008_chamber81_commutator_graph.json"

def analyze():
 c=cycles();G=levi_graph()
 edge=tuple(sorted(G.edges()))[0]
 rows=[(i,set(x)) for i,x in enumerate(c) if all(y in x for y in edge)]
 assert len(rows)==81
 A=np.zeros((81,81),dtype=np.int64)
 hist=Counter()
 for i,(_,x) in enumerate(rows):
  for j,(_,y) in enumerate(rows[i+1:],start=i+1):
   s=x&y; pp=sum(z<40 for z in s);ll=sum(z>=40 for z in s)
   hist[f"p{pp}_l{ll}"]+=1
   A[i,j]=A[j,i]=int(pp!=ll)
 deg=Counter(map(int,A.sum(axis=1)))
 common=A@A
 edge_common=Counter(int(common[i,j]) for i in range(81) for j in range(i+1,81) if A[i,j])
 nonedge_common=Counter(int(common[i,j]) for i in range(81) for j in range(i+1,81) if not A[i,j])
 vals=np.linalg.eigvalsh(A.astype(float))
 eig=Counter(str(round(float(z),8)) for z in vals)
 out={"fixed_chamber_vertices":list(edge),"rank81_apartments":81,
      "degree_histogram":dict(deg),
      "edge_common_neighbor_histogram":dict(edge_common),
      "nonedge_common_neighbor_histogram":dict(nonedge_common),
      "adjacency_eigenvalue_multiplicity":dict(eig),
      "spectral_extrema":[float(vals.min()),float(vals.max())],
      "intersection_signatures":dict(hist),
      "is_SRG_81_32_13_12": deg==Counter({32:81}) and edge_common==Counter({13:1296}) and nonedge_common==Counter({12:1944}),
      "note":"81 apartments through a chamber are a known Steinberg basis (BT744). This is NEW center-commutator adjacency on that carrier; no Cayley-group identification established"}
 return out
if __name__=="__main__":
 x=analyze()
 OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(json.dumps(x,indent=2),flush=True)
 print("CHAMBER81_GRAPH_PASS",flush=True)
