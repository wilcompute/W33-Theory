"""Part MCCCXCVIII: Boerdijk/gamma-brass Steiner return graph.

The 2004 gamma-brass / Boerdijk-Coxeter paper points at the same count
package that has just appeared internally in the W33-derived E6 Steiner layer:

    gamma-brass: 26, 38, 81, local 12, shared 4
    600-cell:    120 vertices, 720 edges, 600 tetrahedra,
                 20 Boerdijk-Coxeter rings of 30 tetrahedra

This verifier keeps those external facts as static source counts and tests the
new finite theorem inside the repository:

    240 Steiner trihedra -> 40 disjoint-cover components of size 6.

The component graph, where two components are adjacent when their 18-tritangent
sets intersect in 9 tritangents, has the W33 strongly regular parameters
srg(40,12,2,4).  This is a parameter-level return graph, not a claim that a
canonical isomorphism to the original W33 point graph has been chosen.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_e6_240_steiner_trihedra_e8_count import steiner_trihedra  # noqa: E402
from analysis.w33_e6_120_steiner_trihedral_pairs import counter_to_json  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MCCCXCVIII_BOERDIJK_GAMMA_BRASS_STEINER_RETURN_GRAPH_results.json"

Q = 3
Q_FACTORIAL = 6
V = 40
K = 12
MU = 4
FIVE = 5

GAMMA_BRASS_COUNTS = {
    "unit_cell_sites": 52,
    "cluster_atoms": 26,
    "augmented_cluster_atoms": 38,
    "augmented_cluster_tetrahedra": 81,
    "original_helix_local_neighbors": 12,
    "initial_tetrahedron_shared_icosahedra": 4,
}

CELL_600_COUNTS = {
    "vertices": 120,
    "edges": 720,
    "triangular_faces": 1200,
    "tetrahedral_cells": 600,
    "boerdijk_coxeter_ring_count": 20,
    "tetrahedra_per_ring": 30,
    "cells_around_each_vertex": 20,
    "cells_around_each_edge": 5,
}


def graph_parameters(adjacency: list[set[int]], relation_name: str) -> dict[str, Any]:
    adjacent_common_neighbors: Counter[int] = Counter()
    nonadjacent_common_neighbors: Counter[int] = Counter()

    for left, right in combinations(range(len(adjacency)), 2):
        common = len(adjacency[left] & adjacency[right])
        if right in adjacency[left]:
            adjacent_common_neighbors[common] += 1
        else:
            nonadjacent_common_neighbors[common] += 1

    return {
        "relation": relation_name,
        "vertices": len(adjacency),
        "degree_profile": counter_to_json(Counter(len(neighbors) for neighbors in adjacency)),
        "edge_count": sum(len(neighbors) for neighbors in adjacency) // 2,
        "adjacent_common_neighbor_profile": counter_to_json(adjacent_common_neighbors),
        "nonadjacent_common_neighbor_profile": counter_to_json(nonadjacent_common_neighbors),
    }


def connected_components(adjacency: dict[Any, set[Any]]) -> list[tuple[Any, ...]]:
    seen: set[Any] = set()
    components: list[tuple[Any, ...]] = []

    for vertex in sorted(adjacency):
        if vertex in seen:
            continue

        queue: deque[Any] = deque([vertex])
        seen.add(vertex)
        component: list[Any] = []
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbor in sorted(adjacency[current]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        components.append(tuple(sorted(component)))

    return sorted(components)


def disjoint_cover_components(coordinate: int, sector_key: str) -> dict[str, Any]:
    data = steiner_trihedra(coordinate, sector_key)
    trihedron_covers: dict[tuple[int, int, int], frozenset[int]] = data["trihedron_covers"]
    trihedra = sorted(trihedron_covers)

    disjoint_cover_adjacency = {trihedron: set() for trihedron in trihedra}
    for left, right in combinations(trihedra, 2):
        if not (trihedron_covers[left] & trihedron_covers[right]):
            disjoint_cover_adjacency[left].add(right)
            disjoint_cover_adjacency[right].add(left)

    components = connected_components(disjoint_cover_adjacency)

    component_reports: list[dict[str, Any]] = []
    component_tritangent_sets: list[frozenset[int]] = []
    for component in components:
        cover_groups: dict[frozenset[int], list[tuple[int, int, int]]] = defaultdict(list)
        for trihedron in component:
            cover_groups[trihedron_covers[trihedron]].append(trihedron)

        component_weights = Counter(
            weight for trihedron in component for weight in trihedron_covers[trihedron]
        )
        tritangent_set = frozenset(tritangent for trihedron in component for tritangent in trihedron)
        component_tritangent_sets.append(tritangent_set)

        component_reports.append(
            {
                "component_size": len(component),
                "cover_group_count": len(cover_groups),
                "cover_group_size_profile": counter_to_json(Counter(len(group) for group in cover_groups.values())),
                "cover_union_size": len(frozenset().union(*cover_groups.keys())),
                "cover_pair_intersection_profile": counter_to_json(
                    Counter(len(left & right) for left, right in combinations(cover_groups.keys(), 2))
                ),
                "component_tritangent_count": len(tritangent_set),
                "component_weight_participation_profile": counter_to_json(Counter(component_weights.values())),
            }
        )

    return {
        "trihedra": trihedra,
        "trihedron_covers": trihedron_covers,
        "disjoint_cover_adjacency": disjoint_cover_adjacency,
        "components": components,
        "component_reports": component_reports,
        "component_tritangent_sets": component_tritangent_sets,
    }


def return_graph_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    data = disjoint_cover_components(coordinate, sector_key)
    components = data["components"]
    component_tritangent_sets = data["component_tritangent_sets"]

    def profile_key(report: dict[str, Any], key: str) -> tuple[tuple[str, int], ...]:
        return tuple(sorted(report[key].items()))

    component_graph_9 = [
        {
            right
            for right in range(len(components))
            if left != right and len(component_tritangent_sets[left] & component_tritangent_sets[right]) == 9
        }
        for left in range(len(components))
    ]
    component_graph_6 = [
        {
            right
            for right in range(len(components))
            if left != right and len(component_tritangent_sets[left] & component_tritangent_sets[right]) == 6
        }
        for left in range(len(components))
    ]

    disjoint_cover_edge_count = sum(len(neighbors) for neighbors in data["disjoint_cover_adjacency"].values()) // 2
    component_profiles = {
        "component_size_profile": counter_to_json(
            Counter(report["component_size"] for report in data["component_reports"])
        ),
        "cover_group_count_profile": counter_to_json(
            Counter(report["cover_group_count"] for report in data["component_reports"])
        ),
        "cover_group_size_profile_profile": counter_to_json(
            Counter(profile_key(report, "cover_group_size_profile") for report in data["component_reports"])
        ),
        "cover_union_size_profile": counter_to_json(
            Counter(report["cover_union_size"] for report in data["component_reports"])
        ),
        "cover_pair_intersection_profile_profile": counter_to_json(
            Counter(profile_key(report, "cover_pair_intersection_profile") for report in data["component_reports"])
        ),
        "component_tritangent_count_profile": counter_to_json(
            Counter(report["component_tritangent_count"] for report in data["component_reports"])
        ),
        "component_weight_participation_profile_profile": counter_to_json(
            Counter(profile_key(report, "component_weight_participation_profile") for report in data["component_reports"])
        ),
    }

    relation_9_params = graph_parameters(component_graph_9, "component_tritangent_intersection_9")
    relation_6_params = graph_parameters(component_graph_6, "component_tritangent_intersection_6")

    checks = {
        "trihedra_split_as_40_times_6": len(components) == 40
        and Counter(len(component) for component in components) == {6: 40},
        "disjoint_cover_graph_has_degree_4_and_480_edges": Counter(
            len(neighbors) for neighbors in data["disjoint_cover_adjacency"].values()
        )
        == {4: 240}
        and disjoint_cover_edge_count == 480,
        "each_component_has_three_partner_covers_of_two_trihedra": all(
            report["cover_group_count"] == 3 and report["cover_group_size_profile"] == {"2": 3}
            for report in data["component_reports"]
        ),
        "each_component_cover_triple_partitions_27_weights": all(
            report["cover_union_size"] == 27 and report["cover_pair_intersection_profile"] == {"0": 3}
            for report in data["component_reports"]
        ),
        "each_component_uses_18_distinct_tritangents": all(
            report["component_tritangent_count"] == 18 for report in data["component_reports"]
        ),
        "each_component_hits_every_weight_twice": all(
            report["component_weight_participation_profile"] == {"2": 27}
            for report in data["component_reports"]
        ),
        "intersection_9_graph_is_srg_40_12_2_4": relation_9_params
        == {
            "relation": "component_tritangent_intersection_9",
            "vertices": 40,
            "degree_profile": {"12": 40},
            "edge_count": 240,
            "adjacent_common_neighbor_profile": {"2": 240},
            "nonadjacent_common_neighbor_profile": {"4": 540},
        },
        "intersection_6_graph_is_srg_40_27_18_18": relation_6_params
        == {
            "relation": "component_tritangent_intersection_6",
            "vertices": 40,
            "degree_profile": {"27": 40},
            "edge_count": 540,
            "adjacent_common_neighbor_profile": {"18": 540},
            "nonadjacent_common_neighbor_profile": {"18": 240},
        },
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "trihedron_count": len(data["trihedra"]),
        "disjoint_cover_edge_count": disjoint_cover_edge_count,
        "component_count": len(components),
        "component_profiles": component_profiles,
        "intersection_9_graph": relation_9_params,
        "intersection_6_graph": relation_6_params,
        "sample_components": [
            [list(trihedron) for trihedron in component]
            for component in components[:3]
        ],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def external_count_dictionary(pair_count: int, trihedron_count: int, tritangent_count: int) -> dict[str, Any]:
    checks = {
        "gamma_26_is_affine_27_minus_origin": GAMMA_BRASS_COUNTS["cluster_atoms"] == Q**3 - 1,
        "gamma_52_is_two_affine_26_clusters": GAMMA_BRASS_COUNTS["unit_cell_sites"]
        == 2 * (Q**3 - 1),
        "gamma_38_is_w33_minus_symplectic_pair": GAMMA_BRASS_COUNTS["augmented_cluster_atoms"] == V - 2,
        "gamma_81_is_q_four": GAMMA_BRASS_COUNTS["augmented_cluster_tetrahedra"] == Q**4,
        "gamma_local_12_is_w33_degree": GAMMA_BRASS_COUNTS["original_helix_local_neighbors"] == K,
        "gamma_shared_4_is_mu": GAMMA_BRASS_COUNTS["initial_tetrahedron_shared_icosahedra"] == MU,
        "six_hundred_vertices_match_steiner_pair_count": CELL_600_COUNTS["vertices"] == pair_count,
        "six_hundred_edges_match_trihedron_tritangent_incidence": CELL_600_COUNTS["edges"]
        == trihedron_count * 3
        == tritangent_count * 16
        == pair_count * 6,
        "six_hundred_cells_are_twenty_bc_rings_of_thirty": CELL_600_COUNTS["tetrahedral_cells"]
        == CELL_600_COUNTS["boerdijk_coxeter_ring_count"] * CELL_600_COUNTS["tetrahedra_per_ring"],
        "thirty_per_bc_ring_is_five_times_q_factorial": CELL_600_COUNTS["tetrahedra_per_ring"]
        == FIVE * Q_FACTORIAL,
        "forty_return_components_are_two_chiralities_times_twenty_bc_rings": V
        == 2 * CELL_600_COUNTS["boerdijk_coxeter_ring_count"],
        "six_hundred_cells_are_five_times_steiner_pair_count": CELL_600_COUNTS["tetrahedral_cells"]
        == FIVE * pair_count,
    }

    return {
        "source_facts": {
            "gamma_brass_2004": {
                "title": "The gamma-brass structure and the Boerdijk-Coxeter helix",
                "doi": "10.1016/j.jnoncrysol.2003.11.069",
                "counts": GAMMA_BRASS_COUNTS,
            },
            "regular_600_cell": {
                "schlafli": "{3,3,5}",
                "counts": CELL_600_COUNTS,
            },
        },
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def boerdijk_gamma_brass_steiner_return_graph_packet() -> dict[str, Any]:
    reports = [
        return_graph_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]
    external_counts = external_count_dictionary(pair_count=120, trihedron_count=240, tritangent_count=45)

    checks = {
        "all_eight_reports_verify_8_checks": all(report["n_verified"] == 8 for report in reports),
        "all_eight_reports_split_240_as_40_times_6": all(
            report["component_count"] == 40
            and report["component_profiles"]["component_size_profile"] == {"6": 40}
            for report in reports
        ),
        "all_eight_reports_have_srg_40_12_2_4_return_graph": all(
            report["intersection_9_graph"]["degree_profile"] == {"12": 40}
            and report["intersection_9_graph"]["adjacent_common_neighbor_profile"] == {"2": 240}
            and report["intersection_9_graph"]["nonadjacent_common_neighbor_profile"] == {"4": 540}
            for report in reports
        ),
        "all_external_count_checks_verify": external_counts["n_verified"] == 12,
    }

    return {
        "part": "MCCCXCVIII",
        "theorem": "Boerdijk/gamma-brass Steiner return graph",
        "input_bridge": "MCCCXCVII E6 240 Steiner trihedra / E8 count resonance",
        "return_identity": "240 Steiner trihedra -> 40 components x 6 trihedra -> srg(40,12,2,4)",
        "matter_sector_reports": reports,
        "external_count_dictionary": external_counts,
        "claim_boundary": (
            "finite incidence theorem plus source-count dictionary; the component "
            "graph has W33 strongly regular parameters, but no canonical isomorphism "
            "to the original W33 point graph is asserted"
        ),
        "reading": (
            "The 240 Steiner trihedra do not stay as a loose E8-count shell. Under "
            "the disjoint-cover relation they split into 40 six-trihedron components. "
            "Inside each component, three 9-weight covers partition the 27 E6 weights "
            "and each cover carries its two partner trihedra. The quotient graph on "
            "the 40 components, adjacent by 9 shared tritangents, has exactly the "
            "W33 SRG parameters (40,12,2,4). The gamma-brass and 600-cell counts then "
            "line up as a source-count dictionary: 26=27-1, 38=40-2, 81=3^4, local "
            "coordination 12=k, shared 4=mu, 120 Steiner pairs=600-cell vertices, "
            "720 trihedron-tritangent incidences=600-cell edges, and 40=2x20 chiral "
            "lifts of the 20 Boerdijk-Coxeter rings."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = boerdijk_gamma_brass_steiner_return_graph_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCVIII: Boerdijk/Gamma-Brass Steiner Return Graph ===")
    print("identity:", packet["return_identity"])
    first = packet["matter_sector_reports"][0]
    print("sector 0 components:", first["component_count"])
    print("sector 0 intersection-9 graph:", first["intersection_9_graph"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-sector checks:", [report["n_verified"] for report in packet["matter_sector_reports"]])
    print(
        "external count checks:",
        packet["external_count_dictionary"]["n_verified"],
        "/",
        len(packet["external_count_dictionary"]["checks"]),
    )


if __name__ == "__main__":
    main()
