#!/usr/bin/env python3
"""Orbit-level Weil/Laplace positivity for the repaired Casey cocycle.

This module makes one precise bridge and one precise limitation.

For a reflected zero orbit

    rho = 1/2 + delta + i gamma,
    rho* = 1/2 - delta + i gamma,

and a vertical boundary sigma = 1/2 + a with a > |delta|, the repaired
reflection-cocycle current has squared energy

    E(a,delta) = pi delta^2 / (a (a^2-delta^2)).

The same number is a positive Laplace/Hardy quadratic form:

    E/pi = || exp(-(a-delta)x) - exp(-(a+delta)x) ||^2_{L^2(0,infinity)}.

Equivalently, it is the quadratic form of the Cauchy Gram kernel
K(c,d)=1/(c+d) on the two exponentials.  This removes orbit-by-orbit
cancellation and proves that a convergent sum of these energies vanishes iff
every included orbit lies on Re(s)=1/2.

This is an RH-equivalent detector after a classical zero-set convergence and
weighting theorem is supplied.  It is not, by itself, the full Weil explicit
formula or a proof that the classical total energy is zero.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Iterable

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]


def cocycle_current(a: float, delta: float, y: float) -> float:
    """Reflection-cocycle current at y=t-gamma.

    The overall sign is immaterial for the squared energy.  Here we use

        y/((a+delta)^2+y^2) - y/((a-delta)^2+y^2).
    """
    if a <= abs(delta):
        raise ValueError("require a>|delta|")
    return y / ((a + delta) ** 2 + y * y) - y / (
        (a - delta) ** 2 + y * y
    )


def closed_energy(a: float, delta: float) -> float:
    if a <= abs(delta):
        raise ValueError("require a>|delta|")
    return math.pi * delta * delta / (a * (a * a - delta * delta))


def laplace_profile(a: float, delta: float, x: float) -> float:
    if a <= abs(delta) or x < 0:
        raise ValueError("require a>|delta| and x>=0")
    return math.exp(-(a - delta) * x) - math.exp(-(a + delta) * x)


def laplace_norm_closed(a: float, delta: float) -> float:
    """pi times the exact L2 norm squared of the Laplace profile."""
    return closed_energy(a, delta)


def numerical_current_energy(a: float, delta: float) -> mp.mpf:
    f = lambda y: cocycle_current(a, delta, float(y)) ** 2
    return mp.quad(f, [-mp.inf, 0, mp.inf])


def numerical_laplace_energy(a: float, delta: float) -> mp.mpf:
    f = lambda x: mp.pi * laplace_profile(a, delta, float(x)) ** 2
    return mp.quad(f, [0, mp.inf])


def cauchy_gram(a: float, delta: float) -> tuple[tuple[float, float], ...]:
    """Gram matrix of exp(-(a-delta)x), exp(-(a+delta)x) in L2(0,infinity)."""
    if a <= abs(delta):
        raise ValueError("require a>|delta|")
    return (
        (1 / (2 * (a - delta)), 1 / (2 * a)),
        (1 / (2 * a), 1 / (2 * (a + delta))),
    )


def gram_determinant(a: float, delta: float) -> float:
    g = cauchy_gram(a, delta)
    return g[0][0] * g[1][1] - g[0][1] * g[1][0]


def gram_difference_energy(a: float, delta: float) -> float:
    """pi * (1,-1) G (1,-1)^T."""
    g = cauchy_gram(a, delta)
    q = g[0][0] + g[1][1] - 2 * g[0][1]
    return math.pi * q


def finite_orbit_energy(
    deltas: Iterable[float], a: float = 0.5, weights: Iterable[float] | None = None
) -> float:
    ds = list(deltas)
    ws = [1.0] * len(ds) if weights is None else list(weights)
    if len(ds) != len(ws):
        raise ValueError("deltas and weights must have the same length")
    if any(w < 0 for w in ws):
        raise ValueError("weights must be nonnegative")
    return sum(w * closed_energy(a, d) for d, w in zip(ds, ws))


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 50
    samples = ((0.5, 0.0), (0.5, 0.05), (0.7, -0.12), (1.0, 0.2))
    identities = []
    max_current_error = mp.mpf("0")
    max_laplace_error = mp.mpf("0")
    max_gram_error = 0.0

    for a, delta in samples:
        exact = closed_energy(a, delta)
        current = numerical_current_energy(a, delta)
        laplace = numerical_laplace_energy(a, delta)
        gram = gram_difference_energy(a, delta)
        max_current_error = max(max_current_error, abs(current - exact))
        max_laplace_error = max(max_laplace_error, abs(laplace - exact))
        max_gram_error = max(max_gram_error, abs(gram - exact))
        identities.append(
            {
                "a": a,
                "delta": delta,
                "closed_energy": exact,
                "current_integral": mp.nstr(current, 30),
                "laplace_integral": mp.nstr(laplace, 30),
                "gram_energy": gram,
                "gram_determinant": gram_determinant(a, delta),
            }
        )

    critical = finite_orbit_energy([0.0, 0.0, 0.0], a=0.5)
    off_line = finite_orbit_energy([0.0, 0.05, -0.12, 0.2], a=0.5)
    weighted_off_line = finite_orbit_energy(
        [0.0, 0.05, -0.12], a=0.5, weights=[3.0, 2.0, 5.0]
    )

    checks = {
        "current_parseval_identity": max_current_error < mp.mpf("1e-10"),
        "laplace_norm_identity": max_laplace_error < mp.mpf("1e-10"),
        "cauchy_gram_identity": max_gram_error < 1e-12,
        "gram_psd": all(item["gram_determinant"] >= -1e-14 for item in identities),
        "energy_zero_on_line": critical == 0.0,
        "energy_positive_for_off_line_orbit": off_line > 0.0,
        "positive_weights_preserve_detection": weighted_off_line > 0.0,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "orbit-level Weil/Laplace positivity for Casey reflection cocycle",
        "theorem": {
            "current_energy": "integral_R A(a,delta,y)^2 dy = pi*delta^2/[a(a^2-delta^2)]",
            "laplace_form": (
                "E/pi = integral_0^inf (exp(-(a-delta)x)-exp(-(a+delta)x))^2 dx"
            ),
            "gram_form": "E/pi = (1,-1) K (1,-1)^T, K_ij=1/(c_i+c_j)",
            "finite_equivalence": (
                "for nonnegative weights and a finite orbit set, total E=0 iff every delta=0"
            ),
        },
        "fourier_interpretation": {
            "transform": (
                "A_hat(omega)=i*pi*sgn(omega)*[exp(-(a-delta)|omega|)-exp(-(a+delta)|omega|)]"
            ),
            "meaning": (
                "the repaired torque is the boundary Fourier image of a positive Laplace-space difference"
            ),
        },
        "samples": identities,
        "finite_orbit_examples": {
            "all_on_line": critical,
            "contains_off_line_orbits": off_line,
            "weighted_contains_off_line_orbit": weighted_off_line,
        },
        "claim_boundary": {
            "proved": (
                "an orbit-level positive quadratic form exactly detects horizontal displacement"
            ),
            "not_proved": (
                "that the full Weil explicit-formula quadratic form equals this orbit sum, or that the classical total vanishes"
            ),
            "next_transfer": (
                "identify an admissible test-function family and convergent zero/prime weighting that turns the classical Weil form into this cocycle norm"
            ),
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_weil_cocycle_positivity_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
