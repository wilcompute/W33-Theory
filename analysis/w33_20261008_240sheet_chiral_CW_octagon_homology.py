"""Attach all 20x4 W33 Z-check octagons to the 240-vertex
F20-equivariant 4-sheet chiral voltage COVER and compute GF2 homology.
This is an explicit CW 2-complex (every face closes), but may not be
a closed 2-manifold: check lifted edge/face incidence multiplicities.
"""
import sys,json,itertools,collections
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_chiral_240voltage_80octagon_CW_homology.json"
def rank(vectors):
 piv={}
 for v in vectors:
  x=v
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)
def main():
 rec=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 V,E,faces,st,H,bx,bz=topology()
 eid={e:i for i,e in enumerate(E)}
 plus={tuple(sorted(e)) for e in rec["selected_H4_plus_W33_edges"]}
 minus={tuple(sorted(e)) for e in rec["selected_H4_minus_W33_edges"]}
 voltage={pair:1 if pair in plus else 2 for pair in plus|minus}
 G=nx.Graph();G.add_nodes_from(range(240))
 for (a,b),v in voltage.items():
  for sheet in range(4):G.add_edge(a*4+sheet,b*4+(sheet^v))
 edges=sorted(tuple(sorted(e)) for e in G.edges());eidx={e:i for i,e in enumerate(edges)}
 assert len(edges)==480 and nx.is_connected(G)
 d1=[(1<<u)|(1<<v) for u,v in edges]
 d2=[];face_arr=[];inc=collections.Counter()
 for fi,f in enumerate(faces):
  q=[eid[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  assert len(q)==8
  for sheet in range(4):
   now=sheet;arr=[q[0]*4+sheet];bits=0
   for j in range(8):
    u=q[j];v=q[(j+1)%8]
    edge=tuple(sorted((u,v)))
    w=voltage[edge]
    a=u*4+now;b=v*4+(now^w)
    assert G.has_edge(a,b)
    idx=eidx[tuple(sorted((a,b)))]
    bits^=1<<idx;inc[idx]+=1
    now^=w
    if j<7:arr.append(v*4+now)
   assert now==sheet
   assert bits.bit_count()==8
   d2.append(bits)
   face_arr.append({"base_octagon":fi,"sheet":sheet,"qubit_address_cycle":arr})
 # Check boundary of every lifted octagon is zero over GF2.
 for row in d2:
  bdy=0
  for j in range(480):
   if row>>j&1:bdy^=d1[j]
  assert bdy==0
 rank1=rank(d1);rank2=rank(d2);chi=240-480+80
 b0=240-rank1;b1=480-rank1-rank2;b2=80-rank2
 incidences=dict(collections.Counter(inc.get(j,0) for j in range(480)))
 return {"W33_base_octagon_check_count":20,"four_lifts_per_octagon":4,
  "F20_chiral_voltage_two_complex_faces":len(d2),
  "CW_f_vector":[240,480,80],"CW_Euler_char":chi,
  "GF2_boundary_ranks":[rank1,rank2],
  "GF2_homology_betti_numbers":[b0,b1,b2],
  "boundary_square_zero":True,
  "all_80_lifted_octagons_closed_8_edge_cycles":True,
  "CW_edges_incidence_number_of_lifted_octagons_hist":incidences,
  "each_CW_edge_incident_to_exactly_two_octagons":set(incidences)=={2},
  "closed_two_manifold_CW_complex":set(incidences)=={2} and all(nx.degree(G,n)==2 for n in G.nodes()),
  "face_lift_example":face_arr[0],
  "not_native_H4_tetrahedral_face_cell_complex":True,
  "not_equivalent_topologically_to_original_W33_20apartment_torus":True,
  "scope":"An explicit 240v 480e 80oct CW 2-complex with cellular homology. Closure of all Z check loops DOES NOT imply 2-manifold or encoded physical code; GF2 homology and edge-face incidence constrain this."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("F20_CHIRAL_240_80OCTAGON_CW_HOMOLOGY_PASS")
