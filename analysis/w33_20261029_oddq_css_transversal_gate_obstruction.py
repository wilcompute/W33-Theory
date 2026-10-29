#!/usr/bin/env python3
"""Independent transversal-gate audit for odd-order GQ(q,q) adjacency CSS codes.

Exact q=3 reconstruction and 2^16-word audit; all-odd-q proof uses
only generalized-quadrangle strongly-regular parameters. No hardware claim.
"""
import itertools
import json
from collections import Counter

def canonical(v, p):
    s = pow(next(x for x in v if x % p), -1, p)
    return tuple((s*x) % p for x in v)

def adjacency_q3():
    p = 3
    points = sorted({canonical(v, p) for v in itertools.product(range(p), repeat=4) if any(v)})
    def pair(x, y):
        return (x[0]*y[1] - x[1]*y[0] + x[2]*y[3] - x[3]*y[2]) % p
    rows = [sum(1 << j for j,y in enumerate(points) if i != j and pair(x,y) == 0)
            for i,x in enumerate(points)]
    assert len(points) == 40 and all(x.bit_count() == 12 for x in rows)
    assert all((rows[i]&rows[j]).bit_count() == (2 if (rows[i]>>j)&1 else 4)
               for i in range(40) for j in range(i+1,40))
    return rows

def binary_basis(rows):
    pivots = {}
    for word in rows:
        while word:
            k = word.bit_length()-1
            if k in pivots:
                word ^= pivots[k]
            else:
                pivots[k] = word
                break
    return list(pivots.values())

def exact_weight_distribution(basis):
    x = 0
    prev = 0
    counts = Counter({0: 1})
    for i in range(1, 1 << len(basis)):
        gray = i ^ (i >> 1)
        bit = (gray ^ prev).bit_length()-1
        x ^= basis[bit]
        counts[x.bit_count()] += 1
        prev = gray
    return dict(sorted(counts.items()))

def odd_q_certificate(q):
    assert q >= 3 and q % 2 == 1
    degree = q*(q+1)
    adjacent_overlap = q-1
    other_overlap = q+1
    assert degree % 2 == adjacent_overlap % 2 == other_overlap % 2 == 0
    # All row pairings, including self pairings, vanish in F2.
    # All row weights are 0 mod 4 iff q == 3 mod 4.
    if degree % 8 != 0:
        witness = {"kind": "single adjacency row", "weight": degree}
    else:
        weight = 2*degree - 2*adjacent_overlap
        assert weight % 8 == 4
        witness = {"kind": "sum of two adjacent adjacency rows", "weight": weight}
    return {
        "q": q,
        "points": (q+1)*(q*q+1),
        "row_weight": degree,
        "neighbor_overlap": adjacent_overlap,
        "nonneighbor_overlap": other_overlap,
        "self_orthogonal": True,
        "doubly_even": q%4 == 3,
        "uniform_S_preserves_CSS": q%4 == 3,
        "uniform_T_obstruction": {**witness, "weight_mod8": witness["weight"]%8},
    }

def main():
    rows = adjacency_q3()
    basis = binary_basis(rows)
    assert len(basis) == 16
    dist = exact_weight_distribution(basis)
    expected = {0:1,8:45,12:1120,16:15570,20:32064,
                24:15570,28:1120,32:45,40:1}
    assert dist == expected and sum(dist.values()) == 65536
    assert all(weight % 4 == 0 for weight in dist)
    assert all((x & y).bit_count() % 2 == 0 for x in rows for y in rows)
    anchors = [odd_q_certificate(q) for q in (3,5,7,9,11,13,17,19,23,31)]
    assert all(a["uniform_T_obstruction"]["weight_mod8"] != 0 for a in anchors)
    result = {
        "status": "PASS",
        "q3_binary_code": "[40,16,8]",
        "q3_CSS": "[[40,8,6]]_2 (distance independently certified by prior W33 repo test)",
        "q3_full_weight_enumerator": dist,
        "q3_uniform_H_and_S_preserve": True,
        "all_odd_q_uniform_T_obstructed": True,
        "odd_q_examples": anchors,
    }
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()
