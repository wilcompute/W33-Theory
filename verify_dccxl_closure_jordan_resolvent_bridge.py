#!/usr/bin/env python3
"""Part DCCXL: closure Jordan-resolvent bridge.

DCCXXXIX gives the finite closure propagator

    K(a,b) = 2^{-(b-a)}  for a <= b.

On the six causal classes this is the upper-triangular Toeplitz matrix

    K = I + N + N^2 + ... + N^5 = (I - N)^(-1),

where N = (1/2)S and S is the one-step nilpotent shift.  Therefore the
closure semigroup is unipotent/Jordan: all eigenvalues are 1, K-I is
nilpotent of index 6, and log(K) is the finite nilpotent generator.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxix_closure_semigroup_propagator_bridge import (  # noqa: E402
    build_bridge as build_dccxxxix_bridge,
)


OUT_PATH = ROOT / "data" / "dccxl_closure_jordan_resolvent_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    causal_class_count: int
    nilpotent_index: int
    resolvent_trace: int
    resolvent_determinant: int
    all_identities_hold: bool


Matrix = list[list[Fraction]]


def _zero(n: int) -> Matrix:
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def _identity(n: int) -> Matrix:
    mat = _zero(n)
    for i in range(n):
        mat[i][i] = Fraction(1)
    return mat


def _add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def _scale(c: Fraction, a: Matrix) -> Matrix:
    return [[c * x for x in row] for row in a]


def _mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    out = _zero(n)
    for i in range(n):
        for j in range(n):
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(n))
    return out


def _pow(a: Matrix, exponent: int) -> Matrix:
    n = len(a)
    out = _identity(n)
    for _ in range(exponent):
        out = _mul(out, a)
    return out


def _is_zero(a: Matrix) -> bool:
    return all(x == 0 for row in a for x in row)


def _trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def _strict_upper_shift(n: int) -> Matrix:
    mat = _zero(n)
    for i in range(n - 1):
        mat[i][i + 1] = Fraction(1)
    return mat


def _frac(x: Fraction) -> dict[str, int]:
    return {"numerator": x.numerator, "denominator": x.denominator}


def _json_matrix(a: Matrix) -> list[list[dict[str, int]]]:
    return [[_frac(x) for x in row] for row in a]


def _matrix_from_propagator_table(table: list[list[dict[str, int]]]) -> Matrix:
    mat: Matrix = []
    for row in table:
        mat.append(
            [
                Fraction(cell["numerator"], cell["denominator"])
                for cell in row
            ]
        )
    return mat


def build_bridge() -> dict[str, Any]:
    dccxxxix = build_dccxxxix_bridge()
    propagator = _matrix_from_propagator_table(dccxxxix["propagator_table"])
    n = len(propagator)
    identity = _identity(n)
    shift = _strict_upper_shift(n)
    nilpotent_generator = _scale(Fraction(1, 2), shift)

    resolvent_sum = _zero(n)
    for power in range(n):
        resolvent_sum = _add(resolvent_sum, _pow(nilpotent_generator, power))

    inverse_factor = _sub(identity, nilpotent_generator)
    inverse_check = _mul(inverse_factor, propagator)
    strict_part = _sub(propagator, identity)

    log_generator = _zero(n)
    for power in range(1, n):
        log_generator = _add(
            log_generator,
            _scale(Fraction(1, power), _pow(nilpotent_generator, power)),
        )

    identities = {
        "propagator_matches_dccxxxix_table": propagator == resolvent_sum,
        "nilpotent_generator_has_index_six": (
            not _is_zero(_pow(nilpotent_generator, n - 1))
            and _is_zero(_pow(nilpotent_generator, n))
        ),
        "propagator_is_exact_resolvent": inverse_check == identity,
        "resolvent_is_unipotent_trace_six_det_one": (
            _trace(propagator) == n
            and all(propagator[i][i] == 1 for i in range(n))
        ),
        "strict_propagator_part_has_same_nilpotent_index": (
            not _is_zero(_pow(strict_part, n - 1))
            and _is_zero(_pow(strict_part, n))
        ),
        "log_generator_is_nilpotent": _is_zero(_pow(log_generator, n)),
        "log_generator_first_superdiagonal_is_one_half": all(
            log_generator[i][i + 1] == Fraction(1, 2) for i in range(n - 1)
        ),
        "maximal_propagator_entry_is_one_over_32": propagator[0][-1] == Fraction(1, 32),
    }

    summary = BridgeSummary(
        causal_class_count=n,
        nilpotent_index=n,
        resolvent_trace=int(_trace(propagator)),
        resolvent_determinant=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "operator_definition": {
            "shift": "S[i,i+1]=1 on six proper-time levels",
            "nilpotent_generator": "N=(1/2)S",
            "propagator": "K=(I-N)^(-1)=I+N+N^2+N^3+N^4+N^5",
            "log_generator": "log(K)=sum_{m=1}^5 N^m/m",
        },
        "matrices": {
            "nilpotent_generator": _json_matrix(nilpotent_generator),
            "propagator": _json_matrix(propagator),
            "strict_part": _json_matrix(strict_part),
            "log_generator": _json_matrix(log_generator),
        },
        "jordan_read": {
            "eigenvalues": ["1"] * n,
            "minimal_polynomial": "(x - 1)^6 for K; x^6 for K-I and N",
            "holonomy_link": (
                "The closure-time propagator is the finite unipotent/Jordan lift of the earlier "
                "nilpotent holonomy frontier: the remaining live datum is a nilpotent shift, "
                "now extended from one local slot to a six-level causal chain."
            ),
        },
        "theorem": (
            "The DCCXXXIX closure propagator is exactly the resolvent of a one-step nilpotent "
            "shift N=(1/2)S on six causal classes.  Thus K=(I-N)^(-1), K is unipotent "
            "with trace 6 and determinant 1, K-I is nilpotent of index 6, and log(K) is "
            "a finite nilpotent generator."
        ),
        "honesty_boundary": (
            "This is a finite matrix/operator theorem.  It does not identify the finite "
            "unipotent chain with a continuum heat kernel, Lorentzian propagator, or physical "
            "Hamiltonian without a separate limit/dynamics theorem."
        ),
        "identities": identities,
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
