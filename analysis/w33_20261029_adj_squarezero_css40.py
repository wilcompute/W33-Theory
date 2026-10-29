#!/usr/bin/env python3
"""Exact W(3,3) binary adjacency CSS [[40,8,6]] and logical hexads.

An explicit finite geometry/code certificate, not a physical photon,
fault-tolerance threshold or priority claim for binary SRG adjacency codes.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import json

def point(v):
    x=next(a for a in v if a)
    return tuple(a*(1 if x==1 else 2)%3 for a in v)

def points():
    return sorted({point(v) for v in product(range(3),repeat=4) if any(v)})

def symp(u,v):
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3

def basis(rows):
    piv={}
    for row in rows:
        x=row
        while x:
            j=x.bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return [piv[j] for j in sorted(piv,reverse=True)]

def rank(rows):
    return len(basis(rows))

def adjacency():
    P=points()
    assert len(P)==40
    A=[sum(1<<j for j,y in enumerate(P) if i!=j and symp(x,y)==0)
       for i,x in enumerate(P)]
    return P,A

def lines(P,A):
    index={x:i for i,x in enumerate(P)}
    found=set()
    for i,j in combinations(range(40),2):
        if not (A[i]>>j)&1:continue
        u,v=P[i],P[j]
        S=frozenset(index[point(tuple((a*u[k]+b*v[k])%3 for k in range(4)))]
                    for a,b in product(range(3),repeat=2) if a or b)
        assert len(S)==4
        found.add(S)
    return sorted(found,key=lambda t:tuple(sorted(t)))

def row_distribution(A):
    b=basis(A); out=Counter(); w=0; old=0
    for i in range(1<<len(b)):
        gray=i^(i>>1)
        if i:w^=b[(gray^old).bit_length()-1]
        old=gray
        out[w.bit_count()]+=1
    return dict(sorted(out.items()))

def low_kernel(A):
    counts={};hexads=[]
    for n in range(1,7):
        counts[n]=0
        for I in combinations(range(40),n):
            x=0
            for i in I:x^=A[i]
            if not x:
                counts[n]+=1
                if n==6:hexads.append(sum(1<<i for i in I))
    return counts,hexads

def cut_rank(A,S):
    mask=sum(1<<i for i in S)
    return rank([A[i] & (((1<<40)-1)^mask) for i in S])

def verify():
    P,A=adjacency()
    assert len(A)==40 and all(a.bit_count()==12 for a in A)
    assert all(((A[i]>>j)&1)==((A[j]>>i)&1) for i in range(40) for j in range(40))
    assert all((A[i]&A[j]).bit_count()%2==0 for i in range(40) for j in range(40))
    assert all((A[i]&A[j]).bit_count()==(2 if (A[i]>>j)&1 else 4)
               for i,j in combinations(range(40),2))
    assert rank(A)==16
    W=row_distribution(A)
    assert W=={0:1,8:45,12:1120,16:15570,20:32064,24:15570,
               28:1120,32:45,40:1}
    lows,words=low_kernel(A)
    assert lows=={1:0,2:0,3:0,4:0,5:0,6:240}
    L=lines(P,A)
    assert len(L)==40
    assert all(sum(i in L0 for L0 in L)==4 for i in range(40))
    hexads={sum(1<<i for i in a^b) for a,b in combinations(L,2)
            if len(a&b)==1}
    assert len(hexads)==240 and hexads==set(words)
    assert set(sum((w>>i)&1 for w in words) for i in range(40))=={36}
    assert {cut_rank(A,line) for line in L}=={4}
    assert {cut_rank(A,[i for i in range(40) if (w>>i)&1]) for w in words}=={5}
    # Distinguish the point-line incidence matrix B from adjacency A.
    B=[sum(1<<j for j,line in enumerate(L) if i in line) for i in range(40)]
    assert rank(B)==25
    assert all(((B[i]&B[j]).bit_count()%2)==((A[i]>>j)&1)
               for i in range(40) for j in range(40))
    return {
      "schema":"w33.binary.adjacency_css40.hexad.v1",
      "parameters":{"v":40,"degree":12,"lambda":2,"mu":4,"edges":240,"lines":40},
      "binary_adjacency_rank":16,"A_squared_mod2_is_zero":True,
      "point_line_incidence_rank":25,"B_BT_mod2_equals_A":True,
      "CSS":{"n":40,"k":8,"d":6,"X_checks":16,"Z_checks":16,
             "X_distance":6,"Z_distance":6},
      "rowspace_weight_enumerator":{str(k):v for k,v in W.items()},
      "kernel_low_weight_counts":{str(k):v for k,v in lows.items()},
      "minimum_logical_hexads":len(hexads),
      "geometric_description":"Each weight-six vector is the symmetric difference of two intersecting 4-point isotropic lines; shared point deleted.",
      "hexads_per_vertex":36,
      "graph_state_entanglement":{"line_cut_ebits":4,"hexad_cut_ebits":5,
                                  "global_binary_adjacency_rank_ceiling":16},
      "sample_hexad":sorted(i for i in range(40) if (min(hexads)>>i)&1),
      "adjacency_rows_hex":[hex(x) for x in A],
      "projective_point_coordinates":[list(x) for x in P],
      "line_vertex_indices":[sorted(x) for x in L],
      "caveat":"Finite binary CSS code, not a universal physical gauge theory, photon loss threshold, or 240 W33-edge/E8-root equivariant bijection."
    }

if __name__=="__main__":
    import sys
    record=verify()
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in record.items()
                      if k not in ("adjacency_rows_hex","projective_point_coordinates","line_vertex_indices")},indent=2))
