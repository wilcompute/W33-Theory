#!/usr/bin/env python3
"""Find an explicit isomorphism between Witting ray orthogonality and W(3,3).

We construct:
  G_rays: 40 vertices, edges where <ri|rj> = 0.
  G_f3  : 40 vertices, points in PG(3,3) with symplectic orthogonality.
Then we solve graph isomorphism via backtracking with pruning.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def construct_f3_points():
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
    return proj_points


def omega_symp(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_adjacency_rays(rays, tol=1e-8):
    n = len(rays)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.vdot(rays[i], rays[j])) < tol:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def build_adjacency_f3(points):
    n = len(points)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega_symp(points[i], points[j]) == 0:
                adj[i].add(j)
                adj[j].add(i)
    return adj


def is_compatible(u, v, mapping, adj_r, adj_f):
    # adjacency must match for mapped vertices
    for u2, v2 in mapping.items():
        if (u2 in adj_r[u]) != (v2 in adj_f[v]):
            return False
    return True


def backtrack(order, candidates, mapping, used, adj_r, adj_f):
    if len(mapping) == len(order):
        return mapping
    # pick next vertex with smallest candidate set
    u = min((u for u in order if u not in mapping), key=lambda x: len(candidates[x]))
    for v in list(candidates[u]):
        if v in used:
            continue
        if not is_compatible(u, v, mapping, adj_r, adj_f):
            continue
        # assign
        mapping[u] = v
        used.add(v)

        # forward-checking: update candidates for neighbors/unmapped
        updated = []
        failed = False
        for u2 in order:
            if u2 in mapping:
                continue
            # filter candidates of u2 by adjacency compatibility with u
            new_cand = set()
            for v2 in candidates[u2]:
                if v2 in used:
                    continue
                if (u2 in adj_r[u]) == (v2 in adj_f[v]):
                    new_cand.add(v2)
            if not new_cand:
                failed = True
                break
            if new_cand != candidates[u2]:
                updated.append((u2, candidates[u2]))
                candidates[u2] = new_cand
        if not failed:
            result = backtrack(order, candidates, mapping, used, adj_r, adj_f)
            if result is not None:
                return result

        # undo
        for u2, old in updated:
            candidates[u2] = old
        used.remove(v)
        del mapping[u]
    return None


def main():
    rays = construct_witting_40_rays()
    f3_points = construct_f3_points()
    adj_r = build_adjacency_rays(rays)
    adj_f = build_adjacency_f3(f3_points)
    n = len(rays)

    # initial candidates: all f3 points
    candidates = {u: set(range(n)) for u in range(n)}

    # fix one vertex mapping to break symmetry
    mapping = {0: 0}
    used = {0}

    # update candidates based on fixed mapping
    for u in range(1, n):
        candidates[u] = {v for v in candidates[u] if (u in adj_r[0]) == (v in adj_f[0])}

    order = list(range(n))
    result = backtrack(order, candidates, mapping, used, adj_r, adj_f)

    if result is None:
        print("No isomorphism found.")
        return

    # verify
    ok = True
    for i in range(n):
        for j in range(i + 1, n):
            r_edge = j in adj_r[i]
            f_edge = result[j] in adj_f[result[i]]
            if r_edge != f_edge:
                ok = False
                break
        if not ok:
            break

    # neighbor-set signature for each mapped vertex
    nbr_sig = {}
    for u in range(n):
        mapped = result[u]
        nbr_sig[str(u)] = sorted(int(result[x]) for x in adj_r[u])

    out = {
        "found": ok,
        "mapping": {str(k): int(v) for k, v in result.items()},
        "neighbor_signature": nbr_sig,
    }

    out_path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_graph_isomorphism.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting Ray ↔ W(3,3) Graph Isomorphism\n\n")
        f.write(f"Found isomorphism: **{ok}**\n\n")
        if ok:
            f.write("## Mapping (ray index → F3^4 point index)\n\n")
            for k in sorted(result.keys()):
                f.write(f"{k} -> {result[k]}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
