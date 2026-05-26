#!/usr/bin/env python3
"""W(3,3) cyclotomic genus reciprocal-sheet theorem.

This continues the MCCLXVI-MCCLXXV cyclotomic spectral algebra packet after
the corrected MCCLXVIII sign convention.  The useful object is not one
positive-temperature oscillator, but a reciprocal pair of live/dual sheets.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path


Q = 3
V = 40
K = 12
R = 2
S = -4
MU = 4
F_MULT = 24
G_MULT = 15
P_IH = 11
PHI3 = 13
PHI6 = 7
ALPHA_INV = 137


def factorial(n: int) -> int:
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def mobius(n: int) -> int:
    if n == 1:
        return 1
    factors: list[int] = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            temp //= d
            if temp % d == 0:
                return 0
        d += 1
    if temp > 1:
        factors.append(temp)
    return (-1) ** len(factors)


def cyclotomic_value(n: int, q: int) -> int:
    result = Fraction(1)
    for d in range(1, n + 1):
        if n % d:
            continue
        mu = mobius(n // d)
        if mu == 1:
            result *= q**d - 1
        elif mu == -1:
            result /= q**d - 1
    assert result.denominator == 1
    return result.numerator


def pisano_period(modulus: int) -> int:
    prev, curr = 0, 1
    for period in range(1, modulus * modulus * 2 + 1):
        prev, curr = curr, (prev + curr) % modulus
        if prev == 0 and curr == 1:
            return period
    raise RuntimeError(f"Pisano period search failed for {modulus}")


def wq_spectral_data(q: int) -> dict[str, Fraction | int]:
    v = (q**4 - 1) // (q - 1)
    k = q * (q + 1)
    r = q - 1
    mu = q + 1
    f = k * r
    g = (v - 1) - f
    g1 = Fraction(q**3 + g, 2)
    g2 = Fraction(q**3 - g, 2)
    e_low = k - r
    e_high = k + mu
    return {
        "v": v,
        "k": k,
        "r": r,
        "mu": mu,
        "f": f,
        "g": g,
        "g1": g1,
        "g2": g2,
        "e_low": e_low,
        "e_high": e_high,
        "gap": e_high - e_low,
        "phi6": q**2 - q + 1,
    }


def omega_live(beta: float) -> float:
    return 21 * math.exp(-10 * beta) - 6 * math.exp(-16 * beta)


def omega_dual(beta: float) -> float:
    return 21 * math.exp(-16 * beta) - 6 * math.exp(-10 * beta)


def fraction_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def generate_payload() -> dict:
    g1 = (Q**3 + G_MULT) // 2
    g2 = (Q**3 - G_MULT) // 2
    e_low = K - R
    e_high = K + MU
    gap = e_high - e_low
    beta_plus = math.log(Fraction(PHI6, R)) / gap
    beta_minus = -beta_plus

    live_derivative_now = -g1 * e_low + g2 * e_high
    dual_derivative_now = -g1 * e_high + g2 * e_low
    derivative_center = Fraction(live_derivative_now + dual_derivative_now, 2)
    derivative_half_split = Fraction(live_derivative_now - dual_derivative_now, 2)

    ratio_witnesses = []
    for q in range(3, 15):
        data = wq_spectral_data(q)
        lhs = data["g1"] / data["g2"]
        rhs = Fraction(data["phi6"], data["r"])
        ratio_witnesses.append(
            {
                "q": q,
                "g1_over_g2": fraction_string(lhs),
                "phi6_over_r": fraction_string(rhs),
                "equal": lhs == rhs,
            }
        )

    gap_factorial_witnesses = [
        {
            "q": q,
            "spectral_gap_2q": 2 * q,
            "q_factorial": factorial(q),
            "equal": 2 * q == factorial(q),
        }
        for q in range(1, 9)
    ]

    checks = {
        "live_root_is_negative_sheet": abs(omega_live(beta_minus)) < 1e-12,
        "dual_root_is_positive_sheet": abs(omega_dual(beta_plus)) < 1e-12,
        "root_variables_are_reciprocal": Fraction(PHI6, R) * Fraction(R, PHI6) == 1,
        "root_ratio_is_cyclotomic": Fraction(PHI6, R) == Fraction(g1, g2),
        "ratio_uniqueness_scanned_q3_to_q14": [
            item["q"] for item in ratio_witnesses if item["equal"]
        ]
        == [3],
        "ratio_uniqueness_factor": "q^3*(3-q)",
        "gap_is_factorial_clock_only_at_q3": [
            item["q"] for item in gap_factorial_witnesses if item["equal"]
        ]
        == [3],
        "nontrivial_gap_factorial_lock": 2 * Q == factorial(Q) == gap,
        "now_value_is_negative_multiplicity": omega_live(0) == omega_dual(0) == G_MULT,
        "heat_trace_now_is_vertex_count": 1 + F_MULT + G_MULT == V,
        "dual_now_derivative_is_pisano_alpha": -dual_derivative_now
        == pisano_period(ALPHA_INV),
        "derivatives_center_on_phi3_g": derivative_center == -PHI3 * G_MULT,
        "derivatives_split_by_q4": derivative_half_split == Q**4,
        "phi4_is_low_energy_and_pi11": cyclotomic_value(4, Q)
        == e_low
        == V // MU
        == pisano_period(P_IH),
        "phi5_is_ihara_square": cyclotomic_value(5, Q) == P_IH**2,
    }

    verified = sum(1 for value in checks.values() if value is True)
    total_boolean_checks = sum(1 for value in checks.values() if isinstance(value, bool))

    payload = {
        "theorem": "MCCLXXVI_CYCLOTOMIC_GENUS_RECIPROCAL_SHEETS",
        "statement": (
            "The corrected W33 genus oscillator is a reciprocal live/dual "
            "two-sheet system.  The live sheet zero is beta=-ln(7/2)/6, "
            "the dual sheet zero is beta=+ln(7/2)/6, and the positive "
            "sheet's derivative at now equals -pi(137)."
        ),
        "constants": {
            "q": Q,
            "v": V,
            "k": K,
            "r": R,
            "mu": MU,
            "f": F_MULT,
            "g": G_MULT,
            "g1": g1,
            "g2": g2,
            "Phi3": PHI3,
            "Phi6": PHI6,
            "p_Ih": P_IH,
            "alpha_inverse_shadow": ALPHA_INV,
        },
        "energies": {
            "E_low": e_low,
            "E_high": e_high,
            "gap": gap,
            "gap_identity": "E_high-E_low=6=q!=2q",
        },
        "roots": {
            "beta_minus_live": beta_minus,
            "beta_plus_dual": beta_plus,
            "x_minus_exp_gap_beta": fraction_string(Fraction(R, PHI6)),
            "x_plus_exp_gap_beta": fraction_string(Fraction(PHI6, R)),
            "x_plus_times_x_minus": 1,
        },
        "now": {
            "Omega_live_0": omega_live(0),
            "Omega_dual_0": omega_dual(0),
            "Z_0": 1 + F_MULT + G_MULT,
            "live_derivative_0": live_derivative_now,
            "dual_derivative_0": dual_derivative_now,
            "derivative_center": fraction_string(derivative_center),
            "derivative_half_split": fraction_string(derivative_half_split),
            "pisano_137": pisano_period(ALPHA_INV),
        },
        "uniqueness": {
            "ratio_factor": "g1/g2=Phi6/r has numerator q^3*(3-q)",
            "ratio_scan": ratio_witnesses,
            "gap_factorial_scan": gap_factorial_witnesses,
        },
        "checks": checks,
        "verified_boolean_checks": verified,
        "total_boolean_checks": total_boolean_checks,
        "all_verified": verified == total_boolean_checks,
    }
    return payload


def main() -> None:
    payload = generate_payload()
    out = Path("PART_MCCLXXVI_CYCLOTOMIC_GENUS_RECIPROCAL_SHEETS_results.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("MCCLXXVI: CYCLOTOMIC GENUS RECIPROCAL SHEETS")
    print(f"verified: {payload['verified_boolean_checks']}/{payload['total_boolean_checks']}")
    print(f"beta- live = {payload['roots']['beta_minus_live']:.12f}")
    print(f"beta+ dual = {payload['roots']['beta_plus_dual']:.12f}")
    print(
        "dOmega_dual/dβ|0 = "
        f"{payload['now']['dual_derivative_0']} = -pi(137)"
    )
    if not payload["all_verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
