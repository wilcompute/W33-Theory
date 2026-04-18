"""The full offline-supported moonshine seed closes on one finite transport graph.

The monster script already supports a deterministic offline seed of 32
McKay-Thompson classes:

    1A,
    2A, 2B,
    3A, 3B, 3C,
    4A, 4B, 4C, 4D,
    5A, 5B,
    6A, 6B, 6C, 6D, 6E,
    7A, 7B,
    8A, 8A', 8B, 8E,
    9A,
    10A, 10B, 10C, 10D, 10E,
    11A,
    13A, 13B.

On this seed, q-series replicability already determines exact transport maps:

    square, cube, fifth, and derived fourth maps,

and the composite divisor-sum relations for orders

    4, 6, 8, 9, 10

are fully verified.  Where Atlas power targets are present, every inferred
transport edge matches the Atlas target exactly.

So the supported moonshine seed is not only a library of formulas.  It is one
finite, Atlas-compatible transport graph.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_supported_seed_moonshine_transport_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import analyze_monster_moonshine_power_closure


def _order(name: str) -> int:
    if name in ("1A", "ID", "IDENTITY"):
        return 1
    digits = ""
    for ch in name:
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else 0


def build_summary(max_q_exp: int = 24) -> dict[str, Any]:
    closure = analyze_monster_moonshine_power_closure(max_q_exp=max_q_exp)

    supported = [str(c) for c in closure["supported_classes"]]
    by_order: dict[int, list[str]] = {}
    for cls in supported:
        by_order.setdefault(_order(cls), []).append(cls)
    by_order = {k: sorted(v) for k, v in sorted(by_order.items())}

    atlas_validation = closure["atlas_validation"]
    atlas_available_counts = {}
    atlas_match_counts = {}
    for kind in ("square", "cube", "fifth"):
        rows = atlas_validation[kind]
        avail = [v for v in rows.values() if v["atlas_targets"] is not None]
        atlas_available_counts[kind] = len(avail)
        atlas_match_counts[kind] = sum(1 for v in avail if v["matches"] is True)

    composite_checks = closure["replicability"]["composite_checks"]
    composite_rows = [
        {
            "class_name": str(chk["class_name"]),
            "verified": bool(chk["verified"]),
            "power_map_source": str(chk["power_map_source"]),
            "power_map": {str(k): str(v) for k, v in chk["power_map"].items()},
        }
        for chk in composite_checks
    ]

    theorem = {
        "the_supported_seed_has_exactly_32_offline_classes": len(supported) == 32,
        "the_supported_seed_orders_are_exactly_1_2_3_4_5_6_7_8_9_10_11_13": list(by_order.keys()) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13],
        "all_atlas_available_square_edges_match_the_q_series_inference": (
            atlas_match_counts["square"] == atlas_available_counts["square"]
        ),
        "all_atlas_available_cube_edges_match_the_q_series_inference": (
            atlas_match_counts["cube"] == atlas_available_counts["cube"]
        ),
        "all_atlas_available_fifth_edges_match_the_q_series_inference": (
            atlas_match_counts["fifth"] == atlas_available_counts["fifth"]
        ),
        "all_18_composite_transport_checks_are_exact_and_atlas_validated": (
            len(composite_rows) == 18
            and all(row["verified"] for row in composite_rows)
            and all(row["power_map_source"] == "atlas" for row in composite_rows)
        ),
        "the_supported_offline_seed_therefore_closes_as_one_finite_transport_graph": (
            len(supported) == 32
            and atlas_match_counts["square"] == atlas_available_counts["square"]
            and atlas_match_counts["cube"] == atlas_available_counts["cube"]
            and atlas_match_counts["fifth"] == atlas_available_counts["fifth"]
            and len(composite_rows) == 18
            and all(row["verified"] for row in composite_rows)
        ),
    }
    theorem["the_supported_seed_moonshine_transport_graph_is_fully_closed"] = all(theorem.values())

    return {
        "supported_seed_moonshine_transport_dictionary": {
            "supported_classes": supported,
            "supported_classes_by_order": by_order,
            "power_maps": closure["power_maps"],
            "atlas_available_counts": atlas_available_counts,
            "atlas_match_counts": atlas_match_counts,
            "composite_rows": composite_rows,
        },
        "supported_seed_moonshine_transport_theorem": theorem,
        "interpretation": (
            "The full offline-supported moonshine seed already behaves like a finite "
            "transport graph. The q-series power maps close internally, every "
            "Atlas-available square/cube/fifth edge matches the inferred target, "
            "and the whole composite layer at orders 4, 6, 8, 9, 10 is validated. "
            "So the supported seed is an exact transport subsystem, not just a "
            "collection of isolated McKay-Thompson formulas."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 SUPPORTED-SEED MOONSHINE TRANSPORT BRIDGE")
    print("=" * 72)
    for key, value in summary["supported_seed_moonshine_transport_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
