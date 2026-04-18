"""The full Ogg-prime moonshine layer is a finite extension of the 1A quiver.

Ogg's Monster-prime set is

    {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71}.

The low-order quiver already covered the small prime layer:

    2A, 2B, 3A, 3B, 3C, 5A, 5B, 7A, 7B, 13A, 13B.

The remaining prime-order moonshine nodes are:

    11A, 17A, 19A, 23AB, 29A, 31AB, 41A, 47AB, 59AB, 71AB,

where the AB families share the same Hauptmodul.

Every one of these remaining prime families already satisfies prime
replicability sourced by 1A, so the Ogg-prime moonshine layer is not an
open-ended zoo. It is a finite extension of the low-order quiver by ten
additional prime families.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ogg_prime_moonshine_quiver_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_low_order_moonshine_quiver_bridge import build_summary as build_low_order_summary
from w33_monster_ogg_supersingular import MONSTER_PRIMES
from scripts.w33_leech_monster import mckay_thompson_series, verify_fricke_prime_replicability


OGG_EXTENSION_FAMILIES = [
    {"family": "11A", "prime": 11, "classes": ["11A"]},
    {"family": "17A", "prime": 17, "classes": ["17A"]},
    {"family": "19A", "prime": 19, "classes": ["19A"]},
    {"family": "23AB", "prime": 23, "classes": ["23A", "23B"]},
    {"family": "29A", "prime": 29, "classes": ["29A"]},
    {"family": "31AB", "prime": 31, "classes": ["31A", "31B"]},
    {"family": "41A", "prime": 41, "classes": ["41A"]},
    {"family": "47AB", "prime": 47, "classes": ["47A", "47B"]},
    {"family": "59AB", "prime": 59, "classes": ["59A", "59B"]},
    {"family": "71AB", "prime": 71, "classes": ["71A", "71B"]},
]


def _family_row(spec: dict[str, Any], max_q_exp: int = 10) -> dict[str, Any]:
    series = {
        cls: mckay_thompson_series(cls, max_q_exp=max_q_exp)
        for cls in spec["classes"]
    }
    if any(v is None for v in series.values()):
        raise RuntimeError(f"Series unavailable for {spec['family']}")

    reps = {
        cls: verify_fricke_prime_replicability(cls, max_q_exp=max_q_exp)
        for cls in spec["classes"]
    }

    first = series[spec["classes"][0]]
    same_series = all(series[cls] == first for cls in spec["classes"][1:])

    return {
        "family": spec["family"],
        "prime": spec["prime"],
        "classes": list(spec["classes"]),
        "shared_series_q_minus_1_to_q5": {
            str(exp): int(first.get(exp, 0))
            for exp in range(-1, 6)
            if int(first.get(exp, 0)) != 0
        },
        "faber_coeffs": {
            cls: [int(c) for c in reps[cls]["faber_coeffs"]]
            for cls in spec["classes"]
        },
        "theorems": {
            "all_class_series_are_available": all(series[cls] is not None for cls in spec["classes"]),
            "all_classes_satisfy_prime_replicability": all(bool(reps[cls]["verified"]) for cls in spec["classes"]),
            "shared_series_holds_for_AB_family": same_series if len(spec["classes"]) > 1 else True,
        },
    }


def build_summary() -> dict[str, Any]:
    low_order = build_low_order_summary()
    rows = [_family_row(spec) for spec in OGG_EXTENSION_FAMILIES]

    covered_primes = sorted(
        {
            2, 3, 5, 7, 13,  # low-order quiver primes
            *[row["prime"] for row in rows],
        }
    )

    edges = [
        {"src": "1A", "dst": row["family"], "kind": "prime_faber_source"}
        for row in rows
    ]

    theorem = {
        "the_low_order_quiver_already_closes_the_small_monster_prime_layer": (
            low_order["low_order_moonshine_quiver_theorem"]["the_low_order_moonshine_quiver_is_fully_closed"]
        ),
        "the_remaining_ten_ogg_prime_families_all_have_exact_prime_replicability": all(
            row["theorems"]["all_classes_satisfy_prime_replicability"] for row in rows
        ),
        "the_AB_ogg_prime_families_share_exact_hauptmoduls": all(
            row["theorems"]["shared_series_holds_for_AB_family"]
            for row in rows
            if len(row["classes"]) > 1
        ),
        "the_full_prime_layer_covers_exactly_the_15_monster_primes": covered_primes == sorted(MONSTER_PRIMES),
        "the_full_ogg_prime_moonshine_layer_is_generated_from_1A_by_a_finite_quiver_extension": (
            low_order["low_order_moonshine_quiver_theorem"]["the_low_order_moonshine_base_is_generated_by_one_finite_quiver_from_1A"]
            and all(row["theorems"]["all_classes_satisfy_prime_replicability"] for row in rows)
            and covered_primes == sorted(MONSTER_PRIMES)
        ),
    }
    theorem["the_ogg_prime_moonshine_quiver_is_fully_closed"] = all(theorem.values())

    return {
        "ogg_prime_moonshine_quiver_dictionary": {
            "low_order_quiver_node_counts": low_order["low_order_moonshine_quiver_dictionary"]["node_counts"],
            "extension_rows": rows,
            "extension_edges": edges,
            "covered_monster_primes": covered_primes,
        },
        "ogg_prime_moonshine_quiver_theorem": theorem,
        "interpretation": (
            "The low-order moonshine quiver was only the first finite chunk. The "
            "remaining Ogg-prime layer also closes on exact prime-replicability "
            "families sourced by 1A, with the AB pairs collapsing to shared "
            "Hauptmoduls. So the full Monster-prime layer is a finite quiver "
            "extension, not an uncontrolled list of modular functions."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 OGG-PRIME MOONSHINE QUIVER BRIDGE")
    print("=" * 72)
    for key, value in summary["ogg_prime_moonshine_quiver_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
