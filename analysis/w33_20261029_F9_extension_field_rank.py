#!/usr/bin/env python3
"""Independent extension-field q=9 replay of the W(3,q) binary incidence law.
F9 = F3[t]/(t*t+1), encoded 3*a+b for a+b*t; 1 is integer 3.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json
from w33_incidence_even_line_resolution_20261029 import rank_basis,matvec
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261029_F9_extended_incidence.json"
def add(x,y):
    a,b=divmod(x,3);c,d=divmod(y,3)
    return 3*((a+c)%3)+(b+d)%3
def neg(x):
    a,b=divmod(x,3)
    return 3*((-a)%3)+((-b)%3)
def mul(x,y):
    a,b=divmod(x,3);c,d=divmod(y,3)
    return 3*((a*c+2*b*d)%3)+((a*d+b*c)%3)
INV={x:next(y for y in range(1,9) if mul(x,y)==3) for x in range(1,9)}
def norm(v):
    v=tuple(v)
    first=next((x for x in v if x),None)
    return tuple(mul(x,INV[first]) for x in v) if first is not None else None
def omega(x,y):
    return add(add(mul(x[0],y[1]),mul(x[2],y[3])),
               neg(add(mul(x[1],y[0]),mul(x[3],y[2]))))
def main():
    q=9
    assert all(mul(x,INV[x])==3 for x in range(1,9))
    pts=sorted(set(filter(None,(norm(x) for x in product(range(q),repeat=4)))))
    I={p:i for i,p in enumerate(pts)}
    lines=set()
    for i,x in enumerate(pts):
        for y in pts[i+1:]:
            if omega(x,y):continue
            line=frozenset(I[norm(tuple(add(mul(a,u),mul(b,v)) for u,v in zip(x,y)))]
                  for a,b in product(range(q),repeat=2) if a or b)
            assert len(line)==q+1
            lines.add(line)
    lines=sorted(lines,key=lambda z:tuple(sorted(z)))
    v=len(pts)
    assert len(lines)==v==820
    A=[0]*v;N=[0]*v
    lm=[]
    for j,line in enumerate(lines):
        mask=sum(1<<k for k in line);lm.append(mask)
        for i in line:
            A[i]|=mask^(1<<i)
            N[i]|=1<<j
    full=(1<<v)-1
    for row in A:
        assert matvec(A,row)==0
        combined=0
        z=row
        while z:
            low=z&-z
            combined ^= N[low.bit_length()-1]
            z ^= low
        assert combined==full
    ra=len(rank_basis(A));rn=len(rank_basis(N))
    even_span=len(rank_basis([lm[0]^x for x in lm[1:]]))
    assert (ra,rn,even_span,v-2*ra)==(370,451,450,80)
    assert rn+ra==v+1
    data={"field":"F3[t]/(t^2+1)","v":v,"rank_A_mod2":ra,
          "rank_N_mod2":rn,"even_line_span_rank":even_span,
          "kernel_rank":v-ra,"logical_dimension":v-2*ra,
          "A_squared_zero_mod2":True,"AN_equal_J_mod2":True,
          "scope":"independent finite-field, finite-geometry code; distance remains unproved"}
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    print(json.dumps(data,sort_keys=True))
if __name__=="__main__":main()
