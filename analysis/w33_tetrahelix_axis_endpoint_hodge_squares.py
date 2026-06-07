#!/usr/bin/env python3
"""BT504: Tetrahelix Axis Endpoint Hodge-Square Theorem.

BT503 showed that the 12 tetrahelix axes through one tetrahedron are the
24 vertex orders modulo reversal, split 6+6 by parity.

This theorem studies the endpoint graph of those axes.

Each axis connects two (7,3) face-coordinate points.  There are 12 such
face points total: 4 faces * 3 points per face.  Since each point is used
by exactly two axes, the endpoint graph is 2-regular on 12 vertices.

Executable result:
    endpoint graph = 3 disjoint C4 cycles.

Those 3 squares correspond to the 3 pairs of opposite edges in K4, i.e.
the three Hodge-star / bivector channels of a tetrahedron.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

VERTICES = tuple(range(4))
OPPOSITE_EDGE_PAIRS = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]


def canonical_axis(path: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    rev = tuple(reversed(path))
    return min(path, rev)


def face_point_key(a: int, b: int, c: int) -> tuple[int, int, int]:
    return min((a, b, c), (c, b, a))


def parity(path: tuple[int, ...]) -> str:
    inv = 0
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            if path[i] > path[j]:
                inv += 1
    return "even" if inv % 2 == 0 else "odd"


def missing_vertex(face_point: tuple[int, int, int]) -> int:
    return next(v for v in VERTICES if v not in face_point)


def hodge_channel_for_axis(axis: tuple[int, int, int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    # The endpoints are on faces abc and bcd, whose missing vertices are d and a.
    # The axis is naturally assigned to the opposite-edge pair {a,d} and {b,c}.
    a, b, c, d = axis
    e1 = tuple(sorted((a, d)))
    e2 = tuple(sorted((b, c)))
    return tuple(sorted((e1, e2)))


def main() -> dict:
    axes = sorted({canonical_axis(p) for p in itertools.permutations(VERTICES)})
    assert len(axes) == 12

    G = nx.Graph()
    edge_axis = {}
    channel_counter: Counter[str] = Counter()
    axes_by_channel: defaultdict[str, list[str]] = defaultdict(list)
    for axis in axes:
        a, b, c, d = axis
        u = face_point_key(a, b, c)
        v = face_point_key(b, c, d)
        ch = hodge_channel_for_axis(axis)
        ch_key = str(ch)
        G.add_edge(u, v, axis="".join(map(str, axis)), chirality=parity(axis), channel=ch_key)
        edge_axis[str((u, v))] = "".join(map(str, axis))
        channel_counter[ch_key] += 1
        axes_by_channel[ch_key].append("".join(map(str, axis)))

    assert G.number_of_nodes() == 12
    assert G.number_of_edges() == 12
    assert sorted(dict(G.degree()).values()) == [2] * 12
    comps = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    assert sorted(c.number_of_nodes() for c in comps) == [4, 4, 4]
    assert all(nx.is_isomorphic(c, nx.cycle_graph(4)) for c in comps)
    assert len(comps) == 3

    # Each component has two even and two odd axes.
    component_packets = []
    for i, comp in enumerate(comps):
        chirality = Counter(comp.edges[e]["chirality"] for e in comp.edges())
        channels = Counter(comp.edges[e]["channel"] for e in comp.edges())
        assert chirality == Counter({"even": 2, "odd": 2})
        assert len(channels) == 1
        component_packets.append({
            "component": i,
            "nodes": [str(n) for n in sorted(comp.nodes())],
            "edges": [str(e) for e in sorted(comp.edges())],
            "chirality_profile": dict(chirality),
            "hodge_channel": next(iter(channels)),
        })

    # The channels are exactly the 3 opposite-edge pairs of the tetrahedron.
    expected_channels = {str(tuple(sorted((tuple(sorted(a)), tuple(sorted(b)))))) for a, b in OPPOSITE_EDGE_PAIRS}
    assert set(channel_counter) == expected_channels
    assert Counter(channel_counter.values()) == Counter({4: 3})

    # Face coverage: every tetrahedron face contributes three endpoint points.
    face_profile = Counter(tuple(sorted(node)) for node in G.nodes())
    assert face_profile == Counter({face: 3 for face in itertools.combinations(VERTICES, 3)})

    results = {
        "theorem": "BT504 Tetrahelix Axis Endpoint Hodge-Square Theorem",
        "endpoint_graph": {
            "vertices": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "degree": 2,
            "decomposition": "3 disjoint C4 cycles",
            "component_sizes": [c.number_of_nodes() for c in comps],
        },
        "component_packets": component_packets,
        "hodge_channels": {
            "opposite_edge_pairs": sorted(expected_channels),
            "axis_count_per_channel": {k: v for k, v in sorted(channel_counter.items())},
            "reading": "three C4 endpoint cycles = three opposite-edge/Hodge-star channels of K4",
        },
        "face_coverage": {
            "face_point_profile": {str(k): v for k, v in sorted(face_profile.items())},
            "reading": "four faces each carry three (7,3) points",
        },
        "chirality_balance": {
            "per_square": "2 even + 2 odd axes",
            "global": "6 even + 6 odd axes",
        },
        "substrate_reading": {
            "3": "three opposite-edge bivector/Hodge channels",
            "4": "each channel is a C4 square",
            "12": "three C4 cycles = local BC-axis codec",
            "24": "oriented axis-endpoint incidences = tetrahedron flags",
        },
    }

    out = Path("data/PART_BT504_TETRAHELIX_AXIS_ENDPOINT_HODGE_SQUARES_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
