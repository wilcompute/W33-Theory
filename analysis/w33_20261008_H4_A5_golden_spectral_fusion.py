"""Exact spectral fusion law for two chiral A5 5-cycle Cayley graphs
realized by antipodal 600-cell coordinates.

Each chiral normal Cayley class-5 graph has spectrum
12^1,(2+2sqrt5)^9,(2-2sqrt5)^9,(-3)^16,0^25.
Adding mirror 5-cycle class cancels irrationality, spectrum
24^1,4^18,(-6)^16,0^25.

This is an exact character-theoretic prediction independently checked
by explicit eigenvalues and powers of 60x60 adjacency matrices.
"""
import json,itertools,sys,math,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,compose,permutation_order
from w33_20261008_H4_A5_chiral_Cayley_pair import main as certificate
OUT=ROOT/"data/w33_20261008_H4_A5_golden_spectrum_chiral_fusion.json"
def main():
 cert=certificate()
 gp=clifford_antipodal_permutations();idx={p:k for k,p in gp.items()}
 C=[tuple(p) for p in cert["A5_neighbor_identity_permutations"]]
 D=[tuple(p) for p in cert["mirror_A5_5cycle_identity_permutations"]]
 mats=[]
 for gens in (C,D,C+D):
  A=np.zeros((60,60),dtype=np.int64)
  for i,p in gp.items():
   for g in gens:A[i,idx[compose(p,g)]]=1
  assert np.all(A==A.T) and np.array_equal(np.diag(A),np.zeros(60))
  assert set(A.sum(axis=1))=={len(gens)}
  mats.append(A)
 A,B,U=mats
 assert np.array_equal(A+B,U)
 assert not np.any(A&B)
 predicted_one={12:1,2+2*math.sqrt(5):9,2-2*math.sqrt(5):9,-3:16,0:25}
 predicted_union={24:1,4:18,-6:16,0:25}
 def matches(matrix,expected):
  values=np.linalg.eigvalsh(matrix.astype(float))
  predicted=sorted(x for lam,m in expected.items() for x in [lam]*m)
  diff=float(max(abs(x-y) for x,y in zip(values,predicted)))
  assert diff<1e-8,diff
  return diff
 epsA=matches(A,predicted_one);epsB=matches(B,predicted_one);epsU=matches(U,predicted_union)
 assert int(np.trace(A@A))==60*12
 assert int(np.trace(U@U))==60*24
 assert int(np.trace(A@A@A))==6*600
 # Compare W33 vertex graph spectrum integer [12,2,-4],
 # distinct vertex count and eigenvalues.
 return {"600cell_antipodal_graph_H4_vertices":60,
  "chiral_A5_class5_5cycle_graph_degree":12,
  "spectrum_chiral_class5":"12^1, (2+2sqrt(5))^9, (2-2sqrt(5))^9, (-3)^16, 0^25",
  "second_mirror_chiral_graph_same_spectrum":True,
  "mirror_edge_sets_disjoint":True,
  "union_degree":24,
  "spectrum_union_chirality_fused":"24^1, 4^18, (-6)^16, 0^25",
  "golden_irrationality_cancels_in_chiral_pair":True,
  "independent_numeric_spectral_max_error":[epsA,epsB,epsU],
  "triangle_count_each_chiral":int(np.trace(A@A@A))//6,
  "W33_point_graph_spectrum":"12^1,2^24,(-4)^15 on 40 vertices",
  "same_degree_12_but_graph_spectra_distinct":True,
  "physical_limit":"Character-theoretic spectral fusion, no identified physical mass, coupling, CP operation or chiral fermion."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("H4_GOLDEN_SPECTRAL_FUSION_PASS")
