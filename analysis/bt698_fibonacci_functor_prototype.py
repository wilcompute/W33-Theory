#!/usr/bin/env python3
"""
BT698 — Fibonacci functor prototype.

Construct the safest first functor from the local K33 cycle code to Fibonacci
fusion registers.

Layer 1: K33 classical cycle code.
  K33 has |E|=9, |V|=6, beta_1=4, minimum cycle weight 4.
  Choose a spanning tree with 5 edges; the four omitted chords give four
  fundamental 4-cycle/6-cycle generators.  The cycle code is F2^4.

Layer 2: Fibonacci register architecture.
  One four-anyon Fibonacci block with fixed total charge has dimension 2.
  Four independent blocks therefore have Hilbert dimension 2^4=16, matching
  the 16 binary cycle-code states.

Prototype functor:
  F : H1(K33;F2) -> tensor_basis((C^2_Fib)^\otimes4)
      b=(b0,b1,b2,b3) |-> |b0 b1 b2 b3>_Fib.

Boundary:
  This is a register functor / basis identification.  It is not yet a braid
  representation functor: assigning the K33 graph automorphisms or cycle moves
  to Fibonacci braid words is a separate BT target.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import Counter
import numpy as np


def gf2_rank(M: np.ndarray) -> int:
    A = (M.copy() % 2).astype(np.uint8)
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i,c]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            A[[r,pivot]] = A[[pivot,r]]
        for i in range(m):
            if i != r and A[i,c]:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return r


def main() -> None:
    left = range(3)
    right = range(3)
    edges = [(i,j) for i in left for j in right]
    edge_index = {e:i for i,e in enumerate(edges)}

    # Incidence matrix over F2.
    H = np.zeros((6,9), dtype=np.uint8)
    for idx,(i,j) in enumerate(edges):
        H[i,idx] = 1
        H[3+j,idx] = 1
    rank = gf2_rank(H)
    beta1 = 9-rank
    assert rank == 5
    assert beta1 == 4

    # A convenient spanning tree: all edges incident to L0 plus vertical spine R0-L1,L2.
    tree = [(0,0),(0,1),(0,2),(1,0),(2,0)]
    chords = [e for e in edges if e not in tree]
    assert len(chords) == 4

    # Fundamental cycles relative to that tree.
    # In K33, chord (i,j), i,j != 0, closes rectangle L0-R0-Li-Rj-L0.
    basis = []
    for i,j in chords:
        cyc_edges = [(0,0), (i,0), (i,j), (0,j)]
        v = np.zeros(9, dtype=np.uint8)
        for e in cyc_edges:
            v[edge_index[e]] = 1
        assert np.all((H @ v) % 2 == 0)
        assert int(v.sum()) == 4
        basis.append(v)
    B = np.stack(basis, axis=1)  # 9 x 4
    assert gf2_rank(B.T) == 4

    # Generate all 16 codewords.
    codewords = []
    weights = Counter()
    for bits in product([0,1], repeat=4):
        coeff = np.array(bits, dtype=np.uint8)
        cw = (B @ coeff) % 2
        assert np.all((H @ cw) % 2 == 0)
        codewords.append((bits, tuple(int(x) for x in cw)))
        weights[int(cw.sum())] += 1
    assert len({cw for _,cw in codewords}) == 16
    assert min(w for w,c in weights.items() if w > 0) == 4

    # Fibonacci block dimensions: one fixed-total four-anyon block = C^2.
    fib_block_dim = 2
    blocks = 4
    fib_hilbert_dim = fib_block_dim ** blocks
    assert fib_hilbert_dim == len(codewords) == 16

    print("BT698 Fibonacci functor prototype: PASS")
    print("K33_cycle_code=[9,4,4]")
    print(f"cycle_basis_chords={chords}")
    print("basis_cycles_are_rectangles=True")
    print(f"cycle_code_weight_distribution={dict(sorted(weights.items()))}")
    print("fib_fixed_total_four_anyon_block_dim=2")
    print("fib_blocks_required_for_full_code=4")
    print("tensor_hilbert_dim=16")
    print("functor=F2^4 cycle bits -> computational basis of (C^2_Fib)^tensor4")
    print("boundary=register functor only; braid-word functor remains open")


if __name__ == "__main__":
    main()
