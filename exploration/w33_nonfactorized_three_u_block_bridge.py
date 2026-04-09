"""Exact block form for non-factorized qutrit family couplings.

This module identifies the first exact coupling class that can evade the
factorized-family no-go theorem.

Let Q_0, Q_1, Q_2 be the complete orthogonal rank-one qutrit projectors already
isolated in earlier bridges. For arbitrary external operators B_0, B_1, B_2,
consider the non-factorized family packet

    M = Q_0 ⊗ B_0 + Q_1 ⊗ B_1 + Q_2 ⊗ B_2.

Because the Q_i form a complete orthogonal resolution of identity, M is
unitarily equivalent to the block direct sum

    B_0 ⊕ B_1 ⊕ B_2.

So the full hierarchy problem reduces exactly to the three external block
spectra. This is the first exact escape from the factorized no-go, and it is
the natural abstract model for coupling the family qutrit packet to the K3
``3U`` hyperbolic triplet.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_nonfactorized_three_u_block_bridge_summary.json"
FLOAT_TOL = 1e-10


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _complex_matrix(serialized: list[list[list[float]]]) -> np.ndarray:
    return np.array(
        [[complex(entry[0], entry[1]) for entry in row] for row in serialized],
        dtype=complex,
    )


def _spectral_packet(matrix: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    eigenvalues = np.linalg.eigvals(matrix)
    return {
        "shape": list(matrix.shape),
        "rank": int(np.linalg.matrix_rank(matrix)),
        "singular_values": [float(value) for value in singular_values],
        "eigenvalues": [[float(value.real), float(value.imag)] for value in eigenvalues],
    }


def _projector_eigenbasis(projectors: list[np.ndarray]) -> np.ndarray:
    columns = []
    for projector in projectors:
        column = None
        for index in range(projector.shape[1]):
            candidate = projector[:, index]
            if np.linalg.norm(candidate) > FLOAT_TOL:
                column = candidate
                break
        if column is None:
            raise ValueError("rank-one projector had no nonzero column")
        column = column / np.linalg.norm(column)
        for entry in column:
            if abs(entry) > FLOAT_TOL:
                column = column * np.exp(-1j * np.angle(entry))
                break
        columns.append(column)
    basis = np.column_stack(columns)
    if not np.allclose(np.conjugate(basis).T @ basis, np.eye(len(projectors)), atol=FLOAT_TOL):
        raise ValueError("projector basis failed to be unitary")
    return basis


def _nonfactorized_operator(projectors: list[np.ndarray], blocks: list[np.ndarray]) -> np.ndarray:
    total = np.zeros(
        (
            3 * blocks[0].shape[0],
            3 * blocks[0].shape[1],
        ),
        dtype=complex,
    )
    for projector, block in zip(projectors, blocks):
        total += np.kron(projector, block)
    return total


def _block_direct_sum(blocks: list[np.ndarray]) -> np.ndarray:
    rows = []
    zero_blocks = [
        np.zeros_like(blocks[0], dtype=complex)
        for _ in blocks
    ]
    for i, block in enumerate(blocks):
        row = []
        for j in range(len(blocks)):
            row.append(block if i == j else zero_blocks[j])
        rows.append(row)
    return np.block(rows)


def _serialized_complex_matrix(matrix: np.ndarray) -> list[list[list[float]]]:
    return [
        [[float(value.real), float(value.imag)] for value in row]
        for row in matrix
    ]


@lru_cache(maxsize=1)
def build_nonfactorized_three_u_block_summary() -> dict[str, Any]:
    rank_one = _read_json("w33_a4_rank_one_qutrit_bridge_summary.json")
    projectors = [
        _complex_matrix(packet["matrix"])
        for packet in rank_one["qutrit_projector_orbit"]["projectors"]
    ]
    basis = _projector_eigenbasis(projectors)

    hyperbolic = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sample_block_families = {
        "democratic_three_u": [hyperbolic, hyperbolic, hyperbolic],
        "weighted_three_u": [hyperbolic, 2.0 * hyperbolic, 4.0 * hyperbolic],
        "mixed_three_u": [
            hyperbolic,
            np.array([[1.0, 0.0], [0.0, 3.0]], dtype=complex),
            np.array([[0.0, 1.0], [5.0, 0.0]], dtype=complex),
        ],
    }

    family_reports: dict[str, Any] = {}
    for name, blocks in sample_block_families.items():
        operator = _nonfactorized_operator(projectors, blocks)
        direct_sum = _block_direct_sum(blocks)
        conjugated = np.kron(np.conjugate(basis).T, np.eye(blocks[0].shape[0], dtype=complex)) @ operator @ np.kron(
            basis,
            np.eye(blocks[0].shape[0], dtype=complex),
        )
        operator_packet = _spectral_packet(operator)
        direct_sum_packet = _spectral_packet(direct_sum)
        family_reports[name] = {
            "blocks": [_serialized_complex_matrix(block) for block in blocks],
            "operator_packet": operator_packet,
            "direct_sum_packet": direct_sum_packet,
            "fourier_block_diagonalization_is_exact": bool(
                np.allclose(conjugated, direct_sum, atol=FLOAT_TOL)
            ),
            "operator_and_block_sum_are_isospectral": bool(
                np.allclose(
                    np.array(operator_packet["singular_values"]),
                    np.array(direct_sum_packet["singular_values"]),
                    atol=FLOAT_TOL,
                )
            ),
        }

    return {
        "status": "ok",
        "sample_nonfactorized_packets": family_reports,
        "nonfactorized_three_u_block_theorem": {
            "every_tested_packet_fourier_block_diagonalizes_exactly": all(
                report["fourier_block_diagonalization_is_exact"]
                for report in family_reports.values()
            ),
            "every_tested_packet_is_isospectral_to_external_block_direct_sum": all(
                report["operator_and_block_sum_are_isospectral"]
                for report in family_reports.values()
            ),
            "democratic_three_u_packet_has_no_internal_hierarchy": (
                len(
                    set(
                        round(value, 8)
                        for value in family_reports["democratic_three_u"]["operator_packet"]["singular_values"]
                        if value > FLOAT_TOL
                    )
                )
                == 1
            ),
            "weighted_three_u_packet_has_genuine_hierarchy": (
                len(
                    set(
                        round(value, 8)
                        for value in family_reports["weighted_three_u"]["operator_packet"]["singular_values"]
                        if value > FLOAT_TOL
                    )
                )
                == 3
            ),
            "mixed_three_u_packet_has_genuine_hierarchy": (
                len(
                    set(
                        round(value, 8)
                        for value in family_reports["mixed_three_u"]["operator_packet"]["singular_values"]
                        if value > FLOAT_TOL
                    )
                )
                >= 3
            ),
            "first_exact_escape_from_factorized_no_go_is_external_block_split": (
                all(report["fourier_block_diagonalization_is_exact"] for report in family_reports.values())
                and all(report["operator_and_block_sum_are_isospectral"] for report in family_reports.values())
                and len(
                    set(
                        round(value, 8)
                        for value in family_reports["weighted_three_u"]["operator_packet"]["singular_values"]
                        if value > FLOAT_TOL
                    )
                )
                == 3
            ),
        },
        "interpretive_read": (
            "Inference from the exact projector algebra: once the full qutrit "
            "orbit is kept, family hierarchy is equivalent to splitting the "
            "three external blocks. The family packet itself no longer needs "
            "extra complexity; it only needs three distinct external partners."
        ),
        "bridge_verdict": (
            "The first exact hierarchy-generating bridge class is now clear. "
            "For a non-factorized packet Q_0⊗B_0 + Q_1⊗B_1 + Q_2⊗B_2, the "
            "qutrit Fourier transform block-diagonalizes the operator to "
            "B_0 ⊕ B_1 ⊕ B_2. So the family spectrum is exactly the union of the "
            "three external block spectra. This is the natural abstract model "
            "for coupling the family qutrit packet to the explicit K3 3U "
            "hyperbolic triplet. The hierarchy problem has therefore reduced "
            "to an external block-splitting problem, not an internal family "
            "combinatorics problem."
        ),
        "source_files": [
            "data/w33_a4_rank_one_qutrit_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_nonfactorized_three_u_block_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
