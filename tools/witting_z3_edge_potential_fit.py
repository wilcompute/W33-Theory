#!/usr/bin/env python3
"""Fit closed-form Z3 edge labels as affine/quadratic functions of (mu,nu).

We use the Z3 edge potential labels and attempt exact fits per family pair.
"""
from __future__ import annotations

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
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def build_nonorth_edges(rays, tol=1e-8):
    edges = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            if abs(np.vdot(rays[i], rays[j])) >= tol:
                edges.append((i, j))
    return edges


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def solve_edge_potential(rays):
    edges = build_nonorth_edges(rays)
    edge_index = {e: idx for idx, e in enumerate(edges)}
    triangles = []
    for i in range(40):
        for j in range(i + 1, 40):
            if (i, j) not in edge_index:
                continue
            for k in range(j + 1, 40):
                if (i, k) in edge_index and (j, k) in edge_index:
                    triangles.append((i, j, k))

    d1 = np.zeros((len(triangles), len(edges)), dtype=int)
    t = np.zeros(len(triangles), dtype=int)
    for t_idx, (i, j, k) in enumerate(triangles):
        e_jk = edge_index[(j, k)]
        e_ik = edge_index[(i, k)]
        e_ij = edge_index[(i, j)]
        d1[t_idx, e_jk] = 1
        d1[t_idx, e_ik] = -1
        d1[t_idx, e_ij] = 1
        ip = np.vdot(rays[i], rays[j]) * np.vdot(rays[j], rays[k]) * np.conjugate(np.vdot(rays[i], rays[k]))
        t[t_idx] = phase_to_k(np.angle(ip)) % 3

    # solve d1 x = t over GF(3) (one solution)
    A = d1.copy() % 3
    b = t.copy() % 3
    m, n = A.shape
    row = 0
    piv = [-1] * n
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
        piv[col] = row
        row += 1
        if row == m:
            break
    x = np.zeros(n, dtype=int)
    for col, r in enumerate(piv):
        if r != -1:
            x[col] = b[r] % 3
    return edges, x


def ray_family(idx):
    if idx < 4:
        return ("B", None, None)
    t = idx - 4
    pair = t // 4
    fam = t % 4
    mu = pair // 3
    nu = pair % 3
    return (f"F{fam}", mu, nu)


def solve_affine_mod3(X, y):
    X = np.array(X, dtype=int) % 3
    y = np.array(y, dtype=int) % 3
    m, n = X.shape
    row = 0
    piv = [-1] * n
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if X[r, col] % 3 != 0:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            X[[row, pivot]] = X[[pivot, row]]
            y[[row, pivot]] = y[[pivot, row]]
        inv = 1 if X[row, col] == 1 else 2
        X[row] = (X[row] * inv) % 3
        y[row] = (y[row] * inv) % 3
        for r in range(m):
            if r == row:
                continue
            if X[r, col] % 3 != 0:
                factor = X[r, col] % 3
                X[r] = (X[r] - factor * X[row]) % 3
                y[r] = (y[r] - factor * y[row]) % 3
        piv[col] = row
        row += 1
        if row == m:
            break
    for r in range(m):
        if np.all(X[r] % 3 == 0) and y[r] % 3 != 0:
            return None
    sol = np.zeros(n, dtype=int)
    for col, r in enumerate(piv):
        if r != -1:
            sol[col] = y[r] % 3
    return sol


def features_affine(mi, ni, mj, nj):
    return [mi, ni, mj, nj, 1]


def features_quadratic(mi, ni, mj, nj):
    v = [mi, ni, mj, nj]
    feats = []
    feats.extend(v)
    feats.extend([(x * x) % 3 for x in v])
    # cross terms
    for a in range(4):
        for b in range(a + 1, 4):
            feats.append((v[a] * v[b]) % 3)
    feats.append(1)
    return feats


def main():
    print("Z3 EDGE LABEL FIT (AFFINE/QUADRATIC)")
    print("=" * 60)
    rays = construct_witting_40_rays()
    edges, labels = solve_edge_potential(rays)

    # collect per family-pair data
    data = {}
    for idx, (i, j) in enumerate(edges):
        fi, mui, nui = ray_family(i)
        fj, muj, nuj = ray_family(j)
        key = tuple(sorted((fi, fj)))
        if key not in data:
            data[key] = []
        data[key].append((mui, nui, muj, nuj, int(labels[idx])))

    out_lines = []
    for key in sorted(data.keys()):
        X_aff = []
        y = []
        X_quad = []
        for mui, nui, muj, nuj, lab in data[key]:
            mi = 0 if mui is None else mui
            ni = 0 if nui is None else nui
            mj = 0 if muj is None else muj
            nj = 0 if nuj is None else nuj
            X_aff.append(features_affine(mi, ni, mj, nj))
            X_quad.append(features_quadratic(mi, ni, mj, nj))
            y.append(lab)

        sol_aff = solve_affine_mod3(X_aff, y)
        if sol_aff is None:
            out_lines.append(f"{key}: affine NO")
        else:
            pred = (np.array(X_aff) @ sol_aff) % 3
            exact = bool(np.all(pred == (np.array(y) % 3)))
            out_lines.append(f"{key}: affine {'OK' if exact else 'PARTIAL'} {sol_aff.tolist()}")

        sol_quad = solve_affine_mod3(X_quad, y)
        if sol_quad is None:
            out_lines.append(f"{key}: quad NO")
        else:
            pred = (np.array(X_quad) @ sol_quad) % 3
            exact = bool(np.all(pred == (np.array(y) % 3)))
            out_lines.append(f"{key}: quad {'OK' if exact else 'PARTIAL'}")

    out_path = ROOT / "docs" / "witting_z3_edge_potential_fit.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
