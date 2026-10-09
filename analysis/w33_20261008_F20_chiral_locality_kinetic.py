"""Symmetry/locality kinetic obstruction: F20 C4 exchanges actual
600cell-native (+) and mirror (-) chiral edge couplings within the
selected 60 W33 qubit addresses. A two-parameter hopping operator
H=a Aplus + b Aminus is F20-invariant iff a=b.
This is a discrete operator fact, not a Lorentzian stress tensor.
"""
from pathlib import Path
import json,sys,collections
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_H4_native_mirror_F20_kinetic_locality_firewall.json"
def main():
 data=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 prior=json.loads((ROOT/"data/w33_20261008_F20_A5_antipodal_60_bijection.json").read_text())
 _,E,_,_,_,_,_=topology();ei={e:i for i,e in enumerate(E)}
 plus={tuple(sorted(e)) for e in data["selected_H4_plus_W33_edges"]}
 minus={tuple(sorted(e)) for e in data["selected_H4_minus_W33_edges"]}
 gp=nx.Graph();gm=nx.Graph();gp.add_nodes_from(range(60));gm.add_nodes_from(range(60))
 gp.add_edges_from(plus);gm.add_edges_from(minus)
 assert gp.number_of_edges()==gm.number_of_edges()==60
 degP=dict(collections.Counter(dict(gp.degree()).values()))
 degM=dict(collections.Counter(dict(gm.degree()).values()))
 assert sum(k*v for k,v in degP.items())==120 and sum(k*v for k,v in degM.items())==120
 histplus=dict(collections.Counter(len(c) for c in nx.connected_components(gp)))
 histminus=dict(collections.Counter(len(c) for c in nx.connected_components(gm)))
 A=np.zeros((60,60),dtype=np.int64);B=A.copy()
 for u,v in plus:A[u,v]=A[v,u]=1
 for u,v in minus:B[u,v]=B[v,u]=1
 assert not np.array_equal(A,B) and np.max(A*B)==0
 s=tuple(prior["F20_generators_W33_80point_s"])
 r=tuple(prior["F20_generators_W33_80point_r"])
 def ind(p):return np.array([ei[tuple(sorted((p[u],p[v])))] for u,v in E])
 si=ind(s);ri=ind(r)
 assert np.array_equal(A[np.ix_(si,si)],B)
 assert np.array_equal(B[np.ix_(si,si)],A)
 assert np.array_equal(A[np.ix_(ri,ri)],A) and np.array_equal(B[np.ix_(ri,ri)],B)
 # A+B is unique F20-invariant vector in real span(A,B)
 H=A+B
 assert np.array_equal(H[np.ix_(si,si)],H)
 for a,b in ((0,1),(1,0),(1,2),(2,3),(1,1)):
  lhs=(a*A+b*B)[np.ix_(si,si)]
  rhs=a*A+b*B
  assert np.array_equal(lhs,rhs)==(a==b)
 eig=np.linalg.eigvalsh(H.astype(float))
 # graph energy quadratic positive semidefinite 4I-H
 L=4*np.eye(60)-H
 assert np.min(np.linalg.eigvalsh(L))>-1e-9
 return {"plus_native_600cell_edges_in_selected_W33_support":len(plus),
  "minus_nonnative_mirror_edges_in_selected_W33_support":len(minus),
  "plus_degree_hist":degP,"minus_degree_hist":degM,
  "plus_connected_component_size_hist":histplus,
  "minus_connected_component_size_hist":histminus,
  "F20_order4_exchanges_native_plus_and_nonnative_minus":True,
  "F20_order5_preserves_both_chiral_classes":True,
  "F20_invariant_two_class_couplings_iff_equal_a_b":True,
  "unique_F20_invariant_generator_in_span_Aplus_Aminus":"Aplus + Aminus",
  "F20_symmetric_discrete_Laplacian":"4I-(Aplus+Aminus)",
  "symmetric_chiral_Laplacian_smallest_eigenvalue":float(np.min(np.linalg.eigvalsh(L))),
  "symmetric_chiral_Laplacian_max_eigenvalue":float(np.max(np.linalg.eigvalsh(L))),
  "this_F20_symmetric_operator_not_native_600cell_nearest_neighbor_Laplacian":True,
  "not_local_Lorentzian_gravity_or_physical_stress_energy":True,
  "scientific_boundary":"An exact symmetry-vs-native-H4-nearest-neighbor-locality obstruction restricted to two-class hopping. Full F20 invariance requires two chiral couplings equal, introducing mirror edges; other representations or enlarged native carrier remain open."}
if __name__=="__main__":
 v=main();OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
 print(v,flush=True);print("F20_TWOCHIRAL_NATIVE_H4_LOCALITY_NO_GO_PASS")
