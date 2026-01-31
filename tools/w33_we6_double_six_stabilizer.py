#!/usr/bin/env python3
"""
Compute the W(E6) action on a Schläfli 27-orbit (27 lines on a cubic surface),
enumerate the 36 Schläfli double-sixes, and verify the stabilizer sizes.

This is a key structural backbone:
- W(E6) acts on the 27 lines with order 51840.
- There are exactly 36 double-sixes.
- The stabilizer of a (unordered) double-six has order 1440, hence index 36.

This matches the classical geometry and provides an explicit, computation-backed
symmetry-breaking hinge:
  W(E6) -> stabilizer(double-six)  (index 36).

No Sage/GAP required; pure Python + numpy.

Outputs:
- we6_double_six_stabilizer_summary.json
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent

E8_SIMPLE_ROOTS = np.array(
    [
        [1, -1, 0, 0, 0, 0, 0, 0],
        [0, 1, -1, 0, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 1, -1, 0, 0],
        [0, 0, 0, 0, 0, 1, -1, 0],
        [0, 0, 0, 0, 0, 1, 1, 0],
        [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5],
    ],
    dtype=float,
)
E6_SIMPLE_ROOTS = E8_SIMPLE_ROOTS[2:8]


def construct_e8_roots() -> np.ndarray:
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in [1.0, -1.0]:
                for sj in [1.0, -1.0]:
                    r = np.zeros(8)
                    r[i], r[j] = si, sj
                    roots.append(r)
    for bits in range(256):
        signs = np.array([1.0 if (bits >> k) & 1 else -1.0 for k in range(8)])
        if int(np.sum(signs < 0)) % 2 == 0:
            roots.append(signs * 0.5)
    return np.array(roots)


def snap(v: np.ndarray, tol: float = 1e-6):
    s = np.round(v * 2) / 2
    if np.max(np.abs(v - s)) < tol:
        return tuple(s.tolist())
    return tuple(np.round(v, 8).tolist())


def weyl_reflect(v: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    return v - 2 * np.dot(v, alpha) / np.dot(alpha, alpha) * alpha


def compute_we6_orbits(roots: np.ndarray):
    keys = [snap(r) for r in roots]
    key_to_idx = {k: i for i, k in enumerate(keys)}
    used = np.zeros(len(roots), dtype=bool)
    orbits = []
    for start in range(len(roots)):
        if used[start]:
            continue
        orbit = [start]
        used[start] = True
        frontier = [start]
        while frontier:
            cur = frontier.pop()
            v = roots[cur]
            for alpha in E6_SIMPLE_ROOTS:
                w = weyl_reflect(v, alpha)
                j = key_to_idx[snap(w)]
                if not used[j]:
                    used[j] = True
                    orbit.append(j)
                    frontier.append(j)
        orbits.append(orbit)
    return orbits


def build_schlafli_adj(roots: np.ndarray, orbit_idx):
    R = roots[orbit_idx]
    gram = R @ R.T
    adj = np.zeros((len(orbit_idx), len(orbit_idx)), dtype=np.uint8)
    ip_counts = Counter()
    for i in range(len(orbit_idx)):
        for j in range(i + 1, len(orbit_idx)):
            ip = float(gram[i, j])
            ip_counts[round(ip, 6)] += 1
            if abs(ip - 1.0) < 1e-6:
                adj[i, j] = adj[j, i] = 1
    deg = adj.sum(axis=1)
    if not np.all(deg == 16):
        raise RuntimeError(f"Unexpected Schläfli degrees: {Counter(deg.tolist())}")
    return adj, {str(k): int(v) for k, v in sorted(ip_counts.items())}


def perm_compose(p, q):
    return tuple(p[i] for i in q)


def perm_inv(p):
    inv = [0] * len(p)
    for i, j in enumerate(p):
        inv[j] = i
    return tuple(inv)


def close_group(gens):
    idp = tuple(range(len(gens[0])))
    seen = {idp}
    dq = deque([idp])
    all_gens = list(gens) + [perm_inv(g) for g in gens]
    while dq:
        cur = dq.popleft()
        for g in all_gens:
            nxt = perm_compose(g, cur)
            if nxt not in seen:
                seen.add(nxt)
                dq.append(nxt)
    return list(seen)


def find_k6_cliques(adj):
    n = adj.shape[0]
    nbr = [set(np.where(adj[i] == 1)[0]) for i in range(n)]
    out = set()

    def extend(clique, candidates):
        if len(clique) == 6:
            out.add(tuple(sorted(clique)))
            return
        if len(clique) + len(candidates) < 6:
            return
        for v in sorted(list(candidates)):
            new_cand = candidates.intersection(nbr[v])
            candidates.remove(v)
            extend(clique + [v], new_cand)

    extend([], set(range(n)))
    return sorted(out)


def is_double_six(adj, A, B):
    # Schläfli graph edges = skewness.
    # In a double-six, each ai is skew to exactly one bj, and vice versa.
    if set(A) & set(B):
        return None
    pairing = {}
    used_b = set()
    for a in A:
        nbrs = [b for b in B if adj[a, b] == 1]
        if len(nbrs) != 1:
            return None
        b = nbrs[0]
        if b in used_b:
            return None
        pairing[int(a)] = int(b)
        used_b.add(b)
    for b in B:
        nbrs = [a for a in A if adj[a, b] == 1]
        if len(nbrs) != 1:
            return None
    return pairing


def main():
    roots = construct_e8_roots()
    orbits = compute_we6_orbits(roots)
    orbits27 = [o for o in orbits if len(o) == 27]
    if not orbits27:
        raise RuntimeError("No 27-orbits found")
    orbit = orbits27[0]
    orb_map = {idx: i for i, idx in enumerate(orbit)}

    # Generators: simple reflections restricted to the 27-orbit
    keys = [snap(r) for r in roots]
    key_to_idx = {k: i for i, k in enumerate(keys)}
    gens = []
    for alpha in E6_SIMPLE_ROOTS:
        perm = [None] * 27
        for idx in orbit:
            i = orb_map[idx]
            w = weyl_reflect(roots[idx], alpha)
            j = key_to_idx[snap(w)]
            perm[i] = orb_map[j]
        gens.append(tuple(perm))

    G = close_group(gens)

    adj, ip_counts = build_schlafli_adj(roots, orbit)

    k6 = find_k6_cliques(adj)

    ds = []
    for i in range(len(k6)):
        for j in range(i + 1, len(k6)):
            A = k6[i]
            B = k6[j]
            pairing = is_double_six(adj, A, B)
            if pairing is not None:
                ds.append((A, B, pairing))

    if len(ds) != 36:
        raise RuntimeError(f"Expected 36 double-sixes, got {len(ds)}")

    # Stabilizer size (unordered double-six, so allow swap of A and B)
    A0 = set(ds[0][0])
    B0 = set(ds[0][1])
    stab = 0
    for g in G:
        Ag = {g[i] for i in A0}
        Bg = {g[i] for i in B0}
        if (Ag == A0 and Bg == B0) or (Ag == B0 and Bg == A0):
            stab += 1

    summary = {
        "we6_group_order": len(G),
        "orbit_size": 27,
        "schlafli_ip_counts": ip_counts,
        "n_k6_cliques": len(k6),
        "n_double_sixes": len(ds),
        "double_six_stabilizer_size_allow_swap": stab,
        "double_six_orbit_size": len(G) // stab,
        "example_double_six": {
            "A": list(map(int, ds[0][0])),
            "B": list(map(int, ds[0][1])),
            "pairing_A_to_B_skew_edges": ds[0][2],
        },
    }

    (ROOT / "we6_double_six_stabilizer_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
