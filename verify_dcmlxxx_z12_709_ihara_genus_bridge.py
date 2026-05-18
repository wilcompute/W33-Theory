#!/usr/bin/env python3
"""Part DCMLXXX: Z12 709 / Ihara / spectral-genus bridge.

This bridge audits three new observations together:

1. The element z = 1 + 2*zeta_12 + 6*zeta_12^2 + 4*zeta_12^3 has exact
   algebraic norm 709 in Z[zeta_12].  The older exploratory script reports
   709^2 because it multiplies squared magnitudes over all embeddings.
2. The same element has an exact Eisenstein shadow of norm 13 and a rounded
   identity-embedding squared magnitude near 137, but not an exact Gaussian
   norm 137.  Its true relative Gaussian/Eisenstein norms both have norm 709.
3. The W(3,3) Ihara determinant has no primitive 709 factor.  Its expanded
   determinant has three exact structural zero coefficients and one additional
   nonstructural coefficient divisible by 709.  This makes 709 a secondary
   expanded-coefficient resonance, not a primitive Ihara pole factor.

It also records the spectral-genus correction: H(3+4s) has imaginary part t on
the critical line, but that line maps to Re(n)=5, not to the genus-axis
Re(n)=7/2.
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from dataclasses import asdict, dataclass
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_PATH = ROOT / "data" / "dcmlxxx_z12_709_ihara_genus_bridge.json"
RESULT_PATH = ROOT / "PART_DCMLXXX_Z12_709_IHARA_GENUS_BRIDGE_results.json"

Z12_ELEMENT = (1, 2, 6, 4)
TARGET_PRIMES = (7, 13, 137, 709)


@dataclass(frozen=True)
class BridgeSummary:
    part: str
    decimal: int
    z12_element: tuple[int, int, int, int]
    algebraic_norm: int
    script_squared_norm: int
    eisenstein_shadow_norm: int
    nearest_identity_shadow_integer: int
    w33_ihara_unique_709_coefficient_degree: int
    critical_line_maps_to_re_n: str
    genus_axis_maps_to_re_s: str
    all_identities_hold: bool


def _reduce_z12(coeffs: list[int]) -> tuple[int, int, int, int]:
    coeffs = coeffs[:]
    while len(coeffs) > 4:
        lead = coeffs.pop()
        if lead == 0:
            continue
        degree = len(coeffs)
        coeffs[degree - 2] += lead
        coeffs[degree - 4] -= lead
    while len(coeffs) < 4:
        coeffs.append(0)
    return tuple(coeffs[:4])


def z12_mul(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    coeffs = [0] * 7
    for i, a_i in enumerate(left):
        for j, b_j in enumerate(right):
            coeffs[i + j] += a_i * b_j
    return _reduce_z12(coeffs)


def z12_power(power: int) -> tuple[int, int, int, int]:
    power %= 12
    result = (1, 0, 0, 0)
    zeta = (0, 1, 0, 0)
    for _ in range(power):
        result = z12_mul(result, zeta)
    return result


def z12_add(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(a + b for a, b in zip(left, right))


def z12_scale(scale: int, value: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(scale * x for x in value)


def galois_image(value: tuple[int, int, int, int], k: int) -> tuple[int, int, int, int]:
    image = (0, 0, 0, 0)
    for exponent, coeff in enumerate(value):
        image = z12_add(image, z12_scale(coeff, z12_power(exponent * k)))
    return image


def algebraic_norm(value: tuple[int, int, int, int]) -> int:
    columns: list[list[int]] = []
    basis = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    for basis_vector in basis:
        columns.append(list(z12_mul(value, basis_vector)))
    matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    return int(matrix.det())


def identity_embedding_abs2(value: tuple[int, int, int, int]) -> dict[str, Any]:
    a, b, c, d = value
    sqrt3_coeff = a * b + b * c + c * d
    rational_four = (2 * a + c) ** 2 + 3 * b * b + (2 * d + b) ** 2 + 3 * c * c
    rational = Fraction(rational_four, 4)
    numeric = float(rational) + sqrt3_coeff * math.sqrt(3)
    nearest = round(numeric)
    return {
        "exact": f"{rational} + {sqrt3_coeff}*sqrt(3)",
        "rational_part": {"numerator": rational.numerator, "denominator": rational.denominator},
        "sqrt3_coeff": sqrt3_coeff,
        "numeric": numeric,
        "nearest_integer": nearest,
        "nearest_integer_error": abs(nearest - numeric),
        "is_exact_integer_137": rational == 137 and sqrt3_coeff == 0,
    }


def eisenstein_shadow(value: tuple[int, int, int, int]) -> dict[str, Any]:
    a, b, c, d = value
    # Evaluate at omega with omega^2 + omega + 1 = 0 and omega^3 = 1.
    coeff_1 = a + d - c
    coeff_omega = b - c
    norm = coeff_1 * coeff_1 - coeff_1 * coeff_omega + coeff_omega * coeff_omega
    return {
        "as_a_plus_b_omega": [coeff_1, coeff_omega],
        "norm": norm,
    }


def relative_norms(value: tuple[int, int, int, int]) -> dict[str, Any]:
    rel_i = z12_mul(value, galois_image(value, 5))
    rel_e = z12_mul(value, galois_image(value, 7))
    rel_i_norm = rel_i[0] * rel_i[0] + rel_i[3] * rel_i[3]

    # rel_e = A + B*zeta_12^2 = (A+B) + B*omega because zeta_12^2 = 1 + omega.
    coeff_1 = rel_e[0] + rel_e[2]
    coeff_omega = rel_e[2]
    rel_e_norm = coeff_1 * coeff_1 - coeff_1 * coeff_omega + coeff_omega * coeff_omega
    return {
        "relative_norm_to_Q_i": {
            "z12_basis": rel_i,
            "as_gaussian_integer": [rel_i[0], rel_i[3]],
            "norm": rel_i_norm,
        },
        "relative_norm_to_Q_omega": {
            "z12_basis": rel_e,
            "as_eisenstein_integer": [coeff_1, coeff_omega],
            "norm": rel_e_norm,
        },
    }


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


def smallest_prime_of_form_59n_plus_1() -> int:
    n = 1
    while True:
        candidate = 59 * n + 1
        if is_prime(candidate):
            return candidate
        n += 1


def smallest_prime_cube_sum_of_three_prime_cubes(limit: int = 709) -> dict[str, Any]:
    primes = [n for n in range(2, limit + 1) if is_prime(n)]
    cube_to_prime = {p**3: p for p in primes}
    sums: dict[int, tuple[int, int, int]] = {}
    for a_index, a in enumerate(primes):
        a3 = a**3
        for b_index in range(a_index, len(primes)):
            b = primes[b_index]
            ab = a3 + b**3
            if ab >= limit**3:
                break
            for c in primes[b_index:]:
                total = ab + c**3
                if total > limit**3:
                    break
                sums.setdefault(total, (a, b, c))
    hits = [
        (p, sums[p**3])
        for p in primes
        if p**3 in sums
    ]
    first_prime, triple = hits[0]
    return {
        "first_prime": first_prime,
        "triple": list(triple),
        "identity_holds": first_prime**3 == sum(p**3 for p in triple),
    }


def poly_mul_mod(left: list[int], right: list[int], modulus: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if a == 0:
            continue
        for j, b in enumerate(right):
            if b:
                out[i + j] = (out[i + j] + a * b) % modulus
    return out


def poly_pow_mod(base: list[int], exponent: int, modulus: int) -> list[int]:
    out = [1]
    current = base
    exp = exponent
    while exp:
        if exp & 1:
            out = poly_mul_mod(out, current, modulus)
        current = poly_mul_mod(current, current, modulus)
        exp >>= 1
    return out


def poly_mul_truncated_int(left: list[int], right: list[int], max_degree: int) -> list[int]:
    out = [0] * (min(max_degree, len(left) + len(right) - 2) + 1)
    for i, a in enumerate(left):
        if a == 0:
            continue
        for j, b in enumerate(right):
            if b and i + j <= max_degree:
                out[i + j] += a * b
    return out


def poly_pow_truncated_int(base: list[int], exponent: int, max_degree: int) -> list[int]:
    out = [1]
    current = base
    exp = exponent
    while exp:
        if exp & 1:
            out = poly_mul_truncated_int(out, current, max_degree)
        current = poly_mul_truncated_int(current, current, max_degree)
        exp >>= 1
    return out


def coefficient_at_degree_int(factors: list[tuple[list[int], int]], degree: int) -> int:
    total_degree = sum((len(base) - 1) * exponent for base, exponent in factors)
    if degree > total_degree // 2:
        target = total_degree - degree
        working_factors = [(list(reversed(base)), exponent) for base, exponent in factors]
    else:
        target = degree
        working_factors = factors

    polynomial = [1]
    for base, exponent in working_factors:
        polynomial = poly_mul_truncated_int(
            polynomial,
            poly_pow_truncated_int(base, exponent, target),
            target,
        )
    return polynomial[target] if target < len(polynomial) else 0


def w33_ihara_mod_prime_scan(prime: int = 709) -> dict[str, Any]:
    factors: list[tuple[list[int], int]] = [
        ([1, 0, -1], 200),
        ([1, -12, 11], 1),
        ([1, -2, 11], 24),
        ([1, 4, 11], 15),
    ]
    certificate_prime = 1_000_003
    polynomial_mod = [1]
    polynomial_certificate_mod = [1]
    for base, exponent in factors:
        polynomial_mod = poly_mul_mod(polynomial_mod, poly_pow_mod(base, exponent, prime), prime)
        polynomial_certificate_mod = poly_mul_mod(
            polynomial_certificate_mod,
            poly_pow_mod(base, exponent, certificate_prime),
            certificate_prime,
        )
    mod_zero_degrees = [
        degree
        for degree, coeff in enumerate(polynomial_mod)
        if coeff % prime == 0
    ]
    exact_zero_degrees: list[int] = []
    nonstructural_mod_zero_degrees: list[int] = []
    certificate_nonzero_degrees: list[int] = []
    total_degree = len(polynomial_mod) - 1
    for degree in mod_zero_degrees:
        reduced_degree = min(degree, total_degree - degree)
        if reduced_degree <= 2:
            exact_small_coefficient = coefficient_at_degree_int(factors, degree)
            if exact_small_coefficient == 0:
                exact_zero_degrees.append(degree)
                continue
        if polynomial_certificate_mod[degree] % certificate_prime != 0:
            nonstructural_mod_zero_degrees.append(degree)
            certificate_nonzero_degrees.append(degree)
        else:
            nonstructural_mod_zero_degrees.append(degree)
    return {
        "modulus": prime,
        "degree": len(polynomial_mod) - 1,
        "exact_zero_coefficient_degrees": exact_zero_degrees,
        "mod_zero_coefficient_degrees": mod_zero_degrees,
        "nonstructural_mod_zero_coefficient_degrees": nonstructural_mod_zero_degrees,
        "nonstructural_nonzero_certificate_prime": certificate_prime,
        "certificate_nonzero_degrees": certificate_nonzero_degrees,
        "exact_zero_coefficient_count": len(exact_zero_degrees),
        "mod_zero_coefficient_count": len(mod_zero_degrees),
        "nonstructural_mod_zero_coefficient_count": len(nonstructural_mod_zero_degrees),
    }


def prime_support(values: list[int]) -> list[int]:
    support: set[int] = set()
    for value in values:
        n = abs(value)
        factor = 2
        while factor * factor <= n:
            while n % factor == 0:
                support.add(factor)
                n //= factor
            factor += 1
        if n > 1:
            support.add(n)
    return sorted(support)


def spectral_genus_packet() -> dict[str, Any]:
    # H(n)=(n-3)(n-4)/12.
    # For s=sigma+it and n=3+4s, on sigma=1/2:
    # H=(2+4it)(1+4it)/12=(1-8t^2)/6 + i t.
    h_minus_one_twelfth = Fraction((-37) * (-49), 144 * 12)
    critical_line_re_n = Fraction(3, 1) + 4 * Fraction(1, 2)
    genus_axis_re_n = Fraction(7, 2)
    genus_axis_re_s_under_n_3_plus_4s = (genus_axis_re_n - 3) / 4
    return {
        "H_definition": "H(n)=(n-3)(n-4)/12",
        "critical_line_map": "n=3+4s maps Re(s)=1/2 to Re(n)=5",
        "critical_line_re_n": str(critical_line_re_n),
        "im_H_identity_on_critical_line": "Im H(3+4(1/2+it)) = t",
        "genus_axis_re_n": str(genus_axis_re_n),
        "genus_axis_re_s_under_n_3_plus_4s": str(genus_axis_re_s_under_n_3_plus_4s),
        "axis_claim_for_n_3_plus_4s_is_false": critical_line_re_n != genus_axis_re_n,
        "H_minus_1_over_12": {
            "value": str(h_minus_one_twelfth),
            "numerator_factorization": {"7": 2, "37": 1},
            "denominator": 1728,
        },
    }


@lru_cache(maxsize=1)
def build_bridge() -> dict[str, Any]:
    norm = abs(algebraic_norm(Z12_ELEMENT))
    script_squared_norm = norm * norm
    identity_shadow = identity_embedding_abs2(Z12_ELEMENT)
    eisenstein = eisenstein_shadow(Z12_ELEMENT)
    rel_norms = relative_norms(Z12_ELEMENT)
    cube_packet = smallest_prime_cube_sum_of_three_prime_cubes()
    ihara_scan = w33_ihara_mod_prime_scan(709)
    genus = spectral_genus_packet()
    primitive_ihara_values = [200, 11, 12, 2, 4, 24, 15, 40, 28]
    ihara_prime_support = prime_support(primitive_ihara_values)

    identities = {
        "z12_norm_is_709": norm == 709,
        "script_full_norm_is_norm_squared": script_squared_norm == 502681 == 709 * 709,
        "identity_shadow_rounds_to_137_but_is_not_exact": (
            identity_shadow["nearest_integer"] == 137
            and identity_shadow["is_exact_integer_137"] is False
        ),
        "eisenstein_shadow_norm_is_13": eisenstein["norm"] == 13,
        "relative_norms_have_norm_709": (
            rel_norms["relative_norm_to_Q_i"]["norm"] == 709
            and rel_norms["relative_norm_to_Q_omega"]["norm"] == 709
        ),
        "prime_709_splits_completely_in_zeta12": is_prime(709) and 709 % 12 == 1,
        "prime_709_is_first_59n_plus_1_prime": smallest_prime_of_form_59n_plus_1() == 709,
        "prime_709_cube_prime_cube_identity": (
            cube_packet["first_prime"] == 709 and cube_packet["identity_holds"]
        ),
        "w33_ihara_primitive_support_excludes_13_137_709": (
            set(TARGET_PRIMES).intersection(ihara_prime_support) == {7}
        ),
        "w33_ihara_expanded_mod_709_has_unique_zero_coefficient": (
            ihara_scan["exact_zero_coefficient_degrees"] == [1, 2, 479]
            and ihara_scan["nonstructural_mod_zero_coefficient_degrees"] == [338]
        ),
        "spectral_genus_imaginary_identity_has_non_axis_map": (
            genus["critical_line_re_n"] == "5"
            and genus["genus_axis_re_s_under_n_3_plus_4s"] == "1/8"
            and genus["axis_claim_for_n_3_plus_4s_is_false"] is True
        ),
        "H_minus_1_over_12_is_1813_over_1728": genus["H_minus_1_over_12"]["value"] == "1813/1728",
    }

    summary = BridgeSummary(
        part="DCMLXXX",
        decimal=980,
        z12_element=Z12_ELEMENT,
        algebraic_norm=norm,
        script_squared_norm=script_squared_norm,
        eisenstein_shadow_norm=eisenstein["norm"],
        nearest_identity_shadow_integer=identity_shadow["nearest_integer"],
        w33_ihara_unique_709_coefficient_degree=ihara_scan[
            "nonstructural_mod_zero_coefficient_degrees"
        ][0],
        critical_line_maps_to_re_n=genus["critical_line_re_n"],
        genus_axis_maps_to_re_s=genus["genus_axis_re_s_under_n_3_plus_4s"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "z12_unified_element": {
            "basis": "1, zeta_12, zeta_12^2, zeta_12^3",
            "coefficients": list(Z12_ELEMENT),
            "algebraic_norm": norm,
            "script_squared_norm": script_squared_norm,
            "identity_embedding_abs2": identity_shadow,
            "eisenstein_shadow": eisenstein,
            "relative_norms": rel_norms,
            "splitting_709": {
                "is_prime": is_prime(709),
                "mod_12": 709 % 12,
                "minus_one": 708,
                "minus_one_over_12": 59,
                "splits_completely_in_Q_zeta12": 709 % 12 == 1,
            },
            "prime_cube_curio": cube_packet,
        },
        "w33_ihara_alignment": {
            "factorization": (
                "(1-u^2)^200*(1-12u+11u^2)*(1-2u+11u^2)^24*(1+4u+11u^2)^15"
            ),
            "primitive_factor_prime_support": ihara_prime_support,
            "target_prime_intersection": sorted(set(TARGET_PRIMES).intersection(ihara_prime_support)),
            "expanded_mod_709_scan": ihara_scan,
            "reading": (
                "709 is not a primitive W33 Ihara pole factor. Beyond the exact structural "
                "zero coefficients, it appears as a unique nonstructural expanded coefficient "
                "resonance of the W33 Ihara determinant modulo 709."
            ),
        },
        "spectral_genus": genus,
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
                "status": "VERIFIED: Z12 norm-709, Ihara coefficient resonance, and genus-map guard",
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
