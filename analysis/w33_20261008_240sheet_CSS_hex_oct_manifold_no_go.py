"""Lift all W33 star-X triangles as length-six faces in the formal
240-vertex Z2^2 chiral graph. Their voltage is nonzero, giving TWO
hexagonal faces for each of 40 stars. Every cover edge sits in exactly
one hexagon. Together with all four lifts of 20 Z octagons, incidence
is 1 or 3, never 2: an exact full CSS face-as-manifold NO-GO.
"""
from pathlib import Path
import itertools,json,sys,collections
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
from w33_20261008_240sheet_chiral_CW_octagon_homology import rank
OUT=ROOT/"data/w33_20261008_chiral_240cover_CSS_80hex_80oct_nonmanifold.json"
def main():
 orig=json.loads((ROOT/"data/w33_20261008_W33_to_H4_chiral_4regular_embedding.json").read_text())
 V,E,faces,st,H,bx,bz=topology()
 eid={e:i for i,e in enumerate(E)}
 plus={tuple(sorted(e)) for e in orig["selected_H4_plus_W33_edges"]}
 minus={tuple(sorted(e)) for e in orig["selected_H4_minus_W33_edges"]}
 voltage={uv:1 if uv in plus else 2 for uv in plus|minus}
 G=nx.Graph();G.add_nodes_from(range(240))
 for (i,j),w in voltage.items():
  for sh in range(4):G.add_edge(i*4+sh,j*4+(sh^w))
 ed=sorted(tuple(sorted(e)) for e in G.edges());EI={e:i for i,e in enumerate(ed)}
 assert len(ed)==480
 def walk(seq,starting_sheet):
  now=starting_sheet;mask=0;nodes=[]
  for a,b in zip(seq,seq[1:]+seq[:1]):
   x=a*4+now;nodes.append(x)
   now^=voltage[tuple(sorted((a,b)))]
   y=b*4+now
   edge=tuple(sorted((x,y)))
   assert edge in EI
   mask^=1<<EI[edge]
  return mask,now,nodes
 octs=[];hexes=[]
 for f in faces:
  q=[eid[tuple(sorted((u,v)))] for u,v in zip(f,f[1:]+f[:1])]
  for sh in range(4):
   mask,last,nodes=walk(q,sh)
   assert last==sh and mask.bit_count()==8
   octs.append(mask)
 for star in V:
  q=sorted(i for i,e in enumerate(E) if star in e)
  assert len(q)==3
  for sh in range(4):
   mask,last,nodes=walk(q+q,sh)
   assert last==sh and mask.bit_count()==6
   if mask not in hexes:hexes.append(mask)
 assert len(octs)==80 and len(hexes)==80
 assert len(set(hexes))==80
 CI=collections.Counter();HI=collections.Counter()
 for m in octs:
  for j in range(480):
   if m>>j&1:CI[j]+=1
 for m in hexes:
  for j in range(480):
   if m>>j&1:HI[j]+=1
 assert set(HI.values())=={1}
 combined=dict(collections.Counter(CI[j]+HI[j] for j in range(480)))
 assert combined=={3:320,1:160}
 cols=octs+hexes;rank2=rank(cols)
 d1=[(1<<u)|(1<<v) for u,v in ed]
 for mask in cols:
  bdy=0
  for j in range(480):
   if mask>>j&1:bdy^=d1[j]
  assert bdy==0
 rank1=rank(d1)
 b0=240-rank1;b1=480-rank1-rank2;b2=160-rank2
 assert 240-480+160==b0-b1+b2
 return {"CW_f_vector":[240,480,160],
  "X_star_base_checks":40,"star_hexagon_lifts":len(hexes),
  "Z_octagon_base_checks":20,"Z_octagon_lifts":len(octs),
  "each_cover_edge_occurs_in_exactly_one_X_star_hexagon":True,
  "octagon_face_incidence_count_hist":dict(collections.Counter(CI[j] for j in range(480))),
  "union_hexagon_plus_octagon_edge_face_incidence_hist":combined,
  "exactly_two_faces_per_edge_in_full_CSS_chiral_CW":False,
  "closed_two_manifold_possible_with_these_full_CSS_face_attachments":False,
  "GF2_boundary_ranks":[rank1,rank2],
  "GF2_homology_betti_numbers":[b0,b1,b2],
  "GF2_boundary_square_zero":True,
  "physical_boundaries":"This is a formal 240-vertex CW cell atlas. Its 160 faces do not make a closed manifold, nor a native 600-cell/BC or a physical syndrome machine."}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(r,flush=True);print("CHIRAL_FULL_80HEX_80OCT_CSS_NONMANIFOLD_NO_GO_PASS")
