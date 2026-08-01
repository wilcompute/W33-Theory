"""Shared exact W(3,3) geometry for Passes 1801--1805."""
from __future__ import annotations
import itertools
from typing import Iterable
import networkx as nx
import numpy as np
Q=3
OMEGA=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=np.int64)%Q

def norm(v:Iterable[int])->tuple[int,...]:
 v=tuple(int(x)%Q for x in v)
 for x in v:
  if x:
   inv=1 if x==1 else 2
   return tuple(inv*y%Q for y in v)
 raise ValueError('zero vector')
def symp(a,b)->int:return int(np.array(a,dtype=np.int64)@OMEGA@np.array(b,dtype=np.int64)%Q)
def rank_mod(matrix:np.ndarray,p:int)->int:
 a=np.array(matrix,dtype=np.int64)%p;m,n=a.shape;r=0
 for c in range(n):
  nz=np.flatnonzero(a[r:,c])
  if not len(nz):continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]]
  a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  nz=np.flatnonzero(a[:,c]);nz=nz[nz!=r]
  for j in nz:a[j]=(a[j]-a[j,c]*a[r])%p
  r+=1
  if r==m:break
 return r
def basis_columns(matrix:np.ndarray,p:int)->list[int]:
 a=np.array(matrix,dtype=np.int64)%p;m,n=a.shape;r=0;out=[]
 for c in range(n):
  nz=np.flatnonzero(a[r:,c])
  if not len(nz):continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]]
  a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  nz=np.flatnonzero(a[:,c]);nz=nz[nz!=r]
  for j in nz:a[j]=(a[j]-a[j,c]*a[r])%p
  out.append(c);r+=1
  if r==m:break
 return out
def rowspace_basis(rows:np.ndarray,p:int=2)->np.ndarray:
 a=np.array(rows,dtype=np.int64)%p
 if a.ndim==1:a=a.reshape(1,-1)
 if not a.size:return np.zeros((0,a.shape[1]),dtype=np.uint8)
 m,n=a.shape;r=0
 for c in range(n):
  nz=np.flatnonzero(a[r:,c])
  if not len(nz):continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]]
  a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  nz=np.flatnonzero(a[:,c]);nz=nz[nz!=r]
  for j in nz:a[j]=(a[j]-a[j,c]*a[r])%p
  r+=1
  if r==m:break
 return a[:r].astype(np.uint8 if p==2 else np.int64)
def nullspace(matrix:np.ndarray,p:int=2)->np.ndarray:
 a=np.array(matrix,dtype=np.int64)%p;m,n=a.shape;r=0;piv=[]
 for c in range(n):
  nz=np.flatnonzero(a[r:,c])
  if not len(nz):continue
  i=r+int(nz[0]);a[[r,i]]=a[[i,r]]
  a[r]=a[r]*pow(int(a[r,c]),-1,p)%p
  nz=np.flatnonzero(a[:,c]);nz=nz[nz!=r]
  for j in nz:a[j]=(a[j]-a[j,c]*a[r])%p
  piv.append(c);r+=1
  if r==m:break
 free=[c for c in range(n) if c not in piv];out=[]
 for f in free:
  v=np.zeros(n,dtype=np.int64);v[f]=1
  for i in range(r-1,-1,-1):v[piv[i]]=(-int(np.dot(a[i],v)))%p
  out.append(v)
 return np.array(out,dtype=np.uint8 if p==2 else np.int64)
def inv_mod(a:np.ndarray,p:int)->np.ndarray:
 a=np.array(a,dtype=np.int64)%p;n=a.shape[0];aug=np.c_[a,np.eye(n,dtype=np.int64)]%p
 for c in range(n):
  nz=np.flatnonzero(aug[c:,c]);assert len(nz)
  i=c+int(nz[0]);aug[[c,i]]=aug[[i,c]]
  aug[c]=aug[c]*pow(int(aug[c,c]),-1,p)%p
  for j in range(n):
   if j!=c and aug[j,c]:aug[j]=(aug[j]-aug[j,c]*aug[c])%p
 return aug[:,n:]%p
def complete_basis(subspace:np.ndarray,n:int,p:int=2)->np.ndarray:
 s=rowspace_basis(subspace,p);cols=[v.copy() for v in s]
 b=np.column_stack(cols) if cols else np.zeros((n,0),dtype=np.int64);r=len(cols)
 for i in range(n):
  e=np.zeros(n,dtype=np.int64);e[i]=1
  if rank_mod(np.column_stack([b,e]),p)>r:cols.append(e);b=np.column_stack(cols);r+=1
  if r==n:break
 return b%p
def transform_module(gens:list[np.ndarray],subspace:np.ndarray,p:int=2,extra:np.ndarray|None=None):
 s=rowspace_basis(subspace,p);n=gens[0].shape[0];d=len(s);b=complete_basis(s,n,p);bi=inv_mod(b,p)
 mats=[]
 for g in gens+([] if extra is None else [extra]):
  t=(bi@g@b)%p;assert not np.any(t[d:,:d]);mats.append(t)
 subs=[x[:d,:d] for x in mats[:len(gens)]];quos=[x[d:,d:] for x in mats[:len(gens)]]
 if extra is None:return subs,quos,b,bi
 return subs,quos,b,bi,mats[-1][:d,:d],mats[-1][d:,d:]
