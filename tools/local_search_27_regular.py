#!/usr/bin/env python3
"""Randomized local search to find 27-vertex induced subgraph with degree 16.
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

from tools.find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                                  construct_w33_points)


def score_subset(subset, neigh):
    # returns number of vertices in subset with intra-degree == 16
    s = set(subset)
    cnt = 0
    degs = {}
    for v in subset:
        d = len(neigh[v] & s)
        degs[v] = d
        if d == 16:
            cnt += 1
    return cnt, degs


def local_search(iterations=20000, timeout=30):
    start = time.time()
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    n = len(lines)
    neigh = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if set(lines[i]).isdisjoint(set(lines[j])):
                neigh[i].add(j)
                neigh[j].add(i)

    best_subset = None
    best_score = -1
    nodes = list(range(n))

    # initialize with random start sets
    for restart in range(20):
        subset = set(random.sample(nodes, 27))
        sc, degs = score_subset(subset, neigh)
        if sc > best_score:
            best_score = sc
            best_subset = set(subset)
        it = 0
        while time.time() - start < timeout and it < iterations:
            it += 1
            # try random swap: remove u from subset, add v from outside
            u = random.choice(list(subset))
            v = random.choice([x for x in nodes if x not in subset])
            subset.remove(u)
            subset.add(v)
            sc2, degs2 = score_subset(subset, neigh)
            # accept if better or with small prob
            if sc2 >= sc or random.random() < 0.001:
                sc = sc2
                degs = degs2
                if sc2 > best_score:
                    best_score = sc2
                    best_subset = set(subset)
                    print("New best", best_score, "at time", time.time() - start)
            else:
                subset.remove(v)
                subset.add(u)
            if best_score == 27:
                print("Found perfect subset")
                (ART / "w33_schlafli_candidate_subset_local.json").write_text(
                    json.dumps({"subset": sorted(list(best_subset))}, indent=2),
                    encoding="utf-8",
                )
                return best_subset
    print("Best score found:", best_score)
    return best_subset


if __name__ == "__main__":
    import json

    res = local_search(iterations=5000, timeout=30)
    print(res)
