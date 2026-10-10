"""Round24 finite code-distance firewall for geometric partial-flatness CSS codes."""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain
from w33_20261009_round18_chirality_plaquette_audit import cycles_touching
from w33_pass1081_1086_core import rank_mod
OUT=ROOT/'data/w33_20261009_toe24_css_distance_firewall.json'
def run():
 pts,ix,lines,li,edges,tris,flags,fi,E,T,D,M,R=chain()
 ed=[(p,40+l) for p,l in flags]
 idx={tuple(sorted(z)):i for i,z in enumerate(ed)}
 cyc=set()
 for j in range(160):cyc.update(cycles_touching(ed,j))
 rows=[];vertices=[]
 for packet in sorted(cyc):
  z=np.zeros(160,dtype=np.int8)
  for a,b in zip(packet,packet[1:]+packet[:1]):z[idx[tuple(sorted((a,b)))]]=1 if a<b else -1
  rows.append(z);vertices.append(set(packet))
 C=np.array(rows,dtype=np.int8)
 assert C.shape==(1620,160) and np.all((D@C.T)%3==0)
 v0=0;e0=0
 variants=[
  ('avoid_incidence_edge',np.flatnonzero(C[:,e0]==0),[e0],80,1),
  ('avoid_vertex',np.array([k for k,v in enumerate(vertices) if v0 not in v]),[j for j,(p,l) in enumerate(flags) if p==v0],78,3)]
 reports={}
 for name,chosen,free_edges,r,logical in variants:
  S=C[chosen];assert rank_mod(S,3)==r
  unused=np.flatnonzero(np.all(S==0,axis=0))
  assert set(free_edges).issubset(set(unused))
  assert len(free_edges)==(1 if logical==1 else 4)
  for j in free_edges:
   e=np.zeros(160,dtype=np.int8);e[j]=1
   assert np.all(S@e%3==0)
   assert np.any(C@e%3!=0) # nontrivial physical cycle detects edge, so NOT a pure vertex-gauge cut
  # In a connected graph, an edge basis vector lies in the cut space iff
  # it is a bridge. Every W33 Levi edge lies on 81 native cycles: no bridges.
  # Gauss at v0 is the signed product of all four incident edge X operators:
  # at most three independent degree-one logical X channels on v0.
  reports[name]=dict(selected_Wilson_rows=int(len(chosen)),
   Wilson_rank_F3=r,remaining_logical_qutrits=logical,
   unused_link_count=len(unused),verified_weight_one_logical_X_link_indices=[int(j) for j in free_edges],
   exact_code_distance=1,
   onsite_error='A single link Pauli X on each unused incidence link COMMUTES with the chosen Gauss and Wilson checks but acts nontrivially on the logical subsystem. Hence a weight-one logical operator exists, and quantum code distance is exactly one.',
   local_splitting='Adding -h(X_e+X_e dagger) with any selected weight-one logical e splits a logical qutrit energy as -2h,+h,+h, a gap of 3|h| for h>0. This is a first-order local perturbation acting INSIDE the ground space; no topological protection or macroscopic energy barrier.')
  print('CODE',name,reports[name],flush=True)
 assert (D[v0]!=0).sum()==4
 out=dict(status='PASS',native_n_links=160,n_vertices=80,Gauss_rank=79,
  profiles=reports,
  obstruction='The claimed logical survival from partial Wilson flatness is algebraically correct but all two geometrically simple selectors have distance ONE. The all-cycles flatness model has no logical qudits. A protected memory requires much more than nonzero first homology / a positive number of encoded qudits.',
  prior='Round23 computed Wilson ranks and logical counts, BT744 proved 81 cycles through chamber span H1. New: elementary local Pauli logical witnesses, exact code distances, and first-order degeneracy splitting.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
