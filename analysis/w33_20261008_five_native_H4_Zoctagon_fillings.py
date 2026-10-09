"""Actual 120-vertex lift of five native 600-cell octagons from
a maximally native F20 perfect chiral-pair selector.

Construct GF2 2-chain fillings in original H4 triangular face complex,
with boundary equal to actual lifted 8- or 16-edge cycle. This shows
actual homological filling, not single native 2-cell identification.
"""
from pathlib import Path
import sys,json,itertools,collections
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"));sys.path.insert(0,str(ROOT))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_W33_H4_chiral_4regular_embedding import group_isomorphism
from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations
from w33_20261008_native_H4_Regge_S3 import rank
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
from w33_clifford_antipodal_spread_incidence_bridge import antipodal_pair_index
OUT=ROOT/"data/w33_20261008_five_native_H4_Z_octagon_GF2_surface_fillings.json"
def main():
 v=json.loads((ROOT/"data/w33_20261008_all120_perfect_F20_selectors_native_H4_face_nogo.json").read_text())["first_five_face_native_selector"]
 orig=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 five=[tuple(x) for x in orig["S5_coset_even_A5_permutations"]]
 six=clifford_antipodal_permutations();ix={g:i for i,g in six.items()}
 iso=group_isomorphism(set(five),set(six.values()))
 mapped=[ix[iso[five[j]]] for j in v["coset_address_map_W33_60qubits"]]
 inversepair=collections.defaultdict(list)
 ps=antipodal_pair_index()
 for a,p in ps.items():inversepair[p].append(a)
 assert set(map(len,inversepair.values()))=={2}
 adj=build_adjacency(np.array(build_600cell()),120)
 G=nx.Graph();G.add_nodes_from(range(120));G.add_edges_from((a,b) for a in range(120) for b in range(a+1,120) if adj[a][b])
 edges=sorted(tuple(sorted(e)) for e in G.edges());eidx={e:j for j,e in enumerate(edges)}
 faces=sorted(tuple(t) for t in nx.enumerate_all_cliques(G) if len(t)==3)
 boundaries=[]
 for f in faces:
  boundaries.append(sum(1<<eidx[tuple(sorted(e))] for e in itertools.combinations(f,2)))
 # row reduction for full native H4 triangular boundary map:
 pivots={}
 for j,vec in enumerate(boundaries):
  x=vec;w=1<<j
  while x:
   k=x.bit_length()-1
   if k in pivots:
    x^=pivots[k][0];w^=pivots[k][1]
   else:pivots[k]=(x,w);break
 assert len(pivots)==601
 def fill(cycle):
  x=cycle;w=0
  while x:
   k=x.bit_length()-1
   assert k in pivots
   x^=pivots[k][0];w^=pivots[k][1]
  return [j for j in range(len(faces)) if w>>j&1]
 V,E,C,stab,H,b1,b2=topology();W={e:i for i,e in enumerate(E)}
 records=[]
 for fid in v["native_face_indices"]:
  fc=C[fid]
  arr=[mapped[W[tuple(sorted((u,v)))]] for u,v in zip(fc,fc[1:]+fc[:1])]
  assert len(set(arr))==8
  start=min(inversepair[arr[0]])
  path=[start];pos=start
  for p in arr[1:]+[arr[0]]:
   target=next(k for k in inversepair[p] if adj[pos][k])
   path.append(target);pos=target
  if pos!=start:
   # Continue on opposite sheet to close 16-vertex lift.
   for p in arr[1:]+[arr[0]]:
    target=next(k for k in inversepair[p] if adj[pos][k])
    path.append(target);pos=target
  assert pos==start
  assert len(path)-1 in (8,16)
  mask=0
  for a,b in zip(path,path[1:]):
   mask^=1<<eidx[tuple(sorted((a,b)))]
  assert mask.bit_count()==len(path)-1
  fchain=fill(mask)
  test=0
  for j in fchain:test^=boundaries[j]
  assert test==mask
  records.append({"face_index":fid,"quotient_address_cycle":arr,
    "native_120vertex_lift_length":len(path)-1,
    "native_120vertex_lift_closed_vertices":path,
    "GF2_native_H4_triangle_filling_count":len(fchain),
    "native_600cell_triangle_indices_in_exact_filling":fchain,
    "exact_boundary_verified":True})
 assert len(records)==5
 return {"maximally_native_F20_selected_faces":5,
  "lift_lengths_histogram":dict(collections.Counter(r["native_120vertex_lift_length"] for r in records)),
  "native_H4_triangle_boundary_rank":len(pivots),
  "native_face_lift_and_surface_fill_records":records,
  "all_lifted_boundaries_fill_by_native_H4_triangles_GF2":True,
  "single_native_H4_triangle_identical_to_W33_octagon":False,
  "these_5_of_20_do_not_prove_full_W33_CW_embedding":True,
  "geometric_scope":"Five native quotient cycles lift to explicit closed 8/16-edge cycles on 600-cell 120-vertex graph; each admits a GF2 2-chain of native triangles. The remaining fifteen W33 octagons involve nonnative mirror-graph edges."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k!="native_face_lift_and_surface_fill_records"},flush=True)
 print([{"face":r["face_index"],"length":r["native_120vertex_lift_length"],"filling":r["GF2_native_H4_triangle_filling_count"]} for r in x["native_face_lift_and_surface_fill_records"]],flush=True)
 print("NATIVE_H4_FIVE_OCTAGON_HOMOLOGICAL_FILL_PASS")
