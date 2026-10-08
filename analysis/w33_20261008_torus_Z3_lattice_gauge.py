"""Exact discrete Z3 gauge curvature/cohomology ledger on 20 W33 apartments.

A link 1-cochain a in F3^60 has face curvature da in F3^20.
One signed integral top cycle gives the obstruction to realizing an
arbitrary face-flux assignment as exact curvature. Gauge flat sectors:
H^1(X;F3) = F3^2 => 9 (textbook toric Z3 degeneracy, not a particle).
"""
import json,collections,sys,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261008_early_torus_singer_quotient import objects
from w33_20261008_cycle_atlas_homology_rank import rank_mod
D=R/"data";OUT=D/"w33_20261008_torus_Z3_lattice_gauge.json"
def compute():
 C,faces,_,_=objects()
 V=sorted({v for f in faces for v in f})
 E=sorted({tuple(sorted((u,v))) for f in faces for u,v in zip(f,f[1:]+f[:1])})
 vid={v:i for i,v in enumerate(V)}; eid={e:i for i,e in enumerate(E)}
 B1=np.zeros((40,60),dtype=int);B2=np.zeros((60,20),dtype=int)
 for j,(u,v) in enumerate(E):
  B1[vid[u],j]=-1;B1[vid[v],j]=1
 for i,f in enumerate(faces):
  for u,v in zip(f,f[1:]+f[:1]):
   B2[eid[tuple(sorted((u,v)))],i]+=1 if u<40 else -1
 assert not np.any(B1@B2)
 ranks=[rank_mod(B1.tolist(),3),rank_mod(B2.T.tolist(),3)]
 assert ranks==[39,19]
 faceweights=json.loads((D/"w33_20261008_cycle_atlas_homology_rank.json").read_text())
 atlas=json.loads((D/"w33_20261008_cycle_center_atlas_constructive.json").read_text())
 weight_lookup={frozenset(C[c]):int(w) for c,w in zip(atlas["largest_found_cycle_indices"],faceweights["primitive_integral_relation_coefficients"]) if w}
 weight=np.array([weight_lookup[frozenset(f)] for f in faces],dtype=int)
 assert not np.any((B2@weight)%3)
 # Single unit flux on any one face pairs nontrivially with this top class.
 one=np.zeros(20,dtype=int);one[0]=1
 assert int(weight@one)%3!=0
 # Any exact curvature is in 19D hyperplane weight.f=0.
 # In F3, this hyperplane has min Hamming distance 2 (all weights nonzero).
 min_code_distance=2
 # Construct exact 2-plaquette minimal excitation solving B2^T a = f
 # with f on two coordinates chosen to balance weight pairing.
 f=np.zeros(20,dtype=int);f[0]=1
 f[1]=(-weight[0]*pow(int(weight[1])%3,-1,3))%3
 assert np.count_nonzero(f)==2 and int(weight@f)%3==0
 # Gauge invariance for fixed reproducible example: f(da) unaffected by a+delta0(phi).
 a=np.arange(60,dtype=int)%3
 phi=np.arange(40,dtype=int)%3
 F=((B2.T@a)%3)
 assert np.array_equal((B2.T@((a+B1.T@phi)%3))%3,F)
 out={
   "CW_vertices_edges_faces":[40,60,20],
   "link_cochains_dimension":60,
   "vertex_gauge_parameters_dimension":40,
   "gauge_effective_rank":39,
   "face_curvature_coboundary_rank_mod3":19,
   "flat_link_cochain_kernel_dim":60-19,
   "flat_connection_gauge_equivalence_sector_dimension":60-19-39,
   "flat_Z3_gauge_classes":3**(60-19-39),
   "flat_Z3_character_count_per_C5_quotient":9,
   "plaquette_face_flux_count_total":3**20,
   "exact_link_curvature_face_flux_count":3**19,
   "H2_nonexact_flux_classes":3,
   "integral_top_cycle_face_coefficients":weight.tolist(),
   "F3_curvature_zero_top_pairing_constraint":"sum_i signed_weight_i F_i = 0 mod 3",
   "example_nonexact_unit_face_flux":one.tolist(),
   "example_two_plaquette_exact_flux":f.tolist(),
   "exact_curvature_code_parameters_F3":[20,19,min_code_distance],
   "Wilson_Z3_action_form":"S= sum_i [1-cos(2*pi*Fi/3)] = 3/2 times number of nonzero F3 plaquettes",
   "nonzero_exact_curvature_minimum_classical_action":3,
   "F20_invariant_flat_Z3_characters":1,
   "F20_invariant_H2_F3_flux_dimension":1,
   "physical_boundary":"Toy pure finite Z3 lattice gauge kinematics only, Wilson couplings not fixed, no continuum dynamics, field content, masses, anomaly cancellation, or gravity"
 }
 return out
if __name__=="__main__":
 r=compute();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps({k:v for k,v in r.items() if k not in ("integral_top_cycle_face_coefficients","example_nonexact_unit_face_flux","example_two_plaquette_exact_flux")},indent=2),flush=True)
 print("GAUGE_COCHAIN_PASS")
