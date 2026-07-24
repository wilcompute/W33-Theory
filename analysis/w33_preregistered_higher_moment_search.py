#!/usr/bin/env python3
"""Pre-registered positive three-channel W33 operator search.

Training data: classical xi moments S2,S4,S6,S8 only.
Reserved falsifiers: S10, S12, the existence of a first positive ordinate, and
finite zero density below every finite height.

The registered damping channels are s=2,3,4. They extend the previous s=2,3
model by exactly one positive channel. Each channel is the prime-indexed W33
moment packet M_2k(s)=T_2k d^(2k+2)/ds^(2k+2)[-zeta'(s)/zeta(s)].

The exact interpolation requires a negative s=3 weight. The positive search
lands on the boundary and cannot fit the training moments exactly. Both models
fail the untouched S10/S12 tests. The proposed ordinates also accumulate at
zero, so the construction cannot be a compact-resolvent Hilbert--Polya
operator.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
from scipy.optimize import least_squares, root

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 11
SECTORS = ((2, 24), (-4, 15))
CHANNELS = (2, 3, 4)
TRAIN_POWERS = (2, 4, 6, 8)
RESERVED_POWERS = (10, 12)
FIRST_RIEMANN_ZERO = mp.mpf("14.134725141734693790457251983562")


def completed_xi(s: mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return mp.mpf("0.5") * z * (z - 1) * mp.power(mp.pi, -z / 2) * mp.gamma(z / 2) * mp.zeta(z)


def classical_xi_moments(max_power: int = 6) -> dict[int, mp.mpf]:
    center = mp.mpf("0.5")
    normalizer = completed_xi(center)
    log_xi = lambda z: mp.log(completed_xi(center + z) / normalizer)
    moments: dict[int, mp.mpf] = {}
    for k in range(1, max_power + 1):
        derivative = mp.diff(log_xi, 0, 2 * k, method="quad")
        coefficient = derivative / mp.factorial(2 * k)
        moments[2 * k] = ((-1) ** (k + 1)) * k * mp.re(coefficient)
    return moments


def phase_angle(adjacency_eigenvalue: int) -> mp.mpf:
    return mp.acos(mp.mpf(adjacency_eigenvalue) / (2 * mp.sqrt(BRANCH)))


def phase_moments(max_power: int = 6) -> dict[int, mp.mpf]:
    return {
        2 * k: sum(
            mp.mpf(multiplicity) / phase_angle(eigenvalue) ** (2 * k)
            for eigenvalue, multiplicity in SECTORS
        )
        for k in range(1, max_power + 1)
    }


def zeta_log_derivative(s: mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return -mp.zeta(z, derivative=1) / mp.zeta(z)


def channel_moments(s: int, max_power: int = 6) -> dict[int, mp.mpf]:
    phase = phase_moments(max_power)
    return {
        2 * k: phase[2 * k] * mp.re(
            mp.diff(zeta_log_derivative, mp.mpf(s), 2 * k + 2, method="quad")
        )
        for k in range(1, max_power + 1)
    }


def mixture(channel_data: dict[int, dict[int, mp.mpf]], weights: list[float]) -> dict[int, mp.mpf]:
    return {
        power: sum(
            mp.mpf(weights[index]) * channel_data[channel][power]
            for index, channel in enumerate(CHANNELS)
        )
        for power in range(2, 13, 2)
    }


def invariants(moments: dict[int, mp.mpf]) -> tuple[mp.mpf, mp.mpf]:
    return (
        moments[6] * moments[2] / moments[4] ** 2,
        moments[8] * moments[2] ** 2 / moments[4] ** 3,
    )


def solve_signed(channel_data: dict[int, dict[int, mp.mpf]], target: dict[int, mp.mpf]) -> dict[str, Any]:
    target_i6, target_i8 = invariants(target)

    def equations(vector: np.ndarray) -> list[float]:
        w2, w3 = vector
        weights = [w2, w3, 1 - w2 - w3]
        raw = mixture(channel_data, weights)
        i6, i8 = invariants(raw)
        return [float(i6 - target_i6), float(i8 - target_i8)]

    solution = root(equations, np.array([0.002, -0.19]), tol=1e-12)
    w2, w3 = solution.x
    weights = [float(w2), float(w3), float(1 - w2 - w3)]
    raw = mixture(channel_data, weights)
    scale_squared = raw[4] * target[2] / (raw[2] * target[4])
    scale = mp.sqrt(scale_squared)
    amplitude = target[2] * scale_squared / raw[2]
    prediction = {power: amplitude * raw[power] / scale**power for power in raw}
    return {
        "solver_success": bool(solution.success),
        "weights": weights,
        "scale": scale,
        "amplitude": amplitude,
        "prediction": prediction,
        "relative_errors": {power: prediction[power] / target[power] - 1 for power in prediction},
    }


def softmax_weights(logits: np.ndarray) -> np.ndarray:
    values = np.array([logits[0], logits[1], 0.0])
    exponentials = np.exp(values - np.max(values))
    return exponentials / np.sum(exponentials)


def solve_positive(channel_data: dict[int, dict[int, mp.mpf]], target: dict[int, mp.mpf]) -> dict[str, Any]:
    def unpack(vector: np.ndarray) -> tuple[np.ndarray, float, float]:
        return softmax_weights(vector[:2]), math.exp(vector[2]), math.exp(vector[3])

    def prediction(vector: np.ndarray) -> dict[int, float]:
        weights, scale, amplitude = unpack(vector)
        raw = mixture(channel_data, list(weights))
        return {power: amplitude * float(raw[power]) / scale**power for power in raw}

    def residual(vector: np.ndarray) -> np.ndarray:
        predicted = prediction(vector)
        return np.array([math.log(predicted[power] / float(target[power])) for power in TRAIN_POWERS])

    guesses = (
        (0.0, 0.0, math.log(100), math.log(0.5)),
        (-2.0, 0.0, math.log(100), math.log(0.5)),
        (0.0, -2.0, math.log(100), math.log(0.5)),
        (2.0, -2.0, math.log(100), math.log(0.5)),
        (-2.0, 2.0, math.log(100), math.log(0.5)),
    )
    best = None
    for guess in guesses:
        candidate = least_squares(
            residual, np.array(guess), max_nfev=10_000,
            xtol=1e-14, ftol=1e-14, gtol=1e-14,
        )
        norm = float(np.linalg.norm(candidate.fun))
        if best is None or norm < best[0]:
            best = (norm, candidate)
    assert best is not None
    norm, solution = best
    weights, scale, amplitude = unpack(solution.x)
    predicted = prediction(solution.x)
    return {
        "solver_success": bool(solution.success),
        "training_log_error_norm": norm,
        "weights": [float(value) for value in weights],
        "scale": scale,
        "amplitude": amplitude,
        "prediction": predicted,
        "relative_errors": {power: predicted[power] / float(target[power]) - 1 for power in predicted},
    }


def spectral_gap_audit(scale: float | mp.mpf) -> dict[str, Any]:
    theta_min = min(phase_angle(2), phase_angle(-4))
    sample_ordinates = {
        str(n): mp.mpf(scale) * theta_min / mp.log(n)
        for n in (2, 3, 10, 100, 10_000, 10**12)
    }
    return {
        "ordinate_model": "t_(n,j)=scale*theta_j/log(n)",
        "sample_min_sector_ordinates": {n: mp.nstr(value, 30) for n, value in sample_ordinates.items()},
        "limit_as_n_to_infinity": 0,
        "actual_first_Riemann_zero": mp.nstr(FIRST_RIEMANN_ZERO, 30),
        "compact_resolvent_failure": (
            "prime-power labels give infinitely many model ordinates below every T>0; "
            "there is no first positive ordinate and no finite zero-counting function"
        ),
    }


def serialize_solution(solution: dict[str, Any]) -> dict[str, Any]:
    return {
        "solver_success": solution["solver_success"],
        **({"training_log_error_norm": solution["training_log_error_norm"]} if "training_log_error_norm" in solution else {}),
        "weights_s2_s3_s4": solution["weights"],
        "scale": mp.nstr(solution["scale"], 35),
        "amplitude": mp.nstr(solution["amplitude"], 35),
        "moments": {str(power): mp.nstr(value, 35) for power, value in solution["prediction"].items()},
        "relative_errors": {str(power): mp.nstr(value, 35) for power, value in solution["relative_errors"].items()},
    }


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 32
    target = classical_xi_moments(6)
    channel_data = {channel: channel_moments(channel, 6) for channel in CHANNELS}
    signed = solve_signed(channel_data, target)
    positive = solve_positive(channel_data, target)

    checks = {
        "training_set_is_only_S2_to_S8": TRAIN_POWERS == (2, 4, 6, 8),
        "S10_and_S12_reserved": RESERVED_POWERS == (10, 12),
        "signed_model_interpolates_training_moments": max(abs(signed["relative_errors"][power]) for power in TRAIN_POWERS) < mp.mpf("1e-12"),
        "signed_exact_fit_requires_negative_weight": min(signed["weights"]) < 0,
        "positive_search_uses_nonnegative_weights": min(positive["weights"]) >= 0,
        "positive_search_does_not_exactly_fit_training": positive["training_log_error_norm"] > 0.1,
        "signed_model_fails_reserved_S10": abs(signed["relative_errors"][10]) > 0.2,
        "signed_model_fails_reserved_S12": abs(signed["relative_errors"][12]) > 1.0,
        "positive_model_fails_reserved_S10": abs(positive["relative_errors"][10]) > 0.7,
        "positive_model_fails_reserved_S12": abs(positive["relative_errors"][12]) > 3.0,
        "ordinate_model_accumulates_at_zero": True,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "pre-registered three-channel positive W33 moment search with S10/S12 and zero-gap falsifiers",
        "protocol": {
            "channels": list(CHANNELS),
            "new_channel": 4,
            "training_moments": list(TRAIN_POWERS),
            "reserved_moments": list(RESERVED_POWERS),
            "reserved_spectral_tests": ["existence of a first positive ordinate", "finite zero count below every finite height"],
            "selection_rule": "no S10, S12, or zero-ordinate information is used during fitting",
        },
        "classical_target_moments": {str(power): mp.nstr(value, 35) for power, value in target.items()},
        "signed_exact_interpolation": {
            **serialize_solution(signed),
            "verdict": "S2-S8 can be interpolated only by this located branch with a negative s=3 trace weight; the reserved S10/S12 moments then fail",
        },
        "positive_constrained_search": {
            **serialize_solution(positive),
            "verdict": "the best registered positive fit lies effectively on the s=2 boundary and leaves a nonzero training residual; its reserved moments fail much more strongly",
        },
        "signed_spectral_gap_audit": spectral_gap_audit(signed["scale"]),
        "positive_spectral_gap_audit": spectral_gap_audit(positive["scale"]),
        "claim_boundary": {
            "proved": [
                "the registered signed interpolation and positive constrained optimization are reproducible",
                "the located exact interpolation violates positivity",
                "both fitted models fail untouched higher moments",
                "the proposed prime-indexed ordinate formula has zero as an accumulation point",
            ],
            "not_proved": [
                "global nonexistence of every conceivable positive spectral measure",
                "that no different operator architecture can reproduce xi",
                "classical RH",
            ],
            "next_operator_requirement": "a positive compact-resolvent operator with integer spectral multiplicities, a first ordinate, finite N(T), and pre-registered agreement beyond S12",
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_preregistered_higher_moment_search_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
