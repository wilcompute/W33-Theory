#!/usr/bin/env python3
"""Pass4858 — exact 10-dimensional ternary obstruction module.

Construct GQ(4,2), its Levi H1 over F3, and the 54-dimensional span of the
canonical oriented K3,3 witnesses.  Build the induced PSp/PGSp actions on the
10-dimensional quotient, compute endomorphism rings, and exhaust all projective
vectors to prove irreducibility without importing a representation label.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4858_TERNARY_TEN_MODULE.json'

def Q(x):
 b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1

def rref(M,p=3):
 A=np.array(M,dtype=int)%p;r=0;piv=[]
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  piv.append(c);r+=1
 return A,piv

def rank(M,p=3):return len(rref(M,p)[1])
def null(M,p=3):
 R,piv=rref(M,p);free=[c for c in range(R.shape[1]) if c not in piv];out=[]
 for f in free:
  x=np.zeros(R.shape[1],dtype=int);x[f]=1
  for i,c in enumerate(piv):x[c]=(-R[i,f])%p
  out.append(x)
 return np.array(out,dtype=int)
def invm(A,p=3):
 A=np.array(A,dtype=int)%p;n=A.shape[0];X=np.c_[A,np.eye(n,dtype=int)]
 for c in range(n):
  q=next(i for i in range(c,n) if X[i,c]);X[[c,q]]=X[[q,c]];X[c]=(X[c]*pow(int(X[c,c]),-1,p))%p
  for i in range(n):
   if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%p
 return X[:,n:]%p
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def invp(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def comm(a,b):return comp(comp(comp(a,b),invp(a)),invp(b))
def closure(gens,n=27):
 I=tuple(range(n));S={I};D=deque([I])
 while D:
  a=D.popleft()
  for g in gens:
   z=comp(g,a)
   if z not in S:S.add(z);D.append(z)
 return S

def main()->int:
 qp=[x for x in range(1,64) if Q(x)==0];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 ledges=sorted((p,L) for L,S in enumerate(lines) for p in S);lei={e:i for i,e in enumerate(ledges)}
 D=np.zeros((72,135),dtype=int)
 for e,(p,L) in enumerate(ledges):D[p,e]=1;D[45+L,e]=-1
 HB=null(D,3);assert HB.shape==(64,135)
 K=[];KV=[]
 for S in itertools.combinations(range(27),6):
  H=G.subgraph(S)
  if H.number_of_edges()!=9 or set(dict(H.degree()).values())!={3} or not nx.is_bipartite(H):continue
  A,B=nx.algorithms.bipartite.sets(H)
  if len(A)!=3 or len(B)!=3:continue
  K.append(frozenset(S));v=np.zeros(135,dtype=int)
  for a in A:
   for b in B:
    if G.has_edge(a,b):
     p=next(iter(set(lines[a])&set(lines[b])));v[lei[(p,a)]]=1;v[lei[(p,b)]]=2
  assert not np.any((D@v)%3);KV.append(v)
 KV=np.array(KV,dtype=int);assert len(K)==360 and rank(KV,3)==54
 # basis first 54 K3,3-span then 10 complement rows
 sel=[]
 for v in KV:
  if rank(np.array(sel+[v.tolist()]),3)>len(sel):sel.append(v.tolist())
  if len(sel)==54:break
 B64=np.array(sel,dtype=int)
 for v in HB:
  if rank(np.vstack([B64,v]),3)>len(B64):B64=np.vstack([B64,v])
  if len(B64)==64:break
 assert B64.shape==(64,135)
 _,pc=rref(B64,3);P=B64[:,pc];Pi=invm(P,3)
 co=lambda v:(np.array(v,dtype=int)[pc]@Pi)%3
 # full graph automorphism group and PSp socle
 autos=[tuple(m[i] for i in range(27)) for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()];assert len(autos)==51840
 gens=[];cur={tuple(range(27))}
 for p in autos:
  T=closure(gens+[p])
  if len(T)>len(cur):gens.append(p);cur=T
  if len(cur)==51840:break
 soc=closure([comp(g,g) for g in gens]+[comm(a,b) for a,b in itertools.combinations(gens,2)]);assert len(soc)==25920
 sg=[];cur={tuple(range(27))}
 for p in soc:
  T=closure(sg+[p])
  if len(T)>len(cur):sg.append(p);cur=T
  if len(cur)==25920:break
 point_lines=[frozenset(L for L,S in enumerate(lines) if p in S) for p in range(45)];pl={T:i for i,T in enumerate(point_lines)}
 def qmat(g):
  pg=[pl[frozenset(g[L] for L in T)] for T in point_lines];ep=[lei[(pg[p],g[L])] for p,L in ledges]
  R=np.zeros((64,64),dtype=int)
  for i,v in enumerate(B64):
   w=np.zeros(135,dtype=int)
   for j,x in enumerate(v):w[ep[j]]=x
   R[i]=co(w)
  assert not np.any(R[:54,54:]);return R[54:,54:]%3
 QP=[qmat(g) for g in sg];QF=[qmat(g) for g in gens]
 def enddim(ms):
  rows=[];n=10
  for A in ms:
   for i in range(n):
    for j in range(n):
     z=np.zeros(n*n,dtype=int)
     for k in range(n):z[i*n+k]+=A[k,j];z[k*n+j]-=A[i,k]
     rows.append(z%3)
  return 100-rank(np.array(rows),3)
 assert enddim(QP)==enddim(QF)==1
 def cyclic_dim(v,ms):
  B=[];pos=0
  def add(x):
   x=np.array(x,dtype=int)%3
   if not np.any(x):return
   if rank(np.array(B+[x.tolist()]),3)>len(B):B.append(x.tolist())
  add(v)
  while pos<len(B) and len(B)<10:
   x=np.array(B[pos]);pos+=1
   for A in ms:add(x@A)
  return len(B)
 profile={}
 tested=0
 for n in range(1,3**10):
  x=n;v=[]
  for _ in range(10):v.append(x%3);x//=3
  if next(z for z in v if z)!=1:continue
  d=cyclic_dim(np.array(v),QP);profile[d]=profile.get(d,0)+1;tested+=1
 assert profile=={10:29524}
 out={'pass':4858,'ambient_Levi_H1_dimension_F3':64,'oriented_K33_span_dimension_F3':54,'quotient_dimension_F3':10,
  'PSp':{'order':25920,'endomorphism_ring_dimension_F3':1,'projective_vectors_tested':tested,'cyclic_span_profile':{str(k):v for k,v in profile.items()},'irreducible':True,'absolutely_irreducible':True},
  'PGSp':{'order':51840,'endomorphism_ring_dimension_F3':1,'irreducible':True,'absolutely_irreducible':True,'extension_of_PSp_module':True},
  'ATLAS_crosscheck':'ATLAS lists the faithful 10-dimensional GF(3) irreducible of U4(2)=PSp(4,3); since PSp is simple, this nontrivial 10D quotient is faithful and the exhaustive irreducibility certificate places it in that 10D isomorphism class.',
  'theorem':'The ten ternary homology dimensions outside the canonical K3,3 span form an absolutely irreducible 10-dimensional PSp(4,3)-module over F3, and the action extends absolutely irreducibly to PGSp(4,3). The PSp and PGSp endomorphism rings are both exactly F3.',
  'boundary':'No identification with Lambda^2 of the natural 5D O5(3) module is promoted here without an explicit common-generator intertwiner; that stronger identification is reserved for a separate probe.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
