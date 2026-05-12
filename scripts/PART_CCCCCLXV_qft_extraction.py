#!/usr/bin/env python3
"""
PART_CCCCCLXV_qft_extraction.py

Executable artifact for Part CCCCCLXV.

This script implements the concrete QFT extraction choice:

  external spectral triple:
      compact oriented 4D Riemannian spin manifold with gauge connection

  internal W(3,3) carrier:
      H_F = C_1(W(3,3); C), dim 240
      D_F^2 = Delta_1, the cellular 1-Hodge Laplacian
      Spec(Delta_1) = 0^81, 4^120, 10^24, 16^15

It computes exact internal moments, Seeley--DeWitt convolution coefficients,
and the normalized sector extraction ledger.
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
class QFTExtraction:
    part: str
    title: str
    external_spectral_triple: dict[str, Any]
    internal_carrier: dict[str, Any]
    internal_spectrum: dict[str, int]
    moments: dict[str, str]
    taylor_coefficients: dict[str, str]
    convolution_coefficients: dict[str, dict[str, str]]
    sector_extraction: dict[str, Any]
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
    return sum(mult * (eig ** power) for eig, mult in SPECTRUM.items())


def moments(max_power: int = MAX_ORDER) -> dict[int, int]:
    return {p: moment(p) for p in range(max_power + 1)}


def taylor_coeff(power: int) -> Fraction:
    return Fraction(((-1) ** power) * moment(power), factorial(power))


def frac_to_str(x: Fraction | int) -> str:
    if isinstance(x, int):
        return str(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def convolution(max_r: int = MAX_ORDER) -> dict[str, dict[str, Fraction]]:
    """A_{2r}^{tot} = sum_{l=0}^r c_l a_{2(r-l)}^ext."""
    out: dict[str, dict[str, Fraction]] = {}
    for r in range(max_r + 1):
        terms: dict[str, Fraction] = {}
        for ell in range(r + 1):
            terms[f"a{2 * (r - ell)}_ext"] = taylor_coeff(ell)
        out[f"A{2 * r}_tot"] = terms
    return out


def build_external_triple() -> dict[str, Any]:
    return {
        "algebra": "A_ext = C^infty(M)",
        "hilbert_space": "H_ext = L^2(M,S)",
        "dirac_operator": "D_ext = gamma^mu (nabla_mu^S + A_mu)",
        "grading": "gamma_5",
        "dimension": 4,
        "heat_trace_expansion": "K_ext(t) ~ sum_{r>=0} a_{2r}^{ext} t^{r-2}",
        "normalization": {
            "laplace_type_operator": "P = -(g^{mu nu} nabla_mu nabla_nu + E)",
            "a0_ext": "(4pi)^(-2) int_M sqrt(g) tr(1)",
            "a2_ext": "(4pi)^(-2) int_M sqrt(g) tr(E + R/6)",
            "a4_ext": "(4pi)^(-2)/360 int_M sqrt(g) tr(60RE + 180E^2 + 30Omega^2 + curvature scalars)",
        },
    }


def build_internal_carrier() -> dict[str, Any]:
    return {
        "carrier": "H_F = C_1(W(3,3); C)",
        "dimension": 240,
        "operator": "Delta_1 = d1^* d1 + d2 d2^*",
        "product_operator": "D_tot = D_ext tensor 1_F + gamma_5 tensor D_F",
        "product_square": "D_tot^2 = D_ext^2 tensor 1_F + 1_ext tensor Delta_1",
        "heat_factorization": "K_tot(t) = K_ext(t) K_F(t)",
        "heat_trace": "K_F(t)=81+120 exp(-4t)+24 exp(-10t)+15 exp(-16t)",
        "sector_split": {
            "harmonic_H1_zero_modes": 81,
            "triangle_boundary_gauge_exact": 120,
            "r_sector": 24,
            "s_sector": 15,
        },
        "why_chosen": "Smallest carrier that simultaneously sees the 81 physical H1 modes, 120 triangle-boundary/gauge sector, and 24/15 W(3,3) heavy sectors.",
    }


def build_sector_extraction() -> dict[str, Any]:
    c = {i: taylor_coeff(i) for i in range(MAX_ORDER + 1)}
    return {
        "bosonic_spectral_action": "S_bos(Lambda) ~ f4 Lambda^4 A0 + f2 Lambda^2 A2 + f0 A4 + f_-2 Lambda^-2 A6 + ...",
        "volume_ladder": [frac_to_str(c[i]) for i in range(0, 6)],
        "einstein_hilbert_ladder": {
            "coefficient_series_for_a2_ext_R": "f2 Lambda^2*c0 + f0*c1 + f_-2 Lambda^-2*c2 + f_-4 Lambda^-4*c3 + ...",
            "first_terms": {
                "f2_Lambda2": frac_to_str(c[0]),
                "f0": frac_to_str(c[1]),
                "f_minus2_Lambda_minus2": frac_to_str(c[2]),
                "f_minus4_Lambda_minus4": frac_to_str(c[3]),
            },
        },
        "gauge_sector": {
            "normalization": "a4_ext[F^2] = (4pi)^(-2) int sqrt(g) (1/12) kappa_G tr(F_{mu nu}F^{mu nu})",
            "leading_inverse_coupling": "1/(4 g_G^2) = f0 * 20 * kappa_G / (4pi)^2",
            "derivation": "c0/12 = 240/12 = 20",
            "relative_couplings_depend_on": "representation trace normalizations kappa_G",
        },
        "higgs_sector": {
            "inner_fluctuation": "D_F -> D_F + Phi(x)",
            "required_exact_traces": [
                "tr_F(Phi^2)",
                "tr_F(Phi^4)",
                "tr_F(Delta_1 Phi^2)",
                "tr_F((nabla Phi)^2) after representation choice",
            ],
            "fixed_W33_inputs": {
                "tr_F(1)": "240",
                "tr_F(Delta_1)": "960",
                "tr_F(Delta_1^2)": "8160",
            },
            "guardrail": "No Higgs mass/quartic number is fixed until Phi representation traces are explicit.",
        },
        "fermion_sector": {
            "fermionic_action": "S_ferm = <psi, D_tot^{A,Phi} psi>",
            "massless_matter_carrier": "ker Delta_1, dimension 81",
            "chiral_real_projection": "H_ferm = H1_cell^+ direct_sum H1_cell^-, dimension 162",
            "full_internal_bosonic_carrier": "C_1(W(3,3)), dimension 240",
        },
        "carrier_dictionary": {
            "40": "adjacency theorem kernel",
            "81": "cellular H1 harmonic matter/generation sector",
            "162": "fermionic chiral doubled H1 sector",
            "240": "full cellular 1-chain QFT extraction carrier",
            "480": "directed-edge Hashimoto propagation carrier",
        },
    }


def build_result() -> QFTExtraction:
    moms = moments(MAX_ORDER)
    tay = {str(i): frac_to_str(taylor_coeff(i)) for i in range(MAX_ORDER + 1)}
    conv = {
        key: {name: frac_to_str(val) for name, val in terms.items()}
        for key, terms in convolution(MAX_ORDER).items()
    }
    checks = {
        "dimension_240": sum(SPECTRUM.values()) == 240,
        "zero_modes_81": SPECTRUM[0] == 81,
        "boundary_sector_120": SPECTRUM[4] == 120,
        "heavy_sectors_24_15": SPECTRUM[10] == 24 and SPECTRUM[16] == 15,
        "mu0_240": moms[0] == 240,
        "mu1_960": moms[1] == 960,
        "mu2_8160": moms[2] == 8160,
        "mu3_93120": moms[3] == 93120,
        "mu4_1253760": moms[4] == 1253760,
        "c0_240": taylor_coeff(0) == Fraction(240),
        "c1_minus960": taylor_coeff(1) == Fraction(-960),
        "c2_4080": taylor_coeff(2) == Fraction(4080),
        "c3_minus15520": taylor_coeff(3) == Fraction(-15520),
        "gauge_factor_20": Fraction(240, 12) == Fraction(20),
        "A4_coefficients": convolution(2)["A4_tot"] == {
            "a4_ext": Fraction(240),
            "a2_ext": Fraction(-960),
            "a0_ext": Fraction(4080),
        },
    }
    return QFTExtraction(
        part="CCCCCLXV",
        title="QFT Extraction from the 240-Dimensional W(3,3) 1-Chain Carrier",
        external_spectral_triple=build_external_triple(),
        internal_carrier=build_internal_carrier(),
        internal_spectrum={str(k): v for k, v in SPECTRUM.items()},
        moments={str(k): str(v) for k, v in moms.items()},
        taylor_coefficients=tay,
        convolution_coefficients=conv,
        sector_extraction=build_sector_extraction(),
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = build_result()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "one or more QFT extraction checks failed"
    out = Path("data/PART_CCCCCLXV_qft_extraction_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
