#!/usr/bin/env python3
"""Exact four-CZ logical action of uniform physical S on W33 adjacency CSS.

The plus-type E8/2E8 quadratic space was established in the prior isometry
certificate. This program verifies the new gate-level interpretation.
"""
import json
from w33_20261029_oddq_css_transversal_gate_obstruction import adjacency_q3, binary_basis

def add(x, pivots):
    for k in sorted(pivots, reverse=True):
        if (x >> k) & 1:
            x ^= pivots[k]
    if x:
        pivots[x.bit_length()-1] = x
        return True
    return False

def nullspace(rows, n=40):
    m=rows[:]
    piv={}
    r=0
    for j in range(n):
        s=next((i for i in range(r,n) if (m[i]>>j)&1), None)
        if s is None: continue
        m[r],m[s]=m[s],m[r]
        for i in range(n):
            if i!=r and ((m[i]>>j)&1): m[i]^=m[r]
        piv[j]=r
        r+=1
    basis=[]
    for j in range(n):
        if j in piv: continue
        v=1<<j
        for col,i in piv.items():
            if (m[i]>>j)&1: v^=1<<col
        assert all((v&x).bit_count()%2==0 for x in rows)
        basis.append(v)
    return basis

def span(vectors):
    values=[0]
    for x in vectors:
        values += [y^x for y in values[:]]
    return values

def q(v):
    assert v.bit_count()%2==0
    return (v.bit_count()//2)%2

def polar(x,y):
    return (x&y).bit_count()%2

def hyperbolic(vectors):
    rem=vectors[:]
    pairs=[]
    while rem:
        s=span(rem)
        e=next(x for x in s if x and q(x)==0)
        f=next(x for x in s if polar(e,x) and q(x)==0)
        pairs.append((e,f))
        rank={}
        projected=[]
        for x in rem:
            z=x^(e if polar(x,f) else 0)^(f if polar(x,e) else 0)
            if add(z,rank): projected.append(z)
        rem=projected
    return pairs

def main():
    A=adjacency_q3()
    C=binary_basis(A)
    kernel=nullspace(A)
    assert len(C)==16 and len(kernel)==24
    piv={}
    for v in A: add(v,piv)
    logical=[]
    for v in kernel:
        if add(v,piv): logical.append(v)
    assert len(logical)==8
    # All-ones belongs to C, forcing ker(A) to consist of even-weight vectors.
    assert ((1<<40)-1) in span(C)
    classes=span(logical)
    assert all(v.bit_count()%2==0 for v in classes)
    assert all(q(v)==q(v^A[0]) for v in classes)
    counts=[sum(q(v)==i for v in classes) for i in (0,1)]
    assert counts==[136,120]
    pairs=hyperbolic(logical)
    assert len(pairs)==4
    ordered=[v for pair in pairs for v in pair]
    assert all(q(v)==0 for v in ordered)
    for i,x in enumerate(ordered):
        for j,y in enumerate(ordered):
            assert polar(x,y)==int((i//2==j//2) and (i!=j))
    for bits in range(256):
        x=0
        for i,v in enumerate(ordered):
            if (bits>>i)&1:x^=v
        cz_parity=sum(((bits>>(2*i))&1)*((bits>>(2*i+1))&1) for i in range(4))%2
        assert q(x)==cz_parity
    out={"status":"PASS", "logical_qubits":8, "Arf":0,
         "q0_classes":136, "q1_classes":120,
         "hyperbolic_pairs":4,
         "physical_S_tensor40_logical_action":"CZ(0,1) CZ(2,3) CZ(4,5) CZ(6,7)",
         "basis_caveat":"Four CZ pairs after a chosen hyperbolic logical basis; not a physical layout claim.",
         "prior_art":"Existing W33 E8/2E8 isometry and Pass85 binary weight enumerator."}
    print(json.dumps(out,indent=2))
    return out

if __name__ == "__main__":
    main()
