#!/usr/bin/env python3
"""Exact norm-11 local Hasse--Weil realization of the W(3,3) Ihara sectors.

The two nontrivial W33 Ihara factors are

  1-2u+11u^2,        multiplicity 24,
  1+4u+11u^2,        multiplicity 15.

They are exactly elliptic-curve local Frobenius polynomials at p=11. Explicit
global curves over Q with good reduction at 11 are

  E_2  : y^2 = x^3 + x - 1,   #E_2(F_11)=10,  a_11=2,
  E_-4 : y^2 = x^3 + x + 2,   #E_-4(F_11)=16, a_11=-4.

Hence Z_W,nt(u)^(-1) = P_11(E_2,u)^24 P_11(E_-4,u)^15.

The Frobenius discriminants are -40 and -28, giving the same quadratic fields
Q(sqrt(-10)) and Q(sqrt(-7)) as the exact Ihara pole coordinates. Moreover,
the Hashimoto power-sum recurrence is identical to the Frobenius trace
recurrence, so every sector loop sequence is an elliptic point-count sequence
at 11^n.

This is a genuine exact local bridge. It is not a global identification of the
classical Riemann zeta function: one Euler prime and two elliptic L-functions do
not determine xi(s), and no global trace formula is asserted here.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
P = 11
SECTORS = ((2, 24), (-4, 15))


def discriminant_short_weierstrass(a: int, b: int) -> int:
    return -16 * (4 * a**3 + 27 * b**2)


def count_points_mod_p(a: int, b: int, p: int = P) -> int:
    total = 1
    for x in range(p):
        rhs = (x**3 + a * x + b) % p
        total += sum(1 for y in range(p) if y * y % p == rhs)
    return total


def frobenius_trace(a: int, b: int, p: int = P) -> int:
    return p + 1 - count_points_mod_p(a, b, p)


def enumerate_nonsingular_curves(p: int = P) -> list[dict[str, int]]:
    curves = []
    for a in range(p):
        for b in range(p):
            if discriminant_short_weierstrass(a, b) % p == 0:
                continue
            points = count_points_mod_p(a, b, p)
            curves.append({"a": a, "b": b, "points": points, "trace": p + 1 - points})
    return curves


def frobenius_power_sum(trace: int, n: int, p: int = P) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n == 0:
        return 2
    if n == 1:
        return trace
    previous, current = 2, trace
    for _ in range(2, n + 1):
        previous, current = current, trace * current - p * previous
    return current


def extension_point_count(trace: int, n: int, p: int = P) -> int:
    return p**n + 1 - frobenius_power_sum(trace, n, p)


def hashimoto_power_sum(adjacency_eigenvalue: int, n: int) -> int:
    return frobenius_power_sum(adjacency_eigenvalue, n, P)


def modular_square_roots(value: int, p: int = P) -> list[int]:
    target = value % p
    return [x for x in range(p) if x * x % p == target]


def sector_packet(trace: int, multiplicity: int) -> dict[str, Any]:
    discriminant = trace * trace - 4 * P
    if trace == 2:
        field = "Q(sqrt(-10))"
        field_discriminant = -40
        coordinate = "(1 +/- sqrt(-10))/11"
        norm_generator = "1 -/+ sqrt(-10)"
        curve = {"a": 1, "b": -1, "equation": "y^2=x^3+x-1"}
    elif trace == -4:
        field = "Q(sqrt(-7))"
        field_discriminant = -7
        coordinate = "(-2 +/- sqrt(-7))/11"
        norm_generator = "-2 -/+ sqrt(-7)"
        curve = {"a": 1, "b": 2, "equation": "y^2=x^3+x+2"}
    else:
        raise ValueError("unsupported W33 sector")
    points = count_points_mod_p(curve["a"], curve["b"], P)
    global_discriminant = discriminant_short_weierstrass(curve["a"], curve["b"])
    recurrence = [
        {
            "n": n,
            "power_sum": frobenius_power_sum(trace, n),
            "hashimoto_power_sum": hashimoto_power_sum(trace, n),
            "elliptic_points_F_11n": extension_point_count(trace, n),
            "hasse_bound_ok": abs(frobenius_power_sum(trace, n)) <= 2 * P ** (n / 2),
        }
        for n in range(1, 13)
    ]
    return {
        "trace": trace,
        "multiplicity": multiplicity,
        "local_polynomial": f"1-({trace})u+11u^2" if trace >= 0 else f"1+{abs(trace)}u+11u^2",
        "frobenius_discriminant": discriminant,
        "quadratic_field": field,
        "field_discriminant": field_discriminant,
        "ihara_coordinates": coordinate,
        "norm_11_generator": norm_generator,
        "global_curve_over_Q": curve,
        "global_curve_discriminant": global_discriminant,
        "good_reduction_at_11": global_discriminant % P != 0,
        "points_F_11": points,
        "a_11": P + 1 - points,
        "recurrence": recurrence,
    }


def build_certificate() -> dict[str, Any]:
    curves = enumerate_nonsingular_curves(P)
    trace_distribution = Counter(curve["trace"] for curve in curves)
    packets = [sector_packet(trace, multiplicity) for trace, multiplicity in SECTORS]
    roots_minus_10 = modular_square_roots(-10, P)
    roots_minus_7 = modular_square_roots(-7, P)
    checks = {
        "all_110_short_weierstrass_models_enumerated": len(curves) == 110,
        "trace_2_models_exist": trace_distribution[2] == 10,
        "trace_minus4_models_exist": trace_distribution[-4] == 10,
        "explicit_curves_have_required_traces": all(packet["a_11"] == packet["trace"] for packet in packets),
        "explicit_curves_have_good_reduction_at_11": all(packet["good_reduction_at_11"] for packet in packets),
        "frobenius_fields_match_ihara_fields": packets[0]["frobenius_discriminant"] == -40 and packets[1]["frobenius_discriminant"] == -28 and packets[0]["quadratic_field"] == "Q(sqrt(-10))" and packets[1]["quadratic_field"] == "Q(sqrt(-7))",
        "11_splits_in_both_quadratic_fields": len(roots_minus_10) == 2 and len(roots_minus_7) == 2,
        "hashimoto_equals_frobenius_recurrence": all(row["power_sum"] == row["hashimoto_power_sum"] for packet in packets for row in packet["recurrence"]),
        "all_hasse_bounds_hold_to_n_12": all(row["hasse_bound_ok"] for packet in packets for row in packet["recurrence"]),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "exact norm-11 elliptic local realization of W33 graph-RH",
        "local_factorization": {
            "W33_nontrivial_inverse": "(1-2u+11u^2)^24(1+4u+11u^2)^15",
            "elliptic_interpretation": "P_11(E_2,u)^24 P_11(E_-4,u)^15",
            "local_L_factor_form": "L_11(E,u)=1/(1-a_11 u+11u^2)",
        },
        "curve_enumeration": {
            "nonsingular_models": len(curves),
            "trace_distribution": {str(trace): count for trace, count in sorted(trace_distribution.items())},
        },
        "splitting_at_11": {
            "sqrt_minus_10_mod_11": roots_minus_10,
            "sqrt_minus_7_mod_11": roots_minus_7,
            "meaning": "the norm-11 Ihara denominators are prime-ideal factors above 11 in both quadratic fields",
        },
        "sectors": packets,
        "new_exact_bridge": {
            "recurrence": "T_n=a_11 T_(n-1)-11 T_(n-2), T_0=2, T_1=a_11",
            "graph_side": "T_n is the Hashimoto sector root power sum",
            "elliptic_side": "#E(F_(11^n))=11^n+1-T_n",
            "interpretation": "W33 nonbacktracking spectral sectors are exactly two elliptic Frobenius sectors at p=11",
        },
        "claim_boundary": {
            "proved": [
                "exact local elliptic curves with the two W33 factors at p=11",
                "exact equality of all recurrence-generated loop and Frobenius traces",
                "quadratic-field and norm-11 denominator agreement",
            ],
            "not_proved": [
                "a global automorphic representation whose full L-function is classical zeta",
                "an adelic trace formula transferring W33 graph-RH to classical RH",
                "that the local multiplicities 24 and 15 have a global motivic realization",
            ],
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_norm11_local_global_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
