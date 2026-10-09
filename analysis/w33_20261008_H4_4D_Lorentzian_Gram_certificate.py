"""Nondegenerate Lorentzian 4-simplices on the exact H4 S3xI slab.

For every edge in triangulated prism slab, set squared interval
s(e)=a^2 for same-slice; s(e)=-T^2 for cross-slice.
Use 4x4 vertex-based Lorentzian Gram 2G_ij=s_0i+s_0j-s_ij
to check inertia (3+,1-) in ALL 2400 pentachora; all triangle
hinges spatial (+,+) or timelike (+,-). No dihedral deficits, EOM or ADM
constraint algebra proved.
"""
from pathlib import Path
import sys,itertools,json,collections,math
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import build_600cell,build_adjacency
OUT=ROOT/"data/w33_20261008_H4_Lorentzian_4simplex_metric_signature.json"
def sq(u,v,a,tau):
 if u==v:return 0.
 return a*a if (u//120)==(v//120) else -tau*tau
def gram(nodes,a,tau):
 zero=nodes[0]
 return np.array([[(sq(zero,i,a,tau)+sq(zero,j,a,tau)-sq(i,j,a,tau))/2 for j in nodes[1:]] for i in nodes[1:]],dtype=float)
def main():
 v=build_600cell();adj=build_adjacency(np.array(v),120);g=nx.Graph();g.add_nodes_from(range(120))
 g.add_edges_from((i,j) for i in range(120) for j in range(i+1,120) if adj[i][j])
 tet=sorted(tuple(x) for x in nx.enumerate_all_cliques(g) if len(x)==4)
 pentachora=[tuple(sorted(tuple(t[:k+1])+tuple(x+120 for x in t[k:]))) for t in tet for k in range(4)]
 assert len(pentachora)==2400
 tris={f for s in pentachora for f in itertools.combinations(s,3)}
 edges={e for s in pentachora for e in itertools.combinations(s,2)}
 classified=collections.Counter((sum(x<120 for x in z),sum(x>=120 for x in z)) for z in tris)
 counts=collections.Counter((sum(x<120 for x in z),sum(x>=120 for x in z)) for z in pentachora)
 assert counts=={(4,1):600,(3,2):600,(2,3):600,(1,4):600}
 assert sum(classified.values())==6240
 face_incidence=collections.Counter(f for sm in pentachora for f in itertools.combinations(sm,3))
 mixed_incidence=collections.Counter(face_incidence[f] for f in tris if len({i//120 for i in f})==2)
 spatial_incidence=collections.Counter(face_incidence[f] for f in tris if len({i//120 for i in f})==1)
 assert sum(mixed_incidence.values())==3840
 assert sum(spatial_incidence.values())==2400
 cases=[]
 for tau in (.1,.5,1.0,2.0,10.0):
  rec=collections.defaultdict(list)
  for s in pentachora[:4]:pass
  # Test every simplex, not only representative types.
  for sm in pentachora:
   G=gram(sm,1.,tau)
   e=np.linalg.eigvalsh(G)
   positive=int(np.sum(e>1e-9));negative=int(np.sum(e< -1e-9))
   assert (positive,negative)==(3,1),(tau,sm,e)
   det=float(np.linalg.det(G))
   assert det< -1e-10
   rec[(sum(u<120 for u in sm),sum(u>=120 for u in sm))].append(math.sqrt(-det)/24)
  assert all(max(vols)-min(vols)<1e-10 for vols in rec.values())
  cases.append({"tau_over_a":tau,"metric_signature_3spacelike_1timelike_all_2400":True,
    "4simplex_volume_by_slice_composition":{str(k):vols[0] for k,vols in rec.items()},
    "total_4volume":sum(sum(vols) for vols in rec.values())})
 # Symbolic classification of all four 4-simplex time-slice patterns.
 # Global squared edge intervals have spatial value 1 and temporal -u.
 import sympy as sp
 u=sp.symbols("u",positive=True)
 def sqsym(i,j):
  if i==j:return sp.Integer(0)
  return sp.Integer(1) if i//120==j//120 else -u
 det_polys={}
 for count0 in (1,2,3,4):
  arr=list(range(count0))+list(range(120,120+5-count0))
  q=arr[0]
  GG=sp.Matrix([[(sqsym(q,i)+sqsym(q,j)-sqsym(i,j))/2 for j in arr[1:]] for i in arr[1:]])
  det_polys[count0]=sp.factor(GG.det())
 expected={1:-(8*u+3)/16,2:-(12*u+7)/16,3:-(12*u+7)/16,4:-(8*u+3)/16}
 assert all(sp.simplify(det_polys[k]-expected[k])==0 for k in expected),det_polys
 # Since determinants are strictly negative for every u>0, and the
 # inertia is (3+,1-) at one positive u, it is so for ALL u>0.
 exact_dets={str(k):str(v) for k,v in det_polys.items()}
 for f in tris:
  G=gram(f,1.,1.)
  eigen=np.linalg.eigvalsh(G)
  if len(set(x//120 for x in f))==1:assert np.all(eigen>1e-9)
  else:assert eigen[0]< -1e-9<eigen[1]
 return {"two_spatial_time_slices":True,"spatial_vertex_labels_per_slice":120,
  "4simplex_count":2400,"4simplex_type_hist":{str(k):v for k,v in counts.items()},
  "Lorentzian_signature_cases":cases,
  "total_hinges_triangles":len(tris),"hinge_spacetime_type_hist":{str(k):v for k,v in classified.items()},
  "global_edges":len(edges),
  "mixed_interior_triangle_pentachoron_incidence_hist":dict(mixed_incidence),
  "pure_spatial_boundary_triangle_pentachoron_incidence_hist":dict(spatial_incidence),
  "mixed_timelike_hinge_area_per_triangle_at_a1":"sqrt(u+1/4)/2",
  "spatial_boundary_triangle_area_per_triangle_at_a1":"sqrt(3)/4",
  "total_mixed_hinge_area_at_a1":"1920*sqrt(u+1/4)",
  "total_pure_spatial_boundary_hinge_area_at_a1":"600*sqrt(3)",
  "exact_4simplex_Lorentzian_Gram_determinant_polynomials":exact_dets,
  "all_4simplices_Lorentzian_for_every_positive_tau_over_a":True,
  "exact_per_4simplex_4volume_by_type":"(1,4),(4,1):sqrt(8*u+3)/96 ; (2,3),(3,2):sqrt(12*u+7)/96, u=(tau/a)^2, a=1",
  "all_global_spatial_edges_squared_length":"a^2",
  "all_global_temporal_cross_edges_squared_length":"-tau^2",
  "all_4simplices_non_degenerate_Lorentzian_at_five_tau_values":True,
  "all_spatial_triangles_have_positive_definite_2metric":True,
  "all_mixed_triangles_have_signature_1plus_1minus":True,
  "no_regge_deficit_angles_or_Einstein_equations_derived":True,
  "no_ADM_hypersurface_deformation_algebra_derived":True,
  "global_ordered_prism_triangulation_need_not_preserve_full_F20_as_simplex_maps":True,
  "interpretation":"Concrete global consistent Lorentzian edge-square assignment and nondegenerate 4D simplices for selected tau values; test of local realizability, not a dynamical gravitational solution."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in r.items() if k!="Lorentzian_signature_cases"},flush=True)
 print("tau_cases",r["Lorentzian_signature_cases"],flush=True)
 print("H4_4D_LORENTZIAN_METRIC_INERTIA_PASS")
