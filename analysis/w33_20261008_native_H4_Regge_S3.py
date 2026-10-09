"""Native 600-cell boundary triangulates an explicit piecewise-flat S3:
combinatorial chain ranks and equilateral 3D Regge curvature.

All tetrahedra are enumerated as K4 cliques of the ACTUAL H4
120-vertex adjacency, not assumed from nominal facet count.
Regge curvature is a legitimate *3D spatial* discrete gravitational
functional, but no time/lapse/shift, 4D spacetime or ADM brackets.
"""
from pathlib import Path
import sys,math,itertools,json,collections
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
OUT=ROOT/"data/w33_20261008_600cell_native_Regge_S3_chain_certificate.json"
def rank(cols):
 pivots={}
 for v in cols:
  x=v
  while x:
   j=x.bit_length()-1
   if j in pivots:x^=pivots[j]
   else:pivots[j]=x;break
 return len(pivots)
def main():
 vv=build_600cell();AA=build_adjacency(np.array(vv),len(vv))
 g=nx.Graph();g.add_nodes_from(range(120))
 g.add_edges_from((i,j) for i in range(120) for j in range(i+1,120) if AA[i][j])
 assert g.number_of_edges()==720 and set(dict(g.degree()).values())=={12}
 faces=sorted(tuple(c) for c in nx.enumerate_all_cliques(g) if len(c)==3)
 tets=sorted(tuple(c) for c in nx.enumerate_all_cliques(g) if len(c)==4)
 assert len(faces)==1200 and len(tets)==600
 assert all(len(c)==4 for c in tets)
 fidx={f:i for i,f in enumerate(faces)}
 edges=sorted(g.edges());eidx={e:i for i,e in enumerate(edges)}
 counts=collections.Counter(e for tet in tets for e in itertools.combinations(tet,2))
 assert set(counts.values())=={5}
 tri_count=collections.Counter(t for tet in tets for t in itertools.combinations(tet,3))
 assert set(tri_count.values())=={2}
 d1=[(1<<u)|(1<<v) for u,v in edges]
 d2=[sum(1<<eidx[e] for e in itertools.combinations(f,2)) for f in faces]
 d3=[sum(1<<fidx[f] for f in itertools.combinations(t,3)) for t in tets]
 assert all(rank([x])==1 for x in d3)
 for y in d3:
  boundary=0
  for i in range(len(faces)):
   if y>>i&1:boundary^=d2[i]
  assert boundary==0
 rk1=rank(d1);rk2=rank(d2);rk3=rank(d3)
 assert (rk1,rk2,rk3)==(119,601,599),(rk1,rk2,rk3)
 delta=2*math.pi-5*math.acos(1/3)
 assert 0<delta<.2
 # 3D Regge-Hilbert spatial scalar curvature ∫sqrt(g) R = 2 * sum_edges length * deficit.
 # Regge action S_spatial = sum_edges a delta - lambda * sum_tets Vol(tet)
 # Volume reg tetra sqrt(2)/12 a^3.
 Rint_per_a=2*720*delta
 stationarity_lambda_a_squared=720*delta/(150*math.sqrt(2))
 return {
  "native_600cell_f_vector":[120,720,1200,600],
  "boundary_topological_dimension":3,"Euler_char":120-720+1200-600,
  "tetrahedra_incident_on_each_edge":5,
  "tetrahedra_incident_on_each_triangular_face":2,
  "GF2_cellular_boundary_ranks":[rk1,rk2,rk3],
  "GF2_homology_betti_numbers":[1,0,0,1],
  "boundary_square_zero_GF2":True,
  "regular_euclidean_tetrahedron_dihedral_angle_radians":math.acos(1/3),
  "native_edge_Regge_deficit_radians":delta,
  "native_spatial_integrated_scalar_curvature_per_unit_edge_length":Rint_per_a,
  "regular_tetrahedron_volume_for_edge_a":"sqrt(2)*a^3/12",
  "total_tetrahedron_volume_for_edge_a":"50*sqrt(2)*a^3",
  "equilateral_regge_spatial_action":"S(a)=720*a*(2pi-5 acos(1/3)) - 50*sqrt(2)*Lambda*a^3",
  "minisuperspace_stationary_relation":"Lambda*a^2 = 24*(2pi-5 acos(1/3))/(5*sqrt(2))",
  "Lambda_times_a_squared_at_stationary_relation":stationarity_lambda_a_squared,
  "not_full_Einstein_Regge_equations":True,
  "not_Lorentzian_4D_or_ADM_hypersurface_brackets":True,
  "no_GR_recovery_from_W33_or_physical_metric_measured":True}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(x,flush=True);print("NATIVE_H4_SPATIAL_REGGE_PASS")
