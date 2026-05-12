#!/usr/bin/env python3
"""
PART_CCCCCXLVI_ac_moment_coupling.py

Executable verifier for Part CCCCCXLVI: the almost-commutative
moment-coupling theorem.

Theorem:
    If D_tot = D_ext tensor 1 + gamma_ext tensor D_F with gamma_ext D_ext
    + D_ext gamma_ext = 0, then

        D_tot^2 = D_ext^2 tensor 1 + 1 tensor D_F^2
        K_tot(t) = K_ext(t) K_int(t)

    If K_ext(t) ~ sum_m a_{2m}^{ext} t^{m-2} and
       K_int(t) = sum_l (-1)^l mu_l t^l/l!,
    then

        A_{2r}^{tot} = sum_{l=0}^r (-1)^l mu_l a_{2(r-l)}^{ext}/l!.

For the W(3,3) vertex-space internal Laplacian L_W = 12I - A:
    Spec(L_W) = 0^1, 10^24, 16^15
    mu_0 = 40
    mu_l = 24*10^l + 15*16^l for l >= 1
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction
from math import exp
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MomentCouplingResult:
    part: str
    title: str
    internal_spectrum: dict[str, int]
    moments: dict[str, str]
    taylor_coefficients: dict[str, str]
    convolution_coefficients: dict[str, dict[str, str]]
    flat_torus_leading_example: dict[str, str]
    factorization_check: dict[str, Any]
    checks: dict[str, bool]
    all_checks_pass: bool


def internal_eigenvalues() -> list[int]:
    return [0] + [10] * 24 + [16] * 15


def moment(power: int) -> int:
    eigs = internal_eigenvalues()
    return sum(lam ** power for lam in eigs)


def moments(max_power: int) -> dict[int, int]:
    return {p: moment(p) for p in range(max_power + 1)}


def factorial(n: int) -> int:
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def taylor_coeff(power: int) -> Fraction:
    return Fraction(((-1) ** power) * moment(power), factorial(power))


def convolution_coefficients(max_r: int) -> dict[int, dict[str, Fraction]]:
    """Return A_{2r}^{tot} as coefficients of external a_{2j}."""
    out: dict[int, dict[str, Fraction]] = {}
    for r in range(max_r + 1):
        terms: dict[str, Fraction] = {}
        for ell in range(r + 1):
            external_index = 2 * (r - ell)
            terms[f"a{external_index}_ext"] = taylor_coeff(ell)
        out[2 * r] = terms
    return out


def frac_to_string(x: Fraction | int) -> str:
    if isinstance(x, int):
        return str(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def numeric_heat_internal(t: float) -> float:
    return sum(exp(-t * lam) for lam in internal_eigenvalues())


def finite_factorization_check() -> dict[str, Any]:
    """
    Check K_tot = K_ext K_int for a finite mock external spectrum.
    This is a finite spectral model of the AC Kronecker-sum trace identity.
    """
    ext_eigs = [0, 1, 1, 4, 4, 9]
    int_eigs = internal_eigenvalues()
    samples = []
    ok = True
    for t in [Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)]:
        tf = float(t)
        k_ext = sum(exp(-tf * x) for x in ext_eigs)
        k_int = sum(exp(-tf * y) for y in int_eigs)
        k_product = k_ext * k_int
        k_total = sum(exp(-tf * (x + y)) for x in ext_eigs for y in int_eigs)
        err = abs(k_product - k_total)
        samples.append({
            "t": frac_to_string(t),
            "K_ext*K_int": f"{k_product:.15g}",
            "K_total_direct": f"{k_total:.15g}",
            "abs_error": f"{err:.3e}",
        })
        ok = ok and err < 1e-10
    return {
        "external_mock_spectrum": ext_eigs,
        "internal_spectrum_summary": {"0": 1, "10": 24, "16": 15},
        "samples": samples,
        "passed": ok,
        "interpretation": "Finite Kronecker-sum heat trace exactly factorizes; numerical error is floating roundoff.",
    }


def flat_torus_leading_example(max_r: int) -> dict[str, str]:
    """
    Leading flat 4-torus example: external K_ext ~ 4V(4pi)^-2 t^-2.
    Coefficients shown as multiples of V/(4pi)^2.
    """
    # If a0_ext = 4 V/(4pi)^2 and a_{>0}=0, then A_{2r}=c_r a0_ext.
    example = {}
    for r in range(max_r + 1):
        c = taylor_coeff(r) * 4
        example[f"A{2*r}_tot_multiplier_of_V_over_4pi_squared"] = frac_to_string(c)
    return example


def build_result(max_power: int = 8) -> MomentCouplingResult:
    moms = moments(max_power)
    tay = {str(i): frac_to_string(taylor_coeff(i)) for i in range(max_power + 1)}
    conv_raw = convolution_coefficients(max_power)
    conv = {
        f"A{r}_tot": {k: frac_to_string(v) for k, v in terms.items()}
        for r, terms in conv_raw.items()
    }
    fact = finite_factorization_check()

    checks = {
        "mu0_40": moms[0] == 40,
        "mu1_480": moms[1] == 480,
        "mu2_6240": moms[2] == 6240,
        "mu3_85440": moms[3] == 85440,
        "mu4_1223040": moms[4] == 1223040,
        "taylor_c0_40": taylor_coeff(0) == Fraction(40),
        "taylor_c1_minus480": taylor_coeff(1) == Fraction(-480),
        "taylor_c2_3120": taylor_coeff(2) == Fraction(3120),
        "taylor_c3_minus14240": taylor_coeff(3) == Fraction(-14240),
        "taylor_c4_50960": taylor_coeff(4) == Fraction(50960),
        "convolution_A4_has_3120_a0": conv_raw[4]["a0_ext"] == Fraction(3120),
        "convolution_A4_has_minus480_a2": conv_raw[4]["a2_ext"] == Fraction(-480),
        "convolution_A4_has_40_a4": conv_raw[4]["a4_ext"] == Fraction(40),
        "factorization_numeric": bool(fact["passed"]),
    }

    return MomentCouplingResult(
        part="CCCCCXLVI",
        title="Almost-Commutative Moment-Coupling Theorem",
        internal_spectrum={"0": 1, "10": 24, "16": 15},
        moments={str(k): str(v) for k, v in moms.items()},
        taylor_coefficients=tay,
        convolution_coefficients=conv,
        flat_torus_leading_example=flat_torus_leading_example(8),
        factorization_check=fact,
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = build_result()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "one or more moment-coupling checks failed"

    out = Path("data/PART_CCCCCXLVI_ac_moment_coupling_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
