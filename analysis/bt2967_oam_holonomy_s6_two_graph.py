#!/usr/bin/env python3
"""Pass 2967: exact OAM spread-router gauge curvature and S6 two-graph closure.

The 10x4 spread fabric associates an S4 transport permutation to each ordered
pair of spread lines. Taking permutation sign gives a Z2 edge connection.
Its triangle coboundary is gauge invariant. This verifier enumerates all 36
spreads of W(3,3), proves that every curvature hypergraph is the same
10-point regular two-graph, identifies a switching representative as the
Petersen graph, and proves the full two-graph automorphism group is
PΣL(2,9) ≅ S6 in its degree-10 action on 3+3 partitions of a six-set.
"""
from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2967_OAM_HOLONOMY_S6_TWO_GRAPH_results.json"


def norm(v):
    v = tuple(int(x) % 3 for x in v)
    i = next(i for i, x in enumerate(v) if x)
    return tuple(2*x % 3 for x in v) if v[i] == 2 else v


POINTS = [v for v in itertools.product(range(3), repeat=4) if any(v) and norm(v) == v]
POINT_INDEX = {p: i for i, p in enumerate(POINTS)}
J = np.array([[0,1,0,0], [2,0,0,0], [0,0,0,1], [0,0,2,0]], dtype=int)


def symp(p, q):
    return int(np.array(p) @ J @ np.array(q) % 3)


LINES_SET = set()
for i, j in itertools.combinations(range(40), 2):
    if symp(POINTS[i], POINTS[j]):
        continue
    p = np.array(POINTS[i])
    q = np.array(POINTS[j])
    line = {
        POINT_INDEX[norm(a*p + b*q)]
        for a, b in itertools.product(range(3), repeat=2)
        if a or b
    }
    LINES_SET.add(tuple(sorted(line)))
LINES = sorted(LINES_SET)
BY_POINT = {p: [] for p in range(40)}
for line_id, line in enumerate(LINES):
    for p in line:
        BY_POINT[p].append(line_id)


def enumerate_spreads():
    spreads = []
    def walk(covered, chosen):
        if len(covered) == 40:
            spreads.append(tuple(sorted(chosen)))
            return
        remaining = set(range(40)) - covered
        p = min(
            remaining,
            key=lambda x: sum(
                1 for line_id in BY_POINT[x]
                if not (set(LINES[line_id]) & covered)
            ),
        )
        for line_id in BY_POINT[p]:
            line = set(LINES[line_id])
            if line & covered:
                continue
            walk(covered | line, chosen + [line_id])
    walk(set(), [])
    return sorted(set(spreads))


def compose(p, q):
    return tuple(p[q[a]] for a in range(4))


def permutation_parity(p):
    return sum(
        p[a] > p[b]
        for a in range(len(p))
        for b in range(a+1, len(p))
    ) % 2


def cycle_type(p):
    seen = set()
    lengths = []
    for a in range(4):
        if a in seen:
            continue
        b = a
        n = 0
        while b not in seen:
            seen.add(b)
            n += 1
            b = p[b]
        lengths.append(n)
    return tuple(sorted(lengths, reverse=True))


def spread_transport(spread_ids):
    spread = [LINES[i] for i in spread_ids]
    slot = {p: s for line in spread for s, p in enumerate(line)}
    transport = {}
    for i, j in itertools.permutations(range(10), 2):
        perm = []
        for p in spread[i]:
            targets = [q for q in spread[j] if symp(POINTS[p], POINTS[q]) == 0]
            assert len(targets) == 1
            perm.append(slot[targets[0]])
        perm = tuple(perm)
        assert sorted(perm) == list(range(4))
        transport[i, j] = perm
    return transport


def incidence_graph(blocks):
    graph = nx.Graph()
    for point in range(10):
        graph.add_node(("p", point), kind="point")
    for block_id, block in enumerate(sorted(blocks)):
        graph.add_node(("b", block_id), kind="block")
        for point in block:
            graph.add_edge(("p", point), ("b", block_id))
    return graph


def partition_key(subset):
    subset = frozenset(subset)
    complement = frozenset(set(range(6)) - set(subset))
    return min(tuple(sorted(subset)), tuple(sorted(complement)))


PARTITIONS = sorted({partition_key(subset) for subset in itertools.combinations(range(6), 3)})
PARTITION_INDEX = {part: i for i, part in enumerate(PARTITIONS)}


