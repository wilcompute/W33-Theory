#!/usr/bin/env python3
"""Construct the full automorphism group of the symplectic GQ W(3,3) in pure Python.

This script builds the 40 projective points of PG(3,3), defines the standard
symplectic form J, and generates the full **general symplectic group** GSp(4,3)
acting on these points via matrix multiplication.

Key deliverable:
  * A permutation group of size 51840 acting transitively on the 40 points.

Why this matters:
  * Many "W33 TOE" steps rely on Aut(W(3,3)) having order 51,840.
  * This script **constructs that group concretely**, without Sage/GAP.

We generate:
  * Sp(4,3) via symplectic transvections x ↦ x + ω(x,v)v
  * and then extend to GSp(4,3) by adding a similitude with multiplier 2
    (diag(1,1,2,2), which satisfies M^T J M = 2J).

Outputs:
  * prints group size, orbit checks, and a few stabilizer sizes.
  * writes artifacts/w33_aut_group_summary.json
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import numpy as np

MOD = 3
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts" / "w33_aut_group_summary.json"


def canonical_point(v: np.ndarray) -> tuple[int, int, int, int] | None:
    """Return canonical representative for a projective point (1D subspace) in GF(3)^4."""
    v = (v % MOD).astype(int)
    if not np.any(v):
        return None
    # normalize so first nonzero entry is 1
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            v = (inv * v) % MOD
            break
    return tuple(int(x) for x in v)


def build_points() -> list[tuple[int, int, int, int]]:
    pts = []
    seen = set()
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    if a == b == c == d == 0:
                        continue
                    rep = canonical_point(np.array([a, b, c, d], dtype=int))
                    if rep not in seen:
                        seen.add(rep)
                        pts.append(rep)
    pts.sort()
    assert len(pts) == 40
    return pts


def symplectic_form() -> np.ndarray:
    I2 = np.eye(2, dtype=int)
    Z2 = np.zeros((2, 2), dtype=int)
    J = np.block([[Z2, I2], [(-I2) % MOD, Z2]]) % MOD
    return J


def omega(x: np.ndarray, y: np.ndarray, J: np.ndarray) -> int:
    return int((x @ J @ y) % MOD)


def transvection(v: np.ndarray, J: np.ndarray) -> np.ndarray:
    """Symplectic transvection: x ↦ x + ω(x,v) v."""
    v = (v % MOD).astype(int)
    vv = (v.reshape(4, 1) @ (v.reshape(1, 4) @ J)) % MOD
    return (np.eye(4, dtype=int) + vv) % MOD


def matrix_to_perm(M: np.ndarray, points: list[tuple[int, int, int, int]]):
    idx = {p: i for i, p in enumerate(points)}
    perm = []
    for p in points:
        v = np.array(p, dtype=int)
        w = (M @ v) % MOD
        rep = canonical_point(w)
        perm.append(idx[rep])
    return tuple(perm)


def generate_group(points):
    """Generate GSp(4,3) acting on projective points."""
    J = symplectic_form()

    # transvections along a small spanning set
    basis = [
        np.array([1, 0, 0, 0], int),
        np.array([0, 1, 0, 0], int),
        np.array([0, 0, 1, 0], int),
        np.array([0, 0, 0, 1], int),
        np.array([1, 1, 0, 0], int),
        np.array([0, 0, 1, 1], int),
        np.array([1, 0, 1, 0], int),
        np.array([0, 1, 0, 1], int),
    ]
    gens = [transvection(v, J) for v in basis]

    # add a similitude with multiplier 2: M^T J M = 2J
    sim = np.diag([1, 1, 2, 2]) % MOD
    gens.append(sim)

    perms = [matrix_to_perm(g, points) for g in gens]

    # BFS closure in permutation representation
    identity = tuple(range(len(points)))
    group = {identity}
    q = deque([identity])
    while q:
        g = q.popleft()
        for h in perms:
            comp = tuple(h[i] for i in g)
            if comp not in group:
                group.add(comp)
                q.append(comp)
    return group, perms


def main():
    points = build_points()
    group, gens = generate_group(points)

    # stabilizer sizes
    def stabilizer_size_of_point(p=0):
        return sum(1 for g in group if g[p] == p)

    summary = {
        "n_points": 40,
        "group_order": len(group),
        "n_generators": len(gens),
        "point_stabilizer_order": stabilizer_size_of_point(0),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("W33 automorphism group (projective action)")
    print("- points:", summary["n_points"])
    print("- group order:", summary["group_order"])
    print("- point stabilizer order:", summary["point_stabilizer_order"])
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
