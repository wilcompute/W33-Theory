#!/usr/bin/env python3
"""
PART CXXXVIII — Hashimoto Quadratic-Field Compiler
==================================================

This module is a small exact bridge built on Parts CXXXVI–CXXXVII.

CXXXVII proved that the 480-dimensional non-backtracking Hashimoto carrier
of W(3,3) has the magnitude trichotomy

    |mu| = 11          multiplicity 1
    |mu| = sqrt(11)    multiplicity 78
    |mu| = 1           multiplicity 401

The new observation here is that the 78-dimensional Ramanujan layer is not a
featureless circle.  Bass's quadratic equation

    x^2 - lambda*x + 11 = 0

splits the two nontrivial W(3,3) adjacency sectors into two exact imaginary
quadratic fields:

    lambda =  2  (mult 24):  x =  1 ± i*sqrt(10),   10 = Phi_4(3)
    lambda = -4  (mult 15):  x = -2 ± i*sqrt(7),     7 = Phi_6(3)

So the Ramanujan shell is a two-field cyclotomic compiler:

    11 = 1^2 + Phi_4(3) = 2^2 + Phi_6(3).

This locks the latest QCD beta-cyclotomic sprint (Phi_6=7) into the
Hashimoto/Ihara operator itself, while Phi_4=10 is the companion
Ko-dimension / superstring dimension already present in the repo.

The script emits:
  * the exact characteristic-polynomial factorization of B,
  * the exact Ihara-zeta inverse factorization,
  * the Lucas-recursive trace compiler for tr(B^n),
  * a JSON report suitable for regression tests and downstream docs.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

# W(3,3) / SRG(40,12,2,4) invariants.
Q0 = 3
V = 40
K = 12
LAMBDA_SRG = 2
MU_SRG = 4
M = 240
DIRECTED_EDGES = 2 * M
HASHIMOTO_Q = K - 1
BASS_TRIVIAL_MULT = M - V


def phi3(q: int = Q0) -> int:
    return q * q + q + 1


def phi4(q: int = Q0) -> int:
    return q * q + 1


def phi6(q: int = Q0) -> int:
    return q * q - q + 1


@dataclass(frozen=True)
class QuadraticSector:
    """One Bass quadratic sector for a W(3,3) adjacency eigenvalue."""

    adjacency_eigenvalue: int
    adjacency_multiplicity: int
    real_part: Fraction
    imag_square: int
    cyclotomic_label: str
    field_label: str
    norm: int

    @property
    def doubled_hashimoto_multiplicity(self) -> int:
        return 2 * self.adjacency_multiplicity

    @property
    def root_label(self) -> str:
        sign = "+" if self.real_part >= 0 else "-"
        rp = abs(self.real_part)
        if rp.denominator == 1:
            rp_txt = str(rp.numerator)
        else:
            rp_txt = f"{rp.numerator}/{rp.denominator}"
        return f"{sign}{rp_txt} ± i√{self.imag_square}"


def quadratic_sectors() -> List[QuadraticSector]:
    """Return the two nontrivial Ramanujan sectors of W(3,3)."""
    h = HASHIMOTO_Q
    sectors = []
    for lam, mult, label in [
        (2, 24, "Phi_4(3)"),
        (-4, 15, "Phi_6(3)"),
    ]:
        real = Fraction(lam, 2)
        imag_sq = h - real * real
        assert imag_sq.denominator == 1
        imag_sq_int = int(imag_sq)
        field = f"Q(sqrt(-{imag_sq_int}))"
        sectors.append(
            QuadraticSector(
                adjacency_eigenvalue=lam,
                adjacency_multiplicity=mult,
                real_part=real,
                imag_square=imag_sq_int,
                cyclotomic_label=label,
                field_label=field,
                norm=h,
            )
        )
    return sectors


def lucas_sequence_for_root_pair(trace: int, norm: int, n_max: int) -> List[int]:
    """Return L_n = alpha^n + beta^n for roots of x^2 - trace*x + norm.

    Recurrence:
        L_0 = 2
        L_1 = trace
        L_n = trace*L_{n-1} - norm*L_{n-2}
    """
    if n_max < 0:
        return []
    seq = [2]
    if n_max == 0:
        return seq
    seq.append(trace)
    for _n in range(2, n_max + 1):
        seq.append(trace * seq[-1] - norm * seq[-2])
    return seq


def hashimoto_trace_formula(n: int) -> int:
    """Exact closed non-backtracking trace tr(B^n) for W(3,3).

    Characteristic polynomial:
        (x-11)(x-1)^201 (x+1)^200
        * (x^2 - 2x + 11)^24
        * (x^2 + 4x + 11)^15

    Hence:
        T_n = 11^n + 1^n
              + 24 L_n(2,11) + 15 L_n(-4,11)
              + 200(1 + (-1)^n)
    """
    l_2 = lucas_sequence_for_root_pair(2, HASHIMOTO_Q, n)[n]
    l_neg4 = lucas_sequence_for_root_pair(-4, HASHIMOTO_Q, n)[n]
    return (
        HASHIMOTO_Q**n
        + 1
        + 24 * l_2
        + 15 * l_neg4
        + BASS_TRIVIAL_MULT * (1 + (-1) ** n)
    )


def trace_table(n_max: int = 16) -> List[Dict[str, object]]:
    rows = []
    for n in range(1, n_max + 1):
        t = hashimoto_trace_formula(n)
        denom = DIRECTED_EDGES * HASHIMOTO_Q ** (n - 1)
        rows.append(
            {
                "n": n,
                "trace_B^n": t,
                "closure_fraction": float(Fraction(t, denom)),
                "closure_fraction_exact": str(Fraction(t, denom)),
            }
        )
    return rows


def characteristic_factorization() -> Dict[str, object]:
    """Compact exact charpoly factorization of the Hashimoto operator B."""
    return {
        "factorization": (
            "(x-11)(x-1)^201(x+1)^200"
            "(x^2-2x+11)^24(x^2+4x+11)^15"
        ),
        "degree_check": 1 + 201 + 200 + 2 * 24 + 2 * 15,
        "trace_check": (
            "11 + 201*(1) + 200*(-1) + 24*(2) + 15*(-4) = 0"
        ),
    }


def ihara_zeta_inverse_factorization() -> Dict[str, object]:
    """Bass/Ihara determinant factorization for det(I-uB)."""
    return {
        "factorization": (
            "(1-11u)(1-u)^201(1+u)^200"
            "(1-2u+11u^2)^24(1+4u+11u^2)^15"
        ),
        "bass_form": (
            "(1-u^2)^200(1-12u+11u^2)"
            "(1-2u+11u^2)^24(1+4u+11u^2)^15"
        ),
        "critical_circle": "|u| = 1/sqrt(11) for all 78 nontrivial zeros",
    }


def quadratic_field_compiler_audit(n_max: int = 16) -> Dict[str, object]:
    sectors = quadratic_sectors()
    checks = {
        "phi3": phi3(),
        "phi4": phi4(),
        "phi6": phi6(),
        "hashimoto_q": HASHIMOTO_Q,
        "norm_identity_phi4": 1 * 1 + phi4(),
        "norm_identity_phi6": 2 * 2 + phi6(),
        "ramanujan_layer_dimension": sum(s.doubled_hashimoto_multiplicity for s in sectors),
        "bass_trivial_plus_perron_mate": 2 * BASS_TRIVIAL_MULT + 1,
        "carrier_total": 1
        + sum(s.doubled_hashimoto_multiplicity for s in sectors)
        + (2 * BASS_TRIVIAL_MULT + 1),
        "triangle_trace_T3": hashimoto_trace_formula(3),
    }
    assert checks["norm_identity_phi4"] == HASHIMOTO_Q
    assert checks["norm_identity_phi6"] == HASHIMOTO_Q
    assert checks["ramanujan_layer_dimension"] == 78
    assert checks["bass_trivial_plus_perron_mate"] == 401
    assert checks["carrier_total"] == DIRECTED_EDGES
    assert checks["triangle_trace_T3"] == 960

    return {
        "module": "PART_CXXXVIII_HASHIMOTO_QUADRATIC_FIELD_COMPILER",
        "graph": {
            "v": V,
            "m": M,
            "directed_edges": DIRECTED_EDGES,
            "k": K,
            "lambda": LAMBDA_SRG,
            "mu": MU_SRG,
            "hashimoto_q": HASHIMOTO_Q,
        },
        "new_theorem": (
            "The 78-dimensional nontrivial Hashimoto/Ramanujan layer splits into "
            "two exact imaginary-quadratic cyclotomic sectors: "
            "24 copies of roots 1±i√Phi4(3), and 15 copies of roots -2±i√Phi6(3)."
        ),
        "quadratic_sectors": [asdict(s) | {"root_label": s.root_label} for s in sectors],
        "characteristic_polynomial": characteristic_factorization(),
        "ihara_zeta_inverse": ihara_zeta_inverse_factorization(),
        "trace_compiler": (
            "tr(B^n)=11^n+1+24L_n(2,11)+15L_n(-4,11)+200(1+(-1)^n), "
            "where L_0=2,L_1=a,L_n=aL_{n-1}-11L_{n-2}."
        ),
        "trace_table": trace_table(n_max),
        "checks": checks,
        "interpretive_note": (
            "Phi6=7 is no longer only a QCD beta/Higgs cyclotomic number: it is "
            "the imaginary-square of the s=-4 Hashimoto Ramanujan root. Phi4=10 "
            "is the companion imaginary-square of the r=2 root. The non-backtracking "
            "operator therefore compiles the two cyclotomic sectors {Phi4,Phi6} "
            "directly into closed-loop trace arithmetic."
        ),
    }


def main() -> int:
    audit = quadratic_field_compiler_audit(n_max=16)
    out = ROOT / "PART_CXXXVIII_hashimoto_quadratic_field_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2, default=str), encoding="utf-8")
    print(json.dumps(audit, indent=2, default=str))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
