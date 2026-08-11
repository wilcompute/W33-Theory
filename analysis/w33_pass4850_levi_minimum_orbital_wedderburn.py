#!/usr/bin/env python3
"""Pass4850 — exact orbital algebra of the 1080 binary Levi minimum shell.

Rebuild the 1080 four-cycles of the GQ(4,2) 27-line graph and the full 51840
automorphism group.  Recover the 25920 derived/square subgroup.  For each group,
construct every stabilizer orbital, the full relation-label matrix, exact
intersection numbers, center equations, and a generic integral central element.
Its regular characteristic polynomial determines the split center and complex
matrix-block multiplicities.  The binary-cycle/K3,3 incidence Gram operator is
located exactly in the PGSp orbital basis.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx,sympy as sp
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4850_LEVI_MINIMUM_ORBITAL_WEDDERBURN.json'

def Q(x):
 b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1
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
def act(S,p):return frozenset(p[x] for x in S)

def algebra(q4,idx,group,stab):
 r=None;unseen=set(range(len(q4)));O=[]
 while unseen:
  i=min(unseen);S={idx[act(q4[i],p)] for p in stab};O.append(sorted(S));unseen-=S
 r=len(O);seed=q4[0]
 rel0=np.empty(len(q4),dtype=np.uint8)
 for j,S in enumerate(O):rel0[S]=j
 trans=[None]*len(q4)
 for p in group:
  t=idx[act(seed,p)]
  if trans[t] is None:trans[t]=p
  if all(z is not None for z in trans):break
 rel=np.empty((len(q4),len(q4)),dtype=np.uint8)
 for x,g in enumerate(trans):
  ig=inv(g);rel[x]=[rel0[idx[act(S,ig)]] for S in q4]
 P=np.zeros((r,r,r),dtype=np.int64)
 for k,S in enumerate(O):
  z=S[0];codes=rel[0].astype(np.int64)*r+rel[:,z].astype(np.int64)
  P[:,:,k]=np.bincount(codes,minlength=r*r).reshape(r,r)
 E=np.zeros((r*r,r),dtype=np.int64);row=0
 for j in range(r):
  for k in range(r):E[row,:]=P[:,j,k]-P[j,:,k];row+=1
 EM=sp.Matrix(E);Z=EM.nullspace();center=r-EM.rank();assert center==len(Z)
 primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59]
 z=sp.zeros(r,1)
 for a,b in zip(primes,Z):z+=a*b
 den=sp.ilcm(*[x.q for x in z]);zi=[int(x*den) for x in z]
 L=np.zeros((r,r),dtype=object)
 for j in range(r):
  for k in range(r):L[k,j]=sum(zi[i]*int(P[i,j,k]) for i in range(r))
 LM=sp.Matrix(L.tolist());cp=sp.factor(LM.charpoly().as_expr());ev=LM.eigenvals()
 return O,rel,P,E,center,cp,Counter(ev.values())

def main()->int:
 qp=[x for x in range(1,64) if Q(x)==0];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 q4=[]
 for S in itertools.combinations(range(27),4):
  H=G.subgraph(S)
  if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):q4.append(frozenset(S))
 assert len(q4)==1080;idx={S:i for i,S in enumerate(q4)};seed=q4[0]
 autos=[tuple(m[i] for i in range(27)) for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()];assert len(autos)==51840
 gens=[];cur={tuple(range(27))}
 for p in autos:
  T=closure(gens+[p])
  if len(T)>len(cur):gens.append(p);cur=T
  if len(cur)==51840:break
 soc=closure([comp(g,g) for g in gens]+[comm(a,b) for a,b in itertools.combinations(gens,2)]);assert len(soc)==25920
 stabF=[p for p in autos if act(seed,p)==seed];stabP=[p for p in soc if act(seed,p)==seed];assert (len(stabF),len(stabP))==(48,24)
 OP,relP,PP,EP,cP,cpP,mP=algebra(q4,idx,soc,stabP);OF,relF,PF,EF,cF,cpF,mF=algebra(q4,idx,autos,stabF)
 assert len(OP)==59 and len(OF)==49 and cP==15 and cF==13
 assert mP==Counter({1:7,4:4,9:4}) and mF==Counter({1:6,4:4,9:3})
 # Every irreducible center factor of PSp is either rational or Q(sqrt(-3)).
 facP=sp.factor_list(cpP)[1];quad=[]
 for f,e in facP:
  if sp.Poly(f).degree()==2:
   d=sp.discriminant(f,sp.Symbol('lambda'));quad.append(int(d))
   sf=sp.factorint(abs(int(d)));assert sf.get(3,0)%2==1 and all((a==3 or v%2==0) for a,v in sf.items())
 assert len(quad)==3
 # PGSp generic center factor is completely linear over Q.
 assert all(sp.Poly(f).degree()==1 for f,e in sp.factor_list(cpF)[1])

 # Build 1080x360 K3,3 incidence and locate M M^T in the PGSp orbital basis.
 K=[]
 for S in itertools.combinations(range(27),6):
  H=G.subgraph(S)
  if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
   A,B=nx.algorithms.bipartite.sets(H)
   if len(A)==len(B)==3:K.append(frozenset(S))
 M=np.zeros((1080,360),dtype=np.uint8)
 for j,S in enumerate(K):M[[i for i,C in enumerate(q4) if C<=S],j]=1
 MM=M.astype(np.int16)@M.T.astype(np.int16)
 ledges=sorted((p,L) for L,S in enumerate(lines) for p in S);lei={e:i for i,e in enumerate(ledges)}
 masks=[]
 for S in q4:
  z=0
  for a,b in G.subgraph(S).edges():
   p=next(iter(set(lines[a])&set(lines[b])));z|=1<<lei[(p,a)];z|=1<<lei[(p,b)]
  masks.append(z)
 tags=[]
 for j,S in enumerate(OF):
  z=S[0];shared=(masks[0]&masks[z]).bit_count();inc=int(MM[0,z]);assert {int(MM[0,t]) for t in S}=={inc};tags.append((len(S),shared,inc))
 nz=[j for j,t in enumerate(tags) if t[2]];assert nz==[0,1,5] and [tags[j][2] for j in nz]==[3,1,1]
 mmcoef=np.zeros(49,dtype=int);mmcoef[0]=3;mmcoef[1]=mmcoef[5]=1
 assert np.any(EF@mmcoef)
 Eq=np.zeros((49,49),dtype=int)
 for k in range(49):
  for i in range(49):Eq[k,i]=sum(mmcoef[j]*(PF[i,j,k]-PF[j,i,k]) for j in range(49))
 mmcomm=49-sp.Matrix(Eq).rank();assert mmcomm==27
 out={'pass':4850,
  'PSp':{'orbital_dimension':59,'center_dimension':15,'complex_Wedderburn':'C^7 x M2(C)^4 x M3(C)^4','rational_center':'Q^9 x Q(sqrt(-3))^3','generic_central_charpoly':str(cpP),'regular_eigenvalue_multiplicity_census':{str(k):v for k,v in sorted(mP.items())}},
  'PGSp':{'orbital_dimension':49,'center_dimension':13,'complex_Wedderburn':'C^6 x M2(C)^4 x M3(C)^3','rational_center':'Q^13','generic_central_charpoly':str(cpF),'regular_eigenvalue_multiplicity_census':{str(k):v for k,v in sorted(mF.items())}},
  'outer_action':'The PGSp outer extension lowers permutation rank 59->49 and center dimension 15->13; the PSp rational center has three Eisenstein Q(sqrt(-3)) factors whereas the PGSp center is completely split over Q.',
  'coarse_operator_embedding':{'shared_Levi_edge_orbital_count_census':{str(k):v for k,v in sorted(Counter(t[1] for t in tags).items())},'K33_incidence_Gram':'M M^T = 3 A_0 + A_1 + A_5 in deterministic PGSp orbital order','nonzero_orbitals':[0,1,5],'subdegrees':[tags[j][0] for j in nz],'shared_Levi_edges':[tags[j][1] for j in nz],'is_central':False,'commutant_dimension_inside_orbital_algebra':27},
  'theorem':'The exact 1080-point orbital algebras are noncommutative. Over C the PSp algebra is C^7 x M2^4 x M3^4 and the PGSp algebra is C^6 x M2^4 x M3^3. The PSp rational center retains three Q(sqrt(-3)) components, while the outer extension yields a fully rational PGSp center Q^13. The K3,3 incidence Gram occupies only three PGSp orbitals and is not central.',
  'boundary':'Complex matrix-block sizes and rational centers are exact. Split-versus-division status of every noncommutative rational simple block is not asserted without explicit rational matrix units.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
