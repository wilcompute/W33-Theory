#!/usr/bin/env python3
"""Levi cycle quotient theorem for the W33 signed phase frame.

The previous theorem identified ker(A^T) as the span of signed point/line
four-flag relations.  This script identifies those relations as the oriented
incidence/cut space of the Levi graph of W(3,3).

Levi graph data:
  vertices = 40 points + 40 lines = 80
  edges    = point-line flags = 160
  connected = True
  first Betti/cycle rank = E - V + 1 = 160 - 80 + 1 = 81

Thus the protected 81-dimensional phase image is exactly the flag-edge module
modulo local point/line cut relations, i.e. the cycle space of the Levi graph.
This upgrades 160=81+79 to a graph-homological exact sequence:

  0 -> cut(Levi)_{79} -> R^{Flags}_{160} -> cycle(Levi)_{81} -> 0

and the signed phase matrix A realizes the quotient map into the quadrangle frame.
"""
from __future__ import annotations

import json
from collections import Counter, deque, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

P = 3
Vec = tuple[int, int, int, int]


def canonical(v) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def canonical_projective_vector(v: np.ndarray) -> tuple[int, ...]:
    a = tuple(int(x) for x in v.tolist())
    b = tuple(int(x) for x in (2 * v % P).tolist())
    return min(a, b)


def build_geometry():
    points = []
    seen = set()
    for raw in product(range(P), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)
    point_index = {p: i for i, p in enumerate(points)}
    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    edge_index = {e: k for k, e in enumerate(edges)}
    adjacency = [[False] * len(points) for _ in points]
    for i, j in edges:
        adjacency[i][j] = adjacency[j][i] = True
    lines = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    triangles = sorted({tuple(sorted(t)) for L in lines for t in combinations(L, 3)})
    return points, edges, edge_index, adjacency, lines, triangles


def boundary(edges, edge_index, triangles):
    d2 = np.zeros((len(edges), len(triangles)), dtype=np.int8)
    for col, (a, b, c) in enumerate(triangles):
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    return d2 % P


def x_rays(lines, edges, edge_index, d2):
    HZ = d2.T % P
    rays = {}
    flags = {}
    for li, line in enumerate(lines):
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                v = np.zeros(len(edges), dtype=np.int8)
                for val, s in zip(vals, support):
                    v[s] = val
                if np.all((HZ @ v) % P == 0):
                    key = canonical_projective_vector(v.astype(int))
                    if key not in rays:
                        cnt = Counter()
                        for s in support:
                            cnt.update(edges[s])
                        center = [p for p, c in cnt.items() if c == 3][0]
                        rays[key] = v.copy()
                        flags[key] = (center, li)
    ordered = sorted(rays.items(), key=lambda kv: flags[kv[0]])
    return [v for _, v in ordered], [flags[k] for k, _ in ordered]


def oriented_cycle(order, edges, edge_index):
    v = np.zeros(len(edges), dtype=np.int8)
    for a, b in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((a, b)))
        idx = edge_index[e]
        v[idx] = 1 if (a, b) == edges[idx] else 2
    return v


def z_rays(points, edges, edge_index, adjacency):
    rays = {}
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        for c, d in combinations(common, 2):
            v = oriented_cycle([a, c, b, d], edges, edge_index)
            rays.setdefault(canonical_projective_vector(v.astype(int)), v.copy())
    return list(rays.values())


def connected_levi(lines):
    # Levi vertices: points 0..39, lines 40..79.  Edges are flags.
    adj = defaultdict(list)
    for li, L in enumerate(lines):
        lv = 40 + li
        for p in L:
            adj[p].append(lv)
            adj[lv].append(p)
    seen = {0}
    q = deque([0])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    return len(seen) == 80


def find_signed_relations(A, x_flags, n_points=40, n_lines=40):
    # Build the 160 x 80 relation matrix R with one signed local relation per
    # Levi vertex.  Sign choices are determined by annihilating A.
    point_flags = defaultdict(list)
    line_flags = defaultdict(list)
    for i, (p, L) in enumerate(x_flags):
        point_flags[p].append(i)
        line_flags[L].append(i)
    R = np.zeros((len(x_flags), n_points + n_lines), dtype=np.int16)
    for p, idxs in point_flags.items():
        for signs in product((1, -1), repeat=4):
            if np.all(sum(signs[k] * A[idxs[k], :] for k in range(4)) == 0):
                for s, row in zip(signs, idxs):
                    R[row, p] = s
                break
    for L, idxs in line_flags.items():
        for signs in product((1, -1), repeat=4):
            if np.all(sum(signs[k] * A[idxs[k], :] for k in range(4)) == 0):
                for s, row in zip(signs, idxs):
                    R[row, n_points + L] = s
                break
    return R


def main() -> int:
    points, graph_edges, edge_index, adjacency, lines, triangles = build_geometry()
    d2 = boundary(graph_edges, edge_index, triangles)
    X, x_flags = x_rays(lines, graph_edges, edge_index, d2)
    Z = z_rays(points, graph_edges, edge_index, adjacency)
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    A = np.where(raw == 2, -1, raw).astype(np.int16)
    R = find_signed_relations(A, x_flags)

    levi_vertices = 80
    levi_edges = len(x_flags)
    levi_connected = connected_levi(lines)
    levi_cycle_rank = levi_edges - levi_vertices + (1 if levi_connected else 0)
    rank_A = int(np.linalg.matrix_rank(A.astype(float)))
    rank_R = int(np.linalg.matrix_rank(R.astype(float)))
    nullity_left = len(x_flags) - rank_A

    checks = {
        "geometry_counts": len(points) == 40 and len(lines) == 40 and len(x_flags) == 160 and len(Z) == 1620,
        "levi_connected": levi_connected,
        "levi_cycle_rank_81": levi_cycle_rank == 81,
        "relation_rank_79": rank_R == 79,
        "left_nullity_79": nullity_left == 79,
        "relation_space_is_kernel": rank_R == nullity_left,
        "relations_annihilate_A": bool(np.max(np.abs(A.T @ R)) == 0),
        "quotient_dimension_equals_cycle_rank": len(x_flags) - rank_R == levi_cycle_rank == rank_A,
    }

    payload = {
        "theorem_name": "Levi Cycle Quotient Exact Sequence Theorem",
        "summary": {
            "levi_vertices_points_plus_lines": levi_vertices,
            "levi_edges_flags": levi_edges,
            "levi_connected": levi_connected,
            "levi_cycle_rank": levi_cycle_rank,
            "signed_relation_rank": rank_R,
            "phase_matrix_rank": rank_A,
            "flag_module_dimension": len(x_flags),
            "quotient_dimension": len(x_flags) - rank_R,
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "exact_sequence": "0 -> cut(Levi)_79 -> R^Flags_160 -> cycle(Levi)_81 -> 0",
        "identities": {
            "flag_count": "|Flags| = 160",
            "local_relation_generators": "|Points|+|Lines| = 80",
            "connected_cut_rank": "80 - 1 = 79",
            "cycle_rank": "160 - 80 + 1 = 81",
            "projector_split": "160 = 79 + 81",
            "interpretation": "The protected phase image is the Levi cycle space of W(3,3), and the nullspace is the Levi cut/local-relation space.",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_levi_cycle_quotient_exact_sequence.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
