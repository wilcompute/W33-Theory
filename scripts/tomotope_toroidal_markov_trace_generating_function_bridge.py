#!/usr/bin/env python3
"""Trace generating-function bridge for toroidal Markov transport.

Let

  T(z) = sum_{n>=1} Tr(P^n) z^n

for the 8-state Part-DC transition matrix P.

Using the established nontrivial moment generating function

  M(z) = sum_{n>=0} m_n z^n
       = (6 - (21/32) z^2) / (1 - (21/64) z^2 - (7/512) z^3),

and Tr(P^n) = 1 + m_n (n>=1), we get

  T(z) = z/(1-z) + (M(z) - 6),

which simplifies to a single exact rational function.
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
from scripts.tomotope_toroidal_markov_generating_function_bridge import build_bridge as build_moment_gf  # noqa: E402

OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_trace_generating_function_bridge.json"


@dataclass(frozen=True)
class TraceGeneratingFunctionSummary:
    checked_max_power: int
    numerator_t1_num: int
    numerator_t1_den: int
    numerator_t2_num: int
    numerator_t2_den: int
    numerator_t3_num: int
    numerator_t3_den: int
    numerator_t4_num: int
    numerator_t4_den: int
    denominator_d0_num: int
    denominator_d0_den: int
    denominator_d1_num: int
    denominator_d1_den: int
    denominator_d2_num: int
    denominator_d2_den: int
    denominator_d3_num: int
    denominator_d3_den: int
    denominator_d4_num: int
    denominator_d4_den: int
    all_identities_hold: bool


def _poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0, 1) for _ in range(n)]
    for i in range(len(a)):
        out[i] += a[i]
    for i in range(len(b)):
        out[i] += b[i]
    return out


def _poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0, 1) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def build_bridge(max_power: int = 12) -> dict[str, Any]:
    mgf = build_moment_gf(max_power=max_power)
    rec = build_recurrence(max_power=max_power)

    num = mgf["generating_function"]["numerator"]
    den = mgf["generating_function"]["denominator"]

    # M(z)=N/D
    N = [
        Fraction(num["c0"]["numerator"], num["c0"]["denominator"]),
        Fraction(num["c1"]["numerator"], num["c1"]["denominator"]),
        Fraction(num["c2"]["numerator"], num["c2"]["denominator"]),
    ]
    D = [
        Fraction(den["d0"]["numerator"], den["d0"]["denominator"]),
        Fraction(den["d1"]["numerator"], den["d1"]["denominator"]),
        Fraction(den["d2"]["numerator"], den["d2"]["denominator"]),
        Fraction(den["d3"]["numerator"], den["d3"]["denominator"]),
    ]

    # T(z)=z/(1-z)+(M(z)-6) = z/(1-z) + (N-6D)/D
    one_minus_z = [Fraction(1, 1), Fraction(-1, 1)]
    N_minus_6D = _poly_add(N, [-6 * x for x in D])

    # Combine with common denominator (1-z)D
    num_left = _poly_mul([Fraction(0, 1), Fraction(1, 1)], D)  # z*D
    num_right = _poly_mul(N_minus_6D, one_minus_z)
    T_num = _poly_add(num_left, num_right)
    T_den = _poly_mul(one_minus_z, D)

    # Coefficients of trace series from recurrence payload.
    trace_rows = rec["trace_rows"]
    traces = [
        Fraction(r["trace_pn"]["numerator"], r["trace_pn"]["denominator"]) for r in trace_rows
    ]

    # Validate denominator*T(z) = numerator to checked order.
    # T has no constant term; coefficient at z^n (n>=1) is traces[n-1].
    residuals: list[Fraction] = []
    for n in range(0, max_power + 1):
        lhs = Fraction(0, 1)
        for j, dj in enumerate(T_den):
            k = n - j
            if k <= 0:
                continue
            lhs += dj * traces[k - 1]

        rhs = T_num[n] if n < len(T_num) else Fraction(0, 1)
        residuals.append(lhs - rhs)

    identities = {
        "upstream_moment_gf_identities_hold": bool(mgf["summary"]["all_identities_hold"]),
        "upstream_recurrence_identities_hold": bool(rec["summary"]["all_identities_hold"]),
        "trace_rational_series_matches_coefficients": all(r == 0 for r in residuals),
        "trace_linear_term_is_one": len(T_num) > 1 and T_num[1] == Fraction(1, 1),
    }

    # Pad to fixed displayed degree 4 (enough for this denominator family).
    while len(T_num) < 5:
        T_num.append(Fraction(0, 1))
    while len(T_den) < 5:
        T_den.append(Fraction(0, 1))

    summary = TraceGeneratingFunctionSummary(
        checked_max_power=max_power,
        numerator_t1_num=T_num[1].numerator,
        numerator_t1_den=T_num[1].denominator,
        numerator_t2_num=T_num[2].numerator,
        numerator_t2_den=T_num[2].denominator,
        numerator_t3_num=T_num[3].numerator,
        numerator_t3_den=T_num[3].denominator,
        numerator_t4_num=T_num[4].numerator,
        numerator_t4_den=T_num[4].denominator,
        denominator_d0_num=T_den[0].numerator,
        denominator_d0_den=T_den[0].denominator,
        denominator_d1_num=T_den[1].numerator,
        denominator_d1_den=T_den[1].denominator,
        denominator_d2_num=T_den[2].numerator,
        denominator_d2_den=T_den[2].denominator,
        denominator_d3_num=T_den[3].numerator,
        denominator_d3_den=T_den[3].denominator,
        denominator_d4_num=T_den[4].numerator,
        denominator_d4_den=T_den[4].denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "trace_generating_function": {
            "definition": "T(z)=sum_{n>=1} Tr(P^n) z^n",
            "identity_from_moment_gf": "T(z)=z/(1-z)+(M(z)-6)",
            "numerator": {
                f"t{i}": {"numerator": T_num[i].numerator, "denominator": T_num[i].denominator}
                for i in range(1, 5)
            },
            "denominator": {
                f"d{i}": {"numerator": T_den[i].numerator, "denominator": T_den[i].denominator}
                for i in range(0, 5)
            },
        },
        "identities": identities,
        "notes": (
            "The full trace ladder of the 8-state chain is encoded by one exact "
            "rational series derived from the nontrivial packet generating function."
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
