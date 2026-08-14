#!/usr/bin/env python3
"""Pass5115 (bonkers): native-characteristic rank defects of C2 root-coset incidence."""
from __future__ import annotations
import collections,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5115_Q5_ROOT_COSET_NATIVE_RANK_DEFECT.json'

def incidence(q):
    I=np.eye(4,dtype=np.int64)%q
    def E(i,j):M=np.zeros((4,4),dtype=np.int64);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    Hs=[[(I+t*Z)%q for t in range(q)] for Z in X]
    def key(A):return tuple(map(int,(A%q).flat))
    def mm(A,B):return (A@B)%q
    U={key(I):I};Q=collections.deque([I]);gens=[h[1] for h in Hs]
    while Q:
        a=Q.popleft()
        for g in gens:
            b=mm(a,g);k=key(b)
            if k not in U:U[k]=b;Q.append(b)
    assert len(U)==q**4;els=list(U.values());idx={key(a):i for i,a in enumerate(els)}
    cosets=[]
    for h in Hs:
        seen=set()
        for g in els:
            c=tuple(sorted(idx[key(mm(g,z))] for z in h))
            if c not in seen:seen.add(c);cosets.append(c)
        assert len(seen)==q**3
    M=np.zeros((q**4,4*q**3),dtype=np.int64)
    for j,c in enumerate(cosets):M[list(c),j]=1
    assert set(M.sum(axis=0))=={q} and set(M.sum(axis=1))=={4}
    return M

def rank_mod(M,p):
    A=np.array(M,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if len(nz)==0:continue
        i=r+int(nz[0])
        if i!=r:A[[r,i]]=A[[i,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        hit=np.flatnonzero(A[:,c])
        for j in hit:
            if j!=r:A[j]=(A[j]-A[j,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def row(q,primes):
    M=incidence(q);rr={str(p):rank_mod(M,p) for p in primes}
    return {'q':q,'shape':list(M.shape),'ranks':rr,'column_weight':q,'row_weight':4}

def main():
    a2=row(2,[2,3]);a3=row(3,[2,3,5]);a5=row(5,[2,3,5,7])
    assert a2['ranks']=={'2':15,'3':15}
    assert a3['ranks']=={'2':69,'3':68,'5':69}
    assert a5['ranks']=={'2':405,'3':405,'5':397,'7':405}
    out={'pass':5115,'status':'THEOREM_EXACT_FIELD_RANKS_Q2_Q3_Q5','anchors':{'q2':a2,'q3':a3,'q5':a5},
         'q5_native_defect':{'generic_observed_rank':405,'rank_F5':397,'drop':8,
                             'generic_column_kernel_dimension':95,'native_column_kernel_dimension':103,
                             'generic_left_kernel_dimension':220,'native_left_kernel_dimension':228},
         'comparison':'At q=3 the analogous generic/native ranks are 69/68, a one-dimensional drop; q=2 has no native drop.',
         'pattern_firewall':'For odd anchors q=3,5 the drops 1,8 equal ((q-1)/2)^3, but two anchors do not establish an all-q formula.',
         'boundary':'These are exact finite-field ranks. No full Smith normal form at q=5 and no physical charge/particle interpretation are claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
