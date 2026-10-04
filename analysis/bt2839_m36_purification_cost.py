#!/usr/bin/env python3
"""Pass 2839: exact local cost law for repeated use of the explicit M36 branch."""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


def recurrence(p: float) -> float:
    return p * (4.0 - p) / (3.0 * (p * p - 2.0 * p + 2.0))


def success(p: float) -> float:
    return (p * p - 2.0 * p + 2.0) / 4.0


def expected_input_factor(p: float) -> float:
    return 2.0 / success(p)


def trajectory(p0: float, target: float, max_rounds: int = 500) -> dict:
    p = p0
    cost = 1.0
    for round_index in range(1, max_rounds + 1):
        cost *= expected_input_factor(p)
        p = recurrence(p)
        if p <= target:
            return {
                "p0": p0,
                "target": target,
                "rounds": round_index,
                "expected_raw_inputs_per_accepted_output": cost,
            }
    raise RuntimeError("target not reached")


def main() -> None:
    x = sp.symbols("x")
    exact_recurrence = x * (4 - x) / (3 * (x**2 - 2*x + 2))
    exact_cost = 8 / (x**2 - 2*x + 2)
    assert sp.diff(exact_recurrence, x).subs(x, 0) == sp.Rational(2, 3)
    assert sp.limit(exact_cost, x, 0) == 4
    assert sp.series(exact_recurrence, x, 0, 3) == sp.Rational(2, 3)*x + sp.Rational(1, 2)*x**2 + sp.Order(x**3)

    exponent = math.log(4.0) / math.log(1.5)
    assert abs(exponent - 3.4190225827029095) < 1e-15

    grid = [index / 10000.0 for index in range(1, 10000)]
    assert all(recurrence(value) < value for value in grid if value < 2.0 / 3.0)
    assert all(recurrence(value) > value for value in grid if value > 2.0 / 3.0)
    assert abs(recurrence(2.0 / 3.0) - 2.0 / 3.0) < 1e-15
    assert abs(success(0.0) - 0.5) < 1e-15
    assert abs(expected_input_factor(0.0) - 4.0) < 1e-15

    samples = [
        trajectory(p0, target)
        for p0 in (0.5, 1.0 / 3.0, 0.1)
        for target in (1e-3, 1e-6)
    ]
    result = {
        "schema": "w33.pass2839.m36_repeated_branch_cost.v1",
        "status": "EXACT_LOCAL_ASYMPTOTIC_AND_NUMERICAL_TRAJECTORIES",
        "check_count": 6,
        "checks": {
            "fixed_basin_direction": True,
            "small_error_slope_2_over_3": True,
            "limiting_success_one_half": True,
            "limiting_cost_four": True,
            "overhead_exponent": True,
            "sample_targets_reached": True,
        },
        "recurrence": "p(4-p)/(3(p^2-2p+2))",
        "success_probability": "(p^2-2p+2)/4",
        "accepted_outputs_per_raw_input": "P_succ/2",
        "expected_raw_input_factor_per_round": "2/P_succ = 8/(p^2-2p+2)",
        "purifying_basin": "0<p<2/3",
        "small_error_contraction": "p_next = (2/3)p + O(p^2)",
        "small_error_cost_factor": "2/P_succ = 4 + O(p)",
        "repeated_branch_overhead_exponent": {
            "formula": "log(4)/log(3/2)",
            "value": exponent,
        },
        "samples": samples,
        "claim_boundary": "Repeated use of one explicit iid-depolarizing branch; not an optimized protocol, a lower bound, or a fault-tolerant factory estimate."
    }
    out = Path(__file__).resolve().parents[1] / "data" / "PART_BT2839_M36_REPEATED_BRANCH_COST_results.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS 6/6 gamma", exponent)


if __name__ == "__main__":
    main()
