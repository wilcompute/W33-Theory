#!/usr/bin/env python3
"""Search for alternative E8 root-line partitions that yield SRG(40,12,2,4).

We attempt randomized exact covers of the 120 E8 root lines by 40 orthogonal
triples. For each partition found, we build a 40-vertex graph where adjacency
is defined by selected orthogonal-line-pair counts (0..9), and test for
SRG(40,12,2,4).

Outputs:
- artifacts/e8_partition_search.json
- artifacts/e8_partition_search.md
"""
from __future__ import annotations

import json
import os
import random
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TAG = os.environ.get("E8_PARTITION_TAG", "").strip()
suffix = f"_{TAG}" if TAG else ""
OUT_JSON = ROOT / "artifacts" / f"e8_partition_search{suffix}.json"
OUT_MD = ROOT / "artifacts" / f"e8_partition_search{suffix}.md"

TRIES = int(os.environ.get("E8_PARTITION_TRIES", "20"))
MAX_NODES = int(os.environ.get("E8_PARTITION_MAX_NODES", "200000"))
SEED = int(os.environ.get("E8_PARTITION_SEED", "12345"))
RELATION_MODE = os.environ.get("E8_RELATION_MODE", "orthocount").strip().lower()
MAX_CLASS_UNIONS = int(os.environ.get("E8_PARTITION_MAX_CLASS_UNIONS", "4096"))
TARGET_PATTERN = os.environ.get("E8_PARTITION_TARGET_PATTERN", "").strip()


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


def build_orthogonality_graph(reps: list[np.ndarray]) -> np.ndarray:
    n = len(reps)
    M = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(float(np.dot(reps[i], reps[j]))) < 1e-9:
                M[i, j] = True
                M[j, i] = True
    return M


def root_type(root: np.ndarray) -> str:
    vals = sorted(set(np.abs(root)))
    if vals == [0.0, 1.0]:
        return "type1"
    return "type2"


def find_triangles(adj: np.ndarray) -> list[tuple[int, int, int]]:
    n = adj.shape[0]
    triangles = []
    neigh = [np.where(adj[i])[0] for i in range(n)]
    for i in range(n):
        ni = neigh[i]
        for j in ni:
            if j <= i:
                continue
            common = np.intersect1d(ni, neigh[j], assume_unique=False)
            for k in common:
                if k <= j:
                    continue
                triangles.append((i, int(j), int(k)))
    return triangles


def parse_target_pattern(spec: str):
    # spec example: "20x(0,3);18x(3,0);2x(1,2)"
    if not spec:
        return None
    targets = {}
    parts = [p.strip() for p in spec.split(";") if p.strip()]
    for part in parts:
        if "x" not in part:
            continue
        count_str, pair_str = part.split("x", 1)
        count = int(count_str.strip())
        pair_str = pair_str.strip().strip("()")
        a_str, b_str = pair_str.split(",", 1)
        key = (int(a_str.strip()), int(b_str.strip()))
        targets[key] = count
    return targets


def exact_cover_random(n_vertices: int, triangles: list[tuple[int, int, int]], rng: random.Random):
    tri_for_vertex = [[] for _ in range(n_vertices)]
    for idx, (a, b, c) in enumerate(triangles):
        tri_for_vertex[a].append(idx)
        tri_for_vertex[b].append(idx)
        tri_for_vertex[c].append(idx)

    used_tri = [False] * len(triangles)
    covered = [False] * n_vertices
    solution: list[int] = []
    nodes = 0

    def choose_vertex():
        # choose uncovered vertex with fewest available triangles (random tie-break)
        best_v = None
        best_count = None
        candidates = []
        for v in range(n_vertices):
            if covered[v]:
                continue
            cnt = 0
            for t in tri_for_vertex[v]:
                if used_tri[t]:
                    continue
                a, b, c = triangles[t]
                if covered[a] or covered[b] or covered[c]:
                    continue
                cnt += 1
            if best_count is None or cnt < best_count:
                best_count = cnt
                candidates = [v]
            elif cnt == best_count:
                candidates.append(v)
        if not candidates:
            return None, 0
        return rng.choice(candidates), best_count

    def search():
        nonlocal nodes
        nodes += 1
        if nodes > MAX_NODES:
            return False
        if all(covered):
            return True
        v, cnt = choose_vertex()
        if v is None or cnt == 0:
            return False
        choices = [t for t in tri_for_vertex[v] if not used_tri[t]]
        rng.shuffle(choices)
        for t in choices:
            a, b, c = triangles[t]
            if covered[a] or covered[b] or covered[c]:
                continue
            used_tri[t] = True
            covered[a] = covered[b] = covered[c] = True
            solution.append(t)
            if search():
                return True
            solution.pop()
            covered[a] = covered[b] = covered[c] = False
            used_tri[t] = False
        return False

    ok = search()
    return ok, solution, nodes


def relation_graph_orthocount(triples: list[tuple[int, int, int]], ortho: np.ndarray, selected_counts: set[int]):
    n = len(triples)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        A = triples[i]
        for j in range(i + 1, n):
            B = triples[j]
            cnt = 0
            for a in A:
                for b in B:
                    if ortho[a, b]:
                        cnt += 1
            if cnt in selected_counts:
                adj[i, j] = 1
                adj[j, i] = 1
    return adj


