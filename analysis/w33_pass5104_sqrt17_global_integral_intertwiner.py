#!/usr/bin/env python3
"""Pass5104: explicit global integral sqrt(17) intertwiner and index-2 obstruction."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
import sympy as sp
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5104_SQRT17_GLOBAL_INTEGRAL_INTERTWINER.json'

def int_nullspace(M):
    cols=sp.Matrix(M.tolist()).nullspace();out=[]
    for v in cols:
        den=1
        for x in v:den=sp.ilcm(den,int(x.q))
        out.append([int(x*den) for x in v])
    return np.array(out,dtype=np.int64).T

def rank_mod(M,p=1009):
    A=np.array(M,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]),None)
        if piv is None:continue
        if piv!=r:A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def main():
    A10=sp.Matrix([[1,4],[1,0]]);T6=2*A10;B2=sp.Matrix([[4,2],[2,5]]);Dhist=2*(B2-4*sp.eye(2));C=sp.Matrix([[0,16],[1,2]])
    P=sp.Matrix([[2,-2],[0,1]]);Ph=sp.Matrix([[2,4],[1,1]])
    assert C*P==P*T6 and abs(P.det())==2 and C*Ph==Ph*Dhist and abs(Ph.det())==2
    c,d=sp.symbols('c d',integer=True);Pgen=sp.Matrix([[2*d,8*c-2*d],[c,d]])
    assert C*Pgen==Pgen*T6 and sp.factor(Pgen.det())==-2*(4*c*c-c*d-d*d)
    # Rebuild the exact global theta carrier from Pass5087.
    G=build_W(3);nA=len(G['apartments']);N=np.zeros((40,40),dtype=np.int64)
    for l,L in enumerate(G['lines']):
        for p in L:N[p,l]=1
    B=int_nullspace(N);assert B.shape==(40,15)
    X=np.zeros((nA,40),dtype=np.int64)
    for a,edges in enumerate(G['apt_edges']):
        for e in edges:
            _,l=G['flags'][e];X[a,l]=1
    V=X@B;adj=[set() for _ in range(nA)]
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(4),3):
            ids=[loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]]
            for u,v in itertools.combinations(ids,2):adj[u].add(v);adj[v].add(u)
    def act(M):
        R=np.zeros_like(M)
        for i,nei in enumerate(adj):
            for j in nei:R[i]+=M[j]
        return R
    AV=act(V);A2V=act(AV);assert not np.any(A2V-2*AV-16*V);W=np.column_stack([V,AV]);assert rank_mod(W)==30
    # Interleave the 15 lanes so the action is 15 copies of C.
    perm=[]
    for j in range(15):perm += [j,15+j]
    Wi=W[:,perm]
    blockP=sp.diag(*([P]*15));assert abs(int(blockP.det()))==2**15
    out={'pass':5104,'status':'THEOREM_GLOBAL_INTEGRAL_INTERTWINER','field':'Q(sqrt(17))',
         'theta_companion':C.tolist(),'twisted_T6_block':T6.tolist(),'historical_doubled_shifted_block':Dhist.tolist(),
         'minimal_intertwiner':P.tolist(),'minimal_index':2,'general_integral_solution':'P(c,d)=[[2d,8c-2d],[c,d]], det=-2(4c^2-cd-d^2); every nonsingular integral intertwiner has even determinant.',
         'historical_index2_intertwiner':Ph.tolist(),'global_theta_carrier':{'apartments':1620,'levi_line_kernel_lanes':15,'rank':30,'annihilator':'x^2-2x-16','integral_lattice_index_for_15_lanes':2**15},
         'interpretation':'The global theta lattice is explicitly linked to 15 copies of the twisted T6/historical doubled transfer lattice, but only through an index-two map on each quadratic lane.',
         'boundary':'This is a global apartment-function/operator-lattice intertwiner. It does not identify the historical transfer geometry itself with W33 apartments.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
