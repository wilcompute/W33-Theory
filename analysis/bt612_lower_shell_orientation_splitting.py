#!/usr/bin/env python3
"""BT612: lower-shell orientation splitting theorem.

BT611 showed that the folded cubic Hashimoto transfer

    F3 = T B^3 T^T

has a perfect endpoint component F3 o A4 = 28 A4, while lower distance shells
carry orientation residuals.  BT612 classifies those residuals.

For ordered flags f=(p,l), g=(q,m):

  distance 1:
    same line  -> 4
    same point -> 18

  distance 2:
    p in m and q not in l -> 27
    q in l and p not in m -> 6

  distance 3:
    p and q collinear     -> 24
    p and q noncollinear  -> 26

  distance 4:
    terminal/opposite shell -> 28 uniformly.

Thus the non-radial residual is an ordered orientation phenomenon on the lower
shells only.  The protected terminal shell has no residual.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np


def norm_vec(v: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    v = tuple(x % 3 for x in v)
    if all(x == 0 for x in v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in v)
    raise AssertionError("unreachable")


def symp(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def build_geometry():
    pts = sorted({norm_vec(v) for v in product(range(3), repeat=4) if any(v)})
    pt_index = {p: i for i, p in enumerate(pts)}
    edges = [(i, j) for i, j in combinations(range(len(pts)), 2) if symp(pts[i], pts[j]) == 0]
    adj = [set() for _ in pts]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    lines = set()
    for i, j in edges:
        u, v = pts[i], pts[j]
        line = set()
        for a, b in product(range(3), repeat=2):
            if a == 0 and b == 0:
                continue
            w = norm_vec(tuple((a * u[t] + b * v[t]) % 3 for t in range(4)))
            line.add(pt_index[w])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    line_sets = [set(line) for line in lines]
    edge_line = {}
    for li, line in enumerate(lines):
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li

    flags = []
    flag_index = {}
    for li, line in enumerate(lines):
        for p in line:
            flag_index[(p, li)] = len(flags)
            flags.append((p, li))

    directed = []
    for i, j in edges:
        li = edge_line[(i, j)]
        directed.append((i, j, li))
        directed.append((j, i, li))
    directed_index = {(i, j): idx for idx, (i, j, _li) in enumerate(directed)}
    return pts, edges, adj, lines, line_sets, edge_line, flags, flag_index, directed, directed_index


def flag_distance_matrix(flags):
    n = len(flags)
    A1 = np.zeros((n, n), dtype=int)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i != j and (p == q or l == m):
                A1[i, j] = 1
    dist = np.full((n, n), 99, dtype=int)
    for s in range(n):
        dist[s, s] = 0
        queue = [s]
        for u in queue:
            for v in np.nonzero(A1[u])[0]:
                if dist[s, v] == 99:
                    dist[s, v] = dist[s, u] + 1
                    queue.append(v)
    return dist


def classify_pair(f, g, d: int, line_sets, edge_line) -> str:
    p, l = f
    q, m = g
    p_in_m = p in line_sets[m]
    q_in_l = q in line_sets[l]
    pq_collinear = p != q and tuple(sorted((p, q))) in edge_line
    if d == 0:
        return "same_flag"
    if d == 1:
        if p == q:
            return "A1_same_point"
        if l == m:
            return "A1_same_line"
    if d == 2:
        if p_in_m and not q_in_l:
            return "A2_forward_cross_p_in_target_line"
        if q_in_l and not p_in_m:
            return "A2_backward_cross_q_in_source_line"
    if d == 3:
        if pq_collinear:
            return "A3_collinear_source_points"
        return "A3_noncollinear_source_points"
    if d == 4:
        return "A4_terminal_opposite"
    raise AssertionError((f, g, d, p_in_m, q_in_l, pq_collinear))


def main() -> int:
    pts, edges, adj, lines, line_sets, edge_line, flags, flag_index, directed, directed_index = build_geometry()
    T = np.zeros((160, 480), dtype=int)
    for de, (tail, _head, li) in enumerate(directed):
        T[flag_index[(tail, li)], de] = 1

    B = np.zeros((480, 480), dtype=int)
    for a, (u, v, _li) in enumerate(directed):
        for w in adj[v]:
            if w != u:
                B[a, directed_index[(v, w)]] = 1

    dist = flag_distance_matrix(flags)
    F3 = T @ np.linalg.matrix_power(B, 3) @ T.T

    class_profiles: dict[str, Counter] = defaultdict(Counter)
    distance_class_counts: dict[str, Counter] = defaultdict(Counter)
    for i, f in enumerate(flags):
        for j, g in enumerate(flags):
            d = int(dist[i, j])
            cls = classify_pair(f, g, d, line_sets, edge_line)
            class_profiles[cls][int(F3[i, j])] += 1
            distance_class_counts[str(d)][cls] += 1

    expected_profiles = {
        "same_flag": {12: 160},
        "A1_same_line": {4: 480},
        "A1_same_point": {18: 480},
        "A2_forward_cross_p_in_target_line": {27: 1440},
        "A2_backward_cross_q_in_source_line": {6: 1440},
        "A3_collinear_source_points": {24: 4320},
        "A3_noncollinear_source_points": {26: 4320},
        "A4_terminal_opposite": {28: 12960},
    }
    serial_profiles = {k: {str(a): b for a, b in sorted(v.items())} for k, v in sorted(class_profiles.items())}
    checks = {
        "all_expected_classes_present": set(class_profiles) == set(expected_profiles),
        "profiles_match_expected_values": all(dict(class_profiles[k]) == v for k, v in expected_profiles.items()),
        "distance1_splits_evenly": distance_class_counts["1"] == Counter({"A1_same_line": 480, "A1_same_point": 480}),
        "distance2_splits_evenly": distance_class_counts["2"] == Counter({"A2_forward_cross_p_in_target_line": 1440, "A2_backward_cross_q_in_source_line": 1440}),
        "distance3_splits_evenly": distance_class_counts["3"] == Counter({"A3_collinear_source_points": 4320, "A3_noncollinear_source_points": 4320}),
        "distance4_no_split": distance_class_counts["4"] == Counter({"A4_terminal_opposite": 12960}),
    }
    result = {
        "bt": 612,
        "title": "Lower-shell orientation splitting theorem",
        "operator": "F3 = T B^3 T^T",
        "class_profiles": serial_profiles,
        "distance_class_counts": {d: dict(c) for d, c in distance_class_counts.items()},
        "interpretation": "The lower-shell non-radial residual is completely classified by ordered flag geometry. A1 splits by same-line versus same-point, A2 by forward versus backward cross-incidence, A3 by collinearity of source points, and A4 is unsplit/uniform at 28.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT612_LOWER_SHELL_ORIENTATION_SPLITTING_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
