#!/usr/bin/env python3
"""Exact Witting "quantum cards" deck-control audit for W(3,3).

This audit isolates the operational layer suggested by the 2025 communication
paper on the Witting polytope and folds it into the exact qutrit kernel already
proved in the repo.

Exact content:
1. The 40 Witting rays are the 40 projective points of W(3,3).
2. The 40 orthogonal Witting tetrads are the 40 isotropic lines / rank slots.
3. The 36 symplectic spreads are therefore exactly 36 full "decks":
   each deck partitions the 40 cards into 10 orthogonal tetrad ranks.
4. Deck-deck overlap is rigid: two distinct decks share either 1 or 4 ranks.
5. The overlap-1 deck graph is SRG(36,20,10,12) and has 216 maximal 5-deck
   sweeps that cover all 40 ranks.
6. The overlap-4 deck graph is SRG(36,15,6,6) and has 135 maximal 4-deck
   control packets supported on 24 ranks.

The point is not new phenomenology. It is that the "quantum cards" picture is
already the exact spread-control layer of the same finite geometry.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from exploration.w33_witting_srg_bridge import (  # noqa: E402
    construct_witting_rays,
    mapped_witting_lines,
    symplectic_lines,
    witting_orthogonal_tetrads,
)
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402


Deck = tuple[int, ...]


def _deck_rank_incidence(decks: list[Deck], rank_count: int) -> np.ndarray:
    incidence = np.zeros((rank_count, len(decks)), dtype=int)
    for deck_index, deck in enumerate(decks):
        for rank_index in deck:
            incidence[rank_index, deck_index] = 1
    return incidence


def _adjacency_sets_from_overlap(overlaps: np.ndarray, overlap_value: int) -> tuple[frozenset[int], ...]:
    size = overlaps.shape[0]
    adjacency = [set() for _ in range(size)]
    for left, right in combinations(range(size), 2):
        if int(overlaps[left, right]) == overlap_value:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(neighbors) for neighbors in adjacency)


def _adjacency_matrix(adjacency: tuple[frozenset[int], ...]) -> np.ndarray:
    size = len(adjacency)
    matrix = np.zeros((size, size), dtype=int)
    for left, neighbors in enumerate(adjacency):
        for right in neighbors:
            matrix[left, right] = 1
    return matrix


def _srg_parameters(adjacency: tuple[frozenset[int], ...]) -> dict[str, int]:
    degrees = {len(neighbors) for neighbors in adjacency}
    if len(degrees) != 1:
        raise ValueError("graph is not regular")

    lambda_values = set()
    mu_values = set()
    for left, right in combinations(range(len(adjacency)), 2):
        common = len(adjacency[left] & adjacency[right])
        if right in adjacency[left]:
            lambda_values.add(common)
        else:
            mu_values.add(common)
    if len(lambda_values) != 1 or len(mu_values) != 1:
        raise ValueError("graph is not strongly regular")

    return {
        "n": len(adjacency),
        "k": next(iter(degrees)),
        "lambda": next(iter(lambda_values)),
        "mu": next(iter(mu_values)),
    }


def _all_pairwise_cliques(adjacency: tuple[frozenset[int], ...], clique_size: int) -> list[tuple[int, ...]]:
    vertices = range(len(adjacency))
    return [
        tuple(choice)
        for choice in combinations(vertices, clique_size)
        if all(right in adjacency[left] for left, right in combinations(choice, 2))
    ]


def _common_neighbors(clique: tuple[int, ...], adjacency: tuple[frozenset[int], ...]) -> set[int]:
    if not clique:
        return set()
    neighbors = set(adjacency[clique[0]])
    for vertex in clique[1:]:
        neighbors &= set(adjacency[vertex])
    return neighbors - set(clique)


def _packet_profile(cliques: list[tuple[int, ...]], decks: list[Deck]) -> dict[str, Any]:
    union_sizes = Counter()
    common_rank_counts = Counter()
    multiplicity_profiles = Counter()
    deck_incidence = Counter()
    edge_incidence = Counter()

    for clique in cliques:
        rank_counts = Counter(rank for deck_index in clique for rank in decks[deck_index])
        union_sizes[len(rank_counts)] += 1
        common_rank_counts[sum(1 for count in rank_counts.values() if count == len(clique))] += 1
        multiplicity_profiles[tuple(sorted(Counter(rank_counts.values()).items()))] += 1
        for deck_index in clique:
            deck_incidence[deck_index] += 1
        for edge in combinations(clique, 2):
            edge_incidence[tuple(sorted(edge))] += 1

    return {
        "count": len(cliques),
        "union_sizes": dict(union_sizes),
        "common_rank_counts": dict(common_rank_counts),
        "rank_multiplicity_profiles": {
            str(key): value for key, value in sorted(multiplicity_profiles.items())
        },
        "decks_per_packet_distribution": dict(Counter(deck_incidence.values())),
        "edges_per_packet_distribution": dict(Counter(edge_incidence.values())),
        "sample_packets": [tuple(clique) for clique in cliques[:5]],
    }


def classify_witting_deck_control() -> list[dict[str, Any]]:
    payload = analyze()
    return [
        {"name": "exact_witting_card_decks", "evidence": payload["witting_deck_dictionary"]},
        {"name": "exact_deck_overlap_graphs", "evidence": payload["deck_overlap_dictionary"]},
        {"name": "exact_5deck_global_sweeps", "evidence": payload["maximal_pentad_dictionary"]},
        {"name": "exact_4deck_local_control_packets", "evidence": payload["maximal_tetra_dictionary"]},
    ]


@lru_cache(maxsize=1)
def analyze() -> dict[str, Any]:
    rank_lines = list(symplectic_lines())
    spreads = symplectic_spreads(rank_lines, n_points=40)
    witting_rays = construct_witting_rays()
    witting_tetrads = witting_orthogonal_tetrads()
    mapped_tetrads = mapped_witting_lines()

    incidence = _deck_rank_incidence(spreads, rank_count=len(rank_lines))
    rank_decks = incidence.sum(axis=1)
    deck_ranks = incidence.sum(axis=0)
    overlaps = incidence.T @ incidence
    overlap_distribution = Counter(int(overlaps[left, right]) for left, right in combinations(range(len(spreads)), 2))

    overlap_1 = _adjacency_sets_from_overlap(overlaps, overlap_value=1)
    overlap_4 = _adjacency_sets_from_overlap(overlaps, overlap_value=4)
    overlap_1_matrix = _adjacency_matrix(overlap_1)
    overlap_4_matrix = _adjacency_matrix(overlap_4)

    pentads = _all_pairwise_cliques(overlap_1, clique_size=5)
    tetra_packets = _all_pairwise_cliques(overlap_4, clique_size=4)
    pentad_extensions = Counter(len(_common_neighbors(clique, overlap_1)) for clique in pentads)
    tetra_extensions = Counter(len(_common_neighbors(clique, overlap_4)) for clique in tetra_packets)

    pentad_profile = _packet_profile(pentads, spreads)
    tetra_profile = _packet_profile(tetra_packets, spreads)

    theorem = {
        "the_40_witting_cards_and_40_orthogonal_tetrads_match_the_exact_w33_rank_space": (
            len(witting_rays) == 40
            and len(witting_tetrads) == 40
            and tuple(rank_lines) == mapped_tetrads
        ),
        "the_36_spreads_are_exactly_36_full_witting_decks_of_10_tetrad_ranks": (
            len(spreads) == 36
            and all(len(deck) == 10 for deck in spreads)
            and bool(np.array_equal(deck_ranks, np.full(36, 10, dtype=int)))
        ),
        "every_witting_tetrad_rank_occurs_in_exactly_9_decks": (
            bool(np.array_equal(rank_decks, np.full(40, 9, dtype=int)))
        ),
        "deck_deck_overlap_is_rigidly_1_or_4_tetrad_ranks": (
            overlap_distribution == Counter({1: 360, 4: 270})
        ),
        "the_overlap_1_deck_graph_is_srg_36_20_10_12_and_has_216_maximal_5deck_sweeps": (
            _srg_parameters(overlap_1) == {"n": 36, "k": 20, "lambda": 10, "mu": 12}
            and len(pentads) == 216
            and pentad_extensions == Counter({0: 216})
        ),
        "the_overlap_4_deck_graph_is_srg_36_15_6_6_and_has_135_maximal_4deck_control_packets": (
            _srg_parameters(overlap_4) == {"n": 36, "k": 15, "lambda": 6, "mu": 6}
            and len(tetra_packets) == 135
            and tetra_extensions == Counter({0: 135})
        ),
        "the_5deck_sweeps_cover_all_40_tetrad_ranks_with_profile_30_single_plus_10_double": (
            pentad_profile["union_sizes"] == {40: 216}
            and pentad_profile["common_rank_counts"] == {0: 216}
            and pentad_profile["rank_multiplicity_profiles"] == {"((1, 30), (2, 10))": 216}
            and pentad_profile["decks_per_packet_distribution"] == {30: 36}
            and pentad_profile["edges_per_packet_distribution"] == {6: 360}
        ),
        "the_4deck_control_packets_have_24rank_support_with_profile_16_single_plus_8_triple": (
            tetra_profile["union_sizes"] == {24: 135}
            and tetra_profile["common_rank_counts"] == {0: 135}
            and tetra_profile["rank_multiplicity_profiles"] == {"((1, 16), (3, 8))": 135}
            and tetra_profile["decks_per_packet_distribution"] == {15: 36}
            and tetra_profile["edges_per_packet_distribution"] == {3: 270}
        ),
    }
    theorem["the_witting_quantum_cards_picture_is_exactly_the_spread_control_layer_of_w33"] = all(
        theorem.values()
    )

    return {
        "status": "ok",
        "witting_deck_dictionary": {
            "quantum_card_count": len(witting_rays),
            "orthogonal_tetrad_rank_count": len(witting_tetrads),
            "cards_per_rank": 4,
            "ranks_through_each_card": 4,
            "deck_count": len(spreads),
            "ranks_per_deck": int(deck_ranks[0]),
            "decks_per_rank": int(rank_decks[0]),
            "mapped_witting_tetrads_equal_symplectic_ranks": mapped_tetrads == tuple(rank_lines),
            "decks_partition_all_40_cards": all(
                len({point for rank_index in deck for point in rank_lines[rank_index]}) == 40
                for deck in spreads
            ),
        },
        "deck_overlap_dictionary": {
            "pairwise_rank_overlap_distribution": dict(overlap_distribution),
            "overlap_1_srg_parameters": _srg_parameters(overlap_1),
            "overlap_4_srg_parameters": _srg_parameters(overlap_4),
            "overlap_1_spectrum": [int(value) for value in np.rint(np.linalg.eigvalsh(overlap_1_matrix))],
            "overlap_4_spectrum": [int(value) for value in np.rint(np.linalg.eigvalsh(overlap_4_matrix))],
        },
        "maximal_pentad_dictionary": pentad_profile,
        "maximal_tetra_dictionary": tetra_profile,
        "witting_deck_control_theorem": theorem,
        "bridge_verdict": (
            "The Witting communication picture is now exact on the finite side. The 40 "
            "quantum cards are the 40 Witting rays, the 40 tetrads are the exact rank "
            "slots, and the 36 symplectic spreads are exactly 36 full decks partitioning "
            "the cards into 10 orthogonal ranks. On deck space the control geometry is "
            "rigid: overlaps are only 1 or 4 ranks, the overlap-1 graph is SRG(36,20,10,12) "
            "with 216 maximal 5-deck sweeps covering all 40 ranks, and the overlap-4 graph "
            "is SRG(36,15,6,6) with 135 maximal 4-deck packets supported on 24 ranks. So "
            "the original 'quantum cards' perspective is not a side metaphor; it is the "
            "exact spread-control layer of the same W(3,3) kernel."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXVII_witting_deck_control_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("W33 Witting deck-control audit")
    for key, value in payload["witting_deck_control_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
