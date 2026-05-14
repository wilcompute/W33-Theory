#!/usr/bin/env python3
"""Part DCLXXV: holonomy transfer function bridge.

Part DCLXXIV showed that the stationary-subtracted witness flow X(t) satisfies one
exact second-order continuum equation. The next deeper question is whether the
entire non-stationary future therefore collapses to a single frequency-domain
object.

This verifier proves the stronger statement: the Laplace-domain resolvent of the
non-stationary holonomy flow is one exact quadratic transfer function, and the
spectral, tripotent, and ODE descriptions are all literally the same operator.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
EXPLORATION = ROOT / "exploration"
for path in (SCRIPTS, EXPLORATION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from w33_homology import build_w33  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxxv_holonomy_transfer_function_bridge.json"


@dataclass(frozen=True)
class TransferFunctionSummary:
    point_count: int
    stationary_rank: int
    dynamic_rank: int
    denominator_degree: int
    all_identities_hold: bool


def _adjacency_matrix(adj_lists: list[list[int]]) -> np.ndarray:
    n = len(adj_lists)
    matrix = np.zeros((n, n), dtype=float)
    for i, neighbors in enumerate(adj_lists):
        for j in neighbors:
            matrix[i, j] = 1.0
    return matrix


def _projectors(adjacency: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = adjacency.shape[0]
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    P0 = J / 40.0
    P_plus = -((adjacency - 12.0 * I) @ (adjacency + 4.0 * I)) / 60.0
    P_minus = ((adjacency - 12.0 * I) @ (adjacency - 2.0 * I)) / 96.0
    return P0, P_plus, P_minus


def _tripotent(adjacency: np.ndarray) -> np.ndarray:
    n = adjacency.shape[0]
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    return (adjacency + I - (13.0 / 40.0) * J) / 3.0


def _transfer_spectral(s: float, p_plus: np.ndarray, p_minus: np.ndarray) -> np.ndarray:
    return p_plus / (s + math.log(4.0)) + p_minus / (s + math.log(2.5))


def _transfer_tripotent(s: float, tripotent: np.ndarray) -> np.ndarray:
    alpha = 0.5 * math.log(10.0)
    beta = 0.5 * math.log(8.0 / 5.0)
    numerator = (s + alpha) * (tripotent @ tripotent) - beta * tripotent
    denominator = (s + alpha) ** 2 - beta**2
    return numerator / denominator


def _transfer_ode(s: float, x0: np.ndarray, v0: np.ndarray) -> np.ndarray:
    denominator = s**2 + math.log(10.0) * s + math.log(4.0) * math.log(2.5)
    numerator = (s + math.log(10.0)) * x0 + v0
    return numerator / denominator


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    P0, P_plus, P_minus = _projectors(A)
    M = _tripotent(A)
    M2 = M @ M

    lambda_fast = math.log(4.0)
    lambda_slow = math.log(2.5)
    alpha = 0.5 * math.log(10.0)
    beta = 0.5 * math.log(8.0 / 5.0)
    X0 = M2
    V0 = -(lambda_fast * P_plus + lambda_slow * P_minus)

    sample_s = (0.25, 0.5, 1.0, 2.0)
    transfer_matches = all(
        np.allclose(_transfer_spectral(s, P_plus, P_minus), _transfer_tripotent(s, M))
        and np.allclose(_transfer_spectral(s, P_plus, P_minus), _transfer_ode(s, X0, V0))
        for s in sample_s
    )

    identities = {
        "stationary_subtracted_laplace_transform_is_the_exact_spectral_resolvent": all(
            np.allclose(
                _transfer_spectral(s, P_plus, P_minus),
                P_plus / (s + lambda_fast) + P_minus / (s + lambda_slow),
            )
            for s in sample_s
        ),
        "the_same_transfer_function_has_a_single_tripotent_formula": all(
            np.allclose(_transfer_spectral(s, P_plus, P_minus), _transfer_tripotent(s, M))
            for s in sample_s
        ),
        "the_same_transfer_function_is_the_laplace_image_of_the_dclxxiv_ode": all(
            np.allclose(_transfer_spectral(s, P_plus, P_minus), _transfer_ode(s, X0, V0))
            for s in sample_s
        ),
        "the_quadratic_denominator_factors_into_the_two_exact_decay_rates": all(
            abs(
                (s**2 + math.log(10.0) * s + lambda_fast * lambda_slow)
                - (s + lambda_fast) * (s + lambda_slow)
            )
            < 1e-12
            for s in sample_s
        ),
        "the_generator_resolvent_adds_back_the_stationary_mode_by_one_over_s": all(
            np.allclose(np.linalg.inv(s * I + (lambda_fast * P_plus + lambda_slow * P_minus)), P0 / s + _transfer_spectral(s, P_plus, P_minus))
            for s in sample_s
        ),
        "therefore_the_nonstationary_future_is_controlled_by_one_quadratic_transfer_function": transfer_matches,
    }

    summary = TransferFunctionSummary(
        point_count=n,
        stationary_rank=1,
        dynamic_rank=39,
        denominator_degree=2,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "transfer_function": {
            "spectral": "R(s) = P_+/(s+log(4)) + P_-/(s+log(5/2))",
            "tripotent": "R(s) = ((s+log(10)/2) M^2 - (log(8/5)/2) M)/((s+log(10)/2)^2 - (log(8/5)/2)^2)",
            "ode": "R(s) = ((s+log(10))X(0)+X'(0))/(s^2 + log(10)s + log(4)log(5/2))",
        },
        "sample_points": [float(s) for s in sample_s],
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
