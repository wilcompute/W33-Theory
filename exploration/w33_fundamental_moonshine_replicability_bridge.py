"""The fundamental moonshine classes close one step higher by prime replicability.

The previous bridge fixed the base algebra:

    1A  : linear quotient algebra on the weight-12 plane,
    pA  : quadratic trace/norm algebra for p in {2,3,5,7,13}.

The next exact lift is the prime replicability relation.  For each Fricke prime
class pA, let

    T_p(q) = q^{-1} + sum_{n>=1} a_n^{(p)} q^n,
    J(q)   = T_{1A}(q) = q^{-1} + sum_{n>=1} c_n q^n.

Let Phi_p(x) be the p-th Faber polynomial of T_p, defined by

    Phi_p(T_p(q)) = q^{-p} + O(q).

Then the classical Fricke-prime replicability identity is

    Phi_p(T_p)(q) = J(q^p) + p (T_p |_U_p)(q),

where

    (T_p |_U_p)(q) = sum_{n>=1} a_{pn}^{(p)} q^n.

So the prime Hauptmoduls are not only quadratic trace/norm objects.  Their
next algebraic layer is sourced by the identity class 1A itself.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_fundamental_moonshine_replicability_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import (
    faber_polynomial_series,
    j_coeffs,
    mckay_thompson_series,
    verify_fricke_prime_replicability,
)


PRIME_CLASSES: list[tuple[str, int]] = [("2A", 2), ("3A", 3), ("5A", 5), ("7A", 7), ("13A", 13)]


def _rhs_replicability(series: dict[int, int], p: int, max_q_exp: int) -> dict[int, int]:
    rhs: dict[int, int] = {-p: 1}
    for n in range(1, max_q_exp + 1):
        rhs[n] = rhs.get(n, 0) + p * int(series.get(p * n, 0))

    j_needed = max_q_exp // p
    jpos = j_coeffs(j_needed)
    for n, c in enumerate(jpos, start=1):
        exp = p * n
        if exp <= max_q_exp:
            rhs[exp] = rhs.get(exp, 0) + int(c)
    return rhs


def _row(class_name: str, p: int, max_q_exp: int = 12) -> dict[str, Any]:
    series = mckay_thompson_series(class_name, max_q_exp=p * max_q_exp)
    if series is None:
        raise RuntimeError(f"Series unavailable for {class_name}")

    faber = faber_polynomial_series(series, m=p, max_q_exp=max_q_exp)
    lhs = dict(faber["series"])
    rhs = _rhs_replicability(series, p, max_q_exp)
    verification = verify_fricke_prime_replicability(class_name, max_q_exp=max_q_exp)

    a1 = int(series[1])
    a2 = int(series[2])
    coeffs = list(faber["coeffs"])

    top_linear = coeffs[-2] if p >= 2 else None
    next_linear = coeffs[-3] if p >= 3 else None

    return {
        "class_name": class_name,
        "p": p,
        "a1": a1,
        "a2": a2,
        "faber_coeffs": coeffs,
        "lhs_q_exponents": {str(e): int(lhs.get(e, 0)) for e in [-p] + list(range(1, max_q_exp + 1)) if lhs.get(e, 0) != 0},
        "rhs_q_exponents": {str(e): int(rhs.get(e, 0)) for e in [-p] + list(range(1, max_q_exp + 1)) if rhs.get(e, 0) != 0},
        "theorems": {
            "replicability_holds": bool(verification["verified"]),
            "faber_top_lower_coefficient_is_minus_p_times_a1": top_linear == -p * a1,
            "faber_next_lower_coefficient_is_minus_p_times_a2": next_linear == -p * a2 if p >= 3 else True,
        },
    }


def build_summary(max_q_exp: int = 12) -> dict[str, Any]:
    rows = [_row(class_name, p, max_q_exp=max_q_exp) for class_name, p in PRIME_CLASSES]

    return {
        "fundamental_moonshine_replicability_dictionary": {
            "prime_rows": rows,
            "identity_source_coeffs": j_coeffs(max_q_exp),
        },
        "fundamental_moonshine_replicability_theorem": {
            "all_five_prime_classes_satisfy_prime_replicability": all(
                row["theorems"]["replicability_holds"] for row in rows
            ),
            "the_faber_top_lower_coefficient_is_uniformly_minus_p_times_a1": all(
                row["theorems"]["faber_top_lower_coefficient_is_minus_p_times_a1"] for row in rows
            ),
            "the_faber_next_lower_coefficient_is_uniformly_minus_p_times_a2": all(
                row["theorems"]["faber_next_lower_coefficient_is_minus_p_times_a2"] for row in rows
            ),
            "the_prime_classes_close_one_step_higher_as_1A_sourced_faber_algebras": all(
                all(row["theorems"].values()) for row in rows
            ),
        },
        "interpretation": (
            "The prime Fricke classes are not only quadratic trace/norm algebras. "
            "Their p-th Faber polynomials are sourced by the identity class 1A "
            "through J(q^p), with the same class feeding back through the U_p operator. "
            "So the base moonshine spine lifts from linear/quadratic algebra to a "
            "replication algebra."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 FUNDAMENTAL MOONSHINE REPLICABILITY BRIDGE")
    print("=" * 72)
    for key, value in summary["fundamental_moonshine_replicability_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
