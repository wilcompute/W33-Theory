#!/usr/bin/env python3
"""Pass5121: explicit generator and U81 semidirect V4 action on the q3 Z/3 Smith defect."""
from __future__ import annotations
import json
from collections import deque
from math import gcd
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5121_Q3_INTEGRAL_TORSION_MODULE.json'
SUP=[0,3,4,5,6,8,9,10,13,15,17,18,20,21,22,23,26,27,28,30,31,32,37,38,40,46,49,50,51,52,53,55,56,59,63,64,66,69,72]
VAL=[2,1,1,1,2,2,1,1,1,2,2,2,1,1,2,1,1,2,2,1,2,2,1,1,2,1,2,2,2,2,1,1,2,1,1,1,1,2,1]

def build():
    q=3;I=np.eye(4,dtype=int)%q
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    Hs=[[(I+t*Z)%q for t in range(q)] for Z in X]
    def key(A):return tuple(map(int,(A%q).flat))
    def mm(A,B):return (A@B)%q
    U={key(I):I};Q=deque([I]);gens=[h[1] for h in Hs]
    while Q:
        a=Q.popleft()
        for g in gens:
            b=mm(a,g);k=key(b)
            if k not in U:U[k]=b;Q.append(b)
    els=list(U.values());idx={key(a):i for i,a in enumerate(els)};cos=[]
    for h in Hs:
        seen=set()
        for g in els:
            c=tuple(sorted(idx[key(mm(g,z))] for z in h))
            if c not in seen:seen.add(c);cos.append(c)
    H=np.zeros((81,108),dtype=int)
    for j,c in enumerate(cos):H[list(c),j]=1
    return H,els,key,idx

def rank_mod(A,p):
    A=np.array(A,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):continue
        i=r+int(nz[0]);A[[r,i]]=A[[i,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for j in np.flatnonzero(A[:,c]):
            if j!=r:A[j]=(A[j]-A[j,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def primitive_kernel(M):
    cols=sp.Matrix(M.tolist()).nullspace();out=[]
    for v in cols:
        den=1
        for x in v:den=sp.ilcm(den,int(x.q))
        a=[int(x*den) for x in v];g=0
        for z in a:g=gcd(g,abs(z))
        out.append([z//max(g,1) for z in a])
    return np.array(out,dtype=int).T

def main():
    H,els,key,idx=build();assert H.shape==(81,108)
    K=primitive_kernel(H.T);assert K.shape==(81,12) and rank_mod(K,3)==12
    a=np.zeros(81,dtype=int)
    for i,v in zip(SUP,VAL):a[i]=v
    assert np.all((H.T@a)%3==0) and rank_mod(np.column_stack([K,a]),3)==13
    w=(H.T@a)//3;assert np.count_nonzero(w)==74 and int(w.sum())==76
    labels={'e':(1,1,1,1),'a':(1,1,2,2),'b':(1,2,1,2),'c':(1,2,2,1)};chars={}
    for name,ds in labels.items():
        D=np.diag(ds)%3;Di=np.array(sp.Matrix(D.tolist()).inv_mod(3).tolist(),dtype=int)%3
        p=[idx[key((D@g@Di)%3)] for g in els];at=np.zeros(81,dtype=int)
        for i,j in enumerate(p):at[j]=a[i]
        signs=[s for s in (1,2) if rank_mod(np.column_stack([K,(at-s*a)%3]),3)==12]
        assert len(signs)==1;chars[name]='+' if signs[0]==1 else '-'
    assert chars=={'e':'+','a':'-','b':'+','c':'-'}
    out={'pass':5121,'status':'THEOREM_EXPLICIT_Q3_Z3_SATURATION_MODULE',
         'incidence_shape':[81,108],'rational_left_kernel_dimension':12,'mod3_left_kernel_dimension':13,
         'extra_mod3_vector':{'support':SUP,'values':VAL},
         'torsion_generator_w':{'definition':'w=(H^T a)/3','support':[int(i) for i in np.flatnonzero(w)],
                                'values_on_support':[int(w[i]) for i in np.flatnonzero(w)],'support_size':74,'l1_norm':76},
         'nontriviality':'a adds one dimension modulo 3 beyond the reduction of the primitive integral rational kernel; hence [w] is nonzero and generates the unique Z/3 saturation quotient.',
         'U81_action':'trivial, because Aut(Z/3)=C2 and every homomorphism from the 3-group U81 to C2 is trivial',
         'V4_character':chars,
         'boundary':'This resolves the integral arithmetic torsion module. The character match to the H27 central triality axis is recorded separately in Pass5125; no physical charge is inferred.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
