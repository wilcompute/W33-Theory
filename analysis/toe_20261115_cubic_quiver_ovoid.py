"""Verify minimal reconstructions of the Dickson cubic from quiver supports."""

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import networkx as nx

from toe_20261115_cubic_quiver_steiner import intersection, line_class, projective_points


DATA = Path(__file__).resolve().parents[1] / "data"


def verify(certificate):
    masks = [int(mask, 16) for mask in certificate["orbit_supports_hex_masks"]]
    supports = [{i for i in range(45) if mask & (1 << i)} for mask in masks]
    assert len(supports) == 40 and all(len(support) == 27 for support in supports)
    assert Counter(i for support in supports for i in support) == {i: 24 for i in range(45)}

    adjacency = nx.Graph()
    adjacency.add_nodes_from(range(40))
    for (a, left), (b, right) in combinations(enumerate(supports), 2):
        overlap = len(left & right)
        assert overlap in (15, 18)
        if overlap == 18:
            adjacency.add_edge(a, b)
    polar_lines = [set(clique) for clique in nx.find_cliques(adjacency)]
    assert len(polar_lines) == 40 and all(len(line) == 4 for line in polar_lines)
    point_line_incidence = [{j for j, line in enumerate(polar_lines) if i in line} for i in range(40)]
    for a in range(40):
        for b in range(40):
            assert len(supports[a] & supports[b]) == 15 + 3*len(point_line_incidence[a] & point_line_incidence[b])
    cliques = list(nx.find_cliques(nx.complement(adjacency)))
    assert max(map(len, cliques)) == 10
    ovoids = {frozenset(clique) for clique in cliques if len(clique) == 10}
    assert len(ovoids) == 36
    points = certificate["overlap_isomorphism"]
    sections = {
        frozenset(int(index) for index, point in points.items() if sum(a*b for a, b in zip(point, normal)) % 3 == 0)
        for normal in projective_points(5)
    }
    assert {section for section in sections if len(section) == 10} == ovoids
    for ovoid in ovoids:
        assert all(len(ovoid & line) == 1 for line in polar_lines)
        assert Counter(i for chart in ovoid for i in supports[chart]) == {i: 6 for i in range(45)}
    assert Counter(len(left & right) for left, right in combinations(ovoids, 2)) == {1: 360, 4: 270}
    outside = set(range(40)).difference(min(map(sorted, ovoids)))
    assert all(len(outside & line) == 3 for line in polar_lines)
    assert all(not ovoid <= outside for ovoid in ovoids)
    assert Counter(i for chart in outside for i in supports[chart]) == {i: 18 for i in range(45)}
    # Candidate found by linear programming, checked here without a solver.
    hemisystem = {0, 4, 9, 10, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 28, 29, 30, 33, 37}
    assert all(len(hemisystem & line) == 2 for line in polar_lines)
    assert Counter(i for chart in hemisystem for i in supports[chart]) == {i: 12 for i in range(45)}
    induced = adjacency.subgraph(hemisystem)
    assert nx.is_connected(induced) and not nx.is_bipartite(induced)

    # A double-six consists of two sixes of skew lines. The opposite six
    # meets each line in precisely five places, with one exception per column.
    tritangents = [set(triple) for triple in certificate["tritangents_in_line_labels"]]
    lines = sorted(set.union(*tritangents))
    classes = {line: line_class(line) for line in lines}
    skew = nx.Graph()
    skew.add_nodes_from(lines)
    skew.add_edges_from((a, b) for a, b in combinations(lines, 2) if intersection(classes[a], classes[b]) == 0)
    sixes = [set(clique) for clique in nx.find_cliques(skew) if len(clique) == 6]
    assert len(sixes) == 72
    double_sixes = {
        frozenset(left | right) for left, right in combinations(sixes, 2)
        if left.isdisjoint(right)
        and all(len(skew[line].keys() & right) == 1 for line in left)
        and all(len(skew[line].keys() & left) == 1 for line in right)
    }
    assert len(double_sixes) == 36

    determinant_blocks = []
    for support in supports:
        graph = nx.Graph()
        for index in set(range(45)) - support:
            graph.add_edges_from(combinations(tritangents[index], 2))
        blocks = list(nx.connected_components(graph))
        assert sorted(map(len, blocks)) == [9, 9, 9]
        determinant_blocks.append(blocks)
    charts_by_double_six = {
        tuple(sorted(pair)): frozenset(i for i, blocks in enumerate(determinant_blocks)
                                       if any(pair.isdisjoint(block) for block in blocks))
        for pair in double_sixes
    }
    assert set(charts_by_double_six.values()) == ovoids
    standard_double_six = tuple(sorted(f"{prefix}{i}" for prefix in ("E", "Q") for i in range(1, 7)))
    standard_blocks = [
        block
        for chart in charts_by_double_six[standard_double_six]
        for block in determinant_blocks[chart]
        if block.isdisjoint(standard_double_six)
    ]
    cuts = {
        frozenset(f"L{min(i, j)}{max(i, j)}" for i in side for j in set(range(1, 7)) - set(side))
        for side in combinations(range(1, 7), 3)
    }
    assert len(standard_blocks) == len(cuts) == 10
    assert {frozenset(block) for block in standard_blocks} == cuts

    ranks = []
    for rank in product(range(4), repeat=3):
        pairs = list(combinations(rank, 2))
        if all(a + b <= 3 for a, b in pairs):
            dimension = 6*sum(rank) - sum(a*a for a in rank) - sum(a*b for a, b in pairs)
            ranks.append((rank, dimension))
    assert max(dimension for _, dimension in ranks) == 13
    assert {rank for rank, dimension in ranks if dimension == 13} == {(2, 1, 1), (1, 2, 1), (1, 1, 2)}

    return {
        "optimal_chart_count": 10,
        "point_line_gram_factorization": {"lines": len(polar_lines), "constant": 15, "incidence_coefficient": 3},
        "optimal_elliptic_sections": len(ovoids),
        "reconstruction_outside_ovoid_convex_hull": {"charts": sorted(outside), "factor": "1/18"},
        "extreme_hemisystem_reconstruction": {"charts": sorted(hemisystem), "factor": "1/12"},
        "squared_coefficient_error_by_budget": {k: str(Fraction(12, k) - Fraction(6, 5)) for k in range(1, 11)},
        "ovoid_charts_by_double_six": [
            {"double_six": pair, "charts": sorted(charts)}
            for pair, charts in sorted(charts_by_double_six.items())
        ],
        "trace_critical_rank_strata": [{"ranks": rank, "dimension": dimension} for rank, dimension in ranks],
    }


if __name__ == "__main__":
    certificate = json.loads((DATA / "toe_20261115_cubic_quiver_steiner.json").read_text(encoding="utf-8"))
    result = verify(certificate)
    path = DATA / "toe_20261115_cubic_quiver_ovoid.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified 36 optimal ten-support reconstructions and the trace critical rank strata")
