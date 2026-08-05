#!/usr/bin/env python3
import itertools, collections
import numpy as np
Q=3

def normalize(v):
 w=tuple(int(x)%Q for x in v)
 for x in w:
  if x:
   z=1 if x==1 else 2
   return tuple(z*y%Q for y in w)
 raise ValueError

def symp(u,v): return (u[0]*v[3]-u[3]*v[0]+u[1]*v[2]-u[2]*v[1])%Q

def geometry():
 points=sorted({normalize(v) for v in itertools.product(range(3),repeat=4) if any(v)})
 A=np.zeros((40,40),dtype=np.int8)
 for i,j in itertools.combinations(range(40),2):
  if symp(points[i],points[j])==0:A[i,j]=A[j,i]=1
 octets=[];seen=set()
 for left in itertools.combinations(range(40),4):
  if any(A[i,j] for i,j in itertools.combinations(left,2)):continue
  right=tuple(v for v in range(40) if all(A[v,u] for u in left))
  if len(right)!=4 or any(A[i,j] for i,j in itertools.combinations(right,2)):continue
  key=tuple(sorted((tuple(left),tuple(right))))
  if key not in seen: seen.add(key);octets.append(key)
 octets=sorted(octets)
 edge_to_octets=collections.defaultdict(list)
 for oi,(L,R) in enumerate(octets):
  for u in L:
   for v in R:
    assert A[u,v]
    edge_to_octets[tuple(sorted((u,v)))].append(oi)
 assert len(edge_to_octets)==240 and {len(v) for v in edge_to_octets.values()}=={3}
 faces=sorted(tuple(sorted(v)) for v in edge_to_octets.values())
 graph_edges=sorted({e for f in faces for e in itertools.combinations(f,2)})
 assert len(octets)==45 and len(graph_edges)==720 and len(faces)==240
 eidx={e:i for i,e in enumerate(graph_edges)}
 assert collections.Counter(e for f in faces for e in itertools.combinations(f,2))==collections.Counter({e:1 for e in graph_edges})
 B=np.zeros((45,45),dtype=np.int8)
 for u,v in graph_edges:B[u,v]=B[v,u]=1
 vals=np.linalg.eigvalsh(B)
 spec=collections.Counter(round(float(x)) for x in vals)
 assert spec==collections.Counter({32:1,2:24,-4:20})
 return {'points':points,'w33_adj':A,'octets':octets,'faces':faces,'graph_edges':graph_edges,'edge_index':eidx,'block_graph':B}

def rref(A):
 A=np.array(A,dtype=np.int8)%3;m,n=A.shape;r=0;piv=[]
 for c in range(n):
  p=next((i for i in range(r,m) if A[i,c]),None)
  if p is None:continue
  A[[r,p]]=A[[p,r]]
  if A[r,c]==2:A[r]=(2*A[r])%3
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%3
  piv.append(c);r+=1
  if r==m:break
 return A,piv

def quotient_generators(geo):
 faces=geo['faces'];eidx=geo['edge_index']
 C=np.zeros((480,45),dtype=np.int8)
 M=np.zeros((480,720),dtype=np.int8)
 for fi,(a,b,c) in enumerate(faces):
  C[2*fi,a]=2;C[2*fi,b]=1
  C[2*fi+1,b]=2;C[2*fi+1,c]=1
  for j,(p,q) in enumerate(((0,1),(1,2),(1,0))):
   M[2*fi,3*fi+j]=p;M[2*fi+1,3*fi+j]=q
 assert len(rref(C)[1])==44
 R,piv=rref(C.T)
 free=[j for j in range(480) if j not in piv]
 P=np.zeros((len(free),480),dtype=np.int8)
 for k,f in enumerate(free):
  P[k,f]=1
  for row,p in enumerate(piv):P[k,p]=(-R[row,f])%3
 assert P.shape==(436,480) and not np.any((P@C)%3)
 G=(P@M)%3
 assert len(rref(G)[1])==436
 return G,C,M,P

if __name__=='__main__':
 g=geometry();G,*_=quotient_generators(g)
 print(len(g['octets']),len(g['graph_edges']),len(g['faces']),G.shape,len(rref(G)[1]))
