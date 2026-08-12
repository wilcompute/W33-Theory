#!/usr/bin/env python3
"""Pass4956 — exact 24D point-line intertwiner between W(3,3) and Q(4,3).

The corrected Pass4955 incidence Z has W(3,3) points on the row side and
W(3,3) lines / Q(4,3) points on the column side.  This verifier constructs
that standard incidence directly and proves

    A_W Z = Z A_Q,
    ZZ^T = 4I + A_W,
    Z^T Z = 4I + A_Q.

Therefore Z kills both 15D (-4)-sectors, scales the constants by 4, and gives
an exact isomorphism between the two 24D (+2)-sectors with inverse Z^T/6.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4956_POINT_LINE_24D_INTERTWINER.json'

def canon3(v):
    v=np.array(v,dtype=int)%3
    j=next(i for i,x in enumerate(v) if x)
    return tuple((v*pow(int(v[j]),-1,3))%3)

def rank_q(M):
    A=np.array(M,dtype=object)
    from fractions import Fraction
    A=[[Fraction(int(x)) for x in row] for row in A.tolist()]
    m=len(A);n=len(A[0]);r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i][c]),None)
        if q is None:continue
        A[r],A[q]=A[q],A[r]
        p=A[r][c];A[r]=[x/p for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                f=A[i][c];A[i]=[A[i][j]-f*A[r][j] for j in range(n)]
        r+=1
        if r==m:break
    return r

def main()->int:
    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    W=nx.Graph();W.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(pts[a])@J@np.array(pts[b]))%3==0:W.add_edge(a,b)
    assert W.number_of_edges()==240 and set(dict(W.degree()).values())=={12}
    lines=[frozenset(c) for c in nx.find_cliques(W) if len(c)==4];assert len(lines)==40
    # Every edge lies on exactly one W33 line.
    ec={e:0 for e in W.edges()}
    for L in lines:
        for e in itertools.combinations(sorted(L),2):ec[tuple(sorted(e))]+=1
    assert set(ec.values())=={1}

    Z=np.zeros((40,40),dtype=int)
    for j,L in enumerate(lines):
        for p in L:Z[p,j]=1
    assert set(map(int,Z.sum(0)))=={4} and set(map(int,Z.sum(1)))=={4}

    Q=nx.Graph();Q.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if lines[i]&lines[j]:Q.add_edge(i,j)
    assert Q.number_of_edges()==240 and set(dict(Q.degree()).values())=={12}
    assert not nx.is_isomorphic(W,Q)

    AW=nx.to_numpy_array(W,nodelist=range(40),dtype=int)
    AQ=nx.to_numpy_array(Q,nodelist=range(40),dtype=int)
    I=np.eye(40,dtype=int)
    assert np.array_equal(AW@Z,Z@AQ)
    assert np.array_equal(Z@Z.T,4*I+AW)
    assert np.array_equal(Z.T@Z,4*I+AQ)
    assert rank_q(Z)==25

    # Exact numerator projectors P2_num=60 E_2.
    P2W=-(AW-12*I)@(AW+4*I)
    P2Q=-(AQ-12*I)@(AQ+4*I)
    assert rank_q(P2W)==24 and rank_q(P2Q)==24
    assert np.array_equal(P2W@Z,Z@P2Q)
    assert np.array_equal(Z.T@P2W@Z,6*P2Q)
    assert np.array_equal(Z@P2Q@Z.T,6*P2W)

    # Kernel projectors are the -4 sectors, numerator Pm4=(AW-12I)(AW-2I)
    # which equals 96 E_-4.
    Pm4W=(AW-12*I)@(AW-2*I)
    Pm4Q=(AQ-12*I)@(AQ-2*I)
    assert rank_q(Pm4W)==15 and rank_q(Pm4Q)==15
    assert not np.any(Pm4W@Z)
    assert not np.any(Z@Pm4Q)

    out={
      'pass':4956,
      'incidence_shape':[40,40],
      'row_graph':'W(3,3) point graph',
      'column_graph':'Q(4,3) point graph = W(3,3) line-intersection graph',
      'identities':['A_W Z = Z A_Q','ZZ^T = 4I + A_W','Z^T Z = 4I + A_Q'],
      'rank_Z':25,
      'sector_action':{
        'dimension_1_eigenvalue_12':'Z scales all-ones by 4',
        'dimension_24_eigenvalue_2':'Z is an isomorphism; Z^T Z=ZZ^T=6I on the sector; inverse is Z^T/6',
        'dimension_15_eigenvalue_minus4':'Z annihilates both sides exactly'},
      'projector_numerators':{'E2':'-(A-12I)(A+4I)=60E2','Eminus4':'(A-12I)(A-2I)=96Eminus4'},
      'theorem':'Point-line incidence is the canonical rational intertwiner between the 24-dimensional +2 modules of W(3,3) and its odd-q dual Q(4,3). Its inverse on that sector is Z^T/6. The same unsigned incidence kills both 15-dimensional -4 modules.',
      'boundary':'The 24D bridge is canonical from incidence. No analogous unsigned incidence bridge exists on the 15D blind sectors.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
