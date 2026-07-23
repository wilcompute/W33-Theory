#!/usr/bin/env python3
"""Prime-indexed infinite W(3,3) phase-operator moment program.

The finite W33 phase operator has two positive phase sectors.  This module
constructs a positive weighted direct-integral trace model indexed by prime
powers:

  trace weight: Lambda(n) (log n)^2 n^{-s},
  local inverse ordinate: log(n)/theta_j.

Its even inverse moments are

  M_2k(s) = T_2k * d^(2k+2)/ds^(2k+2)[-zeta'(s)/zeta(s)],  s>1.

A single damping exponent was already falsified at S6.  Here two fixed positive
damping channels, s=2 and s=3, are mixed.  A positive mixing weight, one global
operator scale, and one trace amplitude can interpolate the first three
classical xi moments exactly.  The eighth moment is then an out-of-sample test.
It misses by about 47.5%, rejecting this two-channel tower as the classical
Hilbert--Polya operator.

The construction is valuable because it is a genuine positive infinite trace
model and produces a precise next obstruction.  Moment interpolation is not a
determinant theorem and is not evidence that classical RH has been proved.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import mpmath as mp

from analysis.w33_prime_weight_discovery import (
    classical_xi_moments,
    log_derivative_dirichlet,
    w33_phase_moments,
)

ROOT = Path(__file__).resolve().parents[1]
S_LEFT = mp.mpf("2")
S_RIGHT = mp.mpf("3")


def prime_tower_moments_fast(s: mp.mpf, max_power: int = 4) -> dict[int, mp.mpf]:
    """Compute all required derivatives from one Taylor expansion."""
    phase = w33_phase_moments(max_power)
    max_order = 2 * max_power + 2
    coefficients = mp.taylor(log_derivative_dirichlet, s, max_order)
    return {
        2 * k: mp.mpf(phase[2 * k])
        * coefficients[2 * k + 2]
        * mp.factorial(2 * k + 2)
        for k in range(1, max_power + 1)
    }


def shape_invariant(moments: dict[int, mp.mpf]) -> mp.mpf:
    """Scale/amplitude invariant M6*M2/M4^2."""
    return moments[6] * moments[2] / moments[4] ** 2


def convex_mixture(
    left: dict[int, mp.mpf], right: dict[int, mp.mpf], weight_left: mp.mpf
) -> dict[int, mp.mpf]:
    return {
        k: weight_left * left[k] + (1 - weight_left) * right[k]
        for k in left
    }


def solve_positive_mixture_weight(
    left: dict[int, mp.mpf],
    right: dict[int, mp.mpf],
    target: dict[int, mp.mpf],
    lo: mp.mpf = mp.mpf("0.06"),
    hi: mp.mpf = mp.mpf("0.08"),
) -> mp.mpf:
    target_shape = target[6] * target[2] / target[4] ** 2

    def f(weight: mp.mpf) -> mp.mpf:
        return shape_invariant(convex_mixture(left, right, weight)) - target_shape

    flo = f(lo)
    fhi = f(hi)
    if flo * fhi >= 0:
        raise ValueError("mixture root is not bracketed")
    for _ in range(120):
        mid = (lo + hi) / 2
        fm = f(mid)
        if abs(fm) < mp.mpf("1e-45"):
            return mid
        if flo * fm <= 0:
            hi = mid
            fhi = fm
        else:
            lo = mid
            flo = fm
    return (lo + hi) / 2


def scale_and_amplitude(
    raw: dict[int, mp.mpf], target: dict[int, mp.mpf]
) -> tuple[mp.mpf, mp.mpf]:
    """Solve target_2=A raw_2/c^2 and target_4=A raw_4/c^4."""
    c_squared = raw[4] * target[2] / (raw[2] * target[4])
    scale = mp.sqrt(c_squared)
    amplitude = target[2] * c_squared / raw[2]
    return scale, amplitude


def rescale_moments(
    raw: dict[int, mp.mpf], scale: mp.mpf, amplitude: mp.mpf
) -> dict[int, mp.mpf]:
    return {k: amplitude * value / scale**k for k, value in raw.items()}


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 55
    target = classical_xi_moments(4)
    left = prime_tower_moments_fast(S_LEFT, 4)
    right = prime_tower_moments_fast(S_RIGHT, 4)
    weight = solve_positive_mixture_weight(left, right, target)
    raw = convex_mixture(left, right, weight)
    scale, amplitude = scale_and_amplitude(raw, target)
    prediction = rescale_moments(raw, scale, amplitude)
    relative_errors = {k: prediction[k] / target[k] - 1 for k in (2, 4, 6, 8)}
    checks = {
        "positive_mixture": 0 < weight < 1,
        "positive_trace_amplitude": amplitude > 0,
        "positive_operator_scale": scale > 0,
        "S2_interpolated": abs(relative_errors[2]) < mp.mpf("1e-35"),
        "S4_interpolated": abs(relative_errors[4]) < mp.mpf("1e-35"),
        "S6_interpolated": abs(relative_errors[6]) < mp.mpf("1e-30"),
        "S8_out_of_sample_falsifies_two_channel_tower": abs(relative_errors[8]) > mp.mpf("0.4"),
        "trace_moments_finite_for_s_gt_1": S_LEFT > 1 and S_RIGHT > 1,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "positive prime-indexed infinite W33 phase tower and S8 falsifier",
        "operator_model": {
            "local_W33_sectors": "theta_2=acos(1/sqrt(11)) mult 24; theta_-4=acos(-2/sqrt(11)) mult 15",
            "prime_power_trace_weight": "Lambda(n)(log n)^2 n^(-s)",
            "local_inverse_ordinate": "log(n)/theta_j",
            "moment_formula": "M_2k(s)=T_2k d^(2k+2)/ds^(2k+2)[-zeta'(s)/zeta(s)]",
            "trace_class_region": "s>1 for every fixed even inverse moment",
        },
        "two_channel_interpolation": {
            "damping_exponents": [str(S_LEFT), str(S_RIGHT)],
            "left_weight": mp.nstr(weight, 35),
            "right_weight": mp.nstr(1 - weight, 35),
            "global_operator_scale": mp.nstr(scale, 35),
            "trace_amplitude": mp.nstr(amplitude, 35),
            "interpretation": "three positive calibration parameters interpolate S2,S4,S6; this is a controlled fit, not a derivation",
        },
        "moments": {
            "classical_xi": {str(k): mp.nstr(v, 35) for k, v in target.items()},
            "tower_prediction": {str(k): mp.nstr(v, 35) for k, v in prediction.items()},
            "relative_errors": {str(k): mp.nstr(v, 35) for k, v in relative_errors.items()},
        },
        "out_of_sample_result": {
            "S8_relative_error": mp.nstr(relative_errors[8], 30),
            "verdict": "the two-damping positive W33 prime tower is rejected as the classical xi operator",
        },
        "claim_boundary": {
            "proved": [
                "the weighted direct-integral moments are positive and finite for s>1",
                "a positive two-channel mixture can interpolate the first three xi moments",
                "the resulting model fails the next moment without refitting",
            ],
            "not_proved": ["a regularized determinant identity", "uniqueness of the fitted measure", "classical Hilbert--Polya or RH"],
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_infinite_phase_operator_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
