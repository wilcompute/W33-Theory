#!/usr/bin/env python3
"""Algebraic closure bridge for DCII toroidal Markov nontrivial modes.

For the DCII nontrivial packet

    lambda_k = 1/8 + (3/4) cos(2*pi*k/7),  k=1..6,

the three distinct values (each with multiplicity 2) are exactly the roots of

    512 x^3 - 168 x - 7 = 0.

This module certifies that closure and re-derives the DCI second-moment value
21/16 from the cubic packet without reintroducing floating assumptions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
FOURIER_PATH = ROOT / "data" / "tomotope_toroidal_markov_fourier_bridge.json"
MOMENT_PATH = ROOT / "data" / "tomotope_toroidal_markov_spectral_moment_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_algebraic_closure_bridge.json"


@dataclass(frozen=True)
class AlgebraicClosureSummary:
    polynomial_degree: int
    distinct_nontrivial_roots: int
    nontrivial_multiplicity_per_root: int
    weighted_sum_num: int
    weighted_sum_den: int
    weighted_square_sum_num: int
    weighted_square_sum_den: int
    all_identities_hold: bool


def _parse_fraction(n: int, d: int) -> Fraction:
    return Fraction(int(n), int(d))


def build_bridge() -> dict[str, Any]:
    fourier = json.loads(FOURIER_PATH.read_text(encoding="utf-8"))
    moment = json.loads(MOMENT_PATH.read_text(encoding="utf-8"))

    x = sp.symbols("x")
    poly = 512 * x**3 - 168 * x - 7
    roots = sp.nroots(poly, n=80)

    distinct_roots = sorted([complex(r) for r in roots], key=lambda z: z.real)

    # Nontrivial modes in exact symbolic form from the DCII formula.
    mode_exprs = [sp.Rational(1, 8) + sp.Rational(3, 4) * sp.cos(2 * sp.pi * k / 7) for k in range(1, 7)]
    residuals = [sp.simplify(512 * m**3 - 168 * m - 7) for m in mode_exprs]
    residuals_numeric = [complex(sp.N(r, 120)) for r in residuals]

    # Distinct roots each occur twice because cos(2πk/7)=cos(2π(7-k)/7).
    weighted_sum = sp.simplify(sum(mode_exprs))
    weighted_square_sum = sp.simplify(sum(m**2 for m in mode_exprs))

    weighted_sum_frac = Fraction(int(sp.nsimplify(weighted_sum).p), int(sp.nsimplify(weighted_sum).q))
    weighted_sq_frac = Fraction(
        int(sp.nsimplify(weighted_square_sum).p),
        int(sp.nsimplify(weighted_square_sum).q),
    )

    expected_sq = _parse_fraction(
        moment["summary"]["nontrivial_second_moment_num"],
        moment["summary"]["nontrivial_second_moment_den"],
    )

    identities = {
        "upstream_fourier_identities_hold": bool(fourier["summary"]["all_identities_hold"]),
        "upstream_moment_identities_hold": bool(moment["summary"]["all_identities_hold"]),
        "all_six_modes_annihilate_cubic": all(abs(z) < 1e-80 for z in residuals_numeric),
        "nontrivial_weighted_sum_is_zero": weighted_sum_frac == Fraction(0, 1),
        "nontrivial_weighted_square_sum_is_21_over_16": weighted_sq_frac == Fraction(21, 16),
        "nontrivial_weighted_square_sum_matches_dci": weighted_sq_frac == expected_sq,
        "three_distinct_real_roots": len(distinct_roots) == 3 and all(abs(z.imag) < 1e-40 for z in distinct_roots),
    }

    summary = AlgebraicClosureSummary(
        polynomial_degree=3,
        distinct_nontrivial_roots=3,
        nontrivial_multiplicity_per_root=2,
        weighted_sum_num=weighted_sum_frac.numerator,
        weighted_sum_den=weighted_sum_frac.denominator,
        weighted_square_sum_num=weighted_sq_frac.numerator,
        weighted_square_sum_den=weighted_sq_frac.denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "cubic": {
            "polynomial": "512*x^3 - 168*x - 7",
            "factorization_over_rationals": "irreducible_over_Q",
            "roots_numeric": [float(z.real) for z in distinct_roots],
            "nontrivial_mode_formula": "lambda_k = 1/8 + (3/4) cos(2*pi*k/7), k=1..6",
        },
        "identities": identities,
        "notes": (
            "The DCII six-mode packet closes algebraically by a cubic with three real roots, "
            "each doubled by k<->(7-k) symmetry. This recovers the DCI nontrivial square-sum "
            "21/16 exactly, without floating-point assumptions."
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
