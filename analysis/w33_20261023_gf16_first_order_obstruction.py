#!/usr/bin/env python3
"""Exact GF(16) W(3,q) Pascal CSS module extension via binary bitset elimination.

No dense floating-point linear algebra. Provides independent controls
for the GF(4)/GF(8) and GF(16) first-order connecting obstruction.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np

def f2_tables(q):
    poly={4:0b111,8:0b1011,16:0b10011}[q]
    deg=q.bit_length()-1
    mul=np.zeros((q,q),dtype=np.uint8)
    for a in range(q):
        for b in range(q):
            x=a; y=b; z=0
            while y:
                if y&1:z^=x
                y>>=1;x<<=1
                if x&q:x^=poly
            mul[a,b]=z
    inv=np.array([0]+[next(i for i in range(1,q) if mul[a,i]==1)
                           for a in range(1,q)],dtype=np.uint8)
    return mul,inv


def to_int(x):
    return int.from_bytes(np.packbits(np.asarray(x,dtype=np.uint8),bitorder="little").tobytes(),"little")


def rank_rows(rows):
    piv={}
    for row in rows:
        z=int(row)
        while z:
            bit=z&-z; j=bit.bit_length()-1
            if j in piv:z^=piv[j]
            else:piv[j]=z;break
    return piv


def kernel(piv,n):
    nonp=[j for j in range(n) if j not in piv]
    order=sorted(piv,reverse=True)
    for f in nonp:
        x=1<<f
        for pos in order:
            if ((piv[pos]&x).bit_count())%2:x^=1<<pos
        yield x


def construct(q):
    mul,inv=f2_tables(q)
    pts=[]
    for i in range(4):
        for n in range(q**(3-i)):
            tail=[]; t=n
            for _ in range(3-i):tail.append(t%q);t//=q
            pts.append((0,)*i+(1,)+tuple(tail))
    P=np.array(pts,dtype=np.uint8);n=len(P)
    assert n==(q+1)*(q*q+1)
    def form(w):
        return (mul[P[:,0],w[1]]^mul[P[:,1],w[0]]^
                mul[P[:,2],w[3]]^mul[P[:,3],w[2]])
    cb=rank_rows((to_int(form(row)!=0) for row in P))
    assert len(cb)==q*q,(q,len(cb))
    w=np.array([1,0,0,0],dtype=np.uint8); f=form(w)
    new=P.copy()
    for j in range(4):new[:,j]^=mul[f,w[j]]
    for j in range(n):
        lead=int(np.flatnonzero(new[j])[0])
        new[j]=mul[new[j],inv[new[j,lead]]]
    indices={tuple(row):i for i,row in enumerate(P)}
    perm=np.array([indices[tuple(row)] for row in new],dtype=np.int32)
    assert np.array_equal(perm[perm],np.arange(n))
    def D(x):
        u=np.unpackbits(np.frombuffer(x.to_bytes((n+7)//8,"little"),dtype=np.uint8),
                bitorder="little")[:n]
        return x^to_int(u[perm])
    pivDC=rank_rows(D(z) for z in cb.values())
    K=list(kernel(cb,n))
    assert len(K)==n-len(cb)
    # Every vector in computed K is orthogonal to C.
    for x in K:
        for c in cb.values():
            assert (x&c).bit_count()%2==0
    pivDK=rank_rows(D(x) for x in K)
    piv_sum=rank_rows(list(cb.values())+list(pivDK.values()))
    dim_intersection=len(cb)+len(pivDK)-len(piv_sum)
    delta=dim_intersection-len(pivDC)
    assert delta>=0
    # p=2: dim ker(D) = #T-orbits, nullity controls.
    fixed=int(np.count_nonzero(perm==np.arange(n)))
    moved=n-fixed
    assert moved==q**3
    return {"q":q,"p":2,"n":n,"dimC":len(cb),"dimK":len(K),
            "rankDC":len(pivDC),"rankDK":len(pivDK),
            "rank_C_plus_DK":len(piv_sum),"rank_DK_intersection_C":dim_intersection,
            "rank_delta1":delta,"fixed_points_T":fixed,"moving_pairs":moved//2,
            "all_rows_verified_orthogonal":True}


def run():
    cases=[construct(q) for q in (4,8,16)]
    return {"schema":"w33.gf2_frobenius_delta_exact.v1","cases":cases,
       "scope":"Exact GF(16) first-order extension obstruction measured by kernel/bitset elimination, not a general Frobenius module theorem."}

if __name__=="__main__":
    import sys
    data=json.dumps(run(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(data,encoding="utf-8")
    else:print(data)