def transvection(v)->np.ndarray:
 v=np.array(v,dtype=np.int64)%Q
 return (np.eye(4,dtype=np.int64)+np.outer(v,OMEGA@v))%Q

def build_geometry():
 points=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)});pidx={p:i for i,p in enumerate(points)}
 graph=nx.Graph();graph.add_nodes_from(range(40))
 for i,j in itertools.combinations(range(40),2):
  if symp(points[i],points[j])==0:graph.add_edge(i,j)
 edges=sorted(tuple(sorted(e)) for e in graph.edges());eidx={e:i for i,e in enumerate(edges)}
 lines=set()
 for i,j in edges:
  a=np.array(points[i]);b=np.array(points[j]);span={norm((u*a+v*b)%Q) for u,v in itertools.product(range(Q),repeat=2) if u or v}
  lines.add(tuple(sorted(pidx[x] for x in span)))
 lines=sorted(lines);lidx={l:i for i,l in enumerate(lines)}
 frames=[];matchings=[]
 for li,lj in itertools.combinations(range(40),2):
  left,right=lines[li],lines[lj]
  if set(left)&set(right):continue
  matching=[]
  for a in left:
   partners=[b for b in right if graph.has_edge(a,b)];assert len(partners)==1
   matching.append(eidx[tuple(sorted((a,partners[0])))])
  frames.append((li,lj));matchings.append(tuple(sorted(matching)))
 fidx={f:i for i,f in enumerate(frames)}
 m=np.zeros((540,240),dtype=np.uint8)
 for r,s in enumerate(matchings):m[r,list(s)]=1
 independent=[s for s in itertools.combinations(range(40),4) if graph.subgraph(s).number_of_edges()==0]
 octets=set()
 for left in independent:
  common=set(range(40))-set(left)
  for x in left:common&=set(graph[x])
  if len(common)==4:
   right=tuple(sorted(common))
   if graph.subgraph(right).number_of_edges()==0:octets.add(tuple(sorted((tuple(left),right))))
 octets=sorted(octets);oidx={tuple(sorted(o)):i for i,o in enumerate(octets)}
 k=np.zeros((45,240),dtype=np.uint8)
 for r,(left,right) in enumerate(octets):
  for a in left:
   for b in right:k[r,eidx[tuple(sorted((a,b)))]]=1
 def point_perm(a):return tuple(pidx[norm(a@np.array(p))] for p in points)
 def induced(pp):
  ep=tuple(eidx[tuple(sorted((pp[a],pp[b])))] for a,b in edges)
  lp=tuple(lidx[tuple(sorted(pp[x] for x in line))] for line in lines)
  fp=tuple(fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
  op=[];os=[]
  for left,right in octets:
   li=tuple(sorted(pp[x] for x in left));ri=tuple(sorted(pp[x] for x in right));j=oidx[tuple(sorted((li,ri)))]
   op.append(j);os.append(1 if li==octets[j][0] else -1)
  return pp,ep,lp,fp,tuple(op),tuple(os)
 mats=[transvection(v) for v in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]]
 acts=[induced(point_perm(a)) for a in mats]
 outer=induced(point_perm(np.diag([1,2,1,2])%Q))
 return {'points':points,'graph':graph,'edges':edges,'lines':lines,'frames':frames,'octets':octets,'M':m,'K':k,'acts':acts,'outer':outer,'eidx':eidx}
def permute_rows(v:np.ndarray,p:tuple[int,...])->np.ndarray:
 out=np.zeros_like(v);out[np.array(p)]=v;return out
def build_bockstein(data):
 m=data['M'];k=data['K'];j=((m.astype(np.int64)@k.T.astype(np.int64))//2%2).astype(np.uint8)
 pm=basis_columns(m,2);base=m[:,pm];extra=[];cur=base.copy();r=len(pm)
 for q in range(45):
  cand=np.column_stack([cur,j[:,q]]);rr=rank_mod(cand,2)
  if rr>r:extra.append(q);cur=cand;r=rr
 assert (len(pm),len(extra),r)==(195,30,225)
 rows=basis_columns(cur.T,2);square=cur[rows,:];solver=inv_mod(square,2)
 def coords(v):return (solver@np.array(v,dtype=np.int64)[rows])%2
 beta=np.column_stack([coords(j[:,q])[195:] for q in range(45)])%2
 qgens=[]
 for act in data['acts']:
  qgens.append(np.column_stack([coords(permute_rows(j[:,q],act[3]))[195:] for q in extra])%2)
 qout=np.column_stack([coords(permute_rows(j[:,q],data['outer'][3]))[195:] for q in extra])%2
 return {'J':j,'Beta':beta.astype(np.uint8),'Qgens':[x.astype(np.uint8) for x in qgens],'Qout':qout.astype(np.uint8)}
