#!/usr/bin/env python3
"""Prime-side weight discovery for the Casey/W33 cocycle program.

The Laplace profile from the repaired orbit energy naturally samples prime
powers at x=log(n).  With von Mangoldt weight Lambda(n), the positive prime
sum is

  P(a,d) = sum_{n>=2} Lambda(n) n^{-2a} (n^d-n^{-d})^2.

In its absolute-convergence region a-|d|>1/2 this is the exact second
difference

  L(2(a-d)) - 2 L(2a) + L(2(a+d)),  L(s)=-zeta'(s)/zeta(s).

This is a clean prime analogue of the orbit defect: it is nonnegative term by
term and vanishes at d=0.  It also exposes a hard obstruction.  Casey's
boundary sigma=1 corresponds to a=1/2, where every nonzero d lies outside the
absolute-convergence region.  A classical boundary identity therefore needs
explicit-formula regularization and archimedean/gamma cancellation; the naive
positive prime sum diverges.

The module also tests the simplest prime-indexed W33 moment tower.  A single
damping exponent can match the classical xi quartic ratio but misses the
sextic ratio, providing a falsifiable constraint for the infinite-operator
frontier.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
BRANCH = 11
SECTORS = ((2, 24), (-4, 15))
DAMPING_MATCH_S = mp.mpf("2.21800603941733680576319282566757")


def completed_xi(s: complex | mp.mpc) -> mp.mpc:
    z = mp.mpc(s)
    return (
        mp.mpf("0.5")
        * z
        * (z - 1)
        * mp.power(mp.pi, -z / 2)
        * mp.gamma(z / 2)
        * mp.zeta(z)
    )


def classical_xi_moments(max_power: int = 4) -> dict[int, mp.mpf]:
    mp.mp.dps = 60
    center = mp.mpf("0.5")
    normalizer = completed_xi(center)
    log_xi = lambda z: mp.log(completed_xi(center + z) / normalizer)
    out: dict[int, mp.mpf] = {}
    for k in range(1, max_power + 1):
        derivative = mp.diff(log_xi, 0, 2 * k)
        coefficient = derivative / mp.factorial(2 * k)
        out[2 * k] = ((-1) ** (k + 1)) * k * mp.re(coefficient)
    return out


def log_derivative_dirichlet(s: mp.mpf | float) -> mp.mpf:
    z = mp.mpf(s)
    return -mp.zeta(z, derivative=1) / mp.zeta(z)


def prime_second_difference(a: float, delta: float) -> mp.mpf:
    """Exact convergent prime-power sum through -zeta'/zeta."""
    if a - abs(delta) <= 0.5:
        raise ValueError("absolute convergence requires a-|delta|>1/2")
    return (
        log_derivative_dirichlet(2 * (a - delta))
        - 2 * log_derivative_dirichlet(2 * a)
        + log_derivative_dirichlet(2 * (a + delta))
    )


def von_mangoldt_table(limit: int) -> list[float]:
    if limit < 2:
        raise ValueError("limit must be at least 2")
    table = [0.0] * (limit + 1)
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    for p in range(2, limit + 1):
        if not is_prime[p]:
            continue
        logp = math.log(p)
        power = p
        while power <= limit:
            table[power] = logp
            if power > limit // p:
                break
            power *= p
    return table


def partial_prime_sum(limit: int, a: float, delta: float) -> float:
    vm = von_mangoldt_table(limit)
    total = 0.0
    for n in range(2, limit + 1):
        if vm[n] == 0.0:
            continue
        total += vm[n] * n ** (-2 * a) * (n**delta - n ** (-delta)) ** 2
    return total


def phase_angle(adjacency_eigenvalue: int) -> float:
    return math.acos(adjacency_eigenvalue / (2 * math.sqrt(BRANCH)))


def w33_phase_moments(max_power: int = 4) -> dict[int, float]:
    return {
        2 * k: sum(
            multiplicity / phase_angle(eigenvalue) ** (2 * k)
            for eigenvalue, multiplicity in SECTORS
        )
        for k in range(1, max_power + 1)
    }


