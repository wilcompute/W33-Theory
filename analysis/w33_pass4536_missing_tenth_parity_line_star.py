#!/usr/bin/env python3
"""Pass 4536 -- the missing tenth protected direction is coefficient parity.

Pass 4534 proved that the 240 protected edge images A_*(e_i+e_j) span the
unique 9-dimensional invariant submodule V9 of the 10-dimensional protected
space im(A_*).  This pass identifies the missing quotient exactly.

Because the dual W33 line graph is connected, its edge endpoint vectors
{e_i+e_j : i~j} span the full even-weight hyperplane E <= F_2^40.  The
restriction A_*|_E has rank 9 while A_* has rank 10.  Since ker(A_*) has
dimension 30 and ker(A_*) cap E also has dimension 30, every kernel vector has
even coefficient parity.  Hence parity descends to a well-defined nonzero
linear functional

    pi(A_* b) = sum_i b_i mod 2

on im(A_*), with kernel exactly V9=A_*(E).  Any single line-star column A_*e_i
therefore supplies the missing tenth direction.  Exhausting all 2^10 protected
vectors further proves that the odd coset has minimum ambient weight 12, attained
exactly by the 40 line-star columns (and the even coset's weight-20 shell is
exactly the 240 protected edge images).

This is finite binary linear algebra.  "Parity bit" is not a physical qubit or
measurement until a hardware map is separately supplied.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import numpy as np

from w33_apartment_section_core import build_geometry, rank2
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4536_MISSING_TENTH_PARITY_LINE_STAR.json"


def vecmask(v) -> int:
    return sum(int(b) << i for i, b in enumerate(v) if b)


def independent_columns(A: np.ndarray) -> list[int]:
    """Deterministically choose the first lexicographic column basis over GF(2)."""
    piv: list[int] = []
    current = np.zeros((A.shape[0], 0), dtype=np.uint8)
    r = 0
    for j in range(A.shape[1]):
        trial = np.column_stack((current, A[:, j]))
        rr = rank2(trial)
        if rr > r:
            piv.append(j)
            current = trial
            r = rr
        if r == rank2(A):
            break
    return piv


def main() -> int:
    _pts, _pidx, _lines, _lidx, _Ap, A, *_ = build_geometry()
    assert A.shape == (40, 40) and rank2(A) == 10

    edges = [(i, j) for i in range(40) for j in range(i + 1, 40) if A[i, j]]
    assert len(edges) == 240
    eye = np.eye(40, dtype=np.uint8)
    endpoint = np.asarray([eye[i] ^ eye[j] for i, j in edges], dtype=np.uint8)
    assert rank2(endpoint) == 39  # connected graph -> full even-weight hyperplane
    assert all(int(row.sum()) % 2 == 0 for row in endpoint)

    edge_images = np.asarray([A[:, i] ^ A[:, j] for i, j in edges], dtype=np.uint8)
    assert rank2(edge_images) == 9

    K = np.asarray(nullspace_mod2(A), dtype=np.uint8)
    assert K.shape == (30, 40)
    assert all(int(v.sum()) % 2 == 0 for v in K)

    # Every single line star is outside the edge span and completes it to H10.
    assert all(rank2(np.vstack((edge_images, A[:, i]))) == 10 for i in range(40))
    assert len({vecmask(A[:, i]) for i in range(40)}) == 40

    # Exhaust im(A) using a deterministic ten-column basis, retaining coefficient
    # parity of its canonical preimage. Kernel-evenness proves parity is independent
    # of the chosen preimage.
    piv = independent_columns(A)
    assert len(piv) == 10
    assert rank2(A[:, piv]) == 10
    distributions = {0: Counter(), 1: Counter()}
    image_by_parity = {0: set(), 1: set()}
    for mask in range(1 << 10):
        y = np.zeros(40, dtype=np.uint8)
        parity = 0
        for k, j in enumerate(piv):
            if (mask >> k) & 1:
                y ^= A[:, j]
                parity ^= 1
        m = vecmask(y)
        assert m not in image_by_parity[1 - parity]
        image_by_parity[parity].add(m)
        distributions[parity][int(y.sum())] += 1
    assert len(image_by_parity[0]) == len(image_by_parity[1]) == 512
    assert image_by_parity[0].isdisjoint(image_by_parity[1])

    even_expected = {0: 1, 16: 135, 20: 240, 24: 135, 40: 1}
    odd_expected = {12: 40, 20: 432, 28: 40}
    assert dict(sorted(distributions[0].items())) == even_expected
    assert dict(sorted(distributions[1].items())) == odd_expected

    edge_set = {vecmask(v) for v in edge_images}
    even_weight20 = {
        m for m in image_by_parity[0]
        if int(sum((m >> i) & 1 for i in range(40))) == 20
    }
    assert edge_set == even_weight20
    line_stars = {vecmask(A[:, i]) for i in range(40)}
    odd_weight12 = {
        m for m in image_by_parity[1]
        if int(sum((m >> i) & 1 for i in range(40))) == 12
    }
    assert line_stars == odd_weight12

    # All line-star columns represent the same nonzero class modulo V9 because
    # their pairwise differences are images of even coefficient vectors.
    for i in range(40):
        assert vecmask(A[:, 0] ^ A[:, i]) in image_by_parity[0]

    out = {
        "pass": 4536,
        "protected_dimension": 10,
        "edge_span_dimension": 9,
        "coefficient_even_hyperplane_dimension": 39,
        "kernel_dimension": 30,
        "kernel_is_even": True,
        "canonical_column_basis": piv,
        "quotient_functional": "pi(A_* b) = sum_i b_i mod 2",
        "kernel_of_pi": "V9 = span{A_*(e_i+e_j): i~j} = A_*(even coefficient vectors)",
        "minimal_missing_shell": {
            "ambient_weight": 12,
            "multiplicity": 40,
            "objects": "the forty single-line stars A_* e_i"
        },
        "protected_weight_enumerator_by_pi": {
            "pi_0": {str(k): v for k, v in even_expected.items()},
            "pi_1": {str(k): v for k, v in odd_expected.items()}
        },
        "edge_shell_identity": "the 240 pi=0 vectors of ambient weight 20 are exactly the protected dual-W33 edge images",
        "line_star_coset_identity": "the 40 pi=1 vectors of minimum ambient weight 12 are exactly the forty line-star columns; all represent the same nonzero class in H10/V9",
        "theorem": "The missing tenth protected direction is exactly coefficient parity. One line-star augments the nine local edge directions to all of H10, and no edge combination can change this parity bit.",
        "boundary": "Exact finite GF(2) statement. The quotient functional is not a physical qubit, charge, or measurement without a separate implementation theorem."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
