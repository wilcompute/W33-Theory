"""Tetrahedral chart oscillator and transition algebra on the diffuse atlas.

The previous atlas bridge proved that:

    - one diffuse Yukawa chart carries only a 7-dimensional parabolic
      color-support algebra;
    - a tetrahedral packet of four signed charts restores full ``M_3(C)``.

This module sharpens that result into an operator-level closure.  The same
tetrahedral chart packet already carries:

    - the exact ``K4`` Laplacian ``4I - J`` on chart space;
    - a tight frame identifying its 3-dimensional nontrivial shell with the
      local color mode space;
    - exact directed transition operators between distinct Yukawa charts.

So the atlas is not just "four charts that happen to work".  It is a genuine
tetrahedral harmonic packet with the exact split

    7 = 4 + 3 = 1 + 6

that the docs had already hinted at.

More concretely:

    - 4 chart vertices give the tetrahedral oscillator gap ``4``;
    - the centered nontrivial shell has dimension ``3``;
    - the 6 undirected chart bridges are the shared six-channel count;
    - the 12 directed bridges act as exact chart-to-chart transfer operators.
"""

from __future__ import annotations

from functools import lru_cache
import itertools
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]


from exploration.w33_diffuse_color_parabolic_bridge import (
    _left_color_operator,
    _sign_vector_from_diffuse_line,
)
from exploration.w33_toroidal_tetrahedral_color_atlas_bridge import (
    _chart_yukawas,
)


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tetrahedral_chart_oscillator_bridge_summary.json"

SHARED_SIX_CHANNEL = 6
GAUGE_DIMENSION = 12
PHI6 = 7


def _chart_sign_matrix() -> tuple[list[str], np.ndarray]:
    chart_yukawas = _chart_yukawas()
    names = list(chart_yukawas)
    signs = []
    for name in names:
        signs.append(_sign_vector_from_diffuse_line(chart_yukawas[name]).astype(float))
    return names, np.stack(signs, axis=0)


def _best_cross_right_intertwiner(
    left_operator: np.ndarray,
    source_yukawa: np.ndarray,
    target_yukawa: np.ndarray,
) -> float:
    rows = []
    rhs = []
    for left_index in range(8):
        for right_index in range(8):
            coeff = np.zeros(64, dtype=complex)
            for inner in range(8):
                coeff[inner * 8 + right_index] = -target_yukawa[left_index, inner]
            rows.append(coeff)
            rhs.append(-(left_operator @ source_yukawa)[left_index, right_index])
    matrix = np.stack(rows, axis=0)
    target = np.array(rhs, dtype=complex)
    solution, _, _, _ = np.linalg.lstsq(matrix, target, rcond=None)
    right_operator = solution.reshape(8, 8)
    return float(np.linalg.norm(left_operator @ source_yukawa - target_yukawa @ right_operator))


def _rank(matrices: list[np.ndarray]) -> int:
    flattened = np.stack([matrix.reshape(-1) for matrix in matrices], axis=1)
    return int(np.linalg.matrix_rank(flattened, tol=1e-10))


def _line_stabilizer_basis(sign_vector: np.ndarray) -> list[np.ndarray]:
    rows = []
    for row_index in range(3):
        row = np.zeros(10, dtype=float)
        row[3 * row_index : 3 * row_index + 3] = sign_vector
        row[9] = -sign_vector[row_index]
        rows.append(row)
    matrix = np.stack(rows, axis=0)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > 1e-10))
    nullspace = vh[rank:, :].T
    return [nullspace[:9, column].reshape(3, 3) for column in range(nullspace.shape[1])]


