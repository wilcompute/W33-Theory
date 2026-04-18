"""The first composite moonshine classes close on exact power-map spines.

The base moonshine bridges already fixed:

    1A  : linear quotient algebra,
    2A, 3A, 5A, 7A, 13A : prime trace/norm + prime replicability algebras.

The next exact layer is the first composite closure.  The classes

    4A, 6A, 8A, 10A

each sit on a finite power spine ending at 1A:

    4A  -> 2B -> 1A,
    6A  -> 3A and 2A -> 1A,
    8A  -> 4C -> 2B -> 1A,
    10A -> 5A and 2A -> 1A.

These are not heuristic identifications.  They are exactly the classes picked
out by the m=2 square-relation remainder and by the full divisor-sum
replicability relation for m equal to the class order.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_composite_moonshine_power_spine_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import (
    verify_replicability_relation,
    verify_square_power_relation,
)


COMPOSITE_CASES = [
    {
        "class_name": "4A",
        "order": 4,
        "square_expected": "2B",
        "square_candidates": ("2A", "2B"),
        "power_map": {2: "2B", 4: "1A"},
    },
    {
        "class_name": "6A",
        "order": 6,
        "square_expected": "3A",
        "square_candidates": ("2A", "2B", "3A", "3B", "3C"),
        "power_map": {2: "3A", 3: "2A", 6: "1A"},
    },
    {
        "class_name": "8A",
        "order": 8,
        "square_expected": "4C",
        "square_candidates": ("4A", "4B", "4C", "4D"),
        "power_map": {2: "4C", 4: "2B", 8: "1A"},
    },
    {
        "class_name": "10A",
        "order": 10,
        "square_expected": "5A",
        "square_candidates": ("5A", "5B"),
        "power_map": {2: "5A", 5: "2A", 10: "1A"},
    },
]


def _row(case: dict[str, Any], max_q_exp: int = 12) -> dict[str, Any]:
    class_name = case["class_name"]
    order = int(case["order"])

    square = verify_square_power_relation(
        class_name,
        expected_square_class=case["square_expected"],
        max_q_exp=24,
        candidates=case["square_candidates"],
    )
    composite = verify_replicability_relation(
        class_name,
        m=order,
        power_map=case["power_map"],
        max_q_exp=max_q_exp,
    )

    return {
        "class_name": class_name,
        "order": order,
        "square_expected": case["square_expected"],
        "square_inferred": square["inferred_power_class"],
        "power_map": dict(case["power_map"]),
        "square_target_mismatches": list(square["target_mismatches"]),
        "composite_replicability_mismatches": list(composite["mismatches"]),
        "theorems": {
            "square_map_is_exact": bool(square["verified"]),
            "square_map_inference_matches_expected": str(square["inferred_power_class"]) == str(case["square_expected"]),
            "full_order_replicability_is_exact": bool(composite["verified"]),
        },
    }


def build_summary(max_q_exp: int = 12) -> dict[str, Any]:
    rows = [_row(case, max_q_exp=max_q_exp) for case in COMPOSITE_CASES]

    return {
        "composite_moonshine_power_spine_dictionary": {
            "rows": rows,
        },
        "composite_moonshine_power_spine_theorem": {
            "4A_closes_on_the_power_spine_4A_to_2B_to_1A": all(
                rows[0]["theorems"].values()
            ),
            "6A_closes_on_the_power_spine_6A_to_3A_and_2A_to_1A": all(
                rows[1]["theorems"].values()
            ),
            "8A_closes_on_the_power_spine_8A_to_4C_to_2B_to_1A": all(
                rows[2]["theorems"].values()
            ),
            "10A_closes_on_the_power_spine_10A_to_5A_and_2A_to_1A": all(
                rows[3]["theorems"].values()
            ),
            "the_first_composite_classes_close_on_exact_power_map_spines_ending_at_1A": all(
                all(row["theorems"].values()) for row in rows
            ),
        },
        "interpretation": (
            "The first composite moonshine classes are not independent of the "
            "prime base classes. Their square remainders and full divisor-sum "
            "replicability relations close on finite power-map spines that end "
            "at the identity class 1A."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 COMPOSITE MOONSHINE POWER SPINE BRIDGE")
    print("=" * 72)
    for key, value in summary["composite_moonshine_power_spine_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
