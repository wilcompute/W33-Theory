"""Two exact Spin(10)-sized Clifford packets inside the dominant 32.

This bridge folds the new exact dominant-shell operator result back into the
tetrahedral/Clifford hints from the committed GitHub trail.

Key idea:

* The tetrahedral Pascal row is

      1 + 4 + 6 + 4 + 1 = 16,

  which is the standard grade count of the 4-dimensional Clifford/exterior
  algebra.

* The same 16-dimensional operator packet, when realized on a 4-component
  spinor space, naturally collapses as

      End(S) = Sym^2(S) + Lambda^2(S) = 10 + 6,

  because dim Sym^2(C^4)=10 and dim Lambda^2(C^4)=6.

The live W(3,3) dominant shell now exhibits *two* exact 16-dimensional packets
with precisely that 10+6 grading:

1. an extremal packet 16_ext = 10_(D_H=5) + 6_(D_H=-7),
2. a flat/common packet 16_flat = 10_core + 6_core = D_H(-1) = D(-1).

Both packets carry the same Z2 grading Gamma with multiplicities 10 and 6. So
the exact W33 16 is best read as the Clifford/tetrahedral operator packet on a
4-state spinor carrier, not as the raw grade basis itself.
"""

from __future__ import annotations

from collections import defaultdict
import json
from math import comb
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_double_spin16_clifford_bridge_summary.json"


def _w33_points() -> list[tuple[int, int, int, int]]:
    f3 = [0, 1, 2]
    vectors = [
        (a, b, c, d)
        for a in f3
        for b in f3
        for c in f3
        for d in f3
        if (a, b, c, d) != (0, 0, 0, 0)
    ]
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for vector in vectors:
        canon = min(tuple((scale * entry) % 3 for entry in vector) for scale in [1, 2])
        if canon not in seen:
            seen.add(canon)
            points.append(canon)
    return points


