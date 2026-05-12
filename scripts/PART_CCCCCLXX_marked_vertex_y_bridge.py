#!/usr/bin/env python3
"""
PART_CCCCCLXX_marked_vertex_y_bridge.py

Executable verifier for the first explicit incidence-derived Higgs/Yukawa
bridge atom:

    Y_v = P_K M_v P_B

where M_v marks the 12 edges incident to a chosen vertex v, P_K projects
onto ker(Delta_1), and P_B projects onto the 4-eigenspace / triangle-boundary
sector of the cellular 1-Hodge Laplacian.

Numerically verifies the exact pattern:

    rank(Y_v) = 8
    nonzero sigma^2 = 81/640, multiplicity 8
    S2 = 81/80
    S4 = 6561/51200

and for a triangle frame:

    rank(Y_tau) = 2
    nonzero sigma^2 = 81/640, multiplicity 2
    S2 = 81/320
    S4 = 6561/204800
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
from typing import Any

import numpy as np

F3 = (0, 1, 2)


@dataclass(frozen=True)
class MarkedVertexYBridgeResult:
    part: str
    title: str
    construction: dict[str, Any]
    laplacian_spectrum: dict[str, int]
    vertex_bridge: dict[str, Any]
    triangle_bridge: dict[str, Any]
    effective_mass_atom: dict[str, str]
    checks: dict[str, bool]
    all_checks_pass: bool


def normalize_projective(v: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    if all(x == 0 for x in v):
        return None
    for x in v:
        if x % 3:
            inv = 1 if x % 3 == 1 else 2
            return tuple((y * inv) % 3 for y in v)
    raise AssertionError("unreachable")


def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_w33() -> tuple[list[tuple[int, int, int, int]], list[tuple[int, int]], list[tuple[int, int, int]], np.ndarray]:
    seen = set()
    points: list[tuple[int, int, int, int]] = []
    for raw in product(F3, repeat=4):
        p = normalize_projective(raw)
        if p is not None and p not in seen:
            seen.add(p)
            points.append(p)

    n = len(points)
    adj = np.zeros((n, n), dtype=int)
    edges: list[tuple[int, int]] = []
    for i, j in combinations(range(n), 2):
        if symplectic(points[i], points[j]) == 0:
            adj[i, j] = adj[j, i] = 1
            edges.append((i, j))

    triangles: list[tuple[int, int, int]] = []
    for i, j, k in combinations(range(n), 3):
        if adj[i, j] and adj[i, k] and adj[j, k]:
            triangles.append((i, j, k))

    return points, edges, triangles, adj


def build_boundaries(n: int, edges: list[tuple[int, int]], triangles: list[tuple[int, int, int]]) -> tuple[np.ndarray, np.ndarray]:
    edge_index = {e: idx for idx, e in enumerate(edges)}
    d1 = np.zeros((n, len(edges)), dtype=float)
    for c, (i, j) in enumerate(edges):
        d1[i, c] = -1.0
        d1[j, c] = 1.0

    d2 = np.zeros((len(edges), len(triangles)), dtype=float)
    for c, (i, j, k) in enumerate(triangles):
        # Oriented boundary of [i,j,k] for i<j<k.
        for sign, e in ((1.0, (j, k)), (-1.0, (i, k)), (1.0, (i, j))):
            d2[edge_index[e], c] = sign
    return d1, d2


def projector(eigenvectors: np.ndarray, eigenvalues: np.ndarray, target: float, tol: float = 1e-7) -> np.ndarray:
    sub = eigenvectors[:, np.abs(eigenvalues - target) < tol]
    return sub @ sub.T


def singular_summary(Y: np.ndarray, tol: float = 1e-8) -> dict[str, Any]:
    vals = np.linalg.svd(Y, compute_uv=False)
    nz = vals[vals > tol]
    s2 = float(np.sum(nz**2))
    s4 = float(np.sum(nz**4))
    return {
        "rank": int(len(nz)),
        "nonzero_singular_values": [float(x) for x in nz],
        "nonzero_singular_squared_values": [float(x * x) for x in nz],
        "S2_numeric": s2,
        "S4_numeric": s4,
    }


def build_result() -> MarkedVertexYBridgeResult:
    points, edges, triangles, adj = build_w33()
    d1, d2 = build_boundaries(len(points), edges, triangles)
    delta1 = d1.T @ d1 + d2 @ d2.T
    eigvals, eigvecs = np.linalg.eigh(delta1)

    PK = projector(eigvecs, eigvals, 0.0)
    PB = projector(eigvecs, eigvals, 4.0)

    edge_index = {e: idx for idx, e in enumerate(edges)}

    v = 0
    vertex_mask = np.zeros(len(edges), dtype=float)
    for c, (i, j) in enumerate(edges):
        if i == v or j == v:
            vertex_mask[c] = 1.0
    Yv = PK @ np.diag(vertex_mask) @ PB
    v_summary = singular_summary(Yv)

    tau = triangles[0]
    tri_mask = np.zeros(len(edges), dtype=float)
    for e in combinations(tau, 2):
        tri_mask[edge_index[tuple(sorted(e))]] = 1.0
    Yt = PK @ np.diag(tri_mask) @ PB
    t_summary = singular_summary(Yt)

    sigma2 = Fraction(81, 640)
    vertex_S2 = 8 * sigma2
    vertex_S4 = 8 * sigma2 * sigma2
    tri_S2 = 2 * sigma2
    tri_S4 = 2 * sigma2 * sigma2

    rounded_spectrum: dict[str, int] = {}
    for target in [0, 4, 10, 16]:
        rounded_spectrum[str(target)] = int(np.sum(np.abs(eigvals - target) < 1e-7))

    checks = {
        "points_40": len(points) == 40,
        "edges_240": len(edges) == 240,
        "triangles_160": len(triangles) == 160,
        "spectrum_0_81": rounded_spectrum["0"] == 81,
        "spectrum_4_120": rounded_spectrum["4"] == 120,
        "vertex_mask_12_edges": int(np.sum(vertex_mask)) == 12,
        "vertex_rank_8": v_summary["rank"] == 8,
        "vertex_S2_81_over_80": abs(v_summary["S2_numeric"] - float(vertex_S2)) < 1e-9,
        "vertex_S4_6561_over_51200": abs(v_summary["S4_numeric"] - float(vertex_S4)) < 1e-9,
        "triangle_mask_3_edges": int(np.sum(tri_mask)) == 3,
        "triangle_rank_2": t_summary["rank"] == 2,
        "triangle_S2_81_over_320": abs(t_summary["S2_numeric"] - float(tri_S2)) < 1e-9,
        "triangle_S4_6561_over_204800": abs(t_summary["S4_numeric"] - float(tri_S4)) < 1e-9,
    }

    return MarkedVertexYBridgeResult(
        part="CCCCCLXX",
        title="Marked-Vertex Incidence Bridge for Y",
        construction={
            "vertex_bridge": "Y_v = P_K M_v P_B",
            "triangle_bridge": "Y_tau = P_K M_tau P_B",
            "P_K": "orthogonal projector onto ker Delta_1",
            "P_B": "orthogonal projector onto 4-eigenspace / boundary sector",
            "M_v": "diagonal mask on the 12 edges incident to marked vertex v",
            "M_tau": "diagonal mask on the 3 edges of marked triangle tau",
        },
        laplacian_spectrum=rounded_spectrum,
        vertex_bridge={
            "marked_vertex": v,
            "marked_edges": int(np.sum(vertex_mask)),
            "rank": v_summary["rank"],
            "nonzero_singular_squared_exact": "81/640",
            "nonzero_singular_squared_multiplicity": 8,
            "nonzero_singular_exact": "sqrt(81/640)=9/(8 sqrt(10))",
            "S2_exact": "81/80",
            "S4_exact": "6561/51200",
            "S2_numeric": v_summary["S2_numeric"],
            "S4_numeric": v_summary["S4_numeric"],
        },
        triangle_bridge={
            "marked_triangle": list(tau),
            "marked_edges": int(np.sum(tri_mask)),
            "rank": t_summary["rank"],
            "nonzero_singular_squared_exact": "81/640",
            "nonzero_singular_squared_multiplicity": 2,
            "S2_exact": "81/320",
            "S4_exact": "6561/204800",
            "S2_numeric": t_summary["S2_numeric"],
            "S4_numeric": t_summary["S4_numeric"],
        },
        effective_mass_atom={
            "vertex_mass_eigenvalues": "(81/640)/(4 M_F^2 + h), multiplicity 8",
            "triangle_mass_eigenvalues": "(81/640)/(4 M_F^2 + h), multiplicity 2",
            "single_vertex_residual_kernel_modes": "81 - 8 = 73",
            "principle": "physical Y should be synthesized from incidence-frame bridge atoms",
        },
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = build_result()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "marked-vertex Y bridge checks failed"
    out = Path("data/PART_CCCCCLXX_marked_vertex_y_bridge_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
