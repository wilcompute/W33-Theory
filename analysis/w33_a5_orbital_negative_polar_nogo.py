"""Part MMCCCLXVIII: A5 orbital selector no-go.

MDCLXXXIII showed that the 60 Clifford antipodal addresses form A5 in its
degree-six action, and that the 36 raw L/R cells are the fibers g(i)=j.
MDCLXXXIV showed that the W33 spread graph is the negative-polar graph
NO^-(6,2), not a 6x6 Latin-square graph.

This verifier closes the tempting intermediate path:

    "Maybe the missing selector is just a diagonal-A5-invariant orbital
     graph on the 36 raw L/R cells."

It is not.  The diagonal A5 action on the 36 cells has 16 unordered pair
orbitals.  There is exactly one union of those orbitals with the SRG
parameters (36,15,6,6), and it is the Latin/rook completion: it contains all
row/column rook edges and therefore has K6 cliques.  The W33 negative-polar
spread graph has clique number 4.

So the W33 selector cannot be recovered by selecting diagonal A5 orbitals on
the raw Clifford grid.  The missing twist must break the raw diagonal grid
symmetry, or conjugate it through a nontrivial negative-polar/symplectic
relabeling.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_clifford_antipodal_a5_selector_group import (  # noqa: E402
    clifford_antipodal_permutations,
)
from analysis.w33_spread_negative_polar_selector_signature import (  # noqa: E402
    adjacency_from_edges,
    clique_number,
    graph_parameters,
    no_minus_6_2_graph,
    rook_6_by_6_graph,
    w33_spread_graph,
)


OUTPUT_PATH = ROOT / "PART_MMCCCLXVIII_A5_ORBITAL_NEGATIVE_POLAR_NOGO_results.json"
EXPECTED_SRG_36_15_6_6 = {
    "vertices": 36,
    "degree_profile": {"15": 36},
    "edge_count": 270,
    "adjacent_common_neighbor_profile": {"6": 270},
    "nonadjacent_common_neighbor_profile": {"6": 360},
}


Cell = tuple[int, int]
Edge = tuple[int, int]
Permutation = tuple[int, ...]


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def cells() -> list[Cell]:
    return [(row, column) for row in range(6) for column in range(6)]


def cell_index() -> dict[Cell, int]:
    return {cell: index for index, cell in enumerate(cells())}


def sorted_a5_permutations() -> list[Permutation]:
    return sorted(set(clifford_antipodal_permutations().values()))


def transform_cell(cell: Cell, permutation: Permutation) -> Cell:
    return permutation[cell[0]], permutation[cell[1]]


def transform_edge(edge: Edge, permutation: Permutation) -> Edge:
    indexed_cells = cell_index()
    cell_list = cells()
    left, right = edge
    image_left = indexed_cells[transform_cell(cell_list[left], permutation)]
    image_right = indexed_cells[transform_cell(cell_list[right], permutation)]
    return tuple(sorted((image_left, image_right)))


def diagonal_a5_pair_orbits() -> list[frozenset[Edge]]:
    permutations = sorted_a5_permutations()
    unseen: set[Edge] = set(combinations(range(36), 2))
    orbits: list[frozenset[Edge]] = []

    while unseen:
        seed = min(unseen)
        orbit = {transform_edge(seed, permutation) for permutation in permutations}
        # One pass is enough for a group action, but the closure loop makes the
        # certificate independent of any future ordering changes upstream.
        changed = True
        while changed:
            changed = False
            for edge in list(orbit):
                for permutation in permutations:
                    image = transform_edge(edge, permutation)
                    if image not in orbit:
                        orbit.add(image)
                        changed = True

        unseen -= orbit
        orbits.append(frozenset(orbit))

    return sorted(orbits, key=lambda orbit: min(orbit))


def orbit_report(orbits: list[frozenset[Edge]]) -> list[dict[str, Any]]:
    cell_list = cells()
    report = []
    for index, orbit in enumerate(orbits):
        degrees: Counter[int] = Counter()
        for left, right in orbit:
            degrees[left] += 1
            degrees[right] += 1
        representative = min(orbit)
        report.append(
            {
                "index": index,
                "representative_edge": list(representative),
                "representative_cells": [list(cell_list[representative[0]]), list(cell_list[representative[1]])],
                "size": len(orbit),
                "degree_profile": counter_to_json(Counter(degrees.values())),
            }
        )
    return report


def adjacency_from_orbit_indices(orbits: list[frozenset[Edge]], indices: list[int]) -> list[int]:
    edges: set[Edge] = set()
    for index in indices:
        edges.update(orbits[index])
    return adjacency_from_edges(36, sorted(edges))


def edge_set(adjacency: list[int]) -> set[Edge]:
    return {
        (left, right)
        for left, right in combinations(range(len(adjacency)), 2)
        if (adjacency[left] >> right) & 1
    }


def orbit_indices_for_graph(orbits: list[frozenset[Edge]], adjacency: list[int]) -> list[int]:
    edges = edge_set(adjacency)
    return [index for index, orbit in enumerate(orbits) if set(orbit) <= edges]


def a5_orbital_srg_solutions(orbits: list[frozenset[Edge]]) -> list[list[int]]:
    solutions: list[list[int]] = []
    orbit_sizes = [len(orbit) for orbit in orbits]

    for mask in range(1, 1 << len(orbits)):
        if sum(orbit_sizes[index] for index in range(len(orbits)) if (mask >> index) & 1) != 270:
            continue
        indices = [index for index in range(len(orbits)) if (mask >> index) & 1]
        adjacency = adjacency_from_orbit_indices(orbits, indices)
        if graph_parameters(adjacency) == EXPECTED_SRG_36_15_6_6:
            solutions.append(indices)

    return solutions


def a5_orbital_negative_polar_nogo_packet() -> dict[str, Any]:
    orbits = diagonal_a5_pair_orbits()
    rook_graph = rook_6_by_6_graph()
    w33_graph, _ = w33_spread_graph()
    negative_polar_graph, _ = no_minus_6_2_graph()

    rook_indices = orbit_indices_for_graph(orbits, rook_graph)
    solutions = a5_orbital_srg_solutions(orbits)
    selected_indices = solutions[0]
    selected_graph = adjacency_from_orbit_indices(orbits, selected_indices)
    selected_extra_indices = [index for index in selected_indices if index not in rook_indices]

    selected_clique_number = clique_number(selected_graph)
    w33_clique_number = clique_number(w33_graph)
    negative_polar_clique_number = clique_number(negative_polar_graph)

    checks = {
        "diagonal_a5_has_16_pair_orbitals": len(orbits) == 16,
        "orbitals_partition_all_630_cell_pairs": sum(len(orbit) for orbit in orbits) == 630,
        "raw_rook_graph_is_six_a5_orbitals": rook_indices == [0, 1, 5, 6, 10, 14],
        "unique_a5_orbital_srg_36_15_6_6_solution": solutions == [[0, 1, 2, 5, 6, 7, 10, 12, 14]],
        "a5_solution_is_rook_plus_three_orbitals": selected_extra_indices == [2, 7, 12],
        "a5_solution_has_target_srg_parameters": graph_parameters(selected_graph) == EXPECTED_SRG_36_15_6_6,
        "a5_solution_contains_raw_rook_edges": edge_set(rook_graph) < edge_set(selected_graph),
        "a5_solution_has_k6_cliques": selected_clique_number == 6,
        "w33_negative_polar_has_clique_number_4": w33_clique_number == negative_polar_clique_number == 4,
        "a5_orbital_solution_is_not_w33_negative_polar": selected_clique_number != w33_clique_number,
    }

    return {
        "part": "MMCCCLXVIII",
        "theorem": "A5 orbital selector no-go",
        "input_bridge": "MDCLXXXIII A5 torsor + MDCLXXXIV NO^-(6,2) W33 spread selector",
        "n_pair_orbitals": len(orbits),
        "orbit_size_profile": counter_to_json(Counter(len(orbit) for orbit in orbits)),
        "orbit_report": orbit_report(orbits),
        "raw_rook_orbit_indices": rook_indices,
        "raw_rook_edge_count": len(edge_set(rook_graph)),
        "a5_orbital_srg_solution_count": len(solutions),
        "a5_orbital_srg_solution_indices": selected_indices,
        "a5_orbital_srg_extra_indices_beyond_rook": selected_extra_indices,
        "a5_orbital_srg_parameters": graph_parameters(selected_graph),
        "a5_orbital_srg_clique_number": selected_clique_number,
        "w33_negative_polar_clique_number": w33_clique_number,
        "negative_polar_model_clique_number": negative_polar_clique_number,
        "selector_nogo": (
            "The unique diagonal-A5 orbital union with srg(36,15,6,6) "
            "parameters is the Latin/rook completion with K6 cliques, not "
            "the W33 NO^-(6,2) spread graph."
        ),
        "claim_boundary": (
            "rules out only raw diagonal-A5 orbital selection on the 6x6 "
            "Clifford cells; it does not rule out a non-diagonal A5 subgroup "
            "inside the negative-polar O^-(6,2) action or a symplectic relabeling"
        ),
        "reading": (
            "The A5 torsor found in MDCLXXXIII is real, but keeping its diagonal "
            "action on the 36 L/R cells is too rigid. Its 16 pair-orbitals have "
            "exactly one union with the same SRG parameters as W33 spreads. That "
            "union contains all 180 raw rook edges and adds three extra orbitals "
            "of sizes 15,15,60, so it has row and column K6 cliques. The W33 "
            "spread graph, identified in MDCLXXXIV with NO^-(6,2), has clique "
            "number 4. Therefore the missing selector is not an A5 orbital pick "
            "on the raw grid; it must be a genuine negative-polar/symplectic "
            "twist of the cell labels."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = a5_orbital_negative_polar_nogo_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MMCCCLXVIII: A5 Orbital Negative-Polar No-Go ===")
    print("pair orbitals:", packet["n_pair_orbitals"])
    print("rook orbitals:", packet["raw_rook_orbit_indices"])
    print("unique A5 SRG solution:", packet["a5_orbital_srg_solution_indices"])
    print("A5 solution clique number:", packet["a5_orbital_srg_clique_number"])
    print("W33 negative-polar clique number:", packet["w33_negative_polar_clique_number"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} checks")


if __name__ == "__main__":
    main()
