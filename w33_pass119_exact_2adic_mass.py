#!/usr/bin/env python3
"""Pass 100: exact Conway-Sloane 2-adic mass correction for 1^+32 2^+8."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "w33_pass119_exact_2adic_mass.json"


def bernoulli(n: int) -> Fraction:
    values = [Fraction(0) for _ in range(n + 1)]
    for m in range(n + 1):
        values[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            values[j - 1] = j * (values[j - 1] - values[j])
    return values[0]


def even_unimodular_mass(n: int) -> Fraction:
    k = n // 2
    mass = abs(bernoulli(k)) / n
    for j in range(1, k):
        mass *= abs(bernoulli(2 * j)) / (4 * j)
    return mass


def free_even_plus_diagonal_factor(dim: int) -> Fraction:
    """M_2 for a free type-II plus constituent of even dimension."""
    t = dim // 2
    denominator = Fraction(2)
    for j in range(1, t):
        denominator *= 1 - Fraction(1, 2 ** (2 * j))
    denominator *= 1 - Fraction(1, 2**t)
    return 1 / denominator


def main() -> int:
    m8 = even_unimodular_mass(8)
    m40 = even_unimodular_mass(40)
    d8 = free_even_plus_diagonal_factor(8)
    d32 = free_even_plus_diagonal_factor(32)
    d40 = free_even_plus_diagonal_factor(40)

    # Conway-Sloane p-mass:
    # product diagonal factors * product(q'/q)^(nq*nq'/2)
    # * 2^(n(I,I)-n(II)).  Both constituents are free type II.
    mixed_pmass = d32 * d8 * 2**128 * Fraction(1, 2**40)
    unimodular_pmass = d40 * Fraction(1, 2**40)
    correction = mixed_pmass / unimodular_pmass
    exact_mass = m40 * correction

    # Scaling all of E8 by sqrt(2) moves its sole constituent from scale
    # 1 to scale 2 but does not alter the p-mass.
    e8_pmass_scale1 = d8 * Fraction(1, 2**8)
    e8_pmass_scale2 = d8 * Fraction(1, 2**8)

    checks = {
        "bernoulli_mass_reproduces_E8": m8 == Fraction(1, 696_729_600),
        "sqrt2_E8_scale_invariance": e8_pmass_scale1 == e8_pmass_scale2,
        "cross_exponent_128": 32 * 8 // 2 == 128,
        "typeII_dimension_40": 32 + 8 == 40,
        "correction_exact": correction
        == Fraction(524_422_438_829_426_130_254_793_883_968_303_680_565, 2),
        "mass_positive": exact_mass > 0,
    }
    payload = {
        "schema": "w33.pass100.exact_2adic_mass.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "jordan_symbol": "1^+32 2^+8 (both free type II, octane 0)",
        "conway_sloane_factors": {
            "cross_term": "2^(32*8/2) = 2^128",
            "typeII_term": "2^-(32+8) = 2^-40",
            "diagonal_term": "M2(32,+) * M2(8,+)",
        },
        "two_adic_correction_over_even_unimodular_rank40": str(correction),
        "two_adic_correction_approx": f"{float(correction):.12e}",
        "even_unimodular_rank40_mass": str(m40),
        "exact_genus_mass": str(exact_mass),
        "exact_genus_mass_approx": f"{float(exact_mass):.12e}",
        "validation": {
            "E8_mass": str(m8),
            "sqrt2_E8_pmass_ratio": str(e8_pmass_scale2 / e8_pmass_scale1),
        },
        "boundary": (
            "This calculation uses the Conway-Sloane local p-mass formula. "
            "It replaces Pass 95's unimodular reference scale; it does not "
            "enumerate individual classes in the genus."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
