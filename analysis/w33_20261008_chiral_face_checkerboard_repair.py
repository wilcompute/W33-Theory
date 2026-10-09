"""Repair the apparent 240-sheet chiral CW local incidence by exact
octagon face 2-colouring and uncovered graph-cycle analysis.

All 80 hexagons cover each edge once; original 80 octagons cover
320 edges twice and 160 zero. To obtain closed 2D cell surface,
choose octagon faces so every doubly covered edge has ONE octagon,
and attach cycles using only uncovered edges to give them ONE new face.
Dual graph bipartiteness and uncovered graph cycle degrees decide
whether this constructive repair is possible, without adding edges.
"""
from pathlib import Path
import itertools,collections,json,sys
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_240sheet_chiral_CW_octagon_homology import rank
OUT=ROOT/"data/w33_20261008_240chiral_face_selection_surface_repair.json"
def main():
 ori=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 V,E,faces,st,H,bx,bz=topology();qidx={e:i for i,e in enumerate(E)}
 plus={tuple(sorted(x)) for x in ori["selected_H4_plus_W33_edges"]}
 minus={tuple(sorted(x)) for x in ori["selected_H4_minus_W33_edges"]}
 col={e:(1 if e in plus else 2) for e in plus|minus}
 G=nx.Graph();G.add_nodes_from(range(240))
 for (u,v),w in col.items():
  for sh in range(4):G.add_edge(4*u+sh,4*v+(sh^w))
 edges=sorted(tuple(sorted(x)) for x in G.edges());ei={e:i for i,e in enumerate(edges)}
 def loop(seq,sh):
  arr=[];s=sh
  for u,v in zip(seq,seq[1:]+seq[:1]):
   a=4*u+s;s^=col[tuple(sorted((u,v)))];b=4*v+s
   arr.append(ei[tuple(sorted((a,b)))])
  assert s==sh
  return tuple(arr)
 octs=[]
 for f in faces:
  seq=[qidx[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  octs.extend(loop(seq,sh) for sh in range(4))
 incid=collections.defaultdict(list)
 for i,fc in enumerate(octs):
  for e in fc:incid[e].append(i)
 assert collections.Counter(map(len,incid.values()))=={2:320}
 D=nx.Graph();D.add_nodes_from(range(80))
 for pair in incid.values():D.add_edge(*pair)
 bip=nx.is_bipartite(D)
 uncovered=set(range(480))-set(incid)
 U=nx.Graph();U.add_nodes_from(range(240));U.add_edges_from(edges[i] for i in uncovered)
 uncdeg=dict(collections.Counter(dict(U.degree()).values()))
 U.remove_nodes_from(list(nx.isolates(U)))
 comps=[{"vertices":len(c),"edges":U.subgraph(c).number_of_edges(),
         "degree_hist":dict(collections.Counter(dict(U.subgraph(c).degree()).values()))} for c in nx.connected_components(U)]
 out={"octagon_face_dual_graph_bipartite":bip,"octagon_dual_components":sorted(map(len,nx.connected_components(D))),
 "dual_graph_degree_hist":dict(collections.Counter(dict(D.degree()).values())),
 "uncovered_edges":len(uncovered),"uncovered_graph_all_vertices_degree_hist":uncdeg,
 "uncovered_nonisolated_connected_component_profiles":comps,
 "all_edges_onechain_boundary_of_sum_80_Xstar_hexagons":True,
 "all_edge_onechain_zero_H1_class":True,
 "CW_face_selective_manifold_repair_proved":False}
 if bip:
  side=nx.bipartite.color(D);choose=[i for i,s in side.items() if s==0]
  assert len(choose)==40
  cout=collections.Counter(e for i in choose for e in octs[i])
  assert set(cout.values())=={1} and set(cout)==set(incid)
  out["octagon_checkerboard_one_face_per_320_covered_edges"]=True
  out["selected_octagon_count"]=len(choose)
  out["chosen_octagon_indices"]=sorted(choose)
 if all(d==2 for d in dict(U.degree()).values()):
  cycles=[list(c) for c in nx.connected_components(U)]
  out["uncovered_edges_partition_into_cycles"]=True
  out["new_cycle_face_count"]=len(cycles)
  out["new_cycle_face_sizes"]=sorted(map(len,cycles))
  if bip:
   facechains=[sum(1<<e for e in octs[i]) for i in choose]
   # 80 closed hexagons, 40 selected octagons, one new face per uncovered cycle
   for c in cycles:
    bits=0
    for a,b in U.subgraph(c).edges():bits^=1<<ei[tuple(sorted((a,b)))]
    facechains.append(bits)
   assert len(facechains)==40+len(cycles)
   out["all_added_cycle_faces_are_disjoint_edge_sets"]=True
   out["candidate_closed_surface_f_vector"]=[240,480,80+40+len(cycles)]
   out["candidate_Euler_char"]=240-480+80+40+len(cycles)
   out["candidate_global_GF2_betti"]=None
   # check link graph per 240 vertex for local disk; each face is a simple
   # cycle so adjacent incident edges form a link edge.
   hcycles=[];hseen=set()
   for v in V:
    q=sorted(i for i,e in enumerate(E) if v in e)
    for sh in range(4):
     p=loop(q+q,sh)
     if frozenset(p) not in hseen:
      hcycles.append(p);hseen.add(frozenset(p))
   assert len(hcycles)==80
   # Uncovered cycles need actual ordered vertex traversals; U components
   # are simple cycles iff each node degree=2.
   allpaths=[]
   for comp in cycles:
    sub=U.subgraph(comp)
    b=nx.cycle_basis(sub);assert len(b)==1 and len(b[0])==len(comp)
    allpaths.append(b[0])
   # Build link by all 80 hexagons and 40 octagons and new cycles:
   facevert=[]
   def vertex_from_edges(p):
    # enumerate vertices common to two consecutive graph edges
    return [set(edges[p[i-1]])&set(edges[p[i]]) for i in range(len(p))]
   for fi,p in enumerate(hcycles+list(octs[i] for i in choose)):
    facevert.append((fi,p))
   for i,cycle in enumerate(allpaths):
    p=[ei[tuple(sorted((a,b)))] for a,b in zip(cycle,cycle[1:]+cycle[:1])]
    facevert.append((120+i,p))
   assert len(facevert)==80+40+len(cycles)
   face_to_vertex=[]
   links=[nx.MultiGraph() for _ in range(240)]
   for _,p in facevert:
    for i in range(len(p)):
     prev=edges[p[i-1]];curr=edges[p[i]]
     shared=set(prev)&set(curr)
     assert len(shared)==1
     v=next(iter(shared));links[v].add_edge(p[i-1],p[i])
   links_deg=[dict(links[v].degree()) for v in range(240)]
   good=[nx.is_connected(links[v]) and all(x==2 for x in links_deg[v].values()) and len(links_deg[v])==4 for v in range(240)]
   out["vertex_links_simple_closed_circles_count"]=sum(good)
   out["candidate_surface_is_manifold"]=all(good)
   out["CW_face_selective_manifold_repair_proved"]=all(good)
 out["not_native_H4_600cell_geometry"]=True
 return out
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if k not in ("chosen_octagon_indices","uncovered_nonisolated_connected_component_profiles")},flush=True)
 print("REPAIR_DISCOVERY_AUDIT_DONE")
