#!/usr/bin/env python3
"""Pass 4464 -- symplectic quotient of the W33 apartment-parity code.

Pass 4463 defined the binary apartment-parity code

    C = { b^T H : b in F_2^40 } <= F_2^1620,

where H is line/apartment incidence.  It has dimension 39 because the only
coefficient vector in ker(H^T) is the all-ones vector.

Pass 4461 gave the integer identity

    H H^T = 156 I + 21 A* + 6 J,

so modulo two the induced bilinear form on coefficient vectors is exactly the
dual W33 adjacency matrix A*.

This pass proves

    rank_F2(A*) = 10,
    dim ker_F2(A*) = 30,

and the all-ones coefficient vector lies in ker(A*).  Therefore the radical of
the code C under the ambient binary dot product has dimension

    30 - 1 = 29,

and the quotient C / rad(C) has dimension

    39 - 29 = 10.

Because A* has zero diagonal, the induced bilinear form is alternating; after
quotienting by the radical it is nondegenerate.  Hence

    C / rad(C) is a 10-dimensional symplectic F_2-space.

This is a structural dimension statement, not a count match: the 10 is the
rank of the exact alternating Gram form induced by apartment parity.

For context, if N is the 40x40 point-line incidence matrix, then

    N^T N = 4I + A*  over Z,

so modulo two A*=N^T N.  The verifier also records rank_F2(N)=25; over
characteristic two, rank(N^T N)=10 is smaller because the dot product on the
25-dimensional incidence image has a 15-dimensional radical.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4463_apartment_parity_tomography import rank_mod2

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    _, lines, A, N, edge_line = geometry()
    cycles = simple_four_cycles(A)
    supports = [frozenset(edge_line[e] for e in C) for C in cycles]

    H = np.zeros((40, 1620), dtype=np.uint8)
    for j, support in enumerate(supports):
        for li in support:
            H[li, j] = 1

    Adual = np.zeros((40, 40), dtype=np.uint8)
    for i in range(40):
        for j in range(i + 1, 40):
            if lines[i] & lines[j]:
                Adual[i, j] = Adual[j, i] = 1

    # Recheck earlier invariants rather than importing result JSONs.
    rank_h = rank_mod2(H)
    rank_n = rank_mod2(N)
    rank_adual = rank_mod2(Adual)
    assert rank_h == 39
    assert rank_n == 25
    assert rank_adual == 10
    assert np.array_equal((H @ H.T) % 2, Adual)
    assert np.array_equal((N.T @ N) % 2, Adual)
    assert np.all(np.diag(Adual) == 0)
    assert np.all((Adual @ np.ones(40, dtype=np.uint8)) % 2 == 0)

    coefficient_kernel_dim = 40 - rank_adual
    line_sign_kernel_dim = 40 - rank_h
    radical_dim = coefficient_kernel_dim - line_sign_kernel_dim
    quotient_dim = rank_h - radical_dim
    assert coefficient_kernel_dim == 30
    assert line_sign_kernel_dim == 1
    assert radical_dim == 29
    assert quotient_dim == 10
    assert quotient_dim % 2 == 0

    # Incidence-image radical check: on im(N), the restricted dot product has
    # Gram N^T N of rank 10, so its radical inside the 25-dimensional image is 15.
    incidence_image_radical_dim = rank_n - rank_adual
    assert incidence_image_radical_dim == 15

    result = {
        "pass": 4464,
        "theorem": "W33 apartment parity code symplectic quotient theorem",
        "code": {
            "length": 1620,
            "dimension": 39,
            "radical_dimension": 29,
            "symplectic_quotient_dimension": 10,
        },
        "ranks_F2": {
            "line_apartment_H": rank_h,
            "point_line_incidence_N": rank_n,
            "dual_adjacency_Astar": rank_adual,
        },
        "identities_mod2": [
            "H H^T = A_star",
            "N^T N = A_star",
        ],
        "coefficient_form": {
            "dimension": 40,
            "kernel_dimension": coefficient_kernel_dim,
            "kernel_contains_global_reversal": True,
            "quotient_by_line_sign_kernel_gives_code_radical_dimension": radical_dim,
        },
        "incidence_image": {
            "dimension": 25,
            "restricted_dot_product_rank": 10,
            "radical_dimension": incidence_image_radical_dim,
        },
        "boundary": (
            "The 10-dimensional quotient is structural: it is the nondegenerate quotient of the exact "
            "alternating apartment Gram form over F_2.  No physical qubit count or unrelated Phi_4 "
            "identification is inferred from the dimension alone."
        ),
    }

    out = ROOT / "data" / "PART_W33_PASS4464_APARTMENT_CODE_SYMPLECTIC_QUOTIENT.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4464 -- apartment parity code symplectic quotient")
    print("  dim C = 39")
    print("  rank_F2(A*) = 10")
    print("  dim rad(C) = 29")
    print("  dim C/rad(C) = 10, nondegenerate alternating")
    print("  rank_F2(N) = 25; incidence-image radical = 15")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
