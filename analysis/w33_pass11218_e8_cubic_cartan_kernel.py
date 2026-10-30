#!/usr/bin/env python3
"""Pass 11218 corrected: a regular abelian centralizer for the E8 cubic.

The repository's grade-one bracket is

    [e_(i,a), e_(j,b)] = d_ijk epsilon_abc ebar_(k,c)

on 3 tensor 27.  This producer finds one sparse regular background, computes
its exact rational centralizer in the same 81-coordinate gauge, and proves
that centralizer is a three-dimensional abelian subspace.  A nonzero 78 by 78
principal minor is retained as a compact rank witness.

The generic conclusion uses the classical Vinberg theta-group classification:
the order-three E8 grading with fixed algebra E6+A2 has rank three, little Weyl
group G26, and invariant degrees 6, 12, 18.  Pass 11255 subsequently proved
that the displayed centralizer contains a nonzero ad-nilpotent vector, so this
particular kernel does not realize the abstract Cartan subspace.

This G26 is the little Weyl action on a genuine Cartan subspace.  It is not the extended
qutrit Clifford group, whose proposed identification with G26 was already
refuted by ``w33_extended_clifford_g26_no_go.py``.
"""
from __future__ import annotations

import importlib.util
import json
import math
from functools import reduce
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass11218_e8_cubic_cartan_kernel.json"
PARENT = ROOT / "analysis/w33_e6_cubic_jacobian_rank_stratification.py"


