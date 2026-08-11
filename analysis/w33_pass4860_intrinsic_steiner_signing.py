#!/usr/bin/env python3
"""Pass4860 — root-free E6 switching class from double-six/Steiner incidence.

Rebuild the bare GQ(4,2) 27-line carrier and its 36 double-sixes as the twelve-line
K6,6-minus-matching subgraphs.  Their overlap-6 graph is SRG(36,20,10,12).
Among its 1200 triangles, exactly 120 have empty triple intersection of their
27-line supports (hence union size18); this is exactly the finite Steiner
trihedral-pair definition already certified by MCCCXCVI.

Declare precisely those 120 triangles odd.  Solve the triangle-parity equations
on the 360 double-six edges.  The triangle-edge matrix has rank325, so the
solution space has dimension35; the cut space of the connected 36-vertex graph
also has dimension35 and lies in the homogeneous kernel.  Thus the Steiner odd
triangles determine one switching class uniquely modulo cuts.  A final
cross-check reconstructs E6 roots and proves this class equals sigma_E6.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4860_INTRINSIC_STEINER_SIGNING.json'

def Q(x):
 b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1

def rref2(A,b=None):
 A=np.array(A,dtype=np.uint8);X=A if b is None else np.c_[A,np.array(b,dtype=np.uint8)];m,n=A.shape;r=0;p=[]
 for c in range(n):
  q=next((i for i in range(r,m) if X[i,c]),None)
  if q is None:continue
  X[[r,q]]=X[[q,r]]
  for i in range(m):
   if i!=r and X[i,c]:X[i]^=X[r]
  p.append(c);r+=1
 return X,p

def main()->int:
 qp=[x for x in range(1,64) if Q(x)==0];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6];assert len(C6)==72
 DS=set()
 for A,B in itertools.combinations(C6,2):
  if A&B:continue
  H=G.subgraph(A|B)
  if len(A|B)==12 and H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
 DS=sorted(DS,key=lambda S:tuple(sorted(S)));assert len(DS)==36
 H=nx.Graph();H.add_nodes_from(range(36))
 for i,j in itertools.combinations(range(36),2):
  z=len(DS[i]&DS[j]);assert z in (4,6)
  if z==6:H.add_edge(i,j)
 assert H.number_of_edges()==360 and set(dict(H.degree()).values())=={20}
 E=sorted(tuple(sorted(e)) for e in H.edges());ei={e:i for i,e in enumerate(E)}
 tri=[];profile=Counter()
 for a,b,c in itertools.combinations(range(36),3):
  if H.has_edge(a,b) and H.has_edge(a,c) and H.has_edge(b,c):
   t=(a,b,c);tri.append(t);profile[len(DS[a]&DS[b]&DS[c])]+=1
 assert len(tri)==1200 and profile==Counter({4:1080,0:120})
 M=np.zeros((1200,360),dtype=np.uint8);odd=np.zeros(1200,dtype=np.uint8)
 for r,t in enumerate(tri):
  for e in itertools.combinations(t,2):M[r,ei[tuple(sorted(e))]]=1
  odd[r]=int(len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
 R,piv=rref2(M,odd);assert len(piv)==325
 x=np.zeros(360,dtype=np.uint8)
 for i,c in enumerate(piv):x[c]=R[i,-1]
 assert np.array_equal((M@x)%2,odd) and int(x.sum())==120
 # homogeneous kernel is exactly the graph cut space: dimensions agree.
 assert 360-len(piv)==35 and nx.is_connected(H)
 # Cross-check against roots, but roots are not used to DEFINE the class.
 Cart=np.eye(6,dtype=int)*2
 for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):Cart[a,b]=Cart[b,a]=-1
 def refl(v,i):
  v=np.array(v,dtype=int);m=int(v@Cart[:,i]);w=v.copy();w[i]-=m;return tuple(map(int,w))
 roots={(1,0,0,0,0,0)};D=deque(roots)
 while D:
  v=D.popleft()
  for i in range(6):
   w=refl(v,i)
   if w not in roots:roots.add(w);D.append(w)
 pos=sorted(v for v in roots if all(z>=0 for z in v));assert len(pos)==36
 ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
 for i,j in itertools.combinations(range(36),2):
  z=int(np.array(pos[i])@Cart@np.array(pos[j]));ip[(i,j)]=z
  if abs(z)==1:ER.add_edge(i,j)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(H,ER).isomorphisms_iter())
 sigma=np.zeros(360,dtype=np.uint8)
 for k,(a,b) in enumerate(E):
  i,j=sorted((iso[a],iso[b]));sigma[k]=int(ip[(i,j)]<0)
 assert np.array_equal((M@sigma)%2,odd)
 diff=x^sigma
 # same triangle parities imply diff lies in the 35D homogeneous kernel=cut space.
 assert not np.any((M@diff)%2)
 out={'pass':4860,'double_sixes':36,'double_six_graph':'SRG(36,20,10,12)','graph_edges':360,'graph_triangles':1200,
  'triangle_triple_intersection_profile':{'0':120,'4':1080},'Steiner_trihedral_pairs':120,
  'intrinsic_definition':'A graph triangle is odd iff its three 12-line double-sixes have empty triple intersection (equivalently the MCCCXCVI Steiner trihedral-pair condition; pairwise overlap is already six and the union is then 18).',
  'triangle_edge_matrix_rank_F2':325,'switching_solution_affine_dimension':35,'cut_space_dimension':35,'canonical_rref_representative_weight':int(x.sum()),
  'root_crosscheck':{'E6_negative_edge_signing_has_same_120_odd_triangles':True,'difference_from_intrinsic_rref_solution_is_a_cut':True},
  'theorem':'The E6 switching class sigma_E6 is intrinsic to the classical 27-36-45 cubic-surface incidence data: it is the unique edge-signing class modulo cuts whose odd graph triangles are exactly the 120 Steiner trihedral pairs. Root coordinates are unnecessary for defining the class; the E6 root signing is an independent cross-certificate of the same class.',
  'boundary':'This is a finite two-graph/cubic-surface theorem. It does not assign a physical sign or phase to hardware without an additional realization map.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
