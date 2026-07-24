#!/usr/bin/env python3
"""Renormalized sigma->1 explicit-formula audit for the Casey cocycle.

Put a=sigma-1/2 and consider the positive prime second difference

  P(a,d)=L(2(a-d))-2L(2a)+L(2(a+d)),  L=-zeta'/zeta.

The Dirichlet series is positive only for a-|d|>1/2 and therefore diverges at
Casey's sigma=1 boundary.  Meromorphic continuation has a canonical finite
part.  Writing epsilon=sigma-1,

  FP_prime(d) = lim_{epsilon->0+} [P(1/2+epsilon,d)+1/epsilon]
              = L(1-2d)+L(1+2d)+2 EulerGamma.

The completed xi logarithmic derivative supplies an archimedean finite part
with the same pole.  Their difference is finite without an arbitrary
subtraction:

  C_xi(d) = H(1-2d)-2H(1)+H(1+2d),  H=-xi'/xi
          = FP_prime(d)-FP_arch(d).

The code verifies the cancellation and scans 0<d<1/2.  The completed quantity
is positive on the sampled grid while the prime finite part is negative.  The
grid observation is a numerical frontier, not a proof of global coercivity.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]


def L(s: mp.mpf | mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return -mp.zeta(z, derivative=1) / mp.zeta(z)


def archimedean_A(s: mp.mpf | mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return 1 / z + 1 / (z - 1) - mp.log(mp.pi) / 2 + mp.digamma(z / 2) / 2


def archimedean_constant_at_one() -> mp.mpf:
    return 1 - mp.log(mp.pi) / 2 - mp.euler / 2 - mp.log(2)


def completed_H_at_one() -> mp.mpf:
    return -1 + mp.log(mp.pi) / 2 + mp.log(2) - mp.euler / 2


def completed_H(s: mp.mpf | mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    if abs(z - 1) < mp.mpf("1e-35"):
        return mp.mpc(completed_H_at_one())
    return L(z) - archimedean_A(z)


def prime_finite_part(delta: mp.mpf) -> mp.mpf:
    return mp.re(L(1 - 2 * delta) + L(1 + 2 * delta) + 2 * mp.euler)


def archimedean_finite_part(delta: mp.mpf) -> mp.mpf:
    a0 = archimedean_constant_at_one()
    return mp.re(
        archimedean_A(1 - 2 * delta)
        + archimedean_A(1 + 2 * delta)
        - 2 * a0
    )


def completed_finite_part(delta: mp.mpf) -> mp.mpf:
    return prime_finite_part(delta) - archimedean_finite_part(delta)


def completed_direct_difference(delta: mp.mpf) -> mp.mpf:
    h1 = completed_H_at_one()
    return mp.re(completed_H(1 - 2 * delta) - 2 * h1 + completed_H(1 + 2 * delta))


def epsilon_second_differences(epsilon: mp.mpf, delta: mp.mpf) -> dict[str, mp.mpf]:
    center = 1 + 2 * epsilon
    prime = mp.re(L(center - 2 * delta) - 2 * L(center) + L(center + 2 * delta))
    arch = mp.re(
        archimedean_A(center - 2 * delta)
        - 2 * archimedean_A(center)
        + archimedean_A(center + 2 * delta)
    )
    return {
        "prime_plus_counterterm": prime + 1 / epsilon,
        "arch_plus_counterterm": arch + 1 / epsilon,
        "completed_no_counterterm": prime - arch,
    }


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 70
    grid = [mp.mpf(i) / 1000 for i in range(1, 490)]
    prime_values = [prime_finite_part(delta) for delta in grid]
    arch_values = [archimedean_finite_part(delta) for delta in grid]
    completed_values = [completed_finite_part(delta) for delta in grid]
    ratios = [value / delta**2 for value, delta in zip(completed_values, grid)]

    delta_test = mp.mpf("0.2")
    epsilon_rows = []
    for epsilon in (mp.mpf("1e-2"), mp.mpf("1e-4"), mp.mpf("1e-6"), mp.mpf("1e-8")):
        row = epsilon_second_differences(epsilon, delta_test)
        epsilon_rows.append(
            {
                "epsilon": mp.nstr(epsilon, 8),
                **{key: mp.nstr(value, 30) for key, value in row.items()},
            }
        )

    samples = {}
    for value in ("0.001", "0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.489"):
        delta = mp.mpf(value)
        samples[value] = {
            "prime_finite_part": mp.nstr(prime_finite_part(delta), 30),
            "archimedean_finite_part": mp.nstr(archimedean_finite_part(delta), 30),
            "completed_finite_part": mp.nstr(completed_finite_part(delta), 30),
            "completed_over_delta_squared": mp.nstr(completed_finite_part(delta) / delta**2, 30),
        }

    direct_errors = [
        abs(completed_finite_part(delta) - completed_direct_difference(delta))
        for delta in grid[::37]
    ]
    target_prime = prime_finite_part(delta_test)
    target_arch = archimedean_finite_part(delta_test)
    target_completed = completed_finite_part(delta_test)
    last_epsilon = epsilon_second_differences(mp.mpf("1e-8"), delta_test)

    checks = {
        "finite_part_decomposition_exact": max(direct_errors) < mp.mpf("1e-55"),
        "prime_counterterm_converges": abs(last_epsilon["prime_plus_counterterm"] - target_prime) < mp.mpf("3e-7"),
        "arch_counterterm_converges": abs(last_epsilon["arch_plus_counterterm"] - target_arch) < mp.mpf("3e-7"),
        "completed_difference_converges_without_counterterm": abs(last_epsilon["completed_no_counterterm"] - target_completed) < mp.mpf("3e-12"),
        "prime_finite_part_negative_on_grid": max(prime_values) < 0,
        "archimedean_finite_part_more_negative_on_grid": all(arch < prime for arch, prime in zip(arch_values, prime_values)),
        "completed_finite_part_positive_on_grid": min(completed_values) > 0,
        "completed_quadratic_ratio_stable_on_grid": max(ratios) - min(ratios) < mp.mpf("1e-5"),
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "Hadamard finite-part boundary formula retaining prime and archimedean terms",
        "constants": {
            "a0_archimedean": mp.nstr(archimedean_constant_at_one(), 40),
            "H_1_minus_xi_log_derivative": mp.nstr(completed_H_at_one(), 40),
        },
        "finite_part_theorem": {
            "prime": "FP_P(d)=L(1-2d)+L(1+2d)+2 EulerGamma",
            "archimedean": "FP_A(d)=A(1-2d)+A(1+2d)-2a0",
            "completed": "C_xi(d)=FP_P(d)-FP_A(d)=H(1-2d)-2H(1)+H(1+2d)",
            "counterterm": "+1/epsilon separately renormalizes both prime and archimedean second differences",
            "cancellation": "the completed difference requires no counterterm because the two poles cancel",
        },
        "epsilon_convergence_delta_0_2": epsilon_rows,
        "grid": {
            "delta_range": "0.001 through 0.489 in steps of 0.001",
            "sample_count": len(grid),
            "prime_min": mp.nstr(min(prime_values), 30),
            "prime_max": mp.nstr(max(prime_values), 30),
            "arch_min": mp.nstr(min(arch_values), 30),
            "arch_max": mp.nstr(max(arch_values), 30),
            "completed_min": mp.nstr(min(completed_values), 30),
            "completed_max": mp.nstr(max(completed_values), 30),
            "completed_over_delta_squared_min": mp.nstr(min(ratios), 30),
            "completed_over_delta_squared_max": mp.nstr(max(ratios), 30),
        },
        "samples": samples,
        "interpretation": {
            "prime_only": "canonical finite-part continuation is negative and loses the raw Dirichlet-series positivity",
            "archimedean_role": "gamma and endpoint terms contribute a slightly more negative finite part",
            "completed_result": "their difference is positive on the full sampled defect interval and behaves quadratically near zero",
        },
        "claim_boundary": {
            "proved": [
                "the exact finite-part decomposition and pole cancellation",
                "the raw positive prime series cannot be continued to sigma=1 without renormalization",
            ],
            "numerically_certified": [
                "positivity of the completed finite part on 489 sampled defects",
                "stable quadratic scaling C_xi(delta)/delta^2 on that interval",
            ],
            "not_proved": [
                "analytic positivity for every 0<|delta|<1/2",
                "equality of this one-orbit finite part with a total zero-defect sum",
                "classical RH",
            ],
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_renormalized_boundary_formula_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
