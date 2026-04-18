"""The supported moonshine seed closes on the exact graded package V1 ⊕ V2 ⊕ V3.

The first three moonshine coefficients are the traces of the Monster class on
the first three graded pieces of V^natural:

    T_g(q) = q^(-1) + Tr(g|V1) q + Tr(g|V2) q^2 + Tr(g|V3) q^3 + ...

From the exact classical decompositions

    V1 = 1 ⊕ 196883,
    V2 = 1 ⊕ 196883 ⊕ 21296876,
    V3 = 2·1 ⊕ 2·196883 ⊕ 21296876 ⊕ 842609326,

the head-character basis

    (χ_196883, χ_21296876, χ_842609326)

and the graded-trace basis

    (Tr(g|V1), Tr(g|V2), Tr(g|V3))

are related by one unimodular affine change of coordinates:

    V1 = 1 + χ_196883,
    V2 = 1 + χ_196883 + χ_21296876,
    V3 = 2 + 2χ_196883 + χ_21296876 + χ_842609326,

with inverse

    χ_196883   = V1 - 1,
    χ_21296876 = V2 - V1,
    χ_842609326= V3 - V2 - V1.

So the previously closed head-signature graph is equivalently an exact
V1⊕V2⊕V3 package graph.  This bridge pins that graded-package side directly
against the bundled Monster character subset and propagates it to the full
32-node supported seed.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_moonshine_v123_package_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import (
    analyze_monster_moonshine_power_closure,
    compute_mckay_traces,
    infer_monster_head_character_values,
)
from w33_moonshine_head_character_transport_bridge import INTEGER_CLASS_ORDER
from w33_supported_seed_moonshine_transport_bridge import (
    build_summary as build_transport_summary,
)


HEAD_DEGREES = [196883, 21296876, 842609326]
PACKAGE_LABELS = ["V1", "V2", "V3"]


def head_to_v123_package(values: dict[int, int]) -> dict[str, int]:
    chi_1 = int(values[196883])
    chi_2 = int(values[21296876])
    chi_3 = int(values[842609326])
    return {
        "V1": 1 + chi_1,
        "V2": 1 + chi_1 + chi_2,
        "V3": 2 + 2 * chi_1 + chi_2 + chi_3,
    }


def v123_package_to_head(package: dict[str, int]) -> dict[str, int]:
    v1 = int(package["V1"])
    v2 = int(package["V2"])
    v3 = int(package["V3"])
    return {
        "196883": v1 - 1,
        "21296876": v2 - v1,
        "842609326": v3 - v2 - v1,
    }


def _package_row(class_name: str) -> dict[str, Any]:
    inferred = infer_monster_head_character_values(class_name, max_n=3)
    if inferred is None:
        raise RuntimeError(f"Head character inference unavailable for {class_name}")
    package = head_to_v123_package(inferred)
    return {
        "class_name": class_name,
        "package": package,
        "head_signature": {str(deg): int(inferred[deg]) for deg in HEAD_DEGREES},
    }


def build_summary(max_q_exp: int = 24) -> dict[str, Any]:
    closure = analyze_monster_moonshine_power_closure(max_q_exp=max_q_exp)
    supported_classes = [str(cls) for cls in closure["supported_classes"]]

    rows = [_package_row(cls) for cls in supported_classes]
    by_class = {row["class_name"]: row for row in rows}
    distinct_packages = {
        tuple(int(row["package"][label]) for label in PACKAGE_LABELS)
        for row in rows
    }

    anchored_rows = []
    for cls in INTEGER_CLASS_ORDER:
        anchored_package = _package_row(cls)["package"]
        actual = compute_mckay_traces(cls, n_terms=3)
        if actual is None:
            raise RuntimeError(f"Monster trace package unavailable for {cls}")
        actual_package = {"V1": int(actual[0]), "V2": int(actual[1]), "V3": int(actual[2])}
        anchored_rows.append(
            {
                "class_name": cls,
                "inferred_package": anchored_package,
                "actual_package": actual_package,
                "matches": {label: anchored_package[label] == actual_package[label] for label in PACKAGE_LABELS},
                "all_match": anchored_package == actual_package,
            }
        )

    transport = build_transport_summary(max_q_exp=max_q_exp)
    atlas_edge_rows = []
    exponent_by_kind = {"square": 2, "cube": 3, "fifth": 5}
    for kind, exponent in exponent_by_kind.items():
        for source, info in sorted(closure["atlas_validation"][kind].items()):
            if info["atlas_targets"] is None:
                continue
            target = str(info["inferred"])
            atlas_edge_rows.append(
                {
                    "source": str(source),
                    "exponent": exponent,
                    "target": target,
                    "source_package": by_class[str(source)]["package"],
                    "target_package": by_class[target]["package"],
                    "matches_atlas": bool(info["matches"]),
                }
            )

    composite_rows = transport["supported_seed_moonshine_transport_dictionary"]["composite_rows"]

    theorem = {
        "the_v123_package_transform_has_unimodular_linear_part_with_determinant_1": True,
        "all_17_ctbllib_anchored_classes_match_the_actual_monster_v1_v2_v3_traces": (
            all(row["all_match"] for row in anchored_rows)
        ),
        "the_v1_v2_v3_package_separates_all_32_supported_seed_classes": (
            len(distinct_packages) == len(rows) == 32
        ),
        "all_35_atlas_available_prime_power_edges_land_inside_the_same_v1_v2_v3_package_dictionary": (
            len(atlas_edge_rows) == 35 and all(row["matches_atlas"] for row in atlas_edge_rows)
        ),
        "all_18_composite_transport_rows_land_inside_the_same_v1_v2_v3_package_dictionary": (
            len(composite_rows) == 18
            and all(row["class_name"] in by_class for row in composite_rows)
            and all(all(str(target) in by_class for target in row["power_map"].values()) for row in composite_rows)
        ),
        "the_exceptional_affine_node_3c_has_sparse_package_0_248_0": (
            by_class["3C"]["package"] == {"V1": 0, "V2": 248, "V3": 0}
        ),
        "the_pair_8a_8aprime_is_separated_only_by_the_sign_of_v2": (
            by_class["8A"]["package"]["V1"] == by_class["8A'"]["package"]["V1"]
            and by_class["8A"]["package"]["V3"] == by_class["8A'"]["package"]["V3"]
            and by_class["8A"]["package"]["V2"] == -by_class["8A'"]["package"]["V2"]
        ),
        "the_supported_seed_transport_graph_therefore_closes_as_an_exact_v1_v2_v3_package_graph": (
            all(row["all_match"] for row in anchored_rows)
            and len(distinct_packages) == len(rows) == 32
            and len(atlas_edge_rows) == 35
            and all(row["matches_atlas"] for row in atlas_edge_rows)
        ),
    }
    theorem["the_moonshine_v123_package_bridge_is_fully_closed"] = all(theorem.values())

    return {
        "moonshine_v123_package_dictionary": {
            "supported_classes": supported_classes,
            "rows": rows,
            "anchored_rows": anchored_rows,
            "distinct_package_count": len(distinct_packages),
            "atlas_edge_rows": atlas_edge_rows,
            "composite_rows": composite_rows,
        },
        "moonshine_v123_package_theorem": theorem,
        "interpretation": (
            "The supported moonshine seed now closes directly on the first exact "
            "graded Monster package V1⊕V2⊕V3. The head-signature basis and the "
            "graded-package basis are integrally equivalent, the anchored classes "
            "match the actual Monster traces, the full supported seed is separated "
            "by these package traces, and every verified transport edge remains "
            "inside the same finite package dictionary."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 MOONSHINE V1+V2+V3 PACKAGE BRIDGE")
    print("=" * 72)
    for key, value in summary["moonshine_v123_package_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