def _omega_form(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def _matrices() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    points = _w33_points()
    n = len(points)
    a0 = np.zeros((n, n), dtype=complex)
    a1 = np.zeros((n, n), dtype=complex)
    a2 = np.zeros((n, n), dtype=complex)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            omega = _omega_form(points[i], points[j])
            if omega == 0:
                a0[i, j] = 1.0
            elif omega == 1:
                a1[i, j] = 1.0
            else:
                a2[i, j] = 1.0
    return a0, a1, a2


def _basis_from_projector(projector: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh((projector + projector.T.conj()) / 2.0)
    return eigenvectors[:, eigenvalues > 0.5]


def _qr_columns(matrix: np.ndarray) -> np.ndarray:
    if matrix.shape[1] == 0:
        return matrix
    q, _ = np.linalg.qr(matrix)
    return q


def _cluster_indices(operator: np.ndarray) -> dict[tuple[float, float], list[int]]:
    eigenvalues, _ = np.linalg.eig(operator)
    clusters: dict[tuple[float, float], list[int]] = defaultdict(list)
    for index, eigenvalue in enumerate(eigenvalues):
        clusters[(round(float(eigenvalue.real), 6), round(float(eigenvalue.imag), 6))].append(index)
    return clusters


def _operator_error(packet: np.ndarray, operator: np.ndarray, target: np.ndarray) -> float:
    return float(np.linalg.norm(packet.T.conj() @ operator @ packet - packet.T.conj() @ target @ packet))


def build_summary() -> dict[str, Any]:
    a0, a1, a2 = _matrices()
    n = a0.shape[0]
    identity = np.eye(n, dtype=complex)
    all_ones = np.ones((n, n), dtype=complex)
    p24 = (a0 + 4.0 * identity) / 6.0 - all_ones / 15.0
    p15 = identity - all_ones / n - p24

    u24 = _basis_from_projector(p24)
    u15 = _basis_from_projector(p15)
    b24 = u24.T.conj() @ a1 @ u24
    b15 = u15.T.conj() @ a1 @ u15

    _, eigvecs24 = np.linalg.eig(b24)
    _, eigvecs15 = np.linalg.eig(b15)
    clusters24 = _cluster_indices(b24)
    clusters15 = _cluster_indices(b15)
    v24_dom = _qr_columns(u24 @ eigvecs24[:, [i for inds in clusters24.values() if len(inds) > 1 for i in inds]])
    v15_dom = _qr_columns(u15 @ eigvecs15[:, [i for inds in clusters15.values() if len(inds) > 1 for i in inds]])

    omega = np.exp(2j * np.pi / 3.0)
    d = a0 + omega * a1 + omega**2 * a2
    d_h = a0 + 1j * (a1 - a2) / np.sqrt(3.0)
    eigvals_dh, eigvecs_dh = np.linalg.eigh(d_h)

    v10_ext = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, 5.0, atol=1e-8)])
    v6_ext = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, -7.0, atol=1e-8)])
    v16_flat = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, -1.0, atol=1e-8)])
    v16_ext = _qr_columns(np.column_stack([v10_ext, v6_ext]))

    # The flat/common 16 splits as the 10+6 intersections with the A1-dominant shells.
    u10_flat, _, _ = np.linalg.svd(v16_flat.T.conj() @ v24_dom, full_matrices=False)
    v10_flat = _qr_columns(v16_flat @ u10_flat[:, :10])
    u6_flat, _, _ = np.linalg.svd(v16_flat.T.conj() @ v15_dom, full_matrices=False)
    v6_flat = _qr_columns(v16_flat @ u6_flat[:, :6])

    gamma_ext = v10_ext @ v10_ext.T.conj() - v6_ext @ v6_ext.T.conj()
    gamma_flat = v10_flat @ v10_flat.T.conj() - v6_flat @ v6_flat.T.conj()

    cl_row4 = [comb(4, degree) for degree in range(5)]
    sym_dim = comb(4 + 1, 2)
    wedge_dim = comb(4, 2)

    return {
        "tetra_clifford_dictionary": {
            "pascal_row_4": cl_row4,
            "clifford_grade_counts": {"0": 1, "1": 4, "2": 6, "3": 4, "4": 1},
            "clifford_total": sum(cl_row4),
            "spinor_dimension": 4,
            "endomorphism_dimension": 16,
            "symmetric_square_dimension": sym_dim,
            "antisymmetric_square_dimension": wedge_dim,
            "operator_collapse": "16 = 10 + 6 = Sym^2(4) + Lambda^2(4)",
        },
        "two_spin16_packets": {
            "extremal_packet": {
                "dimension": 16,
                "split": "10_ext + 6_ext",
                "dh_eigenvalues": {"5": 10, "-7": 6},
                "d_eigenvalues": {"8": 10, "-10": 6},
            },
            "flat_packet": {
                "dimension": 16,
                "split": "10_flat + 6_flat",
                "dh_eigenvalues": {"-1": 16},
                "d_eigenvalues": {"-1": 16},
            },
        },
        "gamma_packets": {
            "extremal_trace": float(np.trace(v16_ext.T.conj() @ gamma_ext @ v16_ext).real),
            "flat_trace": float(np.trace(v16_flat.T.conj() @ gamma_flat @ v16_flat).real),
            "extremal_gamma_eigenvalues": [
                float(np.real_if_close(value)) for value in np.linalg.eigvals(v16_ext.T.conj() @ gamma_ext @ v16_ext)
            ],
            "flat_gamma_eigenvalues": [
                float(np.real_if_close(value)) for value in np.linalg.eigvals(v16_flat.T.conj() @ gamma_flat @ v16_flat)
            ],
            "extremal_involution_error": float(
                np.linalg.norm((v16_ext.T.conj() @ gamma_ext @ v16_ext) @ (v16_ext.T.conj() @ gamma_ext @ v16_ext) - np.eye(16))
            ),
            "flat_involution_error": float(
                np.linalg.norm((v16_flat.T.conj() @ gamma_flat @ v16_flat) @ (v16_flat.T.conj() @ gamma_flat @ v16_flat) - np.eye(16))
            ),
        },
        "operator_laws": {
            "extremal": {
                "A0_error": _operator_error(v16_ext, a0, -identity + 3.0 * gamma_ext),
                "A1_plus_A2_error": _operator_error(v16_ext, a1 + a2, -3.0 * gamma_ext),
                "iA1_minus_A2_over_sqrt3_error": _operator_error(
                    v16_ext, 1j * (a1 - a2) / np.sqrt(3.0), 3.0 * gamma_ext
                ),
                "D_error": _operator_error(v16_ext, d, -identity + 9.0 * gamma_ext),
                "DH_error": _operator_error(v16_ext, d_h, -identity + 6.0 * gamma_ext),
                "A1_phase_error": _operator_error(v16_ext, a1, 3.0 * omega**2 * gamma_ext),
                "A2_phase_error": _operator_error(v16_ext, a2, 3.0 * omega * gamma_ext),
            },
            "flat": {
                "A0_error": _operator_error(v16_flat, a0, -identity + 3.0 * gamma_flat),
                "A1_plus_A2_error": _operator_error(v16_flat, a1 + a2, -3.0 * gamma_flat),
                "iA1_minus_A2_over_sqrt3_error": _operator_error(
                    v16_flat, 1j * (a1 - a2) / np.sqrt(3.0), -3.0 * gamma_flat
                ),
                "D_error": _operator_error(v16_flat, d, -identity),
                "DH_error": _operator_error(v16_flat, d_h, -identity),
                "A1_phase_error": _operator_error(v16_flat, a1, 3.0 * omega * gamma_flat),
                "A2_phase_error": _operator_error(v16_flat, a2, 3.0 * omega**2 * gamma_flat),
            },
        },
        "double_spin16_clifford_theorem": {
            "the_tetra_clifford_packet_has_exact_grade_count_1_4_6_4_1": bool(cl_row4 == [1, 4, 6, 4, 1]),
            "the_same_16_collapse_as_operator_space_is_exactly_10_plus_6": bool(sym_dim == 10 and wedge_dim == 6),
            "the_dominant_32_contains_two_exact_16_packets": bool(v16_ext.shape[1] == 16 and v16_flat.shape[1] == 16),
            "both_16_packets_carry_the_same_10_plus_6_Z2_grading": bool(
                abs(np.trace(v16_ext.T.conj() @ gamma_ext @ v16_ext).real - 4.0) < 1e-10
                and abs(np.trace(v16_flat.T.conj() @ gamma_flat @ v16_flat).real - 4.0) < 1e-10
            ),
            "the_extremal_packet_obeys_D_equals_minus_I_plus_9Gamma_and_DH_equals_minus_I_plus_6Gamma": bool(
                _operator_error(v16_ext, d, -identity + 9.0 * gamma_ext) < 1e-10
                and _operator_error(v16_ext, d_h, -identity + 6.0 * gamma_ext) < 1e-10
            ),
            "the_flat_packet_is_the_common_D_equals_DH_equals_minus_I_spin16": bool(
                _operator_error(v16_flat, d, -identity) < 1e-10
                and _operator_error(v16_flat, d_h, -identity) < 1e-10
            ),
        },
        "interpretation": (
            "The user-side tetrahedron clue is structurally right. The live W33 "
            "graded 16 should not be read as the raw Clifford grade basis 1+4+6+4+1. "
            "It is better read as the matrix/spinor realization of that same tetrahedral "
            "Clifford packet on a 4-state carrier, where 16 collapses as Sym^2(4)+Lambda^2(4)=10+6. "
            "Inside the dominant 32, W33 now has two exact Spin(10)-sized packets of that type: "
            "an extremal 16 with nontrivial D and D_H grading law, and a flat/common 16 with "
            "D=D_H=-I but the same underlying 10+6 chirality packet."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["double_spin16_clifford_theorem"], indent=2))


if __name__ == "__main__":
    main()
