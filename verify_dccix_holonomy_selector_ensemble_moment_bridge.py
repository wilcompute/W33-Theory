#!/usr/bin/env python3
"""Part DCCIX: holonomy selector-ensemble-moment bridge.

DCCVIII isolates a Z2 selector orientation over fixed quadratic shell data.
This verifier computes the equal-weight selector ensemble moments:

  - first moment (mean charge vector) is exactly zero,
  - second moment (covariance kernel) is deterministic,
  - the kernel is rank-1 with spectrum {13122, 0}.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from verify_dccviii_holonomy_selector_quadratic_invariant_bridge import (  # noqa: E402
    build_bridge as build_dccviii_bridge,
)


OUT_PATH = ROOT / "data" / "dccix_holonomy_selector_ensemble_moment_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    selector_state_count: int
    mean_vector: list[float]
    covariance_trace: int
    covariance_determinant: int
    covariance_rank: int
    all_identities_hold: bool


def _outer(v: tuple[int, int]) -> list[list[int]]:
    a, b = v
    return [[a * a, a * b], [b * a, b * b]]


def build_bridge() -> dict[str, Any]:
    payload = build_dccviii_bridge()

    profiles = payload["quadratic_profiles"]
    selector_values = sorted(profiles.keys())
    vectors = [tuple(int(x) for x in profiles[value]["charge_vector"]) for value in selector_values]

    state_count = len(vectors)
    mean_vector = [
        sum(v[0] for v in vectors) / state_count,
        sum(v[1] for v in vectors) / state_count,
    ]

    second_moment = [[0.0, 0.0], [0.0, 0.0]]
    for v in vectors:
        outer = _outer(v)
        second_moment[0][0] += outer[0][0] / state_count
        second_moment[0][1] += outer[0][1] / state_count
        second_moment[1][0] += outer[1][0] / state_count
        second_moment[1][1] += outer[1][1] / state_count

    covariance = [
        [second_moment[0][0] - mean_vector[0] * mean_vector[0], second_moment[0][1] - mean_vector[0] * mean_vector[1]],
        [second_moment[1][0] - mean_vector[1] * mean_vector[0], second_moment[1][1] - mean_vector[1] * mean_vector[1]],
    ]

    cov00 = int(round(covariance[0][0]))
    cov01 = int(round(covariance[0][1]))
    cov10 = int(round(covariance[1][0]))
    cov11 = int(round(covariance[1][1]))

    covariance_trace = cov00 + cov11
    covariance_determinant = cov00 * cov11 - cov01 * cov10
    covariance_rank = 1 if covariance_determinant == 0 and covariance_trace != 0 else (0 if covariance_trace == 0 else 2)

    # For this 2x2 symmetric kernel, eigenvalues solve λ^2 - tr λ + det = 0.
    # Here det=0, so the spectrum is {tr, 0}.
    eigenvalues = sorted([covariance_trace, 0], reverse=True)

    identities = {
        "dccviii_already_gives_two_opposite_charge_vectors": (
            selector_values == ["1", "2"]
            and vectors[0] == tuple(-x for x in vectors[1])
        ),
        "selector_ensemble_mean_vector_is_exactly_zero": mean_vector == [0.0, 0.0],
        "selector_ensemble_second_moment_is_the_fixed_polarization_kernel": (
            cov00 == 6561 and cov01 == -6561 and cov10 == -6561 and cov11 == 6561
        ),
        "covariance_kernel_has_rank_one": covariance_rank == 1,
        "covariance_kernel_spectrum_is_13122_and_0": (
            covariance_trace == 13122 and covariance_determinant == 0 and eigenvalues == [13122, 0]
        ),
        "therefore_orientation_is_randomized_in_first_moment_but_retained_in_second_moment": (
            mean_vector == [0.0, 0.0]
            and covariance_rank == 1
            and cov01 == -6561
            and covariance_trace == 13122
        ),
    }

    summary = BridgeSummary(
        selector_state_count=state_count,
        mean_vector=mean_vector,
        covariance_trace=covariance_trace,
        covariance_determinant=covariance_determinant,
        covariance_rank=covariance_rank,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "ensemble": {
            "selector_values": selector_values,
            "charge_vectors": [list(v) for v in vectors],
            "second_moment": [[int(round(x)) for x in row] for row in second_moment],
            "covariance": [[cov00, cov01], [cov10, cov11]],
            "eigenvalues": eigenvalues,
        },
        "interpretation": {
            "verdict": (
                "Averaging over selector orientation erases signed first-moment bias but leaves a deterministic rank-1 polarization covariance kernel. "
                "So the live Z2 orientation is hidden in mean and retained in second moment geometry."
            )
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