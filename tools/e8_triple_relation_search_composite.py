#!/usr/bin/env python3
"""Composite relation search between E8 orthogonal triple blocks.

We refine relation classes by including:
  - triple type pattern (type1/type2 line counts)
  - full 6x6 inner-product counts between triples

We then search unions of up to K classes for SRG(40,12,2,4).

Outputs:
- artifacts/e8_triple_relation_search_composite.json
- artifacts/e8_triple_relation_search_composite.md
"""
from __future__ import annotations

import json
import os
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PARTITION_JSON = ROOT / "artifacts" / "e8_rootline_partition.json"
OUT_JSON = ROOT / "artifacts" / "e8_triple_relation_search_composite.json"
OUT_MD = ROOT / "artifacts" / "e8_triple_relation_search_composite.md"

MAX_COMB_SIZE = int(os.environ.get("E8_COMPOSITE_MAX_COMB", "3"))


def build_e8_roots() -> np.ndarray:
    roots = []
    # type 1: (±1, ±1, 0,...)
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    v = np.zeros(8)
                    v[i] = s1
                    v[j] = s2
                    roots.append(v)
    # type 2: (±1/2)^8 with even number of minus signs
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(np.array(signs) / 2.0)
    return np.array(roots, dtype=float)


def canonical_line(root: np.ndarray) -> tuple[float, ...]:
    idx = None
    for i, x in enumerate(root):
        if abs(x) > 1e-9:
            idx = i
            break
    if idx is None:
        raise ValueError("Zero root")
    if root[idx] < 0:
        root = -root
    return tuple(root.tolist())


def build_root_lines(roots: np.ndarray) -> list[np.ndarray]:
    line_map = {}
    reps = []
    used = set()
    for i, r in enumerate(roots):
        if i in used:
            continue
        key = canonical_line(r)
        if key in line_map:
            continue
        # find -r
        neg = -r
        j = None
        for k, s in enumerate(roots):
            if np.allclose(s, neg):
                j = k
                break
        if j is None:
            raise RuntimeError("Missing neg root")
        used.add(i)
        used.add(j)
        line_map[key] = len(reps)
        reps.append(r)
    return reps


def root_type(root: np.ndarray) -> str:
    vals = sorted(set(np.abs(root)))
    if vals == [0.0, 1.0]:
        return "type1"
    return "type2"


def is_srg(adj: np.ndarray):
    degrees = adj.sum(axis=1)
    if len(set(degrees)) != 1:
        return None
    k = int(degrees[0])
    lambda_set = set()
    mu_set = set()
    n = adj.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            common = int(np.dot(adj[i], adj[j]))
            if adj[i, j] == 1:
                lambda_set.add(common)
            else:
                mu_set.add(common)
    if len(lambda_set) == 1 and len(mu_set) == 1:
        return k, next(iter(lambda_set)), next(iter(mu_set))
    return None


def main():
    if not PARTITION_JSON.exists():
        raise SystemExit("Missing artifacts/e8_rootline_partition.json; run tools/e8_rootline_partition.py")
    partition = json.loads(PARTITION_JSON.read_text())
    triples = partition.get("solution_triples", [])
    if len(triples) != 40:
        raise SystemExit(f"Expected 40 triples, got {len(triples)}")

    roots = build_e8_roots()
    line_reps = build_root_lines(roots)
    if len(line_reps) != 120:
        raise SystemExit(f"Expected 120 root lines, got {len(line_reps)}")

    line_types = [root_type(r) for r in line_reps]
    triple_patterns = []
    for t in triples:
        c1 = sum(1 for idx in t if line_types[idx] == "type1")
        c2 = 3 - c1
        triple_patterns.append((c1, c2))

    # 6-root sets for each triple
    triple_roots = []
    for t in triples:
        roots6 = []
        for idx in t:
            r = line_reps[idx]
            roots6.append(r)
            roots6.append(-r)
        triple_roots.append(np.array(roots6))

    # Build composite relation classes
    class_keys = []
    class_edges = {}
    class_degs = {}
    for i in range(40):
        for j in range(i + 1, 40):
            A = triple_roots[i]
            B = triple_roots[j]
            prod = A @ B.T
            counts = (
                int(np.sum(np.isclose(prod, -1.0))),
                int(np.sum(np.isclose(prod, 0.0))),
                int(np.sum(np.isclose(prod, 1.0))),
            )
            p_i = triple_patterns[i]
            p_j = triple_patterns[j]
            p_key = tuple(sorted([p_i, p_j]))
            key = (p_key, counts)
            if key not in class_edges:
                class_edges[key] = []
            class_edges[key].append((i, j))
    class_keys = list(class_edges.keys())

    # Precompute degree contribution arrays
    for key in class_keys:
        deg = [0] * 40
        for i, j in class_edges[key]:
            deg[i] += 1
            deg[j] += 1
        class_degs[key] = deg

    candidates = []
    target = []

    # search combinations up to MAX_COMB_SIZE
    for r in range(1, MAX_COMB_SIZE + 1):
        for combo in combinations(class_keys, r):
            # degree check
            deg = [0] * 40
            for key in combo:
                arr = class_degs[key]
                for i in range(40):
                    deg[i] += arr[i]
            if len(set(deg)) != 1:
                continue
            # build adjacency
            adj = np.zeros((40, 40), dtype=int)
            for key in combo:
                for i, j in class_edges[key]:
                    adj[i, j] = 1
                    adj[j, i] = 1
            params = is_srg(adj)
            if params:
                k, lam, mu = params
                item = {"combo_size": r, "k": k, "lambda": lam, "mu": mu}
                candidates.append(item)
                if (k, lam, mu) == (12, 2, 4):
                    target.append(item)

    summary = {
        "class_count": len(class_keys),
        "combo_max_size": MAX_COMB_SIZE,
        "candidate_count": len(candidates),
        "target_srg_40_12_2_4": target,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# E8 Composite Triple-Relation Search")
    lines.append("")
    lines.append(f"- relation classes: {summary['class_count']}")
    lines.append(f"- combo max size: {summary['combo_max_size']}")
    lines.append(f"- SRG candidates: {summary['candidate_count']}")
    lines.append(f"- SRG(40,12,2,4) matches: {len(target)}")
    if target:
        for item in target:
            lines.append(f"- combo size={item['combo_size']} -> k={item['k']}, λ={item['lambda']}, μ={item['mu']}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
