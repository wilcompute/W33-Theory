#!/usr/bin/env python3
"""Passes 7081--7096: exact E8 Z3/Z4 common refinement.

This packet puts two independently meaningful E8 gradings on one explicit root
system:

  * the repo's CE2 grading E8 -> (E6+A2) + (27,3) + (27*,3*), dimensions
        86 + 81 + 81;
  * the Kummer/spinor-tenfold grading E8 -> (D5+A3) + (16,4) + (10,6)
        + (16*,4*), dimensions 60 + 64 + 60 + 64.

They are obtained from adjacent simple-root coefficients whose highest-root marks
are 4 and 3.  The two toral gradings commute, so they refine to Z4 x Z3 ~= Z12.
The exact joint dimension table is

        z3=0  1  2
  z4=0   54   3   3
     1   16  48   0
     2    0  30  30
     3   16   0  48

and the CRT Z12 sector dimensions are
  [54,48,30,16,3,0,0,0,3,16,30,48].

The joint neutral semisimple root subsystem is D5+A2 (46 roots); the full
neutral reductive algebra has one additional Cartan direction, hence
  so(10) + sl(3) + u(1), dimension 45+8+1=54.

This is an exact root-system theorem.  It does not identify the resulting Z12
grade group with the separate mu_12 scalar phase group in the photonic/Clifford
lane; that equality of orders is recorded only as a target for an explicit map.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7081_7096_E8_Z3_Z4_Z12_COMMON_REFINEMENT.json'


def e8_roots_doubled():
    roots=[]
    for i,j in combinations(range(8),2):
        for si,sj in product((-2,2), repeat=2):
            v=[0]*8; v[i]=si; v[j]=sj; roots.append(tuple(v))
    for s in product((-1,1), repeat=8):
        if sum(1 for x in s if x==-1)%2==0:
            roots.append(tuple(s))
    assert len(roots)==len(set(roots))==240
    return roots


def dot(a,b): return sum(x*y for x,y in zip(a,b))


def simple_roots(root_subset, h):
    P={r for r in root_subset if dot(r,h)>0}
    assert len(P)*2==len(root_subset)
    out=[]
    for r in sorted(P):
        if not any(tuple(r[i]-a[i] for i in range(8)) in P for a in P):
            out.append(r)
    return out


def inverse_fraction(A):
    n=len(A)
    M=[[Fraction(A[i][j]) for j in range(n)]+[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv=next(i for i in range(c,n) if M[i][c])
        M[c],M[piv]=M[piv],M[c]
        q=M[c][c]; M[c]=[x/q for x in M[c]]
        for i in range(n):
            if i==c: continue
            q=M[i][c]
            if q: M[i]=[M[i][j]-q*M[c][j] for j in range(2*n)]
    return [row[n:] for row in M]


def matvec(A,x): return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]


def coeff_map(roots, simples):
    # simples are columns of the 8x8 coordinate matrix
    S=[[simples[j][i] for j in range(8)] for i in range(8)]
    I=inverse_fraction(S)
    out={}
    for r in roots:
        c=matvec(I,list(r))
        assert all(x.denominator==1 for x in c)
        ci=tuple(int(x) for x in c)
        rec=tuple(sum(simples[j][i]*ci[j] for j in range(8)) for i in range(8))
        assert rec==r
        out[r]=ci
    return out


def cartan(simple):
    return [[dot(a,b)//4 for b in simple] for a in simple]  # doubled roots have norm^2=8


def components_from_cartan(A):
    n=len(A); seen=set(); comps=[]
    for s in range(n):
        if s in seen: continue
        st=[s]; seen.add(s); C=[]
        while st:
            u=st.pop(); C.append(u)
            for v in range(n):
                if u!=v and A[u][v]==-1 and v not in seen:
                    seen.add(v); st.append(v)
        comps.append(sorted(C))
    return comps


def graph_isomorphic_component(A, nodes, target_edges):
    n=len(nodes)
    targ=np.zeros((n,n),dtype=int)
    for i,j in target_edges: targ[i,j]=targ[j,i]=1
    cur=np.zeros((n,n),dtype=int)
    for i,u in enumerate(nodes):
        for j,v in enumerate(nodes):
            if A[u][v]==-1: cur[i,j]=1
    for p in permutations(range(n)):
        if all(cur[i,j]==targ[p[i],p[j]] for i in range(n) for j in range(n)):
            return True
    return False


def classify_root_subsystem(roots, h):
    simp=simple_roots(roots,h); A=cartan(simp); comps=components_from_cartan(A)
    types=[]
    targets={
      'A2':(2,[(0,1)]),
      'A3':(3,[(0,1),(1,2)]),
      'D5':(5,[(0,1),(1,2),(2,3),(2,4)]),
      'E6':(6,[(0,1),(1,2),(2,3),(3,4),(2,5)]),
    }
    for C in comps:
        hit=[]
        for name,(n,edges) in targets.items():
            if len(C)==n and graph_isomorphic_component(A,C,edges): hit.append(name)
        assert len(hit)==1,(len(C),A,C,hit)
        types.append(hit[0])
    return '+'.join(sorted(types)),len(simp),A,comps


def crt(i,j):
    return next(n for n in range(12) if n%4==i and n%3==j)


def main():
    roots=e8_roots_doubled()
    h=(1,3,9,27,81,243,729,2187)
    simp=simple_roots(roots,h)
    assert len(simp)==8
    cm=coeff_map(roots,simp)
    pos=[r for r in roots if dot(r,h)>0]
    highest=max(pos,key=lambda r:sum(cm[r]))
    marks=cm[highest]
    # Deterministic ordering of the simple roots constructed above.
    assert marks==(4,6,5,4,3,2,2,3), marks

    # The useful adjacent nodes in THIS ordering are index 3 (mark 4) and
    # index 4 (mark 3).  Do not infer these indices from a textbook numbering.
    Z4_NODE=3
    Z3_NODE=4
    A8=cartan(simp)
    assert marks[Z4_NODE]==4 and marks[Z3_NODE]==3
    assert A8[Z4_NODE][Z3_NODE]==A8[Z3_NODE][Z4_NODE]==-1

    def grade_dims(node,m):
        cnt=Counter(cm[r][node]%m for r in roots)
        return [cnt[g]+(8 if g==0 else 0) for g in range(m)]

    z4=grade_dims(Z4_NODE,4); z3=grade_dims(Z3_NODE,3)
    assert z4==[60,64,60,64]
    assert z3==[86,81,81]

    Rz4=[r for r in roots if cm[r][Z4_NODE]%4==0]
    Rz3=[r for r in roots if cm[r][Z3_NODE]%3==0]
    t4,rank4,_,_=classify_root_subsystem(Rz4,h)
    t3,rank3,_,_=classify_root_subsystem(Rz3,h)
    assert t4=='A3+D5'
    assert t3=='A2+E6'
    assert rank4==rank3==8

    joint=[[0]*3 for _ in range(4)]
    for r in roots:
        joint[cm[r][Z4_NODE]%4][cm[r][Z3_NODE]%3]+=1
    joint[0][0]+=8 # Cartan
    assert joint==[[54,3,3],[16,48,0],[0,30,30],[16,0,48]]
    assert [sum(row) for row in joint]==z4
    assert [sum(joint[i][j] for i in range(4)) for j in range(3)]==z3

    R00=[r for r in roots if cm[r][Z4_NODE]%4==0 and cm[r][Z3_NODE]%3==0]
    t00,rank00,_,_=classify_root_subsystem(R00,h)
    assert len(R00)==46 and t00=='A2+D5' and rank00==7
    # Full E8 Cartan is 8-dimensional, so one central toral direction remains.
    neutral_dim=len(R00)+8
    assert neutral_dim==54

    z12=[0]*12
    for i in range(4):
        for j in range(3): z12[crt(i,j)]=joint[i][j]
    assert z12==[54,48,30,16,3,0,0,0,3,16,30,48]
    assert sum(z12)==248

    report={
      'passes':list(range(7081,7097)),
      'e8_root_certificate':{
        'roots':240,'rank':8,'simple_roots_doubled':[list(x) for x in simp],
        'highest_root_marks':list(marks),
        'z4_node_index':Z4_NODE,'z3_node_index':Z3_NODE,'nodes_adjacent':True
      },
      'z4_kummer_spinor_grading':{
        'grade_dimensions':z4,'neutral_root_type':'D5+A3','neutral_lie_dimension':60,
        'standard_branching_dimensions':'(45,1)+(1,15) | (16,4) | (10,6) | (16*,4*)'
      },
      'z3_ce2_grading':{
        'grade_dimensions':z3,'neutral_root_type':'E6+A2','neutral_lie_dimension':86,
        'standard_branching_dimensions':'(78,1)+(1,8) | (27,3) | (27*,3*)'
      },
      'joint_Z4xZ3_dimension_table':joint,
      'joint_neutral':{
        'root_count':46,'semisimple_type':'D5+A2','semisimple_rank':7,
        'extra_cartan_rank':1,'reductive_type':'so(10)+sl(3)+u(1)','dimension':54
      },
      'z12_crt_grading_dimensions':z12,
      'z12_sector_interpretation':{
        '0':'54 = so10 + sl3 + u1',
        '1':'48 = 16 x 3 dimension',
        '2':'30 = 10 x 3 dimension',
        '3':'16',
        '4':'3',
        '5':'0','6':'0','7':'0','8':'3','9':'16','10':'30','11':'48'
      },
      'status':'EXACT_COMMON_REFINEMENT_OF_CE2_Z3_AND_KUMMER_Z4_INSIDE_E8',
      'boundary':'The Z12 grading is an E8 root-space grading. The repo also has an independent mu_12 scalar phase-group theorem for qutrit Clifford gates; equality of the orders 12 does not identify those structures. An explicit character/intertwiner is required before connecting them.'
    }
    OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__': main()
