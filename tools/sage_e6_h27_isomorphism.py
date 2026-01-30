#!/usr/bin/env python3
"""Sage: test whether H27 is isomorphic to an E6 minuscule-weight graph.

Discovery-mode script:
1) Build W33 and H27 (non-neighbors of a base vertex).
2) Build E6 minuscule weights (27 weights).
3) Test multiple adjacency rules and check isomorphism to H27.
"""

from __future__ import annotations

import json
from pathlib import Path

# Sage imports
from sage.all import Graph, RootSystem, vector

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
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

    adj = [[0] * n for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
                edges.append((i, j))
    return proj_points, adj, edges


def build_h27(adj, base=0):
    n = len(adj)
    non_neighbors = [j for j in range(n) if j != base and adj[base][j] == 0]
    idx = {v: i for i, v in enumerate(non_neighbors)}

    edges = []
    for i, u in enumerate(non_neighbors):
        for j, v in enumerate(non_neighbors):
            if i < j and adj[u][v]:
                edges.append((i, j))
    G = Graph(edges)
    G.add_vertices(range(27))
    return non_neighbors, G


def e6_minuscule_weights():
    R = RootSystem(["E", 6])
    W = R.weight_lattice()
    WG = W.weyl_group()
    omega1 = W.fundamental_weights()[1]

    # Manual orbit (WG in this Sage build has no .orbit method)
    seen = {}
    queue = [omega1]
    seen[tuple(omega1.to_vector())] = omega1

    gens = WG.gens()
    while queue:
        w = queue.pop()
        for g in gens:
            w2 = g.action(w)
            key = tuple(w2.to_vector())
            if key not in seen:
                seen[key] = w2
                queue.append(w2)

    orbit = list(seen.values())
    ambient = [vector(w.to_vector()) for w in orbit]
    return orbit, ambient


def e6_root_vectors():
    R = RootSystem(["E", 6])
    root_lattice = R.root_lattice()
    roots = [vector(r.to_vector()) for r in root_lattice.roots()]
    return roots


def build_weight_graph(ambient_weights, rule):
    edges = []
    n = len(ambient_weights)
    for i in range(n):
        for j in range(i + 1, n):
            if rule(ambient_weights[i], ambient_weights[j]):
                edges.append((i, j))
    G = Graph(edges)
    G.add_vertices(range(n))
    return G


def main():
    proj_points, adj, _ = build_w33()
    _, G_h27 = build_h27(adj, base=0)

    h27_deg = sorted(set(G_h27.degree()))
    h27_edges = G_h27.num_edges()

    results = {"h27_degree_set": h27_deg, "h27_edges": h27_edges, "tests": []}

    weights, wvecs = e6_minuscule_weights()
    roots = e6_root_vectors()
    root_set = {tuple(r) for r in roots}

    # Compute all inner products to inspect spectrum of values
    ip_vals = set()
    for i in range(len(wvecs)):
        for j in range(i + 1, len(wvecs)):
            ip_vals.add(wvecs[i].dot_product(wvecs[j]))

    # Candidate rules
    def rule_root_diff(u, v):
        return tuple(u - v) in root_set

    # Try inner-product based adjacency for each distinct value
    def rule_ip(val):
        return lambda u, v: (u.dot_product(v) == val)

    tests = []
    tests.append(("diff_is_root", rule_root_diff))
    for val in sorted(ip_vals):
        tests.append((f"ip_eq_{val}", rule_ip(val)))

    # Build pair-type categories for combinatorial search
    pair_types = {}
    type_list = []
    for i in range(len(wvecs)):
        for j in range(i + 1, len(wvecs)):
            ip = wvecs[i].dot_product(wvecs[j])
            d = wvecs[i] - wvecs[j]
            dn = d.dot_product(d)
            key = (ip, dn)
            if key not in pair_types:
                pair_types[key] = []
                type_list.append(key)
            pair_types[key].append((i, j))

    for name, rule in tests:
        G = build_weight_graph(wvecs, rule)
        degs = sorted(set(G.degree()))
        edges = G.num_edges()
        iso = False
        if edges == h27_edges and degs == h27_deg:
            iso = G.is_isomorphic(G_h27)
        results["tests"].append(
            {
                "name": name,
                "degree_set": degs,
                "edges": edges,
                "isomorphic_to_h27": bool(iso),
            }
        )

    # Brute force over small subsets of pair types to match degree 8
    results["pair_types"] = {str(k): len(v) for k, v in pair_types.items()}
    results["pair_type_search"] = []

    # If too many types, skip search
    if len(type_list) <= 10:
        from itertools import combinations

        for r in range(1, len(type_list) + 1):
            for combo in combinations(type_list, r):
                edges = []
                for key in combo:
                    edges.extend(pair_types[key])
                G = Graph(edges)
                G.add_vertices(range(27))
                degs = sorted(set(G.degree()))
                if degs != h27_deg:
                    continue
                if G.num_edges() != h27_edges:
                    continue
                iso = G.is_isomorphic(G_h27)
                results["pair_type_search"].append(
                    {
                        "combo": [str(k) for k in combo],
                        "edges": G.num_edges(),
                        "degree_set": degs,
                        "isomorphic_to_h27": bool(iso),
                    }
                )
                if iso:
                    print("FOUND ISOMORPHIC COMBO:", combo)
                    raise SystemExit

    out = ROOT / "artifacts" / "sage_e6_h27_isomorphism.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("H27 degree set:", h27_deg)
    print("H27 edges:", h27_edges)
    print("Tested", len(tests), "rules")
    for t in results["tests"]:
        if t["isomorphic_to_h27"]:
            print("MATCH:", t)
    print("Wrote", out)


if __name__ == "__main__":
    main()
