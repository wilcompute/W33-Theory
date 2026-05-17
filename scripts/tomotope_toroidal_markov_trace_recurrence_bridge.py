#!/usr/bin/env python3
"""Trace-recurrence bridge for the toroidal Markov chain.

From the trace generating-function bridge with

  T(z) = sum_{n>=1} t_n z^n,  t_n = Tr(P^n),

and denominator

  D(z) = 1 - z - (21/64)z^2 + (161/512)z^3 + (7/512)z^4,

the trace sequence satisfies for n>=5:

  t_n = t_{n-1} + (21/64)t_{n-2} - (161/512)t_{n-3} - (7/512)t_{n-4}.

This bridge certifies that recurrence against exact matrix-power traces.
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

from scripts.tomotope_toroidal_markov_trace_generating_function_bridge import (
    build_bridge as build_trace_gf,
)  # noqa: E402

MARKOV_PATH = ROOT / "data" / "tomotope_toroidal_markov_ground_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_trace_recurrence_bridge.json"


@dataclass(frozen=True)
class TraceRecurrenceSummary:
    checked_max_power: int
    coeff_r1_num: int
    coeff_r1_den: int
    coeff_r2_num: int
    coeff_r2_den: int
    coeff_r3_num: int
    coeff_r3_den: int
    coeff_r4_num: int
    coeff_r4_den: int
    seed_t1_num: int
    seed_t1_den: int
    seed_t2_num: int
    seed_t2_den: int
    seed_t3_num: int
    seed_t3_den: int
    seed_t4_num: int
    seed_t4_den: int
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


def build_bridge(max_power: int = 16) -> dict[str, Any]:
    tgf = build_trace_gf(max_power=max_power)
    markov = json.loads(MARKOV_PATH.read_text(encoding="utf-8"))
    P = [[_parse_fraction(x) for x in row] for row in markov["transition_matrix"]]

    den = tgf["trace_generating_function"]["denominator"]
    d0 = Fraction(den["d0"]["numerator"], den["d0"]["denominator"])
    d1 = Fraction(den["d1"]["numerator"], den["d1"]["denominator"])
    d2 = Fraction(den["d2"]["numerator"], den["d2"]["denominator"])
    d3 = Fraction(den["d3"]["numerator"], den["d3"]["denominator"])
    d4 = Fraction(den["d4"]["numerator"], den["d4"]["denominator"])

    # t_n = r1*t_{n-1}+r2*t_{n-2}+r3*t_{n-3}+r4*t_{n-4}
    r1 = -d1 / d0
    r2 = -d2 / d0
    r3 = -d3 / d0
    r4 = -d4 / d0

    traces = [_trace(_mat_pow(P, n)) for n in range(1, max_power + 1)]

    rec_generated = [traces[0], traces[1], traces[2], traces[3]]
    for n in range(5, max_power + 1):
        t_n = (
            r1 * rec_generated[n - 2]
            + r2 * rec_generated[n - 3]
            + r3 * rec_generated[n - 4]
            + r4 * rec_generated[n - 5]
        )
        rec_generated.append(t_n)

    identities = {
        "upstream_trace_gf_identities_hold": bool(tgf["summary"]["all_identities_hold"]),
        "denominator_shape_matches_expected": (d0, d1, d2, d3, d4)
        == (
            Fraction(1, 1),
            Fraction(-1, 1),
            Fraction(-21, 64),
            Fraction(161, 512),
            Fraction(7, 512),
        ),
        "trace_recurrence_matches_matrix_traces": rec_generated == traces,
    }

    summary = TraceRecurrenceSummary(
        checked_max_power=max_power,
        coeff_r1_num=r1.numerator,
        coeff_r1_den=r1.denominator,
        coeff_r2_num=r2.numerator,
        coeff_r2_den=r2.denominator,
        coeff_r3_num=r3.numerator,
        coeff_r3_den=r3.denominator,
        coeff_r4_num=r4.numerator,
        coeff_r4_den=r4.denominator,
        seed_t1_num=traces[0].numerator,
        seed_t1_den=traces[0].denominator,
        seed_t2_num=traces[1].numerator,
        seed_t2_den=traces[1].denominator,
        seed_t3_num=traces[2].numerator,
        seed_t3_den=traces[2].denominator,
        seed_t4_num=traces[3].numerator,
        seed_t4_den=traces[3].denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "recurrence": {
            "equation": "t_n = t_{n-1} + (21/64)t_{n-2} - (161/512)t_{n-3} - (7/512)t_{n-4}, n>=5",
            "coefficients": {
                "r1": {"numerator": r1.numerator, "denominator": r1.denominator},
                "r2": {"numerator": r2.numerator, "denominator": r2.denominator},
                "r3": {"numerator": r3.numerator, "denominator": r3.denominator},
                "r4": {"numerator": r4.numerator, "denominator": r4.denominator},
            },
        },
        "trace_seeds": {
            f"t{n+1}": {"numerator": tr.numerator, "denominator": tr.denominator}
            for n, tr in enumerate(traces[:4])
        },
        "identities": identities,
        "notes": (
            "The denominator of the exact trace generating function yields a closed "
            "order-4 recurrence for Tr(P^n), verified against exact matrix-power traces."
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
