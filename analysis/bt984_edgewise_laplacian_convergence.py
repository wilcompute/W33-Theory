#!/usr/bin/env python3
"""
BT984 — Edgewise (fat-tower) Laplacian convergence check.

BT983 isolated the R3 obstruction: the barycentric refinement tower is not
shape-regular, so CMS / Dodziuk-Patodi / FEEC hypotheses do not apply to that
tower. The proposed repair is to switch to an edgewise/Freudenthal-Kuhn tower.

This script supplies the first numerical verification layer on a seed with known
continuum spectrum: the unit square with Dirichlet boundary conditions.  We
assemble the P1 finite-element / Whitney-0-form stiffness and mass matrices and
check low generalized eigenvalues

    K u = lambda M u

against the continuum values

    lambda_{m,n}=pi^2(m^2+n^2),  m,n >= 1.

The goal is not to prove R3; it is to make the BT983 route executable: the fat
edgewise tower has bounded element quality and its low spectrum moves toward the
continuum spectrum, exactly as FEEC/Dodziuk-Patodi predict under shape
regularity.  The barycentric tower is included as a control: it may look
numerically decent at low levels, but its minimum angle collapses, so it is not
a valid theorem-carrier for the corpus.
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
    from scipy.linalg import eigh as dense_eigh
    HAVE_SCIPY = True
except Exception:  # pragma: no cover
    HAVE_SCIPY = False


@dataclass
class Mesh:
    verts: list[tuple[float, float]]
    tris: list[tuple[int, int, int]]

    def midpoint_refine(self) -> "Mesh":
        """Edgewise k=2 refinement: each triangle -> four similar children."""
        verts = list(self.verts)
        edge_mid: dict[tuple[int, int], int] = {}

        def mid(a: int, b: int) -> int:
            key = (a, b) if a < b else (b, a)
            if key not in edge_mid:
                pa, pb = verts[a], verts[b]
                verts.append(((pa[0] + pb[0]) / 2.0, (pa[1] + pb[1]) / 2.0))
                edge_mid[key] = len(verts) - 1
            return edge_mid[key]

        tris: list[tuple[int, int, int]] = []
        for a, b, c in self.tris:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            tris.extend([(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)])
        return Mesh(verts, tris)

    def barycentric_refine(self) -> "Mesh":
        """Barycentric refinement: each triangle -> six children."""
        verts = list(self.verts)
        edge_mid: dict[tuple[int, int], int] = {}

        def mid(a: int, b: int) -> int:
            key = (a, b) if a < b else (b, a)
            if key not in edge_mid:
                pa, pb = verts[a], verts[b]
                verts.append(((pa[0] + pb[0]) / 2.0, (pa[1] + pb[1]) / 2.0))
                edge_mid[key] = len(verts) - 1
            return edge_mid[key]

        tris: list[tuple[int, int, int]] = []
        for a, b, c in self.tris:
            pa, pb, pc = verts[a], verts[b], verts[c]
            verts.append(((pa[0] + pb[0] + pc[0]) / 3.0,
                          (pa[1] + pb[1] + pc[1]) / 3.0))
            g = len(verts) - 1
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            tris.extend([(a, ab, g), (ab, b, g), (b, bc, g),
                         (bc, c, g), (c, ca, g), (ca, a, g)])
        return Mesh(verts, tris)

    def min_angle_deg(self) -> float:
        out = 180.0
        for a, b, c in self.tris:
            pts = [self.verts[a], self.verts[b], self.verts[c]]
            for i in range(3):
                p, q, r = pts[i], pts[(i + 1) % 3], pts[(i + 2) % 3]
                u = (q[0] - p[0], q[1] - p[1])
                v = (r[0] - p[0], r[1] - p[1])
                denom = math.hypot(*u) * math.hypot(*v)
                if denom == 0:
                    continue
                cosang = max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / denom))
                out = min(out, math.degrees(math.acos(cosang)))
        return out

    def interior_vertices(self, eps: float = 1e-10) -> list[int]:
        return [i for i, (x, y) in enumerate(self.verts)
                if eps < x < 1.0 - eps and eps < y < 1.0 - eps]

    def fem_matrices(self):
        n = len(self.verts)
        rows: list[int] = []
        cols: list[int] = []
        kvals: list[float] = []
        mvals: list[float] = []
        for a, b, c in self.tris:
            (x1, y1), (x2, y2), (x3, y3) = self.verts[a], self.verts[b], self.verts[c]
            area2 = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
            area = abs(area2) / 2.0
            if area <= 1e-15:
                continue
            bvec = [y2 - y3, y3 - y1, y1 - y2]
            cvec = [x3 - x2, x1 - x3, x2 - x1]
            idx = [a, b, c]
            for i in range(3):
                for j in range(3):
                    rows.append(idx[i])
                    cols.append(idx[j])
                    kvals.append((bvec[i] * bvec[j] + cvec[i] * cvec[j]) / (4.0 * area))
                    mvals.append(area / 12.0 * (2.0 if i == j else 1.0))
        if HAVE_SCIPY:
            K = sp.coo_matrix((kvals, (rows, cols)), shape=(n, n)).tocsr()
            M = sp.coo_matrix((mvals, (rows, cols)), shape=(n, n)).tocsr()
        else:  # pragma: no cover
            K = np.zeros((n, n))
            M = np.zeros((n, n))
            for r, c, kv, mv in zip(rows, cols, kvals, mvals):
                K[r, c] += kv
                M[r, c] += mv
        return K, M


def square_seed() -> Mesh:
    return Mesh(
        verts=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
        tris=[(0, 1, 2), (0, 2, 3)],
    )


def continuum_square_eigs(k: int) -> list[float]:
    vals = []
    # Plenty for small k.
    for m, n in product(range(1, 20), repeat=2):
        vals.append(math.pi ** 2 * (m * m + n * n))
    return sorted(vals)[:k]


def low_eigs(K, M, k: int) -> list[float]:
    n = K.shape[0]
    if n == 0:
        return []
    kk = min(k, n)
    if HAVE_SCIPY and n > kk + 5:
        vals = spla.eigsh(K, M=M, k=kk, sigma=0.0, which="LM",
                          return_eigenvectors=False)
        return [float(x) for x in sorted(vals)]
    if HAVE_SCIPY:
        Kd = K.toarray() if hasattr(K, "toarray") else K
        Md = M.toarray() if hasattr(M, "toarray") else M
        vals = dense_eigh(Kd, Md, eigvals_only=True)
    else:  # pragma: no cover
        L = np.linalg.cholesky(M)
        Linv = np.linalg.inv(L)
        vals = np.linalg.eigvalsh(Linv @ K @ Linv.T)
    return [float(x) for x in sorted(vals)[:kk]]


def restrict_matrices(mesh: Mesh):
    K, M = mesh.fem_matrices()
    interior = mesh.interior_vertices()
    if HAVE_SCIPY:
        K = K[interior, :][:, interior]
        M = M[interior, :][:, interior]
    else:  # pragma: no cover
        K = K[np.ix_(interior, interior)]
        M = M[np.ix_(interior, interior)]
    return K, M, interior


def run_scheme(scheme: str, levels: int, k: int) -> list[dict]:
    mesh = square_seed()
    exact = continuum_square_eigs(k)
    rows: list[dict] = []
    for level in range(levels + 1):
        if level > 0:
            mesh = mesh.midpoint_refine() if scheme == "edgewise" else mesh.barycentric_refine()
        K, M, interior = restrict_matrices(mesh)
        eigs = low_eigs(K, M, min(k, max(0, len(interior) - 1))) if len(interior) else []
        rel_errors = [abs(e - exact[i]) / exact[i] for i, e in enumerate(eigs)]
        row = {
            "level": level,
            "num_vertices": len(mesh.verts),
            "num_triangles": len(mesh.tris),
            "num_interior_vertices": len(interior),
            "min_angle_deg": mesh.min_angle_deg(),
            "eigenvalues": eigs,
            "relative_errors": rel_errors,
        }
        if eigs:
            row["lambda1"] = eigs[0]
            row["lambda1_relative_error"] = rel_errors[0]
        rows.append(row)
    return rows


def heat_trace(eigs: list[float], t: float) -> float:
    return float(sum(math.exp(-t * x) for x in eigs))


def summarize_heat(rows: list[dict], exact_eigs: list[float], t_values: list[float]) -> None:
    exact = {str(t): heat_trace(exact_eigs, t) for t in t_values}
    for row in rows:
        row["heat_trace_partial"] = {}
        for t in t_values:
            if row["eigenvalues"]:
                ht = heat_trace(row["eigenvalues"], t)
                row["heat_trace_partial"][str(t)] = {
                    "fem": ht,
                    "exact_same_truncation": heat_trace(exact_eigs[:len(row["eigenvalues"])], t),
                    "exact_25": exact[str(t)],
                }


def main() -> None:
    k = 8
    exact = continuum_square_eigs(25)
    t_values = [0.01, 0.02, 0.05]
    out = {
        "theorem": "BT984 edgewise fat-tower Whitney-0/P1 Laplacian convergence check",
        "domain": "unit square, Dirichlet boundary",
        "continuum_formula": "lambda_{m,n}=pi^2(m^2+n^2), m,n>=1",
        "exact_first_8": exact[:8],
        "schemes": {
            "edgewise": run_scheme("edgewise", levels=6, k=k),
            "barycentric": run_scheme("barycentric", levels=4, k=k),
        },
    }
    for rows in out["schemes"].values():
        summarize_heat(rows, exact, t_values)

    edge = out["schemes"]["edgewise"]
    bary = out["schemes"]["barycentric"]
    out["verdict"] = {
        "edgewise_shape_regular": abs(edge[0]["min_angle_deg"] - edge[-1]["min_angle_deg"]) < 1e-9,
        "barycentric_min_angle_collapses": bary[-1]["min_angle_deg"] < 0.1 * bary[0]["min_angle_deg"],
        "edgewise_lambda1_error_improves": edge[-1]["lambda1_relative_error"] < edge[2]["lambda1_relative_error"],
        "edgewise_final_lambda1_relative_error": edge[-1]["lambda1_relative_error"],
        "reading": (
            "The edgewise tower preserves a 45-degree minimum angle on the square seed "
            "and drives the low FEM/Whitney-0 eigenvalues toward the exact Dirichlet spectrum. "
            "Barycentric levels are included only as a shape-regularity control: their angles "
            "collapse, so even when finite-level eigenvalues look plausible the tower is not a "
            "valid CMS/DP/FEEC theorem carrier."
        ),
    }

    data_path = Path("data/bt984_edgewise_laplacian_convergence.json")
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print("BT984 edgewise fat-tower Laplacian convergence check")
    print("exact first four:", [round(x, 6) for x in exact[:4]])
    for scheme, rows in out["schemes"].items():
        print(f"\n=== {scheme} ===")
        print("level vertices triangles min_angle lambda1 relerr")
        for row in rows:
            if "lambda1" not in row:
                print(row["level"], row["num_vertices"], row["num_triangles"],
                      f"{row['min_angle_deg']:.4f}", "(too few)")
            else:
                print(row["level"], row["num_vertices"], row["num_triangles"],
                      f"{row['min_angle_deg']:.4f}",
                      f"{row['lambda1']:.8f}",
                      f"{row['lambda1_relative_error']:.6e}")
    print("\nverdict:", out["verdict"])
    print(f"wrote {data_path}")


if __name__ == "__main__":
    main()
