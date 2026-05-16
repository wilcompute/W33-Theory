#!/usr/bin/env python3
"""Part DCCLII: octahedral Poisson-Green bridge.

Builds on DCCLI by deriving the exact Moore-Penrose pseudoinverse of the
octahedral Laplacian and the induced Poisson solver on mean-zero sources.

With spectral projectors P0, P4, P6 (eigenvalues 0,4,6), define
    L_plus = (1/4) P4 + (1/6) P6.
Then
    L L_plus = L_plus L = I - P0,
    L_plus 1 = 0,
and for any source b with sum(b)=0,
    x = L_plus b
solves
    Lx = b,
with zero-mean gauge.
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

from verify_dccli_octahedral_spectral_projector_semigroup_bridge import build_bridge as build_dccli

OUT_PATH = ROOT / "data" / "dcclii_octahedral_poisson_green_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    rank_laplacian: int
    nullity_laplacian: int
    trace_l_plus: float
    all_identities_hold: bool


def as_matrix(a: list[list[float]]) -> np.ndarray:
    return np.array(a, dtype=float)


def to_list(a: np.ndarray, digits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=digits).tolist()


def to_vec(v: np.ndarray, digits: int = 12) -> list[float]:
    return np.round(v, decimals=digits).tolist()


def build_bridge() -> dict[str, Any]:
    dccli = build_dccli()
    P0 = as_matrix(dccli["projectors"]["P0"])
    P4 = as_matrix(dccli["projectors"]["P4"])
    P6 = as_matrix(dccli["projectors"]["P6"])

    n = P0.shape[0]
    I = np.eye(n)

    # Reconstruct L from modal data from DCCLI
    L = 4 * P4 + 6 * P6
    L_plus = 0.25 * P4 + (1.0 / 6.0) * P6

    # Penrose-style checks on symmetric Laplacian pseudoinverse
    LLp = L @ L_plus
    LpL = L_plus @ L

    one = np.ones(n)

    sample_sources = {
        "b1": np.array([1, -1, 0, 0, 0, 0], dtype=float),
        "b2": np.array([2, -1, -1, 0, 0, 0], dtype=float),
        "b3": np.array([1, 1, -1, -1, 0, 0], dtype=float),
    }

    sample_solutions = {}
    for name, b in sample_sources.items():
        x = L_plus @ b
        residual = L @ x - b
        sample_solutions[name] = {
            "source": b,
            "solution": x,
            "residual": residual,
            "source_sum": float(np.sum(b)),
            "solution_sum": float(np.sum(x)),
        }

    identities = {
        "laplacian_rank_is_5": bool(np.linalg.matrix_rank(L, tol=1e-10) == 5),
        "laplacian_nullity_is_1": bool(n - np.linalg.matrix_rank(L, tol=1e-10) == 1),
        "pseudoinverse_penrose_left_right": bool(np.allclose(LLp, I - P0, atol=1e-10) and np.allclose(LpL, I - P0, atol=1e-10)),
        "pseudoinverse_symmetric": bool(np.allclose(L_plus, L_plus.T, atol=1e-12)),
        "pseudoinverse_annihilates_constant_mode": bool(np.allclose(L_plus @ one, 0, atol=1e-12) and np.allclose(one @ L_plus, 0, atol=1e-12)),
        "all_sample_sources_are_mean_zero": bool(all(abs(item["source_sum"]) < 1e-12 for item in sample_solutions.values())),
        "all_sample_poisson_residuals_vanish": bool(all(np.linalg.norm(item["residual"], ord=np.inf) < 1e-10 for item in sample_solutions.values())),
        "all_sample_solutions_are_zero_mean_gauge": bool(all(abs(item["solution_sum"]) < 1e-10 for item in sample_solutions.values())),
    }

    summary = BridgeSummary(
        vertex_count=n,
        rank_laplacian=int(np.linalg.matrix_rank(L, tol=1e-10)),
        nullity_laplacian=int(n - np.linalg.matrix_rank(L, tol=1e-10)),
        trace_l_plus=float(np.trace(L_plus)),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "green_definition": {
            "laplacian": "L = 4P4 + 6P6",
            "pseudoinverse": "L+ = (1/4)P4 + (1/6)P6",
            "poisson_solver": "x = L+ b for sum(b)=0",
        },
        "operators": {
            "L": to_list(L),
            "L_plus": to_list(L_plus),
            "LL_plus": to_list(LLp),
            "L_plusL": to_list(LpL),
        },
        "sample_poisson_solutions": {
            name: {
                "source": to_vec(item["source"]),
                "solution": to_vec(item["solution"]),
                "residual": to_vec(item["residual"]),
                "source_sum": item["source_sum"],
                "solution_sum": item["solution_sum"],
            }
            for name, item in sample_solutions.items()
        },
        "bridge_claim": {
            "exact_layer": (
                "The octahedral closure phase space has an exact Green/Poisson solver: the Laplacian pseudoinverse L+ = (1/4)P4 + (1/6)P6 solves Lx=b uniquely in zero-mean gauge for every mean-zero source."
            ),
            "conditional_layer": (
                "Interpreting this finite Poisson/Green solver as continuum field propagation requires a scaling-limit theorem."
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
