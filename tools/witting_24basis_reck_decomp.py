#!/usr/bin/env python3
"""Reck-style decomposition of 4x4 unitaries for the Witting 24-basis set.

We decompose each 4x4 unitary into a sequence of 2x2 complex Givens rotations
acting on adjacent modes (i-1,i) to zero below-diagonal entries.
Outputs a JSON with operations (i,j,theta,phi) and final diagonal phases.
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


def load_24basis_subset():
    path = ROOT / "artifacts" / "witting_ks_reduce_bases.json"
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("bases", [])
    return []


def complex_givens(a, b):
    """Return c,s for unitary G that zeroes b when applied to [a;b]."""
    if abs(b) < 1e-12:
        return 1.0 + 0j, 0.0 + 0j
    if abs(a) < 1e-12:
        return 0.0 + 0j, 1.0 + 0j

    ra = abs(a)
    rb = abs(b)
    r = np.sqrt(ra**2 + rb**2)

    # phases
    alpha = np.angle(a)
    beta = np.angle(b)

    c = np.exp(1j * beta) * (ra / r)
    s = np.exp(1j * alpha) * (rb / r)
    return c, s


def givens_matrix(n, i, j, c, s):
    """Construct NxN unitary with Givens rotation on rows i,j."""
    G = np.eye(n, dtype=complex)
    G[i, i] = c
    G[i, j] = s
    G[j, i] = -np.conjugate(s)
    G[j, j] = np.conjugate(c)
    return G


def reck_decompose(U):
    """Decompose U into Givens rotations. Returns ops and final diagonal phases."""
    n = U.shape[0]
    U_work = U.copy().astype(complex)
    ops = []

    for col in range(n - 1):
        for row in range(n - 1, col, -1):
            a = U_work[row - 1, col]
            b = U_work[row, col]
            c, s = complex_givens(a, b)
            G = givens_matrix(n, row - 1, row, c, s)
            U_work = G @ U_work
            # store operation (row-1,row,c,s)
            ops.append(
                {
                    "i": row - 1,
                    "j": row,
                    "c": c,
                    "s": s,
                    "theta": float(np.arccos(np.clip(abs(c), 0, 1))),
                    "phi": float((np.angle(s) - np.angle(c)) % (2 * np.pi)),
                }
            )

    # U_work is upper triangular with unit modulus diagonal
    diag = np.diag(U_work)
    phases = [float(np.angle(d)) for d in diag]

    # Verify reconstruction: U approx (G_k^H ... G_1^H) * diag
    return ops, phases


def main():
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    subset_indices = load_24basis_subset()
    if not subset_indices:
        print("Missing 24-basis subset")
        return

    bases = [tetrads[i] for i in subset_indices]

    out = []
    for bi, base in enumerate(bases):
        U = np.column_stack([rays[i] for i in base])
        ops, phases = reck_decompose(U)
        out.append(
            {
                "basis_index": bi,
                "rays": list(base),
                "ops": ops,
                "diag_phases": phases,
            }
        )

    out_path = DOCS / "witting_24basis_reck.json"
    out_path.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
