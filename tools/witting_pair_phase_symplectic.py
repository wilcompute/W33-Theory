#!/usr/bin/env python3
"""Search for pairwise phase laws in F3^4 coordinates.

We use the explicit ray->F3 mapping (graph isomorphism) and test whether
pairwise Pancharatnam phases admit simple algebraic forms over GF(3).
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
    for u2, v2 in mapping.items():
        if (u2 in adj_r[u]) != (v2 in adj_f[v]):
            return False
    return True


def backtrack(order, candidates, mapping, used, adj_r, adj_f):
    if len(mapping) == len(order):
        return mapping
    u = min((u for u in order if u not in mapping), key=lambda x: len(candidates[x]))
    for v in list(candidates[u]):
        if v in used:
            continue
        if not is_compatible(u, v, mapping, adj_r, adj_f):
            continue
        mapping[u] = v
        used.add(v)
        updated = []
        failed = False
        for u2 in order:
            if u2 in mapping:
                continue
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
        for u2, old in updated:
            candidates[u2] = old
        used.remove(v)
        del mapping[u]
    return None


def find_graph_isomorphism(rays, points):
    adj_r = build_adjacency_rays(rays)
    adj_f = build_adjacency_f3(points)
    n = len(rays)
    candidates = {u: set(range(n)) for u in range(n)}
    mapping = {0: 0}
    used = {0}
    for u in range(1, n):
        candidates[u] = {v for v in candidates[u] if (u in adj_r[0]) == (v in adj_f[0])}
    order = list(range(n))
    return backtrack(order, candidates, mapping, used, adj_r, adj_f)


# ------------------ algebra over GF(3) ------------------


def gauss_solve_mod3(A, b):
    """Solve A x = b over GF(3). Returns one solution or None."""
    A = A.copy() % 3
    b = b.copy() % 3
    m, n = A.shape
    row = 0
    pivots = [-1] * n
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if A[r, col] % 3 != 0:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            A[[row, pivot]] = A[[pivot, row]]
            b[[row, pivot]] = b[[pivot, row]]
        inv = 1 if A[row, col] == 1 else 2
        A[row] = (A[row] * inv) % 3
        b[row] = (b[row] * inv) % 3
        for r in range(m):
            if r == row:
                continue
            if A[r, col] % 3 != 0:
                factor = A[r, col] % 3
                A[r] = (A[r] - factor * A[row]) % 3
                b[r] = (b[r] - factor * b[row]) % 3
        pivots[col] = row
        row += 1
        if row == m:
            break
    for r in range(m):
        if np.all(A[r] % 3 == 0) and b[r] % 3 != 0:
            return None
    x = np.zeros(n, dtype=int)
    for col, r in enumerate(pivots):
        if r != -1:
            x[col] = b[r] % 3
    return x


def phase_to_k(angle):
    """Quantize angle to k in Z12 where angle ~= k*pi/6."""
    k = int(np.rint(angle / (np.pi / 6.0))) % 12
    return k


def main():
    print("PAIR-PHASE LAW SEARCH (F3^4)")
    print("=" * 60)
    rays = construct_witting_40_rays()
    points = construct_f3_points()
    mapping = find_graph_isomorphism(rays, points)
    if mapping is None:
        print("No graph isomorphism found.")
        return
    ray_to_f3 = {r: points[mapping[r]] for r in range(40)}

    pairs = []
    for i in range(40):
        for j in range(i + 1, 40):
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                continue
            angle = np.angle(ip)
            k = phase_to_k(angle)
            pairs.append((i, j, k))

    print(f"Non-orth pairs: {len(pairs)}")

    by_omega = {1: [], 2: []}
    for i, j, k in pairs:
        w = omega_symp(ray_to_f3[i], ray_to_f3[j])
        if w in by_omega:
            by_omega[w].append(k)

    print("Phase k (mod 12) distribution by omega:")
    for w in [1, 2]:
        counts = {}
        for k in by_omega[w]:
            counts[k] = counts.get(k, 0) + 1
        print(f"  omega={w}: {dict(sorted(counts.items()))}")

    X = []
    y = []
    for i, j, k in pairs:
        xi = ray_to_f3[i]
        xj = ray_to_f3[j]
        feats = []
        for a in range(4):
            for b in range(4):
                feats.append((xi[a] * xj[b]) % 3)
        for a in range(4):
            feats.append(xi[a] % 3)
        for b in range(4):
            feats.append(xj[b] % 3)
        feats.append(1)
        X.append(feats)
        y.append(k % 3)
    X = np.array(X, dtype=int)
    y = np.array(y, dtype=int)
    sol = gauss_solve_mod3(X, y)
    if sol is None:
        print("No bilinear+linear fit for k mod 3.")
        fit = False
    else:
        fit = True
        preds = (X @ sol) % 3
        ok = int(np.sum(preds == y))
        print(f"Bilinear+linear fit for k mod 3: {ok}/{len(y)} correct")
        if ok == len(y):
            print("Exact mod-3 fit found.")

    # attempt full quadratic fit in 8 vars (x0..x3,y0..y3) for k mod 3
    Z = []
    z = []
    for i, j, k in pairs:
        xi = ray_to_f3[i]
        xj = ray_to_f3[j]
        v = list(xi) + list(xj)  # 8 variables
        feats = []
        # linear terms
        feats.extend([val % 3 for val in v])
        # square terms
        feats.extend([(val * val) % 3 for val in v])
        # cross terms
        for a in range(8):
            for b in range(a + 1, 8):
                feats.append((v[a] * v[b]) % 3)
        # constant
        feats.append(1)
        Z.append(feats)
        z.append(k % 3)
    Z = np.array(Z, dtype=int)
    z = np.array(z, dtype=int)
    sol2 = gauss_solve_mod3(Z, z)
    if sol2 is None:
        print("No quadratic fit for k mod 3.")
        quad_fit = False
    else:
        quad_fit = True
        preds = (Z @ sol2) % 3
        ok = int(np.sum(preds == z))
        print(f"Quadratic fit for k mod 3: {ok}/{len(z)} correct")
        if ok == len(z):
            print("Exact quadratic mod-3 fit found.")

    out = {
        "non_orth_pairs": len(pairs),
        "omega_distribution": {
            str(w): {str(k): by_omega[w].count(k) for k in sorted(set(by_omega[w]))}
            for w in [1, 2]
        },
        "mod3_fit": bool(fit),
        "mod3_quadratic_fit": bool(quad_fit),
    }
    out_path = ROOT / "artifacts" / "witting_pair_phase_symplectic.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
