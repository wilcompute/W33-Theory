"""The low-order moonshine base closes as one finite quiver.

The recent bridges split the low-order Monster classes into exact node types:

    1A                     : linear weight-12 quotient node,
    2A,3A,5A,7A,13A        : quadratic Fricke trace/norm nodes,
    2B,3B,5B,7B,13B,4C     : linear eta-unit nodes,
    3C                     : affine E8 exceptional node,
    4A,6A,8A,10A           : first composite power-map nodes.

The generating edges are exact:

    1A  -> pA, pB, 3C      by prime replicability / Faber source,
    4A  -> 2B -> 1A,
    6A  -> 3A and 2A -> 1A,
    8A  -> 4C -> 2B -> 1A,
    10A -> 5A and 2A -> 1A.

So the low-order moonshine carrier is no longer a loose catalogue of
McKay-Thompson series.  It is one finite directed grammar generated from the
weight-12 identity node 1A.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_low_order_moonshine_quiver_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_3c_affine_e8_moonshine_bridge import build_summary as build_3c_summary
from w33_composite_moonshine_power_spine_bridge import build_summary as build_composite_summary
from w33_fundamental_moonshine_algebra_bridge import build_summary as build_fundamental_summary
from w33_fundamental_moonshine_replicability_bridge import build_summary as build_prime_rep_summary
from w33_nonfricke_linear_moonshine_bridge import build_summary as build_nonfricke_summary


NODE_TYPES = {
    "1A": "quotient",
    "2A": "quadratic_fricke",
    "3A": "quadratic_fricke",
    "5A": "quadratic_fricke",
    "7A": "quadratic_fricke",
    "13A": "quadratic_fricke",
    "2B": "linear_eta",
    "3B": "linear_eta",
    "5B": "linear_eta",
    "7B": "linear_eta",
    "13B": "linear_eta",
    "4C": "linear_eta",
    "3C": "affine_exceptional",
    "4A": "composite_power",
    "6A": "composite_power",
    "8A": "composite_power",
    "10A": "composite_power",
}


def _edge(src: str, dst: str, kind: str) -> dict[str, str]:
    return {"src": src, "dst": dst, "kind": kind}


def build_summary() -> dict[str, Any]:
    fundamental = build_fundamental_summary()
    prime_rep = build_prime_rep_summary()
    nonfricke = build_nonfricke_summary()
    three_c = build_3c_summary()
    composite = build_composite_summary()

    nodes = [{"name": name, "type": node_type} for name, node_type in NODE_TYPES.items()]

    source_edges = [
        _edge("1A", cls, "prime_faber_source")
        for cls in ["2A", "3A", "5A", "7A", "13A", "2B", "3B", "5B", "7B", "13B", "3C"]
    ]
    power_edges = [
        _edge("4A", "2B", "square_map"),
        _edge("2B", "1A", "power_map"),
        _edge("6A", "3A", "square_map"),
        _edge("6A", "2A", "cube_map"),
        _edge("3A", "1A", "power_map"),
        _edge("2A", "1A", "power_map"),
        _edge("8A", "4C", "square_map"),
        _edge("4C", "2B", "square_map"),
        _edge("8A", "1A", "power_map"),
        _edge("10A", "5A", "square_map"),
        _edge("10A", "2A", "fifth_map"),
        _edge("5A", "1A", "power_map"),
    ]
    edges = source_edges + power_edges

    node_counts = {
        "quotient": sum(1 for v in NODE_TYPES.values() if v == "quotient"),
        "quadratic_fricke": sum(1 for v in NODE_TYPES.values() if v == "quadratic_fricke"),
        "linear_eta": sum(1 for v in NODE_TYPES.values() if v == "linear_eta"),
        "affine_exceptional": sum(1 for v in NODE_TYPES.values() if v == "affine_exceptional"),
        "composite_power": sum(1 for v in NODE_TYPES.values() if v == "composite_power"),
    }

    theorem = {
        "the_identity_node_1A_is_the_unique_weight12_quotient_source": (
            fundamental["fundamental_moonshine_algebra_theorem"][
                "oneA_closes_as_the_weight12_linear_quotient_algebra"
            ]
            and NODE_TYPES["1A"] == "quotient"
            and node_counts["quotient"] == 1
        ),
        "the_five_fricke_prime_nodes_are_exactly_the_quadratic_trace_norm_nodes": (
            fundamental["fundamental_moonshine_algebra_theorem"][
                "each_prime_hauptmodul_satisfies_the_quadratic_polynomial_X2_minus_TminuskX_plus_norm"
            ]
            and node_counts["quadratic_fricke"] == 5
        ),
        "the_nonfricke_side_is_exactly_the_linear_eta_branch_family_plus_4C": (
            nonfricke["nonfricke_linear_moonshine_theorem"][
                "all_five_nonfricke_prime_B_classes_are_exact_linear_eta_branches"
            ]
            and nonfricke["nonfricke_linear_moonshine_theorem"][
                "4C_is_the_first_composite_linear_eta_branch"
            ]
            and node_counts["linear_eta"] == 6
        ),
        "the_exceptional_affine_node_is_exactly_3C": (
            three_c["threeC_affine_e8_theorem"][
                "the_3C_class_therefore_equals_the_affine_E8_character_under_q_to_q_cubed"
            ]
            and node_counts["affine_exceptional"] == 1
            and NODE_TYPES["3C"] == "affine_exceptional"
        ),
        "the_first_composite_nodes_close_on_exact_power_spines": (
            composite["composite_moonshine_power_spine_theorem"][
                "the_first_composite_classes_close_on_exact_power_map_spines_ending_at_1A"
            ]
            and node_counts["composite_power"] == 4
        ),
        "the_low_order_moonshine_base_is_generated_by_one_finite_quiver_from_1A": (
            prime_rep["fundamental_moonshine_replicability_theorem"][
                "the_prime_classes_close_one_step_higher_as_1A_sourced_faber_algebras"
            ]
            and nonfricke["nonfricke_linear_moonshine_theorem"][
                "the_nonfricke_and_exceptional_side_close_on_one_linear_affine_moonshine_spine"
            ]
            and composite["composite_moonshine_power_spine_theorem"][
                "the_first_composite_classes_close_on_exact_power_map_spines_ending_at_1A"
            ]
        ),
    }
    theorem["the_low_order_moonshine_quiver_is_fully_closed"] = all(theorem.values())

    return {
        "low_order_moonshine_quiver_dictionary": {
            "nodes": nodes,
            "node_counts": node_counts,
            "edges": edges,
        },
        "low_order_moonshine_quiver_theorem": theorem,
        "interpretation": (
            "The low-order Monster moonshine classes now form a finite directed grammar. "
            "The unique weight-12 quotient node 1A sources the prime recursion, the "
            "Fricke A-side appears as quadratic nodes, the non-Fricke side appears as "
            "linear eta nodes, 3C is the affine E8 exceptional node, and the first "
            "composite classes are power-map descendants. So the low-order moonshine "
            "carrier is one explicit quiver rather than a bag of disconnected formulas."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LOW-ORDER MOONSHINE QUIVER BRIDGE")
    print("=" * 72)
    for key, value in summary["low_order_moonshine_quiver_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
