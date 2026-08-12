#!/usr/bin/env python3
"""Pass4952 — singular-sector theorem for the corrected W33 point-line incidence.

Pass4955 identifies the Pass4946 40x40 non-splitting quotient Z exactly:
rows are W(3,3) points, columns are W(3,3) lines (equivalently Q(4,3)
points).  Hence

    ZZ^T = 4I + A_W,
    Z^T Z = 4I + A_Q,

where A_W is the standard W(3,3) point graph and A_Q is the nonisomorphic
Q(4,3) point graph / W33 line-intersection graph.  Both share the SRG
spectrum 12^1,2^24,(-4)^15, so Z has rank 25 and a 15-dimensional blind
sector on each side.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4952_DUAL_GQ_INCIDENCE_SINGULAR_FILTER.json"


def main() -> int:
    v, k, lam, mu = 40, 12, 2, 4
    line_size = 4
    r, s = 2, -4
    f = (-k - (v - 1) * s) // (r - s)
    g = v - 1 - f
    assert (f, g) == (24, 15)
    assert k + f * r + g * s == 0

    gram_eigs = {
        str(line_size + k): 1,
        str(line_size + r): f,
        str(line_size + s): g,
    }
    assert gram_eigs == {"16": 1, "6": 24, "0": 15}
    rank = 1 + f
    nullity = g
    assert (rank, nullity) == (25, 15)

    out = {
        "pass": 4952,
        "input": {
            "source": "Pass4946 quotient, corrected by Pass4954-Pass4955",
            "incidence": "W(3,3) point-line incidence",
            "rows": "40 W(3,3) points recovered from maximum-cut triples",
            "columns": "40 W(3,3) lines recovered from Steiner fibers; their collinearity graph is Q(4,3)",
            "row_weight": 4,
            "column_weight": 4,
        },
        "two_nonisomorphic_srg_sides": {
            "row_graph": "W(3,3) point graph",
            "column_graph": "Q(4,3) point graph = W(3,3) line-intersection graph",
            "shared_parameters": [v, k, lam, mu],
            "shared_spectrum": {"12": 1, "2": f, "-4": g},
        },
        "incidence_gram_identities": {
            "rows": "ZZ^T=4I+A_W",
            "columns": "Z^TZ=4I+A_Q43",
        },
        "gram_spectrum": gram_eigs,
        "singular_spectrum": {
            "4": 1,
            "sqrt(6)": 24,
            "0": 15,
        },
        "rank": rank,
        "left_kernel_dimension": nullity,
        "right_kernel_dimension": nullity,
        "sector_filter": {
            "constant_sector": "transmitted with singular value 4",
            "24_dimensional_eigenvalue_2_sector": "transmitted with squared singular value 6",
            "15_dimensional_eigenvalue_-4_sector": "annihilated exactly on both the W(3,3)-point and Q(4,3)-line sides",
        },
        "theorem": "The corrected max-cut/Steiner quotient is the W(3,3) point-line incidence matrix. It has rank 25 and singular spectrum 4^1, sqrt(6)^24, 0^15. The left kernel is the 15-dimensional -4 sector of the W(3,3) point graph; the right kernel is the 15-dimensional -4 sector of the nonisomorphic dual Q(4,3) line graph.",
        "boundary": "The unsigned incidence matrix does not identify the two 15-dimensional kernels; it annihilates both. Any bridge between those blind sectors requires additional signed/oriented structure.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
