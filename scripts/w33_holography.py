#!/usr/bin/env python3
"""
Discrete holography / RT-like diagnostics on W(3,3)

Pillar 46 — area-law / minimal-cut behavior on W33
- For random vertex subsets compute the edge-boundary size (# edges crossing the cut)
- Compare boundary size vs subset volume to demonstrate an "area law" (boundary grows sublinearly)
- Provide minimal-cut checks for small partitions (brute-force)

Usage:
    python scripts/w33_holography.py
"""

from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path
from typing import List

import numpy as np
from w33_homology import build_w33


def edge_boundary_size(adj: List[List[int]], S: set) -> int:
    count = 0
    for u in S:
        for v in adj[u]:
            if v not in S:
                count += 1
    return count


def sample_boundary_statistics(adj: List[List[int]], trials: int = 2000):
    n = len(adj)
    stats = []
    for size in range(1, n // 2 + 1):
        sample_sizes = min(trials, math.comb(n, size) if size <= 6 else trials)
        vals = []
        for _ in range(sample_sizes):
            S = set(random.sample(range(n), size))
            vals.append(edge_boundary_size(adj, S))
        stats.append((size, float(np.mean(vals)), float(np.std(vals))))
    return stats


def brute_force_min_cut_for_size(adj: List[List[int]], size: int) -> int:
    # brute-force search for the minimal boundary among subsets of given size
    from itertools import combinations

    n = len(adj)
    best = n * 100
    for comb in combinations(range(n), size):
        S = set(comb)
        b = edge_boundary_size(adj, S)
        if b < best:
            best = b
    return best


def analyze_w33_holography(trials: int = 500):
    t0 = time.time()
    n, vertices, adj, edges = build_w33()
    stats = sample_boundary_statistics(adj, trials=trials)
    # compute minimal-cut for a few small region sizes
    min_cuts = {s: brute_force_min_cut_for_size(adj, s) for s in [1, 2, 3, 4]}

    # entropy-like diagnostics (use log(1 + boundary) as proxy entropy)
    entropy_stats = []
    for size, mean_b, std_b in stats:
        mean_s = float(np.log1p(mean_b))
        std_s = float(std_b / (1.0 + mean_b) if mean_b > 0 else 0.0)
        entropy_stats.append((int(size), mean_s, std_s))

    results = {
        "n": n,
        "sample_boundary_stats": stats,
        "entropy_stats": entropy_stats,
        "min_cuts_small_sizes": min_cuts,
        "elapsed_seconds": time.time() - t0,
    }
    out_dir = Path(__file__).resolve().parent.parent / "checks"
    out_dir.mkdir(exist_ok=True)
    fname = out_dir / f"PART_CXVI_holography_{int(time.time())}.json"
    with open(fname, "w") as f:
        json.dump(results, f, indent=2, default=str)
    return results


if __name__ == "__main__":
    import json

    print(json.dumps(analyze_w33_holography(200), indent=2))