def induced_s6_actions():
    actions = set()
    for sigma in itertools.permutations(range(6)):
        image = []
        for part in PARTITIONS:
            moved = partition_key({sigma[x] for x in part})
            image.append(PARTITION_INDEX[moved])
        actions.add(tuple(image))
    assert len(actions) == 720
    return sorted(actions)


S6_ACTIONS = induced_s6_actions()
all_triples = set(itertools.combinations(range(10), 3))
unseen = set(all_triples)
S6_TRIPLE_ORBITS = []
while unseen:
    seed = min(unseen)
    orbit = {tuple(sorted(action[i] for i in seed)) for action in S6_ACTIONS}
    S6_TRIPLE_ORBITS.append(orbit)
    unseen -= orbit
S6_TRIPLE_ORBITS.sort(key=lambda orbit: min(orbit))
assert [len(orbit) for orbit in S6_TRIPLE_ORBITS] == [60, 60]
CANONICAL_TWO_GRAPH = S6_TRIPLE_ORBITS[0]
CANONICAL_INCIDENCE = incidence_graph(CANONICAL_TWO_GRAPH)


def block_design_checks(blocks):
    point_counts = collections.Counter()
    pair_counts = collections.Counter()
    for block in blocks:
        for p in block:
            point_counts[p] += 1
        for pair in itertools.combinations(block, 2):
            pair_counts[tuple(sorted(pair))] += 1
    ok = (
        len(blocks) == 60
        and set(point_counts.values()) == {18}
        and set(pair_counts.values()) == {4}
    )
    return ok, point_counts, pair_counts


def analyze_spread(spread_ids):
    transport = spread_transport(spread_ids)
    edge_parity = {
        (i, j): permutation_parity(transport[i, j])
        for i, j in itertools.combinations(range(10), 2)
    }
    odd_triangles = set()
    cycle_histogram = collections.Counter()
    for i, j, k in itertools.combinations(range(10), 3):
        holonomy = compose(transport[k, i], compose(transport[j, k], transport[i, j]))
        cycle_histogram[cycle_type(holonomy)] += 1
        curvature = permutation_parity(holonomy)
        edge_coboundary = (
            edge_parity[i, j] + edge_parity[i, k] + edge_parity[j, k]
        ) % 2
        assert curvature == edge_coboundary
        if curvature:
            odd_triangles.add((i, j, k))

    design_ok, point_counts, pair_counts = block_design_checks(odd_triangles)
    bianchi_ok = all(
        sum(
            tuple(sorted(face)) in odd_triangles
            for face in itertools.combinations(tetrahedron, 3)
        ) % 2 == 0
        for tetrahedron in itertools.combinations(range(10), 4)
    )

    gauge_ok = True
    for switch_bits in itertools.product(range(2), repeat=10):
        switched = {
            (i, j): (edge_parity[i, j] + switch_bits[i] + switch_bits[j]) % 2
            for i, j in itertools.combinations(range(10), 2)
        }
        reconstructed = {
            (i, j, k)
            for i, j, k in itertools.combinations(range(10), 3)
            if (switched[i, j] + switched[i, k] + switched[j, k]) % 2
        }
        if reconstructed != odd_triangles:
            gauge_ok = False
            break

    graph = incidence_graph(odd_triangles)
    isomorphic = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        CANONICAL_INCIDENCE,
        node_match=lambda a, b: a["kind"] == b["kind"],
    ).is_isomorphic()

    representative = nx.Graph()
    representative.add_nodes_from(range(10))
    representative.add_edges_from([edge for edge, parity in edge_parity.items() if parity])
    return {
        "odd_triangle_count": len(odd_triangles),
        "cycle_histogram": {
            "-".join(map(str, key)): value for key, value in sorted(cycle_histogram.items())
        },
        "design_2_10_3_4": design_ok,
        "point_replication": sorted(set(point_counts.values())),
        "pair_replication": sorted(set(pair_counts.values())),
        "bianchi_delta_squared_zero": bianchi_ok,
        "all_vertex_sign_gauges_preserve_curvature": gauge_ok,
        "isomorphic_to_s6_two_graph": isomorphic,
        "edge_representative_edges": representative.number_of_edges(),
        "edge_representative_degree_multiset": sorted(dict(representative.degree()).values()),
        "edge_representative_is_petersen": nx.is_isomorphic(representative, nx.petersen_graph()),
    }


