#!/usr/bin/env python3
"""Operational corollary of the exact two-qutrit UMUB SOS bounds.

No experimental data: assumes pure states, per-effect operator-norm
calibration, independent repeated shots per context, and Hoeffding/union.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "w33_exact_mub_sym2_blocks_20261109.json"
OUT = ROOT / "data" / "w33_20261109_umub_operational_margin.json"


def margin(k: int, delta: Fraction, epsilon: Fraction,
           shots_per_basis: int, alpha: float) -> dict:
    if k < 1 or delta <= 0 or not (0 <= epsilon < 1):
        raise ValueError("invalid MUB witness inputs")
    if shots_per_basis < 1 or not (0 < alpha < 1):
        raise ValueError("invalid sampling inputs")
    m = 9 * k
    guaranteed_squared_bias = delta / m
    guaranteed_bias = math.sqrt(float(guaranteed_squared_bias))
    # Each context has N i.i.d. categorical trials. Each coordinate is a
    # Bernoulli indicator; union bound does not require the 9 within-basis
    # outcome frequencies to be mutually independent.
    hoeffding_error = math.sqrt(math.log(2 * m / alpha)
                                / (2 * shots_per_basis))
    worst_case_observed_bias = max(
        0.0, guaranteed_bias - float(epsilon) - hoeffding_error
    )
    return {
        "bases": k,
        "outcomes": m,
        "sos_delta": str(delta),
        "one_outcome_minimum_bias_squared": str(guaranteed_squared_bias),
        "one_outcome_ideal_minimum_absolute_bias": guaranteed_bias,
        "each_effect_operator_norm_error_bound": str(epsilon),
        "shots_per_basis": shots_per_basis,
        "total_shots": k * shots_per_basis,
        "failure_probability_max": alpha,
        "simultaneous_hoeffding_error": hoeffding_error,
        "guaranteed_observed_one_outcome_bias": worst_case_observed_bias,
        "positive_detection_margin": worst_case_observed_bias > 0,
    }


def compute():
    certificate = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert certificate["status"] == "PASS_EXACT_Z_OMEGA_EXHAUSTIVE"
    assert certificate["spectra_of_H_on_Sym2"]["5"]["lower_bound"] == "1/9"
    assert certificate["spectra_of_H_on_Sym2"]["8"]["lower_bound"] == "4/9"
    eps = Fraction(1, 100)
    rows = [margin(k, Fraction(certificate["spectra_of_H_on_Sym2"][str(k)]["lower_bound"]),
                   eps, 20000, 0.01) for k in (5, 8)]
    assert all(row["positive_detection_margin"] for row in rows)
    assert all(row["guaranteed_observed_one_outcome_bias"] > 0.02 for row in rows)
    result = {
        "status": "PASS_CONDITIONAL_OPERATIONAL_BIAS_BOUNDS",
        "source": "data/w33_exact_mub_sym2_blocks_20261109.json",
        "hypotheses": [
            "input state pure in dimension 9",
            "nine labelled outcomes per each of k measurement contexts",
            "actual POVM effects E_j satisfy ||E_j - P_j||_op <= epsilon",
            "each of k contexts sampled N times from independent identical trials",
            "all deviations are from exactly 1/9; alpha is union-bound failure probability"
        ],
        "derivation": "sqrt(sum_j(p_j-1/9)^2) >= sqrt(delta); perturbation L2 <= sqrt(9k)*epsilon; uniform simultaneous Hoeffding error <= sqrt(ln(18k/alpha)/(2N)); therefore some observed |p_hat-1/9| >= sqrt(delta/(9k))-epsilon-Hoeffding with probability >= 1-alpha",
        "rows": rows,
        "counterexample": "The completely mixed rho=I/9 gives uniform probabilities for every ideal basis; this result does not extend to arbitrary mixed states without a purity/distance hypothesis",
        "qualification": "Conservative conditional finite-shot bound, not a lab measurement, detector calibration, quantum error threshold, or TOE prediction."
    }
    return result


if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    result = compute()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for row in result["rows"]:
        print("k=%d ideal=%.8f epsilon=%s Hoeffding=%.8f observed_lower=%.8f"
              % (row["bases"], row["one_outcome_ideal_minimum_absolute_bias"],
                 row["each_effect_operator_norm_error_bound"],
                 row["simultaneous_hoeffding_error"],
                 row["guaranteed_observed_one_outcome_bias"]))