@lru_cache(maxsize=1)
def build_summary() -> dict[str, Any]:
    chart_names, sign_matrix = _chart_sign_matrix()
    chart_yukawas = _chart_yukawas()

    tetra_laplacian = 4 * np.eye(4) - np.ones((4, 4))
    chart_gram = sign_matrix @ sign_matrix.T
    color_gram = sign_matrix.T @ sign_matrix

    projectors = {
        name: np.outer(sign_matrix[index], sign_matrix[index]) / 4.0
        for index, name in enumerate(chart_names)
    }

    directed_transfers: dict[str, np.ndarray] = {}
    directed_transfer_residuals: dict[str, float] = {}
    for source_name, target_name in itertools.permutations(chart_names, 2):
        source_index = chart_names.index(source_name)
        target_index = chart_names.index(target_name)
        transfer = np.outer(sign_matrix[target_index], sign_matrix[source_index]) / 3.0
        key = f"{source_name}_to_{target_name}"
        directed_transfers[key] = transfer
        directed_transfer_residuals[key] = _best_cross_right_intertwiner(
            _left_color_operator(transfer),
            chart_yukawas[source_name],
            chart_yukawas[target_name],
        )

    symmetric_edge_dyads = []
    antisymmetric_edge_dyads = []
    edge_vectors = {}
    for left_index, right_index in itertools.combinations(range(4), 2):
        left_name = chart_names[left_index]
        right_name = chart_names[right_index]
        key = f"{left_name}_{right_name}"
        left = sign_matrix[left_index]
        right = sign_matrix[right_index]
        symmetric_edge_dyads.append(np.outer(left, right) + np.outer(right, left))
        antisymmetric_edge_dyads.append(np.outer(left, right) - np.outer(right, left))
        edge_vectors[key] = ((left - right) / 2.0).tolist()

    all_directed_transfer_matrices = list(directed_transfers.values())
    projector_matrices = list(projectors.values())
    local_parabolics = {
        name: _line_stabilizer_basis(sign_matrix[index])
        for index, name in enumerate(chart_names)
    }

    outgoing_completion_ranks: dict[str, int] = {}
    incoming_completion_ranks: dict[str, int] = {}
    for source_index, source_name in enumerate(chart_names):
        other_indices = [index for index in range(len(chart_names)) if index != source_index]
        for left_index, right_index in itertools.combinations(other_indices, 2):
            left_name = chart_names[left_index]
            right_name = chart_names[right_index]
            key = f"{source_name}_via_{left_name}_{right_name}"
            outgoing_completion_ranks[key] = _rank(
                local_parabolics[source_name]
                + [
                    np.outer(sign_matrix[left_index], sign_matrix[source_index]) / 3.0,
                    np.outer(sign_matrix[right_index], sign_matrix[source_index]) / 3.0,
                ]
            )
            incoming_completion_ranks[key] = _rank(
                local_parabolics[source_name]
                + [
                    np.outer(sign_matrix[source_index], sign_matrix[left_index]) / 3.0,
                    np.outer(sign_matrix[source_index], sign_matrix[right_index]) / 3.0,
                ]
            )

    return {
        "status": "ok",
        "tetrahedral_chart_frame": {
            "chart_names": chart_names,
            "sign_matrix": sign_matrix.astype(int).tolist(),
            "chart_sum_is_zero": sign_matrix.sum(axis=0).astype(int).tolist(),
            "chart_gram": chart_gram.astype(int).tolist(),
            "color_gram": color_gram.astype(int).tolist(),
            "tetra_laplacian": tetra_laplacian.astype(int).tolist(),
            "chart_gram_equals_tetra_laplacian": np.array_equal(chart_gram, tetra_laplacian),
            "color_gram_equals_4I3": np.array_equal(color_gram, 4 * np.eye(3)),
        },
        "projector_packet": {
            "projectors": {
                name: projector.tolist() for name, projector in projectors.items()
            },
            "projector_sum": sum(projector_matrices).tolist(),
            "projector_sum_equals_identity": np.allclose(sum(projector_matrices), np.eye(3)),
            "projector_span_rank": _rank(projector_matrices),
        },
        "edge_transition_packet": {
            "undirected_edge_count": len(edge_vectors),
            "directed_edge_count": len(directed_transfers),
            "edge_vectors": edge_vectors,
            "all_half_edge_vectors_have_norm_squared_two": all(
                abs(float(np.dot(vector, vector)) - 2.0) < 1e-12
                for vector in (np.array(values, dtype=float) for values in edge_vectors.values())
            ),
            "symmetric_edge_span_rank": _rank(symmetric_edge_dyads),
            "antisymmetric_edge_span_rank": _rank(antisymmetric_edge_dyads),
            "directed_transfer_span_rank": _rank(all_directed_transfer_matrices),
            "max_directed_transfer_residual": max(directed_transfer_residuals.values()),
            "directed_transfer_residuals": directed_transfer_residuals,
            "outgoing_completion_ranks": outgoing_completion_ranks,
            "incoming_completion_ranks": incoming_completion_ranks,
        },
        "tetrahedral_oscillator_theorem": {
            "four_chart_vertices_form_a_regular_tetrahedron": (
                np.array_equal(chart_gram, tetra_laplacian)
                and np.array_equal(color_gram, 4 * np.eye(3))
                and np.array_equal(sign_matrix.sum(axis=0), np.zeros(3))
            ),
            "the_chart_frame_realizes_the_exact_k4_laplacian": np.array_equal(chart_gram, tetra_laplacian),
            "the_nontrivial_k4_shell_is_exactly_three_dimensional": np.array_equal(color_gram, 4 * np.eye(3)),
            "the_four_projectors_resolve_the_identity": np.allclose(sum(projector_matrices), np.eye(3)),
            "the_six_undirected_chart_bridges_span_the_full_symmetric_color_sector": (
                _rank(symmetric_edge_dyads) == 6
            ),
            "the_antisymmetric_chart_bridges_span_the_rotation_sector": (
                _rank(antisymmetric_edge_dyads) == 3
            ),
            "the_twelve_directed_chart_bridges_span_the_full_color_matrix_space": (
                _rank(all_directed_transfer_matrices) == 9
            ),
            "every_directed_chart_bridge_is_an_exact_cross_chart_intertwiner": (
                max(directed_transfer_residuals.values()) < 1e-12
            ),
            "any_two_outgoing_bridges_from_one_chart_complete_full_color": (
                all(rank == 9 for rank in outgoing_completion_ranks.values())
            ),
            "incoming_bridges_do_not_complete_the_local_parabolic_chart": (
                all(rank == 7 for rank in incoming_completion_ranks.values())
            ),
            "shared_six_channel_equals_undirected_edge_count": len(edge_vectors) == SHARED_SIX_CHANNEL,
            "gauge_dimension_equals_directed_edge_count": len(directed_transfers) == GAUGE_DIMENSION,
            "phi6_splits_exactly_as_one_plus_six": 1 + len(edge_vectors) == PHI6,
            "phi6_splits_exactly_as_four_plus_three": sign_matrix.shape[0] + sign_matrix.shape[1] == PHI6,
        },
        "bridge_verdict": (
            "The tetrahedral color-atlas is already a harmonic packet. Its four "
            "signed charts form a regular tetrahedron with Gram matrix 4I-J, so "
            "the chart-space oscillator is exactly the K4 Laplacian with gap 4. "
            "The centered shell is 3-dimensional and identified with the local "
            "color mode space by the tight-frame law S^T S = 4I. The six "
            "undirected chart bridges span the full symmetric color sector, the "
            "antisymmetric bridges span the 3-dimensional rotation sector, and "
            "the twelve directed bridges span the full 9-dimensional color matrix "
            "space. Better still, those directed bridges are not only counts: "
            "every one is an exact cross-chart intertwiner on the actual diffuse "
            "Yukawa packet, and any two outgoing bridges from one chart already "
            "complete the full color algebra while the corresponding incoming "
            "bridges do not. So the old clue 7 = 4+3 = 1+6 is now operator-real: "
            "4 chart vertices plus the 3-dimensional centered shell, and equally "
            "1 selector line plus 6 undirected chart bridges, are two exact views "
            "of the same tetrahedral local oscillator."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    write_summary()
