#!/usr/bin/env python3
"""Pass5087 (outside box): exact global Q(sqrt(17)) channel in q=3 theta graph.

Let A_theta be the graph on 1620 apartments in which two apartments are joined
when they occur in one theta check. Lift the 15-dimensional line-side Levi
incidence kernel ker(N) to apartment functions by summing a line vector over the
four line vertices of each apartment. If V is an integral basis matrix for that
lift, exact integer arithmetic gives
    (A_theta^2 - 2 A_theta - 16 I)V = 0,
and rank[V,A_theta V]=30. Therefore the generated 30-space has characteristic
polynomial (x^2-2x-16)^15 and exact eigenchannels 1+-sqrt(17), each multiplicity
15 inside this invariant space. With lambda=(1+sqrt(17))/2, the theta eigenvalue
alpha=1+sqrt(17)=2 lambda generates the conductor-two order Z+2 O_K of
Q(sqrt(17)), discriminant 68.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
import sympy as sp
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5087_THETA_SQRT17_CHANNEL.json'

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
        piv=next((i for i in range(r,m) if A[i,c]%p),None)
        if piv is None:continue
        if piv!=r:A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def main():
    G=build_W(3);nA=len(G['apartments']);assert nA==1620
    N=np.zeros((40,40),dtype=np.int64)
    for l,L in enumerate(G['lines']):
        for p in L:N[p,l]=1
    B=int_nullspace(N);assert B.shape==(40,15) and rank_mod(B)==15
    X=np.zeros((nA,40),dtype=np.int64)
    for a,edges in enumerate(G['apt_edges']):
        for e in edges:
            _,l=G['flags'][e];X[a,l]=1
        assert X[a].sum()==4
    V=X@B
    adj=[set() for _ in range(nA)];checks=0
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(4),3):
            ids=[loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]];checks+=1
            for u,v in itertools.combinations(ids,2):adj[u].add(v);adj[v].add(u)
    assert checks==4320 and set(map(len,adj))=={16}
    def act(M):
        R=np.zeros_like(M)
        for i,nei in enumerate(adj):
            for j in nei:R[i]+=M[j]
        return R
    AV=act(V);A2V=act(AV);assert not np.any(A2V-2*AV-16*V)
    generated=np.column_stack([V,AV]);assert rank_mod(generated)==30
    out={'pass':5087,'status':'THEOREM_EXACT_GLOBAL_QUADRATIC_CHANNEL','q':3,'apartments':1620,'theta_checks':4320,
         'theta_point_graph_degree':16,'levi_line_kernel_dimension':15,'generated_dimension':30,
         'annihilating_polynomial':'x^2-2x-16','discriminant':68,'generated_charpoly':'(x^2-2x-16)^15',
         'eigenchannels':['1+sqrt(17)','1-sqrt(17)'],'multiplicity_inside_generated_space':[15,15],
         'quadratic_order':{'field':'Q(sqrt(17))','maximal_generator':'lambda=(1+sqrt(17))/2','theta_generator':'alpha=2 lambda=1+sqrt(17)','order':'Z[alpha]=Z+2 O_K','conductor':2,'discriminant':68},
         'bridge':'Pass5069 T6 has the same eigenvalues. Together with Pass5091, the maximal-order T10 block, this theta channel, and the q3 recurrence give conductor ladder 1,2,4 with discriminants 17,68,272.',
         'boundary':'The theorem identifies an exact 30-dimensional invariant subspace; it does not claim these are the only occurrences of those eigenvalues in the full 1620-space.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
