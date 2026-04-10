"""Restriction of the tetrahedral S4 packet to the triality/family S3.

The previous bridge showed that the tetrahedral Spin(10)-sized packet refines
under S4 as

    Sym^2(4)   = 1 + 1 + 2 + 3 + 3,
    Lambda^2(4)= 3 + 3'.

The current question is whether the new tetrahedral doublet ``2`` is genuinely
the same family doublet already isolated on the triality/qutrit carrier.

The natural subgroup is the stabilizer of one tetra vertex:

    S3 < S4.

Restricting the S4 irreps to that S3 gives the exact bridge:

    1   ↓ S3 = 1,
    1'  ↓ S3 = 1',
    2   ↓ S3 = 2,
    3   ↓ S3 = 1 + 2,
    3'  ↓ S3 = 1' + 2.

So the tetrahedral doublet is *literally* the same irreducible family doublet
already seen on the triality side.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_s4_s3_family_doublet_bridge_summary.json"


S3_IRREPS: dict[str, list[int]] = {
    "1": [1, 1, 1],
    "1'": [1, -1, 1],
    "2": [2, 0, -1],
}


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _restrict_s4_character_to_s3(character: list[int]) -> list[int]:
    # S4 class order from the upstream bridge:
    #   1^4, 2 1^2, 2^2, 3 1, 4
    # Restrict to the stabilizer S3 class order:
    #   identity, transposition, 3-cycle
    return [character[0], character[1], character[3]]


def _decompose_s3(character: list[int]) -> dict[str, int]:
    class_sizes = [1, 3, 2]
    group_order = 6
    multiplicities: dict[str, int] = {}
    for irrep_name, irrep_character in S3_IRREPS.items():
        inner = sum(size * value * target for size, value, target in zip(class_sizes, character, irrep_character)) / group_order
        multiplicities[irrep_name] = int(round(inner))
    return {name: mult for name, mult in multiplicities.items() if mult}


def build_summary() -> dict[str, Any]:
    s4 = _load_json("w33_s4_tetra_spin10_refinement_bridge_summary.json")
    family = _load_json("w33_triality_family_flag_bridge_summary.json")

    s4_irreps = s4["s4_dictionary"]["irrep_characters"]
    restricted = {name: _restrict_s4_character_to_s3(character) for name, character in s4_irreps.items()}
    decompositions = {name: _decompose_s3(character) for name, character in restricted.items()}

    return {
        "triality_s3_dictionary": {
            "class_order": ["identity", "transposition", "three_cycle"],
            "irrep_characters": S3_IRREPS,
            "family_trace_packet": family["character_packet"]["trace_values"],
        },
        "restricted_characters": restricted,
        "restriction_decompositions": decompositions,
        "s4_s3_family_doublet_theorem": {
            "the_tetrahedral_doublet_restricts_to_the_irreducible_family_doublet": bool(
                decompositions["2"] == {"2": 1}
            ),
            "the_standard_tetra_triplet_restricts_to_the_old_real_family_flag_one_plus_two": bool(
                decompositions["3"] == {"1": 1, "2": 1}
            ),
            "the_twisted_tetra_triplet_restricts_to_the_signed_family_flag_oneprime_plus_two": bool(
                decompositions["3'"] == {"1'": 1, "2": 1}
            ),
            "the_repo_triality_family_packet_is_exactly_the_same_s3_character_one_plus_two": bool(
                family["triality_family_flag_theorem"]["the_triality_character_is_exactly_the_real_one_plus_two_family_flag"]
                and restricted["3"] == [3, 1, 0]
            ),
            "the_new_s4_doublet_is_the_cleanest_current_home_for_middle_vs_outer_family_asymmetry": bool(
                decompositions["2"] == {"2": 1} and restricted["2"] == [2, 0, -1]
            ),
        },
        "interpretation": (
            "The tetrahedral and triality stories have now met at the irreducible level. "
            "The new S4 doublet inside Sym^2(4) is not merely analogous to the old family "
            "doublet; when restricted to the natural vertex-stabilizer S3, it is exactly the "
            "same irreducible 2. So the tetra/Clifford refinement has produced an honest home "
            "for the one-vs-two family split rather than another free parameter."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["s4_s3_family_doublet_theorem"], indent=2))


if __name__ == "__main__":
    main()
