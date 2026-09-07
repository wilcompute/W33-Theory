#!/usr/bin/env python3
"""Pass5153: exact integral Smith form of the q=4 C2 root-coset incidence matrix."""
from __future__ import annotations
import json,collections
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5153_Q4_ROOT_COSET_SMITH.json'

def rank_mod(M,p):
    A=[[int(x)%p for x in row] for row in M];m=len(A);n=len(A[0]);r=0
    for c in range(n):
        i=next((i for i in range(r,m) if A[i][c]),None)
        if i is None:continue
        A[r],A[i]=A[i],A[r];z=pow(A[r][c],-1,p);A[r]=[(z*x)%p for x in A[r]]
        for j in range(m):
            if j!=r and A[j][c]:
                z=A[j][c];A[j]=[(a-z*b)%p for a,b in zip(A[j],A[r])]
        r+=1
        if r==m:break
    return r

def incidence_q4():
    U,H,F=roots(4);idx={g:i for i,g in enumerate(U)};cosets=[]
    for h in H:
        seen=set()
        for g in U:
            c=tuple(sorted(idx[mm(g,z,F)] for z in h))
            if c not in seen:seen.add(c);cosets.append(c)
        assert len(seen)==64
    assert len(cosets)==256
    M=[[0]*256 for _ in range(256)]
    for j,c in enumerate(cosets):
        for i in c:M[i][j]=1
    return M

def main():
    M=incidence_q4();D=smith_normal_form(sp.Matrix(M),domain=sp.ZZ)
    diag=[abs(int(D[i,i])) for i in range(256) if D[i,i]!=0];cnt=collections.Counter(diag)
    assert len(diag)==184 and cnt==collections.Counter({1:180,2:4})
    r2=rank_mod(M,2);r3=rank_mod(M,3);assert (r2,r3)==(180,184)
    out={'pass':5153,'status':'THEOREM_Q4_ROOT_COSET_SMITH_FORM','q':4,'shape':[256,256],
         'smith_nonzero':{'1':180,'2':4},'rank_Q':184,'rank_F2':180,'rank_F3':184,
         'cokernel':'Z^72 direct_sum (Z/2)^4',
         'interpretation':'The entire characteristic-2 rank loss is accounted for by four exact 2-torsion Smith factors.',
         'boundary':'No q5 Smith form is claimed; direct q5 Smith reduction is substantially heavier.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
