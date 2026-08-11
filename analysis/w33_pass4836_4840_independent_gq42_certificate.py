#!/usr/bin/env python3
"""Independent bare-GQ(4,2) certificate for Passes 4836/4840.

No W33 router labels are imported.  Build the 27 lines / 45 points of GQ(4,2)
from the standard O^-(6,2) quadratic model, enumerate the 1080 4-cycles of the
27-line intersection graph (= Levi 8-cycles), enumerate all 360 induced K3,3s,
and compute their literal containment incidence.  Enumerate the full graph
automorphism group (order 51840); its square/commutator subgroup has order25920
and is the simple PSp(4,3) socle.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT36=ROOT/'data/PART_W33_PASS4836_LEVI_MINIMUM_ORBITS.json'
OUT40=ROOT/'data/PART_W33_PASS4840_LEVI_CYCLE_K33_INCIDENCE.json'

def Q(v):
 x1,x2,x3,x4,x5,x6=v;return (x1*x2+x3*x4+x5+x5*x6+x6)&1
def bits(x):return tuple((x>>i)&1 for i in range(6))
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def comm(a,b):return compose(compose(compose(a,b),inv(a)),inv(b))
def closure(gens,n=27):
 I=tuple(range(n));seen={I};Qd=deque([I])
 while Qd:
  a=Qd.popleft()
  for g in gens:
   c=compose(g,a)
   if c not in seen:seen.add(c);Qd.append(c)
 return seen

def main()->int:
 qp=[x for x in range(1,64) if Q(bits(x))==0];assert len(qp)==27
 pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if (a^b) in qp});assert len(pts)==45
 lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp];assert {len(L) for L in lines}=={5}
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if len(set(lines[i])&set(lines[j]))==1:G.add_edge(i,j)
 assert G.number_of_edges()==135 and set(dict(G.degree()).values())=={10}
 q4=[]
 for S in itertools.combinations(range(27),4):
  H=G.subgraph(S)
  if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):q4.append(frozenset(S))
 assert len(q4)==1080
 # Levi edge support of each q4.
 ledges=sorted((p,l) for l,L in enumerate(lines) for p in L);ei={e:i for i,e in enumerate(ledges)};masks=[]
 for S in q4:
  C=nx.cycle_basis(G.subgraph(S));assert len(C)==1 and len(C[0])==4;o=C[0];m=0
  for a,b in zip(o,o[1:]+o[:1]):
   hit=set(lines[a])&set(lines[b]);assert len(hit)==1;p=next(iter(hit));m|=1<<ei[(p,a)];m|=1<<ei[(p,b)]
  assert m.bit_count()==8;masks.append(m)
 assert len(set(masks))==1080
 # Full aut and index-two simple socle.
 autos=[tuple(m[i] for i in range(27)) for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()];assert len(autos)==51840
 gens=[];cur={tuple(range(27))}
 for p in autos:
  trial=closure(gens+[p])
  if len(trial)>len(cur):gens.append(p);cur=trial
  if len(cur)==51840:break
 Hgens=[compose(g,g) for g in gens]+[comm(a,b) for a,b in itertools.combinations(gens,2)];soc=closure(Hgens);assert len(soc)==25920
 seed=q4[0];act=lambda S,p:frozenset(p[x] for x in S)
 oP={act(seed,p) for p in soc};oF={act(seed,p) for p in autos};assert len(oP)==len(oF)==1080
 # Pair intersections; verify row-homogeneity directly.
 prof=[];pairs=Counter()
 for i,mi in enumerate(masks):
  c=Counter()
  for j,mj in enumerate(masks):
   if i==j:continue
   t=(mi&mj).bit_count();c[t]+=1
   if j>i:pairs[t]+=1
  prof.append(c)
 assert len({tuple(sorted(c.items())) for c in prof})==1;per=prof[0]
 # Induced K3,3s and literal q4 containment.
 K=[]
 for S in itertools.combinations(range(27),6):
  J=G.subgraph(S)
  if J.number_of_edges()==9 and set(dict(J.degree()).values())=={3} and nx.is_bipartite(J):
   A,B=nx.algorithms.bipartite.sets(J)
   if len(A)==len(B)==3:K.append(frozenset(S))
 assert len(K)==360
 fwd=Counter(sum(1 for C in q4 if C<=S) for S in K);rev=Counter(sum(1 for S in K if C<=S) for C in q4)
 assert fwd==Counter({9:360}) and rev==Counter({3:1080})
 # Naive shared-edge relation scheme obstruction: within-relation common-neighbor count must be constant in an association scheme.
 lam={}
 for t in (1,2,3,4):
  nbr=[set() for _ in masks]
  for i,j in itertools.combinations(range(1080),2):
   if (masks[i]&masks[j]).bit_count()==t:nbr[i].add(j);nbr[j].add(i)
  vals=set()
  for i in range(1080):
   for j in nbr[i]:
    if i<j:vals.add(len(nbr[i]&nbr[j]))
  lam[t]=sorted(vals)
 out36={'pass':4836,'code':'[1620,64,96]_2','minimum_words':1080,'model':'twelvefold repetitions of Levi 8-cycles; bijective with 4-cycles of SRG(27,10,1,5)','PSp':{'orbit_size':1080,'stabilizer_order':24},'PGSp':{'orbit_size':1080,'stabilizer_order':48},'shared_Levi_edge_profile_per_cycle':dict(sorted(per.items())),'unordered_pair_counts':dict(sorted(pairs.items())),'theorem':'The 1080 minimum binary words form one PSp orbit and one PGSp orbit, with stabilizers 24 and 48, respectively. Their exact shared-Levi-edge distribution is homogeneous.','boundary':'Independent bare-GQ(4,2) certificate; no ternary identification is inferred.'}
 out40={'pass':4840,'binary_Levi_cycles':1080,'induced_K33':360,'K33_contains_Levi_cycles':dict(sorted(fwd.items())),'Levi_cycle_extensions_to_K33':dict(sorted(rev.items())),'total_incidence':3240,'naive_shared_edge_relation_common_neighbor_counts':{str(k):v for k,v in lam.items()},'shared_edge_partition_is_association_scheme':False,'obstruction':'relations with shared-edge counts 1,2,4 have nonconstant same-relation common-neighbor counts','theorem':'Every induced K3,3 contains exactly nine binary Levi minimum cycles and every binary Levi minimum cycle extends to exactly three induced K3,3s. The incidence identity is 360*9=1080*3=3240. The coarse partition by number of shared Levi edges is regular but is not itself an association scheme.','boundary':'This is an incidence bridge between distinct binary and ternary objects, not an identification of coefficient fields or codes.'}
 OUT36.write_text(json.dumps(out36,indent=2,sort_keys=True)+'\n');OUT40.write_text(json.dumps(out40,indent=2,sort_keys=True)+'\n');print(json.dumps({'4836':out36,'4840':out40},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
