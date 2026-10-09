"""F20-equivariant Z2^2 chiral-voltage lift of W33 60-qubit line graph.

Each W33 edge is + or - in actual paired H4 antipodal Cayley relations.
Assign Z2^2 voltages (1,0) and (0,1). All W33 octagon checks have
even color counts: lift to four closed 8-cycles. All 40 triangle
checks have odd total cycle length: lift to 6-cycles, never triangles.
F20 generator r preserves colors; s swaps colors and voltage axes,
making a canonical semilinear F20 action on the FOUR sheet formal
cover. No claim that this is a native 600cell 4-fold cover.
"""
from pathlib import Path
import json,sys,collections,itertools
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_F20_A5_600cell_antipodal_bridge import comp,power
OUT=ROOT/"data/w33_20261008_F20_chiral_Z2square_240voltage_cover.json"
def main():
 orig=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 w0=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 V,E,faces,stab,H,b1,b2=topology()
 idx={tuple(e):i for i,e in enumerate(E)}
 pp={tuple(sorted(e)) for e in orig["selected_H4_plus_W33_edges"]}
 mm={tuple(sorted(e)) for e in orig["selected_H4_minus_W33_edges"]}
 edgevolt={e:(1 if e in pp else 2) for e in pp|mm}
 assert len(edgevolt)==120 and len(pp)==len(mm)==60
 G=nx.Graph();G.add_nodes_from(range(240))
 for (u,v),c in edgevolt.items():
  for a in range(4):G.add_edge(u*4+a,v*4+(a^c))
 assert G.number_of_edges()==480 and set(dict(G.degree()).values())=={4}
 comp_sizes=sorted(map(len,nx.connected_components(G)))
 def winding(seq):
  vol=0
  for u,v in zip(seq,seq[1:]+seq[:1]):vol^=edgevolt[tuple(sorted((u,v)))]
  return vol
 stars=[]
 for v in V:
  s=[i for i,e in enumerate(E) if v in e]
  assert len(s)==3
  stars.append(winding(s))
 octs=[]
 for f in faces:
  s=[idx[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  assert len(s)==8
  octs.append(winding(s))
 assert all(v==0 for v in octs)
 assert len(set(stars))==2 and set(stars)=={1,2}
 assert collections.Counter(stars)=={1:20,2:20}
 r=tuple(w0["F20_generators_W33_80point_r"]);s=tuple(w0["F20_generators_W33_80point_s"])
 perms={}
 for key,p,swap in (("r",r,False),("s",s,True)):
  f=[idx[tuple(sorted((p[u],p[v])))] for u,v in E]
  def bitswap(a):return ((a&1)<<1)|((a&2)>>1)
  action=[f[u]*4+(bitswap(a) if swap else a) for u in range(60) for a in range(4)]
  assert len(set(action))==240
  mapped={tuple(sorted((action[u],action[v]))) for u,v in G.edges()}
  assert mapped==set(map(tuple,map(sorted,G.edges())))
  perms[key]=action
 def apply(p,x):return p[x]
 assert all(apply(perms["r"],apply(perms["r"],apply(perms["r"],apply(perms["r"],apply(perms["r"],i)))))==i for i in range(240))
 assert all((lambda ss:ss==i)((lambda x:perms["s"][perms["s"][perms["s"][perms["s"][x]]]])(i)) for i in range(240))
 sinv=[0]*240
 for i,j in enumerate(perms["s"]):sinv[j]=i
 assert all(perms["s"][perms["r"][sinv[i]]]==perms["r"][perms["r"][i]] for i in range(240))
 return {"base_qubit_vertices":60,"base_line_adjacency_edges":120,
  "formal_chiral_Z2square_cover_vertices":G.number_of_nodes(),
  "formal_cover_edges":G.number_of_edges(),"formal_cover_degree":4,
  "connected_component_sizes":comp_sizes,
  "octagon_face_count":20,"octagon_voltages_hist":dict(collections.Counter(octs)),
  "all_W33_20_Z_checks_lift_as_closed_eight_cycles_on_all_four_sheets":True,
  "X_star_triangle_count":40,"X_star_triangle_voltages_hist":dict(collections.Counter(stars)),
  "all_40_W33_star_triangles_lift_as_length_six_not_length_three":True,
  "F20_C5_generator_preserves_voltage_basis":True,
  "F20_C4_generator_swaps_voltage_bits":True,
  "both_generators_act_as_true_240vertex_graph_automorphisms":True,
  "F20_generator_order_r":5,"F20_generator_order_s":4,
  "F20_relation_s_r_sinv_equals_r_squared_verified_on_240_vertices":True,
  "not_native_600cell_120vertex_cover":True,
  "not_CSS_check_faces_attached_or_native_gravity":True,
  "mathematical_scope":"Canonical colored voltage cover for this selected F20-equivariant W33 chiral adjacency. Formal 240-address graph; four sheets not a native H4 physical vertex representation. Cycles checked combinatorially."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(x,flush=True);print("F20_CHIRAL_240_SHEET_COVER_PASS")
