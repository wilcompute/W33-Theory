"""The live CKM family envelope and paper asymmetry share one tetra-doublet axis.

The previous bridges established:

- the tetrahedral doublet inside Sym^2(4) is the exact family doublet after
  restriction to the natural S3;
- the paper real up/down asymmetry is doublet-dominant.

This bridge checks the sharper statement: whether the paper real asymmetry and
the live CKM family envelope point in the *same* doublet direction.

They do.

After projecting both operators to the canonical S4 doublet inside Sym^2(4),
their coefficient vectors are exactly collinear.  So the paper up/down
asymmetry is not choosing a new family direction.  It is scaling the same
family doublet axis that is already present in the live CKM envelope.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_family_doublet_axis_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_tetrahedral_ckm_oscillator_bridge import (
    _paper_up_down_vectors,
    _two_edge_vector,
)
from exploration.w33_triality_phase_compression_bridge import _load_json


CLASS_ORDER = ("1^4", "2 1^2", "2^2", "3 1", "4")
DOUBLET_CHARACTER = [2, 0, 2, -1, 0]
SYM_BASIS = [(i, j) for i in range(4) for j in range(i, 4)]


def _cycle_type(perm: tuple[int, ...]) -> str:
    seen = [False] * 4
    lengths: list[int] = []
    for start in range(4):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            current = perm[current]
            length += 1
        lengths.append(length)
    lengths.sort(reverse=True)
    return {
        (1, 1, 1, 1): "1^4",
        (2, 1, 1): "2 1^2",
        (2, 2): "2^2",
        (3, 1): "3 1",
        (4,): "4",
    }[tuple(lengths)]


def _permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((4, 4), dtype=float)
    for source, target in enumerate(perm):
        matrix[target, source] = 1.0
    return matrix


def _sym2_rep(matrix: np.ndarray) -> np.ndarray:
    result = np.zeros((10, 10), dtype=float)
    for column, (i, j) in enumerate(SYM_BASIS):
        source = np.zeros((4, 4), dtype=float)
        source[i, j] += 1.0
        source[j, i] += 1.0 if i != j else 0.0
        image = matrix @ source @ matrix.T
        for row, (a, b) in enumerate(SYM_BASIS):
            result[row, column] = image[a, b]
    return result


def _doublet_basis() -> np.ndarray:
    projector = np.zeros((10, 10), dtype=float)
    for perm in itertools.permutations(range(4)):
        class_name = _cycle_type(perm)
        class_index = CLASS_ORDER.index(class_name)
        projector += DOUBLET_CHARACTER[class_index] * _sym2_rep(_permutation_matrix(perm))
    projector *= 2.0 / 24.0

    eigenvalues, eigenvectors = np.linalg.eigh((projector + projector.T) / 2.0)
    return eigenvectors[:, eigenvalues > 0.5]


def _sym_coords(matrix: np.ndarray) -> np.ndarray:
    return np.array([matrix[i, j] for i, j in SYM_BASIS], dtype=float)


def _matrix_from_coords(coords: np.ndarray) -> np.ndarray:
    matrix = np.zeros((4, 4), dtype=float)
    for value, (i, j) in zip(coords, SYM_BASIS):
        matrix[i, j] = value
        matrix[j, i] = value
    return matrix


def build_summary() -> dict[str, Any]:
    basis = _doublet_basis()
    basis_matrices = [_matrix_from_coords(basis[:, index]) for index in range(basis.shape[1])]

    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    live_a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    live_b = float(lift["second_layer_lift_edge"]["amplitude"])
    live = _two_edge_vector(live_a, live_b)
    paper_up, paper_down = _paper_up_down_vectors()

    live_sym = np.outer(live, np.conjugate(live)).real
    paper_real_asym = (np.outer(paper_up, np.conjugate(paper_up)).real - np.outer(paper_down, np.conjugate(paper_down)).real) / 2.0

    live_coords = basis.T @ _sym_coords(live_sym)
    paper_coords = basis.T @ _sym_coords(paper_real_asym)
    live_norm = float(np.linalg.norm(live_coords))
    paper_norm = float(np.linalg.norm(paper_coords))
    axis_overlap = float(abs(np.vdot(live_coords / live_norm, paper_coords / paper_norm)))
    scale_ratio = float(paper_coords[0] / live_coords[0])

    return {
        "tetra_doublet_basis": {
            "dimension": int(basis.shape[1]),
            "basis_matrices": [
                [[float(value) for value in row] for row in matrix]
                for matrix in basis_matrices
            ],
        },
        "projected_doublet_coordinates": {
            "live_family_envelope": [float(value) for value in live_coords],
            "paper_real_asymmetry": [float(value) for value in paper_coords],
            "live_norm": live_norm,
            "paper_norm": paper_norm,
            "scale_ratio_paper_over_live": scale_ratio,
            "absolute_axis_overlap": axis_overlap,
        },
        "ckm_family_doublet_axis_theorem": {
            "the_paper_real_asymmetry_and_live_family_envelope_have_nonzero_projection_on_the_same_tetra_doublet": bool(
                live_norm > 1e-12 and paper_norm > 1e-12
            ),
            "their_tetra_doublet_projections_are_exactly_collinear": bool(
                abs(axis_overlap - 1.0) < 1e-12
            ),
            "the_paper_family_asymmetry_is_the_same_doublet_axis_at_a_smaller_strength": bool(
                abs(axis_overlap - 1.0) < 1e-12 and 0.0 < abs(scale_ratio) < 1.0
            ),
        },
        "interpretation": (
            "The family side has compressed further. The paper's real up/down asymmetry "
            "does not pick a new family direction; after projection to the canonical "
            "tetrahedral doublet, it is exactly collinear with the live CKM family "
            "envelope. So the paper asymmetry is the same tetra/family doublet axis "
            "at a weaker strength."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["ckm_family_doublet_axis_theorem"], indent=2))


if __name__ == "__main__":
    main()
