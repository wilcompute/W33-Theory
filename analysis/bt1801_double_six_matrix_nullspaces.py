#!/usr/bin/env python3
"""BT1801: full double-six matrix and nullspace generators.

Run from repo root.  The script rebuilds the H27/Payne support, the Schlaefli
sixers/double-sixes, the BT1795 transported 18-line set, and writes the full
18 x 36 incidence matrix plus left/right nullspace generators over F2 and F3.
"""
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1801_double_six_matrix_nullspaces_full.json'
F=range(3)
USED=[5,36,10,12,38,34,18,41,29,42,20,30,40,15,22,37,7,44]
TABLES=['T001','T002','T010','T012','T020','T021','T100','T101','T111','T112','T120','T122','T200','T202','T210','T211','T221','T222']
def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
def ppoints(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def pline(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)
def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])
def support():
    P=ppoints(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({pline(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        old.append(tuple(sorted(shell_coord(x) for x in L if x in shell)))
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [tuple(sorted(L)) for L in old+new]
def rref(A,p):
    A=np.array(A,dtype=int)%p; m,n=A.shape; piv=[]; r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]%p),None)
        if q is None: continue
        A[[r,q]]=A[[q,r]]; A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]%p: A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c); r+=1
        if r==m: break
    return A,piv
def nullspace(A,p):
    A=np.array(A,dtype=int)%p; R,piv=rref(A,p); n=A.shape[1]
    free=[j for j in range(n) if j not in piv]; out=[]
    for f in free:
        x=np.zeros(n,dtype=int); x[f]=1
        for row,c in enumerate(piv): x[c]=(-R[row,f])%p
        out.append(x.tolist())
    return out
def main():
    lines=support(); G=nx.Graph(); G.add_nodes_from({p for L in lines for p in L})
    for L in lines:
        for a,b in combinations(L,2): G.add_edge(a,b)
    S=nx.complement(G)
    sixers=set(tuple(sorted(c)) for c in nx.find_cliques(S) if len(c)==6)
    double=[]
    for A,B in combinations(sixers,2):
        A=set(A); B=set(B)
        if A&B: continue
        cross=[(a,b) for a in A for b in B if S.has_edge(a,b)]
        if len(cross)==6 and len(set(a for a,b in cross))==6 and len(set(b for a,b in cross))==6:
            double.append((tuple(sorted(A)),tuple(sorted(B)),tuple(sorted(cross))))
    M=np.zeros((18,36),dtype=int)
    for r,idx in enumerate(USED):
        T=set(lines[idx])
        for c,(A,B,_) in enumerate(double):
            if len(T & (set(A)|set(B)))==2: M[r,c]=1
    payload={'bt':'BT1801','row_labels':TABLES,'column_labels':[f'D{i:02d}' for i in range(36)],'matrix':M.tolist(),'ranks':{'F2':len(rref(M,2)[1]),'F3':len(rref(M,3)[1])},'left_nullspace':{'F2':nullspace(M.T,2),'F3':nullspace(M.T,3)},'right_nullspace':{'F2':nullspace(M,2),'F3':nullspace(M,3)},'checks':{'row_sum_set':sorted(map(int,set(M.sum(axis=1)))),'column_sum_set':sorted(map(int,set(M.sum(axis=0))))}}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'matrix_shape':[18,36],'rank_F2':payload['ranks']['F2'],'rank_F3':payload['ranks']['F3'],'left_F2':len(payload['left_nullspace']['F2']),'right_F2':len(payload['right_nullspace']['F2']),'left_F3':len(payload['left_nullspace']['F3']),'right_F3':len(payload['right_nullspace']['F3'])},indent=2,sort_keys=True))
if __name__=='__main__': main()
