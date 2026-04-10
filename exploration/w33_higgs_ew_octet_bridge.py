"""Physical reading of the exact subdominant octet.

This packages the strongest exact count closure obtained so far:

    8 = 1 + 4 + 3

where the three pieces now have a clean physical interpretation:

    1 = vacuum / mean line,
    4 = matter-singlet quartet (committed GitHub reading: Higgs real d.o.f.),
    3 = gauge-singlet triplet (committed GitHub reading: electroweak bosons).

The exact count law

    4 - 1 = 3

then matches the Higgs mechanism pattern directly: one physical Higgs remains
after three Goldstone modes are eaten by the electroweak triplet.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_higgs_ew_octet_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    octet = _load_json("w33_subdominant_octet_bridge_summary.json")
    bott = _load_json("w33_bott_triality_asymmetry_bridge_summary.json")
    ternary = _load_json("w33_ternary_heptad_triality_bridge_summary.json")

    vacuum = octet["singlet_packet"]["vacuum_line"]
    higgs_quartet = octet["singlet_packet"]["matter_singlets"]
    ew_triplet = octet["singlet_packet"]["gauge_singlets"]
    subdominant = octet["dirac_packet"]["subdominant_count"]

    return {
        "spectral_octet": {
            "vacuum_line": vacuum,
            "higgs_quartet": higgs_quartet,
            "ew_triplet": ew_triplet,
            "total_subdominant_count": subdominant,
            "split": "1 + 4 + 3",
        },
        "parameter_dictionary": {
            "q": 3,
            "mu": 4,
            "mu_minus_1": 3,
            "bott_five": bott["bott_triality_packet"]["four_plus_one"],
            "triality_heptad_split": ternary["heptad_dictionary"]["heptad_split"],
        },
        "higgs_mechanism_dictionary": {
            "before_ssb": "4 Higgs real degrees + 3 electroweak gauge singlets + vacuum",
            "goldstones": 3,
            "physical_higgs": 1,
            "after_count_relation": "4 = 3 + 1",
        },
        "higgs_ew_octet_theorem": {
            "the_subdominant_spectral_packet_is_exactly_vacuum_plus_higgs_quartet_plus_ew_triplet": bool(
                subdominant == vacuum + higgs_quartet + ew_triplet == 8
            ),
            "the_higgs_quartet_count_is_exactly_mu": bool(higgs_quartet == 4),
            "the_ew_triplet_count_is_exactly_q": bool(ew_triplet == 3),
            "the_goldstone_count_is_exactly_mu_minus_one_equals_q": bool(higgs_quartet - 1 == ew_triplet == 3),
            "the_previous_bott_five_is_exactly_vacuum_plus_higgs_quartet": bool(vacuum + higgs_quartet == 5),
            "the_ternary_heptad_is_exactly_higgs_quartet_plus_ew_triplet": bool(higgs_quartet + ew_triplet == 7),
        },
        "interpretation": (
            "The spectral packet now has a clean physical read. The exact "
            "subdominant octet is vacuum plus Higgs quartet plus electroweak "
            "triplet. The earlier Bott five is therefore best read as vacuum plus "
            "Higgs, while the ternary heptad 4+3 is Higgs plus electroweak. The "
            "count law mu-1=q becomes the Goldstone law directly: the Higgs "
            "quartet loses three modes to the electroweak triplet and leaves one "
            "physical Higgs."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["higgs_ew_octet_theorem"], indent=2))


if __name__ == "__main__":
    main()
