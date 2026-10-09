"""Native-H4 obstruction and antipodal lift for selected 40 X-check triangles.

The + 12-regular H4 Cayley relation is ACTUAL 600cell nearest-neighbor
adjacency; the - chiral relation is disjoint MIRROR adjacency.
The selected W33 20 octagons each have 2,4,6 + edges and none all+.
Thus no selected octagon is a native H4 1-skeleton cycle under this
embedding. This does not obstruct abstract 2-chiral union CW supports.
"""
from pathlib import Path
import sys,json,collections,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
from w33_clifford_antipodal_spread_incidence_bridge import antipodal_pair_index
OUT=ROOT/"data/w33_20261008_H4_native_cycle_antipodal_lift_obstruction.json"
def main():
 c=json.loads((ROOT/"data/w33_20261008_H4_chiral_selected_40tri_20oct_CSS_support.json").read_text())
 ps=antipodal_pair_index();A=build_adjacency(np.array(build_600cell()),120)
 fibers=collections.defaultdict(list)
 for v,p in ps.items():fibers[p].append(v)
 assert len(fibers)==60 and set(map(len,fibers.values()))=={2}
 def cycle_lift(path):
  n=len(path);has=[]
  for i in range(n):
   p,q=path[i],path[(i+1)%n]
   aa=[(u,v) for u in fibers[p] for v in fibers[q] if A[u][v]]
   has.append(aa)
  if any(not row for row in has):return {"native":False}
  assert all(len(row)==2 for row in has)
  start=fibers[path[0]][0];x=start
  for j in range(n):
   x=next(v for u,v in has[j] if u==x)
  return {"native":True,"closed_n_cycle":x==start,"lift_cycle_length":n if x==start else 2*n}
 X=c["X_check_records"];Z=c["Z_check_records"]
 triangles=[cycle_lift(x["H4_600cell_antipodal_addresses"]) for x in X]
 octs=[cycle_lift(x["H4_600cell_antipodal_addresses"]) for x in Z]
 cnt=collections.Counter(("native_closed" if v.get("closed_n_cycle") else "native_nontrivial_deck") if v["native"] else "non_native" for v in triangles)
 assert cnt["non_native"]==30
 assert all(not z["native"] for z in octs)
 assert all(row["plus_count"] in (2,4,6) for row in Z)
 plusall=[k for k,x in enumerate(X) if x["plus_count"]==3]
 assert len(plusall)==10
 return {"actual_600cell_native_plus_relation_degree":12,
  "600cell_mirror_minus_relation_disjoint_from_original_edges":True,
  "selected_W33_X_check_triangles":40,
  "X_triangles_all_plus_actual_H4_edges":10,
  "X_triangle_actual_120vertex_lift_classification":dict(cnt),
  "X_triangle_all_plus_records":[{"check":i,**triangles[i]} for i in plusall],
  "selected_W33_Z_octagons":20,
  "Z_octagons_with_all_eight_original_H4_edges":0,
  "Z_octagons_with_mixed_plus_minus_edge_counts":dict(collections.Counter(z["plus_count"] for z in Z)),
  "no_native_600cell_2face_lift_of_selected_W33_octagon_boundaries_for_this_selector":True,
  "not_exclusion_of_other_119_perfect_selectors_or_nonstandard_H4_face_relations":True,
  "geometry_boundary":"Native 600-cell edge graph is only the + relation; the chiral-paired PLUS-UNION-MINUS graph needed for the W33 support embedding is a different 24-regular graph."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k!="X_triangle_all_plus_records"},flush=True)
 print("H4_NATIVE_CYCLE_OBSTRUCTION_PASS")
