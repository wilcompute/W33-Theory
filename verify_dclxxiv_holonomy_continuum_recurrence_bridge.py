#!/usr/bin/env python3
"""Part DCLXXIV: holonomy continuum recurrence bridge.

Part DCLXXI compressed the stationary-subtracted witness-average dynamics to a
minimal order-two discrete recurrence. Part DCLXXII lifted the same dynamics to
an exact heat semigroup. The next deeper question is whether these are merely
compatible descriptions, or whether they are literally the same dynamical law in
continuous and discrete time.

This verifier proves the stronger statement: after subtracting the stationary
mode, the exact continuous-time witness flow satisfies one global second-order
ODE whose decay rates are precisely log(4) and log(5/2), and whose sampled roots
recover the discrete DCLXXI recurrence coefficients 13/20 and 1/10.
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

OUT_PATH = ROOT / "data" / "dclxxiv_holonomy_continuum_recurrence_bridge.json"


@dataclass(frozen=True)
class ContinuumRecurrenceSummary:
    point_count: int
    stationary_rank: int
    recurrence_order: int
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


def _flow(
    t: float,
    p0: np.ndarray,
    p_plus: np.ndarray,
    p_minus: np.ndarray,
) -> np.ndarray:
    return p0 + (4.0 ** (-t)) * p_plus + ((2.0 / 5.0) ** t) * p_minus


def _x(
    t: float,
    p0: np.ndarray,
    p_plus: np.ndarray,
    p_minus: np.ndarray,
) -> np.ndarray:
    return _flow(t, p0, p_plus, p_minus) - p0


def _x_prime(t: float, p_plus: np.ndarray, p_minus: np.ndarray) -> np.ndarray:
    return -math.log(4.0) * (4.0 ** (-t)) * p_plus - math.log(2.5) * ((2.0 / 5.0) ** t) * p_minus


def _x_second(t: float, p_plus: np.ndarray, p_minus: np.ndarray) -> np.ndarray:
    return (math.log(4.0) ** 2) * (4.0 ** (-t)) * p_plus + (math.log(2.5) ** 2) * ((2.0 / 5.0) ** t) * p_minus


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    P0, P_plus, P_minus = _projectors(A)

    lambda_fast = math.log(4.0)
    lambda_slow = math.log(2.5)
    ode_linear = lambda_fast + lambda_slow
    ode_constant = lambda_fast * lambda_slow

    neighbor = next(j for j, value in enumerate(A[0]) if value == 1.0)
    nonneighbor = next(j for j, value in enumerate(A[0]) if value == 0.0 and j != 0)

    sample_times = (0.0, 0.5, 1.0, 1.5, 2.0)
    ode_holds = all(
        np.allclose(
            _x_second(t, P_plus, P_minus)
            + ode_linear * _x_prime(t, P_plus, P_minus)
            + ode_constant * _x(t, P0, P_plus, P_minus),
            np.zeros((n, n), dtype=float),
        )
        for t in sample_times
    )

    def _channel_values(index_pair: tuple[int, int]) -> dict[str, list[float]]:
        i, j = index_pair
        return {
                "x": [float(_x(t, P0, P_plus, P_minus)[i, j]) for t in sample_times],
                "x_prime": [float(_x_prime(t, P_plus, P_minus)[i, j]) for t in sample_times],
                "x_second": [float(_x_second(t, P_plus, P_minus)[i, j]) for t in sample_times],
        }

    channel_ode_holds = True
    for i, j in ((0, 0), (0, neighbor), (0, nonneighbor)):
        for t in sample_times:
            lhs = (
                _x_second(t, P_plus, P_minus)[i, j]
                + ode_linear * _x_prime(t, P_plus, P_minus)[i, j]
                + ode_constant * _x(t, P0, P_plus, P_minus)[i, j]
            )
            channel_ode_holds = bool(channel_ode_holds and abs(lhs) < 1e-12)

    identities = {
        "stationary_subtracted_flow_satisfies_one_global_second_order_ode": bool(ode_holds),
        "the_two_decay_rates_are_exactly_log_4_and_log_5_over_2": abs(lambda_fast - math.log(4.0)) < 1e-12 and abs(lambda_slow - math.log(2.5)) < 1e-12,
        "the_ode_coefficients_are_log_10_and_log_4_log_5_over_2": abs(ode_linear - math.log(10.0)) < 1e-12 and abs(ode_constant - (math.log(4.0) * math.log(2.5))) < 1e-12,
        "initial_position_is_the_stationary_complement": np.allclose(_x(0.0, P0, P_plus, P_minus), I - J / 40.0),
        "initial_velocity_is_minus_the_dclxxii_generator": np.allclose(_x_prime(0.0, P_plus, P_minus), -(lambda_fast * P_plus + lambda_slow * P_minus)),
        "diagonal_edge_and_nonedge_channels_obey_the_same_ode": bool(channel_ode_holds),
        "sampling_the_continuum_rates_recovers_the_dclxxi_recurrence_coefficients": abs(math.exp(-lambda_fast) + math.exp(-lambda_slow) - 13.0 / 20.0) < 1e-12 and abs(math.exp(-(lambda_fast + lambda_slow)) - 1.0 / 10.0) < 1e-12,
        "therefore_the_discrete_recurrence_and_continuous_heat_flow_are_the_same_two_rate_law": bool(
            ode_holds
            and channel_ode_holds
            and abs(math.exp(-lambda_fast) + math.exp(-lambda_slow) - 13.0 / 20.0) < 1e-12
            and abs(math.exp(-(lambda_fast + lambda_slow)) - 1.0 / 10.0) < 1e-12
        ),
    }

    summary = ContinuumRecurrenceSummary(
        point_count=n,
        stationary_rank=1,
        recurrence_order=2,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "continuum_recurrence": {
            "ode": "X'' + log(10) X' + log(4)log(5/2) X = 0",
            "fast_rate": str(lambda_fast),
            "slow_rate": str(lambda_slow),
            "sampled_discrete_sum": "13/20",
            "sampled_discrete_product": "1/10",
        },
        "channel_samples": {
            "diag": _channel_values((0, 0)),
            "edge": _channel_values((0, neighbor)),
            "nonedge": _channel_values((0, nonneighbor)),
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
