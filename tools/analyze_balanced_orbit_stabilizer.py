#!/usr/bin/env python3
"""Analyze the stabilizer and geometry of the balanced 27-edge orbit.

We avoid heavy group-theory libs by enumerating PSp(4,3) as permutations on 40
vertices, then measuring the orbit/stabilizer of the balanced 27-edge set.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from itertools import product
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

    n = len(proj_points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
                edges.append((i, j))

    return proj_points, adj, edges


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
                s = 0
                for l in range(k):
                    s = (s + A[i][l] * B[l][j]) % 3
                result[i][j] = s
        return result

    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    return mat_mult(mat_mult(MT, Omega), M) == Omega


def apply_matrix(M, v):
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(result)


def matrix_to_vertex_perm(M, vertices):
    v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}
    perm = []
    for v in vertices:
        v_new = apply_matrix(M, v)
        if v_new not in v_to_idx:
            return None
        perm.append(v_to_idx[v_new])
    return perm


def get_generators(vertices):
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

    perms = []
    for M in gen_matrices:
        if not check_symplectic(M):
            continue
        perm = matrix_to_vertex_perm(M, vertices)
        if perm and perm != list(range(40)):
            perms.append(perm)
    return perms


def compose(g, p):
    # (g ∘ p)(i) = g[p[i]]
    return [g[x] for x in p]


def enumerate_group(vertex_gens):
    identity = tuple(range(40))
    seen = {identity}
    queue = deque([identity])
    while queue:
        p = queue.popleft()
        for g in vertex_gens:
            new = tuple(compose(g, p))
            if new not in seen:
                seen.add(new)
                queue.append(new)
    return list(seen)


def edge_index_map(edges):
    return {tuple(sorted(e)): i for i, e in enumerate(edges)}


def map_edge_set(perm, edges, edge_to_idx, edge_set_pairs):
    mapped = []
    for i, j in edge_set_pairs:
        a, b = perm[i], perm[j]
        if a > b:
            a, b = b, a
        mapped.append(edge_to_idx[(a, b)])
    return frozenset(mapped)


def main():
    points, adj, edges = build_w33()
    edge_to_idx = edge_index_map(edges)

    # Load balanced orbit id
    bias = json.loads((ROOT / "artifacts" / "su3_phase_orbit_bias.json").read_text())
    balanced_orbit = None
    for k, v in bias["orbit_sums"].items():
        if v == {"0": 9, "1": 9, "2": 9} or v == {0: 9, 1: 9, 2: 9}:
            balanced_orbit = int(k.split("_")[1])
    if balanced_orbit is None:
        print("No balanced orbit found")
        return

    # Load root labels and edge->root map
    we6 = json.loads((ROOT / "artifacts" / "we6_orbit_labels.json").read_text())
    root_to_orbit = {eval(k): v for k, v in we6["mapping"].items()}
    edge_map = json.loads(
        (ROOT / "artifacts" / "explicit_bijection_decomposition.json").read_text()
    )
    edge_to_root_idx = {int(k): v for k, v in edge_map["edge_to_root_index"].items()}
    root_coords = [tuple(r) for r in edge_map["root_coords"]]

    # Balanced edge pairs
    balanced_edge_pairs = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info["orbit_size"] == 27 and info["orbit_id"] == balanced_orbit:
            balanced_edge_pairs.append(e)

    # Root type distribution inside balanced orbit (scaled coords)
    root_type_counts = Counter()
    for e in balanced_edge_pairs:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        has_odd = any(abs(x) % 2 == 1 for x in r)
        root_type_counts["half"] += 1 if has_odd else 0
        root_type_counts["integral"] += 0 if has_odd else 1

    # Axis vertices (support size 1)
    axis_vertices = [
        i for i, p in enumerate(points) if sum(1 for x in p if x != 0) == 1
    ]
    axis_incidence = Counter()
    for i, j in balanced_edge_pairs:
        if i in axis_vertices:
            axis_incidence[i] += 1
        if j in axis_vertices:
            axis_incidence[j] += 1

    # Group enumeration on vertices
    vertex_gens = get_generators(points)
    group = enumerate_group(vertex_gens)
    group_order = len(group)

    # Orbit of balanced edge set (setwise action)
    base_edge_set = frozenset(
        edge_to_idx[tuple(sorted(e))] for e in balanced_edge_pairs
    )
    orbit_sets = set()
    stabilizer_count = 0
    for perm in group:
        mapped = map_edge_set(perm, edges, edge_to_idx, balanced_edge_pairs)
        orbit_sets.add(mapped)
        if mapped == base_edge_set:
            stabilizer_count += 1

    orbit_size = len(orbit_sets)
    stabilizer_size = stabilizer_count

    # Induced action on the 27 edges for stabilizer elements
    # Build index map for the balanced set
    bal_list = sorted(base_edge_set)
    bal_pos = {eidx: k for k, eidx in enumerate(bal_list)}
    induced_orbits = []
    seen_bal = set()
    # Build generators for induced subgroup from stabilizer elements
    # (Not necessarily minimal; we use all stabilizer elements' actions)
    induced_perms = []
    for perm in group:
        mapped = map_edge_set(perm, edges, edge_to_idx, balanced_edge_pairs)
        if mapped != base_edge_set:
            continue
        # Induced permutation on the 27 edges
        perm_map = [None] * len(bal_list)
        for eidx in base_edge_set:
            a, b = edges[eidx]
            a2, b2 = perm[a], perm[b]
            if a2 > b2:
                a2, b2 = b2, a2
            eidx2 = edge_to_idx[(a2, b2)]
            perm_map[bal_pos[eidx]] = bal_pos[eidx2]
        induced_perms.append(tuple(perm_map))

    # Compute orbits on 27 edges under induced perms
    for i in range(len(bal_list)):
        if i in seen_bal:
            continue
        orbit = {i}
        frontier = [i]
        while frontier:
            cur = frontier.pop()
            for p in induced_perms:
                nxt = p[cur]
                if nxt not in orbit:
                    orbit.add(nxt)
                    frontier.append(nxt)
        for x in orbit:
            seen_bal.add(x)
        induced_orbits.append(sorted(orbit))

    results = {
        "balanced_orbit_id": balanced_orbit,
        "balanced_edge_count": len(balanced_edge_pairs),
        "group_order": group_order,
        "orbit_size_of_edge_set": orbit_size,
        "stabilizer_size": stabilizer_size,
        "root_type_counts": dict(root_type_counts),
        "axis_vertices": axis_vertices,
        "axis_incidence": {str(k): v for k, v in axis_incidence.items()},
        "induced_orbit_sizes_on_27_edges": sorted(
            [len(o) for o in induced_orbits], reverse=True
        ),
    }

    out_path = ROOT / "artifacts" / "balanced_orbit_stabilizer.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
