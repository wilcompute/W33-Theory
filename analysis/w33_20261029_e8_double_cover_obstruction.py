#!/usr/bin/env python3
"""Exact integral E8 double-cover obstruction for the W(3,3) logical PSp4(3).

Uses previously certified finite generators as input. The integer witness is
validated against its E8 Gram matrix AND the 4-factor finite group word.
All 315 finite involutions and both conjugacy classes are enumerated.
An order-two element whose E8 lift squares to -I forbids a group section.
"""
from collections import Counter, deque
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT / "data/w33_20261029_explicit_mod2_E8_isometry.json"
OUT = ROOT / "data/w33_20261029_e8_double_cover_obstruction.json"
WORD = (0, 1, 5, 4)
# Columns of an integral E8 Weyl automorphism in the simple-root basis.
WCOL = [
 [1,2,3,2,2,1,1,2], [0,0,0,0,-1,-1,-1,0],
 [-1,-2,-3,-2,-1,-1,0,-2], [0,-1,-1,-1,-1,0,0,0],
 [1,3,4,4,3,2,1,2], [1,1,1,0,0,0,0,0],
 [-2,-3,-5,-4,-3,-2,-1,-2], [0,1,2,1,1,1,0,1]
]
ID8 = tuple(1 << i for i in range(8))

def apply(columns, vector):
    answer = 0
    while vector:
        bit = vector & -vector
        answer ^= columns[bit.bit_length()-1]
        vector ^= bit
    return answer

def compose(left, right):
    return tuple(apply(left, z) for z in right)

def rank8(vectors):
    basis = {}
    for v in vectors:
        while v:
            pivot = v.bit_length()-1
            if pivot not in basis:
                basis[pivot] = v
                break
            v ^= basis[pivot]
    return len(basis)

def mm(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(8))
                       for j in range(8)) for i in range(8))

def transpose(A):
    return tuple(tuple(A[j][i] for j in range(8)) for i in range(8))

def root_q(x, edges):
    return (x.bit_count() + sum(((x >> i)&1)*((x >> j)&1)
                                for i,j in edges)) & 1

def conjugacy(seed, generators):
    reached = {seed}
    queue = deque([seed])
    while queue:
        x = queue.popleft()
        for g in generators:
            inverse = compose(g, g)  # all seven generators have order 3
            y = compose(compose(g,x),inverse)
            if y not in reached:
                reached.add(y)
                queue.append(y)
    return reached

def main():
    old = json.loads(PRIOR.read_text(encoding="utf-8"))
    edges = [tuple(edge) for edge in old["E8_Dynkin_edges"]]
    generators = [tuple(item["E8_simple_root_mod2_columns"])
                  for item in old["checked_group_generators"]]
    assert len(generators) == 7
    assert all(compose(compose(g,g),g) == ID8 for g in generators)
    assert all(root_q(apply(g,x),edges) == root_q(x,edges)
               for g in generators for x in range(256))
    finite = ID8
    for idx in WORD:
        finite = compose(finite,generators[idx])
    assert finite != ID8 and compose(finite,finite) == ID8
    assert rank8([finite[i] ^ ID8[i] for i in range(8)]) == 4

    M = transpose(WCOL)
    I = tuple(tuple(int(i == j) for j in range(8)) for i in range(8))
    minus_I = tuple(tuple(-v for v in row) for row in I)
    Cartan = tuple(tuple(2 if i==j else -1 if (i,j) in edges or
                           (j,i) in edges else 0 for j in range(8))
                   for i in range(8))
    assert mm(mm(transpose(M), Cartan), M) == Cartan
    assert mm(M,M) == minus_I
    reduction = tuple(sum((M[r][c]&1)<<r for r in range(8))
                      for c in range(8))
    assert reduction == finite

    seen = {ID8}
    queue = deque([ID8])
    invol = []
    while queue:
        g = queue.popleft()
        if g != ID8 and compose(g,g) == ID8:
            invol.append(g)
        for h in generators:
            z = compose(g,h)
            if z not in seen:
                seen.add(z)
                queue.append(z)
    assert len(seen) == 25920 and len(invol) == 315
    ranks = Counter(rank8([g[i]^ID8[i] for i in range(8)]) for g in invol)
    assert ranks == {4:270, 2:45}
    cls4 = conjugacy(finite,generators)
    assert len(cls4) == 270
    second = next(g for g in invol if g not in cls4)
    cls2 = conjugacy(second,generators)
    assert len(cls2) == 45 and not (cls2 & cls4)
    result = {
      "status": "PASS", "base": str(PRIOR.relative_to(ROOT)),
      "finite_group_order": len(seen), "involutions": len(invol),
      "involution_rank_class_sizes": {str(k):v for k,v in sorted(ranks.items())},
      "rank4_conjugacy_class_size": len(cls4),
      "rank2_conjugacy_class_size": len(cls2),
      "witness_word_0_based_generators": list(WORD),
      "finite_witness_mod2_columns": finite,
      "integral_lift_columns": WCOL,
      "integral_Cartan_preserved": True, "integral_square": "-I8",
      "non_split_conclusion": "No homomorphic section of the pullback of W(E8) -> O8+(2) over this PSp4(3) subgroup. All 270 conjugate involutions have order-four lifts.",
      "physical_boundary": "Group-theoretic obstruction only; not an E8 physical action, Hamiltonian, or measurement."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("PASS: 25920 group, 315 involutions, class 270+45, integral lift squares -I")
if __name__ == "__main__":
    main()
