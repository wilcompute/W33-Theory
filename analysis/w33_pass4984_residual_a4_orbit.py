#!/usr/bin/env python3
"""Pass4984: classify the 810 A4 words missed by shell3+shell3."""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4984_RESIDUAL_A4_CHORDLESS_ORBIT.json'
def Q6(v):
 a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add(a,b):return tuple(x^y for x,y in zip(a,b))
def pol(a,b):return Q6(add(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
 I=tuple(range(n));S={I};D=deque([I])
 while D:
  a=D.popleft()
  for g in gens:
   z=comp(g,a)
   if z not in S:S.add(z);D.append(z)
 return S
def main():
 vec=[v for v in itertools.product((0,1),repeat=6) if any(v)];sing=[v for v in vec if Q6(v)==0];nons=[v for v in vec if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
 trans=[tuple(si[add(x,v) if pol(x,v) else x] for x in sing) for v in nons]
 gp=[];S={tuple(range(27))}
 for g in [comp(trans[0],t) for t in trans[1:]]:
  T=closure(gp+[g],27)
  if len(T)>len(S):gp.append(g);S=T
  if len(S)==25920:break
 qp=[sum(b<<i for i,b in enumerate(v)) for v in sing];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6];DS=set()
 for X,Y in itertools.combinations(C6,2):
  if X&Y:continue
  H=G.subgraph(X|Y)
  if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(X|Y))
 DS=sorted(DS,key=lambda s:tuple(sorted(s)));di={D:i for i,D in enumerate(DS)};H=nx.Graph();H.add_nodes_from(range(36))
 for i,j in itertools.combinations(range(36),2):
  if len(DS[i]&DS[j])==6:H.add_edge(i,j)
 E=sorted(tuple(sorted(e)) for e in H.edges());ei={e:i for i,e in enumerate(E)}
 C=np.eye(6,dtype=int)*2
 for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
 def ref(v,i):
  v=np.array(v,dtype=int);w=v.copy();w[i]-=int(v@C[:,i]);return tuple(map(int,w))
 roots={(1,0,0,0,0,0)};D=deque(roots)
 while D:
  v=D.popleft()
  for i in range(6):
   w=ref(v,i)
   if w not in roots:roots.add(w);D.append(w)
 pos=sorted(v for v in roots if all(x>=0 for x in v));ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
 for i,j in itertools.combinations(range(36),2):
  z=int(np.array(pos[i])@C@np.array(pos[j]));ip[(i,j)]=z
  if abs(z)==1:ER.add_edge(i,j)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(H,ER).isomorphisms_iter());sigma=np.zeros(360,dtype=np.uint8)
 for k,(a,b) in enumerate(E):
  i,j=sorted((iso[a],iso[b]));sigma[k]=int(ip[(i,j)]<0)
 cycles={}
 for V in itertools.combinations(range(36),4):
  for c in ((V[0],V[1],V[2],V[3]),(V[0],V[1],V[3],V[2]),(V[0],V[2],V[1],V[3])):
   es=[tuple(sorted((c[i],c[(i+1)%4]))) for i in range(4)]
   if all(H.has_edge(*e) for e in es):cycles[tuple(sorted(ei[e] for e in es))]=frozenset(V)
 cls=Counter();res=set()
 for mask,V in cycles.items():
  if sum(int(sigma[k]) for k in mask)&1:continue
  chords=sum(H.has_edge(*e) for e in itertools.combinations(V,2))-4;cls[chords]+=1
  if chords==0:res.add(V)
 assert cls==Counter({0:810,1:6480,2:3240})
 fullgens=gp+[trans[0]];DP=[tuple(di[frozenset(g[x] for x in D)] for D in DS) for g in fullgens];WG=closure(DP,36);base=next(iter(res));orb={frozenset(p[i] for i in base) for p in WG};stab=[p for p in WG if frozenset(p[i] for i in base)==base]
 supp=sorted(base);ind={tuple(supp.index(p[i]) for i in supp) for p in stab}
 assert orb==res and (len(WG),len(stab),len(ind))==(51840,64,8)
 out={'pass':4984,'A4_total':10530,'sigma_even_4cycle_split_by_chords':{'0':810,'1':6480,'2':3240},'shell3_pair_reachable':{'one_chord':6480,'two_chord':3240,'residual':810},'residual_810':{'description':'sigma-even chordless 4-cycles of H36','single_WE6_orbit':True,'orbit_size':810,'stabilizer_order':64,'support_action_order':8,'support_kernel_order':8},'character_relation':'If U0,U1,U2 are character sums on the 0/1/2-chord A4 orbits and V6 is the shell3-pair weight6 sum, then T3^2 = 1080 + 2(U1+2U2+V6); U0 is invisible to the second shell3 convolution.','covering_radius':{'proved_interval':[134,173],'improved_here':False},'theorem':'The 810 A4 words missed by shell3+shell3 are exactly the sigma-even chordless four-cycles of H36. The full A4 shell splits into three single W(E6) orbits of sizes 810,6480,3240 according to chord number 0,1,2; the residual orbit has stabilizer order64.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
