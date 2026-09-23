#!/usr/bin/env python3
"""Complete the rank-73 cubic root chart with the exact dark Fourier/magic modes.

The full 81x270 E8 cubic-incidence transform has rank 73.  The dark eight has
already been decomposed as

    chi_ext + chi_ext^2 + V_omega + V_omega^2,

and the right multiplicity ray selecting V_omega is the qutrit Strange
Clifford image m=(1,-omega,0), with the conjugate ray selecting V_omega^2.

This file turns those theorems into one deterministic full coordinate basis:

  * choose the 73 lexicographically first pivot columns of the 270 cubic
    incidence matrix;
  * append the two external C3 Fourier characters;
  * append three matrix-coefficient columns for V_omega using m;
  * append the three conjugate matrix-coefficient columns for V_omega^2.

The resulting 81x81 matrix has exact rank 81 over Q(omega).  The eight added
columns are exactly orthogonal to all 270 cubic incidence columns. Their
Hermitian Gram is

    diag(81,81,54,54,54,54,54,54).

Thus the frozen 81-address/root space admits a complete hybrid chart
    73 cubic-support coordinates + 8 Fourier/magic dark coordinates.

Boundary: this is an invertible analysis-coordinate chart on the address/root
carrier. It is NOT the missing address-to-trinification/operator intertwiner.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

from sympy import Matrix as SympyMatrix

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

OUT = ROOT / "data/w33_e8_matter81_hybrid_cubic_dark_basis.json"

from w33_exact_eisenstein import (
    ONE,
    OMEGA,
    ZERO,
    identity_matrix,
    matrix_multiply,
    matrix_rank,
    matrix_scale,
    omega_power,
)

F = range(3)
H = tuple(itertools.product(F, repeat=3))
ID = (0, 0, 0)
KID = (ID, 0)
K = tuple((h, p) for h in H for p in F)
K_INDEX = {x: i for i, x in enumerate(K)}

DIRECTIONS = (
    ("omega", (0, 0, 1)),
    ("omega X", (0, 1, 1)),
    ("omega Z", (1, 0, 1)),
    ("Z X", (1, 1, 0)),
    ("omega^2 Z X^2", (1, 2, 2)),
)


def hmul(g, h):
    a, b, c = g
    A, B, C = h
    return ((a + A) % 3, (b + B) % 3, (c + C - b * A) % 3)


def kmul(x, y):
    return (hmul(x[0], y[0]), (x[1] + y[1]) % 3)


def right_cosets(subgroup):
    unseen = set(K)
    out = []
    while unseen:
        g = min(unseen)
        coset = frozenset(kmul(g, h) for h in subgroup)
        out.append(coset)
        unseen -= coset
    return out


def lifted_instructions():
    lines = []
    records = []
    for direction_index, (name, d) in enumerate(DIRECTIONS):
        for slope in (1, 2):
            generator = (d, slope)
            subgroup = frozenset((KID, generator, kmul(generator, generator)))
            cosets = right_cosets(subgroup)
            assert len(cosets) == 27
            for coset_index, line in enumerate(cosets):
                lines.append(line)
                records.append(
                    {
                        "direction_index": direction_index,
                        "direction_name": name,
                        "external_slope_mod3": slope,
                        "coset_index": coset_index,
                    }
                )
    assert len(lines) == len(set(lines)) == 270
    return lines, records


I3 = identity_matrix(3)
X = [
    [ZERO, ZERO, ONE],
    [ONE, ZERO, ZERO],
    [ZERO, ONE, ZERO],
]


def matpow(A, n):
    out = identity_matrix(len(A))
    for _ in range(n):
        out = matrix_multiply(out, A)
    return out


def matvec(A, v):
    return [
        sum((A[i][j] * v[j] for j in range(len(v))), ZERO)
        for i in range(len(A))
    ]


def rho_s(h, s):
    a, b, c = h
    Zs = [
        [ONE, ZERO, ZERO],
        [ZERO, omega_power(s), ZERO],
        [ZERO, ZERO, omega_power(2 * s)],
    ]
    return matrix_scale(
        omega_power(s * c),
        matrix_multiply(matpow(Zs, a), matpow(X, b)),
    )


def hermitian_dot(left, right):
    return sum(
        (a.conjugate() * b for a, b in zip(left, right)),
        ZERO,
    )


def pair_token(x):
    a, b = x.as_pair()
    return f"{a.numerator}/{a.denominator},{b.numerator}/{b.denominator}"


def main(write=True):
    lines, instruction_records = lifted_instructions()

    incidence_int = [[0] * 270 for _ in range(81)]
    for j, line in enumerate(lines):
        for x in line:
            incidence_int[K_INDEX[x]][j] = 1

    sym = SympyMatrix(incidence_int)
    assert sym.rank() == 73
    pivot_columns = list(sym.rref()[1])
    assert len(pivot_columns) == 73
    expected_pivots = [
        0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,
        27,28,30,31,33,34,36,37,39,40,42,43,45,46,48,49,51,52,54,55,56,57,63,
        64,65,66,72,73,74,75,81,82,90,91,99,100,108,109,110,111,117,120,126,
        129,135,136
    ]
    assert pivot_columns == expected_pivots

    # Two external Fourier character columns.
    dark_columns = [
        [omega_power(t * p) for h, p in K]
        for t in (1, 2)
    ]
    dark_labels = [
        "chi_ext",
        "chi_ext^2",
    ]

    # Three matrix coefficients for each conjugate H27 Schrodinger sector.
    for s, sector in ((1, "V_omega"), (2, "V_omega^2")):
        m = [ONE, -omega_power(s), ZERO]
        values_by_h = {h: matvec(rho_s(h, s), m) for h in H}
        for component in range(3):
            dark_columns.append(
                [values_by_h[h][component] for h, p in K]
            )
            dark_labels.append(f"{sector}:component_{component}")

    assert len(dark_columns) == 8
    assert matrix_rank([[col[row] for col in dark_columns] for row in range(81)]) == 8

    # Every dark mode is annihilated by every cubic-incidence column.
    for dark in dark_columns:
        for line in lines:
            assert sum((dark[K_INDEX[x]] for x in line), ZERO) == ZERO

    # Dark Hermitian Gram is diagonal with exact norms 81,81,54^6.
    dark_norms = []
    for i, left in enumerate(dark_columns):
        for j, right in enumerate(dark_columns):
            value = hermitian_dot(left, right)
            if i == j:
                expected = 81 * ONE if i < 2 else 54 * ONE
                assert value == expected
                dark_norms.append(int(expected.a))
            else:
                assert value == ZERO
    assert dark_norms == [81, 81, 54, 54, 54, 54, 54, 54]

    # Build the deterministic full 81x81 hybrid basis.
    columns = []
    for j in pivot_columns:
        columns.append([
            ONE if incidence_int[row][j] else ZERO
            for row in range(81)
        ])
    columns.extend(dark_columns)
    assert len(columns) == 81

    hybrid = [[columns[col][row] for col in range(81)] for row in range(81)]
    assert matrix_rank(hybrid) == 81

    # Compact reproducibility digest of the exact Q(omega) matrix.
    serial = "|".join(
        pair_token(hybrid[row][col])
        for row in range(81)
        for col in range(81)
    )
    digest = "sha256:" + hashlib.sha256(serial.encode()).hexdigest()

    rootlift = json.loads(
        (ROOT / "data/w33_hesse36_e8_matter81_root_lift_boundary.json").read_text()
    )
    dark = json.loads(
        (ROOT / "data/w33_hesse36_e8_matter81_dark8_decomposition.json").read_text()
    )
    strange = json.loads(
        (ROOT / "data/w33_hesse36_dark_schrodinger_strange_state.json").read_text()
    )
    assert rootlift["incidence"]["full_81x270_rank"] == 73
    assert dark["irreducible_decomposition"]["formula"] == (
        "chi_ext + chi_ext^2 + V_omega + V_omega^2"
    )
    assert strange["strange_bridge"]["same_projective_Clifford_orbit"] is True

    out = {
        "schema": "w33.e8_matter81_hybrid_cubic_dark_basis.v1",
        "status": "PASS_FULL_81D_HYBRID_COORDINATE_BASIS_IS_73_CUBIC_PLUS_8_FOURIER_MAGIC_MODES",
        "headline": (
            "The rank-73 cubic root chart is completed exactly by the classified "
            "dark eight. A deterministic set of 73 independent columns from the "
            "270 E8 cubic-incidence channels is augmented by the two nontrivial "
            "external C3 Fourier characters and six H27 matrix-coefficient modes "
            "selected by the Strange/conjugate-Strange multiplicity rays. The "
            "resulting 81x81 matrix has exact rank 81 over Q(omega)."
        ),
        "cubic_sector": {
            "full_instruction_columns": 270,
            "rank": 73,
            "selected_pivot_count": 73,
            "selected_pivot_indices_zero_based": pivot_columns,
            "selected_instruction_records": [
                instruction_records[j] for j in pivot_columns
            ],
        },
        "dark_sector": {
            "dimension": 8,
            "labels": dark_labels,
            "decomposition": "chi_ext + chi_ext^2 + V_omega + V_omega^2",
            "Hermitian_Gram_diagonal": dark_norms,
            "orthogonal_to_all_270_cubic_columns": True,
            "magic_multiplicity_ray": ["1", "-omega", "0"],
            "magic_ray_is_Clifford_equivalent_to_Strange": True,
        },
        "hybrid_basis": {
            "dimension": 81,
            "formula": "73 deterministic cubic pivots + 8 Fourier/magic dark modes",
            "field": "Q(omega)",
            "rank": 81,
            "matrix_digest": digest,
            "coordinate_order": (
                "first 73 selected cubic-incidence columns, then chi_ext, "
                "chi_ext^2, V_omega components 0..2, V_omega^2 components 0..2"
            ),
        },
        "compiler_reading": (
            "This closes the address/root coordinate span with a concrete invertible "
            "analysis transform. The remaining address-to-operator problem is no "
            "longer missing linear coordinates; it is the representation-theoretic "
            "task of matching this hybrid 73+8 chart to the trinification "
            "C9_multiplicity tensor C3_internal tensor C3_external operator chart."
        ),
        "boundary": (
            "The 81x81 hybrid matrix is not claimed to intertwine the regular "
            "address K action with the operator Pauli243 action; the prior rank "
            "obstruction forbids that full equivariance. It is an exact coordinate "
            "basis on the frozen address/root carrier, not a physical dynamics or "
            "vacuum theorem."
        ),
        "parents": [
            "data/w33_hesse36_e8_matter81_root_lift_boundary.json",
            "data/w33_hesse36_e8_matter81_dark8_decomposition.json",
            "data/w33_hesse36_dark_schrodinger_strange_state.json",
        ],
        "checks": {
            "full_incidence_rank73": True,
            "deterministic_73_pivots": True,
            "eight_dark_modes_independent": True,
            "all_dark_modes_annihilate_all_270_cubics": True,
            "dark_Gram_81_81_54x6": True,
            "hybrid_81x81_rank81": True,
            "operator_intertwiner_not_claimed": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
