#!/usr/bin/env python3
"""
BT691 — K33 classical-vs-quantum code boundary.

BT686 and BT688 use K33 code language.  This script separates the clean,
verified classical cycle code from a quantum hypergraph-product interpretation.

Canonical graph K_{3,3}:
  |V|=6, |E|=9, beta_1=9-6+1=4.
  Its classical binary cycle code has parameters [9,4,4].

Boundary:
  The phrase [[9,4,4]] is not the standard hypergraph-product quantum code
  from the incidence matrix of K_{3,3}.  The standard Tillich-Zemor HGP of the
  6x9 incidence matrix H with itself has

      n = n1^2 + r1^2 = 9^2 + 6^2 = 117
      k = 2 * dim ker(H) * dim ker(H^T) = 2*4*0 = 0

  over F2, because rank(H)=5 for connected bipartite K33, so dim ker(H)=4
  and dim ker(H^T)=0.

Thus [9,4,4] is the graph-cycle code / homology carrier; it can support a
four-dimensional logical/fusion register, but it should not be labeled as a
standard [[9,4,4]] quantum stabilizer code without an additional construction.
"""
from __future__ import annotations
import itertools
import numpy as np


def gf2_rank(M: np.ndarray) -> int:
    A = (M.copy() % 2).astype(np.uint8)
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i, c]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            A[[r, pivot]] = A[[pivot, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i, :] ^= A[r, :]
        r += 1
        if r == m:
            break
    return r


def main() -> None:
    left = range(3)
    right = range(3)
    edges = [(i,j) for i in left for j in right]
    vertices = [("L",i) for i in left] + [("R",j) for j in right]
    H = np.zeros((6, 9), dtype=np.uint8)
    for eidx, (i,j) in enumerate(edges):
        H[i, eidx] = 1
        H[3+j, eidx] = 1

    rankH = gf2_rank(H)
    kerH = H.shape[1] - rankH
    cokerH = H.shape[0] - rankH
    beta1 = len(edges) - len(vertices) + 1
    assert rankH == 5
    assert kerH == beta1 == 4
    assert cokerH == 1  # connected graph component count over F2 incidence.

    # Classical cycle-code distance: minimum nonzero even subgraph is a 4-cycle.
    min_weight = 10
    codeword_count = 0
    for mask in range(1, 1 << len(edges)):
        v = np.array([(mask >> i) & 1 for i in range(len(edges))], dtype=np.uint8)
        if np.all((H @ v) % 2 == 0):
            codeword_count += 1
            min_weight = min(min_weight, int(v.sum()))
    assert codeword_count == (2**kerH - 1)
    assert min_weight == 4

    # Standard HGP self-product parameters using H as parity check.
    n_hgp = H.shape[1] ** 2 + H.shape[0] ** 2
    k_hgp = 2 * kerH * (H.shape[0] - rankH)
    assert n_hgp == 117
    assert k_hgp == 8  # includes the one-dimensional left kernel/component factor.

    # If one instead removes the redundant component row to full row rank 5x9,
    # then coker=0 and the self-HGP encodes zero qubits.
    Hred = H[:5, :]
    rank_red = gf2_rank(Hred)
    assert rank_red == 5
    n_hgp_red = 9**2 + 5**2
    k_hgp_red = 2 * (9-rank_red) * (5-rank_red)
    assert n_hgp_red == 106
    assert k_hgp_red == 0

    print("BT691 K33 code boundary: PASS")
    print("classical_cycle_code=[9,4,4]")
    print(f"incidence_rank_F2={rankH}")
    print(f"cycle_dimension={kerH}")
    print(f"cycle_distance={min_weight}")
    print(f"nonzero_cycle_codewords={codeword_count}")
    print(f"standard_HGP_full_incidence_n={n_hgp}")
    print(f"standard_HGP_full_incidence_k={k_hgp}")
    print(f"standard_HGP_reduced_incidence_n={n_hgp_red}")
    print(f"standard_HGP_reduced_incidence_k={k_hgp_red}")
    print("boundary=[9,4,4] is classical graph-cycle/homology code, not automatically [[9,4,4]] quantum stabilizer code")


if __name__ == "__main__":
    main()
