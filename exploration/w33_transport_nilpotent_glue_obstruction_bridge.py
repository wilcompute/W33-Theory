"""Operator-level obstruction behind the transport filtered shadow match.

The transport/K3 bridge now matches the ordered dimension pattern

    81 -> 162 -> 81

exactly. That still does not mean the internal and external 162-sectors are
the same object. The sharper internal theorem is already operator-level:

1. the ternary transport extension is carried by a nontrivial twisted cocycle;
2. the associated fiber shift tensors to a square-zero rank-81 operator on the
   162-dimensional matter sector;
3. the current external K3 shadow is split, so its extension class is zero.

So the current bridge reaches the ordered head/middle/tail pattern, but not the
nontrivial nilpotent glue operator that holds the internal 162-sector
together.
"""

from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from w33_transport_filtered_shadow_bridge import (
    build_transport_filtered_shadow_bridge_summary,
)

DEFAULT_OUTPUT_PATH = (
    ROOT / "data" / "w33_transport_nilpotent_glue_obstruction_bridge_summary.json"
)


def _transport_cocycle_summary() -> dict[str, Any]:
    fallback_path = ROOT / "data" / "w33_transport_ternary_cocycle_bridge_summary.json"
    if fallback_path.exists():
        return json.loads(fallback_path.read_text(encoding="utf-8"))

    try:
        from w33_transport_ternary_cocycle_bridge import (
            build_transport_ternary_cocycle_summary,
        )
    except ModuleNotFoundError as exc:
        if exc.name != "networkx":
            raise
        return json.loads(fallback_path.read_text(encoding="utf-8"))
    return build_transport_ternary_cocycle_summary()


@lru_cache(maxsize=1)
def build_transport_nilpotent_glue_obstruction_bridge_summary() -> dict[str, Any]:
    filtered = build_transport_filtered_shadow_bridge_summary()
    cocycle = _transport_cocycle_summary()

    internal_operator = cocycle["matter_extension_operator"]
    external_filtration = filtered["external_canonical_split_filtration"]

    return {
        "status": "ok",
        "internal_transport_nilpotent_glue": {
            "dimension": internal_operator["dimension"],
            "rank": internal_operator["rank"],
            "nullity": internal_operator["nullity"],
            "square_zero": internal_operator["square_zero"],
            "image_dimension": internal_operator["image_dimension"],
            "kernel_dimension": internal_operator["kernel_dimension"],
            "image_equals_kernel": internal_operator["image_equals_kernel"],
            "logical_qutrits": internal_operator["logical_qutrits"],
        },
        "external_split_filtered_shadow": {
            "ordered_filtration_dimensions": external_filtration[
                "ordered_filtration_dimensions"
            ],
            "ordered_line_types": external_filtration["ordered_line_types"],
            "is_split": external_filtration["is_split"],
            "extension_class_zero": external_filtration["is_split"],
        },
        "transport_nilpotent_glue_obstruction_theorem": {
            "internal_transport_162_has_nontrivial_rank_81_square_zero_glue_operator": (
                internal_operator["dimension"] == 162
                and internal_operator["rank"] == 81
                and internal_operator["nullity"] == 81
                and internal_operator["square_zero"] is True
                and internal_operator["image_equals_kernel"] is True
            ),
            "external_transport_shadow_matches_the_ordered_81_in_162_out_81_filtration": (
                external_filtration["ordered_filtration_dimensions"] == [81, 162, 81]
            ),
            "external_transport_shadow_is_split_and_has_zero_extension_class": (
                external_filtration["is_split"] is True
            ),
            "internal_and_external_transport_packets_match_at_filtered_dimension_level_but_not_at_glue_operator_level": (
                internal_operator["dimension"] == 162
                and internal_operator["rank"] == 81
                and internal_operator["square_zero"] is True
                and external_filtration["ordered_filtration_dimensions"]
                == [81, 162, 81]
                and external_filtration["is_split"] is True
            ),
            "current_bridge_reaches_head_middle_tail_and_ordering_but_not_nilpotent_glue": (
                filtered["transport_filtered_shadow_theorem"][
                    "current_bridge_reaches_filtered_split_shadow_but_not_nonsplit_extension_identity"
                ]
                and internal_operator["rank"] == 81
                and internal_operator["square_zero"] is True
                and external_filtration["is_split"] is True
            ),
        },
        "bridge_verdict": (
            "The transport/K3 comparison is now exact at the ordered filtered "
            "dimension level, but the missing structure is sharper than an "
            "abstract extension-class slogan. Internally the 162-sector "
            "already carries a canonical nontrivial square-zero rank-81 glue "
            "operator with image = kernel = 81, while the current external K3 "
            "shadow is split and therefore carries only the zero extension "
            "class. So the present bridge reaches head, middle, tail, and "
            "ordering, but not the nilpotent glue that binds the internal "
            "transport packet."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(
            build_transport_nilpotent_glue_obstruction_bridge_summary(), indent=2
        ),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
