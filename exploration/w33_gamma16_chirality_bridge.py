"""Exact dominant-shell block law and Z2 grading on the common 16-core.

This bridge sharpens the current W(3,3) packet picture in three ways.

1. The native operators A0, A1, A2, D, D_H preserve the exact split

       40 = 32 + 8
          = (10 + 16 + 6) + (1 + 4 + 3).

   So the dominant shell and the Higgs/EW octet are genuinely separate
   operator blocks, not just compatible dimensions.

2. Inside the dominant shell, the exact 16-dimensional core is common to the
   cube-root Dirac operator D and the Hermitian Dirac operator D_H.

3. On that common 16-core there is a canonical Z2 grading Gamma, built from the
   exact 10/6 intersections with the A1-dominant matter/gauge shells. The
   native operators collapse to affine or phase functions of Gamma:

       A0|16                     = -I + 3 Gamma
       (A1 + A2)|16             = -3 Gamma
       i(A1 - A2)/sqrt(3)|16    = -3 Gamma
       A1|16                    = 3 omega Gamma
       A2|16                    = 3 omega^2 Gamma

   Hence D|16 = D_H|16 = -I exactly.

The tempting E6-like count packet 27 = 1 + 10 + 16 is therefore *not* the live
native block of the operator algebra. The honest exact native block is 32 = 10
+ 16 + 6, with the only visible index-2 structure sitting on the common 16-core.
"""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_gamma16_chirality_bridge_summary.json"


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


def _principal_report(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(left.T.conj() @ right, compute_uv=False)
    return {
        "intersection_dimension": int(np.sum(singular_values > 1 - 1e-8)),
        "principal_singular_values": [float(value) for value in singular_values],
    }


def _off_block_norm(left: np.ndarray, operator: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left.T.conj() @ operator @ right))


