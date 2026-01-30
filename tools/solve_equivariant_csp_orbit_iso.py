#!/usr/bin/env python3
"""CSP: solve for per-line permutations given orbit Gram isomorphisms.

Fixed:
- line -> orbit mapping from edge_root_bijection_summary.json
- canonical edge order per line
- canonical root order per orbit

Variables:
- for each line L, choose permutation pi_L in Aut(G_orbit(L))

Constraints (for each generator g and line L):
  f = pi_{L'} o rho_{g,L} o pi_L^{-1} must be in Iso(orbit(L), orbit(L'))
"""

from __future__ import annotations

import json
from collections import deque
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

    # Precompute orbit Gram matrices and isomorphisms
    C = cartan_e8()
    perms = list(permutations(range(6)))

    def gram(orbit):
        G = [[0] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(6):
                G[i][j] = ip_e8(orbit[i], orbit[j], C)
        return G

    def is_iso(G1, G2, p):
        for i in range(6):
            for j in range(6):
                if G1[i][j] != G2[p[i]][p[j]]:
                    return False
        return True

    G_orb = [gram(orbit_root_order[o]) for o in range(40)]

    Iso = [[[] for _ in range(40)] for _ in range(40)]
    for a in range(40):
        for b in range(40):
            for p in perms:
                if is_iso(G_orb[a], G_orb[b], p):
                    Iso[a][b].append(p)

    # Allowed permutations per line (automorphisms of orbit Gram)
    domain = [Iso[line_to_orbit[li]][line_to_orbit[li]] for li in range(40)]

    # Generators and line action
    edge_gens = get_edge_generators(points, edges)
    edge_index = {tuple(sorted(e)): idx for idx, e in enumerate(edges)}
    edges_sorted = [tuple(sorted(e)) for e in edges]

    line_action = []
    for g in edge_gens:
        info = {}
        for li in range(40):
            edge_list = line_edge_order[li]
            mapped_edges = [edges_sorted[g[edge_index[e]]] for e in edge_list]
            li2 = edge_to_line_idx[mapped_edges[0]]
            edge_list2 = line_edge_order[li2]
            pos_map = [edge_list2.index(me) for me in mapped_edges]
            info[li] = (li2, pos_map)
        line_action.append(info)

    # CSP with AC-3
    def consistent_pair(li, lj, p, q, g_idx, pos_map):
        o = line_to_orbit[li]
        o2 = line_to_orbit[lj]
        # f = q o pos_map o p^{-1}
        p_inv = [0] * 6
        for i in range(6):
            p_inv[p[i]] = i
        f = [0] * 6
        for i in range(6):
            f[i] = q[pos_map[p_inv[i]]]
        return tuple(f) in Iso[o][o2]

    # Build constraints list
    constraints = []
    for g_idx, act in enumerate(line_action):
        for li in range(40):
            lj, pos_map = act[li]
            constraints.append((li, lj, g_idx, pos_map))

    # AC-3 pruning
    domains = [set(map(tuple, d)) for d in domain]
    queue = deque(constraints)
    while queue:
        li, lj, g_idx, pos_map = queue.popleft()
        removed = False
        to_remove = []
        for p in domains[li]:
            ok = False
            for q in domains[lj]:
                if consistent_pair(li, lj, p, q, g_idx, pos_map):
                    ok = True
                    break
            if not ok:
                to_remove.append(p)
        if to_remove:
            for p in to_remove:
                domains[li].remove(p)
            removed = True
        if removed:
            # add all constraints involving li
            for a, b, g2, pm in constraints:
                if b == li and a != lj:
                    queue.append((a, b, g2, pm))

    # If any domain empty, no solution
    if any(len(d) == 0 for d in domains):
        out = {"solution_found": False, "reason": "AC-3 pruned to empty"}
        (ROOT / "artifacts" / "equivariant_csp_orbit_iso.json").write_text(
            json.dumps(out, indent=2), encoding="utf-8"
        )
        print("No solution (AC-3) ")
        return

    # Backtracking
    assignment = [None] * 40
    order = sorted(range(40), key=lambda i: len(domains[i]))

    def backtrack(k=0):
        if k == 40:
            return True
        li = order[k]
        for p in domains[li]:
            assignment[li] = p
            ok = True
            # check constraints with already assigned neighbors
            for a, b, g_idx, pos_map in constraints:
                if a == li and assignment[b] is not None:
                    if not consistent_pair(
                        a, b, assignment[a], assignment[b], g_idx, pos_map
                    ):
                        ok = False
                        break
                if b == li and assignment[a] is not None:
                    if not consistent_pair(
                        a, b, assignment[a], assignment[b], g_idx, pos_map
                    ):
                        ok = False
                        break
            if ok and backtrack(k + 1):
                return True
            assignment[li] = None
        return False

    ok = backtrack(0)
    out = {
        "solution_found": ok,
    }
    (ROOT / "artifacts" / "equivariant_csp_orbit_iso.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Solution", ok)


if __name__ == "__main__":
    main()
