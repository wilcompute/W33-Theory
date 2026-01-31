#!/usr/bin/env python3
"""Random sampling of 27-subsets of W33 lines to look for Schlaefli-like structure.
"""
from __future__ import annotations

import random
import time
from collections import Counter
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

from tools.find_k6_double_sixes_w33_fast import bron_kerbosch_bounded
from tools.find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                                  construct_w33_points)


def eval_subset(nodes, G):
    # nodes: list of indices subset
    # build induced adjacency dict
    S = set(nodes)
    Gs = {v: set(u for u in G[v] if u in S) for v in S}
    k6 = []
    bron_kerbosch_bounded(Gs, set(), set(nodes), set(), 6, k6)
    k6_count = len(k6)
    # count double sixes: pair disjoint k6 and check perfect matching
    # small numbers so brute force
    ds = set()
    for i in range(len(k6)):
        a = set(k6[i])
        for j in range(i + 1, len(k6)):
            b = set(k6[j])
            if a & b:
                continue
            # bipartite matching
            B = nx.Graph()
            A_nodes = [("A", x) for x in a]
            B_nodes = [("B", y) for y in b]
            B.add_nodes_from(A_nodes)
            B.add_nodes_from(B_nodes)
            for x in a:
                for y in b:
                    if y in Gs[x]:
                        B.add_edge(("A", x), ("B", y))
            matching = nx.algorithms.bipartite.matching.hopcroft_karp_matching(
                B, top_nodes=A_nodes
            )
            pairs = [(u, v) for u, v in matching.items() if u[0] == "A"]
            if len(pairs) == 6:
                key = tuple(sorted([tuple(sorted(a)), tuple(sorted(b))]))
                ds.add(key)
    return k6_count, len(ds)


def random_search(iterations=1000, timeout=60):
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    n = len(lines)
    G = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if set(lines[i]).isdisjoint(set(lines[j])):
                G[i].add(j)
                G[j].add(i)

    start = time.time()
    best = None
    best_score = (-1, -1)
    for it in range(iterations):
        if time.time() - start > timeout:
            break
        subset = random.sample(list(range(n)), 27)
        k6c, dsc = eval_subset(subset, G)
        if (k6c, dsc) > best_score:
            best_score = (k6c, dsc)
            best = (subset, k6c, dsc)
            print("New best:", best_score, "it", it)
        if k6c == 72 and dsc == 36:
            print("Found candidate subset")
            (ART / "w33_schlafli_candidate_random.json").write_text(
                json.dumps(
                    {"subset": sorted(subset), "k6": k6c, "double_sixes": dsc}, indent=2
                ),
                encoding="utf-8",
            )
            return subset
    print("Done sampling. Best:", best_score)
    return None


if __name__ == "__main__":
    import json

    random_search(iterations=2000, timeout=60)
