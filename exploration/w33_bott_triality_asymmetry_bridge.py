"""Asymmetry packet as the q=3 Bott/triality octet.

This bridge ties together three independent exact count packages already proved
locally:

1. The repaired down-asymmetry theorem:
      up numerator      = 3,
      down correction   = 5 = 4 + 1.
2. The mod-12 packet selector:
      admissible packet = {0, 3, 4, 7},
      with 3 = mode count, 4 = chart count, 7 = heptad count.
3. The toroidal heptad projector packet:
      centered heptad   = 4 + 1 + 1,
      where 4 is the Csaszar centered shell and 1 is the Szilassi centered shell.

The cheeky but exact closure is:

    3 (triality modes)  +  5 (toroidal 4+1 internal packet)  =  8 = 2^q.

So the real up/down asymmetry slots naturally into the q=3 Bott/triality octet:
the upstairs piece is the triality triplet, while the downstairs correction is
the toroidal internal 4+1 packet.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_bott_triality_asymmetry_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    asymmetry = _load_json("w33_down_asymmetry_projector_bridge_summary.json")
    mod12 = _load_json("w33_mod12_packet_selector_bridge_summary.json")
    heptad = _load_json("w33_toroidal_heptad_projector_bridge_summary.json")

    up_numerator = asymmetry["closure_label_matrix"]["a_count"]
    correction_numerator = asymmetry["closure_label_matrix"]["non_a_nonzero_count"]
    mode_count = mod12["packet_counts"]["mode_count"]
    chart_count = mod12["packet_counts"]["chart_count"]
    heptad_count = mod12["packet_counts"]["heptad_count"]
    csaszar_centered = heptad["projector_heptad"]["csaszar_centered_rank"]
    szilassi_centered = heptad["projector_heptad"]["szilassi_centered_rank"]
    family_separation = heptad["projector_heptad"]["family_separation_rank"]
    q = int(asymmetry["count_dictionary"]["q"])
    bott_octet = 2**q

    return {
        "asymmetry_packet": {
            "up_numerator": up_numerator,
            "down_correction_numerator": correction_numerator,
        },
        "mod12_packet": {
            "mode_count": mode_count,
            "chart_count": chart_count,
            "heptad_count": heptad_count,
        },
        "toroidal_heptad_packet": {
            "csaszar_centered_rank": csaszar_centered,
            "szilassi_centered_rank": szilassi_centered,
            "family_separation_rank": family_separation,
            "centered_four_plus_one_plus_one_rank": heptad["projector_heptad"]["centered_4_plus_1_plus_1_rank"],
        },
        "bott_triality_packet": {
            "q": q,
            "two_to_the_q": bott_octet,
            "three_plus_five": up_numerator + correction_numerator,
            "three_plus_four": mode_count + chart_count,
            "four_plus_one": csaszar_centered + szilassi_centered,
        },
        "bott_triality_asymmetry_theorem": {
            "the_up_numerator_is_exactly_the_mod12_triality_mode_count": (
                up_numerator == mode_count == 3
            ),
            "the_down_correction_is_exactly_the_toroidal_internal_four_plus_one_packet": (
                correction_numerator == csaszar_centered + szilassi_centered == 5
            ),
            "the_mod12_heptad_packet_is_exactly_three_plus_four": (
                heptad_count == mode_count + chart_count == 7
            ),
            "the_real_asymmetry_packet_closes_to_the_q_equals_3_bott_octet": (
                up_numerator + correction_numerator == bott_octet == 8
            ),
            "the_remaining_plus_one_in_the_centered_heptad_is_the_family_separation_mode": (
                heptad["projector_heptad"]["centered_4_plus_1_plus_1_rank"]
                == csaszar_centered + szilassi_centered + family_separation
            ),
        },
        "interpretation": (
            "The real up/down asymmetry is now tied into the toroidal/tetrahedral "
            "packet rather than floating as an isolated rational mismatch. The "
            "upstairs numerator 3 is the same exact mode/triality count selected by "
            "the mod-12 genus law, the downstairs correction 5 is the toroidal "
            "internal 4+1 packet from the heptad projector bridge, and together they "
            "form the q=3 Bott octet 8 = 2^q. The leftover +1 in the centered heptad "
            "is the family-separation mode, so the heptad still refines as 4+1+1 "
            "while the asymmetry uses only the internal 4+1 part."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["bott_triality_asymmetry_theorem"], indent=2))


if __name__ == "__main__":
    main()
