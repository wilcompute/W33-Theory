"""Geometry of the 20-apartment integral cycle relation as a 2-cell boundary."""
import json,sys
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261008_global_cycle_center_census import cycles
from w33_20261008_six_toe_frontier_followthrough import levi_graph
C=cycles(); g=levi_graph()
d=json.loads((R/"data/w33_20261008_cycle_center_atlas_constructive.json").read_text())
h=json.loads((R/"data/w33_20261008_cycle_atlas_homology_rank.json").read_text())
ids=d["largest_found_cycle_indices"]
v=Counter();e=Counter();es=Counter();u=Counter()
for i,(cid,w) in enumerate(zip(ids,h["primitive_integral_relation_coefficients"])):
 if not w: continue
 c=C[cid]
 for x in c:v[x]+=1
 for x,y in zip(c,c[1:]+c[:1]):
  edge=(min(x,y),max(x,y))
  e[edge]+=1
  es[edge]+=w*(1 if x<40 else -1)
assert not any(es.values())
print("FACES",sum(w!=0 for w in h["primitive_integral_relation_coefficients"]))
print("EDGE_APPEARANCE",dict(Counter(e.values())),"VERTEX_FACE_INCIDENCE",dict(Counter(v.values())))
print("V,E,F",len(v),len(e),20,"EULER",len(v)-len(e)+20)
print("EDGE_ORIENTATION_BALANCED",not any(es.values()))
