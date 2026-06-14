#!/usr/bin/env python3
"""
BT985 — Edgewise heat-trace convergence on the fat tower.

BT984 checked individual Whitney-0/P1 eigenvalues on the unit square.  BT985
packages the spectral-action observable directly: truncated heat traces

    H_N(t) = sum_{i<=N} exp(-t lambda_i)

on the edgewise/Freudenthal-Kuhn tower, compared to the exact Dirichlet square
spectrum lambda_{m,n}=pi^2(m^2+n^2).  This is still a flat/boundary seed, so it
is NOT an Einstein-Hilbert curvature proof; it is the numerical bridge needed
for the spectral side of R3: the fat tower stabilizes the heat trace while
preserving the shape-regularity hypothesis required by FEEC/Dodziuk-Patodi.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np

try:
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla
    HAVE_SCIPY = True
except Exception:  # pragma: no cover
    HAVE_SCIPY = False


@dataclass
class Mesh:
    verts: list[tuple[float, float]]
    tris: list[tuple[int, int, int]]

    def edgewise(self) -> "Mesh":
        verts = list(self.verts)
        mids: dict[tuple[int, int], int] = {}

        def mid(a: int, b: int) -> int:
            key = (a, b) if a < b else (b, a)
            if key not in mids:
                pa, pb = verts[a], verts[b]
                verts.append(((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2))
                mids[key] = len(verts) - 1
            return mids[key]

        out = []
        for a, b, c in self.tris:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            out.extend([(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)])
        return Mesh(verts, out)

    def min_angle_deg(self) -> float:
        ans = 180.0
        for tri in self.tris:
            pts = [self.verts[i] for i in tri]
            for i in range(3):
                p, q, r = pts[i], pts[(i + 1) % 3], pts[(i + 2) % 3]
                u = (q[0] - p[0], q[1] - p[1])
                v = (r[0] - p[0], r[1] - p[1])
                den = math.hypot(*u) * math.hypot(*v)
                if den:
                    c = max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / den))
                    ans = min(ans, math.degrees(math.acos(c)))
        return ans

    def interior(self) -> list[int]:
        return [i for i, (x, y) in enumerate(self.verts) if 1e-10 < x < 1 - 1e-10 and 1e-10 < y < 1 - 1e-10]

    def fem(self):
        if not HAVE_SCIPY:
            raise RuntimeError("BT985 needs scipy for sparse generalized eigenvalues")
        n = len(self.verts)
        rows: list[int] = []
        cols: list[int] = []
        kvals: list[float] = []
        mvals: list[float] = []
        for a, b, c in self.tris:
            (x1, y1), (x2, y2), (x3, y3) = self.verts[a], self.verts[b], self.verts[c]
            area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2
            bb = [y2 - y3, y3 - y1, y1 - y2]
            cc = [x3 - x2, x1 - x3, x2 - x1]
            idx = [a, b, c]
            for i in range(3):
                for j in range(3):
                    rows.append(idx[i]); cols.append(idx[j])
                    kvals.append((bb[i] * bb[j] + cc[i] * cc[j]) / (4 * area))
                    mvals.append(area / 12 * (2 if i == j else 1))
        return (sp.coo_matrix((kvals, (rows, cols)), shape=(n, n)).tocsr(),
                sp.coo_matrix((mvals, (rows, cols)), shape=(n, n)).tocsr())


def seed() -> Mesh:
    return Mesh([(0, 0), (1, 0), (1, 1), (0, 1)], [(0, 1, 2), (0, 2, 3)])


def exact_eigs(k: int) -> list[float]:
    vals = [math.pi ** 2 * (m * m + n * n) for m, n in product(range(1, 50), repeat=2)]
    return sorted(vals)[:k]


def low_eigs(mesh: Mesh, k: int) -> list[float]:
    K, M = mesh.fem()
    I = mesh.interior()
    if len(I) <= 2:
        return []
    K = K[I, :][:, I]
    M = M[I, :][:, I]
    kk = min(k, len(I) - 2)
    vals = spla.eigsh(K, M=M, k=kk, sigma=0.0, which="LM", return_eigenvectors=False, tol=1e-10)
    return [float(x) for x in sorted(vals)]


def heat(vals: list[float], t: float) -> float:
    return float(sum(math.exp(-t * x) for x in vals))


def main() -> None:
    k = 80
    ts = [0.01, 0.02, 0.05, 0.1]
    exact = exact_eigs(k)
    mesh = seed()
    levels = []
    for level in range(7):
        if level > 0:
            mesh = mesh.edgewise()
        eigs = low_eigs(mesh, k)
        row = {
            "level": level,
            "num_vertices": len(mesh.verts),
            "num_triangles": len(mesh.tris),
            "num_interior_vertices": len(mesh.interior()),
            "min_angle_deg": mesh.min_angle_deg(),
            "num_eigs": len(eigs),
            "lambda1": eigs[0] if eigs else None,
            "heat": {},
        }
        for t in ts:
            if eigs:
                fem = heat(eigs, t)
                target = heat(exact[:len(eigs)], t)
                row["heat"][str(t)] = {
                    "fem": fem,
                    "exact_same_truncation": target,
                    "relative_error_same_truncation": abs(fem - target) / target,
                }
        levels.append(row)

    out = {
        "theorem": "BT985 edgewise heat-trace convergence on the fat tower",
        "domain": "unit square, Dirichlet boundary",
        "exact_spectrum": "lambda_{m,n}=pi^2(m^2+n^2)",
        "t_values": ts,
        "levels": levels,
        "reading": "The fat edgewise tower stabilizes the heat trace; this is the spectral-action witness, not by itself a curvature proof.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt985_edgewise_heat_trace_convergence.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for row in levels:
        if row["num_eigs"]:
            print(row["level"], row["num_vertices"], row["num_eigs"], row["lambda1"], row["heat"]["0.05"])
    print("wrote data/bt985_edgewise_heat_trace_convergence.json")


if __name__ == "__main__":
    main()
