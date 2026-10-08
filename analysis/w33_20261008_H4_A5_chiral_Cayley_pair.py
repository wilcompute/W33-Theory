"""H4 antipodal 60-graph is precisely one chiral A5 5-cycle normal Cayley graph.

Find the other 12-element 5-cycle class and demonstrate all 120
S6-normalizer automorphisms of Clifford A5; outer automorphisms
exchange the two 12-regular Cayley graphs, while inner preserve each.
C5 normalizer's C4 modular generator acts as chiral selector exchange
on A5 order5 classes, not as same-graph H4 geometry automorphism.
"""
from pathlib import Path
import sys,json,itertools,collections,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"));sys.path.insert(0,str(ROOT))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
from w33_clifford_antipodal_spread_incidence_bridge import antipodal_pair_index
from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,compose,inverse,permutation_order
OUT=ROOT/"data/w33_20261008_H4_A5_chiral_5cycle_normal_Cayley.json"
def main():
 grp=clifford_antipodal_permutations();p2i={v:k for k,v in grp.items()}
 V=build_600cell();adj=build_adjacency(np.array(V),len(V));pair=antipodal_pair_index()
 edges={tuple(sorted((pair[u],pair[v]))) for u in range(120) for v in range(u+1,120) if adj[u][v]}
 assert len(edges)==360
 ide=p2i[tuple(range(6))]
 NS={grp[j if u==ide else u] for u,j in edges if u==ide or j==ide}
 assert len(NS)==12
 prof=collections.Counter(permutation_order(p) for p in NS)
 assert prof=={5:12},prof
 def conjugacy(g):
  return {compose(compose(h,g),inverse(h)) for h in grp.values()}
 assert all(conjugacy(g)==NS for g in NS)
 other={g for g in grp.values() if permutation_order(g)==5}-NS
 assert len(other)==12
 assert set(compose(g,g) for g in NS)==other
 assert set(inverse(g) for g in NS)==NS
 # Exact graph edge reconstruction from left Cayley action
 reconstructed={tuple(sorted((label,p2i[compose(p,g)]))) for label,p in grp.items() for g in NS}
 assert reconstructed==edges
 # Find all normalizing permutations in S6.
 normalizers=[]
 G=set(grp.values())
 for h in itertools.permutations(range(6)):
  inv=inverse(h)
  if all(compose(compose(h,p),inv) in G for p in G):
   normalizers.append(h)
 assert len(normalizers)==120
 inners=[];outers=[];observed=collections.Counter()
 for h in normalizers:
  im={compose(compose(h,g),inverse(h)) for g in NS}
  assert im==NS or im==other
  observed["preserves" if im==NS else "exchanges"]+=1
  (inners if im==NS else outers).append(h)
 assert len(inners)==len(outers)==60
 # Element of order4 in outer coset normalizing a fixed 5-cycle
 r=next(iter(NS));witness=None
 for h in outers:
  if permutation_order(h)==4 and compose(compose(h,r),inverse(h))==compose(r,r):
   witness=h;break
 assert witness is not None
 # Non-geometric outer automorphism on this exact antipodal 600cell graph:
 perm={k:p2i[compose(compose(witness,p),inverse(witness))] for k,p in grp.items()}
 moved={tuple(sorted((perm[i],perm[j]))) for i,j in edges}
 assert not moved.intersection(edges) # two disjoint chiral 12-regular relations
 # Characterize overlap and distinct chiral spectra (isomorphic).
 return {"actual_H4_600cell_antipodal_address_count":60,
  "H4_edges":360,"H4_degree":12,
  "H4_neighbors_of_identity_are_A5_5cycles":True,
  "H4_neighbor_generators_count":12,
  "H4_5cycle_generators_closed_under_A5_conjugation":True,
  "H4_5cycle_generators_inverse_closed":True,
  "H4_adj_exactly_normal_Cayley_graph_A5_class_5a":True,
  "other_5cycle_class_size":12,
  "squares_of_neighbor_generators_equal_other_5cycle_class":True,
  "S6_normalizer_of_Clifford_A5_size":120,
  "S6_inner_normalizers_preserve_chiral_H4_graph":60,
  "S6_outer_normalizers_exchange_two_H4_graph_relations":60,
  "order4_normalizer_witness_S6_permutation":list(witness),
  "order4_witness_conjugates_order5_r_to_r_squared":True,
  "order4_outer_maps_original_360_edges_to_disjoint_mirror_360_edges":True,
  "two_chiral_neighbor_class_edge_sets_disjoint":True,
  "A5_neighbor_identity_permutations":[list(g) for g in sorted(NS)],
  "mirror_A5_5cycle_identity_permutations":[list(g) for g in sorted(other)],
  "not_identification_with_W33_degree4_graph":True,
  "not_physical_parity_or_spacetime_chirality_derived":True,
  "limits":"Exact A5 group/600-cell antipodal Cayley presentation. Outer automorphism is a discrete graph-exchange map, not an ordinary symmetry preserving the chosen H4 12-regular graph or a physical parity transformation."}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k not in ("A5_neighbor_identity_permutations","mirror_A5_5cycle_identity_permutations")},flush=True)
 print("H4_A5_TWO_CHIRAL_CAYLEY_GRAPHS_PASS")
