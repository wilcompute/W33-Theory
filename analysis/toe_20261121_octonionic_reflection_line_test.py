#!/usr/bin/env python3
"""All 729 ambient orthogonal reflections versus true octonionic H(3) incidence.

Finite exhaustive certificate. The reflection pairing need not preserve
exceptional G2 hexagon lines. Run with Python, NumPy and NetworkX.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
import networkx as nx
import toe_20261120_octonion_mereology_radon as H
import toe_20261121_orthogonal_projection_reflection as Q

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261121_octonionic_reflection_lines.json"


def run(write=True):
    pg, quad = Q.point_sets(3)
    index = {v: i for i, v in enumerate(quad)}
    pairs = {(i, j) for i, j in combinations(range(364), 2)
             if H.octo_zero(quad[i], quad[j])}
    assert len(pairs) == 2184
    graph = nx.Graph()
    graph.add_nodes_from(range(364))
    graph.add_edges_from(pairs)
    lines = [frozenset(clique) for clique in nx.find_cliques(graph)]
    line_set = set(lines)
    assert len(lines) == len(line_set) == 364
    assert all(len(line) == 4 for line in lines)
    by_class = Counter()
    examples = {}
    for c in pg:
        value = Q.quadratic(c, 3)
        if value == 0:
            continue
        perm = [index[Q.reflection(x, c, 3)] for x in quad]
        surviving_pairs = sum(tuple(sorted((perm[i], perm[j]))) in pairs
                              for i, j in pairs)
        surviving_lines = sum(frozenset(perm[v] for v in line) in line_set
                              for line in lines)
        fixed_lines = sum(all(Q.polar(quad[v], c, 3) == 0 for v in line)
                          for line in lines)
        assert surviving_pairs == 6 * surviving_lines
        # The only H(3) lines surviving this ambient reflection are
        # the pointwise-fixed H(3) lines contained in the polar hyperplane.
        assert surviving_lines == fixed_lines
        by_class[(value, surviving_pairs, surviving_lines, fixed_lines)] += 1
        examples.setdefault(str(value), c)
    expected = {(1, 168, 28, 28): 351, (2, 312, 52, 52): 378}
    assert dict(by_class) == expected
    result = {
        "schema": "toe.20261121.G2_reflection_line_obstruction.v1",
        "status": "PASS",
        "ambient_projective_centers_examined": 1093,
        "anisotropic_centers_checked": 729,
        "hexagon_points": 364, "hexagon_lines": 364,
        "hexagon_edges": 2184,
        "classes": [
            {"quadratic_norm": 1, "centers": 351, "surviving_edges": 168,
             "surviving_lines": 28, "fixed_pointwise_lines": 28},
            {"quadratic_norm": 2, "centers": 378, "surviving_edges": 312,
             "surviving_lines": 52, "fixed_pointwise_lines": 52}
        ],
        "example_centers": {k: list(v) for k, v in examples.items()},
        "interpretation": "Ambient reflection does not preserve H(3) octonionic incidence; only H-lines contained in its polar fixed hyperplane survive.",
        "boundary": "Exact for the natural H(3) octonionic embedding, not a claim for arbitrary G2(q) embeddings or quantum dynamics."
    }
    if write:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "classes": result["classes"]}))
    return result


if __name__ == "__main__":
    run()
