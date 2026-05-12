#!/usr/bin/env python3
"""
PART_CCCCCLXVI_dimensional_normalization.py

Executable artifact for Part CCCCCLXVI.

This script adds the missing dimensional normalization to the W(3,3)
240-carrier spectral action extraction.

Part CCCCCLXV used the dimensionless cellular 1-Laplacian spectrum

    Spec(Delta_1) = 0^81, 4^120, 10^24, 16^15.

For a physical almost-commutative Dirac operator we introduce an internal
mass scale M_F and use

    D_F^2 = M_F^2 Delta_1.

The expansion is then controlled by x = M_F^2 / Lambda^2.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Any

SPECTRUM = {0: 81, 4: 120, 10: 24, 16: 15}
MAX_ORDER = 8


@dataclass(frozen=True)
class DimensionalNormalizationResult:
    part: str
    title: str
    dimensionless_spectrum: dict[str, int]
    dimensionful_operator: dict[str, str]
    dimensionless_moments: dict[str, str]
    scaled_moments: dict[str, str]
    scaled_taylor_coefficients: dict[str, str]
    normalized_polynomial_coefficients: dict[str, str]
    convolution_coefficients: dict[str, dict[str, str]]
    sector_ledgers: dict[str, Any]
    checks: dict[str, bool]
    all_checks_pass: bool


def factorial(n: int) -> int:
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def moment(power: int) -> int:
    if power == 0:
        return sum(SPECTRUM.values())
    return sum(mult * eig**power for eig, mult in SPECTRUM.items())


def taylor_coeff(power: int) -> Fraction:
    return Fraction(((-1) ** power) * moment(power), factorial(power))


def frac_to_str(x: Fraction | int) -> str:
    if isinstance(x, int):
        return str(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def mf_power(power: int) -> str:
    if power == 0:
        return "1"
    if power == 1:
        return "M_F^2"
    return f"M_F^{2 * power}"


def scaled_term(coeff: Fraction, power: int) -> str:
    c = frac_to_str(coeff)
    p = mf_power(power)
    if p == "1":
        return c
    if c == "1":
        return p
    if c == "-1":
        return f"-{p}"
    return f"{c} {p}"


def normalized_poly_coeff(power: int) -> Fraction:
    return Fraction(taylor_coeff(power), 240)


def convolution(max_r: int = MAX_ORDER) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for r in range(max_r + 1):
        terms: dict[str, str] = {}
        for ell in range(r + 1):
            terms[f"a{2 * (r - ell)}_ext"] = scaled_term(taylor_coeff(ell), ell)
        out[f"A{2 * r}_tot(M_F)"] = terms
    return out


def polynomial(n: int) -> list[str]:
    return [f"{frac_to_str(normalized_poly_coeff(k))} x^{k}" if k else "1" for k in range(n + 1)]


def build_sector_ledgers() -> dict[str, Any]:
    return {
        "dimensionless_ratio": "x = M_F^2 / Lambda^2",
        "volume_density_coefficient": {
            "formula": "sum_{l>=0} f_{4-2l} Lambda^{4-2l} c_l(M_F)",
            "first_terms": {
                "f4_Lambda4": scaled_term(taylor_coeff(0), 0),
                "f2_Lambda2": scaled_term(taylor_coeff(1), 1),
                "f0": scaled_term(taylor_coeff(2), 2),
                "f_minus2_Lambda_minus2": scaled_term(taylor_coeff(3), 3),
                "f_minus4_Lambda_minus4": scaled_term(taylor_coeff(4), 4),
            },
        },
        "einstein_hilbert_coefficient": {
            "formula": "sum_{l>=0} f_{2-2l} Lambda^{2-2l} c_l(M_F) multiplying a2_ext[R]",
            "first_terms": {
                "f2_Lambda2": scaled_term(taylor_coeff(0), 0),
                "f0": scaled_term(taylor_coeff(1), 1),
                "f_minus2_Lambda_minus2": scaled_term(taylor_coeff(2), 2),
                "f_minus4_Lambda_minus4": scaled_term(taylor_coeff(3), 3),
            },
            "normalized_W33_polynomial": "1 - 4x + 17x^2 - (194/3)x^3 + (653/3)x^4 - ...",
        },
        "yang_mills_coefficient": {
            "normalization": "a4_ext[F^2] = (4pi)^(-2) int sqrt(g) (1/12) kappa_G tr(F^2)",
            "formula": "1/(4g_G^2) = kappa_G/(12(4pi)^2) * C_YM",
            "C_YM": {
                "f0": scaled_term(taylor_coeff(0), 0),
                "f_minus2_Lambda_minus2": scaled_term(taylor_coeff(1), 1),
                "f_minus4_Lambda_minus4": scaled_term(taylor_coeff(2), 2),
                "f_minus6_Lambda_minus6": scaled_term(taylor_coeff(3), 3),
            },
            "leading_factor": "20 f0 kappa_G / (4pi)^2",
            "normalized_W33_polynomial": "1 - 4x + 17x^2 - (194/3)x^3 + ...",
        },
        "higgs_guardrail": {
            "fixed_traces": {
                "tr_F(1)": "240",
                "tr_F(M_F^2 Delta_1)": "960 M_F^2",
                "tr_F((M_F^2 Delta_1)^2)": "8160 M_F^4",
            },
            "still_required": [
                "finite algebra representation on C_1(W(3,3))",
                "Phi action on the 81,120,24,15 sectors",
                "tr_F(Phi^2)",
                "tr_F(Phi^4)",
                "tr_F(Delta_1 Phi^2)",
                "tr_F((nabla Phi)^2)",
            ],
        },
        "fermion_projection": {
            "massless_kernel": "ker Delta_1, dimension 81",
            "chiral_double": "162",
            "yukawa_location": "Phi couplings on/through the 81-dimensional kernel and massive sectors",
        },
    }


def build_result() -> DimensionalNormalizationResult:
    dim_moms = {str(k): str(moment(k)) for k in range(MAX_ORDER + 1)}
    scaled_moms = {
        str(k): scaled_term(Fraction(moment(k)), k) for k in range(MAX_ORDER + 1)
    }
    scaled_taylor = {
        str(k): scaled_term(taylor_coeff(k), k) for k in range(MAX_ORDER + 1)
    }
    norm_poly = {
        str(k): frac_to_str(normalized_poly_coeff(k)) for k in range(MAX_ORDER + 1)
    }
    checks = {
        "dimension_240": sum(SPECTRUM.values()) == 240,
        "mu0_240": moment(0) == 240,
        "mu1_960": moment(1) == 960,
        "mu2_8160": moment(2) == 8160,
        "c1_scaled": scaled_term(taylor_coeff(1), 1) == "-960 M_F^2",
        "c2_scaled": scaled_term(taylor_coeff(2), 2) == "4080 M_F^4",
        "normalized_coeff_1_minus4": normalized_poly_coeff(1) == Fraction(-4),
        "normalized_coeff_2_17": normalized_poly_coeff(2) == Fraction(17),
        "normalized_coeff_3_minus194_over_3": normalized_poly_coeff(3) == Fraction(-194, 3),
        "leading_gauge_factor_20": Fraction(240, 12) == Fraction(20),
    }
    return DimensionalNormalizationResult(
        part="CCCCCLXVI",
        title="Dimensional Normalization Ledger for W(3,3) Spectral Action",
        dimensionless_spectrum={str(k): v for k, v in SPECTRUM.items()},
        dimensionful_operator={
            "D_F^2": "M_F^2 Delta_1",
            "D_tot": "D_ext tensor 1_F + gamma_5 tensor D_F",
            "D_tot^2": "D_ext^2 tensor 1_F + 1_ext tensor M_F^2 Delta_1",
            "control_ratio": "x = M_F^2 / Lambda^2",
        },
        dimensionless_moments=dim_moms,
        scaled_moments=scaled_moms,
        scaled_taylor_coefficients=scaled_taylor,
        normalized_polynomial_coefficients=norm_poly,
        convolution_coefficients=convolution(MAX_ORDER),
        sector_ledgers=build_sector_ledgers(),
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = build_result()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "dimensional normalization checks failed"
    out = Path("data/PART_CCCCCLXVI_dimensional_normalization_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
