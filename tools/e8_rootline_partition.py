#!/usr/bin/env python3
"""Find a partition of E8 root lines into triples of mutually orthogonal lines.

If successful, this yields 40 triples of root lines (120 total lines),
equivalently 40 octahedra (6 roots each) in the E8 orthogonality graph.

Outputs:
- artifacts/e8_rootline_partition.json
- artifacts/e8_rootline_partition.md
"""

from __future__ import annotations

import json
import os
from itertools import combinations, product
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "e8_rootline_partition.json"
OUT_MD = ROOT / "artifacts" / "e8_rootline_partition.md"

MAX_NODES = int(os.environ.get("E8_PARTITION_MAX_NODES", "200000"))


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


def canonical_line(root: np.ndarray) -> Tuple[float, ...]:
    # Normalize sign to make first nonzero positive
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


def build_root_lines(
    roots: np.ndarray,
) -> Tuple[List[np.ndarray], List[Tuple[int, int]]]:
    line_map: Dict[Tuple[float, ...], int] = {}
    reps: List[np.ndarray] = []
    pairs: List[Tuple[int, int]] = []
    used = set()
    for i, r in enumerate(roots):
        if i in used:
            continue
        # find index of -r
        neg = -r
        # brute force search via hash
        # build canonical key
        key = canonical_line(r)
        if key in line_map:
            continue
        # find neg index
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
        pairs.append((i, j))
    return reps, pairs


def build_orthogonality_graph(reps: List[np.ndarray]) -> np.ndarray:
    n = len(reps)
    M = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            ip = float(np.dot(reps[i], reps[j]))
            if abs(ip) < 1e-9:
                M[i, j] = 1
                M[j, i] = 1
    return M


def find_triangles(adj: np.ndarray) -> List[Tuple[int, int, int]]:
    n = adj.shape[0]
    triangles = []
    # adjacency lists
    neigh = [np.where(adj[i] == 1)[0] for i in range(n)]
    for i in range(n):
        ni = neigh[i]
        for j_idx in range(len(ni)):
            j = int(ni[j_idx])
            if j <= i:
                continue
            common = np.intersect1d(ni, neigh[j], assume_unique=False)
            for k in common:
                k = int(k)
                if k <= j:
                    continue
                triangles.append((i, j, k))
    return triangles


def exact_cover_triangles(n_vertices: int, triangles: List[Tuple[int, int, int]]):
    # build incidence
    tri_for_vertex: List[List[int]] = [[] for _ in range(n_vertices)]
    for idx, (a, b, c) in enumerate(triangles):
        tri_for_vertex[a].append(idx)
        tri_for_vertex[b].append(idx)
        tri_for_vertex[c].append(idx)

    used_tri = [False] * len(triangles)
    covered = [False] * n_vertices
    solution: List[int] = []
    nodes = 0

    # precompute triangle vertices
    tri_vertices = triangles

    def choose_vertex():
        # choose uncovered vertex with fewest available triangles
        best_v = None
        best_count = None
        for v in range(n_vertices):
            if covered[v]:
                continue
            cnt = 0
            for t in tri_for_vertex[v]:
                if used_tri[t]:
                    continue
                a, b, c = tri_vertices[t]
                if covered[a] or covered[b] or covered[c]:
                    continue
                cnt += 1
            if best_count is None or cnt < best_count:
                best_count = cnt
                best_v = v
            if best_count == 0:
                break
        return best_v, best_count

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
        # try each triangle containing v
        for t in tri_for_vertex[v]:
            if used_tri[t]:
                continue
            a, b, c = tri_vertices[t]
            if covered[a] or covered[b] or covered[c]:
                continue
            # choose t
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


def main():
    roots = build_e8_roots()
    reps, pairs = build_root_lines(roots)
    adj = build_orthogonality_graph(reps)
    triangles = find_triangles(adj)

    ok, sol, nodes = exact_cover_triangles(len(reps), triangles)

    summary = {
        "root_count": int(roots.shape[0]),
        "line_count": int(len(reps)),
        "orthogonality_degree_set": sorted(
            set(int(np.sum(adj[i])) for i in range(len(reps)))
        ),
        "triangle_count": int(len(triangles)),
        "exact_cover_found": bool(ok),
        "search_nodes": int(nodes),
        "max_nodes": int(MAX_NODES),
    }

    if ok:
        # store one solution as list of triples
        triples = []
        for idx in sol:
            a, b, c = triangles[idx]
            triples.append([int(a), int(b), int(c)])
        summary["solution_triples"] = triples

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = []
    lines.append("# E8 Root-Line Orthogonal Triple Partition")
    lines.append("")
    lines.append(f"- E8 roots: {summary['root_count']}")
    lines.append(f"- Root lines (± pairs): {summary['line_count']}")
    lines.append(f"- Orthogonality degree set: {summary['orthogonality_degree_set']}")
    lines.append(f"- Orthogonal triples (triangles): {summary['triangle_count']}")
    lines.append(f"- Exact cover found: {summary['exact_cover_found']}")
    lines.append(
        f"- Search nodes: {summary['search_nodes']} (limit {summary['max_nodes']})"
    )
    if ok:
        lines.append("")
        lines.append("## One Partition (40 triples)")
        for t in summary["solution_triples"]:
            lines.append(f"- {t}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
