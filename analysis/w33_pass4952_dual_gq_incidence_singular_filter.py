#!/usr/bin/env python3
"""Pass4952 — singular-sector theorem for the Pass4946 dual W33 incidence.

Pass4946 proves that the 40x40 quotient non-splitting matrix Z is the point-line
incidence matrix of a generalized quadrangle of order (3,3), whose point and
line collinearity graphs have SRG(40,12,2,4).  This script derives the exact
singular spectrum and identifies the invisible 15-dimensional sectors.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4952_DUAL_GQ_INCIDENCE_SINGULAR_FILTER.json"


def main() -> int:
    v, k, lam, mu = 40, 12, 2, 4
    line_size = 4

    # SRG restricted eigenvalues solve x^2-(lam-mu)x-(k-mu)=0.
    # Here x^2+2x-8=(x-2)(x+4).
    r, s = 2, -4
    # multiplicities from 1+f+g=v and k+f*r+g*s=0.
    f = (-k - (v - 1) * s) // (r - s)
    g = v - 1 - f
    assert (f, g) == (24, 15)
    assert k + f * r + g * s == 0

    # For a GQ incidence matrix Z, ZZ^T = (q+1)I + A_line = 4I+A_line.
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
            "source": "Pass4946 40x40 non-splitting quotient",
            "incidence": "generalized quadrangle point-line incidence of order (3,3)",
            "row_weight": 4,
            "column_weight": 4,
            "point_and_line_collinearity_srg": [v, k, lam, mu],
        },
        "srg_spectrum": {
            "12": 1,
            "2": f,
            "-4": g,
        },
        "incidence_gram_identity": "ZZ^T=4I+A_line and Z^TZ=4I+A_point",
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
            "15_dimensional_eigenvalue_-4_sector": "annihilated exactly on both point and line sides",
        },
        "theorem": "The Pass4946 max-cut/Steiner quotient incidence has rank 25 and singular spectrum 4^1, sqrt(6)^24, 0^15. Its left and right 15-dimensional kernels are exactly the -4 primitive sectors of the dual line and point W33 collinearity actions.",
        "boundary": "The unsigned incidence matrix does not identify the two 15-dimensional kernels; it annihilates both. Any point-line bridge on that sector requires additional signed/oriented data.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