def main():
    assert len(POINTS) == len(LINES) == 40
    spreads = enumerate_spreads()
    assert len(spreads) == 36
    records = [analyze_spread(spread) for spread in spreads]
    assert all(r["odd_triangle_count"] == 60 for r in records)
    assert all(r["design_2_10_3_4"] for r in records)
    assert all(r["bianchi_delta_squared_zero"] for r in records)
    assert all(r["all_vertex_sign_gauges_preserve_curvature"] for r in records)
    assert all(r["isomorphic_to_s6_two_graph"] for r in records)
    assert all(r["cycle_histogram"] == {"2-1-1": 60, "2-2": 60} for r in records)
    assert records[0]["edge_representative_is_petersen"]

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        CANONICAL_INCIDENCE,
        CANONICAL_INCIDENCE,
        node_match=lambda a, b: a["kind"] == b["kind"],
    )
    automorphism_count = sum(1 for _ in matcher.isomorphisms_iter())
    assert automorphism_count == 720
    assert all(
        {tuple(sorted(action[i] for i in block)) for block in CANONICAL_TWO_GRAPH}
        == CANONICAL_TWO_GRAPH
        for action in S6_ACTIONS
    )

    representative_histogram = collections.Counter(
        (
            r["edge_representative_edges"],
            tuple(r["edge_representative_degree_multiset"]),
            r["edge_representative_is_petersen"],
        )
        for r in records
    )
    checks = {
        "w33_40_points_40_lines": len(POINTS) == len(LINES) == 40,
        "all_36_spreads_enumerated": len(spreads) == 36,
        "every_spread_has_60_transposition_and_60_double_transposition_triangles":
            all(r["cycle_histogram"] == {"2-1-1": 60, "2-2": 60} for r in records),
        "odd_holonomies_form_2_10_3_4_design_on_every_spread":
            all(r["design_2_10_3_4"] for r in records),
        "tetrahedral_bianchi_identity_on_every_spread":
            all(r["bianchi_delta_squared_zero"] for r in records),
        "curvature_is_invariant_under_all_1024_vertex_sign_gauges":
            all(r["all_vertex_sign_gauges_preserve_curvature"] for r in records),
        "all_spread_curvatures_are_the_same_s6_two_graph":
            all(r["isomorphic_to_s6_two_graph"] for r in records),
        "canonical_switching_representative_is_petersen":
            records[0]["edge_representative_is_petersen"],
        "two_graph_automorphism_group_order_720": automorphism_count == 720,
        "explicit_s6_degree10_action_preserves_curvature_blocks": len(S6_ACTIONS) == 720,
    }
    assert all(checks.values())
    result = {
        "schema": "w33.pass2967.oam_holonomy_s6_two_graph.v1",
        "status": "COMPLETE_EXACT_FINITE_GAUGE_CLASSIFICATION",
        "checks": checks,
        "check_count": len(checks),
        "spreads": len(spreads),
        "triangle_holonomy": {
            "transpositions": 60,
            "double_transpositions": 60,
            "odd_curvature_blocks": 60,
            "even_curvature_blocks": 60,
        },
        "odd_curvature_design": {
            "parameters": "2-(10,3,4)",
            "point_replication": 18,
            "pair_replication": 4,
            "two_graph_axiom": "Every four-mode tetrahedron contains an even number of odd-curvature faces.",
        },
        "gauge_field": {
            "connection": "sign of each S4 inter-line transport permutation",
            "gauge_group_seen_by_parity": "C2^10 / diagonal C2",
            "curvature": "triangle coboundary of the edge-sign 1-cochain",
            "bianchi": "delta^2=0 on every one of the 210 tetrahedra",
        },
        "classification": {
            "switching_class_contains": "Petersen graph",
            "automorphism_group_order": 720,
            "automorphism_group": "PΣL(2,9) ≅ S6",
            "degree10_model": "S6 acting on the ten unordered 3+3 partitions of a six-set",
            "s6_triple_orbits": [60, 60],
        },
        "raw_slot_gauge_representative_histogram": [
            {
                "spread_count": count,
                "edge_count": key[0],
                "degree_multiset": list(key[1]),
                "is_petersen": key[2],
            }
            for key, count in sorted(representative_histogram.items())
        ],
        "headline": (
            "The 10x4 OAM spread router carries a spread-independent Z2 curvature: "
            "its 60 odd triangle holonomies are the exceptional 10-point S6 two-graph, "
            "with the Petersen graph as a switching representative and an exact "
            "tetrahedral Bianchi identity."
        ),
        "claim_boundary": (
            "Exact for the finite routing permutations. This is a discrete parity "
            "connection, not a measured optical Berry phase or a continuum gauge field."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS", len(checks), "/", len(checks), result["headline"])


if __name__ == "__main__":
    main()
