#!/usr/bin/env python3
"""Fix duplicate root assignments in a bijection by reassigning duplicates
to the nearest unused roots (greedy).

Usage:
  python scripts/fix_duplicates_assign_closest.py --in checks/PART_CVII_e8_bijection_intermediate_1770491204.json --out checks/PART_CVII_e8_bijection_repaired_from_intermediate_1770491204.json
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from importlib import util
from pathlib import Path

import numpy as np

# load helper functions
spec_chk = util.spec_from_file_location("check", "scripts/check_triangle_coverage.py")
check = util.module_from_spec(spec_chk)
spec_chk.loader.exec_module(check)

spec_e8 = util.spec_from_file_location("e8", "scripts/e8_embedding_group_theoretic.py")
e8 = util.module_from_spec(spec_e8)
spec_e8.loader.exec_module(e8)

spec_opt = util.spec_from_file_location("opt", "scripts/optimize_bijection_cocycle.py")
opt = util.module_from_spec(spec_opt)
spec_opt.loader.exec_module(opt)


def compute_costs():
    X, edges = check.compute_embedding_matrix()
    A_mat = np.vstack(
        [(X[i] - X[j]) / (np.linalg.norm(X[i] - X[j]) + 1e-12) for (i, j) in edges]
    )
    roots = check.generate_scaled_e8_roots()
    roots_arr = np.array(roots, dtype=int)
    roots_unit = roots_arr.astype(float) / np.linalg.norm(
        roots_arr.astype(float), axis=1, keepdims=True
    )
    cost = np.linalg.norm(A_mat[:, None, :] - roots_unit[None, :, :], axis=2)
    return cost, edges, roots


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="inpath", required=True)
    parser.add_argument("--out", dest="outpath", required=False)
    args = parser.parse_args()

    inpath = Path(args.inpath)
    if not inpath.exists():
        raise SystemExit(f"Input file not found: {inpath}")

    outpath = (
        Path(args.outpath)
        if args.outpath
        else Path("checks") / f"PART_CVII_e8_bijection_repaired_from_{inpath.stem}.json"
    )

    j = json.loads(inpath.read_text(encoding="utf-8"))
    bij = {int(k): int(v) for k, v in j.get("bijection", {}).items()}

    cost, edges, roots = compute_costs()

    # find duplicates
    vals = list(bij.values())
    cnt = Counter(vals)
    duplicates = [r for r, c in cnt.items() if c > 1]
    if not duplicates:
        print("No duplicates found; writing copy of input to", outpath)
        outpath.write_text(json.dumps(
                {"bijection": {str(k, encoding="utf-8"): int(v) for k, v in bij.items()}}, indent=2
            ),
            encoding="utf-8",
        )
        return

    # determine available roots (those not used)
    used = set(vals)
    all_roots = set(range(len(roots)))
    unused = sorted(list(all_roots - used))
    print(
        f"Found {len(duplicates)} duplicated roots (duplicates_count={sum(cnt[r]-1 for r in duplicates)}). Unused roots: {len(unused)}"
    )

    # build list of edges that have duplicate assignments (but keep one occurrence per duplicate root)
    edge_by_root = {}
    for e, r in bij.items():
        edge_by_root.setdefault(r, []).append(e)

    edges_to_fix = []
    for r, es in edge_by_root.items():
        if len(es) > 1:
            # keep the one edge with smallest cost to root r (best match); reassign others
            es_sorted = sorted(
                es, key=lambda e: cost[e, r] if r < cost.shape[1] else float("inf")
            )
            keep = es_sorted[0]
            for e in es_sorted[1:]:
                edges_to_fix.append(e)

    print(f"Edges to reassign: {len(edges_to_fix)}")

    # greedy: for each edge to fix, assign nearest available root
    # precompute for each edge a sorted list of candidate roots by cost
    N_edges = cost.shape[0]
    root_candidates_sorted = [list(np.argsort(cost[e])) for e in range(N_edges)]

    used_roots = set(bij.values())
    # remove duplicates occurrences, leaving one copy of duplicated roots in used_roots
    # (used_roots already a set)

    for e in edges_to_fix:
        # find nearest root not currently used
        for r in root_candidates_sorted[e]:
            if r not in used_roots:
                bij[e] = int(r)
                used_roots.add(r)
                break
        else:
            # fallback: use any unused (should not happen)
            if unused:
                r = unused.pop(0)
                bij[e] = int(r)
                used_roots.add(r)
            else:
                # no roots available; leave as-is
                print("Warning: no unused roots left to assign for edge", e)

    # final check
    vals2 = list(bij.values())
    cnt2 = Counter(vals2)
    duplicates2 = [r for r, c in cnt2.items() if c > 1]

    outpath.parent.mkdir(parents=True, exist_ok=True)
    outjson = {"bijection": {str(k): int(v) for k, v in bij.items()}}
    outpath.write_text(json.dumps(outjson, indent=2), encoding="utf-8")

    # compute exact counts before/after
    n, vertices, adj, edges = e8.build_w33()
    tri_list = opt.build_triangles(n, adj)
    roots_full = e8.generate_e8_roots()

    exact_before = sum(
        1
        for t in tri_list
        if opt.triangle_exact(
            roots_full,
            {int(k): int(v) for k, v in j.get("bijection", {}).items()},
            edges,
            t,
        )
    )
    exact_after = sum(
        1 for t in tri_list if opt.triangle_exact(roots_full, bij, edges, t)
    )

    print(
        f"Wrote {outpath}: duplicates_before={len(duplicates)}, duplicates_after={len(duplicates2)}, exact_before={exact_before}, exact_after={exact_after}"
    )


if __name__ == "__main__":
    main()
