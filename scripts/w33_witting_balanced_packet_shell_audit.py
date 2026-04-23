#!/usr/bin/env python3
"""Exact balanced-packet shell audit for the Witting deck-control layer.

This audit sharpens the deck-control story one level further.

Starting from the 36 full Witting/W(3,3) decks:
1. Relative to any anchor point, the decks split into four sectors of 9,
   one sector for each anchor line.
2. Inside each 9-deck sector, the overlap-1 graph is exactly three disjoint
   triangles.
3. The 135 maximal 4-deck control packets split as:
      135 = 27 balanced + 108 skew.
   The 27 balanced packets contain exactly one deck from each of the four
   sectors.
4. Those 27 balanced packets are not just another 27-count shadow:
   - deck-overlap-1 on the balanced packets is isomorphic to the exact local
     27-point H27 shell,
   - rank-intersection-14 on the same packets is the Schläfli graph
     SRG(27,16,10,8),
   - rank-intersection-16 is its complement SRG(27,10,1,5).

So the communication/deck layer does not merely sit above the qutrit kernel.
It folds back into the exact local cubic-surface shell.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any

import networkx as nx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_witting_srg_bridge import symplectic_lines  # noqa: E402
from scripts.w33_heisenberg_qutrit import compute_local_structure  # noqa: E402
from scripts.w33_homology import build_w33  # noqa: E402
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402


Deck = tuple[int, ...]
Packet = tuple[int, ...]


def _deck_rank_incidence(decks: list[Deck], rank_count: int) -> np.ndarray:
    incidence = np.zeros((rank_count, len(decks)), dtype=int)
    for deck_index, deck in enumerate(decks):
        for rank_index in deck:
            incidence[rank_index, deck_index] = 1
    return incidence


def _graph_from_predicate(size: int, predicate) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(size))
    for left, right in combinations(range(size), 2):
        if predicate(left, right):
            graph.add_edge(left, right)
    return graph


def _srg_parameters(graph: nx.Graph) -> dict[str, Any]:
    degrees = {degree for _, degree in graph.degree()}
    if len(degrees) != 1:
        raise ValueError("graph is not regular")

    lambda_values = set()
    mu_values = set()
    vertices = list(graph.nodes())
    for left, right in combinations(vertices, 2):
        common = len(set(graph.neighbors(left)) & set(graph.neighbors(right)))
        if graph.has_edge(left, right):
            lambda_values.add(common)
        else:
            mu_values.add(common)

    payload: dict[str, Any] = {
        "n": graph.number_of_nodes(),
        "k": next(iter(degrees)),
    }
    if len(lambda_values) == 1 and len(mu_values) == 1:
        payload["lambda"] = next(iter(lambda_values))
        payload["mu"] = next(iter(mu_values))
        payload["is_strongly_regular"] = True
    else:
        payload["lambda_values"] = sorted(lambda_values)
        payload["mu_values"] = sorted(mu_values)
        payload["is_strongly_regular"] = False
    return payload


def _connected_components(graph: nx.Graph) -> list[tuple[int, ...]]:
    return [tuple(sorted(component)) for component in nx.connected_components(graph)]


def _sector_triangle_partition(
    sectors: dict[int, list[int]],
    overlaps: np.ndarray,
) -> dict[int, list[tuple[int, ...]]]:
    partitions: dict[int, list[tuple[int, ...]]] = {}
    for sector_index, deck_indices in sectors.items():
        graph = _graph_from_predicate(
            len(deck_indices),
            lambda left, right, deck_indices=deck_indices: (
                int(overlaps[deck_indices[left], deck_indices[right]]) == 1
            ),
        )
        relabeled = {local_index: deck_indices[local_index] for local_index in range(len(deck_indices))}
        sector_graph = nx.relabel_nodes(graph, relabeled)
        partitions[sector_index] = sorted(_connected_components(sector_graph))
    return partitions


def _all_four_cliques(graph: nx.Graph) -> list[Packet]:
    return [
        tuple(choice)
        for choice in combinations(sorted(graph.nodes()), 4)
        if all(graph.has_edge(left, right) for left, right in combinations(choice, 2))
    ]


def _balanced_and_skew_packets(
    packets: list[Packet],
    sectors: dict[int, list[int]],
) -> tuple[list[Packet], list[Packet], Counter]:
    deck_to_sector = {
        deck_index: sector_index
        for sector_index, deck_indices in sectors.items()
        for deck_index in deck_indices
    }
    balanced: list[Packet] = []
    skew: list[Packet] = []
    profile = Counter()
    for packet in packets:
        sector_counts = Counter(deck_to_sector[deck_index] for deck_index in packet)
        normalized = tuple(sorted(sector_counts.items()))
        profile[normalized] += 1
        if sector_counts == Counter({0: 1, 1: 1, 2: 1, 3: 1}):
            balanced.append(packet)
        else:
            skew.append(packet)
    return balanced, skew, profile


def _balanced_packet_chart(
    balanced_packets: list[Packet],
    sectors: dict[int, list[int]],
    sector_triangles: dict[int, list[tuple[int, ...]]],
) -> dict[str, Any]:
    triangle_lookup = {
        sector_index: {
            deck_index: triangle_index
            for triangle_index, triangle in enumerate(sector_triangles[sector_index])
            for deck_index in triangle
        }
        for sector_index in sectors
    }

    triangle_pattern_counts = Counter()
    local_state_counts = Counter()
    triangle_to_local_states: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)

    for packet in balanced_packets:
        by_sector = {
            sector_index: next(deck for deck in packet if deck in sectors[sector_index])
            for sector_index in range(4)
        }
        triangle_pattern = tuple(triangle_lookup[sector_index][by_sector[sector_index]] for sector_index in range(4))
        local_state = tuple(
            sector_triangles[sector_index][triangle_pattern[sector_index]].index(by_sector[sector_index])
            for sector_index in range(4)
        )
        triangle_pattern_counts[triangle_pattern] += 1
        local_state_counts[local_state] += 1
        triangle_to_local_states[triangle_pattern].append(local_state)

    local_state_multiplicities = Counter(len(states) for states in triangle_to_local_states.values())

    return {
        "triangle_pattern_count": len(triangle_pattern_counts),
        "triangle_pattern_multiplicity_distribution": dict(Counter(triangle_pattern_counts.values())),
        "local_state_pattern_count": len(local_state_counts),
        "local_state_multiplicity_distribution": dict(Counter(local_state_counts.values())),
        "triangle_to_local_state_count_distribution": dict(local_state_multiplicities),
        "sample_triangle_patterns": [tuple(pattern) for pattern in sorted(triangle_pattern_counts)[:5]],
        "sample_local_states": [tuple(state) for state in sorted(local_state_counts)[:5]],
    }


def _balanced_packet_rank_unions(balanced_packets: list[Packet], decks: list[Deck]) -> list[set[int]]:
    return [{rank for deck_index in packet for rank in decks[deck_index]} for packet in balanced_packets]


def _build_local_shell_graphs(base_vertex: int = 0) -> tuple[nx.Graph, nx.Graph, nx.Graph]:
    n_vertices, _vertices, adjacency, _edges = build_w33()
    adjacency_sets = [set(row) for row in adjacency]
    _neighbors, nonneighbors, _triangles, _h27_neighbors = compute_local_structure(
        base_vertex, n_vertices, adjacency_sets
    )

    local_shell = nx.Graph()
    local_shell.add_nodes_from(range(len(nonneighbors)))
    for left, vertex_left in enumerate(nonneighbors):
        for right, vertex_right in enumerate(nonneighbors[left + 1 :], start=left + 1):
            if vertex_right in adjacency_sets[vertex_left]:
                local_shell.add_edge(left, right)

    nonneighbor_set = set(nonneighbors)
    schlafli = nx.Graph()
    schlafli.add_nodes_from(range(len(nonneighbors)))
    for left, vertex_left in enumerate(nonneighbors):
        for right, vertex_right in enumerate(nonneighbors[left + 1 :], start=left + 1):
            common = len((adjacency_sets[vertex_left] & adjacency_sets[vertex_right]) & nonneighbor_set)
            if common == 3:
                schlafli.add_edge(left, right)

    return local_shell, schlafli, nx.complement(schlafli)


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    decks = symplectic_spreads(list(symplectic_lines()), n_points=40)
    rank_count = 40
    incidence = _deck_rank_incidence(decks, rank_count=rank_count)
    overlaps = incidence.T @ incidence

    anchor_line_indices = [index for index, line in enumerate(symplectic_lines()) if 0 in line]
    sectors = {
        sector_index: [deck_index for deck_index, deck in enumerate(decks) if anchor_line_index in deck]
        for sector_index, anchor_line_index in enumerate(anchor_line_indices)
    }
    sector_triangles = _sector_triangle_partition(sectors, overlaps)

    overlap4_graph = _graph_from_predicate(
        len(decks), lambda left, right: int(overlaps[left, right]) == 4
    )
    packets = _all_four_cliques(overlap4_graph)
    balanced_packets, skew_packets, packet_sector_profiles = _balanced_and_skew_packets(packets, sectors)
    chart = _balanced_packet_chart(balanced_packets, sectors, sector_triangles)

    balanced_rank_unions = _balanced_packet_rank_unions(balanced_packets, decks)
    balanced_deck_overlap1_graph = _graph_from_predicate(
        len(balanced_packets),
        lambda left, right: len(set(balanced_packets[left]) & set(balanced_packets[right])) == 1,
    )
    balanced_rank14_graph = _graph_from_predicate(
        len(balanced_packets),
        lambda left, right: len(balanced_rank_unions[left] & balanced_rank_unions[right]) == 14,
    )
    balanced_rank16_graph = _graph_from_predicate(
        len(balanced_packets),
        lambda left, right: len(balanced_rank_unions[left] & balanced_rank_unions[right]) == 16,
    )

    local_shell_graph, schlafli_graph, intersection_graph = _build_local_shell_graphs()

    theorem = {
        "the_36_decks_split_as_four_anchor_sectors_of_size_9": (
            tuple(sorted(len(deck_indices) for deck_indices in sectors.values())) == (9, 9, 9, 9)
        ),
        "inside_each_9deck_sector_the_overlap1_graph_is_three_disjoint_triangles": (
            all(
                sorted(len(component) for component in sector_triangles[sector_index]) == [3, 3, 3]
                for sector_index in sectors
            )
        ),
        "the_135_fourdeck_packets_split_as_27_balanced_plus_108_skew": (
            len(packets) == 135 and len(balanced_packets) == 27 and len(skew_packets) == 108
        ),
        "the_27_balanced_packets_factor_as_9_sector_triangle_patterns_times_3_internal_states": (
            chart["triangle_pattern_count"] == 9
            and chart["triangle_pattern_multiplicity_distribution"] == {3: 9}
            and chart["triangle_to_local_state_count_distribution"] == {3: 9}
        ),
        "deck_overlap_1_on_the_balanced_packets_is_isomorphic_to_the_exact_local_h27_shell": (
            _srg_parameters(balanced_deck_overlap1_graph)
            == {"n": 27, "k": 8, "lambda_values": [1], "mu_values": [0, 3], "is_strongly_regular": False}
            and nx.is_isomorphic(balanced_deck_overlap1_graph, local_shell_graph)
        ),
        "rank_intersection_14_on_the_balanced_packets_is_the_schlafli_graph": (
            _srg_parameters(balanced_rank14_graph)
            == {"n": 27, "k": 16, "lambda": 10, "mu": 8, "is_strongly_regular": True}
            and nx.is_isomorphic(balanced_rank14_graph, schlafli_graph)
        ),
        "rank_intersection_16_on_the_balanced_packets_is_the_intersection_graph": (
            _srg_parameters(balanced_rank16_graph)
            == {"n": 27, "k": 10, "lambda": 1, "mu": 5, "is_strongly_regular": True}
            and nx.is_isomorphic(balanced_rank16_graph, intersection_graph)
        ),
    }
    theorem["the_balanced_packet_shell_reconstructs_the_local_cubic_surface_layer"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "anchor_sector_dictionary": {
            "anchor_line_indices": anchor_line_indices,
            "sector_sizes": {str(sector_index): len(deck_indices) for sector_index, deck_indices in sectors.items()},
            "sector_triangle_components": {
                str(sector_index): [tuple(component) for component in sector_triangles[sector_index]]
                for sector_index in sectors
            },
        },
        "fourdeck_packet_dictionary": {
            "packet_count": len(packets),
            "balanced_packet_count": len(balanced_packets),
            "skew_packet_count": len(skew_packets),
            "sector_profile_distribution": {str(key): value for key, value in sorted(packet_sector_profiles.items())},
        },
        "balanced_packet_chart": chart,
        "balanced_packet_graphs": {
            "deck_overlap_distribution": dict(
                Counter(
                    len(set(balanced_packets[left]) & set(balanced_packets[right]))
                    for left, right in combinations(range(len(balanced_packets)), 2)
                )
            ),
            "rank_intersection_distribution": dict(
                Counter(
                    len(balanced_rank_unions[left] & balanced_rank_unions[right])
                    for left, right in combinations(range(len(balanced_packets)), 2)
                )
            ),
            "balanced_shell_parameters": _srg_parameters(balanced_deck_overlap1_graph),
            "balanced_rank14_parameters": _srg_parameters(balanced_rank14_graph),
            "balanced_rank16_parameters": _srg_parameters(balanced_rank16_graph),
            "isomorphic_to_local_shell": nx.is_isomorphic(balanced_deck_overlap1_graph, local_shell_graph),
            "isomorphic_to_schlafli": nx.is_isomorphic(balanced_rank14_graph, schlafli_graph),
            "isomorphic_to_intersection_graph": nx.is_isomorphic(balanced_rank16_graph, intersection_graph),
        },
        "balanced_packet_shell_theorem": theorem,
        "bridge_verdict": (
            "The new deck-control layer closes back onto the old local E6 shell. Relative to a "
            "chosen anchor point the 36 decks split into four 9-deck sectors, each sector breaks "
            "into three overlap-1 triangles, and the 135 four-deck packets split as 27 balanced "
            "plus 108 skew. The 27 balanced packets are exactly the missing bridge: their raw "
            "deck-overlap graph is isomorphic to the honest 8-regular H27 shell, while two "
            "different exact rank-intersection relations on the same 27 packets recover the "
            "Schläfli graph and its intersection complement. So the Witting communication layer "
            "is not merely compatible with the local cubic-surface layer; it reconstructs it."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXVIII_witting_balanced_packet_shell_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting balanced-packet shell audit")
    for key, value in payload["balanced_packet_shell_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
