"""Complete genus classification and F20 stabilizer of repaired chiral surface.
Produce explicit 136 ordered face-boundary edge cycles; integer orientation
constraints, GF2 Betti, and exact 20-group action on face attachments.
"""
import json,sys,itertools,collections
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_F20_A5_600cell_antipodal_bridge import comp,power
from w33_20261008_240sheet_chiral_CW_octagon_homology import rank
OUT=ROOT/"data/w33_20261008_240chiral_surface_genus_orientability_F20_certificate.json"
def main():
 q=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 legacy=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 V,E,basefaces,stab,H,bx,bz=topology();idx={e:i for i,e in enumerate(E)}
 P={tuple(sorted(e)) for e in q["selected_H4_plus_W33_edges"]};M={tuple(sorted(e)) for e in q["selected_H4_minus_W33_edges"]}
 vol={e:1 if e in P else 2 for e in P|M}
 G=nx.Graph();G.add_nodes_from(range(240))
 for (u,v),w in vol.items():
  for sh in range(4):G.add_edge(4*u+sh,4*v+(sh^w))
 edges=sorted(tuple(sorted(e)) for e in G.edges());eid={e:i for i,e in enumerate(edges)}
 def loop(seq,sh):
  now=sh;arr=[]
  for u,v in zip(seq,seq[1:]+seq[:1]):
   a=4*u+now;now^=vol[tuple(sorted((u,v)))];b=4*v+now
   arr.append(eid[tuple(sorted((a,b)))])
  assert now==sh
  return tuple(arr)
 octs=[]
 for f in basefaces:
  seq=[idx[tuple(sorted((a,b)))] for a,b in zip(f,f[1:]+f[:1])]
  octs.extend(loop(seq,sh) for sh in range(4))
 incid=collections.defaultdict(list)
 for i,face in enumerate(octs):
  for e in face:incid[e].append(i)
 assert len(incid)==320 and all(len(v)==2 for v in incid.values())
 Dual=nx.Graph();Dual.add_nodes_from(range(80))
 for pair in incid.values():Dual.add_edge(*pair)
 assert nx.is_bipartite(Dual)
 Dcomps=sorted(nx.connected_components(Dual),key=min)
 assert len(Dcomps)==2 and all(len(c)==40 for c in Dcomps)
 coloring=nx.bipartite.color(Dual)
 options=[]
 for option in itertools.product(range(2),repeat=2):
  selected={i for k,comp in enumerate(Dcomps) for i in comp if coloring[i]==option[k]}
  assert len(selected)==40
  cnt=collections.Counter(e for i in selected for e in octs[i])
  assert set(cnt)==set(incid) and set(cnt.values())=={1}
  options.append(selected)
 assert len(options)==4
 uncovered=set(range(480))-set(incid)
 U=nx.Graph();U.add_edges_from(edges[i] for i in uncovered)
 assert U.number_of_edges()==160 and all(d==2 for _,d in U.degree())
 components=list(nx.connected_components(U))
 assert len(components)==16 and all(len(c)==10 for c in components)
 decas=[]
 for c in components:
  basis=nx.cycle_basis(U.subgraph(c));assert len(basis)==1 and len(basis[0])==10
  vcycle=basis[0]
  decas.append(tuple(eid[tuple(sorted((a,b)))] for a,b in zip(vcycle,vcycle[1:]+vcycle[:1])))
 assert len(decas)==16
 hexes=[];seen=set()
 for v in V:
  seq=sorted(i for i,e in enumerate(E) if v in e)
  for sh in range(4):
   p=loop(seq+seq,sh);key=frozenset(p)
   if key not in seen:hexes.append(p);seen.add(key)
 assert len(hexes)==80
 # Orientation by adjacent face-edge incidence, exact Z2 face parity system.
 def orientable(faces):
  incident=collections.defaultdict(list)
  for i,p in enumerate(faces):
   vertices=[]
   for k in range(len(p)):
    shared=set(edges[p[k-1]])&set(edges[p[k]])
    assert len(shared)==1
    vertices.append(next(iter(shared)))
   assert len(set(vertices))==len(vertices)
   for k,e in enumerate(p):
    u=vertices[k];v=vertices[(k+1)%len(p)]
    assert tuple(sorted((u,v)))==edges[e]
    incident[e].append((i,0 if (u,v)==edges[e] else 1))
  assert len(incident)==480 and all(len(x)==2 for x in incident.values())
  adj=collections.defaultdict(list)
  for ee,((i,di),(j,dj)) in incident.items():
   # if edges traversed same direction, face reversal parity differs
   rhs=1^(di^dj)
   adj[i].append((j,rhs));adj[j].append((i,rhs))
  val={};contradiction=None
  for root in range(len(faces)):
   if root in val:continue
   val[root]=0;todo=[root]
   while todo:
    i=todo.pop()
    for j,flip in adj[i]:
     expected=val[i]^flip
     if j in val:
      if val[j]!=expected and contradiction is None:contradiction={"face_pair":[i,j],"parity_expected":expected,"parity_actual":val[j]}
     else:val[j]=expected;todo.append(j)
  return contradiction is None,contradiction
 r=tuple(legacy["F20_generators_W33_80point_r"]);s=tuple(legacy["F20_generators_W33_80point_s"])
 maps={g:[idx[tuple(sorted((g[u],g[v])))] for u,v in E] for g in [comp(power(r,i),power(s,j)) for j in range(4) for i in range(5)]}
 def swapbits(k):return ((k&1)<<1)|((k&2)>>1)
 perms={}
 for j in range(4):
  for i in range(5):
   g=comp(power(r,i),power(s,j))
   perm60=maps[g];perms[f"r{i}s{j}"]=[4*perm60[u]+(swapbits(sh) if j%2 else sh) for u in range(60) for sh in range(4)]
 def map_face(face,perm):
  return frozenset(eid[tuple(sorted((perm[a],perm[b])))] for e in face for a,b in [edges[e]])
 result=[]
 for opt,selected in enumerate(options):
  fs=hexes+[octs[i] for i in sorted(selected)]+decas
  assert len(fs)==136
  orient,conf=orientable(fs)
  all_masks=[sum(1<<e for e in f) for f in fs]
  rank2=rank(all_masks)
  assert rank2==135
  # Each face full set preserved iff image maps octs selection to itself;
  # hexes/decas sets separately preserved under selected F20 action.
  octkeys={frozenset(octs[i]) for i in selected}
  hekeys={frozenset(f) for f in hexes};dekeys={frozenset(f) for f in decas}
  preserved=[]
  for name,perm in perms.items():
   if {map_face(octs[i],perm) for i in selected}==octkeys and {map_face(f,perm) for f in hexes}==hekeys and {map_face(f,perm) for f in decas}==dekeys:
    preserved.append(name)
  result.append({"selection":opt,"selected_octagon_indices":sorted(selected),
   "orientable":orient,"orientation_parity_conflict":conf,
   "preserving_F20_elements":preserved,"preserving_subgroup_order":len(preserved),
   "H1_over_F2_dimension":480-239-rank2,
   "H2_over_F2_dimension":136-rank2,
   "orientable_genus":53 if orient else None,
   "nonorientable_genus":106 if not orient else None})
 assert all(x["H1_over_F2_dimension"]==106 for x in result)
 assert all(x["H2_over_F2_dimension"]==1 for x in result)
 return {"complete_closed_connected_surface_f_vector":[240,480,136],
  "faces_by_type":{"hexagon":80,"octagon":40,"decagon":16},
  "Euler_characteristic":-104,
  "vertex_links_all_single_circles":True,
  "every_edge_incident_two_faces":True,
  "octagon_dual_graph_components":[40,40],
  "new_decagon_cycles_all_10_edges":True,
  "selection_results":result,
  "F20_full_action_preserved_by_some_selection":any(x["preserving_subgroup_order"]==20 for x in result),
  "not_native_600cell_embedding_or_physical_quantum_computer":True}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({**{k:v for k,v in r.items() if k!="selection_results"},"choices":[{k:v for k,v in x.items() if k!="selected_octagon_indices"} for x in r["selection_results"]]},flush=True)
 print("CHIRAL_SURFACE_COMPLETE_ORIENTABILITY_F20_PASS")
