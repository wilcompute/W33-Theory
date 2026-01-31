#!/usr/bin/env python3
"""Find K6 cliques in G_lines using bounded Bron-Kerbosch (early cutoff at size 6).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Set

import networkx as nx

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

from tools.find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                                  construct_w33_points)


def bron_kerbosch_bounded(G, R, P, X, k, output):
    # bounded BK: stop expanding if |R| + |P| < k or |R| > k
    if len(R) == k:
        output.append(set(R))
        return
    if not P and not X:
        # maximal clique smaller than k; ignore
        return
    # pivot selection
    u = max(P | X, key=lambda v: len(G[v])) if (P | X) else None
    for v in list(P - (set(G[u]) if u is not None else set())):
        bron_kerbosch_bounded(G, R | {v}, P & set(G[v]), X & set(G[v]), k, output)
        P.remove(v)
        X.add(v)


def main():
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    n = len(lines)
    G = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if set(lines[i]).isdisjoint(set(lines[j])):
                G[i].add(j)
                G[j].add(i)

    # find all K6 cliques
    cliques = []
    bron_kerbosch_bounded(G, set(), set(range(n)), set(), 6, cliques)
    print("Found k6 cliques (bounded):", len(cliques))

    # pair disjoint cliques and check for perfect matching
    import networkx as nx

    double_sixes = set()
    for i in range(len(cliques)):
        a = cliques[i]
        for b in cliques[i + 1 :]:
            if a & b:
                continue
            # build bipartite edges
            B = nx.Graph()
            A_nodes = [("A", x) for x in a]
            B_nodes = [("B", y) for y in b]
            B.add_nodes_from(A_nodes)
            B.add_nodes_from(B_nodes)
            for x in a:
                for y in b:
                    if y in G[x]:
                        B.add_edge(("A", x), ("B", y))
            matching = nx.algorithms.bipartite.matching.hopcroft_karp_matching(
                B, top_nodes=A_nodes
            )
            pairs = [(u, v) for u, v in matching.items() if u[0] == "A"]
            if len(pairs) == 6:
                key = tuple(sorted([tuple(sorted(a)), tuple(sorted(b))]))
                double_sixes.add(key)

    print("Found double-sixes (unordered):", len(double_sixes))
    out = {"k6_count": len(cliques), "double_six_count": len(double_sixes)}
    (ART / "w33_k6_double_sixes_fast.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
