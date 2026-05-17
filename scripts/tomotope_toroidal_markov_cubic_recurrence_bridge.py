#!/usr/bin/env python3
"""Cubic-recurrence bridge for toroidal Markov nontrivial moments.

Uses the algebraic closure from the DCII nontrivial packet:

    512*x^3 - 168*x - 7 = 0.

Hence every nontrivial mode lambda satisfies

    lambda^3 = (21/64) lambda + (7/512),

and the nontrivial power-sum sequence

    m_n = sum_{k=1}^6 lambda_k^n

obeys the exact linear recurrence

    m_{n+3} = (21/64) m_{n+1} + (7/512) m_n.

This module verifies the recurrence against direct mode sums and against
Markov-matrix traces from the Part DC transition operator.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tomotope_toroidal_markov_algebraic_closure_bridge import build_bridge as build_algebraic  # noqa: E402

MARKOV_PATH = ROOT / "data" / "tomotope_toroidal_markov_ground_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_cubic_recurrence_bridge.json"


@dataclass(frozen=True)
class CubicRecurrenceSummary:
    checked_max_power: int
    recurrence_coeff_a_num: int
    recurrence_coeff_a_den: int
    recurrence_coeff_b_num: int
    recurrence_coeff_b_den: int
    m0_num: int
    m0_den: int
    m1_num: int
    m1_den: int
    m2_num: int
    m2_den: int
    all_identities_hold: bool


def _parse_fraction(text: str) -> Fraction:
    a, b = text.split("/")
    return Fraction(int(a), int(b))


def _mat_mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    out = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out


def _mat_pow(a: list[list[Fraction]], n: int) -> list[list[Fraction]]:
    size = len(a)
    out = [[Fraction(int(i == j), 1) for j in range(size)] for i in range(size)]
    base = a
    exp = n
    while exp > 0:
        if exp & 1:
            out = _mat_mul(out, base)
        base = _mat_mul(base, base)
        exp >>= 1
    return out


def _trace(a: list[list[Fraction]]) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def build_bridge(max_power: int = 12) -> dict[str, Any]:
    markov = json.loads(MARKOV_PATH.read_text(encoding="utf-8"))
    algebraic = build_algebraic()

    P = [[_parse_fraction(x) for x in row] for row in markov["transition_matrix"]]

    # Nontrivial mode packet from DCII.
    mode_exprs = [
        sp.Rational(1, 8) + sp.Rational(3, 4) * sp.cos(2 * sp.pi * k / 7)
        for k in range(1, 7)
    ]

    a = Fraction(21, 64)
    b = Fraction(7, 512)

    # Exact symbolic moments m_n, then convert to rational via nsimplify.
    m: list[Fraction] = []
    for n in range(max_power + 1):
        expr = sp.simplify(sum(mu**n for mu in mode_exprs))
        q = sp.together(sp.nsimplify(expr))
        q_num, q_den = sp.fraction(q)
        m.append(Fraction(int(q_num), int(q_den)))

    # Recurrence-generated moments from initial data m0,m1,m2.
    m_rec = [m[0], m[1], m[2]]
    for n in range(max_power - 2):
        m_rec.append(a * m_rec[n + 1] + b * m_rec[n])

    # Trace(P^n) should equal 1 + m_n for n >= 1 (eigs: 1,0,lambda_1..lambda_6).
    trace_rows: list[dict[str, Any]] = []
    for n in range(1, max_power + 1):
        tr = _trace(_mat_pow(P, n))
        rhs = Fraction(1, 1) + m[n]
        trace_rows.append(
            {
                "n": n,
                "trace_pn": {"numerator": tr.numerator, "denominator": tr.denominator},
                "one_plus_nontrivial_moment": {
                    "numerator": rhs.numerator,
                    "denominator": rhs.denominator,
                },
            }
        )

    identities = {
        "upstream_algebraic_identities_hold": bool(algebraic["summary"]["all_identities_hold"]),
        "initial_m0_is_6": m[0] == Fraction(6, 1),
        "initial_m1_is_0": m[1] == Fraction(0, 1),
        "initial_m2_is_21_over_16": m[2] == Fraction(21, 16),
        "recurrence_matches_symbolic_moments": all(m[n] == m_rec[n] for n in range(max_power + 1)),
        "trace_equals_one_plus_nontrivial_moment": all(
            Fraction(r["trace_pn"]["numerator"], r["trace_pn"]["denominator"])
            == Fraction(
                r["one_plus_nontrivial_moment"]["numerator"],
                r["one_plus_nontrivial_moment"]["denominator"],
            )
            for r in trace_rows
        ),
    }

    summary = CubicRecurrenceSummary(
        checked_max_power=max_power,
        recurrence_coeff_a_num=a.numerator,
        recurrence_coeff_a_den=a.denominator,
        recurrence_coeff_b_num=b.numerator,
        recurrence_coeff_b_den=b.denominator,
        m0_num=m[0].numerator,
        m0_den=m[0].denominator,
        m1_num=m[1].numerator,
        m1_den=m[1].denominator,
        m2_num=m[2].numerator,
        m2_den=m[2].denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "recurrence": {
            "equation": "m_{n+3} = (21/64) m_{n+1} + (7/512) m_n",
            "coefficients": {
                "a": {"numerator": a.numerator, "denominator": a.denominator},
                "b": {"numerator": b.numerator, "denominator": b.denominator},
            },
        },
        "moments": [
            {"n": n, "numerator": m[n].numerator, "denominator": m[n].denominator}
            for n in range(max_power + 1)
        ],
        "trace_rows": trace_rows,
        "identities": identities,
        "notes": (
            "The cubic mode closure upgrades to a finite exact recurrence for all "
            "nontrivial power moments, and those moments reconstruct Markov traces "
            "via Tr(P^n)=1+m_n for n>=1."
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
