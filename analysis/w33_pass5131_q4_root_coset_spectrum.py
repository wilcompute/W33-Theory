#!/usr/bin/env python3
"""Pass5131 (bonkers): exact characteristic-two C2 root-coset derivative spectrum.

Use genuine F4 arithmetic and the standard symplectic Borel parametrization
  U(a,S)=[[A,A S],[0,A^{-T}]], A=[[1,a],[0,1]], S symmetric.
This gives |U|=4^4=256 and four order-4 positive-root subgroups.  The 256
root cosets produce a square 256x256 incidence matrix H and derivative graph
A=HH^T-4I.  An exact integer annihilator plus trace moments certifies the
full spectrum; field elimination gives the native F2 rank drop.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5131_Q4_ROOT_COSET_SPECTRUM.json'

def add(a,b):return a^b
def mul(a,b):
    a0,a1=a&1,(a>>1)&1;b0,b1=b&1,(b>>1)&1
    c0=(a0*b0)^(a1*b1);c1=(a0*b1)^(a1*b0)^(a1*b1)
    return c0|(c1<<1) # w^2=w+1

def mm(A,B):
    return tuple(tuple(__import__('functools').reduce(add,(mul(A[i][k],B[k][j]) for k in range(len(B))),0) for j in range(len(B[0]))) for i in range(len(A)))
def tr(A):return tuple(zip(*A))
def umat(a,b,c,d):
    A=((1,a),(0,1));S=((b,c),(c,d));B=mm(A,S);D=tr(((1,a),(0,1))) # A^{-T}=A^T in char2
    return ((1,a,B[0][0],B[0][1]),(0,1,B[1][0],B[1][1]),(0,0,D[0][0],D[0][1]),(0,0,D[1][0],D[1][1]))

def rank_mod(M,p):
    A=np.array(M,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):continue
        i=r+int(nz[0])
        if i!=r:A[[r,i]]=A[[i,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for j in np.flatnonzero(A[:,c]):
            if j!=r:A[j]=(A[j]-A[j,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def main():
    U=[umat(a,b,c,d) for a,b,c,d in itertools.product(range(4),repeat=4)];assert len(set(U))==256
    idx={g:i for i,g in enumerate(U)}
    roots=[ [umat(t,0,0,0) for t in range(4)], [umat(0,t,0,0) for t in range(4)],
            [umat(0,0,t,0) for t in range(4)], [umat(0,0,0,t) for t in range(4)] ]
    cosets=[]
    for R in roots:
        seen=set()
        for g in U:
            C=tuple(sorted(idx[mm(g,h)] for h in R))
            if C not in seen:seen.add(C);cosets.append(C)
        assert len(seen)==64
    assert len(cosets)==256
    H=np.zeros((256,256),dtype=np.int64)
    for j,C in enumerate(cosets):H[list(C),j]=1
    assert set(H.sum(0))==set(H.sum(1))=={4}
    A=H@H.T-4*np.eye(256,dtype=np.int64);assert set(A.sum(1))=={12}
    # Exact square-free annihilator:
    # x(x-12)(x-8)(x-6)(x-4)(x-2)(x+4)(x^2-8).
    coeff=[1,-28,244,-336,-5152,20608,6656,-129024,147456,0]
    Y=np.eye(256,dtype=np.int64)
    for c in coeff[1:]:Y=A@Y+c*np.eye(256,dtype=np.int64)
    assert not np.any(Y)
    traces=[256];P=np.eye(256,dtype=np.int64)
    for k in range(1,8):P=P@A;traces.append(int(np.trace(P)))
    expected=[256,0,3072,6144,99840,568320,6030336,54104064];assert traces==expected
    spectrum={'12':1,'8':6,'6':24,'4':9,'2':24,'0':84,'-4':72,'+2sqrt2':18,'-2sqrt2':18}
    # The listed multiplicities uniquely solve trace moments 0..7 under the annihilator.
    def ps(k):
        z=1*12**k+6*8**k+24*6**k+9*4**k+24*2**k+84*(0**k if k else 1)+72*((-4)**k)
        if k%2==0:z+=18*2*(8**(k//2))
        return z
    assert [ps(k) for k in range(8)]==traces
    ranks={str(p):rank_mod(H,p) for p in (2,3,5,7)}
    assert ranks=={'2':180,'3':184,'5':184,'7':184}
    out={'pass':5131,'status':'THEOREM_Q4_ROOT_COSET_EXACT_SPECTRUM','q':4,'U_order':256,'root_cosets':256,
      'incidence_shape':[256,256],'root_coset_size':4,'cosets_per_root_direction':64,'derivative_degree':12,
      'annihilator':'x(x-12)(x-8)(x-6)(x-4)(x-2)(x+4)(x^2-8)','trace_moments_0_to_7':traces,
      'spectrum':spectrum,'incidence_ranks':ranks,'generic_rank':184,'native_F2_rank':180,'native_rank_drop':4,
      'synthesis':'The first-derivative root-coset geometry survives characteristic two with a clean quadratic irrational pair ±2sqrt(2), while the incidence module acquires a four-dimensional native-characteristic defect.',
      'boundary':'Exact finite-field/group-incidence theorem. The rank defect is not assigned a physical charge, state count, or particle interpretation.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
