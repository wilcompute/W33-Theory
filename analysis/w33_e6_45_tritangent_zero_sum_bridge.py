"""Part MCCCXCI: E6 45 tritangent zero-sum bridge.

MCCCXC identified each W33-derived 81-root matter sector as

    81 = 27_E6 weights x 3_A2 phases.

On the 27 E6 weights, the inner-product -2/3 graph is the complement of the
Schlaefli graph: srg(27,10,1,5).  Because lambda=1, each edge sits in exactly
one triangle, giving 45 triangles total.  This verifier checks the stronger
weight statement: every such triangle is a zero-sum triple of E6 weights.

This is the finite tritangent/cubic layer:

    27 minuscule weights -> 45 zero-sum triples.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_e8_e6_a2_coordinate_decomposition import sectorize_by_coordinate  # noqa: E402
from analysis.w33_e6_minuscule_27_a2_phase_factorization import project_to_e6  # noqa: E402
from analysis.w33_tetracode_e8_root_system_bridge import Vector, counter_to_json, inner  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MCCCXCI_E6_45_TRITANGENT_ZERO_SUM_BRIDGE_results.json"


def vector_sum(vectors: list[Vector]) -> Vector:
    return tuple(sum(vector[idx] for vector in vectors) for idx in range(8))


def projected_weights(coordinate: int, sector_key: str) -> list[Vector]:
    return sorted({project_to_e6(root, coordinate) for root in sectorize_by_coordinate(coordinate)[sector_key]})


def edge_list(weights: list[Vector], edge_inner_product: Fraction = Fraction(-2, 3)) -> list[tuple[int, int]]:
    return [
        (left, right)
        for left, right in combinations(range(len(weights)), 2)
        if inner(weights[left], weights[right]) == edge_inner_product
    ]


def triangle_list(edges: list[tuple[int, int]], vertex_count: int = 27) -> list[tuple[int, int, int]]:
    edge_set = set(edges)
    triangles: list[tuple[int, int, int]] = []
    for left, middle, right in combinations(range(vertex_count), 3):
        if (left, middle) in edge_set and (left, right) in edge_set and (middle, right) in edge_set:
            triangles.append((left, middle, right))
    return triangles


def tritangent_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    weights = projected_weights(coordinate, sector_key)
    edges = edge_list(weights)
    triangles = triangle_list(edges, len(weights))
    edge_triangle_counts = Counter(
        sum(1 for triangle in triangles if left in triangle and right in triangle)
        for left, right in edges
    )
    vertex_triangle_counts = Counter(
        sum(1 for triangle in triangles if vertex in triangle)
        for vertex in range(len(weights))
    )
    zero_sum_count = sum(
        1
        for triangle in triangles
        if all(entry == 0 for entry in vector_sum([weights[idx] for idx in triangle]))
    )
    triangle_inner_profiles = Counter(
        tuple(
            sorted(
                inner(weights[left], weights[right])
                for left, right in combinations(triangle, 2)
            )
        )
        for triangle in triangles
    )

    checks = {
        "weight_count_is_27": len(weights) == 27,
        "edge_count_is_135": len(edges) == 135,
        "triangle_count_is_45": len(triangles) == 45,
        "each_edge_lies_in_one_triangle": edge_triangle_counts == {1: 135},
        "each_weight_lies_in_five_triangles": vertex_triangle_counts == {5: 27},
        "all_triangles_are_zero_sum": zero_sum_count == 45,
        "all_triangle_edges_have_inner_minus_2_over_3": triangle_inner_profiles
        == {(Fraction(-2, 3), Fraction(-2, 3), Fraction(-2, 3)): 45},
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "weight_count": len(weights),
        "edge_count": len(edges),
        "triangle_count": len(triangles),
        "zero_sum_triangle_count": zero_sum_count,
        "edge_triangle_multiplicity_profile": counter_to_json(edge_triangle_counts),
        "vertex_triangle_multiplicity_profile": counter_to_json(vertex_triangle_counts),
        "triangle_inner_product_profile": counter_to_json(triangle_inner_profiles),
        "sample_triangles": [list(triangle) for triangle in triangles[:8]],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def e6_45_tritangent_zero_sum_packet() -> dict[str, Any]:
    reports = [
        tritangent_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]

    checks = {
        "all_eight_reports_verify_7_checks": all(report["n_verified"] == 7 for report in reports),
        "all_eight_reports_have_45_zero_sum_triangles": all(
            report["triangle_count"] == 45 and report["zero_sum_triangle_count"] == 45 for report in reports
        ),
        "all_eight_reports_have_edge_unique_triangle_property": all(
            report["edge_triangle_multiplicity_profile"] == {"1": 135} for report in reports
        ),
        "all_eight_reports_have_five_triangles_per_weight": all(
            report["vertex_triangle_multiplicity_profile"] == {"5": 27} for report in reports
        ),
    }

    return {
        "part": "MCCCXCI",
        "theorem": "E6 45 tritangent zero-sum bridge",
        "input_bridge": "MCCCXC E6 minuscule 27 x A2 phase factorization",
        "tritangent_identity": "27 E6 weights -> 45 zero-sum triples",
        "matter_sector_reports": reports,
        "claim_boundary": (
            "finite E6 minuscule incidence theorem; it identifies the zero-sum "
            "triple/tritangent layer inside the W33-derived matter weights, without "
            "asserting a continuum Yukawa model by itself"
        ),
        "reading": (
            "The complement Schlaefli graph on each 27-weight E6 minuscule matter "
            "chart has 135 edges and 45 triangles. Every edge lies in exactly one "
            "triangle, every weight lies in five triangles, and every triangle is "
            "a zero-sum triple of projected E6 weights. This is the finite cubic "
            "incidence layer: the 27 matter weights carry exactly 45 tritangent "
            "zero-sum triples."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e6_45_tritangent_zero_sum_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCI: E6 45 Tritangent Zero-Sum Bridge ===")
    print("identity:", packet["tritangent_identity"])
    first = packet["matter_sector_reports"][0]
    print("sector 0 triangles:", first["triangle_count"])
    print("sector 0 zero-sum triangles:", first["zero_sum_triangle_count"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-sector checks:", [report["n_verified"] for report in packet["matter_sector_reports"]])


if __name__ == "__main__":
    main()
