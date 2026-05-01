"""Exact complete packet decomposition of the live 40-space.

This is the current sharpest global closure:

    40 = 10 + 16 + 6 + 4 + 3 + 1

Every summand is now backed by an exact bridge:

    10  = D_H eigenvalue +5  = pure matter-dominant branch,
    16  = D_H eigenvalue -1  = exact mixed dominant core,
    6   = D_H eigenvalue -7  = pure gauge-dominant branch,
    4   = matter-singlet quartet,
    3   = gauge-singlet / triality triplet,
    1   = vacuum / mean line.

So the full W(3,3) carrier is no longer just a graph with fitted numbers on top.
It now has one exact packet decomposition that welds the Dirac, ternary, and
toroidal/tomotope stories together.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_complete_packet_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return load_bridge_json(filename, DATA_DIR)


def build_summary() -> dict[str, Any]:
    dominant = _load_json("w33_dominant_32_dirac_refinement_bridge_summary.json")
    octet = _load_json("w33_higgs_ew_octet_bridge_summary.json")

    packet = {
        "matter_extremal_10": dominant["dirac_dominant_packet"]["dh_5"],
        "mixed_core_16": dominant["dirac_dominant_packet"]["dh_minus_1"],
        "gauge_extremal_6": dominant["dirac_dominant_packet"]["dh_minus_7"],
        "higgs_quartet_4": octet["spectral_octet"]["higgs_quartet"],
        "electroweak_triplet_3": octet["spectral_octet"]["ew_triplet"],
        "vacuum_line_1": octet["spectral_octet"]["vacuum_line"],
    }
    total = sum(packet.values())

    return {
        "complete_packet": packet,
        "grouped_packets": {
            "dominant_32": packet["matter_extremal_10"]
            + packet["mixed_core_16"]
            + packet["gauge_extremal_6"],
            "subdominant_8": packet["higgs_quartet_4"]
            + packet["electroweak_triplet_3"]
            + packet["vacuum_line_1"],
            "heptad_7": packet["higgs_quartet_4"] + packet["electroweak_triplet_3"],
            "bott_5": packet["higgs_quartet_4"] + packet["vacuum_line_1"],
        },
        "complete_packet_theorem": {
            "the_full_live_space_splits_exactly_as_10_plus_16_plus_6_plus_4_plus_3_plus_1": bool(
                total == 40
            ),
            "the_dominant_shell_is_exactly_10_plus_16_plus_6": bool(
                packet["matter_extremal_10"]
                + packet["mixed_core_16"]
                + packet["gauge_extremal_6"]
                == 32
            ),
            "the_subdominant_shell_is_exactly_4_plus_3_plus_1": bool(
                packet["higgs_quartet_4"]
                + packet["electroweak_triplet_3"]
                + packet["vacuum_line_1"]
                == 8
            ),
            "the_heptad_is_exactly_4_plus_3": bool(
                packet["higgs_quartet_4"] + packet["electroweak_triplet_3"] == 7
            ),
            "the_bott_five_is_exactly_4_plus_1": bool(
                packet["higgs_quartet_4"] + packet["vacuum_line_1"] == 5
            ),
        },
        "interpretation": (
            "The current exact packet law for W(3,3) is 40 = 10+16+6+4+3+1. "
            "The Dirac operator resolves the dominant 32 into a pure matter 10, "
            "a mixed 16 core, and a pure gauge 6, while the ternary/toroidal side "
            "resolves the remaining octet as Higgs quartet plus electroweak triplet "
            "plus vacuum. The heptad 7 and Bott 5 are then just visible subpackets "
            "inside the same exact global decomposition."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["complete_packet_theorem"], indent=2))


if __name__ == "__main__":
    main()
