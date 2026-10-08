"""Witness: one of exactly 120 F20-equivariant embeddings of the W33
60-edge qubit line graph into the *union* of the two 600-cell 60-address
chiral A5 normal Cayley graphs.

Construct an explicit abstract group isomorphism A5 on five labels to the
ACTUAL Clifford A5 on six labels by generators and all 60 Cayley relations.
Transport all 60 W33 edge labels to actual 600-cell antipodal pair indices.
Check every W33 adjacency is present in exactly one of H4+ and H4-,
and the order-four F20 map exchanges these edge colors.
"""
from pathlib import Path
import itertools,collections,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_F20_A5_600cell_antipodal_bridge import comp,order,power
from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,inverse
OUT=ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json"
def group_isomorphism(source,target):
 si=tuple(range(5));ti=tuple(range(6))
 A=next(g for g in source if order(g)==5)
 B=next(g for g in source if order(g)==3 and order(comp(A,g))==2)
 starget=next((a,b) for a in target if order(a)==5 for b in target if order(b)==3 and order(comp(a,b))==2)
 ta,tb=starget
 gens=[(A,ta),(B,tb),(inverse(A),inverse(ta)),(inverse(B),inverse(tb))]
 m={si:ti};queue=collections.deque([si])
 while queue:
  u=queue.popleft()
  for sg,tg in gens:
   v=comp(u,sg);w=comp(m[u],tg)
   if v in m:assert m[v]==w
   else:m[v]=w;queue.append(v)
 assert len(m)==60 and set(m.values())==set(target)
 for a,b in itertools.product(source,repeat=2):
  assert m[comp(a,b)]==comp(m[a],m[b])
 return m
def main():
 Emap=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 census=json.loads((ROOT/"data/w33_20261008_F20_48000_selectors_chiral_union_census.json").read_text())
 chiral=json.loads((ROOT/"data/w33_20261008_H4_A5_chiral_5cycle_normal_Cayley.json").read_text())
 assert int(census["intersection_size_histogram"]["120"])==120
 six=clifford_antipodal_permutations()
 # Full 600-cell 60 address label <-> 6-point group permutation.
 ix={p:i for i,p in six.items()}
 five=[tuple(g) for g in Emap["S5_coset_even_A5_permutations"]]
 iso=group_isomorphism(set(five),set(six.values()))
 map60=[ix[iso[five[i]]] for i in census["best_map_W33_to_A5_coset_index"]]
 assert len(set(map60))==60
 pos={tuple(g) for g in chiral["A5_neighbor_identity_permutations"]}
 neg={tuple(g) for g in chiral["mirror_A5_5cycle_identity_permutations"]}
 assert len(pos)==len(neg)==12 and not pos&neg
 V,E,F,stab,H,b1,b2=topology()
 idx={e:i for i,e in enumerate(E)}
 edges=set()
 for vi in V:
  touching=[idx[e] for e in E if vi in e]
  assert len(touching)==3
  for u,v in itertools.combinations(touching,2):edges.add(tuple(sorted((u,v))))
 assert len(edges)==120
 plus=set();minus=set()
 for u,v in edges:
  x,y=six[map60[u]],six[map60[v]]
  rel=comp(inverse(x),y)
  assert (rel in pos)^(rel in neg)
  (plus if rel in pos else minus).add((u,v))
 assert len(plus)+len(minus)==120
 # Verify actual 600cell class edges using prevalidated actual Cayley presentation.
 hist=collections.Counter()
 for i in range(60):
  p=sum(u==i or v==i for u,v in plus)
  n=sum(u==i or v==i for u,v in minus)
  assert p+n==4
  hist[(p,n)]+=1
 from w33_20261008_F20_A5_600cell_antipodal_bridge import comp as compose
 r=tuple(Emap["F20_generators_W33_80point_r"])
 s=tuple(Emap["F20_generators_W33_80point_s"])
 def moved(edge,g):
  u,v=edge
  a,b=E[u];c,d=E[v]
  return tuple(sorted((idx[tuple(sorted((g[a],g[b])))],idx[tuple(sorted((g[c],g[d])))])))
 assert {moved(e,r) for e in plus}==plus
 assert {moved(e,r) for e in minus}==minus
 assert {moved(e,s) for e in plus}==minus
 assert {moved(e,s) for e in minus}==plus
 return {"F20_equivariant_selectors_enumerated":48000,
  "perfect_selectors":int(census["intersection_size_histogram"]["120"]),
  "concrete_selected_60_W33_edge_to_600cell_antipodal_pair_address":map60,
  "every_W33_edge_qubit_adjacency_in_H4_chiral_class_union":True,
  "actual_600cell_plus_graph_incident_W33_edges":len(plus),
  "actual_600cell_minus_graph_incident_W33_edges":len(minus),
  "local_plus_minus_degree_hist":{str(k):v for k,v in hist.items()},
  "5point_to_6point_A5_group_isom_verified_all_3600_products":True,
  "selected_H4_plus_W33_edges":[list(x) for x in sorted(plus)],
  "selected_H4_minus_W33_edges":[list(x) for x in sorted(minus)],
  "order5_W33_normalizer_r_preserves_both_edge_colors":True,
  "order4_W33_normalizer_s_exchanges_two_edge_colors":True,
  "W33_60_edge_line_graph_is_4regular_spanning_subgraph_of_24regular_H4_pair_union":True,
  "W33_graph_is_not_the_entire_degree12_H4_plus_or_minus_graph":True,
  "geometry_boundary":"This is a genuine combinatorial incidence-preserving subgraph embedding into a 24-regular union on actual H4 antipodal coordinates, via an explicitly chosen A5 group iso. It does not embed W33 full 20 octagonal 2-cells, nor yield a canonical embedding into a single 600-cell chiral graph."}
if __name__=="__main__":
 out=main();OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in out.items() if k not in ("concrete_selected_60_W33_edge_to_600cell_antipodal_pair_address","selected_H4_plus_W33_edges","selected_H4_minus_W33_edges")},flush=True)
 print("H4_W33_F20_CHIRAL_4REGULAR_EXPLICIT_EMBEDDING_PASS")
