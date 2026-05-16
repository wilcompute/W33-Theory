#!/usr/bin/env python3
"""Part DCCLIII: octahedral effective-resistance / Dirichlet bridge.

Builds on DCCLII by extracting effective resistances from the exact Laplacian
pseudoinverse and verifying Dirichlet-energy identities for dipole sources.

For Laplacian pseudoinverse L+:
    R_ij = L+_ii + L+_jj - 2 L+_ij.

On the octahedron graph there are two pair-orbits:
- adjacent pairs (12): R_adj = 5/12,
- antipodal pairs (3): R_opp = 1/2.

Kirchhoff index:
    Kf = sum_{i<j} R_ij = n * tr(L+) = 13/2.

For dipole source b = e_i - e_j, potential x = L+ b satisfies
    Lx = b,
    x^T L x = b^T x = R_ij.
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

from verify_dcclii_octahedral_poisson_green_bridge import build_bridge as build_dcclii

OUT_PATH = ROOT / "data" / "dccliii_octahedral_effective_resistance_dirichlet_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    adjacent_pair_count: int
    antipodal_pair_count: int
    adjacent_resistance: float
    antipodal_resistance: float
    kirchhoff_index: float
    all_identities_hold: bool


def as_matrix(a: list[list[float]]) -> np.ndarray:
    return np.array(a, dtype=float)


def to_list(a: np.ndarray, digits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=digits).tolist()


def to_vec(v: np.ndarray, digits: int = 12) -> list[float]:
    return np.round(v, decimals=digits).tolist()


def build_bridge() -> dict[str, Any]:
    dcclii = build_dcclii()
    L = as_matrix(dcclii["operators"]["L"])
    L_plus = as_matrix(dcclii["operators"]["L_plus"])

    n = L.shape[0]
    # Robust adjacency recovery from Laplacian off-diagonals:
    # edges have L_ij = -1, non-edges have L_ij = 0 (up to rounding noise).
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if L[i, j] < -0.5:
                A[i, j] = 1.0

    R = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            R[i, j] = L_plus[i, i] + L_plus[j, j] - 2 * L_plus[i, j]

    adjacent_pairs = []
    antipodal_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] > 0.5:
                adjacent_pairs.append((i, j))
            else:
                antipodal_pairs.append((i, j))

    adj_vals = np.array([R[i, j] for i, j in adjacent_pairs], dtype=float)
    opp_vals = np.array([R[i, j] for i, j in antipodal_pairs], dtype=float)

    kirchhoff_index = float(sum(R[i, j] for i in range(n) for j in range(i + 1, n)))

    # Dipole checks: adjacent and antipodal representatives
    dipoles = {
        "adjacent_0_2": (0, 2),
        "antipodal_0_1": (0, 1),
    }
    dipole_checks = {}
    for name, (i, j) in dipoles.items():
        b = np.zeros(n)
        b[i] = 1.0
        b[j] = -1.0
        x = L_plus @ b
        residual = L @ x - b
        energy = float(x @ (L @ x))
        work = float(b @ x)
        dipole_checks[name] = {
            "i": i,
            "j": j,
            "source": to_vec(b),
            "potential": to_vec(x),
            "residual": to_vec(residual),
            "energy": energy,
            "work": work,
            "effective_resistance": float(R[i, j]),
            "potential_mean": float(np.mean(x)),
        }

    identities = {
        "adjacent_pairs_count_is_12": len(adjacent_pairs) == 12,
        "antipodal_pairs_count_is_3": len(antipodal_pairs) == 3,
        "adjacent_resistance_is_5_over_12": np.allclose(adj_vals, 5.0 / 12.0, atol=1e-10),
        "antipodal_resistance_is_1_over_2": np.allclose(opp_vals, 1.0 / 2.0, atol=1e-10),
        "kirchhoff_index_is_13_over_2": abs(kirchhoff_index - 6.5) < 1e-10,
        "kirchhoff_matches_n_trace_lplus": abs(kirchhoff_index - (n * float(np.trace(L_plus)))) < 1e-10,
        "dipole_residuals_vanish": all(max(abs(v) for v in d["residual"]) < 1e-10 for d in dipole_checks.values()),
        "dirichlet_energy_equals_work_equals_resistance": all(
            abs(d["energy"] - d["work"]) < 1e-10 and abs(d["work"] - d["effective_resistance"]) < 1e-10
            for d in dipole_checks.values()
        ),
        "dipole_potentials_have_zero_mean": all(abs(d["potential_mean"]) < 1e-10 for d in dipole_checks.values()),
    }

    summary = BridgeSummary(
        vertex_count=n,
        adjacent_pair_count=len(adjacent_pairs),
        antipodal_pair_count=len(antipodal_pairs),
        adjacent_resistance=float(np.mean(adj_vals)),
        antipodal_resistance=float(np.mean(opp_vals)),
        kirchhoff_index=kirchhoff_index,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "resistance_definition": {
            "formula": "R_ij = L+_ii + L+_jj - 2L+_ij",
            "adjacent_value": "5/12",
            "antipodal_value": "1/2",
            "kirchhoff": "Kf = sum_{i<j} R_ij = n tr(L+) = 13/2",
        },
        "operators": {
            "L": to_list(L),
            "L_plus": to_list(L_plus),
            "resistance_matrix": to_list(R),
        },
        "pair_orbits": {
            "adjacent_pairs": adjacent_pairs,
            "antipodal_pairs": antipodal_pairs,
        },
        "dipole_checks": dipole_checks,
        "bridge_claim": {
            "exact_layer": (
                "The octahedral closure phase space has two exact resistance orbits (adjacent 5/12, antipodal 1/2), Kirchhoff index 13/2, and exact dipole Dirichlet identity x^TLx=b^Tx=R_ij under x=L+b."
            ),
            "conditional_layer": (
                "Interpreting this finite resistance/energy law as continuum field resistance geometry requires a scaling limit theorem."
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
