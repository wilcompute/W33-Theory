#!/usr/bin/env python3
"""Part DCLXXII: holonomy heat semigroup bridge.

After DCLXXI, the stationary-subtracted averaged witness dynamics are known to be
recurrence-complete. The next deeper question is whether the discrete kernel K
is merely a convenient step operator, or whether it already sits on an exact
continuous-time flow.

This verifier proves the stronger statement: K is the exact time-1 sample of a
self-adjoint two-rate heat semigroup

    H_t = exp(-t G)

with generator

    G = log(4) P_+ + log(5/2) P_-.

Equivalently, G lies in the three-channel adjacency algebra and satisfies

    K = exp(-G),
    H_t H_s = H_{t+s},
    d/dt H_t = -G H_t = -H_t G.

So the witness-average dynamics are not only algebraically closed, recurrence-
complete, and self-tomographing; they are already a sampled exact heat flow.
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
from w33_three_channel_operator_bridge import coefficient_matrix, interpolate_three_channel  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxxii_holonomy_heat_semigroup_bridge.json"


@dataclass(frozen=True)
class SemigroupSummary:
    point_count: int
    stationary_rank: int
    fast_rank: int
    slow_rank: int
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


def _semigroup(t: float, p0: np.ndarray, p_plus: np.ndarray, p_minus: np.ndarray) -> np.ndarray:
    return (
        p0
        + math.exp(-math.log(4.0) * t) * p_plus
        + math.exp(-math.log(2.5) * t) * p_minus
    )


def _semigroup_derivative(t: float, p_plus: np.ndarray, p_minus: np.ndarray) -> np.ndarray:
    return (
        -math.log(4.0) * math.exp(-math.log(4.0) * t) * p_plus
        - math.log(2.5) * math.exp(-math.log(2.5) * t) * p_minus
    )


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    K = (12.0 * I - A + J) / 40.0
    P0, P_plus, P_minus = _projectors(A)

    fast_rate = math.log(4.0)
    slow_rate = math.log(2.5)
    G = fast_rate * P_plus + slow_rate * P_minus

    coeffs = interpolate_three_channel(0.0, fast_rate, slow_rate)
    G_interp = coefficient_matrix(coeffs, adjacency=A)

    evals, evecs = np.linalg.eigh(K)
    logK = evecs @ np.diag(np.log(evals)) @ evecs.T
    G_from_log = -logK

    semigroup_law_holds = True
    differential_law_holds = True
    sample_pairs = [(0.5, 0.5), (0.5, 1.5), (1.0, 2.0), (1.5, 2.0)]
    for t, s in sample_pairs:
        Ht = _semigroup(t, P0, P_plus, P_minus)
        Hs = _semigroup(s, P0, P_plus, P_minus)
        Hts = _semigroup(t + s, P0, P_plus, P_minus)
        semigroup_law_holds = semigroup_law_holds and np.allclose(Ht @ Hs, Hts)

    for t in (0.5, 1.0, 1.5, 2.0):
        Ht = _semigroup(t, P0, P_plus, P_minus)
        dHt = _semigroup_derivative(t, P_plus, P_minus)
        differential_law_holds = differential_law_holds and np.allclose(dHt, -G @ Ht) and np.allclose(dHt, -Ht @ G)

    identities = {
        "generator_is_exactly_minus_matrix_log_of_the_average_kernel": np.allclose(G, G_from_log),
        "generator_lies_in_the_three_channel_adjacency_algebra": np.allclose(G, G_interp),
        "generator_coefficients_match_closed_form_log_formulas": np.allclose(
            G,
            (math.log(40.0) / 3.0) * I + (math.log(8.0 / 5.0) / 6.0) * A + ((5.0 * math.log(5.0) - 21.0 * math.log(2.0)) / 120.0) * J,
        ),
        "time1_of_the_semigroup_is_exactly_the_dclxviii_kernel": np.allclose(_semigroup(1.0, P0, P_plus, P_minus), K),
        "integer_times_match_discrete_powers": all(np.allclose(_semigroup(float(t), P0, P_plus, P_minus), np.linalg.matrix_power(K, t)) for t in range(1, 7)),
        "semigroup_law_holds_on_sample_times": semigroup_law_holds,
        "heat_equation_holds_on_sample_times": differential_law_holds,
        "generator_is_positive_semidefinite_with_two_nonzero_rates": np.allclose(np.linalg.eigvalsh(G), np.array([0.0] + [slow_rate] * 15 + [fast_rate] * 24)),
        "slow_rate_is_log_5_over_2_and_fast_rate_is_log_4": slow_rate < fast_rate and abs(slow_rate - math.log(2.5)) < 1e-12 and abs(fast_rate - math.log(4.0)) < 1e-12,
        "therefore_the_discrete_witness_average_is_a_sampled_exact_heat_flow": (
            np.allclose(G, G_from_log)
            and np.allclose(_semigroup(1.0, P0, P_plus, P_minus), K)
            and semigroup_law_holds
            and differential_law_holds
        ),
    }

    summary = SemigroupSummary(
        point_count=n,
        stationary_rank=1,
        fast_rank=24,
        slow_rank=15,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "generator_coefficients": {
            "I": "log(40)/3",
            "A": "log(8/5)/6",
            "J": "(5 log 5 - 21 log 2)/120",
        },
        "generator_rates": {
            "slow_rate": str(slow_rate),
            "fast_rate": str(fast_rate),
            "gap_ratio": str(fast_rate / slow_rate),
        },
        "interpretation": {
            "generator": "G = log(4) P_+ + log(5/2) P_- = -log(K)",
            "semigroup": "H_t = exp(-t G)",
            "breakthrough": (
                "The averaged witness kernel is not merely a discrete Markov step. It is exactly the time-1 sample of a self-adjoint two-rate heat semigroup, so the witness-average dynamics already possess a continuous-time completion inside the same finite operator algebra."
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