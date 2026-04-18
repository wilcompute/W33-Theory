"""The moonshine package is exact through V4, with the first real boundary at V5.

The first four graded Monster pieces are controlled by the exact classical
decompositions

    V1 = 1 ⊕ 196883,
    V2 = 1 ⊕ 196883 ⊕ 21296876,
    V3 = 2·1 ⊕ 2·196883 ⊕ 21296876 ⊕ 842609326,
    V4 = 2·1 ⊕ 3·196883 ⊕ 2·21296876 ⊕ 842609326 ⊕ 19360062527.

Hence the quartic character is forced by the first four moonshine coefficients:

    χ_196883        = V1 - 1,
    χ_21296876      = V2 - V1,
    χ_842609326     = V3 - V2 - V1,
    χ_19360062527   = V4 - V3 - V2 + 1.

Unlike the earlier head package, the next quintic layer is not uniformly safe:
the degree-only decomposition currently used in the monster script already
fails against bundled CTblLib character data at 2A and 2B.  So the honest
exact boundary of the presently validated graded package is V4.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_moonshine_v4_boundary_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import (
    analyze_monster_moonshine_power_closure,
    load_monster_ctbllib_charcols,
    mckay_thompson_series,
)


INTEGER_CLASS_ORDER = [
    "1A",
    "2A",
    "2B",
    "3A",
    "3B",
    "3C",
    "5A",
    "5B",
    "7A",
    "7B",
    "11A",
    "13A",
    "13B",
    "17A",
    "19A",
    "29A",
    "41A",
]

HEAD4_DEGREES = [196883, 21296876, 842609326, 19360062527]
HEAD5_DEGREES = [196883, 21296876, 842609326, 19360062527, 293553734298]


def exact_v4_package_from_series(class_name: str) -> dict[str, int]:
    series = mckay_thompson_series(class_name, max_q_exp=4)
    if series is None:
        raise RuntimeError(f"Moonshine series unavailable for {class_name}")
    return {f"V{n}": int(series.get(n, 0)) for n in range(1, 5)}


def exact_chi4_from_series(class_name: str) -> int:
    package = exact_v4_package_from_series(class_name)
    return package["V4"] - package["V3"] - package["V2"] + 1


def naive_chi5_from_series(class_name: str) -> int:
    series = mckay_thompson_series(class_name, max_q_exp=5)
    if series is None:
        raise RuntimeError(f"Moonshine series unavailable for {class_name}")
    v1 = int(series.get(1, 0))
    v2 = int(series.get(2, 0))
    v3 = int(series.get(3, 0))
    v4 = int(series.get(4, 0))
    v5 = int(series.get(5, 0))
    chi1 = v1 - 1
    chi2 = v2 - v1
    chi3 = v3 - v2 - v1
    chi4 = v4 - v3 - v2 + 1
    return v5 - (3 + 5 * chi1 + 4 * chi2 + chi3 + 2 * chi4)


def _ctbllib_character(cols: dict[str, Any], class_name: str, degree: int) -> int:
    row = next(r for r in cols["irreps"] if int(r["deg"]) == degree)
    if class_name == "1A":
        return int(row["deg"])
    return int(row[class_name])


def build_summary(max_q_exp: int = 24) -> dict[str, Any]:
    cols = load_monster_ctbllib_charcols()
    if cols is None:
        raise RuntimeError("Bundled Monster CTblLib character subset unavailable")

    closure = analyze_monster_moonshine_power_closure(max_q_exp=max_q_exp)
    supported_classes = [str(cls) for cls in closure["supported_classes"]]

    supported_rows = []
    for cls in supported_classes:
        package = exact_v4_package_from_series(cls)
        supported_rows.append(
            {
                "class_name": cls,
                "package": package,
                "chi_19360062527": package["V4"] - package["V3"] - package["V2"] + 1,
            }
        )

    anchored_v4_rows = []
    anchored_v5_boundary_rows = []
    for cls in INTEGER_CLASS_ORDER:
        package = exact_v4_package_from_series(cls)
        actual_chi4 = _ctbllib_character(cols, cls, 19360062527)
        inferred_chi4 = package["V4"] - package["V3"] - package["V2"] + 1
        anchored_v4_rows.append(
            {
                "class_name": cls,
                "package": package,
                "inferred_chi_19360062527": inferred_chi4,
                "actual_chi_19360062527": actual_chi4,
                "chi4_match": inferred_chi4 == actual_chi4,
            }
        )

        actual_chi5 = _ctbllib_character(cols, cls, 293553734298)
        naive_chi5 = naive_chi5_from_series(cls)
        anchored_v5_boundary_rows.append(
            {
                "class_name": cls,
                "naive_chi_293553734298": naive_chi5,
                "actual_chi_293553734298": actual_chi5,
                "chi5_match": naive_chi5 == actual_chi5,
                "difference": naive_chi5 - actual_chi5,
            }
        )

    distinct_packages = {
        tuple(int(row["package"][f"V{n}"]) for n in range(1, 5)) for row in supported_rows
    }

    atlas_edge_rows = []
    exponent_by_kind = {"square": 2, "cube": 3, "fifth": 5}
    for kind, exponent in exponent_by_kind.items():
        for source, info in sorted(closure["atlas_validation"][kind].items()):
            if info["atlas_targets"] is None:
                continue
            target = str(info["inferred"])
            source_row = next(row for row in supported_rows if row["class_name"] == str(source))
            target_row = next(row for row in supported_rows if row["class_name"] == target)
            atlas_edge_rows.append(
                {
                    "source": str(source),
                    "exponent": exponent,
                    "target": target,
                    "source_package": source_row["package"],
                    "target_package": target_row["package"],
                    "matches_atlas": bool(info["matches"]),
                }
            )

    theorem = {
        "all_17_ctbllib_anchored_classes_match_the_exact_quartic_character_formula": (
            all(row["chi4_match"] for row in anchored_v4_rows)
        ),
        "the_v1_v2_v3_v4_package_separates_all_32_supported_seed_classes": (
            len(supported_rows) == 32 and len(distinct_packages) == 32
        ),
        "all_35_atlas_available_prime_power_edges_land_inside_the_same_v4_package_dictionary": (
            len(atlas_edge_rows) == 35 and all(row["matches_atlas"] for row in atlas_edge_rows)
        ),
        "the_exceptional_affine_node_3c_has_sparse_quartic_package_0_248_0_0": (
            next(row for row in supported_rows if row["class_name"] == "3C")["package"]
            == {"V1": 0, "V2": 248, "V3": 0, "V4": 0}
        ),
        "the_pair_8a_8aprime_has_equal_odd_packages_and_opposite_even_packages": (
            next(row for row in supported_rows if row["class_name"] == "8A")["package"]
            == {"V1": 36, "V2": 128, "V3": 386, "V4": 1024}
            and next(row for row in supported_rows if row["class_name"] == "8A'")["package"]
            == {"V1": 36, "V2": -128, "V3": 386, "V4": -1024}
        ),
        "the_naive_quintic_lift_already_fails_on_the_anchored_subset": (
            any(not row["chi5_match"] for row in anchored_v5_boundary_rows)
            and {row["class_name"] for row in anchored_v5_boundary_rows if not row["chi5_match"]} == {"2A", "2B"}
        ),
        "the_honest_exact_graded_package_boundary_is_therefore_v4": (
            all(row["chi4_match"] for row in anchored_v4_rows)
            and any(not row["chi5_match"] for row in anchored_v5_boundary_rows)
        ),
    }
    theorem["the_moonshine_v4_boundary_bridge_is_fully_closed"] = all(theorem.values())

    return {
        "moonshine_v4_boundary_dictionary": {
            "supported_rows": supported_rows,
            "distinct_package_count": len(distinct_packages),
            "anchored_v4_rows": anchored_v4_rows,
            "anchored_v5_boundary_rows": anchored_v5_boundary_rows,
            "atlas_edge_rows": atlas_edge_rows,
        },
        "moonshine_v4_boundary_theorem": theorem,
        "interpretation": (
            "The graded moonshine package is now pinned exactly through V4. "
            "The quartic character formula agrees with bundled Monster data on "
            "the full anchored subset, the supported 32-node seed closes on one "
            "finite V1⊕V2⊕V3⊕V4 package dictionary, and the first honest failure "
            "of the naive higher lift appears immediately at V5 on 2A and 2B. "
            "So V4 is the current exact boundary."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 MOONSHINE V4 BOUNDARY BRIDGE")
    print("=" * 72)
    for key, value in summary["moonshine_v4_boundary_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
