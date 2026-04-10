"""S4 refinement of the tetrahedral Spin(10)-sized packet.

The exact W33 dominant-shell result already gives

    16 = 10 + 6 = Sym^2(4) + Lambda^2(4)

for the live tetra/carrier ``4``.  This bridge asks the next natural question:
how does that packet refine under the actual tetrahedral symmetry on the
4-carrier?

For the permutation representation of S4 on four tetra vertices:

    4 = 1 + 3.

The induced representation-theoretic refinement is exact:

    Sym^2(4)   = 1 + 1 + 2 + 3 + 3,
    Lambda^2(4)= 3 + 3',

so the Clifford/tensor packet becomes

    16 = 1 + 1 + 2 + 3 + 3 + 3 + 3'.

This is stronger than the earlier count-level statement.  In particular, the
first genuinely non-singlet/non-triplet residue is a canonical tetrahedral
doublet ``2``.  That makes it the cleanest current home for any surviving
``middle-vs-outer`` asymmetry story.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_s4_tetra_spin10_refinement_bridge_summary.json"


CLASS_ORDER = ("1^4", "2 1^2", "2^2", "3 1", "4")
CLASS_SIZES = {"1^4": 1, "2 1^2": 6, "2^2": 3, "3 1": 8, "4": 6}

# Standard S4 irreducible characters on the class order above.
IRREP_CHARACTERS: dict[str, list[int]] = {
    "1": [1, 1, 1, 1, 1],
    "1'": [1, -1, 1, 1, -1],
    "2": [2, 0, 2, -1, 0],
    "3": [3, 1, -1, 0, -1],
    "3'": [3, -1, -1, 0, 1],
}


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


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
    if lengths == [1, 1, 1, 1]:
        return "1^4"
    if lengths == [2, 1, 1]:
        return "2 1^2"
    if lengths == [2, 2]:
        return "2^2"
    if lengths == [3, 1]:
        return "3 1"
    if lengths == [4]:
        return "4"
    raise ValueError(f"Unexpected cycle structure: {lengths}")


def _parity(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(4):
        for j in range(i + 1, 4):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def _permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((4, 4), dtype=float)
    for source, target in enumerate(perm):
        matrix[target, source] = 1.0
    return matrix


def _sym2_matrix(matrix: np.ndarray) -> np.ndarray:
    basis = [(i, j) for i in range(4) for j in range(i, 4)]
    result = np.zeros((10, 10), dtype=float)
    for column, (i, j) in enumerate(basis):
        source = np.zeros((4, 4), dtype=float)
        source[i, j] += 1.0
        source[j, i] += 1.0 if i != j else 0.0
        image = matrix @ source @ matrix.T
        for row, (a, b) in enumerate(basis):
            result[row, column] = image[a, b]
    return result


def _wedge2_matrix(matrix: np.ndarray) -> np.ndarray:
    basis = [(i, j) for i in range(4) for j in range(i + 1, 4)]
    result = np.zeros((6, 6), dtype=float)
    for column, (i, j) in enumerate(basis):
        image_i = np.argmax(matrix[:, i])
        image_j = np.argmax(matrix[:, j])
        a, b = sorted((image_i, image_j))
        sign = 1.0 if (image_i, image_j) == (a, b) else -1.0
        row = basis.index((a, b))
        result[row, column] = sign
    return result


def _character_by_class(representation_builder) -> list[int]:
    traces: dict[str, list[int]] = {class_name: [] for class_name in CLASS_ORDER}
    for perm in itertools.permutations(range(4)):
        class_name = _cycle_type(perm)
        matrix = _permutation_matrix(perm)
        representation = representation_builder(matrix)
        traces[class_name].append(int(round(float(np.trace(representation)))))
    return [traces[class_name][0] for class_name in CLASS_ORDER]


def _decompose(character: list[int]) -> dict[str, int]:
    multiplicities: dict[str, int] = {}
    group_order = 24
    for irrep_name, irrep_character in IRREP_CHARACTERS.items():
        inner = sum(
            CLASS_SIZES[class_name] * char_value * irrep_value
            for class_name, char_value, irrep_value in zip(CLASS_ORDER, character, irrep_character)
        ) / group_order
        multiplicities[irrep_name] = int(round(inner))
    return {name: mult for name, mult in multiplicities.items() if mult}


def build_summary() -> dict[str, Any]:
    golden = _load_json("w33_golden_tetra_clifford_refinement_bridge_summary.json")
    double_spin = _load_json("w33_double_spin16_clifford_bridge_summary.json")

    perm_character = _character_by_class(lambda matrix: matrix)
    sym2_character = _character_by_class(_sym2_matrix)
    wedge2_character = _character_by_class(_wedge2_matrix)

    perm_decomp = _decompose(perm_character)
    sym2_decomp = _decompose(sym2_character)
    wedge2_decomp = _decompose(wedge2_character)

    spin16_refinement = {
        "1": sym2_decomp.get("1", 0) + wedge2_decomp.get("1", 0),
        "1'": sym2_decomp.get("1'", 0) + wedge2_decomp.get("1'", 0),
        "2": sym2_decomp.get("2", 0) + wedge2_decomp.get("2", 0),
        "3": sym2_decomp.get("3", 0) + wedge2_decomp.get("3", 0),
        "3'": sym2_decomp.get("3'", 0) + wedge2_decomp.get("3'", 0),
    }

    return {
        "s4_dictionary": {
            "class_order": list(CLASS_ORDER),
            "class_sizes": CLASS_SIZES,
            "irrep_characters": IRREP_CHARACTERS,
        },
        "tetra_carrier_representation": {
            "character": perm_character,
            "decomposition": perm_decomp,
            "golden_split": golden["tetra_carrier_dictionary"]["split"],
        },
        "spin10_sized_packets": {
            "sym2_character": sym2_character,
            "sym2_decomposition": sym2_decomp,
            "wedge2_character": wedge2_character,
            "wedge2_decomposition": wedge2_decomp,
            "combined_spin16_refinement": spin16_refinement,
        },
        "w33_dictionary": {
            "double_spin16_packets": double_spin["two_spin16_packets"],
            "operator_collapse": double_spin["tetra_clifford_dictionary"]["operator_collapse"],
            "golden_kernel_closed_form": golden["golden_kernel_line"]["closed_form"],
        },
        "s4_tetra_spin10_refinement_theorem": {
            "the_tetra_carrier_is_exactly_the_permutation_representation_4_equals_1_plus_3": bool(
                perm_decomp == {"1": 1, "3": 1}
            ),
            "the_spin10_sized_symmetric_packet_refines_as_1_plus_1_plus_2_plus_3_plus_3": bool(
                sym2_decomp == {"1": 2, "2": 1, "3": 2}
            ),
            "the_bivector_packet_refines_as_3_plus_3prime": bool(
                wedge2_decomp == {"3": 1, "3'": 1}
            ),
            "the_full_spin16_packet_refines_as_1_plus_1_plus_2_plus_3_plus_3_plus_3_plus_3prime": bool(
                spin16_refinement == {"1": 2, "1'": 0, "2": 1, "3": 3, "3'": 1}
            ),
            "the_only_new_nontrivial_residue_beyond_singlets_and_triplets_is_the_canonical_tetra_doublet": bool(
                sym2_decomp.get("2", 0) == 1 and wedge2_decomp.get("2", 0) == 0
            ),
        },
        "interpretation": (
            "The exact tetra carrier now has a genuine S4 refinement, not just a "
            "dimension match. Under the tetrahedral permutation symmetry, the 4 "
            "carrier is 1+3, the symmetric Spin(10)-sized packet is 1+1+2+3+3, "
            "and the bivector packet is 3+3'. So the refined 16 is "
            "1+1+2+3+3+3+3'. The key new object is the canonical tetrahedral "
            "doublet 2 inside Sym^2(4). If a real middle-versus-outer asymmetry "
            "survives the current cleanup, this is the first honest place it can live."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["s4_tetra_spin10_refinement_theorem"], indent=2))


if __name__ == "__main__":
    main()
