#!/usr/bin/env python3
"""Search for an order-6 element in W(E8) whose orbits on roots give 40 rays.

If found, test whether the 40 orbits define a 40-vertex graph with SRG(40,12,2,4)
when we connect two orbits if they contain orthogonal roots (inner product 0).
"""

from __future__ import annotations

import random
from collections import Counter

from sage.all import RootSystem


def build_e8():
    RS = RootSystem(["E", 8])
    RL = RS.root_lattice()
    roots = list(RL.roots())  # 240 roots
    W = RL.weyl_group()
    C = RS.cartan_matrix()
    return RL, roots, W, C


def vector_key(r):
    # Use tuple of coefficients in simple root basis
    return tuple(r.to_vector())


def orbits_under(w, roots):
    seen = set()
    orbits = []
    root_map = {vector_key(r): r for r in roots}

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


def orbit_sizes(orbits):
    return Counter(len(o) for o in orbits)


def has_fixed_root(w, roots):
    for r in roots:
        if w.action(r) == r:
            return True
    return False


def orbit_graph(orbits, C):
    # adjacency if any pair between orbits is orthogonal
    n = len(orbits)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            ortho = False
            for r in orbits[i]:
                for s in orbits[j]:
                    v = r.to_vector()
                    w = s.to_vector()
                    ip = v * C * w
                    if ip == 0:
                        ortho = True
                        break
                if ortho:
                    break
            if ortho:
                adj[i][j] = adj[j][i] = 1
    return adj


def srg_params(adj):
    n = len(adj)
    degrees = [sum(row) for row in adj]
    if len(set(degrees)) != 1:
        return None
    k = degrees[0]
    # compute lambda and mu from first pair
    # lambda for adjacent, mu for non-adjacent
    lam = None
    mu = None
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(1 for t in range(n) if adj[i][t] and adj[j][t])
            if adj[i][j]:
                lam = common
            else:
                mu = common
            if lam is not None and mu is not None:
                return (n, k, lam, mu)
    return None


def orbit_pair_signatures(orbits, C):
    # For each pair of orbits, compute counts of inner products
    # using the Cartan-based inner product.
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
            sig = tuple(counts.get(v, 0) for v in vals)
            signatures.setdefault(sig, []).append((i, j))
    return signatures


def graph_from_signature(n, pairs):
    adj = [[0] * n for _ in range(n)]
    for i, j in pairs:
        adj[i][j] = adj[j][i] = 1
    return adj


def test_candidate(name, w, roots, C):
    order = w.order()
    print(f"Testing {name}: order={order}")
    if order != 6:
        return False
    if has_fixed_root(w, roots):
        print("  Has fixed roots; skipping.")
        return False
    orbits = orbits_under(w, roots)
    sizes = orbit_sizes(orbits)
    print(f"  Orbit sizes: {sizes}")
    if sizes == Counter({6: 40}):
        print("  Found 40 orbits of size 6!")
        adj = orbit_graph(orbits, C)
        params = srg_params(adj)
        print(f"  Orbit graph SRG params: {params}")
        degs = Counter(sum(row) for row in adj)
        print(f"  Degree distribution: {degs}")
        # Analyze pair signatures to see if any yields SRG(40,12,2,4)
        signatures = orbit_pair_signatures(orbits, C)
        print(f"  Distinct pair signatures: {len(signatures)}")
        n = len(orbits)
        result = None
        for sig, pairs in signatures.items():
            adj_sig = graph_from_signature(n, pairs)
            params_sig = srg_params(adj_sig)
            if params_sig is not None and params_sig[1] == 12:
                print(
                    f"  Candidate signature {sig} -> SRG params {params_sig} with {len(pairs)} edges"
                )
                result = {
                    "name": name,
                    "signature": sig,
                    "params": params_sig,
                    "pairs": pairs,
                    "orbits": orbits,
                }
        if result is not None:
            return result
        return True
    return False


def main():
    RL, roots, W, C = build_e8()
    print(f"E8 roots: {len(roots)}")
    print(f"W(E8) order: {W.order()}")

    # Build a Coxeter element and test its 5th power (order 6)
    simples = W.simple_reflections()
    # Deterministic order of simple reflections 1..8
    coxeter = None
    for i in range(1, 9):
        coxeter = simples[i] if coxeter is None else coxeter * simples[i]

    cand = coxeter**5  # should have order 6
    res = test_candidate("coxeter^5", cand, roots, C)
    if isinstance(res, dict):
        # Persist results
        import json
        from pathlib import Path

        out = {
            "element": res["name"],
            "signature": [int(x) for x in res["signature"]],
            "srg_params": [int(x) for x in res["params"]],
            "orbit_count": len(res["orbits"]),
            "orbit_size": len(res["orbits"][0]),
            "edges": [[int(i), int(j)] for i, j in res["pairs"]],
            "orbits": [
                [[int(x) for x in r.to_vector()] for r in orb] for orb in res["orbits"]
            ],
        }
        out_path = Path("artifacts/e8_coxeter6_orbits.json")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"Wrote {out_path}")
        return
    if res is True:
        return

    # Try random conjugates of coxeter^5
    max_conj = 200
    for t in range(max_conj):
        g = W.random_element()
        w = g * cand * ~g
        res = test_candidate(f"conjugate {t}", w, roots, C)
        if isinstance(res, dict):
            return
        if res is True:
            return

    # Fallback: random elements of order 6
    max_rand = 200
    for t in range(max_rand):
        w = W.random_element()
        res = test_candidate(f"random {t}", w, roots, C)
        if isinstance(res, dict):
            return
        if res is True:
            return

    print("No suitable element found in search.")


if __name__ == "__main__":
    main()
