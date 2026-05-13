#!/usr/bin/env python3
"""Part DCII: Fourier diagonalization of the toroidal Markov bridge.

For the 8-state chain from Part DC (7 active cycle modes + ground), this module
records the closed-form spectrum:

  eigenvalues = {1, 0} U { 1/8 + (3/4) cos(2*pi*k/7) : k=1..6 }.

It then verifies the exact trigonometric sum identities that recover the
spectral-moment bridge from Part DCI.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MOMENT_PATH = ROOT / "data" / "tomotope_toroidal_markov_spectral_moment_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_fourier_bridge.json"


def _close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


@dataclass(frozen=True)
class FourierSummary:
    active_cycle_size: int
    nontrivial_mode_count: int
    affine_offset_num: int
    affine_offset_den: int
    cosine_scale_num: int
    cosine_scale_den: int
    nontrivial_sum_num: int
    nontrivial_sum_den: int
    nontrivial_square_sum_num: int
    nontrivial_square_sum_den: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    moment = json.loads(MOMENT_PATH.read_text(encoding="utf-8"))
    expected = moment["summary"]

    n = 7
    offset = Fraction(1, 8)
    scale = Fraction(3, 4)

    # k = 1..6 nontrivial active-cycle Fourier modes.
    cos_values = [math.cos(2.0 * math.pi * k / n) for k in range(1, n)]
    lambdas = [float(offset) + float(scale) * c for c in cos_values]

    # Exact finite trigonometric sums for n=7:
    # sum_{k=1}^{6} cos(2*pi*k/7) = -1,
    # sum_{k=1}^{6} cos^2(2*pi*k/7) = 5/2.
    cos_sum_exact = Fraction(-1, 1)
    cos_sq_sum_exact = Fraction(5, 2)

    # Nontrivial eigenvalue sums computed exactly from identities.
    nontrivial_sum = 6 * offset + scale * cos_sum_exact
    nontrivial_square_sum = (
        6 * (offset * offset)
        + 2 * offset * scale * cos_sum_exact
        + (scale * scale) * cos_sq_sum_exact
    )

    trace_p_exact = Fraction(1, 1) + Fraction(0, 1) + nontrivial_sum
    trace_p2_exact = Fraction(1, 1) + Fraction(0, 1) + nontrivial_square_sum

    identities = {
        "nontrivial_sum_is_zero": nontrivial_sum == Fraction(0, 1),
        "trace_p_is_one": trace_p_exact == Fraction(1, 1),
        "nontrivial_square_sum_is_21_over_16": nontrivial_square_sum == Fraction(21, 16),
        "trace_p2_is_37_over_16": trace_p2_exact == Fraction(37, 16),
        "trace_p_matches_dci": (
            trace_p_exact
            == Fraction(int(expected["trace_p_num"]), int(expected["trace_p_den"]))
        ),
        "trace_p2_matches_dci": (
            trace_p2_exact
            == Fraction(int(expected["trace_p2_num"]), int(expected["trace_p2_den"]))
        ),
        "nontrivial_square_sum_matches_dci": (
            nontrivial_square_sum
            == Fraction(
                int(expected["nontrivial_second_moment_num"]),
                int(expected["nontrivial_second_moment_den"]),
            )
        ),
        "float_sum_consistent_with_exact": _close(sum(lambdas), float(nontrivial_sum)),
        "float_square_sum_consistent_with_exact": _close(
            sum(x * x for x in lambdas), float(nontrivial_square_sum)
        ),
    }

    summary = FourierSummary(
        active_cycle_size=n,
        nontrivial_mode_count=6,
        affine_offset_num=offset.numerator,
        affine_offset_den=offset.denominator,
        cosine_scale_num=scale.numerator,
        cosine_scale_den=scale.denominator,
        nontrivial_sum_num=nontrivial_sum.numerator,
        nontrivial_sum_den=nontrivial_sum.denominator,
        nontrivial_square_sum_num=nontrivial_square_sum.numerator,
        nontrivial_square_sum_den=nontrivial_square_sum.denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "closed_form": {
            "formula": "lambda_k = 1/8 + (3/4) cos(2*pi*k/7), k=1..6",
            "nontrivial_modes_numeric": lambdas,
            "special_modes": [1.0, 0.0],
        },
        "trigonometric_identities": {
            "sum_cos_2pi_k_over_7_k_1_to_6": "-1",
            "sum_cos2_2pi_k_over_7_k_1_to_6": "5/2",
        },
        "identities": identities,
        "notes": (
            "Fourier bridge: the six nontrivial Markov modes on the active 7-cycle "
            "are an affine cosine packet. Their exact square-sum is 21/16, which "
            "is the spectral source of the 21->42->168 transport ladder."
        ),
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
