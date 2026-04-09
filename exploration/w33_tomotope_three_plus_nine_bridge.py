"""The faithful tomotope 12-point model splits as 3 ⊕ 9.

Starting from the faithful degree-12 tomotope action on the mode-major packet

    12 = 3 blocks of 4 chart states,

apply the same 4-point chart-Fourier transform on each block that produced the
atlas singlet-plus-triplet split.  This yields

    4 = 1 ⊕ 3

on each mode block, hence

    12 = 3 ⊗ (1 ⊕ 3) = 3 ⊕ 9.

This bridge verifies that the faithful tomotope generators preserve that split
exactly:

    - the 3D sector is the blockwise chart-average sector;
    - the quotient S3 acts faithfully on that 3D sector;
    - the complementary 9D sector is invariant.

So the tomotope packet itself already separates into a triality carrier of
dimension 3 and a colored nonet of dimension 9.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_tomotope_mode_chart_action_bridge import user_tomotope_generators


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tomotope_three_plus_nine_bridge_summary.json"


def _chart_fourier_matrix() -> np.ndarray:
    columns = np.array(
        [
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0, 1.0],
        ],
        dtype=float,
    ).T / 2.0
    return columns


def _permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    size = len(permutation)
    matrix = np.zeros((size, size), dtype=float)
    for column, row in enumerate(permutation):
        matrix[row, column] = 1.0
    return matrix


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[index] for index in right)


def _generate_group(generators: dict[str, tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(12))
    group = {identity}
    queue = [identity]
    while queue:
        element = queue.pop()
        for generator in generators.values():
            image = _compose(element, generator)
            if image not in group:
                group.add(image)
                queue.append(image)
    return group


def build_summary() -> dict[str, Any]:
    generators = user_tomotope_generators()
    block_fourier = _chart_fourier_matrix()
    change_of_basis = np.kron(np.eye(3, dtype=float), block_fourier)
    transformed_generators: dict[str, np.ndarray] = {}

    singlet_indices = [0, 4, 8]
    nonet_indices = [index for index in range(12) if index not in singlet_indices]
    reorder = singlet_indices + nonet_indices

    singlet_actions: dict[str, list[list[float]]] = {}
    nonet_residuals: dict[str, float] = {}
    cross_residuals: dict[str, float] = {}
    for name, permutation in generators.items():
        matrix = _permutation_matrix(permutation)
        transformed = change_of_basis.T @ matrix @ change_of_basis
        transformed_generators[name] = transformed

        singlet_block = transformed[np.ix_(singlet_indices, singlet_indices)]
        cross_upper = transformed[np.ix_(singlet_indices, nonet_indices)]
        cross_lower = transformed[np.ix_(nonet_indices, singlet_indices)]
        nonet_block = transformed[np.ix_(nonet_indices, nonet_indices)]
        reordered = transformed[np.ix_(reorder, reorder)]

        singlet_actions[name] = singlet_block.tolist()
        nonet_residuals[name] = float(
            np.linalg.norm(
                reordered
                - np.block(
                    [
                        [singlet_block, np.zeros((3, 9))],
                        [np.zeros((9, 3)), nonet_block],
                    ]
                )
            )
        )
        cross_residuals[name] = float(np.linalg.norm(cross_upper) + np.linalg.norm(cross_lower))

    quotient_group = {
        tuple(
            (
                change_of_basis.T
                @ _permutation_matrix(permutation)
                @ change_of_basis
            )[np.ix_(singlet_indices, singlet_indices)].reshape(-1)
        )
        for permutation in _generate_group(generators)
    }

    summary: dict[str, Any] = {
        "change_of_basis": {
            "block_fourier_matrix": _chart_fourier_matrix().tolist(),
            "singlet_indices": singlet_indices,
            "nonet_indices": nonet_indices,
        },
        "singlet_sector_actions": singlet_actions,
        "invariance_checks": {
            "cross_residuals": cross_residuals,
            "block_residuals": nonet_residuals,
        },
        "tomotope_three_plus_nine_theorem": {
            "the_chart_fourier_transform_splits_each_4_block_as_1_plus_3": np.allclose(
                block_fourier.T @ block_fourier,
                np.eye(4),
            ),
            "every_generator_preserves_the_global_three_dimensional_singlet_sector": all(
                residual < 1e-12 for residual in cross_residuals.values()
            ),
            "every_generator_preserves_the_complementary_nine_dimensional_sector": all(
                residual < 1e-12 for residual in nonet_residuals.values()
            ),
            "the_induced_action_on_the_three_singlet_modes_is_the_triality_s3_quotient": len(
                quotient_group
            )
            == 6,
        },
        "interpretation": (
            "After blockwise chart Fourier transform, the faithful tomotope packet "
            "splits exactly as 3 ⊕ 9. The 3D summand is the chart-average triality "
            "sector, and the 9D complement is the invariant colored nonet."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["tomotope_three_plus_nine_theorem"], indent=2))


if __name__ == "__main__":
    main()
