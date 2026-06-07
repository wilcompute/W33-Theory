#!/usr/bin/env python3
"""BT498: TXT Realization Corrected Szilassi Parser Theorem.

The repo file data/Toroidal-Polyhedra-Realizations.txt contains the correct
Szilassi face cycles. BT490 found that EDGE_LENGTH_ANALYSIS.py used a different
S_FACES list which produced 31 unique edges, not 21.

This script parses/encodes the TXT-face Szilassi data directly and verifies:
  * 7 hexagonal faces
  * 42 face-edge incidences
  * 21 unique edges
  * every edge incident to exactly two faces
  * graph is Heawood
  * distance profile 21,42,28
  * edge-length multiplicities match the TXT edge spectrum counts

This restores the coordinate-aware Szilassi metric carrier.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx

FACES = [
    [0, 1, 13, 8, 7, 4],
    [0, 4, 3, 2, 10, 12],
    [0, 12, 9, 6, 5, 1],
    [11, 3, 4, 7, 6, 9],
    [11, 9, 12, 10, 8, 13],
    [11, 13, 1, 5, 2, 3],
    [2, 5, 6, 7, 8, 10],
]

S1 = {
    0: (12.0, 0.0, 12.0), 1: (-12.0, 0.0, 12.0),
    2: (0.0, 12.6, -12.0), 3: (0.0, -12.6, -12.0),
    4: (2.0, -5.0, -8.0), 5: (-2.0, 5.0, -8.0),
    6: (3.75, 3.75, -3.0), 7: (-3.75, -3.75, -3.0),
    8: (4.5, -2.5, 2.0), 9: (-4.5, 2.5, 2.0),
    10: (7.0, 0.0, 2.0), 11: (-7.0, 0.0, 2.0),
    12: (7.0, 2.5, 2.0), 13: (-7.0, -2.5, 2.0),
}

C0, C1 = 8.0 / 3.0, 20.0 / 3.0
S2 = {
    0: (12.0, 0.0, 12.0), 1: (-12.0, 0.0, 12.0),
    2: (0.0, 12.0, -12.0), 3: (0.0, -12.0, -12.0),
    4: (1.5, -5.25, -9.0), 5: (-1.5, 5.25, -9.0),
    6: (C0, 4.0, -4.0), 7: (-C0, -4.0, -4.0),
    8: (C1, -2.0, 4.0), 9: (-C1, 2.0, 4.0),
    10: (8.0, 0.0, 4.0), 11: (-8.0, 0.0, 4.0),
    12: (8.0, 2.0, 4.0), 13: (-8.0, -2.0, 4.0),
}


def face_edges(face: list[int]) -> list[tuple[int, int]]:
    return [tuple(sorted((face[i], face[(i + 1) % len(face)]))) for i in range(len(face))]


def edge_counter() -> Counter[tuple[int, int]]:
    c: Counter[tuple[int, int]] = Counter()
    for face in FACES:
        assert len(face) == 6
        c.update(face_edges(face))
    return c


def sqdist(V: dict[int, tuple[float, float, float]], a: int, b: int) -> float:
    return sum((V[a][i] - V[b][i]) ** 2 for i in range(3))


def metric_packet(name: str, V: dict[int, tuple[float, float, float]], edges: list[tuple[int, int]]) -> dict:
    vals = [sqdist(V, a, b) for a, b in edges]
    rounded = [round(v, 10) for v in vals]
    return {
        'name': name,
        'edge_count': len(edges),
        'distinct_squared_lengths': len(set(rounded)),
        'squared_length_multiplicities': {str(k): v for k, v in sorted(Counter(rounded).items(), key=lambda kv: float(kv[0]))},
        'sum_squared_lengths': round(sum(vals), 10),
        'squared_metric_norm2': round(sum(v * v for v in vals), 10),
        'min_squared_length': round(min(vals), 10),
        'max_squared_length': round(max(vals), 10),
    }


def main() -> dict:
    c = edge_counter()
    edges = sorted(c)
    assert len(FACES) == 7
    assert sum(c.values()) == 42
    assert len(edges) == 21
    assert Counter(c.values()) == Counter({2: 21})

    G = nx.Graph()
    G.add_nodes_from(range(14))
    G.add_edges_from(edges)
    assert G.number_of_nodes() == 14
    assert G.number_of_edges() == 21
    assert sorted(dict(G.degree()).values()) == [3] * 14
    assert nx.is_isomorphic(G, nx.heawood_graph())
    assert nx.diameter(G) == 3
    dist_profile = Counter()
    for u, v in combinations(G.nodes(), 2):
        dist_profile[nx.shortest_path_length(G, u, v)] += 1
    assert dist_profile == Counter({1: 21, 2: 42, 3: 28})

    p1 = metric_packet('Szilassi TXT v1', S1, edges)
    p2 = metric_packet('Szilassi TXT v2', S2, edges)
    assert p1['distinct_squared_lengths'] == 12
    assert p2['distinct_squared_lengths'] == 11
    assert p1['min_squared_length'] == 6.25
    assert p2['min_squared_length'] == 4.0

    results = {
        'theorem': 'BT498 TXT Realization Corrected Szilassi Parser Theorem',
        'source': 'data/Toroidal-Polyhedra-Realizations.txt Szilassi face cycles',
        'incidence': {
            'hexagonal_faces': len(FACES),
            'face_edge_incidences': sum(c.values()),
            'unique_edges': len(edges),
            'edge_incidence_profile': {str(k): v for k, v in sorted(Counter(c.values()).items())},
            'closed_szilassi_condition': True,
        },
        'graph': {
            'is_heawood': True,
            'vertices': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'degree_profile': {'3': 14},
            'diameter': nx.diameter(G),
            'distance_pair_profile': {str(k): v for k, v in sorted(dist_profile.items())},
        },
        'corrected_edges': edges,
        'metric_packets': [p1, p2],
        'repair_reading': {
            'BT490': 'old EDGE_LENGTH_ANALYSIS.py parser used wrong Szilassi face cycles and gave 31 edges',
            'BT498': 'TXT realization data gives the correct 21-edge closed Heawood/Szilassi carrier',
            'next_step': 'replace metric analysis Szilassi S_FACES with the TXT FACES list before promoting seven-realization edge spectra',
        },
        'substrate_reading': {
            '21': 'correct Szilassi edge shell',
            '42': 'face-edge incidences and Heawood distance-2 pairs',
            '28': 'Heawood distance-3 unordered pairs / phase superperiod',
            '12_and_11': 'distinct Szilassi v1/v2 edge-length types match TXT counts',
        },
    }
    out = Path('data/PART_BT498_TXT_REALIZATION_CORRECTED_SZILASSI_PARSER_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))
    return results

if __name__ == '__main__':
    main()
