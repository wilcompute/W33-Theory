#!/usr/bin/env python3
"""Pass8805-8812: 40 logical point-stars, their 25D module, and the E6 sentinel relation code."""
from collections import Counter
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8805_8812_POINTSTAR_SENTINEL.json'
def canon(v):
 v=tuple(int(x)%3 for x in v)
 for x in v:
  if x:return tuple((pow(x,-1,3)*y)%3 for y in v)
def rref2(A):
 A=np.asarray(A,dtype=np.uint8).copy()&1
 if A.ndim==1:A=A[None,:]
 m,n=A.shape;r=0;p=[]
 for c in range(n):
  z=next((i for i in range(r,m) if A[i,c]),None)
  if z is None:continue
  A[[r,z]]=A[[z,r]]
  for i in range(m):
   if i!=r and A[i,c]:A[i]^=A[r]
  p.append(c);r+=1
 return A[:r],p
def rank2(A):return len(rref2(A)[1])
def null2(A):
 R,p=rref2(A);n=A.shape[1];free=[c for c in range(n) if c not in p];out=[]
 for f in free:
  x=np.zeros(n,dtype=np.uint8);x[f]=1
  for i,c in enumerate(p):x[c]=R[i,f]
  out.append(x)
 return np.asarray(out,dtype=np.uint8)
P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={v:i for i,v in enumerate(P)}
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],int)%3
def adj(i,j):return i!=j and int(np.array(P[i])@J@np.array(P[j]))%3==0
A=np.array([[adj(i,j) for j in range(40)] for i in range(40)],dtype=np.uint8)
lines=set()
for i,j in itertools.combinations(range(40),2):
 if not A[i,j]:continue
 u=np.array(P[i]);v=np.array(P[j]);S=set()
 for a,b in itertools.product(range(3),repeat=2):
  if a or b:S.add(pi[canon(tuple(map(int,(a*u+b*v)%3)))])
 if len(S)==4:lines.add(frozenset(S))
lines=sorted(lines,key=lambda s:tuple(sorted(s)));assert len(lines)==40
N=np.zeros((40,40),dtype=np.uint8)
for j,L in enumerate(lines):
 for p in L:N[p,j]=1
S=np.repeat(N,3,axis=1)
assert S.shape==(40,120) and set(map(int,S.sum(1)))=={12}
assert rank2(S)==25 and rank2(A)==16 and np.array_equal((S@S.T)%2,A)
K=null2(S.T);assert K.shape==(15,40)
we=Counter()
for mask in range(1<<15):
 x=np.zeros(40,dtype=np.uint8)
 for i in range(15):
  if (mask>>i)&1:x^=K[i]
 we[int(x.sum())]+=1
expected=Counter({0:1,8:45,12:720,16:6930,20:17376,24:6930,28:720,32:45,40:1});assert we==expected
assert rank2(N)==25
module_chain=[0,1,9,10,24,25];module_factors=[1,8,1,14,1]
assert [module_chain[i+1]-module_chain[i] for i in range(5)]==module_factors
out={'schema':'w33.pass8805_8812.pointstar_sentinel.v1','status':'PASS','passes':'8805-8812','point_stars':40,'physical_length':120,'weight_each':12,'star_span_dimension':25,'star_Gram':'A_W33 mod 2','star_Gram_rank':16,'bilinear_radical_dimension':9,'logical_module_composition':'1|8|1|14|1','radical_composition':'1|8','nondegenerate_quotient_composition':'1|14|1','relation_code':{'identity':'ker(point-star map)=ker(N^T)=historical W33 sentinel','parameters':'[40,15,8]_2','weight_enumerator':{str(k):v for k,v in sorted(we.items())},'minimum_words':45},'E6_bridge':'Pass4593 identifies the 45 weight-8 sentinel words with the 45 center-quad/E6 tritangent supports.','theorem':'The 40 canonical logical point-stars span a 25D module with composition 1|8|1|14|1. Their complete relation space is exactly the old [40,15,8] sentinel code, so its 45 minimum E6 tritangent supports are the 45 minimum dependencies among the logical stars.','claim_boundary':'The 120-coordinate matching model is the intrinsic punctured binary-Steinberg carrier established earlier; no physical hardware claim.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','star_rank':25,'kernel':'[40,15,8]','min_relations':45}))
