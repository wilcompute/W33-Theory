#!/usr/bin/env python3
"""Generate unitary matrices for the 24-basis Witting subset.

Each basis is orthonormal, so a unitary can be formed by taking the
basis vectors as columns. This file exports those unitaries for
experimental use.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


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


def orthogonal(v1, v2, tol=1e-8):
    return abs(np.vdot(v1, v2)) < tol


def find_tetrads(rays):
    n = len(rays)
    ortho = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if orthogonal(rays[i], rays[j]):
                ortho[i, j] = ortho[j, i] = True
    tetrads = []
    for a, b, c, d in combinations(range(n), 4):
        if (
            ortho[a, b]
            and ortho[a, c]
            and ortho[a, d]
            and ortho[b, c]
            and ortho[b, d]
            and ortho[c, d]
        ):
            tetrads.append((a, b, c, d))
    return tetrads


def main():
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)

    subset_path = ROOT / "artifacts" / "witting_ks_reduce_bases.json"
    if not subset_path.exists():
        print("Missing artifacts/witting_ks_reduce_bases.json")
        return

    subset = json.loads(subset_path.read_text())
    indices = subset.get("bases", [])
    bases = [tetrads[i] for i in indices]

    out = []
    for bi, base in enumerate(bases):
        # Build unitary with rays as columns
        U = np.column_stack([rays[i] for i in base])
        # Verify unitarity (numerical)
        check = np.allclose(U.conj().T @ U, np.eye(4), atol=1e-8)
        out.append(
            {
                "basis_index": bi,
                "rays": list(base),
                "unitary": [[complex(x) for x in row] for row in U],
                "unitary_ok": bool(check),
            }
        )

    out_path = DOCS / "witting_24basis_unitaries.json"
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
