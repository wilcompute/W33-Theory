#!/usr/bin/env python3
"""Build explicit W33-edge -> E8-root mapping using W(E6) orbit labels.

Uses a deterministic, documented rule:
1) Compute W33 edges and H12/H27 decomposition around base vertex v0=0.
2) Identify 4 H12 triangles; take first two (lexicographic) as T0,T1.
3) Map:
   - H27-H27 edges (108) -> first four size-27 orbits (4*27)
   - Cross edges from T0,T1 to H27 (54) -> remaining two size-27 orbits (2*27)
   - Remaining 78 edges -> 72-orbit (first 72) + six size-1 roots (first 6)

Root ordering is canonical by root_key (2*coords integer tuple) lexicographic.
Edge ordering is lexicographic by (i,j).
"""
from __future__ import annotations

import json
from itertools import product, combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def construct_w33():
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
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    edges = []
    adj = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))
                adj[i][j] = adj[j][i] = 1
    return proj_points, edges, adj


def find_h12_triangles(adj, v0=0):
    n = len(adj)
    nbrs = [j for j in range(n) if adj[v0][j] == 1]
    tris = []
    for a, b, c in combinations(nbrs, 3):
        if adj[a][b] and adj[a][c] and adj[b][c]:
            tris.append(tuple(sorted((a, b, c))))
    tris = sorted(tris)
    return nbrs, tris


def edge_lists(edges, adj, v0=0):
    n = len(adj)
    nbrs = [j for j in range(n) if adj[v0][j] == 1]
    h27 = [j for j in range(n) if j != v0 and adj[v0][j] == 0]
    nbrs_set = set(nbrs)
    h27_set = set(h27)

    # Edge partitions
    h27_edges = []
    cross_edges = []
    h12_edges = []
    incident_edges = []

    for i, j in edges:
        if i == v0 or j == v0:
            incident_edges.append((i, j))
        elif i in h27_set and j in h27_set:
            h27_edges.append((i, j))
        elif (i in nbrs_set and j in nbrs_set):
            h12_edges.append((i, j))
        elif (i in nbrs_set and j in h27_set) or (j in nbrs_set and i in h27_set):
            cross_edges.append((i, j))

    return incident_edges, h12_edges, cross_edges, h27_edges


def load_orbit_labels(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    mapping = data["mapping"]
    # Build root list keyed by root_key
    roots = []
    for key_str, info in mapping.items():
        key = tuple(int(x) for x in key_str.strip('()').split(','))
        roots.append((key, info["orbit_id"], info["orbit_size"]))
    # Canonical order by key
    roots.sort(key=lambda x: x[0])
    return roots


def key_to_root(key):
    # key is 2*coords integer tuple
    return [k/2 for k in key]


def main():
    vertices, edges, adj = construct_w33()
    edges = sorted(edges)

    # Partition edges
    incident_edges, h12_edges, cross_edges, h27_edges = edge_lists(edges, adj, v0=0)

    # Triangles in H12
    nbrs, tris = find_h12_triangles(adj, v0=0)
    # Choose two triangles for 27-orbits
    tris = sorted(tris)
    triA, triB = tris[0], tris[1]
    tri_set = set(triA) | set(triB)

    # Cross edges from selected triangles to H27
    h27_set = set([j for j in range(40) if j != 0 and adj[0][j] == 0])
    cross_AB = [e for e in cross_edges if (e[0] in tri_set or e[1] in tri_set)]
    cross_rest = [e for e in cross_edges if e not in cross_AB]

    # Load orbit labels
    roots = load_orbit_labels(ROOT / "artifacts" / "we6_orbit_labels.json")

    # Partition roots by orbit size
    size1 = [r for r in roots if r[2] == 1]
    size27 = [r for r in roots if r[2] == 27]
    size72 = [r for r in roots if r[2] == 72]

    # Group size27 by orbit_id
    orbit27 = {}
    for key, oid, osize in size27:
        orbit27.setdefault(oid, []).append(key)
    # Canonical order of 27-orbits by min key
    orbit27_list = sorted(orbit27.values(), key=lambda keys: min(keys))
    # Sort keys inside each orbit
    orbit27_list = [sorted(keys) for keys in orbit27_list]

    # Sort size1 keys
    size1_keys = [k for k, _, _ in size1]
    size1_keys.sort()
    # Sort size72 keys
    size72_keys = [k for k, _, _ in size72]
    size72_keys.sort()

    # Sanity checks
    assert len(h27_edges) == 108
    assert len(cross_AB) == 54
    assert len(cross_rest) == 54
    assert len(h12_edges) == 12
    assert len(incident_edges) == 12
    assert len(orbit27_list) == 6
    assert all(len(o) == 27 for o in orbit27_list)
    assert len(size1_keys) == 6
    assert len(size72_keys) == 72

    # Map edges -> roots
    edge_to_root = {}

    # 1) H27 edges -> first 4 orbit27
    h27_edges_sorted = sorted(h27_edges)
    for i in range(4):
        chunk = h27_edges_sorted[i*27:(i+1)*27]
        keys = orbit27_list[i]
        for e, k in zip(chunk, keys):
            edge_to_root[e] = k

    # 2) Cross edges from triA,triB -> remaining 2 orbit27
    cross_AB_sorted = sorted(cross_AB)
    for i in range(2):
        chunk = cross_AB_sorted[i*27:(i+1)*27]
        keys = orbit27_list[4+i]
        for e, k in zip(chunk, keys):
            edge_to_root[e] = k

    # 3) Remaining edges -> size72 + size1
    remaining_edges = [e for e in edges if e not in edge_to_root]
    remaining_edges = sorted(remaining_edges)
    # First 6 -> size1 roots
    for e, k in zip(remaining_edges[:6], size1_keys):
        edge_to_root[e] = k
    # Next 72 -> size72 roots
    for e, k in zip(remaining_edges[6:6+72], size72_keys):
        edge_to_root[e] = k

    # Sanity
    assert len(edge_to_root) == 240

    # Build inverse
    root_to_edge = {str(k): e for e, k in edge_to_root.items()}

    # Save
    out_edges = {str(e): key_to_root(k) for e, k in edge_to_root.items()}
    out_roots = {str(k): list(edge) for k, edge in root_to_edge.items()}

    (ROOT / "artifacts").mkdir(parents=True, exist_ok=True)
    (ROOT / "artifacts" / "edge_to_e8_root_we6_orbits.json").write_text(
        json.dumps(out_edges, indent=2), encoding="utf-8"
    )
    (ROOT / "artifacts" / "e8_root_to_edge_we6_orbits.json").write_text(
        json.dumps(out_roots, indent=2), encoding="utf-8"
    )

    summary = {
        "triangles": tris,
        "selected_triangles": [triA, triB],
        "counts": {
            "h27_edges": len(h27_edges),
            "cross_AB": len(cross_AB),
            "cross_rest": len(cross_rest),
            "h12_edges": len(h12_edges),
            "incident_edges": len(incident_edges),
            "size27_orbits": len(orbit27_list),
            "size1_roots": len(size1_keys),
            "size72_roots": len(size72_keys),
        },
        "mapping": {
            "h27_edges_to_4x27": True,
            "cross_AB_to_2x27": True,
            "remaining_to_72plus6": True,
        },
    }
    (ROOT / "artifacts" / "edge_root_we6_orbit_mapping_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print("Wrote artifacts/edge_to_e8_root_we6_orbits.json")
    print("Wrote artifacts/e8_root_to_edge_we6_orbits.json")
    print("Wrote artifacts/edge_root_we6_orbit_mapping_summary.json")


if __name__ == "__main__":
    main()
