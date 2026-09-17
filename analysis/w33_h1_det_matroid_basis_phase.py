#!/usr/bin/env python3
"""Matroid-basis formula for the quartic H1 determinant phase over F3.

The latest determinant-magic witness uses four independent Pauli directions
(e1,e2,e3,e4), forms S=sum_i v_i v_i^T and X=S J, and obtains det(X)=1.
This file proves the basis-independent generalization.

For V=[v_1 ... v_m] in F3^{4 x m},

    det(V V^T)
      = sum_{|I|=4} det(V_I)^2                 (Cauchy--Binet)
      = # {basis 4-subsets of the column matroid M(V)}  (mod 3),

because every nonzero square in F3 equals 1.  Since det(J)=1,

    det(X) = T_M(1,1) mod 3,   X=(V V^T)J,

where T_M(1,1) is the number of matroid bases.

Thus the candidate central-character phase is

    omega^(r det X) = omega^(r T_M(1,1) mod 3).

For exactly four projective Pauli directions this is nontrivial iff the four
directions form a projective basis; every projective basis gives det(X)=1.
We also exhaust all 4- and 5-subsets of PG(3,3) as a regression census.

Scope: this is exact finite algebra/combinatorics.  It does not establish the
VOA/OPE coupling needed to turn the candidate phase into a physical gate.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_h1_det_matroid_basis_phase.json"
P = 3
J = np.array(
    [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
    dtype=np.int64,
) % P


def canon(v):
    v = np.asarray(v, dtype=np.int64) % P
    i = next(i for i, x in enumerate(v) if x)
    return tuple((v * pow(int(v[i]), -1, P)) % P)


PG = sorted(
    {canon(v) for v in itertools.product(range(P), repeat=4) if any(v)}
)
assert len(PG) == 40


def det_mod3(A):
    A = np.asarray(A, dtype=np.int64).copy() % P
    n = A.shape[0]
    d = 1
    for c in range(n):
        q = next((r for r in range(c, n) if A[r, c]), None)
        if q is None:
            return 0
        if q != c:
            A[[c, q]] = A[[q, c]]
            d = -d
        a = int(A[c, c])
        d = d * a % P
        ia = pow(a, -1, P)
        for r in range(c + 1, n):
            if A[r, c]:
                A[r] = (A[r] - A[r, c] * ia * A[c]) % P
    return d % P


def basis_count(columns):
    """Number of rank-4 column bases, counted by ground-set index subset."""
    V = np.asarray(columns, dtype=np.int64).T % P
    if V.shape[0] != 4:
        raise ValueError("columns must lie in F3^4")
    return sum(
        det_mod3(V[:, I]) != 0
        for I in itertools.combinations(range(V.shape[1]), 4)
    )


def determinant_phase_exponent(columns, r=1):
    """Return r*det((VV^T)J) mod 3."""
    V = np.asarray(columns, dtype=np.int64).T % P
    S = V @ V.T % P
    X = S @ J % P
    return (r * det_mod3(X)) % P


def main(write=True):
    assert det_mod3(J) == 1

    # Exhaust all 4-subsets of projective Pauli directions.
    four = Counter()
    basis4 = set()
    for I in itertools.combinations(range(40), 4):
        cols = [PG[i] for i in I]
        b = basis_count(cols)
        d = determinant_phase_exponent(cols, r=1)
        assert b in (0, 1) and d == b
        four[(b, d)] += 1
        if b:
            basis4.add(I)

    # Closed-form count of unordered projective bases:
    # |GL(4,3)| / ((3-1)^4 4!).
    gl43 = math.prod(P**4 - P**i for i in range(4))
    closed_projective_bases = gl43 // ((P - 1) ** 4 * math.factorial(4))
    assert closed_projective_bases == 63180 == len(basis4)
    assert sum(four.values()) == math.comb(40, 4) == 91390
    assert four == Counter({(1, 1): 63180, (0, 0): 28210})

    # Exhaust all 5-subsets.  Cauchy--Binet predicts d = #bases mod 3.
    five_basis = Counter()
    five_det = Counter()
    for I in itertools.combinations(range(40), 5):
        b = sum(tuple(x for x in I if x != drop) in basis4 for drop in I)
        cols = [PG[i] for i in I]
        d = determinant_phase_exponent(cols, r=1)
        assert d == b % 3
        five_basis[b] += 1
        five_det[d] += 1

    assert five_basis == Counter({0: 51480, 3: 252720, 4: 252720, 5: 101088})
    assert five_det == Counter({0: 304200, 1: 252720, 2: 101088})
    assert sum(five_basis.values()) == math.comb(40, 5) == 658008

    # Direct generic checks, including repeated/parallel columns.
    samples = [
        [PG[0], PG[1], PG[2], PG[3]],
        [PG[0], PG[0], PG[1], PG[2], PG[3]],
        [PG[0], PG[1], PG[2], PG[3], PG[4], PG[5]],
    ]
    for cols in samples:
        b = basis_count(cols)
        d = determinant_phase_exponent(cols, r=1)
        assert d == b % 3

    out = {
        "schema": "w33.h1_det_matroid_basis_phase.v1",
        "status": "PASS",
        "headline": (
            "For any Pauli-direction matrix V over F3, the quartic H1 determinant "
            "det((VV^T)J) equals the number of rank-4 bases of the represented "
            "column matroid modulo 3. Equivalently det(X)=T_M(1,1) mod 3. "
            "The two-operator e1,e2,e3,e4 witness is therefore not exceptional: "
            "every projective basis gives determinant 1."
        ),
        "identity": {
            "cauchy_binet": "det(V V^T) = sum_{|I|=4} det(V_I)^2",
            "F3_reduction": "det(V_I)^2 is 1 for a basis and 0 otherwise",
            "symplectic_factor": "det(J)=1",
            "matroid": "det((V V^T)J) = #bases(M(V)) mod 3 = T_M(1,1) mod 3",
            "candidate_phase": "omega^(r T_M(1,1)) for central character r in F3",
            "deletion_contraction": (
                "For an ordinary element e, the phase exponent obeys "
                "b(M)=b(M\\e)+b(M/e) mod 3."
            ),
        },
        "PG33_four_subset_census": {
            "total": math.comb(40, 4),
            "projective_bases": len(basis4),
            "dependent": four[(0, 0)],
            "closed_form_projective_bases": "|GL(4,3)|/(2^4*4!) = 63180",
            "determinant_distribution": {"0": four[(0, 0)], "1": four[(1, 1)], "2": 0},
        },
        "PG33_five_subset_census": {
            "total": math.comb(40, 5),
            "basis_count_distribution": {str(k): five_basis[k] for k in sorted(five_basis)},
            "determinant_distribution": {str(k): five_det[k] for k in range(3)},
        },
        "minimality": (
            "With four projective directions, det(X) is nonzero iff they span F3^4; "
            "then det(X)=1. Fewer than four directions have rank at most three and "
            "determinant zero."
        ),
        "interpretation": (
            "The proposed determinant phase is a mod-3 matroid/Tutte invariant of "
            "the Pauli support, not a coordinate artifact. It can be evaluated "
            "recursively by deletion-contraction."
        ),
        "boundary": (
            "This theorem identifies the exact finite combinatorial invariant seen by "
            "the determinant candidate. It does not prove that the A8^3 VOA OPE "
            "couples to this invariant or that hardware can address the coefficient."
        ),
        "checks": {
            "PG33_40_points": True,
            "cauchy_binet_basis_law_exhaustive_4sets": True,
            "cauchy_binet_basis_law_exhaustive_5sets": True,
            "projective_basis_count_63180": True,
            "five_subset_census_658008": True,
            "four_direction_minimality": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
