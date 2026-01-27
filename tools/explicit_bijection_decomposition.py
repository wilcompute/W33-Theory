#!/usr/bin/env python3
"""Explicit W33 edge -> E8 root bijection using E6×SU(3) decomposition.

We use:
- E8 roots split by dot pairs with u1,u2 into: 72 + 6 + 27×6
- W33 edges split via vertex-0 decomposition into 108 (H27) + 108 (cross) + 12 + 12
- A deterministic assignment of edge subsets to root classes

This yields a fully explicit bijection (not group-equivariant), but
preserves the E6×SU(3) structural decomposition.
"""
from __future__ import annotations

import json
from itertools import product, combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------- W33 construction ----------------

def construct_w33_points():
    F3 = [0, 1, 2]
    points = []
    seen = set()
    for v in product(F3, repeat=4):
        if all(x == 0 for x in v):
            continue
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            points.append(v)
    return points


def omega(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def construct_w33_edges(points):
    edges = []
    adj = [[0]*40 for _ in range(40)]
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(points[i], points[j]) == 0:
                edges.append((i, j))
                adj[i][j] = adj[j][i] = 1
    return edges, adj

# ---------------- E8 roots and decomposition ----------------

def build_e8_roots_scaled():
    roots = []
    # type 1
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in (2, -2):
                for s2 in (2, -2):
                    r = [0] * 8
                    r[i] = s1
                    r[j] = s2
                    roots.append(tuple(r))
    # type 2
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(signs))
    return roots


def dot(a, b):
    return sum(a[i] * b[i] for i in range(8))


def classify_roots_by_dot(roots):
    u1 = (1,1,1,1,1,1,1,1)
    u2 = (1,1,1,1,1,1,-1,-1)
    classes = {}
    for i, r in enumerate(roots):
        d = (dot(r, u1), dot(r, u2))
        classes.setdefault(d, []).append(i)
    return classes

# ---------------- Bijection construction ----------------

def main():
    points = construct_w33_points()
    edges, adj = construct_w33_edges(points)

    # edge decomposition relative to v0=0
    v0 = 0
    H12 = [j for j in range(40) if adj[v0][j] == 1]
    H27 = [j for j in range(40) if j != v0 and adj[v0][j] == 0]

    edges_set = {tuple(sorted(e)) for e in edges}

    # triangles among H12
    triangles = []
    for a, b, c in combinations(H12, 3):
        if adj[a][b] and adj[a][c] and adj[b][c]:
            triangles.append(tuple(sorted((a, b, c))))
    triangles = sorted(set(triangles))

    # edge categories
    edges_incident = sorted([e for e in edges if v0 in e])  # 12
    edges_h12 = sorted([e for e in edges if e[0] in H12 and e[1] in H12])  # 12
    edges_h27 = sorted([e for e in edges if e[0] in H27 and e[1] in H27])  # 108

    # cross edges by triangle
    cross_by_tri = []
    for t in triangles:
        tset = set(t)
        cross = []
        for e in edges:
            i, j = e
            if (i in tset and j in H27) or (j in tset and i in H27):
                cross.append(tuple(sorted(e)))
        cross_by_tri.append(sorted(set(cross)))

    # sanity counts
    assert len(edges_incident) == 12
    assert len(edges_h12) == 12
    assert len(edges_h27) == 108
    assert len(cross_by_tri) == 4 and all(len(c) == 27 for c in cross_by_tri)

    # E8 roots decomposition by dot pairs
    roots = build_e8_roots_scaled()
    classes = classify_roots_by_dot(roots)

    # dot-pair classes of size 27 and 1
    class27_keys = [k for k, v in classes.items() if len(v) == 27]
    class1_keys = [k for k, v in classes.items() if len(v) == 1]
    class72_keys = [k for k, v in classes.items() if len(v) == 72]

    # deterministic ordering
    class27_keys = sorted(class27_keys)
    class1_keys = sorted(class1_keys)
    class72_key = class72_keys[0]

    # build ordered root lists
    class27_lists = [sorted(classes[k]) for k in class27_keys]
    class1_list = [classes[k][0] for k in class1_keys]  # 6 roots
    class72_list = sorted(classes[class72_key])  # 72 roots

    # Edge-to-root mapping strategy:
    # - Map H27 edges (108) to first 4 of the 27-classes (4*27)
    # - Map cross edges from first 2 triangles (54) to last 2 of the 27-classes
    # - Remaining edges (78) to 72 E6 roots + 6 SU3 roots

    mapping = {}

    # H27 edges -> first 4 classes
    h27_edges = edges_h27
    for idx in range(4):
        edge_chunk = h27_edges[idx*27:(idx+1)*27]
        root_chunk = class27_lists[idx]
        for e, r_idx in zip(edge_chunk, root_chunk):
            mapping[e] = r_idx

    # Cross edges from first 2 triangles -> remaining 2 classes
    cross_edges_selected = cross_by_tri[0] + cross_by_tri[1]
    for idx in range(2):
        edge_chunk = cross_edges_selected[idx*27:(idx+1)*27]
        root_chunk = class27_lists[4 + idx]
        for e, r_idx in zip(edge_chunk, root_chunk):
            mapping[e] = r_idx

    # Remaining edges -> E6 roots (72) + SU3 roots (6)
    remaining_edges = [e for e in edges if e not in mapping]
    remaining_edges = sorted(remaining_edges)
    assert len(remaining_edges) == 78

    # First 6 edges -> SU3 roots
    for e, r_idx in zip(remaining_edges[:6], class1_list):
        mapping[e] = r_idx

    # Remaining 72 edges -> E6 roots
    for e, r_idx in zip(remaining_edges[6:], class72_list):
        mapping[e] = r_idx

    # Final sanity
    assert len(mapping) == 240
    assert len(set(mapping.values())) == 240

    # Build edge index mapping
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    edge_to_root_index = {edge_to_idx[e]: mapping[e] for e in mapping}

    out = {
        "edge_to_root_index": edge_to_root_index,
        "root_coords": [list(r) for r in roots],
        "class27_keys": class27_keys,
        "class1_keys": class1_keys,
        "class72_key": class72_key,
        "triangles": triangles,
    }

    out_path = ROOT / "artifacts" / "explicit_bijection_decomposition.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
