#!/usr/bin/env python3
"""Identify the dark H27 multiplicity ray with qutrit Strange magic.

The rank-73 root-lift theorem leaves one copy each of the conjugate 3D H27
Schrodinger modules in the dark eight.  In the regular representation this
means that the right/multiplicity qutrit factor contains a one-dimensional
common annihilator for the four selected noncentral Hesse directions.

In the frozen convention
    rho(a,b,c) = omega^c Z^a X^b,  ZX=omega XZ,
the four selected noncentral generators are
    omega X, omega Z, Z X, omega^2 Z X^2.

For each d let A_d = I + rho(d) + rho(d)^2.  A_d is three times the
eigenvalue-one projector.  Stacking the four A_d gives exact rank 2, hence a
unique projective common kernel.  It is

    m = (1,-omega,0)^T.

Moreover, for the repository's qutrit Strange reference
    s = (0,1,-1)^T
we have exactly
    m = Z X^2 s.

Thus the dark multiplicity ray is a single-qutrit Clifford image of the
Strange magic state.  The omega^2 dark sector carries its complex conjugate.

This is NOT the M36 resource: M36_Q4_RAW is the separate ququart/two-qubit
Witting-ray resource and its injection boundary is unchanged.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

OUT = ROOT / "data/w33_hesse36_dark_schrodinger_strange_state.json"

from w33_exact_eisenstein import (
    ONE,
    OMEGA,
    ZERO,
    identity_matrix,
    matrix_add,
    matrix_multiply,
    matrix_rank,
    matrix_scale,
    omega_power,
)


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


def matrix_equal(A, B):
    return len(A) == len(B) and all(
        len(a) == len(b) and all(x == y for x, y in zip(a, b))
        for a, b in zip(A, B)
    )


I3 = identity_matrix(3)
X = [
    [ZERO, ZERO, ONE],
    [ONE, ZERO, ZERO],
    [ZERO, ONE, ZERO],
]
Z = [
    [ONE, ZERO, ZERO],
    [ZERO, OMEGA, ZERO],
    [ZERO, ZERO, omega_power(2)],
]


def rho(g):
    a, b, c = g
    return matrix_scale(
        omega_power(c),
        matrix_multiply(matpow(Z, a), matpow(X, b)),
    )


def main(write=True):
    # Exact qutrit Weyl relation.
    assert matrix_equal(matrix_multiply(Z, X), matrix_scale(OMEGA, matrix_multiply(X, Z)))

    directions = [
        ("omega X", (0, 1, 1)),
        ("omega Z", (1, 0, 1)),
        ("Z X", (1, 1, 0)),
        ("omega^2 Z X^2", (1, 2, 2)),
    ]

    projectors = []
    for _name, d in directions:
        R = rho(d)
        assert matrix_equal(matpow(R, 3), I3)
        projectors.append(matrix_add(I3, R, matpow(R, 2)))

    stacked = [row for A in projectors for row in A]
    assert matrix_rank(stacked) == 2

    magic_ray = [ONE, -OMEGA, ZERO]
    assert all(all(x == ZERO for x in matvec(A, magic_ray)) for A in projectors)

    strange = [ZERO, ONE, -ONE]
    zx2_strange = matvec(matrix_multiply(Z, matpow(X, 2)), strange)
    assert zx2_strange == magic_ray

    # Projective norm squared is 2 both before and after the Clifford.
    norm_magic = sum((x.conjugate() * x for x in magic_ray), ZERO)
    norm_strange = sum((x.conjugate() * x for x in strange), ZERO)
    assert norm_magic == norm_strange == 2 * ONE

    dark = json.loads(
        (ROOT / "data/w33_hesse36_e8_matter81_dark8_decomposition.json").read_text()
    )
    pass416 = json.loads(
        (ROOT / "data/w33_pass416_qutrit_distillation_search.json").read_text()
    )
    economy = json.loads((ROOT / "data/w33_magic_economy.json").read_text())
    m36_source = (ROOT / "analysis/bt2767_m36_factory.py").read_text()

    assert dark["irreducible_decomposition"]["formula"] == (
        "chi_ext + chi_ext^2 + V_omega + V_omega^2"
    )
    assert pass416["reference_validation"]["Strange_state_definition"] == (
        "(|1>-|2>)/sqrt(2)"
    )
    assert pass416["checks"]["strange_state_reference_fixed"] is True
    assert economy["mana"]["strange_is"] == "log(5/3) (max single-qutrit mana)"
    assert "36 ququart/two-qubit Witting rays" in m36_source
    assert "does not identify them with qutrit magic states" in m36_source

    out = {
        "schema": "w33.hesse36_dark_schrodinger_strange_state.v1",
        "status": "PASS_DARK_SCHRODINGER_MULTIPLICITY_RAY_IS_QUTRIT_STRANGE_CLIFFORD_IMAGE",
        "headline": (
            "The six-dimensional Schrodinger part of the rank-73 dark complement "
            "has a unique qutrit multiplicity ray. The four selected noncentral "
            "H27 Hesse directions have eigenvalue-one projectors whose stacked "
            "matrix has rank two, and their common kernel is the projective ray "
            "(1,-omega,0). Exactly, (1,-omega,0)=Z X^2 (0,1,-1), so this ray is "
            "a Clifford image of the repository's qutrit Strange magic state. "
            "The conjugate V_omega^2 sector carries the conjugate ray."
        ),
        "qutrit_convention": {
            "weyl_relation": "Z X = omega X Z",
            "selected_noncentral_directions": [
                {"name": name, "H27_coordinate": list(d)} for name, d in directions
            ],
            "projector_formula": "A_d = I + rho(d) + rho(d)^2",
            "stacked_projector_rank": 2,
            "common_kernel_dimension": 1,
        },
        "dark_multiplicity_ray": {
            "unnormalized": ["1", "-omega", "0"],
            "squared_norm": 2,
            "annihilated_by_all_four_Hesse_projectors": True,
            "interpretation": (
                "right/multiplicity qutrit ray selecting the surviving left "
                "V_omega copy in the regular H27 module"
            ),
        },
        "strange_bridge": {
            "repository_reference_state": "(|1>-|2>)/sqrt(2)",
            "unnormalized_reference": ["0", "1", "-1"],
            "exact_Clifford_word": "Z X^2",
            "exact_identity": "(1,-omega,0) = Z X^2 (0,1,-1)",
            "same_projective_Clifford_orbit": True,
            "repository_strange_mana": "log(5/3)",
        },
        "dark8_reading": {
            "formula": dark["irreducible_decomposition"]["formula"],
            "one_dimensional_part": "chi_ext + chi_ext^2",
            "six_dimensional_part": "V_omega + V_omega^2",
            "six_dimensional_multiplicity_data": (
                "Strange ray plus its complex conjugate in the right qutrit factor"
            ),
        },
        "M36_firewall": {
            "same_resource_as_M36_Q4_RAW": False,
            "M36_carrier": "ququart/two-qubit Witting rays",
            "this_carrier": "single-qutrit H27 multiplicity ray",
            "M36_injection_boundary_changed": False,
        },
        "compiler_consequence": (
            "The root-level dark sector is no longer anonymous: its two 3D pieces "
            "are selected by a qutrit Strange/conjugate-Strange multiplicity pair, "
            "while its two 1D pieces are the nontrivial external C3 Fourier "
            "characters. This gives a natural Fourier-plus-magic basis for the "
            "eight modes that cubic incidence misses."
        ),
        "boundary": (
            "The Clifford equivalence to the qutrit Strange state is exact finite "
            "linear algebra. It does not identify the dark ray with the separate "
            "M36 ququart resource, prove a physical magic-state injection route, "
            "or show that the dark root coordinates are dynamically populated."
        ),
        "parents": [
            "data/w33_hesse36_e8_matter81_dark8_decomposition.json",
            "data/w33_pass416_qutrit_distillation_search.json",
            "data/w33_magic_economy.json",
        ],
        "checks": {
            "ZX_equals_omega_XZ": True,
            "four_order3_projectors": True,
            "stacked_projector_rank2": True,
            "unique_common_kernel_ray": True,
            "ray_is_1_minusomega_0": True,
            "exact_ZX2_strange_identity": True,
            "strange_reference_certificate_loaded": True,
            "M36_type_firewall": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
