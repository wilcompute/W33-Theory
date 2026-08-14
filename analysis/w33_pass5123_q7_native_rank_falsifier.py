#!/usr/bin/env python3
"""Pass5123 (bonkers): exact q=7 native-rank falsifier for C2 root-coset incidence."""
from __future__ import annotations
import argparse,collections,json
from pathlib import Path
import numpy as np
from numba import njit
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5123_Q7_NATIVE_RANK_FALSIFIER.json'

@njit
def rank_mod(A,p):
    A=A.copy()%p;m,n=A.shape;r=0
    for c in range(n):
        piv=-1
        for i in range(r,m):
            if A[i,c]%p:
                piv=i;break
        if piv<0:continue
        if piv!=r:
            tmp=A[r].copy();A[r]=A[piv];A[piv]=tmp
        inv=pow(int(A[r,c]),p-2,p)
        A[r]=(A[r]*inv)%p
        for i in range(m):
            if i!=r and A[i,c]%p:
                A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def incidence(q):
    I=np.eye(4,dtype=np.int16)%q
    def E(i,j):M=np.zeros((4,4),dtype=np.int16);M[i,j]=1;return M
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
    els=list(U.values());idx={key(a):i for i,a in enumerate(els)};cos=[]
    for h in Hs:
        seen=set()
        for g in els:
            c=tuple(sorted(idx[key(mm(g,z))] for z in h))
            if c not in seen:seen.add(c);cos.append(c)
    M=np.zeros((q**4,4*q**3),dtype=np.int16)
    for j,c in enumerate(cos):M[list(c),j]=1
    return M

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');args=ap.parse_args()
    frozen={'q3':{'generic_rank':69,'native_rank':68,'drop':1},
            'q5':{'generic_rank':405,'native_rank':397,'drop':8},
            'q7':{'shape':[2401,1372],'generic_rank':1183,'native_rank':1173,'drop':10,
                  'generic_primes_checked':[2,11]}}
    if args.full:
        M=incidence(7);assert list(M.shape)==[2401,1372]
        # rank is unchanged by transpose; transpose has fewer elimination rows.
        r2=int(rank_mod(M.T.astype(np.int64),2));r7=int(rank_mod(M.T.astype(np.int64),7));r11=int(rank_mod(M.T.astype(np.int64),11))
        assert (r2,r7,r11)==(1183,1173,1183)
    out={'pass':5123,'status':'THEOREM_Q7_EXACT_NATIVE_RANK_FALSIFIER','anchors':frozen,
         'killed_conjecture':'native rank drop = ((q-1)/2)^3 for odd q; q7 would predict 27 but exact drop is 10',
         'q7_kernel_dimensions':{'generic_column':1372-1183,'native_column':1372-1173,
                                 'generic_left':2401-1183,'native_left':2401-1173},
         'boundary':'Three exact odd-prime anchors are now known, but no replacement all-q drop formula is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
