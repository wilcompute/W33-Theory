"""The supported moonshine seed closes as an exact head-signature graph.

The previous bridge anchored 17 McKay-Thompson classes against bundled
CTblLib-derived Monster character values on the first three nontrivial
irreducibles:

    196883, 21296876, 842609326.

The supported offline moonshine seed contains 32 classes with exact q-series
transport already closed under the available square/cube/fifth maps and the 18
composite divisor-sum checks.  This bridge propagates the validated
head-character inference from the anchored 17-class subset to the full 32-node
seed.

The result is sharper than a coefficient dictionary:

    - every supported class has an exact integral head signature;
    - the first three nontrivial head traces separate all 32 supported nodes;
    - all 35 Atlas-available prime-power transport edges land inside the same
      signature dictionary;
    - all 18 composite transport rows land inside the same signature
      dictionary.

So the supported moonshine seed is not only a transport graph of q-series.  It
is already a finite trace graph on the first three nontrivial Monster modules.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_supported_seed_head_signature_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import (
    analyze_monster_moonshine_power_closure,
    infer_monster_head_character_values,
)
from w33_moonshine_head_character_transport_bridge import (
    HEAD_DEGREES,
    INTEGER_CLASS_ORDER,
    build_summary as build_head_transport_summary,
)
from w33_supported_seed_moonshine_transport_bridge import (
    build_summary as build_transport_summary,
)


def _signature(values: dict[int, int]) -> tuple[int, int, int]:
    return tuple(int(values[deg]) for deg in HEAD_DEGREES)


def _signature_row(class_name: str) -> dict[str, Any]:
    inferred = infer_monster_head_character_values(class_name, max_n=3)
    if inferred is None:
        raise RuntimeError(f"Head character inference unavailable for {class_name}")
    return {
        "class_name": class_name,
        "signature": {str(deg): int(inferred[deg]) for deg in HEAD_DEGREES},
        "with_trivial": {str(deg): int(inferred[deg]) for deg in [1] + HEAD_DEGREES},
    }


def build_summary(max_q_exp: int = 24) -> dict[str, Any]:
    closure = analyze_monster_moonshine_power_closure(max_q_exp=max_q_exp)
    supported_classes = [str(cls) for cls in closure["supported_classes"]]

    rows = [_signature_row(cls) for cls in supported_classes]
    by_class = {row["class_name"]: row for row in rows}
    distinct_signatures = {
        tuple(int(row["signature"][str(deg)]) for deg in HEAD_DEGREES)
        for row in rows
    }

    head_transport = build_head_transport_summary()
    transport = build_transport_summary(max_q_exp=max_q_exp)
    anchored_rows = {
        row["class_name"]: row
        for row in head_transport["moonshine_head_character_transport_dictionary"]["rows"]
    }

    atlas_edge_rows = []
    exponent_by_kind = {"square": 2, "cube": 3, "fifth": 5}
    for kind, exponent in exponent_by_kind.items():
        for source, info in sorted(closure["atlas_validation"][kind].items()):
            atlas_targets = info["atlas_targets"]
            target = info["inferred"]
            if atlas_targets is None:
                continue
            if target not in supported_classes:
                raise RuntimeError(f"Inferred target {target} is not in the supported seed")
            atlas_edge_rows.append(
                {
                    "source": str(source),
                    "exponent": exponent,
                    "target": str(target),
                    "source_signature": by_class[str(source)]["signature"],
                    "target_signature": by_class[str(target)]["signature"],
                    "atlas_targets": [str(x) for x in atlas_targets],
                    "matches_atlas": bool(info["matches"]),
                }
            )

    composite_rows = transport["supported_seed_moonshine_transport_dictionary"]["composite_rows"]

    theorem = {
        "all_32_supported_seed_classes_admit_exact_integral_head_signatures": (
            len(rows) == 32 and all(len(row["signature"]) == 3 for row in rows)
        ),
        "the_17_ctbllib_anchored_classes_match_actual_monster_head_characters": (
            all(anchored_rows[cls]["all_match"] for cls in INTEGER_CLASS_ORDER)
        ),
        "the_first_three_nontrivial_head_irreps_separate_all_32_supported_seed_classes": (
            len(distinct_signatures) == len(rows) == 32
        ),
        "all_35_atlas_available_prime_power_edges_land_inside_the_same_head_signature_dictionary": (
            len(atlas_edge_rows) == 35 and all(row["matches_atlas"] for row in atlas_edge_rows)
        ),
        "all_18_composite_transport_rows_land_inside_the_same_head_signature_dictionary": (
            len(composite_rows) == 18
            and all(row["class_name"] in by_class for row in composite_rows)
            and all(all(str(target) in by_class for target in row["power_map"].values()) for row in composite_rows)
        ),
        "the_supported_seed_transport_graph_therefore_closes_as_a_32_node_head_signature_graph": (
            head_transport["moonshine_head_character_transport_theorem"][
                "the_moonshine_head_character_transport_bridge_is_fully_closed"
            ]
            and transport["supported_seed_moonshine_transport_theorem"][
                "the_supported_seed_moonshine_transport_graph_is_fully_closed"
            ]
            and len(distinct_signatures) == len(rows) == 32
            and len(atlas_edge_rows) == 35
        ),
    }
    theorem["the_supported_seed_head_signature_bridge_is_fully_closed"] = all(theorem.values())

    return {
        "supported_seed_head_signature_dictionary": {
            "supported_classes": supported_classes,
            "rows": rows,
            "distinct_signature_count": len(distinct_signatures),
            "atlas_edge_rows": atlas_edge_rows,
            "composite_rows": composite_rows,
        },
        "supported_seed_head_signature_theorem": theorem,
        "interpretation": (
            "The supported moonshine seed is now closed on the trace side. "
            "The 17 CTblLib-anchored classes validate the head-character "
            "inference, that inference extends to all 32 supported classes, "
            "the first three nontrivial traces separate every supported node, "
            "and every verified transport edge stays inside the same finite "
            "signature dictionary. So the q-series transport graph already "
            "lifts to a 32-node Monster head-signature graph."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 SUPPORTED-SEED HEAD SIGNATURE BRIDGE")
    print("=" * 72)
    for key, value in summary["supported_seed_head_signature_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
