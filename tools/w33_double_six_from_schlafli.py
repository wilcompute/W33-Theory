#!/usr/bin/env python3
"""Compute Schlaefli double-sixes inside a 27-orbit of W(E6) acting on E8 roots.

This is a *fixed* version of the logic in tools.zip/compute_double_sixes.py.

Important correction:
  In the Schlaefli graph (SRG(27,16,10,8)), vertices correspond to the 27 lines
  on a cubic surface, and **edges correspond to skew lines**.  A six-tuple of
  mutually skew lines is therefore a **K6 clique**, not an independent set.

We:
  1) build E8 roots,
  2) find a 27-element orbit of W(E6),
  3) build the Schlaefli adjacency by inner product value (ip=1),
  4) enumerate K6 cliques (should be 72),
  5) pair them into double-sixes (should be 36) via a perfect-matching cross pattern.

Outputs:
  - /mnt/data/double_six_example.json
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
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
    dtype=np.float64,
)

# E6 subdiagram (a3..a8)
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


def snap(v: np.ndarray, tol: float = 1e-6) -> tuple[float, ...]:
    s = np.round(v * 2) / 2
    if np.max(np.abs(v - s)) < tol:
        return tuple(float(x) for x in s)
    return tuple(float(round(x, 8)) for x in v)


def reflect(v: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    return v - 2 * np.dot(v, alpha) / np.dot(alpha, alpha) * alpha


def we6_orbits(roots: np.ndarray) -> list[list[int]]:
    keys = [snap(r) for r in roots]
    key_to_idx = {k: i for i, k in enumerate(keys)}
    used = np.zeros(len(roots), dtype=bool)
    orbits: list[list[int]] = []
    for start in range(len(roots)):
        if used[start]:
            continue
        orb = [start]
        used[start] = True
        stack = [start]
        while stack:
            cur = stack.pop()
            v = roots[cur]
            for alpha in E6_SIMPLE_ROOTS:
                w = reflect(v, alpha)
                j = key_to_idx.get(snap(w))
                if j is not None and not used[j]:
                    used[j] = True
                    orb.append(j)
                    stack.append(j)
        orbits.append(orb)
    return orbits


def schlafli_adj(roots: np.ndarray, orbit: list[int]):
    orb_roots = roots[orbit]
    gram = orb_roots @ orb_roots.T
    ip_counts = Counter()
    n = len(orbit)
    for i in range(n):
        for j in range(i + 1, n):
            ip_counts[float(gram[i, j])] += 1
    # adjacency at ip=1 gives SRG(27,16,10,8)
    adj = np.abs(gram - 1.0) < 1e-9
    np.fill_diagonal(adj, False)
    return adj, ip_counts


def find_k_cliques(adj: np.ndarray, k: int) -> list[tuple[int, ...]]:
    n = adj.shape[0]
    # Convert numpy indices to native Python ints to avoid json-serialization issues downstream.
    nbr = [set(int(x) for x in np.nonzero(adj[i])[0]) for i in range(n)]
    out: list[tuple[int, ...]] = []

    def backtrack(clique, candidates):
        if len(clique) == k:
            out.append(tuple(int(x) for x in clique))
            return
        if len(clique) + len(candidates) < k:
            return
        # simple branching
        cand_list = sorted(candidates)
        while cand_list:
            v = cand_list.pop(0)
            new_cand = candidates & nbr[v]
            backtrack(clique + [v], new_cand)
            candidates.remove(v)

    for v in range(n):
        backtrack([v], set(range(v + 1, n)) & nbr[v])
    return out


def double_sixes_from_k6(adj: np.ndarray, k6s: list[tuple[int, ...]]):
    k6_set = set(k6s)
    ds = []
    used = set()
    for A in k6s:
        if A in used:
            continue
        Aset = set(A)
        for B in k6s:
            if B in used or B == A:
                continue
            Bset = set(B)
            if Aset & Bset:
                continue
            # cross edges must form a perfect matching: each a has exactly one neighbour in B, and vice versa
            ok = True
            match = {}
            inv = {}
            for a in A:
                neigh = [b for b in B if adj[a, b]]
                if len(neigh) != 1:
                    ok = False
                    break
                b = neigh[0]
                if b in inv:
                    ok = False
                    break
                match[a] = b
                inv[b] = a
            if ok and len(match) == 6:
                # ensure no extra edges (already implied by degree==1 condition)
                ds.append((A, B, match))
                used.add(A)
                used.add(B)
                break
    return ds


def main():
    roots = construct_e8_roots()
    orbits = we6_orbits(roots)
    o27 = next(o for o in orbits if len(o) == 27)
    adj, ip_counts = schlafli_adj(roots, o27)
    k6s = find_k_cliques(adj, 6)
    ds = double_sixes_from_k6(adj, k6s)

    payload = {
        "orbit_size": len(o27),
        "ip_counts": {str(k): int(v) for k, v in sorted(ip_counts.items())},
        "k6_count": len(k6s),
        "double_six_count": len(ds),
        "example": {
            "A": ds[0][0] if ds else None,
            "B": ds[0][1] if ds else None,
            "match": {str(k): int(v) for k, v in (ds[0][2].items() if ds else [])},
        },
    }
    out_path = ROOT / "artifacts" / "double_six_example.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
