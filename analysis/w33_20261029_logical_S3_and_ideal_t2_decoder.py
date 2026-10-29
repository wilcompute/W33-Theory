#!/usr/bin/env python3
"""Exact ideal Pauli decoder and restricted physical H/S group on W33 CSS."""
import itertools,json
from collections import deque

def adjacency():
    p=3
    def norm(v):
        t=pow(next(x for x in v if x),-1,3)
        return tuple(t*a%3 for a in v)
    pts=sorted({norm(x) for x in itertools.product(range(3),repeat=4) if any(x)})
    def form(a,b):return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3
    return [sum(1<<j for j,y in enumerate(pts) if i!=j and form(x,y)==0) for i,x in enumerate(pts)]

def syn(A,x):
    return sum(((x&a).bit_count()%2)<<i for i,a in enumerate(A))

def decoder(A):
    lookup={0:0}
    for w in (1,2):
        for inds in itertools.combinations(range(40),w):
            x=sum(1<<j for j in inds);s=syn(A,x)
            assert s not in lookup
            lookup[s]=x
    assert len(lookup)==821
    count=1
    for w in (1,2):
        for inds in itertools.combinations(range(40),w):
            for paulis in itertools.product((1,2,3),repeat=w):
                x=sum(1<<i for i,a in zip(inds,paulis) if a&1)
                z=sum(1<<i for i,a in zip(inds,paulis) if a&2)
                assert lookup[syn(A,x)]==x and lookup[syn(A,z)]==z
                count+=1
    assert count==7141
    return dict(syndromes=821,checked_pauli_errors=count,assumption="perfect syndrome extraction, ideal correction")

def mul(a,b):
    def image(x):
        result=0
        for j in range(4):
            if x>>j&1:result^=a[j]
        return result
    return tuple(image(x) for x in b)

def logical_group():
    I=(1,2,4,8)
    HF=(8,4,2,1) # SWAP(H tensor H), symplectic image
    CZ=(9,6,4,8) # physical S becomes logical CZ in hyperbolic pair
    assert mul(HF,HF)==I and mul(CZ,CZ)==I
    r=mul(HF,CZ)
    assert mul(mul(r,r),r)==I
    seen={I};Q=deque([I])
    while Q:
        x=Q.popleft()
        for g in (HF,CZ):
            y=mul(g,x)
            if y not in seen:seen.add(y);Q.append(y)
    assert len(seen)==6
    # Check (HF * CZ)^3=I EXACTLY including phases: use integers 2HF and CZ.
    M=[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
    # swap second/third rows of H tensor H is incorporated above.
    M=[[M[i][j]*(-1 if j==3 else 1) for j in range(4)] for i in range(4)]
    def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    cube=mm(mm(M,M),M)
    assert all(cube[i][j]==(8 if i==j else 0) for i in range(4) for j in range(4))
    return dict(group="S3",order=6,per_pair_H="SWAP(H tensor H)",per_pair_S="CZ",pairs=4,
                exact_phase_relation="H^2=S^2=(HS)^3=I",
                addressability="same two physical global gates act on all four pairs simultaneously")

def main():
    A=adjacency()
    assert len(A)==40 and all(row.bit_count()==12 for row in A)
    result={"status":"PASS","geometry":"W(3,3) adjacency CSS [[40,8,6]]",
            "ideal_decoder":decoder(A),"uniform_H_S_logical_group":logical_group(),
            "scope":"No physical photonic encoding, noisy syndrome extraction, independent logical-pair gates, or threshold."}
    print(json.dumps(result,indent=2))
    return result

if __name__=="__main__":main()
