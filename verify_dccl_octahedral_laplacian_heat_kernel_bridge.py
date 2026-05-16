#!/usr/bin/env python3
"""Part DCCL: octahedral Laplacian / heat-kernel bridge.

Builds on DCCXLIX (closure-clock phase space = octahedron) by adding the exact
spectral dynamics of that phase space.

For the octahedron graph O with 6 vertices, adjacency A, and Laplacian
    L = D - A,
this verifier proves:
- O has degree 4 and 12 edges,
- Laplacian spectrum is exactly {0, 4, 4, 4, 6, 6},
- triangle count is 8 (matching octahedron faces),
- heat kernel K_t = exp(-tL) is symmetric and row-stochastic,
- closure levels from DCCXLIX match the 6-state Laplacian phase space.

This turns DCCXLIX's geometric identification into a concrete finite diffusion /
harmonic dynamics law on the same phase space.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlix_octahedron_closure_phase_space import build_bridge as build_dccxlix

OUT_PATH = ROOT / "data" / "dccl_octahedral_laplacian_heat_kernel_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    edge_count: int
    degree: int
    triangle_count: int
    spectral_gap: int
    all_identities_hold: bool


def octahedron_vertices() -> list[tuple[str, int]]:
    return [
        ("B23", +1), ("B23", -1),
        ("B31", +1), ("B31", -1),
        ("B12", +1), ("B12", -1),
    ]


def adjacency_matrix(verts: list[tuple[str, int]]) -> np.ndarray:
    n = len(verts)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if verts[i][0] != verts[j][0]:
                A[i, j] = 1.0
    return A


def heat_kernel(L: np.ndarray, t: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(L)
    exp_vals = np.diag(np.exp(-t * vals))
    return vecs @ exp_vals @ vecs.T


def to_list(a: np.ndarray, ndigits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=ndigits).tolist()


def build_bridge() -> dict[str, Any]:
    dccxlix = build_dccxlix()

    verts = octahedron_vertices()
    A = adjacency_matrix(verts)
    n = A.shape[0]
    deg = A.sum(axis=1)
    D = np.diag(deg)
    L = D - A

    eigvals = np.linalg.eigvalsh(L)
    eigvals_int = [int(round(x)) for x in eigvals]

    # triangles = tr(A^3)/6 for simple undirected graph
    triangles = int(round(np.trace(np.linalg.matrix_power(A.astype(int), 3)) / 6))

    sample_t = [0.0, 0.5, 1.0, 2.0]
    kernels = {str(t): heat_kernel(L, t) for t in sample_t}

    identities = {
        "vertex_count_is_6": n == 6,
        "edge_count_is_12": int(A.sum() // 2) == 12,
        "regular_degree_is_4": np.allclose(deg, 4),
        "laplacian_spectrum_is_0_4_4_4_6_6": eigvals_int == [0, 4, 4, 4, 6, 6],
        "triangle_count_is_8": triangles == 8,
        "triangle_count_matches_octahedron_faces": triangles == dccxlix["summary"]["octahedron_F"],
        "heat_kernel_is_symmetric": all(np.allclose(K, K.T, atol=1e-12) for K in kernels.values()),
        "heat_kernel_rows_sum_to_one": all(np.allclose(K.sum(axis=1), 1.0, atol=1e-12) for K in kernels.values()),
        "heat_kernel_is_nonnegative": all((K >= -1e-12).all() for K in kernels.values()),
        "t0_heat_kernel_is_identity": np.allclose(kernels["0.0"], np.eye(n), atol=1e-12),
        "phase_space_size_matches_closure_levels": n == dccxlix["summary"]["nilpotence_index"] == 6,
    }

    summary = BridgeSummary(
        vertex_count=n,
        edge_count=int(A.sum() // 2),
        degree=int(round(float(deg[0]))),
        triangle_count=triangles,
        spectral_gap=eigvals_int[1],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "graph_model": {
            "vertices": verts,
            "adjacency": to_list(A, ndigits=0),
            "laplacian": to_list(L, ndigits=0),
        },
        "spectral_data": {
            "laplacian_eigenvalues": eigvals_int,
            "spectral_gap": eigvals_int[1],
            "triangle_count": triangles,
        },
        "sample_heat_kernels": {k: to_list(v) for k, v in kernels.items()},
        "bridge_claim": {
            "exact_layer": (
                "The octahedral closure phase space has Laplacian spectrum (0,4,4,4,6,6) and an exact stochastic symmetric heat-kernel dynamics whose triangle count equals the 8 face modes."
            ),
            "conditional_layer": (
                "Interpreting this finite harmonic dynamics as continuum spacetime diffusion requires an additional scaling/limit theorem."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
