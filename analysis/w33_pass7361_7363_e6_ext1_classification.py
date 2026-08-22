#!/usr/bin/env python3
"""Pass7361-7363: classify the two characteristic-3 extension directions in the E6 root module."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7361_7363_E6_EXT1_CLASSIFICATION.json'
P=3
EDGES={(0,1),(1,2),(2,3),(3,4),(2,5)}

def rref(A,p=P):
 A=np.asarray(A,dtype=np.int64).copy()%p;m,n=A.shape;r=0;pv=[]
 for c in range(n):
  z=next((i for i in range(r,m) if A[i,c]),None)
  if z is None:continue
  A[[r,z]]=A[[z,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  pv.append(c);r+=1
  if r==m:break
 return A,pv

def rank(A):return len(rref(A)[1])
def nullity(A):return np.asarray(A).shape[1]-rank(A)
def inv(A):
 A=np.asarray(A,dtype=np.int64)%P;n=len(A);X=np.c_[A,np.eye(n,dtype=int)]
 for c in range(n):
  z=next(i for i in range(c,n) if X[i,c]);X[[c,z]]=X[[z,c]];X[c]=X[c]*pow(int(X[c,c]),-1,P)%P
  for i in range(n):
   if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%P
 return X[:,n:]%P

def actions():
 C=np.eye(6,dtype=int)*2
 for a,b in EDGES:C[a,b]=C[b,a]=-1
 def ref(v,i):
  v=np.asarray(v,dtype=int);w=v.copy();w[i]-=int(v@C[:,i]);return w
 S=[]
 for i in range(6):
  M=np.zeros((6,6),dtype=int)
  for j in range(6):
   e=np.zeros(6,dtype=int);e[j]=1;M[:,j]=ref(e,i)%3
  S.append(M%3)
 F=np.vstack([(M-np.eye(6,dtype=int))%3 for M in S])
 R,pv=rref(F);free=[j for j in range(6) if j not in pv];assert len(free)==1
 f=np.zeros(6,dtype=int);f[free[0]]=1
 for i,c in enumerate(pv):f[c]=(-R[i,free[0]])%3
 B=[f]
 for e in np.eye(6,dtype=int):
  if rank(np.column_stack(B+[e]))>len(B):B.append(e)
  if len(B)==6:break
 B=np.column_stack(B)%3;Bi=inv(B);Q=[]
 for M in S:
  A=Bi@M@B%3;assert A[0,0]==1 and np.all(A[1:,0]==0);Q.append(A[1:,1:]%3)
 return Q

def h1(ACT):
 d=ACT[0].shape[0];ng=len(ACT);eq=[]
 def rel(word):
  M=np.zeros((d,ng*d),dtype=int);pref=np.eye(d,dtype=int)
  for g in word:
   M[:,g*d:(g+1)*d]=(M[:,g*d:(g+1)*d]+pref)%P;pref=pref@ACT[g]%P
  assert np.array_equal(pref,np.eye(d,dtype=int));return M
 for i in range(ng):eq.append(rel([i,i]))
 for i in range(ng):
  for j in range(i+1,ng):eq.append(rel([i,j]*(3 if (i,j) in EDGES else 2)))
 Z=ng*d-rank(np.vstack(eq));Cob=np.vstack([(A-np.eye(d,dtype=int))%P for A in ACT]);B=rank(Cob)
 return Z,B,Z-B

def main():
 Q=actions();zd,bd,h=h1(Q);Qd=[inv(A).T%P for A in Q];zdd,bdd,hd=h1(Qd)
 assert (zd,bd,h)==(6,5,1);assert (zdd,bdd,hd)==(6,5,1)
 out={'schema':'w33.pass7361_7363.e6_ext1_classification.v1','status':'PASS','field':'F3','simple_module_dimension':5,'H1_W_E6_M':{'cocycles':zd,'coboundaries':bd,'dimension':h},'H1_W_E6_Mdual':{'cocycles':zdd,'coboundaries':bdd,'dimension':hd},'consequence':'Ext^1(1,5) and Ext^1(5,1) are both one-dimensional; the two nonsplit layers in the Pass7329-7336 module 1|5|1 represent the unique nonzero extension classes in the two directions.','boundary':'Finite modular representation theorem from the Coxeter presentation; this identifies the extension spaces, not a physical interaction.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','Ext_1_5':1,'Ext_5_1':1}))
if __name__=='__main__':main()
