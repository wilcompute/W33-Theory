"""CKM family/CP separation on the tetrahedral Clifford packet.

This bridge takes the live and paper four-slot CKM packets and decomposes their
quadratic carriers on the exact tetrahedral Clifford packet.

For a four-slot complex family vector ``v``, the rank-one Hermitian packet

    P = v v*

splits canonically as

    P = S + i A,

with

    S^T = S   in Sym^2(4),
    A^T = -A  in Lambda^2(4).

Using the tetrahedral S4 refinement already established locally,

    Sym^2(4)   = 1 + 1 + 2 + 3 + 3,
    Lambda^2(4)= 3 + 3',

we can ask where the live CKM family envelope and CP phase actually sit.

The sharp current answer is:

1. Conjugate CKM branches have exactly the same symmetric family envelope and
   differ only by the sign of the bivector packet.
2. So CP really does live on the bivector shell Lambda^2(4).
3. The paper up/down *real* asymmetry is dominated by the tetrahedral doublet,
   which by the previous S4->S3 bridge is the exact family doublet.
4. The paper *imaginary* asymmetry lives entirely in the bivector shell and is
   nearly Hodge-balanced between the two 3-dimensional bivector sectors.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_clifford_sector_separation_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_tetrahedral_ckm_oscillator_bridge import (
    _paper_up_down_vectors,
    _two_edge_vector,
)
from exploration.w33_triality_phase_compression_bridge import _load_json


CLASS_ORDER = ("1^4", "2 1^2", "2^2", "3 1", "4")
IRREP_CHARACTERS: dict[str, list[int]] = {
    "1": [1, 1, 1, 1, 1],
    "1'": [1, -1, 1, 1, -1],
    "2": [2, 0, 2, -1, 0],
    "3": [3, 1, -1, 0, -1],
    "3'": [3, -1, -1, 0, 1],
}

SYM_BASIS = [(i, j) for i in range(4) for j in range(i, 4)]
WEDGE_BASIS = [(i, j) for i in range(4) for j in range(i + 1, 4)]


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


def _wedge2_rep(matrix: np.ndarray) -> np.ndarray:
    result = np.zeros((6, 6), dtype=float)
    for column, (i, j) in enumerate(WEDGE_BASIS):
        image_i = np.argmax(matrix[:, i])
        image_j = np.argmax(matrix[:, j])
        a, b = sorted((image_i, image_j))
        sign = 1.0 if (image_i, image_j) == (a, b) else -1.0
        row = WEDGE_BASIS.index((a, b))
        result[row, column] = sign
    return result


def _build_irrep_projectors() -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    sym_projectors = {name: np.zeros((10, 10), dtype=float) for name in IRREP_CHARACTERS}
    wedge_projectors = {name: np.zeros((6, 6), dtype=float) for name in IRREP_CHARACTERS}
    for perm in itertools.permutations(range(4)):
        class_name = _cycle_type(perm)
        class_index = CLASS_ORDER.index(class_name)
        matrix = _permutation_matrix(perm)
        sym_rep = _sym2_rep(matrix)
        wedge_rep = _wedge2_rep(matrix)
        for irrep_name, character in IRREP_CHARACTERS.items():
            sym_projectors[irrep_name] += character[class_index] * sym_rep
            wedge_projectors[irrep_name] += character[class_index] * wedge_rep

    for irrep_name, character in IRREP_CHARACTERS.items():
        dim = character[0]
        sym_projectors[irrep_name] *= dim / 24.0
        wedge_projectors[irrep_name] *= dim / 24.0

    return sym_projectors, wedge_projectors


def _sym_coords(matrix: np.ndarray) -> np.ndarray:
    return np.array([matrix[i, j] for i, j in SYM_BASIS], dtype=float)


def _wedge_coords(matrix: np.ndarray) -> np.ndarray:
    return np.array([matrix[i, j] for i, j in WEDGE_BASIS], dtype=float)


def _sector_norms(
    vector: np.ndarray,
    sym_projectors: dict[str, np.ndarray],
    wedge_projectors: dict[str, np.ndarray],
) -> dict[str, Any]:
    projector = np.outer(vector, np.conjugate(vector))
    symmetric = projector.real
    bivector = projector.imag
    sym_coords = _sym_coords(symmetric)
    wedge_coords = _wedge_coords(bivector)
    return {
        "vector_real_imag": [
            {"real": float(value.real), "imag": float(value.imag)} for value in vector
        ],
        "sym_irrep_norms": {
            irrep_name: float(np.linalg.norm(projector_matrix @ sym_coords))
            for irrep_name, projector_matrix in sym_projectors.items()
        },
        "wedge_irrep_norms": {
            irrep_name: float(np.linalg.norm(projector_matrix @ wedge_coords))
            for irrep_name, projector_matrix in wedge_projectors.items()
        },
    }


def build_summary() -> dict[str, Any]:
    sym_projectors, wedge_projectors = _build_irrep_projectors()

    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    live_a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    live_b = float(lift["second_layer_lift_edge"]["amplitude"])
    live_plus = _two_edge_vector(live_a, live_b)
    live_minus = np.conjugate(live_plus)

    paper_up, paper_down = _paper_up_down_vectors()

    live_plus_packet = _sector_norms(live_plus, sym_projectors, wedge_projectors)
    live_minus_packet = _sector_norms(live_minus, sym_projectors, wedge_projectors)
    paper_up_packet = _sector_norms(paper_up, sym_projectors, wedge_projectors)
    paper_down_packet = _sector_norms(paper_down, sym_projectors, wedge_projectors)

    p_live_plus = np.outer(live_plus, np.conjugate(live_plus))
    p_live_minus = np.outer(live_minus, np.conjugate(live_minus))
    p_paper_up = np.outer(paper_up, np.conjugate(paper_up))
    p_paper_down = np.outer(paper_down, np.conjugate(paper_down))

    live_family_envelope_error = float(np.linalg.norm(p_live_plus.real - p_live_minus.real))
    live_cp_flip_error = float(np.linalg.norm(p_live_plus.imag + p_live_minus.imag))

    real_asymmetry = (p_paper_up.real - p_paper_down.real) / 2.0
    imag_asymmetry = (p_paper_up.imag - p_paper_down.imag) / 2.0
    real_asymmetry_sym_coords = _sym_coords(real_asymmetry)
    imag_asymmetry_wedge_coords = _wedge_coords(imag_asymmetry)

    real_asymmetry_norms = {
        irrep_name: float(np.linalg.norm(projector_matrix @ real_asymmetry_sym_coords))
        for irrep_name, projector_matrix in sym_projectors.items()
    }
    imag_asymmetry_norms = {
        irrep_name: float(np.linalg.norm(projector_matrix @ imag_asymmetry_wedge_coords))
        for irrep_name, projector_matrix in wedge_projectors.items()
    }

    real_total = np.sqrt(sum(value * value for value in real_asymmetry_norms.values()))
    imag_total = np.sqrt(sum(value * value for value in imag_asymmetry_norms.values()))
    doublet_share = real_asymmetry_norms["2"] / real_total if real_total > 0 else 0.0
    hodge_balance_ratio = (
        imag_asymmetry_norms["3"] / imag_asymmetry_norms["3'"]
        if imag_asymmetry_norms["3'"] > 0
        else 0.0
    )

    return {
        "live_branch_packet": {
            "plus_branch": live_plus_packet,
            "minus_branch": live_minus_packet,
            "symmetric_family_envelope_match_error": live_family_envelope_error,
            "bivector_cp_sign_flip_error": live_cp_flip_error,
        },
        "paper_packet": {
            "up": paper_up_packet,
            "down": paper_down_packet,
            "real_asymmetry_sym_irrep_norms": real_asymmetry_norms,
            "imag_asymmetry_wedge_irrep_norms": imag_asymmetry_norms,
            "real_asymmetry_doublet_share": doublet_share,
            "imag_asymmetry_hodge_balance_ratio_3_over_3prime": hodge_balance_ratio,
        },
        "ckm_clifford_sector_separation_theorem": {
            "conjugate_live_ckm_branches_have_exactly_the_same_symmetric_family_envelope": bool(
                live_family_envelope_error < 1e-12
            ),
            "conjugate_live_ckm_branches_differ_only_by_sign_on_the_bivector_cp_shell": bool(
                live_cp_flip_error < 1e-12
            ),
            "the_live_and_paper_family_envelopes_live_on_the_symmetric_tetra_packet_sym2_4": bool(
                max(live_plus_packet["sym_irrep_norms"]["1'"], live_plus_packet["sym_irrep_norms"]["3'"]) < 1e-12
                and max(paper_up_packet["sym_irrep_norms"]["1'"], paper_up_packet["sym_irrep_norms"]["3'"]) < 1e-12
                and max(paper_down_packet["sym_irrep_norms"]["1'"], paper_down_packet["sym_irrep_norms"]["3'"]) < 1e-12
            ),
            "the_live_and_paper_cp_packets_live_on_the_bivector_shell_lambda2_4": bool(
                max(
                    live_plus_packet["wedge_irrep_norms"]["1"],
                    live_plus_packet["wedge_irrep_norms"]["1'"],
                    live_plus_packet["wedge_irrep_norms"]["2"],
                    paper_up_packet["wedge_irrep_norms"]["1"],
                    paper_up_packet["wedge_irrep_norms"]["1'"],
                    paper_up_packet["wedge_irrep_norms"]["2"],
                ) < 1e-12
            ),
            "the_paper_real_up_down_asymmetry_is_doublet_dominant": bool(
                doublet_share > 0.8
            ),
            "the_paper_imaginary_asymmetry_is_nearly_hodge_balanced_between_the_two_bivector_triplets": bool(
                abs(hodge_balance_ratio - 1.0) < 0.01
            ),
        },
        "interpretation": (
            "The tetra-Clifford split is now doing real work on the CKM side. "
            "The live branch pair has one common symmetric family envelope and "
            "a sign-flipped bivector packet, so CP lives on Lambda^2(4). The "
            "paper up/down real asymmetry is dominated by the tetrahedral doublet "
            "inside Sym^2(4), which is exactly the family doublet after restriction "
            "to the natural S3. Meanwhile the paper imaginary asymmetry lives "
            "entirely on the bivector shell and is almost perfectly balanced "
            "between its two 3-dimensional sectors."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["ckm_clifford_sector_separation_theorem"], indent=2))


if __name__ == "__main__":
    main()
