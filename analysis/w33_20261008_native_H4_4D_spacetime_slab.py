"""Actual 4D simplicial spacetime TOPOLOGY from native 600-cell S3.

Triangulate S3 x [0,1] by a global vertex-ordered staircase subdivision
of each of the 600 native tetrahedra x interval into 4 pentachora.
Explicitly verify face incidences, both 600-tetra S3 boundaries, Euler
characteristic zero, mod2 relative fundamental top-chain and rank(d4).
This does not equip the slab with a Lorentzian metric or ADM constraints.
"""
from pathlib import Path
import sys,itertools,collections,json
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/"analysis"))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
from w33_20261008_native_H4_Regge_S3 import rank
OUT=ROOT/"data/w33_20261008_native_H4_4D_S3_time_slab_staircase_certificate.json"
def main():
 V=build_600cell();A=build_adjacency(np.array(V),120)
 g=nx.Graph();g.add_nodes_from(range(120))
 g.add_edges_from((i,j) for i in range(120) for j in range(i+1,120) if A[i][j])
 tets=sorted(tuple(c) for c in nx.enumerate_all_cliques(g) if len(c)==4)
 assert len(tets)==600
 s4=[]
 for tet in tets:
  for cut in range(4):
   p=tuple([v for v in tet[:cut+1]]+[v+120 for v in tet[cut:]])
   assert len(set(p))==5
   s4.append(tuple(sorted(p)))
 assert len(s4)==2400 and len(set(s4))==2400
 faces=[set() for _ in range(5)]
 for s in s4:
  for k in range(1,6):
   for c in itertools.combinations(s,k):faces[k-1].add(c)
 fs=[len(v) for v in faces]
 assert fs[0]==240 and fs[-1]==2400
 chi=sum((-1)**k*val for k,val in enumerate(fs))
 assert chi==0
 tfaces=collections.Counter(f for simplex in s4 for f in itertools.combinations(simplex,4))
 assert set(tfaces.values())=={1,2}
 boundary={f for f,v in tfaces.items() if v==1}
 Btm={tuple(v for v in tet) for tet in tets}
 Top={tuple(v+120 for v in tet) for tet in tets}
 assert boundary==Btm|Top and not (Btm&Top)
 assert len(boundary)==1200
 facet_index={f:i for i,f in enumerate(sorted(tfaces))}
 d4=[sum(1<<facet_index[face] for face in itertools.combinations(tet,4)) for tet in s4]
 assert rank(d4)==2400
 total=0
 for b in d4:total^=b
 expected=sum(1<<facet_index[f] for f in boundary)
 assert total==expected
 # Each 4-simplex has 5 tetra facets, and every triangle occurs twice
 # in the 4-simplex's tetrahedral boundary (d3*d4=0).
 for tet in s4:
  tr=collections.Counter(t for f in itertools.combinations(tet,4) for t in itertools.combinations(f,3))
  assert set(tr.values())=={2}
 return {"native_H4_spatial_S3_tetrahedra":600,
  "spacetime_product_topology":"S3 x [0,1]",
  "time_slices":2,"vertices_per_slice":120,
  "4D_simplicial_f_vector":fs,
  "Euler_char":chi,
  "4D_staircase_4simplices":len(s4),
  "4D_tetrahedral_facets_total":len(tfaces),
  "boundary_native_S3_tetrahedra_each_slice":600,
  "boundary_tetrahedral_facets_total":len(boundary),
  "all_interior_tetra_facets_incident_on_2_4simplices":True,
  "only_boundary_tetra_facets_at_t0_and_t1":True,
  "boundary_map_d4_GF2_rank":rank(d4),
  "relative_fundamental_4_chain_boundary_equals_t0_plus_t1_S3":True,
  "boundary_square_zero_GF2_verified":True,
  "global_vertex_order_used_for_prismatic_triangulation":True,
  "global_order_may_not_be_F20_equivariant_as_simplicial_triangulation":True,
  "not_physical_Lorentzian_metric_or_4D_Einstein_Regge_action":True,
  "lapse_shift_ADM_constraint_algebra_not_derived":True,
  "boundary":"Explicit true 4D simplicial product cobordism; time-slice topology alone does not specify causality, edge lengths, dynamical spacetime or quantum-gravitational coupling."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("H4_4D_SPACETIME_SLAB_TOPOLOGY_PASS")