def prime_tower_moments(s: mp.mpf | float, max_power: int = 4) -> dict[int, mp.mpf]:
    """Moments of the simplest positive prime-indexed W33 tower.

    The trace weight is Lambda(n)(log n)^2 n^{-s}; local inverse ordinates are
    log(n)/theta_j.  Therefore M_{2k}=T_{2k} L^{(2k+2)}(s).
    """
    z = mp.mpf(s)
    phase = w33_phase_moments(max_power)
    return {
        2 * k: mp.mpf(phase[2 * k]) * mp.diff(log_derivative_dirichlet, z, 2 * k + 2)
        for k in range(1, max_power + 1)
    }


def ratio_invariants(moments: dict[int, mp.mpf | float]) -> dict[str, mp.mpf]:
    s2 = mp.mpf(moments[2])
    return {
        "S4_over_S2_squared": mp.mpf(moments[4]) / s2**2,
        "S6_over_S2_cubed": mp.mpf(moments[6]) / s2**3,
    }


def build_certificate() -> dict[str, Any]:
    mp.mp.dps = 50
    safe_a = 1.0
    safe_delta = 0.2
    exact_prime = prime_second_difference(safe_a, safe_delta)
    partials = {str(limit): partial_prime_sum(limit, safe_a, safe_delta) for limit in (1_000, 10_000, 100_000)}
    boundary_partials = {str(limit): partial_prime_sum(limit, 0.5, 0.1) for limit in (1_000, 10_000, 100_000)}
    classical = classical_xi_moments(3)
    candidate = prime_tower_moments(DAMPING_MATCH_S, 3)
    classical_ratios = ratio_invariants(classical)
    candidate_ratios = ratio_invariants(candidate)
    sextic_relative_error = candidate_ratios["S6_over_S2_cubed"] / classical_ratios["S6_over_S2_cubed"] - 1
    checks = {
        "prime_second_difference_positive": exact_prime > 0,
        "partial_sum_approaches_exact": abs(mp.mpf(partials["100000"]) - exact_prime) < mp.mpf("0.003"),
        "boundary_partial_sums_increase": boundary_partials["1000"] < boundary_partials["10000"] < boundary_partials["100000"],
        "quartic_ratio_matched": abs(candidate_ratios["S4_over_S2_squared"] - classical_ratios["S4_over_S2_squared"]) < mp.mpf("1e-12"),
        "sextic_ratio_rejects_one_damping_model": abs(sextic_relative_error) > mp.mpf("0.1"),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "prime-weight discovery and one-damping W33 tower falsifier",
        "prime_cocycle_identity": {
            "sum": "sum Lambda(n)n^(-2a)(n^delta-n^(-delta))^2",
            "closed_form": "L(2(a-delta))-2L(2a)+L(2(a+delta)), L=-zeta'/zeta",
            "a": safe_a,
            "delta": safe_delta,
            "exact_value": mp.nstr(exact_prime, 30),
            "partial_sums": partials,
            "small_delta_limit": "P(a,delta)/delta^2 -> 4 L''(2a), a positive log-prime-square moment",
        },
        "convergence": {
            "condition": "a-|delta|>1/2",
            "equivalent_sigma_condition": "sigma>1+|delta| because a=sigma-1/2",
            "casey_boundary_sigma_1": "fails for every nonzero delta",
            "boundary_delta_0_1_partial_sums": boundary_partials,
            "interpretation": "the naive positive prime lift cannot be placed directly on sigma=1; explicit-formula regularization is mandatory",
        },
        "single_damping_tower": {
            "definition": "M_2k(s)=T_2k * d^(2k+2)/ds^(2k+2)[-zeta'(s)/zeta(s)]",
            "damping_s_matching_classical_quartic_ratio": mp.nstr(DAMPING_MATCH_S, 30),
            "classical_ratios": {key: mp.nstr(value, 30) for key, value in classical_ratios.items()},
            "candidate_ratios": {key: mp.nstr(value, 30) for key, value in candidate_ratios.items()},
            "sextic_relative_error": mp.nstr(sextic_relative_error, 30),
            "verdict": "prime damping repairs much of the rigid W33 moment mismatch, but one exponent cannot reproduce xi beyond S4",
        },
        "claim_boundary": {
            "proved": [
                "an exact positive von-Mangoldt second-difference identity in its convergence half-plane",
                "the sigma=1 naive sum is outside that convergence half-plane",
                "the one-damping prime tower fails an out-of-sample sextic moment",
            ],
            "not_proved": ["a regularized prime/zero equality at sigma=1", "a unique classical weighting", "an operator determinant equal to xi"],
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_prime_weight_discovery_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
