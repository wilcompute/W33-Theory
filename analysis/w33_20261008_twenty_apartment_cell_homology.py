#!/usr/bin/env python3
"""Integer cellular homology of the explicit branched 20-apartment 2-cycle.

The octagons are attached as 2-cells to a shared 40-vertex/60-edge graph.
This CW complex need NOT be a manifold merely because Euler characteristic 0.
"""
import json,sys,math
from collections import Counter,defaultdict
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_global_cycle_center_census import cycles
from w33_20261008_six_toe_frontier_followthrough import levi_graph
OUT=ROOT/"data"/"w33_20261008_twenty_apartment_cell_homology.json"

def main():
  C=cycles();G=levi_graph()
  design=json.loads((ROOT/"data/w33_20261008_cycle_center_atlas_constructive.json").read_text())
  rel=json.loads((ROOT/"data/w33_20261008_cycle_atlas_homology_rank.json").read_text())
  selected=[(cid,w) for cid,w in zip(design["largest_found_cycle_indices"],rel["primitive_integral_relation_coefficients"]) if w]
  assert len(selected)==20 and set(w for cid,w in selected)=={-1,1}
  E=set();V=set();multiplicity=Counter()
  for cid,_ in selected:
    c=C[cid]
    V.update(c)
    for a,b in zip(c,c[1:]+c[:1]):
      e=(min(a,b),max(a,b));E.add(e);multiplicity[e]+=1
  E=sorted(E);V=sorted(V);ed={e:i for i,e in enumerate(E)};vd={v:i for i,v in enumerate(V)}
  nv,ne,nf=len(V),len(E),len(selected)
  assert (nv,ne,nf)==(40,60,20)
  boundary1=sp.zeros(nv,ne)
  for idx,(a,b) in enumerate(E):
    boundary1[vd[a],idx]=-1
    boundary1[vd[b],idx]=1
  boundary2=sp.zeros(ne,nf)
  for k,(cid,w) in enumerate(selected):
    c=C[cid]
    for a,b in zip(c,c[1:]+c[:1]):
      boundary2[ed[(min(a,b),max(a,b))],k]+=(1 if a<40 else -1)
  assert boundary1*boundary2==sp.zeros(nv,nf)
  assert boundary2*sp.Matrix([w for _,w in selected])==sp.zeros(ne,1)
  # Rank over Z via Smith normal form on integral boundary matrices.
  D1=smith_normal_form(boundary1,domain=ZZ)
  D2=smith_normal_form(boundary2,domain=ZZ)
  sv1=[abs(int(D1[i,i])) for i in range(min(D1.rows,D1.cols)) if D1[i,i]!=0]
  sv2=[abs(int(D2[i,i])) for i in range(min(D2.rows,D2.cols)) if D2[i,i]!=0]
  rank1=len(sv1);rank2=len(sv2)
  b0=nv-rank1;b1=ne-rank1-rank2;b2=nf-rank2
  assert (rank1,rank2)==(39,19)
  assert (b0,b1,b2)==(1,2,1)
  # Torsion of H1 is torsion(coker partial2) as coker partial2
  # extends im(partial1), which is free abelian; both have same torsion.
  h1tors=[v for v in sv2 if v>1]
  assert not h1tors,(h1tors,sv2)
  assert len(E)==60 and Counter(multiplicity.values())=={2:40,4:20}
  degree=Counter()
  for a,b in E:
    degree[a]+=1;degree[b]+=1
  assert Counter(degree.values())=={3:40}
  out={"CW_cells_V_E_F":[nv,ne,nf],
       "underlying_graph_components":b0,
       "skeleton_vertex_degree_histogram":dict(Counter(degree.values())),
       "octagon_edge_face_multiplicity_histogram":dict(Counter(multiplicity.values())),
       "chain_boundary_ranks_over_Q":[rank1,rank2],
       "smith_d1_nonzero_diagonal_histogram":dict(Counter(sv1)),
       "smith_d2_nonzero_diagonal_histogram":dict(Counter(sv2)),
       "homology_betti_H0_H1_H2":[b0,b1,b2],
       "H1_torsion_invariant_factors":h1tors,
       "integral_H0_H1_H2":["Z","Z^2","Z"],
       "euler_characteristic":nv-ne+nf,
       "topological_type":"Integral homology of T2, but non-manifold (20 edges incident to four 2-cells), not homeomorphic to ordinary torus",
       "20_signed_faces_boundary_sum_zero":True,
       "owner_boundary":"Explicit 20-face relation inside new selected 45-cycle compatible atlas; BT744 owns W33 apartments and Steinberg 81, earlier toroidal Csaszar counts independent"
      }
  return out
if __name__=="__main__":
  r=main()
  OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
  print(json.dumps(r,indent=2),flush=True)
  print("TWENTY_CELL_HOMOLOGY_PASS",flush=True)
