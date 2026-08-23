#!/usr/bin/env python3
"""Pass8813-8820: explicit Leech36 -> W33 local geometry -> CSS point-star coordinate diagram."""
from collections import defaultdict
import itertools,json
from pathlib import Path
import numpy as np, networkx as nx
from analysis.w33_pass8101_8108_leech_h27_gl23_lagrangian_controller import lagrangians,proj
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8813_8820_LEECH_W33_CSS_DIAGRAM.json'
def canon(v):
 v=tuple(int(x)%3 for x in v)
 for x in v:
  if x:return tuple((pow(x,-1,3)*y)%3 for y in v)
P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={v:i for i,v in enumerate(P)}
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],int)%3
def adj(i,j):return i!=j and int(np.array(P[i])@J@np.array(P[j]))%3==0
lines=set()
for i,j in itertools.combinations(range(40),2):
 if not adj(i,j):continue
 u=np.array(P[i]);v=np.array(P[j]);S=set()
 for a,b in itertools.product(range(3),repeat=2):
  if a or b:S.add(pi[canon(tuple(map(int,(a*u+b*v)%3)))])
 if len(S)==4:lines.add(frozenset(S))
lines=sorted(lines,key=lambda s:tuple(sorted(s)));li={L:i for i,L in enumerate(lines)};assert len(lines)==40
p=0;away=[L for L in lines if p not in L];assert len(away)==36
nbr=[q for q in range(40) if adj(p,q)];assert len(nbr)==12
WF=[frozenset(i for i,L in enumerate(away) if q in L) for q in nbr];assert len(set(WF))==12 and set(map(len,WF))=={3}
LL=lagrangians();A=np.zeros((144,144),dtype=np.uint8)
for i,j in itertools.combinations(range(144),2):
 if len(LL[i]&LL[j])==9:A[i,j]=A[j,i]=1
CC=[sorted(c) for c in nx.connected_components(nx.from_numpy_array(A))];assert list(map(len,CC))==[36,36,36,36]
C=CC[0];AL=A[np.ix_(C,C)];F=defaultdict(list)
for loc,g in enumerate(C):F[proj(LL[g])].append(loc)
LF=[frozenset(x) for x in F.values()];assert len(LF)==12 and set(map(len,LF))=={3}
def aug(A0,F0):
 G=nx.Graph()
 for i in range(36):G.add_node(('v',i),kind='v')
 for i,j in np.argwhere(np.triu(A0,1)):G.add_edge(('v',int(i)),('v',int(j)))
 for k,S in enumerate(F0):
  G.add_node(('f',k),kind='f')
  for i in S:G.add_edge(('f',k),('v',i))
 return G
AW=np.zeros((36,36),dtype=np.uint8)
for i,j in itertools.combinations(range(36),2):
 if away[i]&away[j]:AW[i,j]=AW[j,i]=1
gm=nx.algorithms.isomorphism.GraphMatcher(aug(AL,LF),aug(AW,WF),node_match=lambda a,b:a['kind']==b['kind'])
iso=next(gm.isomorphisms_iter());assert all(iso[('f',k)][0]=='f' for k in range(12))
through=[L for L in lines if p in L];assert len(through)==4
coords={};groups=defaultdict(list)
for L in through:
 V=sorted(L);others=[x for x in V if x!=p]
 for q in others:
  rem=[x for x in others if x!=q];M=frozenset((tuple(sorted((p,q))),tuple(sorted(rem))))
  coords[q]=(li[L],M);groups[li[L]].append(q)
assert set(coords)==set(nbr) and sorted(map(len,groups.values()))==[3,3,3,3]
out={'schema':'w33.pass8813_8820.leech_w33_css_diagram.v1','status':'PASS','passes':'8813-8820','Leech':{'component_vertices':36,'fibres':'12 x 3'},'W33':{'lines_away_from_p':36,'neighbor_indexed_fibres':'12 x 3','lines_through_p':4},'CSS':{'point_star_weight':12,'coordinates_at_p':12,'coordinate_rule':'q -> unique matching on line pq containing edge {p,q}','parallel_class_shape':'4 x 3'},'fiber_preserving_Leech_to_W33_isomorphism':True,'W33_neighbor_to_CSS_coordinate_bijection':True,'theorem':'The Pass8481 Leech36/W33 weld extends canonically to the punctured CSS matching carrier: Leech fibres map to W33 neighbor fibres, and each neighbor q selects one of the twelve point-star coordinates by the matching containing pq.','claim_boundary':'Exact finite commuting diagram; no statement that a Leech Lagrangian is a physical CSS qubit.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','diagram':'Leech36->W33->CSS','shape':'12=4x3'}))
