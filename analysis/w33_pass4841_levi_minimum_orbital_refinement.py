#!/usr/bin/env python3
"""Pass4841: full stabilizer suborbit refinement of the 1080 Levi minima.
Build bare GQ(4,2), enumerate its 1080 line-graph four-cycles, enumerate the
51840 graph automorphisms, recover the 25920 square/commutator socle, and compute
stabilizer suborbits.  This is the exact refinement behind the failed coarse
shared-edge association-scheme attempt of Pass4840.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4841_LEVI_MINIMUM_ORBITAL_REFINEMENT.json'
def Q(v):
 a,b,c,d,e,f=v;return (a*b+c*d+e+e*f+f)&1
def bits(x):return tuple((x>>i)&1 for i in range(6))
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def comm(a,b):return comp(comp(comp(a,b),inv(a)),inv(b))
def closure(gens,n=27):
 I=tuple(range(n));S={I};D=deque([I])
 while D:
  a=D.popleft()
  for g in gens:
   c=comp(g,a)
   if c not in S:S.add(c);D.append(c)
 return S
def main()->int:
 qp=[x for x in range(1,64) if Q(bits(x))==0];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 q4=[]
 for S in itertools.combinations(range(27),4):
  H=G.subgraph(S)
  if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):q4.append(frozenset(S))
 assert len(q4)==1080;idx={S:i for i,S in enumerate(q4)}
 autos=[tuple(m[i] for i in range(27)) for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()];assert len(autos)==51840
 gens=[];cur={tuple(range(27))}
 for p in autos:
  T=closure(gens+[p])
  if len(T)>len(cur):gens.append(p);cur=T
  if len(cur)==51840:break
 soc=closure([comp(g,g) for g in gens]+[comm(a,b) for a,b in itertools.combinations(gens,2)]);assert len(soc)==25920
 act=lambda S,p:frozenset(p[x] for x in S);seed=q4[0];stabP=[p for p in soc if act(seed,p)==seed];stabF=[p for p in autos if act(seed,p)==seed];assert len(stabP)==24 and len(stabF)==48
 def suborbits(H):
  unseen=set(range(1080));O=[]
  while unseen:
   i=min(unseen);S={idx[act(q4[i],p)] for p in H};O.append(S);unseen-=S
  return O
 OP=suborbits(stabP);OF=suborbits(stabF);cp=Counter(map(len,OP));cf=Counter(map(len,OF));assert len(OP)==59 and len(OF)==49
 out={'pass':4841,'minimum_shell_size':1080,'PSp':{'stabilizer_order':24,'permutation_rank':59,'subdegree_census':dict(sorted(cp.items()))},'PGSp':{'stabilizer_order':48,'permutation_rank':49,'subdegree_census':dict(sorted(cf.items()))},'PSp_subdegrees_sorted':sorted(map(len,OP)),'PGSp_subdegrees_sorted':sorted(map(len,OF)),'theorem':'The minimum-shell action is far finer than shared-edge count: PSp has permutation rank 59 and PGSp rank 49 on the 1080 Levi minima. The outer involution fuses ten pairs of PSp suborbits, reducing rank by ten.','boundary':'These are stabilizer orbitals on binary minima. Shared-edge/K3,3/line-overlap statistics are coarse invariants and do not define the full orbital scheme.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
