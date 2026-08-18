#!/usr/bin/env python3
"""Exact cyclotomic Fourier decomposition of the Pass7164 E8 C6 lift."""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass7163_7170_e8_hexagonal_lift as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7164_E8_FOURIER_ADDENDUM.json'
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    a,b=x;c,d=y
    return (a*c-b*d,a*d+b*c+b*d)
ZERO=(0,0);ONE=(1,0)
ZPOW=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
def zpow(e):return ZPOW[e%6]
def mmul(A,B):
    n=len(A);C=[[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
      for k in range(n):
        if A[i][k]==ZERO:continue
        for j in range(n):
          if B[k][j]!=ZERO:C[i][j]=add(C[i][j],mul(A[i][k],B[k][j]))
    return C
def shift(A,lam):
    C=[r[:] for r in A]
    for i in range(len(A)):C[i][i]=add(C[i][i],(-lam,0))
    return C
def ident(n):return [[ONE if i==j else ZERO for j in range(n)] for i in range(n)]
def iszero(A):return all(x==ZERO for r in A for x in r)
def trace(A):
    z=ZERO
    for i in range(len(A)):z=add(z,A[i][i])
    return z

def main():
    R,fib,phase,radj,base_adj,zero,twelve,diff=b.e8_fibers()
    for a in range(40):
        D={(phase[a][v]-phase[a][u])%6 for u in fib[a] for v in (radj[u]&set(fib[a]))}
        assert D=={1,5}
    cross={}
    for a,bb in twelve:
        D={(phase[bb][v]-phase[a][u])%6 for u in fib[a] for v in fib[bb] if v in radj[u]}
        assert len(D)==2 and any((s+1)%6 in D for s in D)
        cross[(a,bb)]=D;cross[(bb,a)]={(-d)%6 for d in D}
    expected={0:[(-4,24),(8,15),(56,1)],1:[(-2,36),(28,4)],2:[(-4,30),(8,10)],3:[(-2,40)],4:[(-4,30),(8,10)],5:[(-2,36),(28,4)]}
    sectors={}
    for k in range(6):
        M=[[ZERO for _ in range(40)] for _ in range(40)]
        for a in range(40):M[a][a]=add(zpow(k),zpow(-k))
        for (a,bb),D in cross.items():
            z=ZERO
            for d in D:z=add(z,zpow(k*d))
            M[a][bb]=z
        vals=expected[k];P=ident(40)
        for lam,mult in vals:P=mmul(P,shift(M,lam))
        assert iszero(P)
        tr=trace(M);assert tr[1]==0
        assert sum(m for _,m in vals)==40
        assert sum(lam*m for lam,m in vals)==tr[0]
        sectors[str(k)]={'minimal_annihilating_polynomial_roots':[lam for lam,_ in vals],
                         'spectrum':{str(lam):mult for lam,mult in vals},
                         'trace':tr[0],'dimension':40,'exact_cyclotomic_polynomial_check':True}
    full={}
    for vals in expected.values():
        for lam,m in vals:full[lam]=full.get(lam,0)+m
    assert full=={-4:84,8:35,56:1,-2:112,28:8}
    out={'schema':'w33.pass7164.e8_fourier_addendum.v1','status':'PASS',
         'field':'Z[zeta_6], zeta_6^2-zeta_6+1=0','fiber_fourier_dimensions':[40]*6,
         'sectors':sectors,'full_root_graph_spectrum':{str(k):v for k,v in sorted(full.items())},
         'k0_identity':'M_0 = 2J - 2 A_W33',
         'k0_derivation':'W33 spectrum 12^1,2^24,(-4)^15 gives 56^1,(-4)^24,8^15',
         'boundary':'Exact cyclotomic matrix identities for the Pass7164 C6 lift; no physical Fourier-mode claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','full':out['full_root_graph_spectrum']}))
if __name__=='__main__':main()
