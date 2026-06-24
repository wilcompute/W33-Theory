#!/usr/bin/env python3
"""BT1668 — gauge-twirled bridge support test.

BT1665 showed that a selected 8-cycle bridge depends on the root/basis gauge.
BT1668 twirls that selector over all 80 root gauges and measures the resulting
support distribution on W33 Levi edges and vertices.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx

MOD = 3


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...] | None:
    vv = tuple(x % MOD for x in v)
    if all(x == 0 for x in vv):
        return None
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % MOD for y in vv)
    raise AssertionError("unreachable")


def symplectic_form(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % MOD


def w33_collinearity_graph() -> nx.Graph:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for v in itertools.product(range(MOD), repeat=4):
        c = canonical_projective(v)
        if c is not None and c not in seen:
            seen.add(c)
            points.append(c)  # type: ignore[arg-type]
    points.sort()
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for i, j in itertools.combinations(range(len(points)), 2):
        if symplectic_form(points[i], points[j]) == 0:
            graph.add_edge(i, j)
    return graph


def w33_levi_graph() -> nx.Graph:
    w33 = w33_collinearity_graph()
    lines = [tuple(sorted(c)) for c in nx.find_cliques(w33) if len(c) == 4]
    lines.sort()
    levi = nx.Graph()
    for p in range(w33.number_of_nodes()):
        levi.add_node(("p", p))
    for li, line in enumerate(lines):
        ln = ("l", li)
        levi.add_node(ln)
        for p in line:
            levi.add_edge(("p", p), ln)
    return levi


def cycle_edge_set(cycle: list[object]) -> set[tuple[object, object]]:
    return {tuple(sorted((cycle[i], cycle[(i + 1) % len(cycle)]), key=repr)) for i in range(len(cycle))}


def selected_cycles(levi: nx.Graph, root: object) -> list[list[object]]:
    basis = nx.cycle_basis(levi, root=root)
    return sorted(basis, key=lambda c: (len(c), repr(c)))[:8]


def entropy(counts: Counter) -> tuple[float, float]:
    total = sum(counts.values())
    probs = [v / total for v in counts.values()]
    h = -sum(p * math.log(p, 2) for p in probs)
    return h, 2**h


def main() -> None:
    levi = w33_levi_graph()
    roots = sorted(levi.nodes(), key=repr)
    edge_counts: Counter[str] = Counter()
    vertex_counts: Counter[str] = Counter()
    cycle_counts: Counter[str] = Counter()

    for root in roots:
        for cycle in selected_cycles(levi, root):
            cycle_counts[str(sorted(cycle, key=repr))] += 1
            for edge in cycle_edge_set(cycle):
                edge_counts[str(edge)] += 1
            for vertex in cycle:
                vertex_counts[str(vertex)] += 1

    edge_entropy, effective_edges = entropy(edge_counts)
    vertex_entropy, effective_vertices = entropy(vertex_counts)

    result = {
        "theorem": "BT1668 Gauge-Twirl Bridge Support Test",
        "twirl": "average the BT1662 eight-cycle selector over all 80 Levi root gauges",
        "coverage": {
            "roots": len(roots),
            "selected_cycles_per_root": 8,
            "cycle_length": 8,
            "edge_incidence_events": sum(edge_counts.values()),
            "vertex_incidence_events": sum(vertex_counts.values()),
            "unique_cycles_seen": len(cycle_counts),
            "max_cycle_reuse_count": max(cycle_counts.values()),
            "levi_edges_covered": len(edge_counts),
            "levi_vertices_covered": len(vertex_counts),
            "total_levi_edges": levi.number_of_edges(),
            "total_levi_vertices": levi.number_of_nodes(),
        },
        "edge_distribution": {
            "min_count": min(edge_counts.values()),
            "max_count": max(edge_counts.values()),
            "entropy_bits": round(edge_entropy, 12),
            "effective_support_size": round(effective_edges, 12),
        },
        "vertex_distribution": {
            "min_count": min(vertex_counts.values()),
            "max_count": max(vertex_counts.values()),
            "entropy_bits": round(vertex_entropy, 12),
            "effective_support_size": round(effective_vertices, 12),
        },
        "top_edge_counts": edge_counts.most_common(12),
        "top_vertex_counts": vertex_counts.most_common(12),
        "conclusion": "Root-gauge twirling destroys the special eight-cycle support and spreads over every Levi edge and vertex. The gauge-averaged bridge is global, not a smaller canonical 8-cycle embedding.",
        "boundary": "This is a root-gauge twirl, not yet a full Sp(4,3) automorphism twirl. It is enough to show that the deterministic bridge does not collapse to a sparse natural support.",
    }
    assert result["coverage"]["levi_edges_covered"] == 160
    assert result["coverage"]["levi_vertices_covered"] == 80
    assert result["coverage"]["edge_incidence_events"] == 5120
    out = Path("data/PART_BT1668_GAUGE_TWIRL_BRIDGE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
