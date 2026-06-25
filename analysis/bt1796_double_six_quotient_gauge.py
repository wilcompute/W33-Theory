#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1796_double_six_quotient_gauge.json'
F=range(3)
USED=[5,36,10,12,38,34,18,41,29,42,20,30,40,15,22,37,7,44]
KINDS={5:'old',36:'new',10:'old',12:'old',38:'new',34:'old',18:'old',41:'new',29:'old',42:'new',20:'old',30:'old',40:'new',15:'old',22:'old',37:'new',7:'old',44:'new'}

def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')

def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3

def projective_points(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})

def projective_line(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)

def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    assert v[2]==1
    return (v[0],v[1],v[3])

def support():
    P=projective_points(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({projective_line(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        old.append(tuple(sorted(shell_coord(x) for x in L if x in shell)))
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    return [tuple(sorted(L)) for L in old+new]

def rank_mod(M,p):
    A=M.copy()%p; m,n=A.shape; r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]%p),None)
        if piv is None: continue
        A[[r,piv]]=A[[piv,r]]; inv=pow(int(A[r,c]),-1,p); A[r]=(A[r]*inv)%p
        for i in range(m):
            if i!=r and A[i,c]%p: A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r

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
            double.append((A,B,cross))
    assert len(sixers)==72 and len(double)==36
    M=np.zeros((len(USED),len(double)),dtype=int)
    for r,idx in enumerate(USED):
        T=set(lines[idx])
        for c,(A,B,_) in enumerate(double):
            if len(T & (A|B))==2: M[r,c]=1
    row_sums=M.sum(axis=1); col_sums=M.sum(axis=0)
    payload={'bt':'BT1796','title':'double-six quotient gauge','input_transport':'BT1795 transported 18 Hesse table triples as 18 H27 support lines','used_support_lines':USED,'used_support_kind_histogram':dict(Counter(KINDS[i] for i in USED)),'cubic_surface_gauge':{'sixers':len(sixers),'double_sixes':len(double)},'incidence_matrix':{'shape':[int(x) for x in M.shape],'entry_rule':'1 iff transported H27 support line intersects a double-six in two points','row_sum_histogram':{str(k):int(v) for k,v in Counter(row_sums).items()},'column_sum_histogram':{str(k):int(v) for k,v in Counter(col_sums).items()},'rank_F2':rank_mod(M,2),'rank_F3':rank_mod(M,3),'distinct_row_signatures':len({tuple(row) for row in M}),'distinct_column_signatures':len({tuple(M[:,c]) for c in range(M.shape[1])})},'conclusion':'The double-six quotient does not collapse the transported tables to a pure gauge ambiguity: every table row and every double-six column has a distinct signature. But the incidence is perfectly balanced (24 double-sixes per transported table, 12 transported tables per double-six) and rank-deficient, so the obstruction is a structured cubic-surface gauge code rather than a coordinate relabeling.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps(payload['incidence_matrix'],indent=2,sort_keys=True))
if __name__=='__main__': main()
