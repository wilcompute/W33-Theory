#!/usr/bin/env python3
"""Exact binary incidence resolution for W(3,q), q=3,5,7 (prime).
No external packages. Geometry is reconstructed from F_q^4, not cached data.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
from pathlib import Path
import json

def rank_basis(rows):
    basis = {}
    for row in rows:
        add(row, basis)
    return basis

def reduce_row(x, basis):
    for j in sorted(basis, reverse=True):
        if (x >> j) & 1:
            x ^= basis[j]
    return x

def add(x, basis):
    x = reduce_row(x, basis)
    if not x:
        return False
    basis[x.bit_length()-1] = x
    return True

def make_geometry(q):
    def norm(x):
        x = tuple(int(a) % q for a in x)
        pivot = next((a for a in x if a), None)
        return tuple(a * pow(pivot, -1, q) % q for a in x) if pivot else None

    points = sorted({y for x in product(range(q), repeat=4)
                     if (y := norm(x)) is not None})
    idx = {p:i for i,p in enumerate(points)}
    def omega(x,y):
        return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2]) % q
    line_sets = set()
    for i,x in enumerate(points):
        for y in points[i+1:]:
            if omega(x,y):
                continue
            line = frozenset(idx[norm(((a*u+b*v) % q for u,v in zip(x,y)))]
                             for a,b in product(range(q),repeat=2) if a or b)
            assert len(line) == q+1
            line_sets.add(line)
    lines = sorted(line_sets, key=lambda x: tuple(sorted(x)))
    v = len(points)
    assert len(lines)==v==(q+1)*(q*q+1)
    adjacency = [0]*v
    incidence_rows = [0]*v
    line_masks = []
    for j,line in enumerate(lines):
        mask = sum(1<<p for p in line)
        line_masks.append(mask)
        for p in line:
            incidence_rows[p] |= (1<<j)
            adjacency[p] |= (mask^(1<<p))
    assert all(r.bit_count() == q*(q+1) for r in adjacency)
    assert all(r.bit_count() == q+1 for r in incidence_rows)
    return points, lines, line_masks, adjacency, incidence_rows, norm, omega

def matvec(rows, vector):
    out = 0
    for i,r in enumerate(rows):
        if (r & vector).bit_count() & 1:
            out |= 1<<i
    return out

def arf_invariant(vectors):
    def pair(a,b):
        return (a&b).bit_count() & 1
    def quad(a):
        return (a.bit_count() // 2) & 1
    remaining = vectors[:]
    arf = 0
    pairs = 0
    while remaining:
        e = remaining.pop(0)
        i = next(i for i,f in enumerate(remaining) if pair(e,f))
        f = remaining.pop(i)
        arf ^= quad(e) & quad(f)
        remaining = [w ^ (e if pair(w,f) else 0)
                       ^ (f if pair(w,e) else 0) for w in remaining]
        assert all(not pair(w,e) and not pair(w,f) for w in remaining)
        pairs += 1
    return arf, pairs

def compute(q):
    pts, lines, line_masks, A, N, norm, omega = make_geometry(q)
    v = len(pts)
    full = (1<<v)-1
    # Exact integer identity AN=J+(q-1)N, reduced modulo 2: AN=J.
    # N N^T=(q+1)I + A gives A=NN^T modulo 2.
    for x in A:
        folded = 0
        for j in range(v):
            if (x>>j)&1: folded ^= N[j]
        assert folded == full, "AN=J failed"
        assert matvec(A,x) == 0, "A^2=0 failed"
    assert all(matvec(A,l)==full for l in line_masks)
    basis_A = rank_basis(A)
    rank_A = len(basis_A)
    rank_N = len(rank_basis(N))
    assert rank_A+rank_N == v+1
    assert rank_A == (q**3+q+2)//2
    assert rank_N == (q*q+1)*(q+2)//2
    even_line_basis = rank_basis([line_masks[0]^l for l in line_masks[1:]])
    assert len(even_line_basis) == v-rank_A
    assert all(matvec(A,x)==0 for x in even_line_basis.values())
    full_basis = basis_A.copy()
    logical = []
    for line in line_masks[1:]:
        candidate = line_masks[0]^line
        if add(candidate,full_basis):
            logical.append(candidate)
    k = v-2*rank_A
    assert len(logical)==k==q*q-1
    # Every syndrome-free word has even Hamming weight because AN=J
    # implies the all-ones word lies in im(A).
    assert all(x.bit_count()%2==0 for x in logical)
    stab_doubly_even = q % 4 == 3
    # Generator self-intersections establish the mod-four obstruction.
    assert (q*(q+1))%4 == (0 if stab_doubly_even else 2)
    result = dict(q=q,points=v,lines=v,rank_incidence=rank_N,
                  rank_adjacency=rank_A,kernel_dimension=v-rank_A,
                  even_line_span_dimension=len(even_line_basis),
                  logical_dimension=k, incidence_rank_complement=True,
                  adjacency_nilpotent_mod2=True, adjacency_line_syndrome="all-ones",
                  doubly_even_stabilizer=stab_doubly_even)
    if stab_doubly_even:
        arf,pairs=arf_invariant(logical)
        result.update(arf_invariant=arf,orthogonal_type="plus" if arf==0 else "minus",
                      hyperbolic_pairs=pairs)
        assert arf==0
    if q==3:
        counts = Counter()
        for coeff in range(1<<k):
            x = 0
            for j,b in enumerate(logical):
                if (coeff>>j)&1:x^=b
            counts[(x.bit_count()//2)&1]+=1
        assert (counts[0],counts[1])==(136,120)
        result["quadratic_counts"]={"singular_including_zero":136,"nonsingular":120}
        hexads=set()
        for i,a in enumerate(line_masks):
            for b in line_masks[i+1:]:
                if (a&b).bit_count()==1:hexads.add(a^b)
        assert len(hexads)==240
        assert all(z.bit_count()==6 and matvec(A,z)==0 for z in hexads)
        result["intersecting_line_hexads"]=240
    return result

def main():
    results=[compute(q) for q in (3,5,7)]
    out=Path(__file__).resolve().parents[1]/"data/w33_incidence_even_line_resolution_20261029.json"
    out.write_text(json.dumps({"checked_fields":[3,5,7],"results":results},indent=2)+"\n",
                   encoding="utf-8")
    for result in results:
        print(json.dumps(result,sort_keys=True))
    print("W33 incidence-even-line resolution: ALL CHECKS PASS")

if __name__=="__main__":
    main()
