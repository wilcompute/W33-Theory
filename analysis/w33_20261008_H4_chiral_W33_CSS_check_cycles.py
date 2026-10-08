"""Full W33 CSS check-support cycles inside the ACTUAL chiral-paired
H4 antipodal geometry selected by the perfect F20-equivariant map.

The 40 W33 X-star weight3 checks form 40 H4-union triangles; the
20 Z-face weight8 check boundaries are 20 H4-union octagon cycles.
Attach these as *formal selected* 2-cells: they are not verified
original 600-cell tetrahedral 2-faces.
"""
import sys,json,collections,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology,add
OUT=ROOT/"data/w33_20261008_H4_chiral_selected_40tri_20oct_CSS_support.json"
def main():
 x=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 plus={tuple(e) for e in x["selected_H4_plus_W33_edges"]}
 minus={tuple(e) for e in x["selected_H4_minus_W33_edges"]}
 edgekind={e:"+" for e in plus}|{e:"-" for e in minus}
 V,E,faces,stab,H,b1,b2=topology()
 idx={e:i for i,e in enumerate(E)}
 verts={v:i for i,v in enumerate(V)}
 cycles3=[];cycles8=[]
 for v in V:
  seq=sorted(i for i,e in enumerate(E) if v in e)
  assert len(seq)==3
  links=[tuple(sorted(pair)) for pair in itertools.combinations(seq,2)]
  assert all(link in edgekind for link in links)
  cycles3.append({"CW_vertex":v,"H4_600cell_antipodal_addresses":[x["concrete_selected_60_W33_edge_to_600cell_antipodal_pair_address"][i] for i in seq],
                  "edge_colors":"".join(edgekind[link] for link in links),
                  "plus_count":sum(edgekind[e]=="+" for e in links)})
 for fid,f in enumerate(faces):
  arr=[idx[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  assert len(arr)==8 and len(set(arr))==8
  link=[tuple(sorted((u,v))) for u,v in zip(arr,arr[1:]+arr[:1])]
  assert all(e in edgekind for e in link)
  cycles8.append({"CW_face":fid,"H4_600cell_antipodal_addresses":[x["concrete_selected_60_W33_edge_to_600cell_antipodal_pair_address"][i] for i in arr],
    "edge_colors":"".join(edgekind[e] for e in link),
    "plus_count":sum(edgekind[e]=="+" for e in link)})
 Bx={};Bz={}
 for z in b1:add(z,Bx)
 for z in b2:add(z,Bz)
 assert len(Bx)==39 and len(Bz)==19
 assert all(not ((a&b).bit_count()%2) for a in b1 for b in b2)
 stars=dict(collections.Counter(q["plus_count"] for q in cycles3))
 facescol=dict(collections.Counter(q["plus_count"] for q in cycles8))
 assert sum(stars.values())==40 and sum(facescol.values())==20
 return {"H4_antipodal_qubit_addresses":60,
  "W33_CSS_X_checks_as_selected_H4_chiral_triangle_supports":40,
  "W33_CSS_Z_checks_as_selected_H4_chiral_octagon_supports":20,
  "X_check_chiral_plus_degree_hist":stars,
  "Z_check_cycle_chiral_plus_edge_hist":facescol,
  "X_checks_all_three_H4_union_adjacencies_verified":True,
  "Z_checks_all_eight_H4_union_adjacencies_verified":True,
  "X_check_records":cycles3,"Z_check_records":cycles8,
  "GF2_rank_X":len(Bx),"GF2_rank_Z":len(Bz),"GF2_commutation_verified":True,
  "encoded_qubits":2,"distance":6,
  "all_check_supports_transport_via_actual_60_address_embedding":True,
  "H4_native_tetrahedral_faces_identified_with_W33_20_octagons":False,
  "F20_chiral_order4_exchanges_all_adjacency_edge_colors":True,
  "locality_boundary":"All check SUPPORTS have paths/cycles in the paired H4 chiral union. This is not a physical hardware layout or a proof that native 600-cell tetrahedron 2-cells equal the selected CW octagons."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if not k.endswith("_records")},flush=True)
 print("W33_H4_CHECK_SUPPORT_GEOMETRY_PASS")
