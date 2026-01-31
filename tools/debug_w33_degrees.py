#!/usr/bin/env python3
import itertools
from collections import Counter
from pathlib import Path

from find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                            construct_w33_points)

if __name__ == "__main__":
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    n = len(lines)
    adj = [0] * n
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if set(lines[i]).isdisjoint(set(lines[j])):
                adj[i] += 1
    print("W33 lines:", n)
    c = Counter(adj)
    print("Degree histogram:", c)
    geq16 = sum(v for k, v in c.items() if k >= 16)
    nodes_geq16 = [i for i, d in enumerate(adj) if d >= 16]
    print("Nodes with degree>=16:", len(nodes_geq16))
    print("Degrees>=16 samples (first 10):", nodes_geq16[:10])
    # per-vertex degrees
    print("All degrees:", adj)

    # quick check: any 27-subset where every member has degree>=16 must have all 27 in nodes_geq16
    print("Can choose 27 from eligible nodes?", len(nodes_geq16) >= 27)

    # show sorted degrees
    print("Sorted degrees:", sorted(adj))
