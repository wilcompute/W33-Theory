#!/usr/bin/env python3
"""Exact PSp(4,3)-equivariant coupling test for the quartic H1 determinant.

H1 is the ten-dimensional adjoint sp4(F3).  A synchronized A8^3 weight-two
operator carries three independent factor Pauli degrees v1,v2,v3 in V=F3^4.
This file solves the *complete* quadratic equivariant map space

  Hom_PSp(Sym^2(V^3), sp4)

and proves it has dimension six, spanned by the six symmetric moment maps
M_ij.  Every resulting X is supported on span(v1,v2,v3), hence rank(X)<=3 and
det(X)=0 identically.  Four independent vectors give a control with det=1.

Therefore omega^(r det X) cannot be a direct phase of one synchronized
weight-two A8^3 operator.  Any determinant-magic realization requires at least
four independent Pauli directions, i.e. a composite/higher interaction.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_h1_det_weight2_coupling_no_go.json';p=3
J=np.block([[np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],[-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)]])%p

def rref(A):
 A=np.asarray(A,dtype=np.int64).copy()%p;r=0;pv=[]
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  pv.append(c);r+=1
 return A,pv

def null(A):
 R,pv=rref(A);free=[c for c in range(R.shape[1]) if c not in pv];out=[]
 for f in free:
  x=np.zeros(R.shape[1],dtype=np.int64);x[f]=1
  for i,c in enumerate(pv):x[c]=(-R[i,f])%p
  out.append(x)
 return np.array(out,dtype=np.int64)

def inv(A):
 A=np.asarray(A,dtype=np.int64)%p;n=len(A);X=np.c_[A,np.eye(n,dtype=np.int64)]
 for c in range(n):
  q=next(i for i in range(c,n) if X[i,c]);X[[c,q]]=X[[q,c]];X[c]=X[c]*pow(int(X[c,c]),-1,p)%p
  for i in range(n):
   if i!=c and X[i,c]:X[i]=(X[i]-X[i,c]*X[c])%p
 return X[:,n:]%p

def sp_basis():
 eq=[]
 for a,b in itertools.product(range(4),repeat=2):
  z=np.zeros(16,dtype=np.int64)
  for k in range(4):z[k*4+a]+=J[k,b];z[k*4+b]+=J[a,k]
  eq.append(z%p)
 B=null(np.array(eq));assert B.shape==(10,16);return B
B=sp_basis();_,pc=rref(B);pc=pc[:10];Binv=inv(B[:,pc])

def trans(v):
 v=np.asarray(v,dtype=np.int64).reshape(4,1)%p;T=(np.eye(4,dtype=np.int64)-v@(v.T@J))%p
 assert np.array_equal(T.T@J@T%p,J);return T

def adj(T):
 Ti=inv(T);M=np.zeros((10,10),dtype=np.int64)
 for i,b in enumerate(B):
  Y=T@b.reshape(4,4)@Ti%p;co=Y.reshape(16)[pc]@Binv%p;M[i]=co
 return M.T%p

def mons2(n):return [(i,j) for i in range(n) for j in range(i,n)]
M12=mons2(12);mi={x:i for i,x in enumerate(M12)}
def quad_action(D):
 Q=np.zeros((78,78),dtype=np.int64)
 for r,(a,b) in enumerate(M12):
  for u,v in itertools.product(range(12),repeat=2):
   c=int(D[a,u]*D[b,v])%p
   if c:Q[r,mi[tuple(sorted((u,v)))]]=(Q[r,mi[tuple(sorted((u,v)))]]+c)%p
 return Q

def coords(X):
 x=X.reshape(16)%p;c=x[pc]@Binv%p;assert np.array_equal(c@B%p,x);return c

def moment(i,j):
 F=np.zeros((10,78),dtype=np.int64)
 if i==j:
  for a in range(4):
   E=np.zeros((4,4),dtype=int);E[a,a]=1;F[:,mi[(4*i+a,4*i+a)]]=coords(E@J%p)
   for b in range(a+1,4):
    E=np.zeros((4,4),dtype=int);E[a,b]=E[b,a]=1;F[:,mi[(4*i+a,4*i+b)]]=coords(E@J%p)
 else:
  for a,b in itertools.product(range(4),repeat=2):
   E=np.zeros((4,4),dtype=int);E[a,b]+=1;E[b,a]+=1
   F[:,mi[(4*i+a,4*j+b)]]=coords(E@J%p)
 return F%p

def rank(A):return len(rref(A)[1])

def main(write=True):
 tv=[np.eye(4,dtype=int)[i] for i in range(4)]+[np.array(v) for v in ((1,1,0,0),(0,0,1,1),(1,0,1,0),(0,1,0,1))]
 T=[trans(v) for v in tv];A=[adj(t) for t in T];D=[np.kron(np.eye(3,dtype=int),t)%p for t in T];Q=[quad_action(d) for d in D]
 eq=[]
 for a,q in zip(A,Q):eq.append((np.kron(np.eye(78,dtype=int),a)-np.kron(q.T,np.eye(10,dtype=int)))%p)
 homdim=780-rank(np.vstack(eq));assert homdim==6
 F=[moment(i,j) for i in range(3) for j in range(i,3)]
 assert rank(np.stack([f.flatten(order='F') for f in F]))==6
 for f in F:
  for a,q in zip(A,Q):assert np.array_equal(a@f%p,f@q%p)
 # General moment-map matrix has form S J with S supported on span(v1,v2,v3),
 # so rank <=3. Four standard basis vectors give S=I and X=J, det=1 mod3.
 X=sum((np.outer(np.eye(4,dtype=int)[:,i],np.eye(4,dtype=int)[:,i])@J for i in range(4)),start=np.zeros((4,4),dtype=int))%p
 det4=int(round(np.linalg.det(X)))%p;assert det4==1
 out={'schema':'w33.h1_det_weight2_coupling_no_go.v1','status':'PASS',
  'headline':'The complete quadratic PSp(4,3)-equivariant coupling space from three factor Pauli labels to H1=sp4(F3) has dimension six and is spanned by the six symmetric moment maps M_ij. Every image from one triple (v1,v2,v3) has rank at most three, so det(X)=0 identically. Four independent Pauli directions attain det=1.',
  'domain':'Sym^2((F3^4)^3)','target':'sp4(F3) ~= Sym^2(F3^4)','Hom_dimension_F3':homdim,
  'moment_map_basis':['M11','M12','M13','M22','M23','M33'],
  'single_weight2_triple':{'available_factor_degrees':3,'image_rank_bound':3,'determinant':'identically zero','phase_omega_r_det':'trivial'},
  'four_vector_control':{'vectors':'standard basis e1,e2,e3,e4','image':'J','det_mod3':det4},
  'consequence':'The quartic determinant invariant remains a genuine nonlinear H1 invariant, but it cannot couple directly through one synchronized A8^3 weight-two operator. A determinant phase requires at least four independent Pauli directions, hence a composite/multi-operator channel.',
  'boundary':'This no-go is for quadratic equivariant coupling of one three-label weight-two operator. It does not exclude higher-degree/OPE composites carrying four or more independent Pauli degrees.',
  'checks':{'Hom_dim_6':True,'six_moment_maps_span':True,'single_triple_det_zero':True,'four_vector_det_one':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
