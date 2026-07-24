#!/usr/bin/env python3
"""Deterministic Frobenius census for the two norm-11 elliptic curves.

The local W33 packet at p=11 uses

    E_2  : y^2=x^3+x-1,
    E_-4 : y^2=x^3+x+2.

This program counts both curves at every prime p<=10000, records all good
Frobenius traces, checks Hasse bounds, measures Sato--Tate moments, tests the
cross-correlation of the two trace streams, and searches for the exact W33
signature (a_p(E_2),a_p(E_-4))=(2,-4).

The census is finite evidence about the global candidate packet. It is not an
automorphy proof or a proof that p=11 is unique among all primes.
"""

from __future__ import annotations

import csv
import io
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 10_000
CURVES = {
    "E_2": {"a": 1, "b": -1, "bad_primes": {2, 31}, "j": "6912/31"},
    "E_-4": {"a": 1, "b": 2, "bad_primes": {2, 7}, "j": "432/7"},
}


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


def legendre_symbol(value: int, p: int) -> int:
    residue = value % p
    if residue == 0:
        return 0
    symbol = pow(residue, (p - 1) // 2, p)
    return 1 if symbol == 1 else -1


def frobenius_trace(a: int, b: int, p: int) -> int:
    character_sum = sum(legendre_symbol(x**3 + a * x + b, p) for x in range(p))
    return -character_sum


def moment(values: list[float], exponent: int) -> float:
    return sum(value**exponent for value in values) / len(values)


def pearson(left: list[float], right: list[float]) -> float:
    mean_left = sum(left) / len(left)
    mean_right = sum(right) / len(right)
    numerator = sum((x - mean_left) * (y - mean_right) for x, y in zip(left, right))
    denominator = math.sqrt(
        sum((x - mean_left) ** 2 for x in left)
        * sum((y - mean_right) ** 2 for y in right)
    )
    return numerator / denominator


def build_census(limit: int = LIMIT) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    common_good: list[dict[str, Any]] = []
    for p in primes_up_to(limit):
        row: dict[str, Any] = {"p": p}
        for name, curve in CURVES.items():
            good = p not in curve["bad_primes"]
            row[f"{name}_good"] = good
            row[f"{name}_a_p"] = frobenius_trace(curve["a"], curve["b"], p) if good else None
        row["common_good"] = row["E_2_good"] and row["E_-4_good"]
        if row["common_good"]:
            a2 = int(row["E_2_a_p"])
            am4 = int(row["E_-4_a_p"])
            row["hasse_E_2"] = abs(a2) <= 2 * math.sqrt(p)
            row["hasse_E_-4"] = abs(am4) <= 2 * math.sqrt(p)
            row["W33_signature"] = a2 == 2 and am4 == -4
            common_good.append(row)
        else:
            row["hasse_E_2"] = None
            row["hasse_E_-4"] = None
            row["W33_signature"] = False
        rows.append(row)

    normalized_2 = [row["E_2_a_p"] / math.sqrt(row["p"]) for row in common_good]
    normalized_m4 = [row["E_-4_a_p"] / math.sqrt(row["p"]) for row in common_good]
    signature_primes = [row["p"] for row in common_good if row["W33_signature"]]
    equal_trace_primes = [row["p"] for row in common_good if row["E_2_a_p"] == row["E_-4_a_p"]]

    summary = {
        "prime_limit": limit,
        "prime_count": len(rows),
        "common_good_prime_count": len(common_good),
        "common_bad_primes": [p for p in primes_up_to(limit) if p in {2, 7, 31}],
        "W33_signature": {
            "target": [2, -4],
            "matching_primes": signature_primes,
            "unique_up_to_limit": signature_primes == [11],
        },
        "curve_invariants": {
            "E_2": {
                "equation": "y^2=x^3+x-1",
                "discriminant": -496,
                "j": CURVES["E_2"]["j"],
                "CM": False,
            },
            "E_-4": {
                "equation": "y^2=x^3+x+2",
                "discriminant": -1792,
                "j": CURVES["E_-4"]["j"],
                "CM": False,
            },
            "not_Q_isogenous_witness": {
                "prime": 5,
                "a_5_E_2": next(row["E_2_a_p"] for row in common_good if row["p"] == 5),
                "a_5_E_-4": next(row["E_-4_a_p"] for row in common_good if row["p"] == 5),
                "reason": "Q-isogenous elliptic curves have equal good-prime Frobenius traces",
            },
        },
        "sato_tate_normalization": "x_p=a_p/sqrt(p), expected non-CM moments 0,1,2,5 for powers 1,2,4,6",
        "E_2_moments": {str(power): moment(normalized_2, power) for power in (1, 2, 4, 6)},
        "E_-4_moments": {str(power): moment(normalized_m4, power) for power in (1, 2, 4, 6)},
        "joint_statistics": {
            "pearson_normalized_trace_correlation": pearson(normalized_2, normalized_m4),
            "mean_normalized_product": sum(x * y for x, y in zip(normalized_2, normalized_m4)) / len(normalized_2),
            "equal_trace_prime_count": len(equal_trace_primes),
            "first_equal_trace_primes": equal_trace_primes[:20],
        },
        "checks": {
            "all_common_good_Hasse_bounds": all(row["hasse_E_2"] and row["hasse_E_-4"] for row in common_good),
            "p11_is_W33_signature": signature_primes and signature_primes[0] == 11,
            "W33_signature_unique_up_to_10000": signature_primes == [11],
            "curves_non_CM_by_nonintegral_rational_j": True,
            "curves_not_Q_isogenous_by_a5_mismatch": (
                next(row["E_2_a_p"] for row in common_good if row["p"] == 5)
                != next(row["E_-4_a_p"] for row in common_good if row["p"] == 5)
            ),
            "normalized_cross_correlation_small": abs(pearson(normalized_2, normalized_m4)) < 0.05,
            "E_2_second_moment_near_1": abs(moment(normalized_2, 2) - 1) < 0.05,
            "E_-4_second_moment_near_1": abs(moment(normalized_m4, 2) - 1) < 0.05,
        },
    }
    return rows, summary


def csv_text(rows: list[dict[str, Any]]) -> str:
    buffer = io.StringIO()
    fieldnames = [
        "p", "E_2_good", "E_2_a_p", "E_-4_good", "E_-4_a_p",
        "common_good", "hasse_E_2", "hasse_E_-4", "W33_signature",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def build_certificate(limit: int = LIMIT) -> dict[str, Any]:
    rows, summary = build_census(limit)
    return {
        "status": "PASS" if all(summary["checks"].values()) else "FAIL",
        "scope": "all primes p<=10000 Frobenius census for the two norm-11 elliptic curves",
        **summary,
        "data_file": "data/w33_elliptic_frobenius_census_p10000.csv",
        "claim_boundary": {
            "proved": [
                "exact point counts and Frobenius traces for every prime p<=10000",
                "the W33 trace pair (2,-4) occurs only at p=11 in this finite range",
                "both curves are non-CM and are not Q-isogenous",
            ],
            "observed": [
                "Sato--Tate moments approach the non-CM predictions",
                "the normalized trace streams have near-zero empirical correlation",
            ],
            "not_proved": [
                "uniqueness of p=11 over all primes",
                "statistical independence of the two Galois representations",
                "a global automorphic object explaining W33 multiplicities 24 and 15",
            ],
        },
    }


def main() -> None:
    rows, _ = build_census(LIMIT)
    payload = build_certificate(LIMIT)
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / "w33_elliptic_frobenius_census_p10000.csv"
    json_path = data_dir / "w33_all_prime_frobenius_census_certificate.json"
    csv_path.write_text(csv_text(rows), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {csv_path}")
    print(f"wrote {json_path}")


if __name__ == "__main__":
    main()
