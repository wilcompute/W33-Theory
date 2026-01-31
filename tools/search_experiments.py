#!/usr/bin/env python3
"""Run parameter-sweep experiments for the equivariant bijection local search.

Produces artifacts/eq_search_experiments_{timestamp}.json with a summary of runs.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List

from tools.e8_w33_bijection import load_explicit_bijection
from tools.search_equivariant_bijection_hillclimb import local_search

ROOT = Path(__file__).resolve().parents[1]


def triangle_count_for_mapping(mapping: List[int], roots: List[List[int]]):
    import numpy as np

    R = np.array(roots, dtype=int)
    dotm = R @ R.T
    # Reconstruct adjacency triangles in same manner as local_search
    from tools.search_equivariant_bijection_hillclimb import \
        build_adjacency_list

    _, adj = build_adjacency_list()
    triangles = []
    n = len(adj)
    for a in range(n):
        for b in range(a + 1, n):
            if not adj[a][b]:
                continue
            for c in range(b + 1, n):
                if adj[a][c] and adj[b][c]:
                    triangles.append((a, b, c))
    cnt = 0
    for a, b, c in triangles:
        if (
            int(dotm[mapping[a], mapping[b]]) == -2
            and int(dotm[mapping[a], mapping[c]]) == -2
            and int(dotm[mapping[b], mapping[c]]) == -2
        ):
            cnt += 1
    return cnt


def run_sweep(
    triangle_weights: List[int],
    seeds: List[int],
    iterations: int = 2000,
    time_limit: float = 2.0,
) -> Dict:
    data = load_explicit_bijection()
    roots = data["root_coords"]
    baseline_res = local_search(iterations=1, seed=0, time_limit=0.1, triangle_weight=0)
    baseline_score = baseline_res["baseline_score"]

    runs = []
    best_overall = None
    for tw in triangle_weights:
        for s in seeds:
            t0 = time.time()
            res = local_search(
                iterations=iterations, seed=s, time_limit=time_limit, triangle_weight=tw
            )
            res["triangle_weight"] = tw
            res["seed"] = s
            res["time_taken"] = time.time() - t0
            # compute triangle count for best mapping
            tri_cnt = triangle_count_for_mapping(res["mapping"], roots)
            res["triangle_count"] = tri_cnt
            runs.append(res)
            if best_overall is None or res["best_score"] > best_overall["best_score"]:
                best_overall = res

    out = {
        "baseline_score": baseline_score,
        "runs": runs,
        "best_overall": best_overall,
    }
    out_path = ROOT / "artifacts" / f"eq_search_experiments_{int(time.time())}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote", out_path)
    return out


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--weights", type=int, nargs="+", default=[0, 5, 20])
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1])
    p.add_argument("--iterations", type=int, default=2000)
    p.add_argument("--time-limit", type=float, default=2.0)
    args = p.parse_args()
    run_sweep(
        triangle_weights=args.weights,
        seeds=args.seeds,
        iterations=args.iterations,
        time_limit=args.time_limit,
    )