def build_summary() -> dict[str, Any]:
    a0, a1, a2 = _matrices()
    n = a0.shape[0]
    identity = np.eye(n, dtype=complex)
    all_ones = np.ones((n, n), dtype=complex)
    p1 = all_ones / n
    p24 = (a0 + 4.0 * identity) / 6.0 - all_ones / 15.0
    p15 = identity - p1 - p24

    u24 = _basis_from_projector(p24)
    u15 = _basis_from_projector(p15)

    b24 = u24.T.conj() @ a1 @ u24
    b15 = u15.T.conj() @ a1 @ u15
    clusters24 = _cluster_indices(b24)
    clusters15 = _cluster_indices(b15)

    matter_singlet_indices = [indices[0] for indices in clusters24.values() if len(indices) == 1]
    gauge_singlet_indices = [indices[0] for indices in clusters15.values() if len(indices) == 1]
    matter_dominant_indices = [index for indices in clusters24.values() if len(indices) > 1 for index in indices]
    gauge_dominant_indices = [index for indices in clusters15.values() if len(indices) > 1 for index in indices]

    _, eigvecs24 = np.linalg.eig(b24)
    _, eigvecs15 = np.linalg.eig(b15)
    v4 = _qr_columns(u24 @ eigvecs24[:, matter_singlet_indices])
    v3 = _qr_columns(u15 @ eigvecs15[:, gauge_singlet_indices])
    v24_dom = _qr_columns(u24 @ eigvecs24[:, matter_dominant_indices])
    v15_dom = _qr_columns(u15 @ eigvecs15[:, gauge_dominant_indices])

    omega = np.exp(2j * np.pi / 3.0)
    d = a0 + omega * a1 + omega**2 * a2
    d_h = a0 + 1j * (a1 - a2) / np.sqrt(3.0)

    eigvals_d, eigvecs_d = np.linalg.eigh(d)
    eigvals_dh, eigvecs_dh = np.linalg.eigh(d_h)

    v10 = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, 5.0, atol=1e-8)])
    v16 = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, -1.0, atol=1e-8)])
    v6 = _qr_columns(eigvecs_dh[:, np.isclose(eigvals_dh, -7.0, atol=1e-8)])

    v16_d = _qr_columns(eigvecs_d[:, np.isclose(eigvals_d, -1.0, atol=1e-8)])
    v10_d = _qr_columns(eigvecs_d[:, np.isclose(eigvals_d, 8.0, atol=1e-8)])
    v6_d = _qr_columns(eigvecs_d[:, np.isclose(eigvals_d, -10.0, atol=1e-8)])

    q8 = _qr_columns(
        eigvecs_dh[
            :,
            ~(
                np.isclose(eigvals_dh, 5.0, atol=1e-8)
                | np.isclose(eigvals_dh, -1.0, atol=1e-8)
                | np.isclose(eigvals_dh, -7.0, atol=1e-8)
            ),
        ]
    )
    q7 = _qr_columns(np.column_stack([v4, v3]))
    residual = (identity - q7 @ q7.T.conj()) @ q8
    residual_u, _, _ = np.linalg.svd(residual, full_matrices=False)
    v1 = _qr_columns(residual_u[:, :1])

    v32 = _qr_columns(np.column_stack([v10, v16, v6]))
    v8 = _qr_columns(np.column_stack([v1, v4, v3]))

    # Exact 10/6 inside the common 16-core.
    u10, _, _ = np.linalg.svd(v16.T.conj() @ v24_dom, full_matrices=False)
    core10 = _qr_columns(v16 @ u10[:, :10])
    u6, _, _ = np.linalg.svd(v16.T.conj() @ v15_dom, full_matrices=False)
    core6 = _qr_columns(v16 @ u6[:, :6])
    gamma = core10 @ core10.T.conj() - core6 @ core6.T.conj()

    gamma16 = v16.T.conj() @ gamma @ v16
    gamma_involution_error = float(np.linalg.norm(gamma16 @ gamma16 - np.eye(16)))

    # Tempting but false E6-like count packet.
    candidate27 = _qr_columns(np.column_stack([v1, v10, v16]))
    candidate13 = _qr_columns(np.column_stack([v6, v4, v3]))

    def operator_block_report(operator: np.ndarray) -> dict[str, float]:
        return {
            "32_to_8": _off_block_norm(v32, operator, v8),
            "8_to_32": _off_block_norm(v8, operator, v32),
            "10_to_16": _off_block_norm(v10, operator, v16),
            "10_to_6": _off_block_norm(v10, operator, v6),
            "16_to_6": _off_block_norm(v16, operator, v6),
        }

    return {
        "exact_packets": {
            "dominant_shell": {"10": 10, "16": 16, "6": 6, "total": 32},
            "bosonic_octet": {"1": 1, "4": 4, "3": 3, "total": 8},
            "full_split": "40 = (10 + 16 + 6) + (1 + 4 + 3)",
        },
        "shared_dirac_core": {
            "D_minus_1_vs_DH_minus_1": _principal_report(v16_d, v16),
            "D_8_vs_DH_5": _principal_report(v10_d, v10),
            "D_minus_10_vs_DH_minus_7": _principal_report(v6_d, v6),
        },
        "native_block_reports": {
            "A0": operator_block_report(a0),
            "A1": operator_block_report(a1),
            "A2": operator_block_report(a2),
            "D": operator_block_report(d),
            "DH": operator_block_report(d_h),
        },
        "gamma16_packet": {
            "trace": float(np.trace(gamma16).real),
            "eigenvalues": [float(np.real_if_close(value)) for value in np.linalg.eigvals(gamma16)],
            "involution_error": gamma_involution_error,
            "A0_affine_gamma_error": float(
                np.linalg.norm(v16.T.conj() @ a0 @ v16 - (v16.T.conj() @ (-identity + 3.0 * gamma) @ v16))
            ),
            "A1_plus_A2_gamma_error": float(
                np.linalg.norm(v16.T.conj() @ (a1 + a2) @ v16 - (v16.T.conj() @ (-3.0 * gamma) @ v16))
            ),
            "iA1_minus_A2_over_sqrt3_gamma_error": float(
                np.linalg.norm(
                    v16.T.conj() @ (1j * (a1 - a2) / np.sqrt(3.0)) @ v16
                    - (v16.T.conj() @ (-3.0 * gamma) @ v16)
                )
            ),
            "A1_phase_gamma_error": float(
                np.linalg.norm(v16.T.conj() @ a1 @ v16 - (3.0 * omega * gamma16))
            ),
            "A2_phase_gamma_error": float(
                np.linalg.norm(v16.T.conj() @ a2 @ v16 - (3.0 * omega**2 * gamma16))
            ),
            "D_minus_identity_error": float(np.linalg.norm(v16.T.conj() @ d @ v16 + np.eye(16))),
            "DH_minus_identity_error": float(np.linalg.norm(v16.T.conj() @ d_h @ v16 + np.eye(16))),
            "core10_dimension": 10,
            "core6_dimension": 6,
        },
        "false_but_tempting_packet": {
            "candidate_split": "27 = 1 + 10 + 16 versus 13 = 6 + 4 + 3",
            "A0_off_block": _off_block_norm(candidate27, a0, candidate13),
            "A1_off_block": _off_block_norm(candidate27, a1, candidate13),
            "A2_off_block": _off_block_norm(candidate27, a2, candidate13),
            "D_off_block": _off_block_norm(candidate27, d, candidate13),
            "DH_off_block": _off_block_norm(candidate27, d_h, candidate13),
        },
        "gamma16_chirality_theorem": {
            "the_native_operator_stack_preserves_the_exact_32_plus_8_split": bool(
                all(
                    report["32_to_8"] < 1e-10 and report["8_to_32"] < 1e-10
                    for report in {
                        "A0": operator_block_report(a0),
                        "A1": operator_block_report(a1),
                        "A2": operator_block_report(a2),
                        "D": operator_block_report(d),
                        "DH": operator_block_report(d_h),
                    }.values()
                )
            ),
            "the_dominant_shell_refines_exactly_as_invariant_10_plus_16_plus_6": bool(
                all(
                    report["10_to_16"] < 1e-10
                    and report["10_to_6"] < 1e-10
                    and report["16_to_6"] < 1e-10
                    for report in {
                        "A0": operator_block_report(a0),
                        "A1": operator_block_report(a1),
                        "A2": operator_block_report(a2),
                        "D": operator_block_report(d),
                        "DH": operator_block_report(d_h),
                    }.values()
                )
            ),
            "the_exact_16_core_is_common_to_the_two_live_dirac_operators": bool(
                _principal_report(v16_d, v16)["intersection_dimension"] == 16
            ),
            "the_common_16_carries_a_canonical_Z2_grading": bool(
                gamma_involution_error < 1e-10
            ),
            "the_native_operators_on_the_16_core_are_exact_functions_of_that_grading": bool(
                float(np.linalg.norm(v16.T.conj() @ a0 @ v16 - (v16.T.conj() @ (-identity + 3.0 * gamma) @ v16))) < 1e-10
                and float(np.linalg.norm(v16.T.conj() @ (a1 + a2) @ v16 - (v16.T.conj() @ (-3.0 * gamma) @ v16))) < 1e-10
                and float(
                    np.linalg.norm(
                        v16.T.conj() @ (1j * (a1 - a2) / np.sqrt(3.0)) @ v16
                        - (v16.T.conj() @ (-3.0 * gamma) @ v16)
                    )
                ) < 1e-10
                and float(np.linalg.norm(v16.T.conj() @ a1 @ v16 - (3.0 * omega * gamma16))) < 1e-10
                and float(np.linalg.norm(v16.T.conj() @ a2 @ v16 - (3.0 * omega**2 * gamma16))) < 1e-10
            ),
            "the_count_packet_27_equals_1_plus_10_plus_16_is_not_a_native_invariant_split": bool(
                _off_block_norm(candidate27, a1, candidate13) > 1e-6
                and _off_block_norm(candidate27, d_h, candidate13) > 1e-6
            ),
        },
        "interpretation": (
            "The live exact operator geometry is 32 plus 8, not a naive 27 plus 13. "
            "The dominant shell is an invariant 10 plus 16 plus 6 block for A0, A1, A2, D, and D_H. "
            "Inside it, the shared 16-dimensional D and D_H core carries the only exact native Z2 grading "
            "seen so far: Gamma with eigenvalue multiplicities 10 and 6 and trace 4 = mu. On that core the "
            "native operators collapse to phase or affine functions of Gamma, so the index-2 chirality hint "
            "from the paper is not empty rhetoric anymore. But the honest exact block is the common 16 inside "
            "the dominant 32, not the tempting E6-like count packet 1 + 10 + 16."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["gamma16_chirality_theorem"], indent=2))


if __name__ == "__main__":
    main()
