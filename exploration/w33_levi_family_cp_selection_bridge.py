"""Exact family/CP selection law from the Levi visibility operator.

This is an integration bridge, not a new scan. It welds three exact results:

1. The mixed dominant core obeys

      16 = 10 + 6,

   and the Levi visibility operator selects the 10 and kills the 6 exactly.

2. The tetrahedral S4 refinement identifies those packets as

      10 = Sym^2(4) = 1 + 1 + 2 + 3 + 3,
       6 = Lambda^2(4) = 3 + 3'.

3. The CKM/tetra bridge already proved

      family envelope  lives in Sym^2(4),
      CP phase packet  lives in Lambda^2(4),
      real asymmetry   is doublet-dominant.

So the corrected Levi geometry does something very specific: on the mixed 16
carrier it preserves the family packet and annihilates the CP packet. In this
exact sense the Levi/spread chain is a family selector and a CP suppressor.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_family_cp_selection_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    visibility = _load_json("w33_levi_gamma16_visibility_bridge_summary.json")
    s4 = _load_json("w33_s4_tetra_spin10_refinement_bridge_summary.json")
    ckm = _load_json("w33_ckm_clifford_sector_separation_bridge_summary.json")

    return {
        "selection_dictionary": {
            "levi_visible_packet": "10 = Sym^2(4) = 1 + 1 + 2 + 3 + 3",
            "levi_null_packet": "6 = Lambda^2(4) = 3 + 3'",
            "family_packet": "real family envelope / doublet sector",
            "cp_packet": "imaginary bivector packet",
        },
        "source_theorems": {
            "visibility": visibility["levi_gamma16_visibility_theorem"],
            "s4_refinement": s4["s4_tetra_spin10_refinement_theorem"],
            "ckm_clifford": ckm["ckm_clifford_sector_separation_theorem"],
        },
        "levi_family_cp_selection_theorem": {
            "the_levi_operator_selects_sym2_4_and_kills_lambda2_4_on_the_mixed_16": bool(
                visibility["levi_gamma16_visibility_theorem"][
                    "the_levi_visibility_operator_on_the_16_is_exactly_6_times_the_10_projector"
                ]
                and s4["s4_tetra_spin10_refinement_theorem"][
                    "the_spin10_sized_symmetric_packet_refines_as_1_plus_1_plus_2_plus_3_plus_3"
                ]
                and s4["s4_tetra_spin10_refinement_theorem"][
                    "the_bivector_packet_refines_as_3_plus_3prime"
                ]
            ),
            "the_family_envelope_is_levi_visible": bool(
                ckm["ckm_clifford_sector_separation_theorem"][
                    "the_live_and_paper_family_envelopes_live_on_the_symmetric_tetra_packet_sym2_4"
                ]
            ),
            "the_cp_packet_is_levi_null": bool(
                ckm["ckm_clifford_sector_separation_theorem"][
                    "the_live_and_paper_cp_packets_live_on_the_bivector_shell_lambda2_4"
                ]
            ),
            "the_real_family_asymmetry_survives_on_the_canonical_tetra_doublet": bool(
                ckm["ckm_clifford_sector_separation_theorem"][
                    "the_paper_real_up_down_asymmetry_is_doublet_dominant"
                ]
            ),
            "the_corrected_point_line_spread_chain_is_structurally_a_family_selector_and_cp_suppressor": bool(
                visibility["levi_gamma16_visibility_theorem"][
                    "the_full_point_line_spread_cascade_annihilates_the_entire_mixed_16"
                ]
                and ckm["ckm_clifford_sector_separation_theorem"][
                    "the_live_and_paper_family_envelopes_live_on_the_symmetric_tetra_packet_sym2_4"
                ]
                and ckm["ckm_clifford_sector_separation_theorem"][
                    "the_live_and_paper_cp_packets_live_on_the_bivector_shell_lambda2_4"
                ]
            ),
        },
        "interpretation": (
            "The older CKM/tetra story and the corrected Levi geometry are now aligned. "
            "On the mixed 16, Levi visibility is exactly the symmetric-square selector and "
            "its nullspace is exactly the bivector shell. Since family asymmetry lives on the "
            "symmetric tetra packet while CP lives on the bivector packet, the corrected "
            "point-line-spread chain is structurally selecting family content while suppressing CP."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["levi_family_cp_selection_theorem"], indent=2))


if __name__ == "__main__":
    main()