def load_parent():
    spec = importlib.util.spec_from_file_location("w33_cubic_rank_parent", PARENT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {PARENT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dense_from_sparse(entries):
    out = [0] * 81
    for e6id, phase, value in entries:
        out[3 * e6id + phase] = int(value)
    return out


BACKGROUND = [
    (0, 2, 2),
    (4, 1, 6),
    (5, 0, 2),
    (5, 1, 5),
    (17, 0, 6),
    (18, 0, 1),
    (20, 0, 1),
    (25, 2, 3),
    (26, 1, 4),
]


def primitive_integer_vector(v):
    den = sp.ilcm(*[x.q for x in v])
    z = [int(x * den) for x in v]
    g = reduce(math.gcd, (abs(x) for x in z if x))
    z = [x // g for x in z]
    if next(x for x in z if x) < 0:
        z = [-x for x in z]
    return z


def sparse_coordinates(v):
    return [
        {"e6id": i // 3, "phase": i % 3, "value": int(x)}
        for i, x in enumerate(v)
        if x
    ]


def bracket(u, v, records):
    # jacobian(u) * v, written directly so all arithmetic remains exact.
    out = [0] * 81
    for left, right, target, coefficient in records:
        out[target] += coefficient * u[left] * v[right]
    return out


def main(write: bool = True):
    parent = load_parent()
    records = parent.build_records()
    assert len(records) == 1620

    v = dense_from_sparse(BACKGROUND)
    A = sp.Matrix(parent.jacobian(v, records))
    nullspace = A.nullspace()
    kernel = [primitive_integer_vector(z) for z in nullspace]
    K = sp.Matrix.hstack(*(sp.Matrix(z) for z in kernel))

    assert len(kernel) == 3
    assert A.rank() == 78
    assert K.rank() == 3
    assert all(A * sp.Matrix(z) == sp.zeros(81, 1) for z in kernel)
    assert all(
        bracket(kernel[i], kernel[j], records) == [0] * 81
        for i in range(3)
        for j in range(i + 1, 3)
    )

    background_coefficients = list(sp.linsolve((K, sp.Matrix(v))))
    assert background_coefficients == [(0, 1, 0)]

    # Three coordinate rows on which the kernel projects isomorphically.
    _, kernel_pivot_rows = K.T.rref()
    kernel_pivot_rows = tuple(int(i) for i in kernel_pivot_rows)
    assert kernel_pivot_rows == (1, 2, 16)
    kernel_coordinate_minor = int(K[list(kernel_pivot_rows), :].det())
    assert kernel_coordinate_minor == -16128

    # The complementary principal restriction is nondegenerate.  Its exact
    # determinant is the square of the Pfaffian and certifies rank >= 78.
    keep = [i for i in range(81) if i not in kernel_pivot_rows]
    principal = A.extract(keep, keep)
    principal_det = int(principal.det(method="domain-ge"))
    expected_det = 2**76 * 3**24 * 5**2 * 7**2
    assert principal_det == expected_det
    pfaffian_abs = math.isqrt(principal_det)
    assert pfaffian_abs**2 == principal_det
    assert pfaffian_abs == 2**38 * 3**12 * 5 * 7

    fi = json.loads((ROOT / "data/w33_physical_fi_e6_a2_z3_grading.json").read_text())
    assert fi["E8"]["fixed_dimension"] == 86
    assert "E6+A2" in fi["E8"].get("fixed_type", fi["E8"].get("fixed_lie_algebra", ""))

    old_no_go = json.loads((ROOT / "data/w33_extended_clifford_g26_no_go.json").read_text())
    assert old_no_go["status"] == "PASS_EXTENDED_QUTRIT_1296_IS_NOT_SHEPHARD_TODD_G26"

    out = {
        "schema": "w33.pass11218.e8-cubic-cartan-kernel.v1",
        "status": "PASS_GENERIC_CUBIC_JACOBIAN_RANK78_WITH_EXPLICIT_ABELIAN_CENTRALIZER_CARTAN_LABEL_RETRACTED",
        "headline": (
            "The recurring 78+3 split is structural.  In the canonical signed 3 tensor 27 bracket, "
            "one sparse nine-coordinate background has exact Jacobian rank 78 and an exact "
            "three-dimensional kernel.  The kernel is pairwise bracket-commuting and contains the "
            "background, so it is an exact abelian centralizer in the repository gauge.  Pass 11255 "
            "proves that it contains a nonzero nilpotent element and therefore is not a Cartan slice.  Vinberg's "
            "classification identifies this E8 order-three E6+A2 grading as rank three with little "
            "Weyl group G26 and invariant degrees 6,12,18.  Thus rank 78 is the generic rank, and "
            "the abstract generic quotient has three algebraically independent invariant coordinates, but "
            "those coordinates have not yet been embedded in this signed tensor gauge."
        ),
        "coordinate_gauge": {
            "dimension": 81,
            "index": "n=3*e6id+external_phase",
            "bracket": "d_ijk epsilon_abc",
            "signed_e6_triads": 45,
            "ordered_bracket_records": len(records),
        },
        "explicit_regular_background": {
            "support_size": len(BACKGROUND),
            "coordinates": sparse_coordinates(v),
            "exact_rank": 78,
            "kernel_dimension": 3,
            "coordinates_in_stored_kernel_basis": [0, 1, 0],
        },
        "abelian_centralizer": {
            "dimension": 3,
            "basis": [sparse_coordinates(z) for z in kernel],
            "basis_pairwise_brackets_zero": True,
            "background_in_kernel": True,
            "centralizer_equals_displayed_kernel": True,
            "is_cartan_subspace": False,
            "correction_certificate": "data/w33_pass11255_restricted_pfaffian_cartan_audit.json",
            "kernel_projection_pivot_coordinates": [
                {"flat_index": i, "e6id": i // 3, "phase": i % 3}
                for i in kernel_pivot_rows
            ],
            "kernel_coordinate_minor": kernel_coordinate_minor,
        },
        "rank_witness": {
            "deleted_flat_indices": list(kernel_pivot_rows),
            "principal_minor_size": 78,
            "determinant": str(principal_det),
            "determinant_factorization": {"2": 76, "3": 24, "5": 2, "7": 2},
            "absolute_pfaffian": str(pfaffian_abs),
            "absolute_pfaffian_factorization": {"2": 38, "3": 12, "5": 1, "7": 1},
        },
        "vinberg_classification": {
            "grading": "inner order-three grading of E8 with g0=E6+A2 and g1=(27,3)",
            "rank": 3,
            "little_weyl_group": "Shephard-Todd G26",
            "invariant_degrees": [6, 12, 18],
            "source": (
                "M. Reeder, P. Levy, J.-K. Yu, B. Gross, Gradings of positive rank on simple "
                "Lie algebras, Table 21, E8 row 3b"
            ),
            "source_url": "https://abel.math.harvard.edu/~gross/preprints/PosRank.pdf",
            "deduction": (
                "The rank-three theta classification supplies the universal corank-at-least-three "
                "bound.  The displayed nonzero 78x78 minor attains it.  Maximal rank is an open "
                "condition, hence rank 78 holds on a nonempty Zariski-open subset of g1."
            ),
        },
        "g26_firewall": {
            "genuine_action": "little Weyl action on an as-yet unembedded three-dimensional Cartan subspace",
            "excluded_action": "the full retained-phase extended qutrit Clifford group",
            "prior_certificate": "data/w33_extended_clifford_g26_no_go.json",
            "compatible_with_prior_no_go": True,
        },
        "prior_corpus_checked": [
            "analysis/PASS1020_E8_TRANSITIVE_51840.md",
            "analysis/w33_eisenstein_forcing.py",
            "analysis/w33_eisenstein_grand_synthesis.py",
            "analysis/w33_pass1047_eisenstein_parabolic_ladder.g",
            "analysis/w33_pass8909_8924_the_centraliser_is_the_clifford_group.py",
            "analysis/w33_BREAKTHROUGH_341_witting_polytope_SQNA.py",
            "analysis/w33_BREAKTHROUGH_343_witting_SQNA_protocol.py",
            "analysis/w33_extended_clifford_g26_no_go.py",
            "analysis/w33_pass1020_e8_transitive_51840.g",
            "analysis/w33_pass1039b_gaussian_base.g",
            "exploration/WITTING_W33_S12_SYNTHESIS.py",
        ],
        "physics_boundary": (
            "The degrees 6,12,18 give three invariant coordinates on the abstract generic algebraic "
            "quotient.  This does not identify them with the displayed kernel, choose a vacuum, define "
            "a positive stable physical potential, or derive masses or mixing angles.  Those tasks "
            "require an explicit semisimple Cartan embedding and a kinetic metric."
        ),
        "pass11255_correction": {
            "retained": "exact rank 78, kernel dimension three, commuting centralizer, and rank witness",
            "withdrawn": "the displayed kernel is a Cartan subspace carrying the G26 quotient coordinates",
            "reason": "the first stored kernel vector has ad-nilpotency index five",
        },
        "checks": {
            "canonical_signed_tensor_loaded": True,
            "sparse_background_support9": True,
            "exact_rank78": True,
            "exact_kernel_dimension3": True,
            "kernel_is_abelian": True,
            "background_is_kernel_basis_vector": True,
            "nonzero_78_principal_minor": True,
            "principal_determinant_is_pfaffian_square": True,
            "local_e6_a2_grading_certificate_loaded": True,
            "prior_g26_clifford_no_go_preserved": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
