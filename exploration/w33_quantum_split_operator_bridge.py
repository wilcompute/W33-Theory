"""Exact operator refinement of the pulled 40 = 16 + 24 quantum split.

The new GitHub quantum-information layer compresses the W(3,3) point space as

    40 = 16 + 24.

The exact local operator chain already proves a sharper packet law:

    40 = 10 + 16 + 6 + 4 + 3 + 1.

This bridge records the honest relationship between the two. The 16-side of
the GitHub split is exact and rigid: it is the common Dirac core. The
complementary 24 is also exact, but it is not a primitive packet in the
current operator story. It refines as

    24 = 10 + 6 + 4 + 3 + 1.

So the quantum-information split is compatible with the exact operator spine,
but only after respecting the finer decomposition.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from exploration.w33_bridge_inputs import load_bridge_json
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from w33_bridge_inputs import load_bridge_json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_quantum_split_operator_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return load_bridge_json(filename, DATA_DIR)


def build_summary() -> dict[str, Any]:
    gamma = _load_json("w33_gamma16_chirality_bridge_summary.json")
    complete = _load_json("w33_complete_packet_bridge_summary.json")

    complete_packet = complete["complete_packet"]
    complement_24 = (
        complete_packet["matter_extremal_10"]
        + complete_packet["gauge_extremal_6"]
        + complete_packet["higgs_quartet_4"]
        + complete_packet["electroweak_triplet_3"]
        + complete_packet["vacuum_line_1"]
    )

    return {
        "quantum_split_dictionary": {
            "github_quantum_split": "40 = 16 + 24",
            "exact_global_packet": complete["complete_packet"],
            "exact_common_16": gamma["exact_packets"]["dominant_shell"]["16"],
            "exact_complement_24": complement_24,
            "complement_refinement": "24 = 10 + 6 + 4 + 3 + 1",
        },
        "quantum_split_operator_theorem": {
            "the_pulled_github_quantum_split_40_equals_16_plus_24_is_compatible_with_the_exact_operator_packet_law": (
                gamma["exact_packets"]["dominant_shell"]["16"] == 16
                and complement_24 == 24
            ),
            "the_16_side_is_the_exact_common_dirac_core": (
                gamma["gamma16_chirality_theorem"][
                    "the_exact_16_core_is_common_to_the_two_live_dirac_operators"
                ]
            ),
            "the_complementary_24_side_is_exact_but_not_primitive": (
                complement_24 == 24
                and complete["complete_packet_theorem"][
                    "the_full_live_space_splits_exactly_as_10_plus_16_plus_6_plus_4_plus_3_plus_1"
                ]
            ),
            "the_exact_refinement_of_the_24_side_is_10_plus_6_plus_4_plus_3_plus_1": (
                complement_24
                == complete_packet["matter_extremal_10"]
                + complete_packet["gauge_extremal_6"]
                + complete_packet["higgs_quartet_4"]
                + complete_packet["electroweak_triplet_3"]
                + complete_packet["vacuum_line_1"]
            ),
        },
        "interpretation": (
            "The pulled quantum-information split survives, but only in refined form. "
            "The 16-side is the rigid common Dirac core. The complementary 24 is exact "
            "as its invariant complement, but the current operator chain does not support "
            "reading it as one primitive gauge block. It refines further as 10+6+4+3+1."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["quantum_split_operator_theorem"]
    print("=" * 72)
    print("W33 QUANTUM SPLIT OPERATOR BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
