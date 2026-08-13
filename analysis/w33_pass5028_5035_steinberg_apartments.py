#!/usr/bin/env python3
"""Passes 5028-5035: exact W33 cover-building continuation.

Reconstructs W(3,3) from F_3^4 and verifies the chamber Steinberg projector,
1620 apartments, apartment/cover spectrum, three critical groups, apartment
orbit/stabilizers, and the homology representation ledger.  Requires numpy.
"""
from __future__ import annotations
from collections import Counter, deque
from itertools import combinations, product
from math import lcm, sqrt
import json
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parents[1]/"data/PART_W33_PASS5028_5035_STEINBERG_APARTMENTS_RESULTS.json"
def norm(v):
 v=tuple(x%3 for x in v);i=next(i for i,x in enumerate(v) if x);a=1 if v[i]==1 else 2;return tuple(a*x%3 for x in v)
def symp(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
def vp(a,p,K):
 a%=p**K
 if a==0:return K
 e=0
 while a%p==0:a//=p;e+=1
 return e
def psnf(M,p,K):
 A=[list(map(int,r)) for r in np.array(M,dtype=object)];n=len(A);m=len(A[0]);mod=p**K;r=0;out=[]
 for i in range(n):
  for j in range(m):A[i][j]%=mod
 while r<min(n,m):
  best=K;pos=None
  for i in range(r,n):
   for j in range(r,m):
    e=vp(A[i][j],p,K)
    if e<best:best=e;pos=(i,j)
    if best==0:break
   if best==0:break
  if pos is None or best>=K:out += [K]*(min(n,m)-r);break
  i,j=pos;A[r],A[i]=A[i],A[r]
  for row in A:row[r],row[j]=row[j],row[r]
  pe=p**best;inv=pow((A[r][r]//pe)%mod,-1,mod)
  for jj in range(r,m):A[r][jj]=A[r][jj]*inv%mod
  for ii in range(r+1,n):
   a=A[ii][r]%mod
   if a:
    c=a//pe
    for jj in range(r,m):A[ii][jj]=(A[ii][jj]-c*A[r][jj])%mod
  for jj in range(r+1,m):
   a=A[r][jj]%mod
   if a:
    c=a//pe
    for ii in range(r,n):A[ii][jj]=(A[ii][jj]-c*A[ii][r])%mod
  out.append(best);r+=1
 return out
def crit(M):
 e2=sorted(psnf(M,2,180));e5=sorted(psnf(M,5,40));return Counter(2**a*5**b for a,b in zip(e2,e5) if 2**a*5**b!=1)
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def closure(gens,n,cap):
 I=tuple(range(n));G={I};todo=[I]
 while todo:
  a=todo.pop()
  for g in gens:
   b=compose(g,a)
   if b not in G:
    G.add(b);todo.append(b)
    if len(G)>cap:raise RuntimeError("group cap")
 return G
def main():
 pts=[]
 for v in product(range(3),repeat=4):
  if any(v) and norm(v) not in pts:pts.append(norm(v))
 pi={v:i for i,v in enumerate(pts)};A=np.zeros((40,40),dtype=np.int64)
 for i,u in enumerate(pts):
  for j,v in enumerate(pts):A[i,j]=int(i!=j and symp(u,v)==0)
 lines=[c for c in combinations(range(40),4) if all(A[i,j] for i,j in combinations(c,2))];assert len(lines)==40
 N=np.zeros((40,40),dtype=np.int64);pl={}
 for l,L in enumerate(lines):
  for p in L:N[p,l]=1
  for a,b in combinations(L,2):pl[tuple(sorted((a,b)))]=l
 flags=[(p,l) for l,L in enumerate(lines) for p in L];fi={f:i for i,f in enumerate(flags)};assert len(flags)==160
 Alev=np.block([[np.zeros((40,40),dtype=np.int64),N],[N.T,np.zeros((40,40),dtype=np.int64)]])
 Llev=np.diag(Alev.sum(1))-Alev;D=np.zeros((80,160),dtype=np.int64)
 for j,(p,l) in enumerate(flags):D[p,j]=1;D[40+l,j]=-1
 aps=[c for c in combinations(range(40),4) if np.all(A[np.ix_(c,c)].sum(1)==2)];assert len(aps)==1620
 def cyc(ps):
  ps=list(ps);s=min(ps);a=min(x for x in ps if A[s,x]);b=next(x for x in ps if x not in (s,a) and A[a,x]);c=next(x for x in ps if x not in (s,a,b));assert A[b,c] and A[c,s];return [s,a,b,c]
 X=np.zeros((160,1620),dtype=np.int64);Y=np.zeros((1620,200),dtype=np.int64);B=np.zeros((1620,40),dtype=np.int64)
 for k,ps in enumerate(aps):
  C=cyc(ps)
  for p in ps:Y[k,p]=1
  for i in range(4):
   p,q=C[i],C[(i+1)%4];l=pl[tuple(sorted((p,q)))];B[k,l]=1;u,v=fi[(p,l)],fi[(q,l)];X[u,k]=1;X[v,k]=-1;Y[k,40+u]=Y[k,40+v]=1
 adj=[[] for _ in flags]
 for i,(p,l) in enumerate(flags):
  for j,(q,m) in enumerate(flags):
   if i!=j and ((p==q)^(l==m)):adj[i].append(j)
 dist=np.zeros((160,160),dtype=np.int8)
 for s in range(160):
  d=[-1]*160;d[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
  dist[s]=d
 R=np.array([[(-1)**int(dist[i,j])*3**(4-int(dist[i,j])) for j in range(160)] for i in range(160)],dtype=np.int64)
 assert np.array_equal(X@X.T,R) and np.array_equal(R@R,160*R) and np.all(D@R==0) and np.linalg.matrix_rank(X.astype(float))==81
 ev=np.sort(np.linalg.eigvalsh((Y.T@Y).astype(float)));want=np.sort(np.array([0.]*40+[40.]*81+[72.]*15+[144.]*15+[243-9*sqrt(409)]*24+[243+9*sqrt(409)]*24+[1296.]));assert np.max(abs(ev-want))<1e-7
 edges=[(i,j) for i in range(80) for j in range(i+1,80) if Alev[i,j]];As=np.zeros((240,240),dtype=np.int64)
 for k,(i,j) in enumerate(edges):b=80+k;As[i,b]=As[b,i]=As[j,b]=As[b,j]=1
 Lsub=np.diag(As.sum(1))-As
 Asu=np.zeros((240,240),dtype=np.int64)
 for l,L in enumerate(lines):
  z=200+l
  for p in L:Asu[p,z]=Asu[z,p]=1;f=40+fi[(p,l)];Asu[f,z]=Asu[z,f]=1
 Lsup=np.diag(Asu.sum(1))-Asu
 Klev=crit(Llev[:-1,:-1]);Ksup=crit(Lsup[:-1,:-1]);Ksub=crit(Lsub[:-1,:-1]);assert Klev==Counter({4:6,40:22,160:1}) and Ksup==Klev and Ksub==Counter({2:52,8:6,80:22,320:1})
 lineA=N.T@N-4*np.eye(40,dtype=np.int64);assert np.array_equal(B.T@B,156*np.eye(40,dtype=np.int64)+21*lineA+6*np.ones((40,40),dtype=np.int64))
 def tp(v):
  return tuple(pi[norm(tuple((x[i]+symp(x,v)*v[i])%3 for i in range(4)))] for x in pts)
 gens=[tp(v) for v in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(0,1,1,2),(1,1,0,2)]]
 P=closure(gens,40,30000);assert len(P)==25920
 sim=tuple(pi[norm((x[0],x[1],2*x[2]%3,2*x[3]%3))] for x in pts);PG=closure(gens+[sim],40,60000);assert len(PG)==51840
 base=frozenset(aps[0]);orb={base};todo=[base]
 while todo:
  S=todo.pop()
  for g in gens:
   T=frozenset(g[x] for x in S)
   if T not in orb:orb.add(T);todo.append(T)
 assert len(orb)==1620 and sum(frozenset(g[x] for x in base)==base for g in P)==16 and sum(frozenset(g[x] for x in base)==base for g in PG)==32
 assert Counter(map(int,Y.sum(0)))==Counter({81:160,162:40}) and Counter(map(int,B.sum(0)))==Counter({162:40})
 out={"status":"PASS","checks":{"points":40,"lines":40,"chambers":160,"apartments":1620,"steinberg_rank":81,"R2":"160R","apartment_frame":"XX^T=R=160P_St","apartment_cover_rank":160,"critical_levi":dict(Klev),"critical_support":dict(Ksup),"critical_subdivision":dict(Ksub),"PSp_apartment_orbit":1620,"PSp_apartment_stabilizer":16,"PGSp_apartment_stabilizer":32}}
 OUT.write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
