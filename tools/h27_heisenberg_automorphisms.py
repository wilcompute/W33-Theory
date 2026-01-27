#!/usr/bin/env python3
"""Enumerate Heisenberg-style automorphisms of H27 and verify adjacency.

Model: vertices are (u,z) with u in F3^2, z in F3.
Adjacency: (u,z) ~ (v,w) iff u != v and w = z + B(u,v),
where B(u,v) = u2*v1 + 2*u1*v2 (alternating form).

Automorphisms of form:
  u' = A u + b
  z' = det(A) z + B(Au, b) + c
with A in GL(2,3), b in F3^2, c in F3.

Outputs:
- artifacts/h27_heisenberg_automorphisms.json
- artifacts/h27_heisenberg_automorphisms.md
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "h27_heisenberg_automorphisms.json"
OUT_MD = ROOT / "artifacts" / "h27_heisenberg_automorphisms.md"


def B(u, v):
    """Alternating bilinear form on F3^2."""
    return (u[1] * v[0] + 2 * u[0] * v[1]) % 3


def det2(A):
    return (A[0][0] * A[1][1] - A[0][1] * A[1][0]) % 3


def all_GL23():
    mats = []
    for a, b, c, d in product([0, 1, 2], repeat=4):
        A = ((a, b), (c, d))
        if det2(A) % 3 != 0:
            mats.append(A)
    return mats


def model_adj(u, z, v, w):
    return u != v and (w - z) % 3 == B(u, v)


def apply_auto(A, b, c, u, z):
    detA = det2(A)
    u2 = ((A[0][0] * u[0] + A[0][1] * u[1] + b[0]) % 3,
          (A[1][0] * u[0] + A[1][1] * u[1] + b[1]) % 3)
    # compute B(Au, b)
    Au = ((A[0][0] * u[0] + A[0][1] * u[1]) % 3,
          (A[1][0] * u[0] + A[1][1] * u[1]) % 3)
    # sign is negative to ensure w' - z' = B(Au+b, Av+b)
    z2 = (detA * z - B(Au, b) + c) % 3
    return u2, z2


def main():
    GL = all_GL23()
    points = [(u, z) for u in product([0, 1, 2], repeat=2) for z in [0, 1, 2]]

    # build adjacency matrix
    n = len(points)
    adj = np.zeros((n, n), dtype=int)
    for i, (u, z) in enumerate(points):
        for j, (v, w) in enumerate(points):
            if i != j and model_adj(u, z, v, w):
                adj[i, j] = 1

    auto_count = 0
    for A in GL:
        detA = det2(A)
        for b in product([0, 1, 2], repeat=2):
            for c in [0, 1, 2]:
                # verify adjacency preservation
                ok = True
                for i, (u, z) in enumerate(points):
                    u2, z2 = apply_auto(A, b, c, u, z)
                    i2 = points.index((u2, z2))
                    for j, (v, w) in enumerate(points):
                        if i == j:
                            continue
                        v2, w2 = apply_auto(A, b, c, v, w)
                        j2 = points.index((v2, w2))
                        if adj[i, j] != adj[i2, j2]:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    auto_count += 1

    results = {
        "GL23_size": len(GL),
        "automorphism_count": auto_count,
        "expected_size": len(GL) * 9 * 3,
    }

    lines = []
    lines.append("# H27 Heisenberg Automorphisms")
    lines.append("")
    lines.append(f"- |GL(2,3)| = {len(GL)}")
    lines.append(f"- Automorphisms found (A,b,c form): {auto_count}")
    lines.append(f"- Expected size: {len(GL) * 9 * 3}")

    OUT_JSON.write_text(json.dumps(results, indent=2))
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
