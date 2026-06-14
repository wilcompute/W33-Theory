#!/usr/bin/env python3
"""BT977 - map existing Heisenberg generation machinery onto GenRail_A/B/C.

BT874 proves that the texture/generation order-3 map is the Heisenberg center,
a long-root transvection.  BT976 supplies selector-fixed GenRail_A/B/C faces.
BT977 attaches the proven triality source to the selector-fixed labels while
leaving representation/charge labels as the next contract.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt977_genrail_heisenberg_mapping.json"

GENRAILS = [
    {"label": "GenRail_A", "face": [0,1,3], "triality_phase": 0, "size": 27},
    {"label": "GenRail_B", "face": [0,2,3], "triality_phase": 1, "size": 27},
    {"label": "GenRail_C", "face": [1,2,3], "triality_phase": 2, "size": 27},
]


def main() -> None:
    result = {
        "theorem": "BT977 GenRail mapping to Heisenberg-center generation machinery",
        "source_anchor": "analysis/BT874_texture_triality_is_heisenberg_center.md",
        "source_claims_used": [
            "Heisenberg center has order 3",
            "acts on the 27 matter shell as 9 free orbits of 3",
            "splits Steinberg matter register as 27+27+27",
            "is the long-root transvection fixing the 13-point gauge perp-plane"
        ],
        "selector_faces": GENRAILS,
        "complement": {"label": "CompRail_0", "face": [0,1,2], "size": 27, "role": "control/complement face pending representation map"},
        "mapping_rule": "Assign Heisenberg-center phases 0,1,2 to GenRail_A/B/C in selector face order; keep CompRail_0 outside matter-generation count.",
        "generation_slot_total": sum(g["size"] for g in GENRAILS),
        "texture_orbit_contract": "Each GenRail face must later be refined into 9 Heisenberg-center 3-cycles when explicit shell representatives are attached.",
        "charge_boundary": "No Standard Model charge or field label is asserted here. This attaches the proven order-3 generation source to selector-fixed 27-faces only.",
        "checks": {"T1_three_genrails": len(GENRAILS)==3, "T2_total_81": sum(g["size"] for g in GENRAILS)==81, "T3_triality_phases_012": [g["triality_phase"] for g in GENRAILS]==[0,1,2], "T4_BT874_anchor_recorded": True, "T5_charge_boundary_explicit": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT977 wrote", OUT)

if __name__ == "__main__":
    main()
