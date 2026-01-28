#!/usr/bin/env python3
"""Construct an explicit root -> W33 edge bijection via Coxeter element.

Steps:
1) Build E8 roots and Coxeter element c.
2) Let w = c^5 (order 6). Orbits of w are 40 rays of size 6.
3) Build orbit adjacency graph using the orthogonality signature (0,0,36,0,0).
4) Build W33 graph from symplectic F3^4 projective points.
5) Find graph isomorphism orbit-graph -> W33 graph to align labels.
6) Test mapping root -> edge via (orbit(r), orbit(c^k r)) for k=1..5.
7) If a k yields a bijection onto all 240 W33 edges, export mapping.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from sage.all import Graph, RootSystem

ROOT = Path(__file__).resolve().parents[1]


def build_e8():
    RS = RootSystem(["E", 8])
    RL = RS.root_lattice()
    roots = list(RL.roots())  # 240 roots
    W = RL.weyl_group()
    C = RS.cartan_matrix()
    return RS, RL, roots, W, C


def vector_key(r):
    return tuple(int(x) for x in r.to_vector())


def orbits_under(w, roots):
    seen = set()
    orbits = []
    for r in roots:
        k = vector_key(r)
        if k in seen:
            continue
        orbit = []
        cur = r
        while True:
            ck = vector_key(cur)
            if ck in seen:
                break
            seen.add(ck)
            orbit.append(cur)
            cur = w.action(cur)
        orbits.append(orbit)
    return orbits


def orbit_pair_signatures(orbits, C):
    vals = [-2, -1, 0, 1, 2]
    signatures = {}
    n = len(orbits)
    for i in range(n):
        for j in range(i + 1, n):
            counts = Counter()
            for r in orbits[i]:
                vr = r.to_vector()
                for s in orbits[j]:
                    vs = s.to_vector()
                    ip = vr * C * vs
                    counts[ip] += 1
            sig = tuple(int(counts.get(v, 0)) for v in vals)
            signatures.setdefault(sig, []).append((i, j))
    return signatures


def build_orbit_graph(orbits, C):
    signatures = orbit_pair_signatures(orbits, C)
    # Use orthogonality signature (all 36 inner products are 0)
    sig = (0, 0, 36, 0, 0)
    pairs = signatures.get(sig, [])
    n = len(orbits)
    G = Graph()
    G.add_vertices(list(range(n)))
    G.add_edges(pairs)
    return G, sig, pairs


def build_w33_graph():
    # Construct W33 from F3^4 with symplectic form
    F3 = [0, 1, 2]
    vectors = [
        v
        for v in __import__("itertools").product(F3, repeat=4)
        if any(x != 0 for x in v)
    ]
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
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    G = Graph()
    G.add_vertices(list(range(n)))
    G.add_edges(edges)
    return G, proj_points, edges


def find_isomorphism(G_orbit, G_w33):
    iso = G_orbit.is_isomorphic(G_w33, certificate=True)
    if not iso[0]:
        raise RuntimeError("Orbit graph is not isomorphic to W33 graph")
    mapping = iso[1]  # dict: orbit vertex -> w33 vertex
    return mapping


def edge_set(edges):
    return {tuple(sorted(e)) for e in edges}


def main():
    RS, RL, roots, W, C = build_e8()
    print(f"E8 roots: {len(roots)}")

    simples = W.simple_reflections()
    coxeter = None
    for i in range(1, 9):
        coxeter = simples[i] if coxeter is None else coxeter * simples[i]

    w = coxeter**5
    print(f"w order: {w.order()}")

    orbits = orbits_under(w, roots)
    sizes = Counter(len(o) for o in orbits)
    print(f"Orbit sizes: {sizes}")

    G_orbit, sig, orbit_pairs = build_orbit_graph(orbits, C)
    print(f"Orbit graph edges: {len(orbit_pairs)} signature={sig}")

    G_w33, proj_points, w33_edges = build_w33_graph()
    print(f"W33 edges: {len(w33_edges)}")

    mapping = find_isomorphism(G_orbit, G_w33)
    print("Isomorphism found.")

    # Inverse map for convenience
    inv_mapping = {v: k for k, v in mapping.items()}

    # Root -> orbit index
    orbit_idx = {}
    for oi, orb in enumerate(orbits):
        for r in orb:
            orbit_idx[vector_key(r)] = oi

    # Try mappings r -> (orbit(r), orbit(c^k r)) for k=1..5
    w33_edge_set = edge_set(w33_edges)

    chosen_k = None
    root_to_edge = {}

    for k in range(1, 6):
        used_edges = {}
        ok = True
        for r in roots:
            rk = vector_key(r)
            okr = orbit_idx[rk]
            cr = (coxeter**k).action(r)
            okc = orbit_idx[vector_key(cr)]
            e_orbit = tuple(sorted((okr, okc)))
            # Map orbit vertices -> W33 vertices
            e_w33 = tuple(sorted((mapping[e_orbit[0]], mapping[e_orbit[1]])))
            if e_w33 not in w33_edge_set:
                ok = False
                break
            # Check injectivity
            if e_w33 in used_edges:
                ok = False
                break
            used_edges[e_w33] = rk
        if ok and len(used_edges) == 240:
            chosen_k = k
            root_to_edge = used_edges
            print(f"Found bijection with k={k}")
            break
        else:
            print(f"k={k} failed: edges={len(used_edges)}")

    if chosen_k is None:
        print("No bijection found for k=1..5.")

    # Random search for a single group element g with bijection property
    print(
        "Searching for g in W(E8) such that r -> (orbit(r), orbit(g r)) is bijective..."
    )
    candidate_g = None
    if chosen_k is None:
        for t in range(300):
            g = W.random_element()
            used_edges = {}
            ok = True
            for r in roots:
                rk = vector_key(r)
                okr = orbit_idx[rk]
                gr = g.action(r)
                okg = orbit_idx[vector_key(gr)]
                e_orbit = tuple(sorted((okr, okg)))
                e_w33 = tuple(sorted((mapping[e_orbit[0]], mapping[e_orbit[1]])))
                if e_w33 not in w33_edge_set:
                    ok = False
                    break
                if e_w33 in used_edges:
                    ok = False
                    break
                used_edges[e_w33] = rk
            if ok and len(used_edges) == 240:
                candidate_g = g
                root_to_edge = used_edges
                print(f"Found bijection with random g at try {t}")
                break

        if candidate_g is None:
            print("No explicit root->edge bijection found.")

    # If no structured mapping found, build a deterministic bipartite matching
    # between roots and incident edges (root in orbit A or B).
    def hopcroft_karp(left_adj, n_left, n_right):
        INF = 10**9
        pair_u = [-1] * n_left
        pair_v = [-1] * n_right
        dist = [0] * n_left

        from collections import deque

        def bfs():
            q = deque()
            for u in range(n_left):
                if pair_u[u] == -1:
                    dist[u] = 0
                    q.append(u)
                else:
                    dist[u] = INF
            d_augment = INF
            while q:
                u = q.popleft()
                if dist[u] < d_augment:
                    for v in left_adj[u]:
                        if pair_v[v] == -1:
                            d_augment = dist[u] + 1
                        else:
                            if dist[pair_v[v]] == INF:
                                dist[pair_v[v]] = dist[u] + 1
                                q.append(pair_v[v])
            return d_augment != INF

        def dfs(u):
            for v in left_adj[u]:
                if pair_v[v] == -1 or (
                    dist[pair_v[v]] == dist[u] + 1 and dfs(pair_v[v])
                ):
                    pair_u[u] = v
                    pair_v[v] = u
                    return True
            dist[u] = INF
            return False

        matching = 0
        while bfs():
            for u in range(n_left):
                if pair_u[u] == -1:
                    if dfs(u):
                        matching += 1
        return matching, pair_u, pair_v

    if chosen_k is None and candidate_g is None:
        # Build edges between orbits (undirected)
        orbit_edges = sorted(tuple(sorted(e)) for e in orbit_pairs)
        edge_index = {e: idx for idx, e in enumerate(orbit_edges)}

        # Left nodes: roots; Right nodes: edges
        left_adj = [[] for _ in range(len(roots))]
        for ri, r in enumerate(roots):
            oi = orbit_idx[vector_key(r)]
            # edges incident to orbit oi
            for e in orbit_edges:
                if e[0] == oi or e[1] == oi:
                    left_adj[ri].append(edge_index[e])

        matching, pair_u, pair_v = hopcroft_karp(left_adj, len(roots), len(orbit_edges))
        print(f"Hopcroft-Karp matching size: {matching}")
        if matching != 240:
            print("Matching failed; no bijection found.")
            return

        root_to_edge = {}
        for ri, ej in enumerate(pair_u):
            e_orbit = orbit_edges[ej]
            e_w33 = tuple(sorted((mapping[e_orbit[0]], mapping[e_orbit[1]])))
            root_to_edge[e_w33] = vector_key(roots[ri])

        mapping_mode = "hopcroft_karp_incident"
        chosen_k = None
        candidate_g = None

    else:
        # Prefer random-g mapping if found; otherwise use chosen_k
        mapping_mode = "coxeter_power" if chosen_k is not None else "random_g"

        if mapping_mode == "coxeter_power":
            used_edges = {}
            for r in roots:
                rk = vector_key(r)
                okr = orbit_idx[rk]
                cr = (coxeter**chosen_k).action(r)
                okc = orbit_idx[vector_key(cr)]
                e_orbit = tuple(sorted((okr, okc)))
                e_w33 = tuple(sorted((mapping[e_orbit[0]], mapping[e_orbit[1]])))
                used_edges[e_w33] = rk
            root_to_edge = used_edges

    # Build output mapping: root vector -> W33 edge (u,v)
    out = {
        "mapping_mode": mapping_mode,
        "coxeter_power_for_edge": int(chosen_k) if chosen_k is not None else None,
        "random_g_word": (
            candidate_g.reduced_word() if candidate_g is not None else None
        ),
        "orbit_signature": list(sig),
        "orbit_to_w33_vertex": {int(k): int(v) for k, v in mapping.items()},
        "w33_vertices": proj_points,
        "root_to_edge": {
            str(list(rv)): [int(e[0]), int(e[1])] for e, rv in root_to_edge.items()
        },
    }

    out_path = ROOT / "artifacts" / "e8_root_to_w33_edge.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
