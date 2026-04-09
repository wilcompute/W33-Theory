"""Leptonic-first six-scale scaffold from the clean Higgs pair.

This module combines two exact pieces already established:

  1. the clean Higgs sector is exactly the pair H_2, Hbar_2, and both slots
     support only the two leptonic channels
         L_1 <-> nu_c,   L_2 <-> e_c;
  2. the selector-side hyperbolic 3U packet supplies three exact heavy/light
     family pairs.

Consequently the current exact bridge data support a native three-family,
two-channel leptonic scaffold before any quark-sector promotion is added.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from exploration.w33_fermionic_connes_sector import build_clean_higgs_geometry_summary


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_leptonic_six_scale_bridge_summary.json"


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_leptonic_six_scale_summary() -> dict[str, Any]:
    higgs = build_clean_higgs_geometry_summary()
    seesaw = _read_json("w33_three_family_seesaw_bridge_summary.json")

    clean_support = {
        slot: [
            (entry["left_slot"], entry["right_slot"], entry["value"])
            for entry in higgs["yukawa_support"][slot]
        ]
        for slot in higgs["clean_higgs_slots"]
    }

    return {
        "status": "ok",
        "clean_higgs_slots": higgs["clean_higgs_slots"],
        "clean_higgs_support": clean_support,
        "family_pairs": seesaw["family_pairs"],
        "family_orderings": seesaw["orderings"],
        "leptonic_six_scale_theorem": {
            "clean_higgs_pair_is_exactly_leptonic": bool(
                higgs["geometry_theorem"]["clean_pair_support_is_exactly_leptonic"]
            ),
            "three_exact_family_pairs_are_available": bool(
                seesaw["three_family_seesaw_theorem"]["three_exact_family_pairs_exist"]
            ),
            "current_exact_bridge_supports_three_family_two_channel_leptonic_scaffold": (
                higgs["geometry_theorem"]["clean_pair_support_is_exactly_leptonic"]
                and seesaw["three_family_seesaw_theorem"]["three_exact_family_pairs_exist"]
            ),
            "heavy_and_light_family_orderings_cross": bool(
                seesaw["three_family_seesaw_theorem"]["heavy_and_light_orderings_are_not_the_same"]
            ),
            "current_exact_clean_bridge_is_not_yet_quark_mass_scaffold": True,
        },
        "interpretive_read": (
            "Inference from the exact clean-Higgs and selector packets: the "
            "current rigid bridge naturally feeds a three-family leptonic "
            "two-channel system first. The quark side remains outside the clean "
            "bridge and should enter only through a later, less rigid layer."
        ),
        "bridge_verdict": (
            "The present exact bridge is leptonic first. The clean Higgs pair "
            "H_2, Hbar_2 acts only on the two leptonic channels L_1<->nu_c and "
            "L_2<->e_c, while the selector-side 3U packet supplies three exact "
            "family seesaw pairs. So the repo already contains a native "
            "three-family, two-channel leptonic six-scale scaffold. Because the "
            "heavy and light family orderings differ, the scaffold also carries "
            "a built-in crossed-order geometry. The quark hierarchy is not yet "
            "in this exact clean layer."
        ),
        "source_files": [
            "data/w33_three_family_seesaw_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_leptonic_six_scale_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
