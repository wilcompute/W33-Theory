#!/usr/bin/env python3
"""Part DCCLIV: octahedral commute/hitting-time bridge.

Builds on DCCLIII by translating exact resistance geometry into exact random-walk
time geometry on the same octahedral closure phase space.

For a connected undirected graph with m edges and effective resistance R_ij:
    commute_time C_ij = H_ij + H_ji = 2m * R_ij.

On the octahedron (m=12) with R_adj=5/12 and R_opp=1/2, this predicts:
    C_adj = 10,
    C_opp = 12.

Using explicit Markov-chain linear solves for hitting times H_ij, this part verifies
those values exactly and identifies orbit-wise one-way hitting times:
    H_adj = 5,
    H_opp = 6.
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

from verify_dccliii_octahedral_effective_resistance_dirichlet_bridge import build_bridge as build_dccliii

OUT_PATH = ROOT / "data" / "dccliv_octahedral_commute_hitting_time_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    edge_count: int
    adjacent_commute_time: float
    antipodal_commute_time: float
    adjacent_hitting_time: float
    antipodal_hitting_time: float
    kemeny_constant: float
    all_identities_hold: bool


def as_matrix(a: list[list[float]]) -> np.ndarray:
    return np.array(a, dtype=float)


def to_list(a: np.ndarray, digits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=digits).tolist()


def hitting_times_from_transition(P: np.ndarray) -> np.ndarray:
    n = P.shape[0]
    H = np.zeros((n, n), dtype=float)
    I = np.eye(n)
    one = np.ones(n)

    for target in range(n):
        idx = [k for k in range(n) if k != target]
        Q = P[np.ix_(idx, idx)]
        rhs = one[idx]
        h = np.linalg.solve(I[np.ix_(idx, idx)] - Q, rhs)
        for loc, state in enumerate(idx):
            H[state, target] = h[loc]
        H[target, target] = 0.0
    return H


def build_bridge() -> dict[str, Any]:
    dccliii = build_dccliii()

    L = as_matrix(dccliii["operators"]["L"])
    R = as_matrix(dccliii["operators"]["resistance_matrix"])
    adjacent_pairs = [tuple(p) for p in dccliii["pair_orbits"]["adjacent_pairs"]]
    antipodal_pairs = [tuple(p) for p in dccliii["pair_orbits"]["antipodal_pairs"]]

    n = L.shape[0]
    degree = float(L[0, 0])
    A = degree * np.eye(n) - L
    m = int(round(A.sum() / 2.0))
    P = A / degree

    H = hitting_times_from_transition(P)
    C = H + H.T

    adj_commute = np.array([C[i, j] for i, j in adjacent_pairs], dtype=float)
    opp_commute = np.array([C[i, j] for i, j in antipodal_pairs], dtype=float)
    adj_hit = np.array([H[i, j] for i, j in adjacent_pairs], dtype=float)
    opp_hit = np.array([H[i, j] for i, j in antipodal_pairs], dtype=float)

    resistance_commute = 2.0 * m * R

    # Kemeny constant from transition spectrum (exclude eigenvalue 1)
    evals = np.linalg.eigvals(P)
    evals = np.real_if_close(evals, tol=1e-10).astype(float)
    evals_sorted = np.sort(evals)[::-1]
    kemeny = float(np.sum([1.0 / (1.0 - lam) for lam in evals_sorted[1:]]))

    identities = {
        "edge_count_is_12": m == 12,
        "commute_equals_2mR_all_pairs": np.allclose(C, resistance_commute, atol=1e-10),
        "adjacent_commute_time_is_10": np.allclose(adj_commute, 10.0, atol=1e-10),
        "antipodal_commute_time_is_12": np.allclose(opp_commute, 12.0, atol=1e-10),
        "adjacent_hitting_time_is_5": np.allclose(adj_hit, 5.0, atol=1e-10),
        "antipodal_hitting_time_is_6": np.allclose(opp_hit, 6.0, atol=1e-10),
        "commute_is_symmetric": np.allclose(C, C.T, atol=1e-12),
        "hitting_diagonal_is_zero": np.allclose(np.diag(H), 0.0, atol=1e-12),
        "kemeny_constant_is_13_over_3": abs(kemeny - (13.0 / 3.0)) < 1e-10,
    }

    summary = BridgeSummary(
        vertex_count=n,
        edge_count=m,
        adjacent_commute_time=float(np.mean(adj_commute)),
        antipodal_commute_time=float(np.mean(opp_commute)),
        adjacent_hitting_time=float(np.mean(adj_hit)),
        antipodal_hitting_time=float(np.mean(opp_hit)),
        kemeny_constant=kemeny,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "random_walk_definition": {
            "transition": "P = A/4",
            "commute_formula": "C_ij = H_ij + H_ji = 2m R_ij",
            "edge_count": m,
        },
        "operators": {
            "transition_matrix": to_list(P),
            "hitting_times": to_list(H),
            "commute_times": to_list(C),
            "resistance_commute_from_2mR": to_list(resistance_commute),
        },
        "pair_orbits": {
            "adjacent_pairs": adjacent_pairs,
            "antipodal_pairs": antipodal_pairs,
        },
        "spectral_walk_data": {
            "transition_eigenvalues": np.round(np.sort(evals)[::-1], decimals=12).tolist(),
            "kemeny_constant": kemeny,
        },
        "bridge_claim": {
            "exact_layer": (
                "On the octahedral closure phase space, effective resistance and random-walk timing coincide exactly via C_ij=2mR_ij, yielding orbit values C_adj=10, C_opp=12 and one-way hitting times H_adj=5, H_opp=6."
            ),
            "conditional_layer": (
                "Interpreting these finite hitting/commute laws as continuum transport times requires a scaling limit."
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
