#!/usr/bin/env python3
"""Pass5139: exact q=5 C2 root-coset derivative spectrum."""
from __future__ import annotations
import collections,json
from pathlib import Path
import numpy as np
import scipy.sparse as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5139_Q5_ROOT_COSET_SPECTRUM.json';Q=5
def E(i,j):M=np.zeros((4,4),dtype=np.int64);M[i,j]=1;return M
def key(A):return tuple(map(int,(A%Q).flat))
def mm(A,B):return(A@B)%Q
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
    I=np.eye(4,dtype=np.int64)%Q;X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)];roots=[[(I+t*Z)%Q for t in range(Q)] for Z in X]
    U={key(I):I};D=collections.deque([I]);gens=[R[1] for R in roots]
    while D:
        a=D.popleft()
        for g in gens:
            b=mm(a,g);k=key(b)
            if k not in U:U[k]=b;D.append(b)
    assert len(U)==625;els=list(U.values());idx={key(a):i for i,a in enumerate(els)};cosets=[]
    for R in roots:
        seen=set()
        for g in els:
            C=tuple(sorted(idx[key(mm(g,h))] for h in R))
            if C not in seen:seen.add(C);cosets.append(C)
        assert len(seen)==125
    rr=[];cc=[]
    for j,C in enumerate(cosets):rr.extend(C);cc.extend([j]*5)
    H=sp.csr_matrix((np.ones(len(rr),dtype=np.int64),(rr,cc)),shape=(625,500));A=(H@H.T-4*sp.eye(625,dtype=np.int64,format='csr')).tocsr();assert set(A.sum(1).A1)=={16}
    coeff=[1,-53,1098,-10816,41765,105363,-1462104,3281394,7425272,-35970640,13145136,70220032,-27444992,-29331456]
    Y=sp.eye(625,dtype=np.int64,format='csr')
    for c in coeff[1:]:Y=A@Y+c*sp.eye(625,dtype=np.int64,format='csr')
    assert Y.nnz==0
    traces=[625];P=sp.eye(625,dtype=np.int64,format='csr')
    for k in range(1,9):P=P@A;traces.append(int(P.diagonal().sum()))
    assert traces==[625,0,10000,30000,450000,3610000,43150000,507010000,6695730000]
    mult={'16':1,'11':8,'6':16,'1':140,'-4':220,'6+sqrt5':20,'6-sqrt5':20,'1+sqrt5':40,'1-sqrt5':40,'(7+sqrt65)/2':20,'(7-sqrt65)/2':20,'1+sqrt15':40,'1-sqrt15':40};assert sum(mult.values())==625
    Hd=H.toarray();ranks={str(p):rank_mod(Hd,p) for p in(2,3,5,7)};assert ranks=={'2':405,'3':405,'5':397,'7':405}
    out={'pass':5139,'status':'THEOREM_Q5_ROOT_COSET_EXACT_SPECTRUM','q':5,'U_order':625,'incidence_shape':[625,500],'derivative_degree':16,'annihilator_factors':['x-16','x-11','x-6','x-1','x+4','x^2-12x+31','x^2-2x-4','x^2-7x-4','x^2-2x-14'],'trace_moments_0_to_8':traces,'spectrum':mult,'incidence_ranks':ranks,'generic_rank':405,'native_F5_rank':397,'native_rank_drop':8,'minus4_multiplicity':220,'boundary':'Exact finite spectral/incidence theorem; quadratic fields and native rank defects carry no physical assignment.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
