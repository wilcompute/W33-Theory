"""Part MCCCXCII: E6 36 double-six bridge.

MCCCXC and MCCCXCI recovered the E6 minuscule 27-weight geometry and its
45 zero-sum tritangent triples.  The next classical cubic-surface invariant is
the 36 double-sixes.

In the Schlaefli graph convention used here, an edge means inner product 1/3,
the 16-valent "skew" relation.  A double-six is two disjoint 6-cliques whose
cross edges form a perfect matching:

    A row: 6 mutually skew weights
    B row: 6 mutually skew weights
    cross skew relation: exactly a matching

The verifier derives this structure from the W33-derived E6 matter weights for
all eight matter charts.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_e6_45_tritangent_zero_sum_bridge import projected_weights  # noqa: E402
from analysis.w33_tetracode_e8_root_system_bridge import counter_to_json, inner  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MCCCXCII_E6_36_DOUBLE_SIX_BRIDGE_results.json"


def schlaefli_adjacency(weights: list[tuple[Fraction, ...]]) -> list[set[int]]:
    adjacency = [set() for _ in weights]
    for left in range(len(weights)):
        for right in range(left + 1, len(weights)):
            if inner(weights[left], weights[right]) == Fraction(1, 3):
                adjacency[left].add(right)
                adjacency[right].add(left)
    return adjacency


def six_cliques(adjacency: list[set[int]]) -> list[tuple[int, ...]]:
    cliques: list[tuple[int, ...]] = []

    def extend(clique: tuple[int, ...], candidates: tuple[int, ...]) -> None:
        if len(clique) == 6:
            cliques.append(clique)
            return
        if len(clique) + len(candidates) < 6:
            return

        for idx, vertex in enumerate(candidates):
            next_candidates = tuple(
                candidate for candidate in candidates[idx + 1 :] if candidate in adjacency[vertex]
            )
            extend(clique + (vertex,), next_candidates)

    extend((), tuple(range(len(adjacency))))
    return cliques


def is_double_six(first: tuple[int, ...], second: tuple[int, ...], adjacency: list[set[int]]) -> bool:
    if set(first) & set(second):
        return False

    first_cross_degrees = [sum(1 for vertex in second if vertex in adjacency[row_vertex]) for row_vertex in first]
    second_cross_degrees = [sum(1 for vertex in first if vertex in adjacency[row_vertex]) for row_vertex in second]
    return first_cross_degrees == [1] * 6 and second_cross_degrees == [1] * 6


def double_sixes(cliques: list[tuple[int, ...]], adjacency: list[set[int]]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for left_idx, first in enumerate(cliques):
        for second in cliques[left_idx + 1 :]:
            if is_double_six(first, second, adjacency):
                pairs.append((first, second))
    return pairs


def cross_edge_profile(double_six_pairs: list[tuple[tuple[int, ...], tuple[int, ...]]], adjacency: list[set[int]]) -> Counter[int]:
    return Counter(
        sum(1 for left in first for right in second if right in adjacency[left])
        for first, second in double_six_pairs
    )


def double_six_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    weights = projected_weights(coordinate, sector_key)
    adjacency = schlaefli_adjacency(weights)
    cliques = six_cliques(adjacency)
    pairs = double_sixes(cliques, adjacency)
    vertex_participation = Counter(vertex for first, second in pairs for row in (first, second) for vertex in row)
    row_participation = Counter(row for pair in pairs for row in pair)
    cross_edges = cross_edge_profile(pairs, adjacency)
    row_degree_profile = Counter(len(adjacency[vertex]) for vertex in range(len(weights)))

    checks = {
        "weight_count_is_27": len(weights) == 27,
        "schlaefli_degree_is_16": row_degree_profile == {16: 27},
        "six_clique_count_is_72": len(cliques) == 72,
        "double_six_count_is_36": len(pairs) == 36,
        "each_six_clique_appears_in_one_double_six": row_participation == {row: 1 for row in cliques},
        "each_weight_appears_in_16_double_sixes": vertex_participation == {vertex: 16 for vertex in range(27)},
        "each_double_six_has_six_cross_matching_edges": cross_edges == {6: 36},
        "all_cross_degrees_are_perfect_matchings": all(
            is_double_six(first, second, adjacency) for first, second in pairs
        ),
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "weight_count": len(weights),
        "schlaefli_degree_profile": counter_to_json(row_degree_profile),
        "six_clique_count": len(cliques),
        "double_six_count": len(pairs),
        "row_clique_participation_profile": counter_to_json(Counter(row_participation.values())),
        "weight_double_six_participation_profile": counter_to_json(Counter(vertex_participation.values())),
        "cross_edge_count_profile": counter_to_json(cross_edges),
        "sample_six_cliques": [list(clique) for clique in cliques[:8]],
        "sample_double_sixes": [
            {"row_a": list(first), "row_b": list(second)}
            for first, second in pairs[:6]
        ],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def e6_36_double_six_packet() -> dict[str, Any]:
    reports = [
        double_six_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]

    checks = {
        "all_eight_reports_verify_8_checks": all(report["n_verified"] == 8 for report in reports),
        "all_eight_reports_have_72_six_cliques": all(report["six_clique_count"] == 72 for report in reports),
        "all_eight_reports_have_36_double_sixes": all(report["double_six_count"] == 36 for report in reports),
        "all_eight_reports_have_one_double_six_per_row_clique": all(
            report["row_clique_participation_profile"] == {"1": 72} for report in reports
        ),
        "all_eight_reports_have_16_double_sixes_per_weight": all(
            report["weight_double_six_participation_profile"] == {"16": 27} for report in reports
        ),
    }

    return {
        "part": "MCCCXCII",
        "theorem": "E6 36 double-six bridge",
        "input_bridge": "MCCCXCI E6 45 tritangent zero-sum bridge",
        "double_six_identity": "27 E6 weights -> 72 six-cliques -> 36 double-sixes",
        "matter_sector_reports": reports,
        "claim_boundary": (
            "finite cubic-surface incidence theorem on the W33-derived E6 minuscule "
            "matter weights; it identifies double-six combinatorics and does not "
            "assert a continuum geometry by itself"
        ),
        "reading": (
            "Each W33-derived 27-weight E6 matter chart contains 72 six-cliques in "
            "the Schlaefli/skew graph. Those six-cliques pair uniquely into 36 "
            "double-sixes, where the cross-skew relation is a perfect matching. "
            "Every weight appears in 16 double-sixes. This recovers the classical "
            "36 double-six layer from the finite W33/E6 matter geometry."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e6_36_double_six_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCII: E6 36 Double-Six Bridge ===")
    print("identity:", packet["double_six_identity"])
    first = packet["matter_sector_reports"][0]
    print("sector 0 six-cliques:", first["six_clique_count"])
    print("sector 0 double-sixes:", first["double_six_count"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-sector checks:", [report["n_verified"] for report in packet["matter_sector_reports"]])


if __name__ == "__main__":
    main()
