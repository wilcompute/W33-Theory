#!/usr/bin/env python3
"""Local search over S6 permutations per line to enforce Gram equivariance.

We optimize mismatch count for adjacent-edge pairs across all 10 generators.
"""

from __future__ import annotations

import json
import random
from itertools import permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    adj = [[0] * 40 for _ in range(40)]
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))
                adj[i][j] = adj[j][i] = 1

    return proj_points, edges, adj


def extract_lines(adj, edges):
    lines = set()
    edge_to_line = {}
    for i, j in edges:
        common = [k for k in range(40) if adj[i][k] and adj[j][k]]
        line = tuple(sorted([i, j, common[0], common[1]]))
        lines.add(line)
        edge_to_line[(i, j)] = line
    lines = sorted(lines)
    line_index = {line: idx for idx, line in enumerate(lines)}
    edge_to_line_idx = {
        tuple(sorted(e)): line_index[edge_to_line[e]] for e in edge_to_line
    }
    return lines, line_index, edge_to_line_idx


def canonical_line_edge_order(line, points):
    ordered_pts = sorted(line, key=lambda idx: points[idx])
    edge_list = []
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = ordered_pts[i], ordered_pts[j]
            edge_list.append(tuple(sorted((a, b))))
    return edge_list


def canonical_orbit_order(orbit):
    roots = [tuple(r) for r in orbit]
    min_root = min(roots)
    min_idx = roots.index(min_root)
    seq = roots[min_idx:] + roots[:min_idx]
    rev = [seq[0]] + list(reversed(seq[1:]))
    return min(seq, rev)


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def check_symplectic(M):
    Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]]

    def mat_mult(A, B):
        n, k, m = len(A), len(B), len(B[0])
        result = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for l in range(k):
                    result[i][j] = (result[i][j] + A[i][l] * B[l][j]) % 3
        return result

    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    result = mat_mult(mat_mult(MT, Omega), M)
    return result == Omega


def apply_matrix(M, v):
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(result)


def matrix_to_vertex_perm(M, vertices):
    v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}
    perm = []
    for v in vertices:
        v_new = apply_matrix(M, v)
        perm.append(v_to_idx[v_new])
    return perm


def vertex_perm_to_edge_perm(vperm, edges):
    edge_to_idx = {frozenset(e): i for i, e in enumerate(edges)}
    perm = []
    for e in edges:
        i, j = e
        new_i, new_j = vperm[i], vperm[j]
        perm.append(edge_to_idx[frozenset([new_i, new_j])])
    return perm


def get_edge_generators(vertices, edges):
    gen_matrices = [
        [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 2, 1]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 2], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0]],
        [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 2]],
    ]
    edge_gens = []
    for M in gen_matrices:
        if not check_symplectic(M):
            continue
        vperm = matrix_to_vertex_perm(M, vertices)
        eperm = vertex_perm_to_edge_perm(vperm, edges)
        edge_gens.append(eperm)
    return edge_gens


def cartan_e8():
    return [
        [2, -1, 0, 0, 0, 0, 0, 0],
        [-1, 2, -1, 0, 0, 0, 0, 0],
        [0, -1, 2, -1, 0, 0, 0, -1],
        [0, 0, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, -1, 0, 0, 0, 0, 2],
    ]


def ip_e8(r, s, C):
    return sum(r[i] * C[i][j] * s[j] for i in range(8) for j in range(8))


def main():
    points, edges, adj = build_w33()
    lines, line_index, edge_to_line_idx = extract_lines(adj, edges)

    line_edge_order = {
        li: canonical_line_edge_order(lines[li], points) for li in range(len(lines))
    }

    orbit_data = json.loads(
        (ROOT / "artifacts" / "e8_coxeter6_orbits.json").read_text()
    )
    orbits = orbit_data["orbits"]
    orbit_root_order = {o: canonical_orbit_order(orbits[o]) for o in range(len(orbits))}

    summary = json.loads(
        (ROOT / "artifacts" / "edge_root_bijection_summary.json").read_text()
    )
    orbit_to_line = {int(k): v for k, v in summary["orbit_to_line"].items()}
    line_to_orbit = {v: k for k, v in orbit_to_line.items()}

    edge_gens = get_edge_generators(points, edges)

    edge_index = {tuple(sorted(e)): idx for idx, e in enumerate(edges)}
    edges_sorted = [tuple(sorted(e)) for e in edges]

    # adjacency pairs for scoring
    adj_pairs = []
    for i in range(len(edges_sorted)):
        e1 = edges_sorted[i]
        s1 = set(e1)
        for j in range(i + 1, len(edges_sorted)):
            if s1 & set(edges_sorted[j]):
                adj_pairs.append((i, j))

    # roots flattened by line, pos
    roots_flat = []
    for li in range(len(lines)):
        o = line_to_orbit[li]
        roots_flat.extend(orbit_root_order[o])
    root_list = [tuple(r) for r in roots_flat]

    C = cartan_e8()
    Gram = [[0] * len(root_list) for _ in range(len(root_list))]
    for i in range(len(root_list)):
        for j in range(len(root_list)):
            Gram[i][j] = ip_e8(root_list[i], root_list[j], C)

    # all S6 perms
    perms = list(permutations(range(6)))

    # precompute line edges idx
    line_edges_idx = {
        li: [edge_index[e] for e in line_edge_order[li]] for li in range(len(lines))
    }

    def build_edge_to_root_idx(line_perm_choice):
        edge_to_root_idx = [None] * len(edges_sorted)
        for li in range(len(lines)):
            perm = perms[line_perm_choice[li]]
            base = li * 6
            for p, e_idx in enumerate(line_edges_idx[li]):
                edge_to_root_idx[e_idx] = base + perm[p]
        return edge_to_root_idx

    def score(line_perm_choice):
        edge_to_root_idx = build_edge_to_root_idx(line_perm_choice)
        mism = 0
        for g in edge_gens:
            for i, j in adj_pairs:
                gi = g[i]
                gj = g[j]
                if (
                    Gram[edge_to_root_idx[i]][edge_to_root_idx[j]]
                    != Gram[edge_to_root_idx[gi]][edge_to_root_idx[gj]]
                ):
                    mism += 1
        return mism

    random.seed(0)
    best_score = None
    best_choice = None

    choice = [random.randrange(len(perms)) for _ in range(len(lines))]
    cur = score(choice)
    best_score = cur
    best_choice = choice[:]

    for it in range(200):
        li = random.randrange(len(lines))
        old = choice[li]
        choice[li] = random.randrange(len(perms))
        s = score(choice)
        if s < cur:
            cur = s
            if s < best_score:
                best_score = s
                best_choice = choice[:]
        else:
            choice[li] = old
        if it % 20 == 0:
            print("iter", it, "cur", cur, "best", best_score)

    out = {
        "best_mismatch_adjacent_pairs": best_score,
        "line_perm_choice": best_choice,
    }
    out_path = ROOT / "artifacts" / "equivariant_search_result_s6.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
