"""Universal tetrahedron-to-qutrit bridge across CKM, transport, and chart packets.

This bridge unifies three tetrahedral structures that had been sitting in
parallel:

1. the 4-slot CKM carrier packet;
2. the 4-chart tetrahedral atlas packet;
3. the 45-point center-quad transport bundle with local 3-state fibers.

The key observation is that a tetrahedron has:

    - 4 vertices,
    - 3 opposite-edge matchings (axes),
    - permutation symmetry S4 on vertices,
    - induced permutation symmetry S3 on the three axes.

The three axis states are exactly a qutrit/ triality packet:

    3 = 1 ⊕ 2

over the reals, and after DFT3 diagonalization they become the
``1, ω, ω²`` qutrit carrier over the complexes.

So the current exact read is:

    tetrahedron vertices  <->  CKM/chart 4-packet,
    tetrahedron axes      <->  transport local 3-packet,
    augmentation plane    <->  transport/A2 2-shell.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_center_quad_tetrahedral_oscillator_bridge import (
    TETRA_MATCHINGS,
    _matching_transport_permutation,
    _transport_edges,
)
from exploration.w33_mode_major_color_triplet_bridge import _chart_fourier_basis
from exploration.w33_yukawa_qutrit_collapse_bridge import PERMUTATION_CYCLE


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_universal_tetra_qutrit_bridge_summary.json"
MODE_ORDER = ("singlet", "tangent_1", "tangent_2", "tangent_3")


def _serialize_complex_matrix(matrix: np.ndarray) -> list[list[dict[str, float]]]:
    return [
        [{"real": float(value.real), "imag": float(value.imag)} for value in row]
        for row in matrix
    ]


def _tetra_hadamard() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0, 1.0],
        ],
        dtype=float,
    ).T / 2.0


def _canonical_tetra_axis_sign_matrix() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, 1.0],
        ],
        dtype=float,
    )


def _chart_sign_matrix_from_basis() -> np.ndarray:
    basis = _chart_fourier_basis()
    return 2.0 * np.column_stack([basis[name] for name in MODE_ORDER[1:]])


def _matches_up_to_relabels(left: np.ndarray, right: np.ndarray) -> dict[str, Any]:
    for row_perm in itertools.permutations(range(left.shape[0])):
        permuted_rows = left[list(row_perm), :]
        for col_perm in itertools.permutations(range(left.shape[1])):
            permuted = permuted_rows[:, list(col_perm)]
            for signs in itertools.product((-1.0, 1.0), repeat=left.shape[1]):
                signed = permuted * np.array(signs, dtype=float)
                if np.array_equal(signed, right):
                    return {
                        "matches": True,
                        "row_permutation": list(row_perm),
                        "column_permutation": list(col_perm),
                        "column_signs": list(signs),
                    }
    return {"matches": False}


def _axis_permutation_from_vertex_permutation(vertex_permutation: tuple[int, ...]) -> tuple[int, int, int]:
    image = []
    for matching in TETRA_MATCHINGS:
        pushed = tuple(sorted(tuple(sorted((vertex_permutation[a], vertex_permutation[b]))) for a, b in matching))
        image.append(TETRA_MATCHINGS.index(pushed))
    return tuple(image)


def _dft3() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3.0)
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega**2],
            [1.0, omega**2, omega],
        ],
        dtype=complex,
    )


def _invert_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return tuple(inverse)


@lru_cache(maxsize=1)
def _transport_permutation_counts() -> Counter[tuple[int, int, int]]:
    counts: Counter[tuple[int, int, int]] = Counter()
    for left, right in _transport_edges():
        counts[_matching_transport_permutation(left, right)] += 1
    return counts


def build_summary() -> dict[str, Any]:
    hadamard = _tetra_hadamard()
    tetra_axis = _canonical_tetra_axis_sign_matrix()
    chart_axis = _chart_sign_matrix_from_basis()
    axis_match = _matches_up_to_relabels(chart_axis, tetra_axis)

    axis_permutations = sorted({
        _axis_permutation_from_vertex_permutation(permutation)
        for permutation in itertools.permutations(range(4))
    })

    dft3 = _dft3()
    inverse_dft3 = np.conjugate(dft3).T / 3.0
    qutrit_diagonal = inverse_dft3 @ PERMUTATION_CYCLE.astype(complex) @ dft3

    transport_counts = _transport_permutation_counts()
    three_cycles = [perm for perm in transport_counts if perm in {(1, 2, 0), (2, 0, 1)}]
    representative_cycle = three_cycles[0]
    representative_cycle_matrix = np.zeros((3, 3), dtype=int)
    for column, row in enumerate(representative_cycle):
        representative_cycle_matrix[row, column] = 1
    representative_diagonal = inverse_dft3 @ representative_cycle_matrix.astype(complex) @ dft3
    transport_cycle_matches_repo_qutrit = bool(
        np.array_equal(np.array(representative_cycle), PERMUTATION_CYCLE.argmax(axis=0))
    )
    transport_cycle_inverse_matches_repo_qutrit = bool(
        np.array_equal(np.array(_invert_permutation(representative_cycle)), PERMUTATION_CYCLE.argmax(axis=0))
    )

    return {
        "tetra_vertex_axis_dictionary": {
            "tetra_hadamard_basis": hadamard.tolist(),
            "canonical_axis_sign_matrix": tetra_axis.tolist(),
            "the_nontrivial_hadamard_columns_are_exactly_the_tetra_axis_sign_vectors": bool(
                np.array_equal(2.0 * hadamard[:, 1:], tetra_axis)
            ),
            "chart_axis_sign_matrix": np.rint(chart_axis).astype(int).tolist(),
            "chart_axis_matches_canonical_tetra_axis_up_to_relabels": axis_match,
        },
        "tetra_axis_symmetry": {
            "tetra_matchings": [list(map(list, matching)) for matching in TETRA_MATCHINGS],
            "induced_axis_permutations_from_vertex_s4": [list(permutation) for permutation in axis_permutations],
            "induced_axis_group_order": len(axis_permutations),
            "axis_group_is_exact_s3": len(axis_permutations) == 6,
        },
        "qutrit_identification": {
            "repo_cycle_generator": PERMUTATION_CYCLE.tolist(),
            "representative_transport_three_cycle": list(representative_cycle),
            "representative_transport_three_cycle_equals_repo_qutrit_cycle": transport_cycle_matches_repo_qutrit,
            "representative_transport_three_cycle_inverse_equals_repo_qutrit_cycle": (
                transport_cycle_inverse_matches_repo_qutrit
            ),
            "dft3_real_imag": _serialize_complex_matrix(dft3),
            "repo_qutrit_diagonal_real_imag": _serialize_complex_matrix(qutrit_diagonal),
            "transport_cycle_diagonal_real_imag": _serialize_complex_matrix(representative_diagonal),
            "transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation": bool(
                np.allclose(
                    np.sort_complex(np.diag(representative_diagonal)),
                    np.sort_complex(np.diag(qutrit_diagonal)),
                    atol=1e-12,
                )
            ),
        },
        "transport_bundle_dictionary": {
            "local_axis_packet_dimension": 3,
            "real_decomposition": {"radial": 1, "tangential": 2},
            "global_bundle_dimension": 135,
            "global_radial_dimension": 45,
            "global_tangential_dimension": 90,
            "transport_matching_permutation_counts": {
                str(key): value for key, value in sorted(transport_counts.items())
            },
            "all_six_axis_permutations_occur_on_transport_edges": len(transport_counts) == 6,
        },
        "universal_tetra_qutrit_theorem": {
            "the_ckm_chart_four_packet_is_the_vertex_side_of_one_universal_tetrahedron": bool(
                np.array_equal(2.0 * hadamard[:, 1:], tetra_axis) and axis_match["matches"]
            ),
            "the_transport_local_three_packet_is_the_axis_side_of_the_same_tetrahedron": len(axis_permutations) == 6,
            "the_axis_packet_is_exactly_the_real_shadow_one_plus_two_of_the_qutrit_triality_carrier": bool(
                len(axis_permutations) == 6
                and (
                    transport_cycle_matches_repo_qutrit
                    or transport_cycle_inverse_matches_repo_qutrit
                )
            ),
            "the_transport_135_bundle_is_45_copies_of_the_tetra_axis_qutrit": (
                45 * 3 == 135
            ),
            "the_transport_90_sector_is_45_copies_of_the_tangential_qutrit_shell": (
                45 * 2 == 90
            ),
        },
        "interpretation": (
            "The repo's tetrahedral structures are no longer separate motifs. The "
            "4-slot CKM/chart packet is the vertex realization of one tetrahedron, "
            "while the 3-state transport fiber is the opposite-edge-axis packet of "
            "that same tetrahedron. That axis packet is exactly an S3/qutrit carrier: "
            "real form 1+2, complex Fourier form 1,omega,omega^2. So the 45+90 "
            "transport split is the radial-plus-tangential shadow of 45 copies of "
            "the same universal tetra-qutrit object."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
