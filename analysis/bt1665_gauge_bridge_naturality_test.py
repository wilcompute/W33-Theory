#!/usr/bin/env python3
"""BT1665 — gauge bridge naturality test.

BT1662 supplied one concrete 8->81 homology-coordinate bridge after choosing a
cycle-basis gauge.  BT1665 varies the Levi root gauge over all 80 Levi vertices and
tests whether the same deterministic recipe is natural.

Result: it is not natural.  All selected cycles remain 8-cycles, but their union
support signatures vary across 38 classes.  Therefore the bridge is useful as a
gauge-fixed coordinate object, not as a canonical W33-invariant map.
"""
from __future__ import annotations

import itertools
import json
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


def cycle_edge_set(cycle: list[object]) -> frozenset[tuple[object, object]]:
    edges = []
    for i in range(len(cycle)):
        edges.append(tuple(sorted((cycle[i], cycle[(i + 1) % len(cycle)]), key=repr)))
    return frozenset(edges)


def selected_signature(levi: nx.Graph, root: object) -> tuple[tuple[int, ...], int, int, int]:
    basis = nx.cycle_basis(levi, root=root)
    selected = sorted(basis, key=lambda c: (len(c), repr(c)))[:8]
    edge_sets = [cycle_edge_set(c) for c in selected]
    union_edges = set().union(*edge_sets)
    union_vertices = set().union(*[set(c) for c in selected])
    pair_overlap = sum(len(edge_sets[i] & edge_sets[j]) for i in range(8) for j in range(i + 1, 8))
    return (tuple(sorted(len(c) for c in selected)), len(union_edges), len(union_vertices), pair_overlap)


def summarize_subset(levi: nx.Graph, roots: list[object]) -> dict[str, object]:
    signatures = [selected_signature(levi, r) for r in roots]
    return {
        "roots": len(roots),
        "distinct_signatures": len(set(signatures)),
        "union_edges_min": min(s[1] for s in signatures),
        "union_edges_max": max(s[1] for s in signatures),
        "union_vertices_min": min(s[2] for s in signatures),
        "union_vertices_max": max(s[2] for s in signatures),
        "pair_edge_overlap_min": min(s[3] for s in signatures),
        "pair_edge_overlap_max": max(s[3] for s in signatures),
    }


def main() -> None:
    levi = w33_levi_graph()
    roots = sorted(levi.nodes(), key=repr)
    signatures = [selected_signature(levi, r) for r in roots]
    counts = Counter(signatures)
    all_selected_are_8_cycles = all(sig[0] == (8, 8, 8, 8, 8, 8, 8, 8) for sig in signatures)
    point_roots = [r for r in roots if r[0] == "p"]
    line_roots = [r for r in roots if r[0] == "l"]

    result = {
        "theorem": "BT1665 Gauge Bridge Naturality Test",
        "recipe_tested": "For each Levi root, compute deterministic cycle_basis, select the eight shortest cycles, and record support signatures.",
        "global_summary": {
            "roots_tested": len(roots),
            "all_selected_cycles_are_8_cycles": all_selected_are_8_cycles,
            "distinct_support_signatures": len(counts),
            "union_edges_min": min(s[1] for s in signatures),
            "union_edges_max": max(s[1] for s in signatures),
            "union_vertices_min": min(s[2] for s in signatures),
            "union_vertices_max": max(s[2] for s in signatures),
            "pair_edge_overlap_min": min(s[3] for s in signatures),
            "pair_edge_overlap_max": max(s[3] for s in signatures),
        },
        "by_root_type": {
            "point_roots": summarize_subset(levi, point_roots),
            "line_roots": summarize_subset(levi, line_roots),
        },
        "most_common_signatures": [
            {"lengths": list(sig[0]), "union_edges": sig[1], "union_vertices": sig[2], "pair_edge_overlap": sig[3], "count": count}
            for sig, count in counts.most_common(10)
        ],
        "conclusion": "The BT1662 bridge is gauge-fixed rather than natural: root/basis choices change support signatures. The invariant content is rank 8 into rank 81, not the chosen eight Levi cycles.",
        "boundary": "This is a root-gauge naturality test, not a full automorphism-group orbit computation. It is enough to falsify canonicity of the deterministic cycle-basis recipe.",
    }
    assert len(roots) == 80
    assert result["global_summary"]["distinct_support_signatures"] == 38
    assert all_selected_are_8_cycles
    out = Path("data/PART_BT1665_GAUGE_BRIDGE_NATURALITY_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
