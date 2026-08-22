#!/usr/bin/env python3
"""Pass7329-7336: identify the seven characteristic-3 Smith directions as an E6 module extension."""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np, sympy as sp, networkx as nx
from w33_pass4992_4999_common import build_base
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data'/'PART_W33_PASS7329_7336_CHAR3_E6_DEFECT.json'

def rr(A,p=3):
 A=np.asarray(A,dtype=np.int64).copy()%p;m,n=A.shape;r=0;pv=[]
 for c in range(n):
  z=next((i for i in range(r,m) if A[i,c]),None)
  if z is None: continue
  A[[r,z]]=A[[z,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(m):
   if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%p
  pv.append(c);r+=1
  if r==m: break
 return A,pv

def rank(A): return len(rr(A)[1])
def ns(A):
 R,pv=rr(A);n=R.shape[1];free=[j for j in range(n) if j not in pv];B=[]
 for f in free:
  v=np.zeros(n,dtype=np.int64);v[f]=1
  for i,c in enumerate(pv):v[c]=(-R[i,f])%3
  B.append(v)
 return B

def basis(B):
 C=[]
 for v in B:
  if rank(C+[v])>len(C):C.append(np.asarray(v,dtype=np.int64)%3)
 return C

def coord(v,B):
 B=np.asarray(B,dtype=np.int64)%3;v=np.asarray(v,dtype=np.int64)%3
 R,pv=rr(np.column_stack((B.T,v)));c=np.zeros(len(B),dtype=np.int64)
 for i,j in enumerate(pv):
  if j<len(B):c[j]=R[i,len(B)]
 assert np.array_equal(c@B%3,v);return c

def pvec(v,g):
 w=np.zeros_like(v)
 for i,j in enumerate(g):w[j]=v[i]
 return w

def orbitspan(v,M):
 B=basis([v]);changed=True
 while changed:
  changed=False
  for x in list(B):
   for A in M:
    C=basis(B+[A@x%3])
    if len(C)>len(B):B=C;changed=True
 return B

def e6(base):
 C=np.eye(6,dtype=int)*2
 for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
 def rf(v,i):
  v=np.array(v,dtype=int);w=v.copy();w[i]-=int(v@C[:,i]);return tuple(map(int,w))
 roots={(1,0,0,0,0,0)};q=deque(roots)
 while q:
  v=q.popleft()
  for i in range(6):
   w=rf(v,i)
   if w not in roots:roots.add(w);q.append(w)
 pos=sorted(v for v in roots if all(x>=0 for x in v));pi={v:i for i,v in enumerate(pos)};assert len(pos)==36
 G=nx.Graph();G.add_nodes_from(range(36))
 for a,b in itertools.combinations(range(36),2):
  if abs(int(np.array(pos[a])@C@np.array(pos[b])))==1:G.add_edge(a,b)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(base['H36'],G).isomorphisms_iter());iv={r:d for d,r in iso.items()}
 perms=[];mats=[]
 for i in range(6):
  rp=[]
  for r in pos:
   z=rf(r,i);z=z if z in pi else tuple(-x for x in z);rp.append(pi[z])
  perms.append(tuple(iv[rp[iso[d]]] for d in range(36)))
  S=np.zeros((6,6),dtype=int)
  for j in range(6):
   x=np.zeros(6,dtype=int);x[j]=1;S[:,j]=np.array(rf(tuple(x),i))%3
  mats.append(S%3)
 return perms,mats

def hom(M7,M6):
 E=[]
 for A,S in zip(M7,M6):
  for r in range(7):
   for c in range(6):
    q=np.zeros(42,dtype=int)
    for k in range(7):q[k*6+c]+=A[r,k]
    for k in range(6):q[r*6+k]-=S[k,c]
    E.append(q%3)
 return [v.reshape(7,6)%3 for v in ns(E)]

def main():
 b=build_base();N=1-np.asarray(b['M'],dtype=int)
 qn=sp.Matrix(N).nullspace();assert len(qn)==15;K=[]
 for v in qn:
  d=sp.ilcm(*[x.q for x in v]);w=np.array([int(d*x) for x in v],dtype=int);g=np.gcd.reduce(np.abs(w[w!=0]));K.append(w//g%3)
 K=basis(K);assert len(K)==15;K22=basis(ns(N));assert len(K22)==22
 full=list(K);T=[]
 for v in K22:
  if rank(full+[v])>len(full):full.append(v);T.append(v)
 assert len(T)==7
 perms,R6=e6(b);M7=[]
 for g in perms:
  A=np.zeros((7,7),dtype=int)
  for i,t in enumerate(T):A[:,i]=coord(pvec(t,g),full)[15:]
  M7.append(A%3)
 F=ns(np.vstack([(A-np.eye(7,dtype=int))%3 for A in M7]));assert len(F)==1
 DF=ns(np.vstack([(A.T-np.eye(7,dtype=int))%3 for A in M7]));assert len(DF)==1;ell=DF[0]
 U=ns([ell]);assert len(U)==6 and all(np.dot(ell,x)%3==0 for x in F)
 cen=Counter()
 for n in range(1,3**7):
  z=n;a=[]
  for _ in range(7):a.append(z%3);z//=3
  cen[len(orbitspan(np.array(a),M7))]+=1
 assert cen==Counter({7:1458,6:726,1:2})
 rfix=ns(np.vstack([(S-np.eye(6,dtype=int))%3 for S in R6]));assert len(rfix)==1
 rc=Counter()
 for n in range(1,3**6):
  z=n;a=[]
  for _ in range(6):a.append(z%3);z//=3
  rc[len(orbitspan(np.array(a),R6))]+=1
 assert rc==Counter({6:726,1:2})
 H=hom(M7,R6);assert len(H)==1 and rank(H[0])==6 and all(np.all((A@H[0]-H[0]@S)%3==0) for A,S in zip(M7,R6))
 out={'schema':'w33.pass7329_7336.char3_e6_defect.v1','status':'PASS','passes':'7329-7336','rank_Q':21,'rank_F3':14,'kernel_Q_reduction_rank':15,'kernel_F3':22,'defect_dimension':7,'T7_submodule_chain':'0 < 1 < U6 < T7','composition_factors':'1|5|1','T7_cyclic_submodule_census':{str(k):v for k,v in sorted(cen.items())},'E6_root_module_census':{str(k):v for k,v in sorted(rc.items())},'Hom_dimension':1,'intertwiner_rank':6,'theorem':'U6 is explicitly the E6 root-lattice module mod 3; its fixed radical line has irreducible 5D quotient; T7/U6 is trivial','boundary':'Exact modular W(E6) representation theorem; no physical meaning is assigned to the extension class.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','defect':7,'composition':'1|5|1','hom_rank':6}))
if __name__=='__main__':main()
