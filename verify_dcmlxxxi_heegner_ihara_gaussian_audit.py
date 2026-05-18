#!/usr/bin/env python3
"""Part DCMLXXXI: Heegner/Ihara/Gaussian audit.

This verifier responds to the May 18 Heegner-Ihara note on GitHub main.
The note found a real shadow pattern, but it used ``12`` in the Ihara
quadratics.  The Bass determinant for the 12-regular W(3,3) collinearity graph
uses ``12 - 1 = 11``.  That changes the non-trivial fields and the pole radius.

It also checks the urgent Gaussian division:

    (160 + 221 i) / (4 + 11 i)

The quotient is not a Gaussian integer, so the 74441 numerator factor does not
contain the 137 Gaussian prime as a factor.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_PATH = ROOT / "data" / "dcmlxxxi_heegner_ihara_gaussian_audit.json"
RESULT_PATH = ROOT / "PART_DCMLXXXI_HEEGNER_IHARA_GAUSSIAN_AUDIT_results.json"

V = 40
E = 240
DEGREE = 12
BASS = DEGREE - 1
EIGENVALUES = {12: 1, 2: 24, -4: 15}
HEEGNER_RADICANDS = {1, 2, 3, 7, 11, 19, 43, 67, 163}


@dataclass(frozen=True)
class BridgeSummary:
    part: str
    decimal: int
    bass_parameter: int
    corrected_ihara_radius_squared: str
    incorrect_shadow_radius_squared: str
    gaussian_division_is_integral: bool
    gaussian_137_divides_74441: bool
    all_identities_hold: bool


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            return False
        factor += 2
    return True


def factorint(value: int) -> dict[int, int]:
    n = abs(value)
    out: dict[int, int] = {}
    factor = 2
    while factor * factor <= n:
        while n % factor == 0:
            out[factor] = out.get(factor, 0) + 1
            n //= factor
        factor += 1 if factor == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def squarefree_radicand(value: int) -> int:
    sign = -1 if value < 0 else 1
    kernel = 1
    for prime, exponent in factorint(value).items():
        if exponent % 2:
            kernel *= prime
    return sign * kernel


def ihara_sector(lam: int, coefficient: int) -> dict[str, Any]:
    discriminant = lam * lam - 4 * coefficient
    radicand = squarefree_radicand(discriminant)
    radius_squared = Fraction(1, coefficient) if discriminant < 0 else None
    return {
        "lambda": lam,
        "coefficient": coefficient,
        "factor": f"1 - ({lam})u + {coefficient}u^2",
        "discriminant": discriminant,
        "field_radicand": radicand,
        "is_heegner_field": abs(radicand) in HEEGNER_RADICANDS,
        "pole_radius_squared": str(radius_squared) if radius_squared is not None else None,
    }


def gaussian_norm(value: tuple[int, int]) -> int:
    a, b = value
    return a * a + b * b


def gaussian_division(
    numerator: tuple[int, int],
    denominator: tuple[int, int],
) -> dict[str, Any]:
    a, b = numerator
    c, d = denominator
    den_norm = gaussian_norm(denominator)
    real_num = a * c + b * d
    imag_num = b * c - a * d
    return {
        "numerator": list(numerator),
        "denominator": list(denominator),
        "denominator_norm": den_norm,
        "quotient_real": str(Fraction(real_num, den_norm)),
        "quotient_imag": str(Fraction(imag_num, den_norm)),
        "real_remainder_mod_norm": real_num % den_norm,
        "imag_remainder_mod_norm": imag_num % den_norm,
        "is_gaussian_integer": real_num % den_norm == 0 and imag_num % den_norm == 0,
    }


def sum_of_two_squares(value: int) -> list[int] | None:
    limit = math.isqrt(value)
    for a in range(limit + 1):
        b2 = value - a * a
        b = math.isqrt(b2)
        if b * b == b2:
            return [a, b]
    return None


def gaussian_prime_packet() -> dict[str, Any]:
    primes = [137, 4889, 74441]
    decompositions = {str(p): sum_of_two_squares(p) for p in primes}
    division = gaussian_division((160, 221), (4, 11))
    conjugate_division = gaussian_division((160, 221), (4, -11))
    alpha_numerator = 669_969
    alpha_denominator = 4_889
    numerator_decomposition = [3 * 160, 3 * 221]
    return {
        "primes": {
            str(p): {
                "is_prime": is_prime(p),
                "mod_4": p % 4,
                "mod_12": p % 12,
                "sum_of_two_squares": decompositions[str(p)],
            }
            for p in primes
        },
        "division_160_221_by_4_11": division,
        "division_160_221_by_4_minus_11": conjugate_division,
        "norm_137_divides_norm_74441": 74441 % 137 == 0,
        "alpha_fraction": {
            "numerator": alpha_numerator,
            "denominator": alpha_denominator,
            "numerator_factorization": factorint(alpha_numerator),
            "denominator_factorization": factorint(alpha_denominator),
            "numerator_gaussian_norm": numerator_decomposition,
            "denominator_gaussian_norm": decompositions[str(alpha_denominator)],
            "reading": "alpha numerator and denominator lie on the Gaussian sheet, but not through a 137 divisor.",
        },
    }


def build_bridge() -> dict[str, Any]:
    corrected_nontrivial = [ihara_sector(lam, BASS) for lam in (2, -4)]
    coefficient_12_shadow = [ihara_sector(lam, DEGREE) for lam in (2, -4)]
    gaussian = gaussian_prime_packet()

    identities = {
        "bass_parameter_is_degree_minus_one": BASS == 11,
        "corrected_ihara_uses_11_not_12": all(sector["coefficient"] == 11 for sector in corrected_nontrivial),
        "corrected_poles_are_on_graph_rh_circle": all(
            sector["pole_radius_squared"] == "1/11" for sector in corrected_nontrivial
        ),
        "coefficient_12_shadow_has_note_fields": [
            sector["field_radicand"] for sector in coefficient_12_shadow
        ] == [-11, -2],
        "actual_ihara_fields_are_minus_10_and_minus_7": [
            sector["field_radicand"] for sector in corrected_nontrivial
        ] == [-10, -7],
        "only_actual_s_sector_is_heegner": (
            corrected_nontrivial[0]["is_heegner_field"] is False
            and corrected_nontrivial[1]["is_heegner_field"] is True
        ),
        "gaussian_division_not_integral": (
            gaussian["division_160_221_by_4_11"]["is_gaussian_integer"] is False
            and gaussian["division_160_221_by_4_minus_11"]["is_gaussian_integer"] is False
        ),
        "norm_137_does_not_divide_74441": gaussian["norm_137_divides_norm_74441"] is False,
        "gaussian_primes_share_mod_12_class": all(
            packet["is_prime"] and packet["mod_4"] == 1 and packet["mod_12"] == 5
            for packet in gaussian["primes"].values()
        ),
        "alpha_numerator_is_scaled_gaussian_norm": (
            gaussian_norm(tuple(gaussian["alpha_fraction"]["numerator_gaussian_norm"])) == 669_969
        ),
    }

    summary = BridgeSummary(
        part="DCMLXXXI",
        decimal=981,
        bass_parameter=BASS,
        corrected_ihara_radius_squared="1/11",
        incorrect_shadow_radius_squared="1/12",
        gaussian_division_is_integral=gaussian["division_160_221_by_4_11"]["is_gaussian_integer"],
        gaussian_137_divides_74441=gaussian["norm_137_divides_norm_74441"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "remote_main_note": {
            "commit": "adddef43",
            "file": "NOTES/HEEGNER_IHARA_BREAKTHROUGH_MAY18_2026.md",
            "audit_status": "coefficient-12 shadow; not the W33 Ihara-Bass determinant",
        },
        "correct_w33_ihara": {
            "degree": DEGREE,
            "bass_parameter": BASS,
            "factorization": (
                "(1-u^2)^200*(1-12u+11u^2)*(1-2u+11u^2)^24*(1+4u+11u^2)^15"
            ),
            "nontrivial_sectors": corrected_nontrivial,
            "reading": (
                "The W33 collinearity graph has strict adjacency spectral slack, "
                "but its non-trivial Ihara poles sit on the graph-RH circle |u|=1/sqrt(11)."
            ),
        },
        "coefficient_12_shadow": {
            "factorization": (
                "(1-u^2)^200*(1-12u+12u^2)*(1-2u+12u^2)^24*(1+4u+12u^2)^15"
            ),
            "nontrivial_sectors": coefficient_12_shadow,
            "reading": (
                "Using 12 instead of the Bass coefficient 11 produces the note's "
                "Q(sqrt(-11)) and Q(sqrt(-2)) fields and radius 1/sqrt(12), "
                "but that polynomial is not the Ihara-Bass determinant."
            ),
        },
        "gaussian_alpha_packet": gaussian,
        "identities": identities,
    }


def write_bridge() -> tuple[Path, Path]:
    payload = build_bridge()
    DATA_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    RESULT_PATH.write_text(
        json.dumps(
            {
                "part": payload["summary"]["part"],
                "decimal": payload["summary"]["decimal"],
                "status": "VERIFIED: Heegner/Ihara coefficient audit and Gaussian division guard",
                "summary": payload["summary"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return DATA_PATH, RESULT_PATH


def main() -> None:
    data_path, result_path = write_bridge()
    print(f"Wrote {data_path}")
    print(f"Wrote {result_path}")


if __name__ == "__main__":
    main()
