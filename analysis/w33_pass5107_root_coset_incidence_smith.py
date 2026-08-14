#!/usr/bin/env python3
"""Pass5107 (bonkers): Smith arithmetic of the C2 root-coset derivative foliation."""
from __future__ import annotations
import itertools,json
from collections import deque,Counter
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5107_ROOT_COSET_INCIDENCE_SMITH.json'

def incidence(q):
    I=np.eye(4,dtype=int)%q
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    mm=lambda A,B:(A@B)%q;key=lambda A:tuple(map(int,A.flat))
    Hroots=[[(I+t*Z)%q for t in range(q)] for Z in X];gens=[h[1] for h in Hroots]
    U={key(I):I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            b=mm(a,g);k=key(b)
            if k not in U:U[k]=b;Q.append(b)
    els=list(U.values());ei={key(a):i for i,a in enumerate(els)};cos=[]
    for h in Hroots:
        seen=set()
        for g in els:
            c=frozenset(ei[key(mm(g,z))] for z in h)
            if c not in seen:seen.add(c);cos.append(c)
    M=np.zeros((q**4,4*q**3),dtype=int)
    for j,c in enumerate(cos):M[list(c),j]=1
    return M,cos

def rank_mod(M,p):
    A=np.array(M,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]),None)
        if piv is None:continue
        if piv!=r:A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r

def snf_summary(M):
    D=smith_normal_form(sp.Matrix(M.tolist()),domain=ZZ);diag=[abs(int(D[i,i])) for i in range(min(D.shape))];return Counter(diag)

def main():
    M2,_=incidence(2);s2=snf_summary(M2);assert s2==Counter({1:15,0:1})
    M3,C3=incidence(3);s3=snf_summary(M3);assert s3==Counter({1:68,0:12,3:1})
    assert rank_mod(M3,2)==69 and rank_mod(M3,3)==68
    # HH^T = 4I + adjacency of the derivative point graph.
    A=M3@M3.T-4*np.eye(81,dtype=int);assert set(np.diag(A))=={0} and set(A.flat)<=set((0,1)) and set(A.sum(1))=={8}
    out={'pass':5107,'status':'THEOREM_ROOT_COSET_SMITH_DEFECT','q2_control':{'shape':[16,32],'rank_Q':15,'smith':'1^15,0^1','cokernel':'Z'},
         'q3':{'shape':[81,108],'row_sum':4,'column_sum':3,'rank_Q':69,'rank_F2':69,'rank_F3':68,'smith':'1^68,3^1,0^12','cokernel':'Z^12 + Z/3',
               'column_kernel_rank_Q':39,'column_kernel_rank_F3':40,'gram_identity':'H H^T = 4 I + A_derivative','minus4_adjacency_eigenspace_dimension':12},
         'interpretation':'The derivative foliation has a 12-dimensional rational incidence defect plus one genuinely ternary torsion class. The extra mod-3 null direction is compatible with every root-coset column having size 3.',
         'boundary':'This is arithmetic of the q3 root-coset incidence matrix, not a claim about a new physical charge or particle sector.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
