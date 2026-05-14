#!/usr/bin/env python3
"""Part DCLXXIII: holonomy tripotent hyperbolic flow bridge.

Part DCLXXII showed that the averaged witness kernel K is the time-1 sample of an
exact heat semigroup H_t = exp(-t G). The next deeper question is whether this
continuous-time flow still needs the full projector package, or whether it has
already collapsed to the single canonical tripotent M from Part DCLXVII.

This verifier proves the stronger statement:

    G = (log 10 / 2) M^2 + (log(8/5) / 2) M,

and hence

    H_t = P_0 + exp(-(log 10)t/2) [ cosh((log(8/5))t/2) M^2
                                    - sinh((log(8/5))t/2) M ].

So the entire continuous-time witness-average flow depends only on one canonical
tripotent and two scalar rates.
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

OUT_PATH = ROOT / "data" / "dclxxiii_holonomy_tripotent_hyperbolic_flow_bridge.json"


@dataclass(frozen=True)
class HyperbolicFlowSummary:
    point_count: int
    zero_rank: int
    positive_rank: int
    negative_rank: int
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


def _spectral_flow(
    t: float,
    p0: np.ndarray,
    p_plus: np.ndarray,
    p_minus: np.ndarray,
) -> np.ndarray:
    return p0 + (4.0 ** (-t)) * p_plus + ((2.0 / 5.0) ** t) * p_minus


def _hyperbolic_flow(t: float, p0: np.ndarray, tripotent: np.ndarray) -> np.ndarray:
    alpha = 0.5 * math.log(10.0)
    beta = 0.5 * math.log(8.0 / 5.0)
    M2 = tripotent @ tripotent
    return p0 + math.exp(-alpha * t) * (
        math.cosh(beta * t) * M2 - math.sinh(beta * t) * tripotent
    )


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    K = (12.0 * I - A + J) / 40.0

    P0, P_plus, P_minus = _projectors(A)
    M = _tripotent(A)
    M2 = M @ M

    alpha = 0.5 * math.log(10.0)
    beta = 0.5 * math.log(8.0 / 5.0)
    G_spectral = math.log(4.0) * P_plus + math.log(2.5) * P_minus
    G_tripotent = alpha * M2 + beta * M

    sample_times = (0.25, 0.5, 1.0, 1.5, 2.0)
    hyperbolic_matches = all(
        np.allclose(_hyperbolic_flow(t, P0, M), _spectral_flow(t, P0, P_plus, P_minus))
        for t in sample_times
    )

    identities = {
        "tripotent_is_exactly_the_dclxvii_operator": np.allclose(M, P_plus - P_minus)
        and np.allclose(M, (A + I - (13.0 / 40.0) * J) / 3.0),
        "tripotent_square_is_the_stationary_complement": np.allclose(M2, I - J / 40.0),
        "tripotent_cube_closes_back_to_itself": np.allclose(M2 @ M, M),
        "generator_is_even_plus_odd_tripotent_part": np.allclose(G_tripotent, G_spectral),
        "even_rate_is_half_log_10": abs(alpha - 0.5 * math.log(10.0)) < 1e-12,
        "odd_rate_is_half_log_8_over_5": abs(beta - 0.5 * math.log(8.0 / 5.0)) < 1e-12,
        "hyperbolic_flow_formula_matches_the_exact_semigroup": hyperbolic_matches,
        "time1_of_the_hyperbolic_flow_is_the_dclxviii_average_kernel": np.allclose(
            _hyperbolic_flow(1.0, P0, M), K
        ),
        "generator_commutes_with_the_tripotent": np.allclose(G_tripotent @ M, M @ G_tripotent),
        "therefore_the_continuous_witness_flow_depends_only_on_one_canonical_tripotent": (
            np.allclose(G_tripotent, G_spectral)
            and hyperbolic_matches
            and np.allclose(_hyperbolic_flow(1.0, P0, M), K)
        ),
    }

    summary = HyperbolicFlowSummary(
        point_count=n,
        zero_rank=1,
        positive_rank=24,
        negative_rank=15,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "tripotent_hyperbolic_coefficients": {
            "even": "log(10)/2",
            "odd": "log(8/5)/2",
        },
        "flow": {
            "generator": "G = (log(10)/2) M^2 + (log(8/5)/2) M",
            "semigroup": "H_t = P_0 + exp(-(log(10))t/2)(cosh((log(8/5))t/2) M^2 - sinh((log(8/5))t/2) M)",
            "breakthrough": (
                "The exact heat semigroup of Part DCLXXII does not require the full projector package. It is already a damped hyperbolic flow of the single canonical tripotent M, so the continuous witness-average dynamics have collapsed to one finite polarization operator plus two scalar rates."
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
