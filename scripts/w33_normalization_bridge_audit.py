#!/usr/bin/env python3
"""Exact bridge between the W(3,q) adjacency family and the lift normalization.

This audit resolves the bookkeeping split that had accumulated between:

1. The per-vertex adjacency moments of the point graph W(3,q), and
2. The April 2026 `q^4 - 1` lift normalization used in the symbolic Ihara /
   uniqueness stack.

The bridge is exact:

  V(q)            = (q + 1)(q^2 + 1)
  N_lift(q)       = q^4 - 1 = (q - 1) V(q)
  N_nonzero(q)    = 2 V(q)
  N_zero(q)       = (q - 3) V(q)
  rho_nonzero(q)  = N_nonzero / N_lift = 2 / (q - 1)
  rho_zero(q)     = N_zero / N_lift = (q - 3) / (q - 1)

For every even moment:

  M_{2n}^lift(q) = rho_nonzero(q) * M_{2n}^adj(q)

So the apparent q=3 uniqueness in the lift-normalized M_2 formula is not a
contradiction with k-regularity. It is exactly the statement that rho_nonzero
equals 1 iff q=3, i.e. the zero-mode sector vanishes only there.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from scripts.w3q_scaling_family import w3q_parameters, w3q_spectral_data


def _validate_q(q_value: int) -> int:
    if not isinstance(q_value, int) or q_value < 3:
        raise ValueError("q must be an integer >= 3 for the lift bridge audit")
    return q_value


def point_graph_vertex_count(q_value: int) -> int:
    q_value = _validate_q(q_value)
    vertex_count, _, _, _ = w3q_parameters(q_value)
    return vertex_count


def lift_mode_count(q_value: int) -> int:
    q_value = _validate_q(q_value)
    return q_value**4 - 1


def nonzero_lift_mode_count(q_value: int) -> int:
    q_value = _validate_q(q_value)
    return 2 * point_graph_vertex_count(q_value)


def zero_mode_count(q_value: int) -> int:
    q_value = _validate_q(q_value)
    return lift_mode_count(q_value) - nonzero_lift_mode_count(q_value)


def nonzero_mode_fraction(q_value: int) -> Fraction:
    q_value = _validate_q(q_value)
    return Fraction(nonzero_lift_mode_count(q_value), lift_mode_count(q_value))


def zero_mode_fraction(q_value: int) -> Fraction:
    q_value = _validate_q(q_value)
    return Fraction(zero_mode_count(q_value), lift_mode_count(q_value))


def normalization_factor(q_value: int) -> Fraction:
    q_value = _validate_q(q_value)
    return Fraction(2, q_value - 1)


def adjacency_even_moment_per_vertex(q_value: int, index: int) -> Fraction:
    q_value = _validate_q(q_value)
    if index < 0:
        raise ValueError("index must be nonnegative")

    vertex_count = point_graph_vertex_count(q_value)
    degree, positive_eigenvalue, negative_eigenvalue = None, None, None
    vertex_count, degree, _, _ = w3q_parameters(q_value)
    spectral = w3q_spectral_data(q_value)
    positive_eigenvalue, negative_eigenvalue = spectral["adjacency_eigenvalues"]
    positive_mult, negative_mult = spectral["multiplicities"]
    power = 2 * index
    numerator = (
        degree**power
        + positive_mult * (positive_eigenvalue**power)
        + negative_mult * (negative_eigenvalue**power)
    )
    return Fraction(numerator, vertex_count)


def lift_even_moment(q_value: int, index: int) -> Fraction:
    q_value = _validate_q(q_value)
    if index < 0:
        raise ValueError("index must be nonnegative")

    spectral = w3q_spectral_data(q_value)
    _, degree, _, _ = w3q_parameters(q_value)
    positive_eigenvalue, negative_eigenvalue = spectral["adjacency_eigenvalues"]
    positive_mult, negative_mult = spectral["multiplicities"]
    power = 2 * index
    numerator = (
        2 * degree**power
        + 2 * positive_mult * (positive_eigenvalue**power)
        + 2 * negative_mult * (negative_eigenvalue**power)
    )
    return Fraction(numerator, lift_mode_count(q_value))


def _fraction_payload(value: Fraction) -> Dict[str, object]:
    return {"exact": str(value), "float": float(value)}


@lru_cache(maxsize=1)
def symbolic_bridge_summary() -> Dict[str, object]:
    q = sp.Symbol("q", positive=True)
    vertex_count = (q + 1) * (q**2 + 1)
    lift_modes = q**4 - 1
    nonzero_modes = 2 * vertex_count
    zero_modes = sp.factor(lift_modes - nonzero_modes)
    rho_nonzero = sp.factor(sp.simplify(nonzero_modes / lift_modes))
    rho_zero = sp.factor(sp.simplify(zero_modes / lift_modes))
    k_q = q * (q + 1)
    f_q = q * (q + 1) ** 2 / 2
    g_q = q * (q**2 + 1) / 2

    def adjacency_even(index: int) -> sp.Expr:
        numerator = k_q ** (2 * index) + f_q * (q - 1) ** (2 * index) + g_q * (q + 1) ** (2 * index)
        return sp.factor(sp.simplify(numerator / vertex_count))

    def lift_even(index: int) -> sp.Expr:
        numerator = 2 * k_q ** (2 * index) + 2 * f_q * (q - 1) ** (2 * index) + 2 * g_q * (q + 1) ** (2 * index)
        return sp.factor(sp.simplify(numerator / lift_modes))

    m2_adj = adjacency_even(1)
    m2_lift = lift_even(1)
    m4_adj = adjacency_even(2)
    m4_lift = lift_even(2)

    return {
        "vertex_count_formula": str(sp.expand(vertex_count)),
        "lift_mode_formula": str(sp.expand(lift_modes)),
        "lift_factorization": str(sp.factor(lift_modes)),
        "zero_mode_formula": str(zero_modes),
        "rho_nonzero": str(rho_nonzero),
        "rho_zero": str(rho_zero),
        "m2_adjacency": str(m2_adj),
        "m2_lift": str(m2_lift),
        "m4_adjacency": str(m4_adj),
        "m4_lift": str(m4_lift),
        "bridge_theorem_exact": {
            "lift_modes_equal_q_minus_1_times_vertex_count": sp.expand(lift_modes - (q - 1) * vertex_count) == 0,
            "zero_modes_equal_q_minus_3_times_vertex_count": zero_modes == (q - 3) * vertex_count,
            "rho_nonzero_is_2_over_q_minus_1": rho_nonzero == sp.Rational(2, 1) / (q - 1),
            "rho_zero_is_q_minus_3_over_q_minus_1": rho_zero == (q - 3) / (q - 1),
            "m2_bridge_holds": sp.simplify(m2_lift - rho_nonzero * m2_adj) == 0,
            "m4_bridge_holds": sp.simplify(m4_lift - rho_nonzero * m4_adj) == 0,
            "m2_gap_is_exactly_zero_fraction_times_k": sp.factor(m2_lift - k_q) == -q * (q - 3) * (q + 1) / (q - 1),
        },
    }


def normalization_bridge_record(q_value: int) -> Dict[str, object]:
    q_value = _validate_q(q_value)
    vertex_count, degree, lam, mu = w3q_parameters(q_value)
    spectral = w3q_spectral_data(q_value)

    m2_adj = adjacency_even_moment_per_vertex(q_value, 1)
    m4_adj = adjacency_even_moment_per_vertex(q_value, 2)
    m2_lift = lift_even_moment(q_value, 1)
    m4_lift = lift_even_moment(q_value, 2)
    rho_nonzero = nonzero_mode_fraction(q_value)
    rho_zero = zero_mode_fraction(q_value)

    return {
        "q": q_value,
        "srg_parameters": (vertex_count, degree, lam, mu),
        "adjacency_eigenvalues": spectral["adjacency_eigenvalues"],
        "adjacency_multiplicities": spectral["multiplicities"],
        "point_graph_vertex_count": vertex_count,
        "lift_mode_count": lift_mode_count(q_value),
        "nonzero_lift_mode_count": nonzero_lift_mode_count(q_value),
        "zero_mode_count": zero_mode_count(q_value),
        "rho_nonzero": _fraction_payload(rho_nonzero),
        "rho_zero": _fraction_payload(rho_zero),
        "normalization_factor": _fraction_payload(normalization_factor(q_value)),
        "moments": {
            "adjacency_m2": _fraction_payload(m2_adj),
            "lift_m2": _fraction_payload(m2_lift),
            "adjacency_m4": _fraction_payload(m4_adj),
            "lift_m4": _fraction_payload(m4_lift),
        },
        "exact_factorizations": {
            "lift_modes_equal_q_minus_1_times_vertex_count": lift_mode_count(q_value) == (q_value - 1) * vertex_count,
            "nonzero_lift_modes_equal_twice_vertex_count": nonzero_lift_mode_count(q_value) == 2 * vertex_count,
            "zero_modes_equal_q_minus_3_times_vertex_count": zero_mode_count(q_value) == (q_value - 3) * vertex_count,
            "rho_nonzero_equals_2_over_q_minus_1": rho_nonzero == Fraction(2, q_value - 1),
            "rho_zero_equals_q_minus_3_over_q_minus_1": rho_zero == Fraction(q_value - 3, q_value - 1),
            "m2_bridge_holds": m2_lift == rho_nonzero * m2_adj,
            "m4_bridge_holds": m4_lift == rho_nonzero * m4_adj,
            "q3_is_exactly_the_zero_mode_free_case": (q_value == 3) == (zero_mode_count(q_value) == 0),
            "q3_is_exactly_the_factor_1_case": (q_value == 3) == (normalization_factor(q_value) == 1),
        },
    }


@lru_cache(maxsize=1)
def analyze(q_values: Tuple[int, ...] = (3, 4, 5, 7, 9, 11)) -> Dict[str, object]:
    records = tuple(normalization_bridge_record(q_value) for q_value in q_values)
    symbolic = symbolic_bridge_summary()

    return {
        "status": "ok",
        "symbolic_bridge": symbolic,
        "records": records,
        "bridge_theorem": {
            "the_lift_normalization_is_exactly_the_nonzero_mode_fraction": all(
                record["normalization_factor"]["exact"] == record["rho_nonzero"]["exact"]
                for record in records
            ),
            "the_zero_mode_fraction_is_exactly_one_minus_the_nonzero_fraction": all(
                Fraction(record["rho_zero"]["exact"]) + Fraction(record["rho_nonzero"]["exact"]) == 1
                for record in records
            ),
            "q3_is_the_unique_zero_mode_free_case_in_the_sample": tuple(
                record["q"] for record in records if record["zero_mode_count"] == 0
            ) == (3,),
            "q3_is_the_unique_factor_1_case_in_the_sample": tuple(
                record["q"] for record in records if record["normalization_factor"]["exact"] == "1"
            ) == (3,),
            "the_april_m2_uniqueness_gap_is_exactly_the_normalization_gap": all(
                record["moments"]["lift_m2"]["exact"] == str(
                    Fraction(record["normalization_factor"]["exact"]) * Fraction(record["moments"]["adjacency_m2"]["exact"])
                )
                for record in records
            ),
        },
        "boundary_note": (
            "This audit does not add a new physical theorem. It resolves an exact bookkeeping split: "
            "the April 2026 lift-normalized moment family is the ordinary per-vertex W(3,q) moment family "
            "multiplied by the nonzero-mode occupancy factor 2/(q-1). The q=3 uniqueness statement is "
            "therefore exactly the vanishing of the zero-mode sector, not a contradiction with "
            "k-regularity on the graph side."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXVII_normalization_bridge_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    q3 = normalization_bridge_record(3)
    print("Normalization bridge audit")
    print(
        "  q=3: "
        f"V={q3['point_graph_vertex_count']}, "
        f"lift_modes={q3['lift_mode_count']}, "
        f"zero_modes={q3['zero_mode_count']}, "
        f"factor={q3['normalization_factor']['exact']}"
    )
    print(
        "  Theorem: "
        f"rho_nonzero(q) = {payload['symbolic_bridge']['rho_nonzero']}, "
        f"rho_zero(q) = {payload['symbolic_bridge']['rho_zero']}"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