def relation_graph_fullip(triples: list[tuple[int, int, int]], line_reps: list[np.ndarray], selected_classes: set[tuple[int, int, int]]):
    # build 6-root sets per triple
    triple_roots = []
    for t in triples:
        roots6 = []
        for idx in t:
            r = line_reps[idx]
            roots6.append(r)
            roots6.append(-r)
        triple_roots.append(np.array(roots6))

    n = len(triples)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        A = triple_roots[i]
        for j in range(i + 1, n):
            B = triple_roots[j]
            prod = A @ B.T
            counts = (
                int(np.sum(np.isclose(prod, -1.0))),
                int(np.sum(np.isclose(prod, 0.0))),
                int(np.sum(np.isclose(prod, 1.0))),
            )
            if counts in selected_classes:
                adj[i, j] = 1
                adj[j, i] = 1
    return adj


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
    rng = random.Random(SEED)
    roots = build_e8_roots()
    lines = build_root_lines(roots)
    ortho = build_orthogonality_graph(lines)
    triangles = find_triangles(ortho)
    line_types = [root_type(r) for r in lines]
    target_pattern = parse_target_pattern(TARGET_PATTERN)

    counts_set = list(range(10))  # 0..9 orthogonal line pairs
    results = {
        "tries": TRIES,
        "max_nodes": MAX_NODES,
        "triangles": len(triangles),
        "found_partition": False,
        "found_relation": None,
        "found_srg": None,
        "relation_mode": RELATION_MODE,
        "target_pattern": TARGET_PATTERN or None,
    }

    for attempt in range(1, TRIES + 1):
        ok, sol, nodes = exact_cover_random(len(lines), triangles, rng)
        if not ok:
            results["last_attempt"] = {"attempt": attempt, "nodes": nodes, "ok": False}
            continue
        triples = [triangles[i] for i in sol]
        # enforce target pattern if provided
        if target_pattern:
            pattern_counts = {}
            for t in triples:
                c1 = sum(1 for idx in t if line_types[idx] == "type1")
                c2 = 3 - c1
                key = (c1, c2)
                pattern_counts[key] = pattern_counts.get(key, 0) + 1
            if pattern_counts != target_pattern:
                results["last_attempt"] = {
                    "attempt": attempt,
                    "nodes": nodes,
                    "ok": True,
                    "pattern_counts": {str(k): v for k, v in pattern_counts.items()},
                    "pattern_match": False,
                }
                continue

        # try all unions of relation classes
        found = None
        if RELATION_MODE == "orthocount":
            for mask in range(1, 1 << len(counts_set)):
                selected = {counts_set[i] for i in range(len(counts_set)) if (mask >> i) & 1}
                adj = relation_graph_orthocount(triples, ortho, selected)
                params = is_srg(adj)
                if params:
                    k, lam, mu = params
                    if (k, lam, mu) == (12, 2, 4):
                        found = {"selected_counts": sorted(list(selected)), "params": params}
                        break
        elif RELATION_MODE == "fullip":
            # compute relation classes between triples
            class_keys = set()
            # sample relation classes first
            for i in range(len(triples)):
                for j in range(i + 1, len(triples)):
                    A = triples[i]
                    B = triples[j]
                    # 6x6 inner products
                    rootsA = []
                    rootsB = []
                    for idx in A:
                        r = lines[idx]
                        rootsA.extend([r, -r])
                    for idx in B:
                        r = lines[idx]
                        rootsB.extend([r, -r])
                    prod = np.array(rootsA) @ np.array(rootsB).T
                    counts = (
                        int(np.sum(np.isclose(prod, -1.0))),
                        int(np.sum(np.isclose(prod, 0.0))),
                        int(np.sum(np.isclose(prod, 1.0))),
                    )
                    class_keys.add(counts)
            class_keys = sorted(class_keys)
            total_subsets = 1 << len(class_keys)
            subsets = []
            if total_subsets > MAX_CLASS_UNIONS:
                for i in range(len(class_keys)):
                    subsets.append({class_keys[i]})
                    subsets.append(set(class_keys) - {class_keys[i]})
            else:
                for mask in range(1, total_subsets):
                    subset = {class_keys[i] for i in range(len(class_keys)) if (mask >> i) & 1}
                    subsets.append(subset)
            for subset in subsets:
                adj = relation_graph_fullip(triples, lines, subset)
                params = is_srg(adj)
                if params:
                    k, lam, mu = params
                    if (k, lam, mu) == (12, 2, 4):
                        found = {"selected_classes": sorted(list(subset)), "params": params}
                        break
        if found:
            results["found_partition"] = True
            results["found_relation"] = found
            results["found_srg"] = (12, 2, 4)
            results["partition_triples"] = triples
            results["attempt"] = attempt
            results["nodes"] = nodes
            break

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines_md = []
    lines_md.append("# E8 Partition Search (Randomized)")
    lines_md.append("")
    lines_md.append(f"- tries: {results['tries']}")
    lines_md.append(f"- max nodes per try: {results['max_nodes']}")
    lines_md.append(f"- triangle count: {results['triangles']}")
    lines_md.append(f"- relation mode: {results['relation_mode']}")
    if results.get("target_pattern"):
        lines_md.append(f"- target pattern: {results['target_pattern']}")
    lines_md.append(f"- found partition with SRG(40,12,2,4): {results['found_partition']}")
    if results["found_partition"]:
        lines_md.append(f"- attempt: {results['attempt']}")
        lines_md.append(f"- selected counts: {results['found_relation']['selected_counts']}")
    else:
        if "last_attempt" in results:
            lines_md.append(f"- last attempt nodes: {results['last_attempt']['nodes']}")
    OUT_MD.write_text("\n".join(lines_md) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
