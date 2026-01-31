#!/usr/bin/env python3
"""Find K6 cliques in the W33 line-disjointness graph and pair them into double-sixes.

Outputs:
- tools/artifacts/w33_k6_double_sixes.json
"""
from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

from tools.find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                                  construct_w33_points)


def main():
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    G = nx.Graph()
    G.add_nodes_from(range(len(lines)))
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if set(lines[i]).isdisjoint(set(lines[j])):
                G.add_edge(i, j)

    # enumerate all cliques up to size 6
    cliques = [c for c in nx.enumerate_all_cliques(G) if len(c) == 6]
    print("Found k6 cliques:", len(cliques))

    # index cliques by frozenset for quick disjoint check
    cliques_sets = [frozenset(c) for c in cliques]

    double_sixes = set()
    for i, a in enumerate(cliques_sets):
        for b in cliques_sets[i + 1 :]:
            if a & b:
                continue
            # bipartite edges between a and b
            # build bipartite graph
            B = nx.Graph()
            B.add_nodes_from([(0, x) for x in a])
            B.add_nodes_from([(1, y) for y in b])
            for x in a:
                for y in b:
                    if (x, y) in G.edges or (y, x) in G.edges:
                        B.add_edge((0, x), (1, y))
            # check for perfect matching of size 6
            matching = nx.algorithms.bipartite.matching.hopcroft_karp_matching(
                B, top_nodes=[(0, x) for x in a]
            )
            # matching verifies pairs from top_nodes only
            pairs = [
                (u, v)
                for u, v in matching.items()
                if isinstance(u, tuple) and u[0] == 0
            ]
            if len(pairs) == 6:
                # canonicalize unordered pair
                key = tuple(sorted([tuple(sorted(a)), tuple(sorted(b))]))
                double_sixes.add(key)

    print("Found double-sixes (unordered):", len(double_sixes))

    out = {
        "k6_count": len(cliques),
        "double_six_count": len(double_sixes),
        "examples": list(list(k) for k in list(double_sixes)[:5]),
    }
    (ART / "w33_k6_double_sixes.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
