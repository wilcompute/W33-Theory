#!/usr/bin/env python3
"""Signed nullspace theorem for the W33 minimal logical phase frame.

The signed flag-quadrangle matrix A has shape 160 x 1620 and rank 81, so the
left nullspace has dimension 79.  This script identifies that nullspace exactly.

For every point p of W(3,3), the four flags (p,L) through p satisfy a signed
four-term relation among rows of A.  For every line L, the four flags (p,L)
on L also satisfy a signed four-term relation.  These 40+40=80 local signed
relations have one global dependence, hence span dimension 79, and they lie in
ker(A^T).  Therefore they are exactly the full rank-79 projector-null sector.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
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


def boundary(points, edges, edge_index, triangles):
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


def find_four_term_relations(A: np.ndarray, flag_groups: dict[int, list[int]]):
    relations = {}
    relation_counts = Counter()
    for key, idxs in flag_groups.items():
        sols = []
        for signs in product((1, -1), repeat=4):
            vec = sum(signs[k] * A[idxs[k], :] for k in range(4))
            if np.all(vec == 0):
                sols.append(signs)
        relations[key] = sols[0]
        relation_counts[len(sols)] += 1
    return relations, relation_counts


def main() -> int:
    points, edges, edge_index, adjacency, lines, triangles = build_geometry()
    d2 = boundary(points, edges, edge_index, triangles)
    X, x_flags = x_rays(lines, edges, edge_index, d2)
    Z = z_rays(points, edges, edge_index, adjacency)
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    A = np.where(raw == 2, -1, raw).astype(np.int16)
    S = A @ A.T

    point_flags: dict[int, list[int]] = defaultdict(list)
    line_flags: dict[int, list[int]] = defaultdict(list)
    for i, (p, L) in enumerate(x_flags):
        point_flags[p].append(i)
        line_flags[L].append(i)

    point_rels, point_rel_counts = find_four_term_relations(A, point_flags)
    line_rels, line_rel_counts = find_four_term_relations(A, line_flags)

    R = np.zeros((len(X), 80), dtype=np.int16)
    for p, idxs in point_flags.items():
        for sign, row_idx in zip(point_rels[p], idxs):
            R[row_idx, p] = sign
    for L, idxs in line_flags.items():
        for sign, row_idx in zip(line_rels[L], idxs):
            R[row_idx, 40 + L] = sign

    AT_R = A.T @ R
    S_R = S @ R
    rank_A = int(np.linalg.matrix_rank(A.astype(float)))
    rank_R = int(np.linalg.matrix_rank(R.astype(float)))

    checks = {
        "geometry_counts": len(points) == 40 and len(edges) == 240 and len(lines) == 40 and len(X) == 160 and len(Z) == 1620,
        "rank_A_81": rank_A == 81,
        "left_nullity_79": len(X) - rank_A == 79,
        "each_point_has_two_global_sign_choices": point_rel_counts == Counter({2: 40}),
        "each_line_has_two_global_sign_choices": line_rel_counts == Counter({2: 40}),
        "relations_annihilate_A": bool(np.max(np.abs(AT_R)) == 0),
        "relations_annihilate_projector": bool(np.max(np.abs(S_R)) == 0),
        "relation_span_rank_79": rank_R == 79,
        "relations_equal_full_left_kernel": rank_R == len(X) - rank_A,
    }

    payload = {
        "theorem_name": "Signed Point-Line Nullspace Theorem",
        "summary": {
            "flags": len(X),
            "quadrangles": len(Z),
            "rank_A": rank_A,
            "left_nullity": len(X) - rank_A,
            "point_relations": 40,
            "line_relations": 40,
            "total_local_relations": 80,
            "relation_span_rank": rank_R,
            "global_dependence_count": 80 - rank_R,
            "all_checks_passed": all(checks.values()),
        },
        "checks": checks,
        "point_relation_solution_counts": dict(point_rel_counts),
        "line_relation_solution_counts": dict(line_rel_counts),
        "identities": {
            "nullity": "160 - 81 = 79",
            "local_relations": "40 point relations + 40 line relations = 80",
            "one_global_dependence": "rank(local relation matrix) = 79",
            "kernel_identification": "span(point/line signed four-flag relations) = ker(A^T) = ker(AA^T)",
        },
    }
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "w33_signed_nullspace_point_line_relations.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["summary"]["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
