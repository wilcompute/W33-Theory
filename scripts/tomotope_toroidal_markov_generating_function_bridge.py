#!/usr/bin/env python3
"""Generating-function bridge for toroidal Markov nontrivial moments.

From the cubic-recurrence bridge:

  m_{n+3} = (21/64) m_{n+1} + (7/512) m_n,
  m_0=6, m_1=0, m_2=21/16,

for m_n = sum_{k=1}^6 lambda_k^n (nontrivial mode packet).

Therefore the ordinary generating function is exactly

  M(z) = sum_{n>=0} m_n z^n
       = (6 - (21/32) z^2) / (1 - (21/64) z^2 - (7/512) z^3).

This bridge certifies that rational form and links it to the trace series

  T(z) = sum_{n>=1} Tr(P^n) z^n = z/(1-z) + (M(z)-m_0).
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tomotope_toroidal_markov_cubic_recurrence_bridge import build_bridge as build_recurrence  # noqa: E402

MARKOV_PATH = ROOT / "data" / "tomotope_toroidal_markov_ground_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_generating_function_bridge.json"


@dataclass(frozen=True)
class GeneratingFunctionSummary:
    checked_max_power: int
    numerator_c0_num: int
    numerator_c0_den: int
    numerator_c1_num: int
    numerator_c1_den: int
    numerator_c2_num: int
    numerator_c2_den: int
    denominator_d0_num: int
    denominator_d0_den: int
    denominator_d1_num: int
    denominator_d1_den: int
    denominator_d2_num: int
    denominator_d2_den: int
    denominator_d3_num: int
    denominator_d3_den: int
    all_identities_hold: bool


def _f(num: int, den: int) -> dict[str, int]:
    return {"numerator": int(num), "denominator": int(den)}


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


def build_bridge(max_power: int = 16) -> dict[str, Any]:
    rec = build_recurrence(max_power=6)
    coeffs = rec["recurrence"]["coefficients"]
    a = Fraction(coeffs["a"]["numerator"], coeffs["a"]["denominator"])
    b = Fraction(coeffs["b"]["numerator"], coeffs["b"]["denominator"])

    m0 = Fraction(rec["summary"]["m0_num"], rec["summary"]["m0_den"])
    m1 = Fraction(rec["summary"]["m1_num"], rec["summary"]["m1_den"])
    m2 = Fraction(rec["summary"]["m2_num"], rec["summary"]["m2_den"])
    moments = [m0, m1, m2]
    while len(moments) <= max_power:
        n = len(moments) - 3
        moments.append(a * moments[n + 1] + b * moments[n])

    # M(z) = N(z)/D(z)
    n0 = m0
    n1 = m1
    n2 = m2 - a * m0
    d0 = Fraction(1, 1)
    d1 = Fraction(0, 1)
    d2 = -a
    d3 = -b

    # Check D(z)M(z)-N(z)=0 to order z^max_power via coefficient recurrence.
    residual_coeffs: list[Fraction] = []
    for n in range(max_power + 1):
        lhs = moments[n]
        if n - 2 >= 0:
            lhs += d2 * moments[n - 2]
        if n - 3 >= 0:
            lhs += d3 * moments[n - 3]

        rhs = Fraction(0, 1)
        if n == 0:
            rhs = n0
        elif n == 1:
            rhs = n1
        elif n == 2:
            rhs = n2
        residual_coeffs.append(lhs - rhs)

    # Trace generating series: Tr(P^n)=1+m_n for n>=1.
    markov = json.loads(MARKOV_PATH.read_text(encoding="utf-8"))
    P = [[_parse_fraction(x) for x in row] for row in markov["transition_matrix"]]
    trace_vals = [_trace(_mat_pow(P, n)) for n in range(1, max_power + 1)]
    trace_from_m = [Fraction(1, 1) + moments[n] for n in range(1, max_power + 1)]

    identities = {
        "upstream_recurrence_identities_hold": bool(rec["summary"]["all_identities_hold"]),
        "numerator_is_6_minus_21_over_32_z2": (n0, n1, n2) == (
            Fraction(6, 1),
            Fraction(0, 1),
            Fraction(-21, 32),
        ),
        "denominator_is_1_minus_21_over_64_z2_minus_7_over_512_z3": (d0, d1, d2, d3)
        == (Fraction(1, 1), Fraction(0, 1), Fraction(-21, 64), Fraction(-7, 512)),
        "rational_function_matches_series": all(c == 0 for c in residual_coeffs),
        "trace_series_equals_one_plus_moments": trace_vals == trace_from_m,
    }

    summary = GeneratingFunctionSummary(
        checked_max_power=max_power,
        numerator_c0_num=n0.numerator,
        numerator_c0_den=n0.denominator,
        numerator_c1_num=n1.numerator,
        numerator_c1_den=n1.denominator,
        numerator_c2_num=n2.numerator,
        numerator_c2_den=n2.denominator,
        denominator_d0_num=d0.numerator,
        denominator_d0_den=d0.denominator,
        denominator_d1_num=d1.numerator,
        denominator_d1_den=d1.denominator,
        denominator_d2_num=d2.numerator,
        denominator_d2_den=d2.denominator,
        denominator_d3_num=d3.numerator,
        denominator_d3_den=d3.denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "generating_function": {
            "moment_series": "M(z)=sum_{n>=0} m_n z^n",
            "closed_form": "M(z)=(6-(21/32)z^2)/(1-(21/64)z^2-(7/512)z^3)",
            "numerator": {
                "c0": _f(n0.numerator, n0.denominator),
                "c1": _f(n1.numerator, n1.denominator),
                "c2": _f(n2.numerator, n2.denominator),
            },
            "denominator": {
                "d0": _f(d0.numerator, d0.denominator),
                "d1": _f(d1.numerator, d1.denominator),
                "d2": _f(d2.numerator, d2.denominator),
                "d3": _f(d3.numerator, d3.denominator),
            },
        },
        "trace_series": {
            "definition": "T(z)=sum_{n>=1} Tr(P^n) z^n",
            "identity": "T(z)=z/(1-z)+(M(z)-6)",
        },
        "identities": identities,
        "notes": (
            "The cubic closure and recurrence compress the entire nontrivial mode "
            "packet into a single rational generating function."
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
