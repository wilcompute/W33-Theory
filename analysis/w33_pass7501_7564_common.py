#!/usr/bin/env python3
"""Shared exact E8/A2/Eisenstein-leaf reconstruction for Pass7501-7564."""
from __future__ import annotations
import itertools
from collections import Counter,deque
import numpy as np

SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),
(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]

def roots():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (2,-2):
            for b in (2,-2):
                v=[0]*8;v[i]=a;v[j]=b;R.append(tuple(v))
    for s in itertools.product((1,-1),repeat=8):
        if sum(x<0 for x in s)%2==0:R.append(tuple(s))
    assert len(R)==240 and len(set(R))==240
    return R

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def refl(x,r):
    q=dot(x,r);assert q%4==0;k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))

def enum_a2(R):
    I={r:i for i,r in enumerate(R)};out=set()
    for i,j in itertools.combinations(range(240),2):
        if dot(R[i],R[j])!=-4:continue
        s=tuple(R[i][k]+R[j][k] for k in range(8));k=I[s]
        out.add(frozenset((i,j,k,I[tuple(-x for x in R[i])],I[tuple(-x for x in R[j])],I[tuple(-x for x in s)])))
    A=sorted(out,key=lambda x:tuple(sorted(x)));assert len(A)==1120
    return A

def rank_mod(M,p):
    A=np.asarray(M,dtype=np.int64).copy()%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if len(nz)==0:continue
        z=r+int(nz[0]);A[[r,z]]=A[[z,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        rows=np.flatnonzero(A[:,c]);rows=rows[rows!=r]
        if len(rows):A[rows]=(A[rows]-A[rows,c,None]*A[r])%p
        r+=1
        if r==m:break
    return r

def canon3(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple((x*y)%3 for y in v) if x==1 else tuple((2*y)%3 for y in v)
    raise ValueError('zero')

def build():
    R=roots();I={r:i for i,r in enumerate(R)};A2=enum_a2(R);ai={S:i for i,S in enumerate(A2)}
    rg=[tuple(I[refl(r,s)] for r in R) for s in SIMPLES]
    ag=[tuple(ai[frozenset(g[x] for x in S)] for S in A2) for g in rg]
    c=tuple(range(240))
    for g in rg:c=comp(g,c)
    J=tuple(range(240))
    for _ in range(10):J=comp(c,J)
    base=frozenset(i for i,S in enumerate(A2) if frozenset(J[x] for x in S)==S);assert len(base)==40
    leaves=[base];li={base:0};dq=deque([base]);parity=[0]
    while dq:
        X=dq.popleft();ix=li[X]
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in li:li[Y]=len(leaves);leaves.append(Y);dq.append(Y);parity.append(parity[ix]^1)
    assert len(leaves)==2240 and Counter(parity)=={0:1120,1:1120}
    lgens=[tuple(li[frozenset(g[x] for x in L)] for L in leaves) for g in ag]
    return R,A2,ag,J,base,leaves,lgens,parity

def a2_scheme(R,A2):
    basis=[next(e for e in itertools.combinations(sorted(S),2) if dot(R[e[0]],R[e[1]])==-4) for S in A2]
    A=np.zeros((1120,1120),dtype=np.uint8)
    for i in range(1120):
        a,b=basis[i]
        for j in range(i+1,1120):
            c,d=basis[j]
            if dot(R[a],R[c])==dot(R[a],R[d])==dot(R[b],R[c])==dot(R[b],R[d])==0:A[i,j]=A[j,i]=1
    C=A.astype(np.int16)@A.astype(np.int16);lab=np.zeros((1120,1120),dtype=np.int8);lab[A.astype(bool)]=1
    non=(A==0)&(~np.eye(1120,dtype=bool))
    for k,mu in enumerate((10,16,40),start=2):lab[non&(C==mu)]=k
    assert [int(np.sum(lab[0]==k)) for k in range(5)]==[1,120,648,270,81]
    return A,C,lab
