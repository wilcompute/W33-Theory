#!/usr/bin/env python3
"""Passes4863/4864 — the ten-dimensional ternary obstruction is O5(3) adjoint.

Reconstruct the Pass4858 quotient from Levi H1 / oriented-K3,3 span.  Independently
construct PG(4,3) with the standard nondegenerate 5D quadratic form.  Its 36
norm-2 projective points, joined when nonorthogonal, form the same
SRG(36,20,10,12) as the double-six carrier.  Conjugate the exact GQ/PGSp action
to this graph, lift common generators to 5x5 orthogonal matrices, take exterior
square, and solve the simultaneous 10x10 intertwiner equations.

The Hom space is one-dimensional and its nonzero element has rank10.  Finally
identify Lambda^2(V) with so(V) by a^b -> (x |-> <b,x>a-<a,x>b).  Matrix
commutator supplies a Lie bracket; transport it through the intertwiner and
verify center0, derived dimension10, Jacobi, and PGSp invariance.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4863_4864_O5_ADJOINT_HOMOLOGY.json'

def Q6(x):
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
def closure(gens,n):
 I=tuple(range(n));S={I};D=deque([I])
 while D:
  a=D.popleft()
  for g in gens:
   z=comp(g,a)
   if z not in S:S.add(z);D.append(z)
 return S

def main()->int:
 # ----- GQ / quotient 10D module.
 qp=[x for x in range(1,64) if Q6(x)==0];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 ledges=sorted((p,L) for L,S in enumerate(lines) for p in S);lei={e:i for i,e in enumerate(ledges)}
 D=np.zeros((72,135),dtype=int)
 for e,(p,L) in enumerate(ledges):D[p,e]=1;D[45+L,e]=-1
 HB=null(D,3);assert HB.shape==(64,135)
 KV=[]
 for S in itertools.combinations(range(27),6):
  H=G.subgraph(S)
  if H.number_of_edges()!=9 or set(dict(H.degree()).values())!={3} or not nx.is_bipartite(H):continue
  A,B=nx.algorithms.bipartite.sets(H)
  if len(A)!=3 or len(B)!=3:continue
  v=np.zeros(135,dtype=int)
  for a in A:
   for b in B:
    if G.has_edge(a,b):
     p=next(iter(set(lines[a])&set(lines[b])));v[lei[(p,a)]]=1;v[lei[(p,b)]]=2
  KV.append(v)
 KV=np.array(KV);assert KV.shape==(360,135) and rank(KV,3)==54
 sel=[]
 for v in KV:
  if rank(np.array(sel+[v.tolist()]),3)>len(sel):sel.append(v.tolist())
  if len(sel)==54:break
 B64=np.array(sel,dtype=int)
 for v in HB:
  if rank(np.vstack([B64,v]),3)>len(B64):B64=np.vstack([B64,v])
  if len(B64)==64:break
 _,pc=rref(B64,3);Pi=invm(B64[:,pc],3)
 co=lambda v:(np.array(v,dtype=int)[pc]@Pi)%3
 autos=[tuple(m[i] for i in range(27)) for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()];assert len(autos)==51840
 gens=[];cur={tuple(range(27))}
 for p in autos:
  T=closure(gens+[p],27)
  if len(T)>len(cur):gens.append(p);cur=T
  if len(cur)==51840:break
 assert len(gens)==8
 point_lines=[frozenset(L for L,S in enumerate(lines) if p in S) for p in range(45)];pl={T:i for i,T in enumerate(point_lines)}
 def qmat(g):
  pg=[pl[frozenset(g[L] for L in T)] for T in point_lines];ep=[lei[(pg[p],g[L])] for p,L in ledges];R=np.zeros((64,64),dtype=int)
  for i,v in enumerate(B64):
   w=np.zeros(135,dtype=int)
   for j,x in enumerate(v):w[ep[j]]=x
   R[i]=co(w)
  assert not np.any(R[:54,54:]);return R[54:,54:]%3
 QF=[qmat(g) for g in gens]
 # ----- 36 double-sixes and their graph.
 C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6];DS=set()
 for A,B in itertools.combinations(C6,2):
  if A&B:continue
  J=G.subgraph(A|B)
  if len(A|B)==12 and J.number_of_edges()==30 and set(dict(J.degree()).values())=={5} and nx.is_bipartite(J):DS.add(frozenset(A|B))
 DS=sorted(DS,key=lambda S:tuple(sorted(S)));di={S:i for i,S in enumerate(DS)};H36=nx.Graph();H36.add_nodes_from(range(36))
 for i,j in itertools.combinations(range(36),2):
  if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
 carperms=[tuple(di[frozenset(g[x] for x in S)] for S in DS) for g in gens]
 # ----- PG(4,3), natural O5 module, and graph isomorphism.
 proj=[]
 for v in itertools.product(range(3),repeat=5):
  if not any(v):continue
  f=next(x for x in v if x);u=tuple((pow(f,-1,3)*x)%3 for x in v)
  if u==v:proj.append(v)
 prof=Counter(sum(x*x for x in v)%3 for v in proj);assert prof==Counter({1:45,0:40,2:36})
 norm2=[v for v in proj if sum(x*x for x in v)%3==2];O=nx.Graph();O.add_nodes_from(range(36))
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))%3
 for i,j in itertools.combinations(range(36),2):
  if dot(norm2[i],norm2[j]):O.add_edge(i,j)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(H36,O).isomorphisms_iter())
 operms=[]
 for p in carperms:
  q=[0]*36
  for i in range(36):q[iso[i]]=iso[p[i]]
  operms.append(tuple(q))
 bind=next(I for I in itertools.combinations(range(36),5) if rank(np.array([norm2[i] for i in I]),3)==5);V=np.array([norm2[i] for i in bind]);Vi=invm(V,3)
 def canon(v):
  v=np.array(v,dtype=int)%3;k=next(i for i,x in enumerate(v) if x);return tuple((v*pow(int(v[k]),-1,3))%3)
 def lift(p):
  tar=[np.array(norm2[p[i]]) for i in bind]
  for tail in itertools.product((1,2),repeat=4):
   W=np.array([(s*t)%3 for s,t in zip((1,)+tail,tar)]);T=(Vi@W)%3
   if all(canon(np.array(v)@T)==norm2[p[i]] for i,v in enumerate(norm2)):
    assert np.array_equal((T@T.T)%3,np.eye(5,dtype=int));return T
  raise AssertionError
 TF=[lift(p) for p in operms]
 pairs=list(itertools.combinations(range(5),2))
 def wedge(T):
  W=np.zeros((10,10),dtype=int)
  for a,(i,j) in enumerate(pairs):
   for b,(k,l) in enumerate(pairs):W[a,b]=(T[i,k]*T[j,l]-T[i,l]*T[j,k])%3
  return W
 WF=[wedge(T) for T in TF]
 # ----- common-generator intertwiner Q X = X wedge.
 rows=[]
 for A,W in zip(QF,WF):
  for i in range(10):
   for j in range(10):
    z=np.zeros(100,dtype=int)
    for k in range(10):z[k*10+j]=(z[k*10+j]+A[i,k])%3;z[i*10+k]=(z[i*10+k]-W[k,j])%3
    rows.append(z)
 Hom=null(np.array(rows),3);assert Hom.shape==(1,100);X=Hom[0].reshape(10,10)%3;assert rank(X,3)==10
 # ----- Lie bracket on Lambda^2 = so5.
 Sk=[]
 for i,j in pairs:
  A=np.zeros((5,5),dtype=int);A[i,j]=1;A[j,i]=-1;Sk.append(A%3)
 def sco(A):return np.array([A[i,j]%3 for i,j in pairs])
 Bst=np.zeros((10,10,10),dtype=int)
 for a,A in enumerate(Sk):
  for b,B in enumerate(Sk):Bst[a,b]=sco((A@B-B@A)%3)
 def br(x,y):
  z=np.zeros(10,dtype=int)
  for a,xa in enumerate(x):
   if xa:
    for b,yb in enumerate(y):
     if yb:z=(z+xa*yb*Bst[a,b])%3
  return z
 E10=np.eye(10,dtype=int)
 assert rank(Bst.reshape(100,10),3)==10
 cen=[]
 for b in range(10):
  for c in range(10):cen.append([Bst[a,b,c] for a in range(10)])
 assert 10-rank(np.array(cen),3)==0
 for a,b,c in itertools.product(range(10),repeat=3):assert not np.any((br(E10[a],br(E10[b],E10[c]))+br(E10[b],br(E10[c],E10[a]))+br(E10[c],br(E10[a],E10[b])))%3)
 for W in WF:
  for a,b in itertools.product(range(10),repeat=2):assert np.array_equal(br(E10[a]@W,E10[b]@W)%3,(Bst[a,b]@W)%3)
 out={'passes':[4863,4864],'natural_O5_model':{'PG4_3_projective_points':121,'norm_profile':{'0':40,'1':45,'2':36},'norm2_nonorthogonality_graph':'SRG(36,20,10,12)','explicit_isomorphism_to_double_six_graph':True,'common_PGSp_generator_count':8,'all_lifted_generators_orthogonal':True},
  'exterior_square_intertwiner':{'quotient_dimension':10,'Lambda2_dimension':10,'simultaneous_Hom_dimension_F3':1,'unique_nonzero_intertwiner_rank':10,'equivariant_isomorphism':True},
  'Lie_algebra':{'model':'Lambda^2(F3^5) ~= so5(F3) via bivectors to skew endomorphisms','dimension':10,'center_dimension':0,'derived_dimension':10,'Jacobi_verified_on_basis':True,'PGSp_generators_preserve_bracket':True,'classical_identification':'so5(F3) ~= sp4(F3) (type B2=C2 in odd characteristic)'},
  'theorem':'The ten-dimensional ternary homology quotient outside the oriented K3,3 span is explicitly PGSp-equivariantly isomorphic to Lambda^2 of the natural five-dimensional O5(3) module. Under the standard bivector/skew-endomorphism map it is the simple adjoint Lie algebra so5(F3) ~= sp4(F3), with the bracket transported canonically to the homology quotient.',
  'boundary':'Finite characteristic-three module/Lie-algebra theorem. No continuum gauge field, particle multiplet, or physical local Lie symmetry is inferred.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
