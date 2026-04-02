"""Exact finite family normal form on the Yukawa frontier.

This module packages the strongest conservative family-sector theorem already
forced by the repo's exact Yukawa bridge chain.

What is established:
  - the six l6 A2 modes are exactly the six ordered generation-transfer
    channels, i.e. the complete oriented three-generation graph;
  - on the replicated seed, the exact nonzero A2 response channels form a
    four-channel star at one distinguished generation, while the two dormant
    channels are the opposite bidirectional pair;
  - the universal reduced generation algebra carries a common exact flag;
  - in the exact flag basis
        u = (1,1,0),  v = (0,0,1),  w = (1,-1,0),
    the two universal generation matrices become explicit upper-unitriangular
    integer matrices with the same nonzero square 2 E_13.

So before any continuum orbit / sigma-model interpretation is added, the
repo-native finite family side already closes as an exact one-versus-two family
packet with a canonical 3x3 flag/unipotent normal form.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
if __package__ in {None, ""}:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from exploration._artifact_paths import load_json_from_repo_data
else:
    from ._artifact_paths import load_json_from_repo_data

DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_family_normal_form_bridge_summary.json"

SYMMETRIC_DOUBLET_VECTOR = np.array([1, 1, 0], dtype=int)
DISTINGUISHED_GENERATION_VECTOR = np.array([0, 0, 1], dtype=int)
DOUBLET_DIFFERENCE_VECTOR = np.array([1, -1, 0], dtype=int)

FLAG_BASIS = np.column_stack(
    [SYMMETRIC_DOUBLET_VECTOR, DISTINGUISHED_GENERATION_VECTOR, DOUBLET_DIFFERENCE_VECTOR]
).astype(int)
TWICE_FLAG_BASIS_INVERSE = np.array(
    [
        [1, 1, 0],
        [0, 0, 2],
        [1, -1, 0],
    ],
    dtype=int,
)


def _read_json(filename: str) -> dict[str, Any]:
    return load_json_from_repo_data(ROOT, Path("data") / filename)


def _sorted_pairs(pairs: set[tuple[int, int]]) -> list[list[int]]:
    return [list(pair) for pair in sorted(pairs)]


def _conjugate_in_flag_basis(matrix: np.ndarray) -> np.ndarray:
    numerators = TWICE_FLAG_BASIS_INVERSE @ matrix @ FLAG_BASIS
    if np.any(numerators % 2):
        raise ValueError("Flag-basis conjugation did not stay integral")
    return (numerators // 2).astype(int)


def _standard_matrix(i: int, j: int) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=int)
    matrix[i, j] = 1
    return matrix


@lru_cache(maxsize=1)
def build_yukawa_family_normal_form_summary() -> dict[str, Any]:
    transport = _read_json("w33_transport_lie_tower_bridge_summary.json")
    selection = _read_json("w33_l6_a2_selection_bridge_summary.json")
    unipotent = _read_json("w33_yukawa_unipotent_reduction_bridge_summary.json")

    channel_entries = selection["a2_seed_channels"]
    active_pairs = {
        (int(entry["source_generation"]), int(entry["target_generation"]))
        for entry in channel_entries
        if not entry["zero_response_on_replicated_seed"]
    }
    dormant_pairs = {
        (int(entry["source_generation"]), int(entry["target_generation"]))
        for entry in channel_entries
        if entry["zero_response_on_replicated_seed"]
    }

    incidence_counts = {generation: 0 for generation in range(3)}
    for source_generation, target_generation in active_pairs:
        incidence_counts[source_generation] += 1
        incidence_counts[target_generation] += 1
    distinguished_generation = next(
        generation for generation, count in incidence_counts.items() if count == 4
    )
    doublet_generations = tuple(
        generation for generation in range(3) if generation != distinguished_generation
    )

    expected_active_pairs = {
        (distinguished_generation, doublet_generations[0]),
        (doublet_generations[0], distinguished_generation),
        (distinguished_generation, doublet_generations[1]),
        (doublet_generations[1], distinguished_generation),
    }
    expected_dormant_pairs = {
        (doublet_generations[0], doublet_generations[1]),
        (doublet_generations[1], doublet_generations[0]),
    }

    algebra = unipotent["universal_generation_algebra"]
    plus_minus = np.array(algebra["plus_minus_generation_matrix"], dtype=int)
    minus_plus = np.array(algebra["minus_plus_generation_matrix"], dtype=int)
    identity = np.eye(3, dtype=int)
    plus_minus_nf = _conjugate_in_flag_basis(plus_minus)
    minus_plus_nf = _conjugate_in_flag_basis(minus_plus)
    plus_minus_nilpotent_nf = plus_minus_nf - identity
    minus_plus_nilpotent_nf = minus_plus_nf - identity
    common_square_nf = plus_minus_nilpotent_nf @ plus_minus_nilpotent_nf

    e12 = _standard_matrix(0, 1)
    e13 = _standard_matrix(0, 2)
    e23 = _standard_matrix(1, 2)

    return {
        "status": "ok",
        "a2_channel_graph": {
            "ordered_generation_pairs": transport["generation_channel_theorem"][
                "ordered_generation_pairs"
            ],
            "active_quartet": _sorted_pairs(active_pairs),
            "dormant_pair": _sorted_pairs(dormant_pairs),
            "distinguished_generation": int(distinguished_generation),
            "doublet_generations": list(doublet_generations),
        },
        "flag_basis": {
            "basis_order": [
                "symmetric_doublet_line",
                "distinguished_generation_axis",
                "doublet_difference_axis",
            ],
            "symmetric_doublet_line": SYMMETRIC_DOUBLET_VECTOR.tolist(),
            "distinguished_generation_axis": DISTINGUISHED_GENERATION_VECTOR.tolist(),
            "doublet_difference_axis": DOUBLET_DIFFERENCE_VECTOR.tolist(),
            "basis_matrix": FLAG_BASIS.astype(int).tolist(),
            "twice_basis_inverse": TWICE_FLAG_BASIS_INVERSE.astype(int).tolist(),
        },
        "generation_normal_form": {
            "plus_minus": plus_minus_nf.astype(int).tolist(),
            "minus_plus": minus_plus_nf.astype(int).tolist(),
            "plus_minus_nilpotent": plus_minus_nilpotent_nf.astype(int).tolist(),
            "minus_plus_nilpotent": minus_plus_nilpotent_nf.astype(int).tolist(),
            "common_square": common_square_nf.astype(int).tolist(),
            "plus_minus_standard_upper_coefficients": {
                "E12": int(plus_minus_nilpotent_nf[0, 1]),
                "E13": int(plus_minus_nilpotent_nf[0, 2]),
                "E23": int(plus_minus_nilpotent_nf[1, 2]),
            },
            "minus_plus_standard_upper_coefficients": {
                "E12": int(minus_plus_nilpotent_nf[0, 1]),
                "E13": int(minus_plus_nilpotent_nf[0, 2]),
                "E23": int(minus_plus_nilpotent_nf[1, 2]),
            },
        },
        "finite_family_theorem": {
            "transport_a2_slice_is_complete_oriented_triangle": bool(
                transport["generation_channel_theorem"]["complete_oriented_three_generation_graph"]
            ),
            "replicated_seed_current_packet_is_exact_4_plus_2_split": (
                len(active_pairs) == 4 and len(dormant_pairs) == 2
            ),
            "active_quartet_is_star_at_distinguished_generation": active_pairs
            == expected_active_pairs,
            "dormant_pair_is_opposite_bidirectional_edge": dormant_pairs
            == expected_dormant_pairs,
            "generation_matrices_commute_exactly": bool(
                algebra["generation_matrices_commute_exactly"]
            ),
            "flag_basis_conjugates_generation_matrices_to_upper_unitriangular_form": bool(
                np.array_equal(np.triu(plus_minus_nf), plus_minus_nf)
                and np.array_equal(np.triu(minus_plus_nf), minus_plus_nf)
                and np.array_equal(np.diag(np.diag(plus_minus_nf)), identity)
                and np.array_equal(np.diag(np.diag(minus_plus_nf)), identity)
            ),
            "common_square_is_exact_central_e13_channel": np.array_equal(
                common_square_nf, 2 * e13
            ),
            "normal_form_is_exact_standard_upper_triangular_packet": np.array_equal(
                plus_minus_nilpotent_nf, e12 - 2 * e13 + 2 * e23
            )
            and np.array_equal(minus_plus_nilpotent_nf, -e12 - 2 * e13 - 2 * e23),
            "finite_family_side_has_exact_one_vs_two_normal_form": (
                transport["generation_channel_theorem"]["complete_oriented_three_generation_graph"]
                and len(active_pairs) == 4
                and len(dormant_pairs) == 2
                and active_pairs == expected_active_pairs
                and dormant_pairs == expected_dormant_pairs
                and bool(algebra["generation_matrices_commute_exactly"])
                and np.array_equal(common_square_nf, 2 * e13)
            ),
        },
        "bridge_verdict": (
            "The exact finite family side is now sharper than a generic 'flag hint'. "
            "The transport/l6 A2 slice is the complete oriented three-generation "
            "graph, the replicated seed picks out an exact four-plus-two split as "
            "the star at one distinguished generation plus the opposite dormant "
            "pair, and the universal generation algebra is conjugate in the exact "
            "basis (1,1,0),(0,0,1),(1,-1,0) to an upper-unitriangular 3x3 packet "
            "with common square 2E13. So the finite family/Yukawa packet already "
            "has an exact one-versus-two normal form before any continuum orbit "
            "interpretation is promoted."
        ),
        "source_files": [
            "data/w33_transport_lie_tower_bridge_summary.json",
            "data/w33_l6_a2_selection_bridge_summary.json",
            "data/w33_yukawa_unipotent_reduction_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_yukawa_family_normal_form_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
