from __future__ import annotations
import numpy as np
from numba import njit,prange
from w33_pass568_572_z9_common import PD,META,BIDX,ALPHAS

# Precompute exact local D contributions for each fibre and (c,a,q), and deep anchor d.
LOCAL=np.zeros((4,27,9,9,6),dtype=np.int64)
DEEP=np.zeros((3,9,9,6),dtype=np.int64)
for fi in range(4):
    coord=[i for i,(b,u,prim) in enumerate(META) if prim and BIDX[b]==fi]
    for c in range(3):
      for a in range(3):
       for q in range(3):
        idx=c*9+a*3+q
        for ii in coord:
            b,u,prim=META[ii];ell=(ALPHAS[fi][0]*u[0]+ALPHAS[fi][1]*u[1])%3
            v=(c+a*ell+q*ell*ell)%3
            if v:
                LOCAL[fi,idx]+=np.array(PD[ii][v],dtype=np.int64)
for d in range(3):
    for ii,(b,u,prim) in enumerate(META):
        if not prim and d:DEEP[d]+=np.array(PD[ii][d],dtype=np.int64)

@njit(cache=True)
def ext_add_inplace(out,a,p):
    for i in range(6):out[i]=(out[i]+a[i])%p

@njit(cache=True)
def ext_mul(a,b,p):
    v=np.zeros(11,dtype=np.int64)
    for i in range(6):
      ai=a[i]
      if ai:
       for j in range(6):
        bj=b[j]
        if bj:v[i+j]=(v[i+j]+(ai*bj)%p)%p
    for k in range(10,5,-1):
      c=v[k]%p
      if c:
       v[k]=0
       v[k-6]=(v[k-6]-c)%p
       v[k-3]=(v[k-3]-c)%p
    return v[:6]

@njit(cache=True)
def matmul_ext(A,B,p):
    out=np.zeros((9,9,6),dtype=np.int64)
    for i in range(9):
      for k in range(9):
       az=False
       for t in range(6):
        if A[i,k,t]!=0:az=True;break
       if az:
        for j in range(9):
         bz=False
         for t in range(6):
          if B[k,j,t]!=0:bz=True;break
         if bz:
          z=ext_mul(A[i,k],B[k,j],p)
          for t in range(6):out[i,j,t]=(out[i,j,t]+z[t])%p
    return out

@njit(cache=True)
def invmod(a,p):
    t,nt=0,1;r,nr=p,a
    while nr:
        q=r//nr;t,nt=nt,t-q*nt;r,nr=nr,r-q*nr
    return t%p

@njit(cache=True)
def charpoly_real_residues(param,p,local,deep):
    # param: c4,a4,d,q4 direct (13 in canonical order c,a,d,q)
    D=np.zeros((9,9,6),dtype=np.int64)
    for fi in range(4):
      c=param[fi];a=param[4+fi];q=param[9+fi]
      idx=c*9+a*3+q
      for i in range(9):
       for j in range(9):
        for t in range(6):D[i,j,t]=(D[i,j,t]+local[fi,idx,i,j,t])%p
    d=param[8]
    for i in range(9):
     for j in range(9):
      for t in range(6):D[i,j,t]=(D[i,j,t]+deep[d,i,j,t])%p
    # power sums
    ps=np.zeros((9,6),dtype=np.int64)
    P=D.copy()
    for k in range(9):
      for i in range(9):
       for t in range(6):ps[k,t]=(ps[k,t]+P[i,i,t])%p
      if k<8:P=matmul_ext(P,D,p)
    e=np.zeros((10,6),dtype=np.int64);e[0,0]=1
    for k in range(1,10):
      s=np.zeros(6,dtype=np.int64)
      for i in range(1,k+1):
        term=ext_mul(e[k-i],ps[i-1],p)
        sign=1 if (i-1)%2==0 else -1
        for t in range(6):s[t]=(s[t]+sign*term[t])%p
      invk=invmod(k,p)
      for t in range(6):e[k,t]=(s[t]*invk)%p
    out=np.zeros((8,3),dtype=np.int64)
    for k in range(2,10):
      sign=-1 if k%2==1 else 1 # charpoly coeff (-1)^k e_k
      out[k-2,0]=(sign*e[k,0])%p
      out[k-2,1]=(sign*e[k,1])%p
      out[k-2,2]=(sign*e[k,4])%p
    return out

@njit(cache=True,parallel=True)
def batch_residues(params,p,local,deep):
    n=params.shape[0];out=np.zeros((n,8,3),dtype=np.int64)
    for i in prange(n):out[i]=charpoly_real_residues(params[i],p,local,deep)
    return out
