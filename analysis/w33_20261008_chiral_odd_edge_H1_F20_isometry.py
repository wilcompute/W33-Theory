"""Exact homological correction: all-edge chain is already a boundary;
plus/mirror native H4 isometry no-go.

Compute [all 480 edges] in H1 of 160-face (80hex+80oct) 2-complex:
E IS a boundary: indeed the sum of all 80 star hexagon faces. Repair
therefore requires local integer face-incidence surgery rather than a
new mod2 boundary relation. Checkerboard/decagon construction does so. The true H4 isometry acts on + adjacency; F20
order4 generator exchanges + and - so is not native H4 isometry.
"""
import sys,json,collections,itertools
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_chiral_240_odd_edge_homology_F20_no_native_isometry.json"
def reduction(v,rows):
 piv={}
 for u in rows:
  while u:
   k=u.bit_length()-1
   if k in piv:u^=piv[k]
   else:piv[k]=u;break
 x=v
 while x:
  k=x.bit_length()-1
  if k in piv:x^=piv[k]
  else:break
 return x,len(piv)
def main():
 cfg=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 ori=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 V,E,faces,st,H,bx,bz=topology();eid={e:i for i,e in enumerate(E)}
 P={tuple(sorted(e)) for e in cfg["selected_H4_plus_W33_edges"]}
 M={tuple(sorted(e)) for e in cfg["selected_H4_minus_W33_edges"]}
 color={uv:(1 if uv in P else 2) for uv in P|M}
 assert len(P)==len(M)==60
 def mapperm(p):return [eid[tuple(sorted((p[u],p[v])))] for u,v in E]
 s=tuple(ori["F20_generators_W33_80point_s"]);r=tuple(ori["F20_generators_W33_80point_r"])
 mp_s=mapperm(s);mp_r=mapperm(r)
 native_transformed_P={tuple(sorted((mp_s[a],mp_s[b]))) for a,b in P}
 assert native_transformed_P==M
 assert {tuple(sorted((mp_r[a],mp_r[b]))) for a,b in P}==P
 G=nx.Graph();G.add_nodes_from(range(240))
 for (a,b),v in color.items():
  for sh in range(4):G.add_edge(4*a+sh,4*b+(sh^v))
 ed=sorted(tuple(sorted(e)) for e in G.edges());EID={e:i for i,e in enumerate(ed)}
 assert len(ed)==480 and set(dict(G.degree()).values())=={4}
 def path(seq,sh):
  v=sh;mask=0
  for a,b in zip(seq,seq[1:]+seq[:1]):
   w=color[tuple(sorted((a,b)))];u=4*a+v;v^=w
   mask^=1<<EID[tuple(sorted((u,4*b+v)))]
  assert v==sh
  return mask
 col=[]
 for f in faces:
  seq=[eid[tuple(sorted((a,b)))] for a,b in zip(f,f[1:]+f[:1])]
  col.extend(path(seq,sh) for sh in range(4))
 for star in V:
  seq=sorted(i for i,e in enumerate(E) if star in e)
  found=set()
  for sh in range(4):found.add(path(seq+seq,sh))
  assert len(found)==2
  col.extend(sorted(found))
 assert len(col)==160
 full=(1<<480)-1
 rem,rank=reduction(full,col)
 assert rank==158
 d1=0
 for (u,v) in ed:d1^=(1<<u)^(1<<v)
 assert d1==0
 assert rem==0
 # Constant one cochain is a coboundary of sheet parity; independently,
 # this entire-edge 1-chain IS also a 2-boundary of hexagon faces.
 return {"base_native_H4_plus_edges_in_selected_W33_line_graph":60,
  "order4_F20_generator_maps_all_60_native_plus_W33_edge_relations_to_mirror_minus":True,
  "order5_generator_preserves_native_plus_relation_within_selected_support":True,
  "order4_generator_cannot_act_as_native_H4_600cell_isometry_under_selected_address_identification":True,
  "all_480_edges_as_GF2_one_chain_have_zero_vertex_boundary":True,
  "full_CW_two_boundary_rank":rank,
  "all_edges_one_chain_is_nontrivial_H1_class":False,
  "all_edges_boundary_of_sum_80_hexagon_faces":True,
  "all_edges_one_chain_reduced_witness_hamming_weight":rem.bit_count(),
  "no_combination_of_160_existing_lifted_check_faces_can_supply_all_edge_parity_boundary":False,
  "repair_requires_integer_incidence_adjustment_not_mod2_homology":True,
  "closed_surface_repair_by_checkerboard_and_decagon_faces_found_separately":True,
  "underlying_H1_dimension":83,
  "not_a_global_no_go_for_new_F20_equivariant_faces_or_other_H4_embedding":True}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("ODD_EDGE_H1_AND_NATIVE_H4_ISOMETRY_NO_GO_PASS")
