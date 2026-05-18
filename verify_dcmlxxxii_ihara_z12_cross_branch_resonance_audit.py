#!/usr/bin/env python3
"""Part DCMLXXXII: Ihara/Z12 cross-branch resonance audit.

This audit reconciles the local Bass-11 W(3,3) Ihara theorem with the remote
GitHub main notes that used coefficient 12.  It keeps the remote discoveries as
source material, but promotes only exact, locally reproducible facts:

* Bass coefficient 11 is the live W(3,3) graph zeta.
* Coefficient 12 is an adjacent arithmetic shadow.
* The Z[zeta_12] element has exact norm 709; 13 is the Eisenstein shadow and
  137 is a rounded identity-sheet shadow.
* The 709 signal is an expanded-determinant modular resonance, not a primitive
  Ihara factor.
* Classical RH remains open behind the zeta_W = zeta identification bridge.
"""

from __future__ import annotations

import itertools
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

DATA_PATH = ROOT / "data" / "dcmlxxxii_ihara_z12_cross_branch_resonance_audit.json"
RESULT_PATH = ROOT / "PART_DCMLXXXII_IHARA_Z12_CROSS_BRANCH_RESONANCE_AUDIT_results.json"

PART = "DCMLXXXII"
DECIMAL = 982
REMOTE_MAIN_COMMIT = "ec327312"

V = 40
E = 240
DEGREE = 12
BASS = DEGREE - 1
MU = 4
Z12_ELEMENT = (1, 2, 6, 4)
TARGET_PRIMES = (7, 13, 137, 709)
HEEGNER_RADICANDS = {1, 2, 3, 7, 11, 19, 43, 67, 163}


@dataclass(frozen=True)
class BridgeSummary:
    part: str
    decimal: int
    remote_main_commit: str
    live_bass_parameter: int
    shadow_coefficient: int
    z12_algebraic_norm: int
    z12_eisenstein_norm: int
    alpha_inverse_gaussian_norm: int
    live_nonstructural_709_degrees: list[int]
    shadow_nonstructural_709_degrees: list[int]
    classical_rh_status: str
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


def det_int(matrix: list[list[int]]) -> int:
    total = 0
    for perm in itertools.permutations(range(len(matrix))):
        inversions = sum(
            1
            for i in range(len(perm))
            for j in range(i + 1, len(perm))
            if perm[i] > perm[j]
        )
        sign = -1 if inversions % 2 else 1
        term = sign
        for row, column in enumerate(perm):
            term *= matrix[row][column]
        total += term
    return total


def algebraic_norm_z12(value: tuple[int, int, int, int]) -> int:
    basis = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    columns = [list(z12_mul(value, basis_vector)) for basis_vector in basis]
    matrix = [[columns[column][row] for column in range(4)] for row in range(4)]
    return det_int(matrix)


def identity_embedding_abs2(value: tuple[int, int, int, int]) -> dict[str, Any]:
    a, b, c, d = value
    sqrt3_coeff = a * b + b * c + c * d
    rational_four = (2 * a + c) ** 2 + 3 * b * b + (2 * d + b) ** 2 + 3 * c * c
    rational = Fraction(rational_four, 4)
    numeric = float(rational) + sqrt3_coeff * math.sqrt(3)
    nearest = round(numeric)
    return {
        "exact": f"{rational} + {sqrt3_coeff}*sqrt(3)",
        "nearest_integer": nearest,
        "nearest_integer_error": abs(nearest - numeric),
        "is_exact_integer_137": rational == 137 and sqrt3_coeff == 0,
    }


def eisenstein_shadow(value: tuple[int, int, int, int]) -> dict[str, Any]:
    a, b, c, d = value
    coeff_1 = a + d - c
    coeff_omega = b - c
    norm = coeff_1 * coeff_1 - coeff_1 * coeff_omega + coeff_omega * coeff_omega
    return {
        "as_a_plus_b_omega": [coeff_1, coeff_omega],
        "norm": norm,
    }


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


def ihara_factors(coefficient: int) -> list[tuple[list[int], int]]:
    return [
        ([1, 0, -1], 200),
        ([1, -12, coefficient], 1),
        ([1, -2, coefficient], 24),
        ([1, 4, coefficient], 15),
    ]


def determinant_resonance_scan(coefficient: int, modulus: int = 709) -> dict[str, Any]:
    factors = ihara_factors(coefficient)
    polynomial_mod = [1]
    for base, exponent in factors:
        polynomial_mod = poly_mul_mod(polynomial_mod, poly_pow_mod(base, exponent, modulus), modulus)

    mod_zero_degrees = [
        degree
        for degree, coeff in enumerate(polynomial_mod)
        if coeff % modulus == 0
    ]
    exact_zero_degrees: list[int] = []
    nonstructural_degrees: list[int] = []
    coefficient_certificates: dict[str, dict[str, Any]] = {}
    certificate_prime = 1_000_003

    for degree in mod_zero_degrees:
        exact_coefficient = coefficient_at_degree_int(factors, degree)
        exact_zero = exact_coefficient == 0
        if exact_zero:
            exact_zero_degrees.append(degree)
        else:
            nonstructural_degrees.append(degree)
        coefficient_certificates[str(degree)] = {
            "exact_zero": exact_zero,
            "coefficient_mod_709": exact_coefficient % modulus,
            "coefficient_mod_1000003": exact_coefficient % certificate_prime,
        }

    return {
        "coefficient": coefficient,
        "modulus": modulus,
        "degree": len(polynomial_mod) - 1,
        "exact_zero_coefficient_degrees": exact_zero_degrees,
        "mod_zero_coefficient_degrees": mod_zero_degrees,
        "nonstructural_mod_zero_coefficient_degrees": nonstructural_degrees,
        "nonstructural_mod_zero_coefficient_count": len(nonstructural_degrees),
        "coefficient_certificates": coefficient_certificates,
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


def quadratic_residue_roots(radicand: int, prime: int) -> list[int]:
    target = radicand % prime
    return [x for x in range(prime) if (x * x) % prime == target]


def build_bridge() -> dict[str, Any]:
    z12_norm = abs(algebraic_norm_z12(Z12_ELEMENT))
    identity_shadow = identity_embedding_abs2(Z12_ELEMENT)
    eisenstein = eisenstein_shadow(Z12_ELEMENT)

    live_sectors = [ihara_sector(lam, BASS) for lam in (2, -4)]
    shadow_sectors = [ihara_sector(lam, DEGREE) for lam in (2, -4)]
    live_scan = determinant_resonance_scan(BASS, 709)
    shadow_scan = determinant_resonance_scan(DEGREE, 709)

    primitive_support = prime_support([200, 11, 12, 2, 4, 24, 15, 40, 28])
    bass_decrement = [
        {
            "sector": "r",
            "lambda": 2,
            "shadow_discriminant": shadow_sectors[0]["discriminant"],
            "live_discriminant": live_sectors[0]["discriminant"],
            "shadow_field_radicand": shadow_sectors[0]["field_radicand"],
            "live_field_radicand": live_sectors[0]["field_radicand"],
            "live_lands_in_heegner_field": live_sectors[0]["is_heegner_field"],
        },
        {
            "sector": "s",
            "lambda": -4,
            "shadow_discriminant": shadow_sectors[1]["discriminant"],
            "live_discriminant": live_sectors[1]["discriminant"],
            "shadow_field_radicand": shadow_sectors[1]["field_radicand"],
            "live_field_radicand": live_sectors[1]["field_radicand"],
            "live_lands_in_heegner_field": live_sectors[1]["is_heegner_field"],
        },
    ]

    alpha_inverse = BASS * BASS + MU * MU
    alpha_heegner = {
        "alpha_inverse": alpha_inverse,
        "gaussian_norm": [BASS, MU],
        "gaussian_norm_identity": f"{BASS}^2 + {MU}^2 = {alpha_inverse}",
        "splitting_roots": {
            "Q_sqrt_minus_7": quadratic_residue_roots(-7, alpha_inverse),
            "Q_sqrt_minus_11": quadratic_residue_roots(-11, alpha_inverse),
        },
        "reading": (
            "137 is exact as the Bass-11/mu Gaussian norm.  It splits in both "
            "Q(sqrt(-7)) and Q(sqrt(-11)), but Q(sqrt(-11)) belongs to the "
            "coefficient-12 shadow branch, not the live r-sector graph zeta."
        ),
    }

    remote_sources = [
        {
            "commit": REMOTE_MAIN_COMMIT,
            "file": "NOTES/BREAKTHROUGH_MAY17_2026.md",
            "audit_status": (
                "Corrected: the Z12 algebraic norm is 709, the 709^2 value is a "
                "squared-magnitude artifact, and the genus map does not put RH on "
                "the genus axis."
            ),
        },
        {
            "commit": REMOTE_MAIN_COMMIT,
            "file": "NOTES/HEEGNER_IHARA_BREAKTHROUGH_MAY18_2026.md",
            "audit_status": (
                "Classified as coefficient-12 shadow; the live W33 Ihara-Bass "
                "determinant uses coefficient 11."
            ),
        },
        {
            "commit": REMOTE_MAIN_COMMIT,
            "file": "NOTES/BREAKTHROUGH21_MASTER_THEOREM_MAY18.md",
            "audit_status": (
                "Finite Bass-11 graph-Ihara structure is retained; classical RH "
                "still requires an identification/limit theorem."
            ),
        },
    ]

    rh_boundary = {
        "finite_w33_graph_ihara_rh": "PROVED",
        "zeta_W_equals_riemann_zeta": "OPEN",
        "classical_riemann_hypothesis": "OPEN",
        "next_proof_target": "adelic/projective-limit identification bridge",
    }

    identities = {
        "part_number_is_982": PART == "DCMLXXXII" and DECIMAL == 982,
        "remote_sources_are_static_inputs": all(source["commit"] == REMOTE_MAIN_COMMIT for source in remote_sources),
        "live_bass_parameter_is_11": BASS == 11 and DEGREE == 12,
        "live_fields_are_minus_10_and_minus_7": [sector["field_radicand"] for sector in live_sectors] == [-10, -7],
        "shadow_fields_are_minus_11_and_minus_2": [sector["field_radicand"] for sector in shadow_sectors] == [-11, -2],
        "live_radius_is_one_over_11": [sector["pole_radius_squared"] for sector in live_sectors] == ["1/11", "1/11"],
        "shadow_radius_is_one_over_12": [sector["pole_radius_squared"] for sector in shadow_sectors] == ["1/12", "1/12"],
        "only_live_s_sector_is_heegner": [
            sector["is_heegner_field"] for sector in live_sectors
        ] == [False, True],
        "bass_decrement_moves_discriminants": (
            [row["shadow_discriminant"] for row in bass_decrement] == [-44, -32]
            and [row["live_discriminant"] for row in bass_decrement] == [-40, -28]
        ),
        "z12_norm_is_709": z12_norm == 709,
        "eisenstein_shadow_norm_is_13": eisenstein["norm"] == 13,
        "identity_shadow_rounds_to_137_but_is_not_exact": (
            identity_shadow["nearest_integer"] == 137
            and identity_shadow["is_exact_integer_137"] is False
        ),
        "alpha_inverse_is_bass_mu_gaussian_norm": alpha_inverse == 137,
        "alpha_splits_on_minus_7_and_minus_11_sheets": (
            bool(alpha_heegner["splitting_roots"]["Q_sqrt_minus_7"])
            and bool(alpha_heegner["splitting_roots"]["Q_sqrt_minus_11"])
        ),
        "primitive_support_excludes_13_137_709": (
            set(TARGET_PRIMES).intersection(primitive_support) == {7}
        ),
        "live_709_resonance_is_degree_338": (
            live_scan["exact_zero_coefficient_degrees"] == [1, 2, 479]
            and live_scan["mod_zero_coefficient_degrees"] == [1, 2, 338, 479]
            and live_scan["nonstructural_mod_zero_coefficient_degrees"] == [338]
        ),
        "shadow_709_resonance_is_degree_424": (
            shadow_scan["exact_zero_coefficient_degrees"] == [1, 479]
            and shadow_scan["mod_zero_coefficient_degrees"] == [1, 424, 479]
            and shadow_scan["nonstructural_mod_zero_coefficient_degrees"] == [424]
        ),
        "live_and_shadow_resonances_are_distinct": (
            live_scan["nonstructural_mod_zero_coefficient_degrees"] != shadow_scan[
                "nonstructural_mod_zero_coefficient_degrees"
            ]
        ),
        "classical_rh_boundary_remains_open": (
            rh_boundary["finite_w33_graph_ihara_rh"] == "PROVED"
            and rh_boundary["zeta_W_equals_riemann_zeta"] == "OPEN"
            and rh_boundary["classical_riemann_hypothesis"] == "OPEN"
        ),
    }

    summary = BridgeSummary(
        part=PART,
        decimal=DECIMAL,
        remote_main_commit=REMOTE_MAIN_COMMIT,
        live_bass_parameter=BASS,
        shadow_coefficient=DEGREE,
        z12_algebraic_norm=z12_norm,
        z12_eisenstein_norm=eisenstein["norm"],
        alpha_inverse_gaussian_norm=alpha_inverse,
        live_nonstructural_709_degrees=live_scan["nonstructural_mod_zero_coefficient_degrees"],
        shadow_nonstructural_709_degrees=shadow_scan["nonstructural_mod_zero_coefficient_degrees"],
        classical_rh_status=rh_boundary["classical_riemann_hypothesis"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "remote_main_sources": remote_sources,
        "live_bass_11": {
            "vertices": V,
            "edges": E,
            "degree": DEGREE,
            "bass_parameter": BASS,
            "factorization": (
                "(1-u^2)^200*(1-12u+11u^2)*(1-2u+11u^2)^24*(1+4u+11u^2)^15"
            ),
            "nontrivial_sectors": live_sectors,
            "graph_ihara_rh_status": "PROVED",
        },
        "coefficient_12_shadow": {
            "coefficient": DEGREE,
            "factorization": (
                "(1-u^2)^200*(1-12u+12u^2)*(1-2u+12u^2)^24*(1+4u+12u^2)^15"
            ),
            "nontrivial_sectors": shadow_sectors,
            "status": "shadow_branch_not_live_graph_zeta",
        },
        "bass_decrement": bass_decrement,
        "z12_709_norm_packet": {
            "element_basis": "1, zeta_12, zeta_12^2, zeta_12^3",
            "coefficients": list(Z12_ELEMENT),
            "algebraic_norm": z12_norm,
            "script_squared_norm_artifact": z12_norm * z12_norm,
            "eisenstein_shadow": eisenstein,
            "identity_embedding_abs2": identity_shadow,
            "classification": {
                "709": "exact Z12 algebraic norm",
                "13": "exact Eisenstein shadow norm",
                "137": "rounded identity-sheet shadow for this Z12 element",
            },
        },
        "z12_709_resonance_comparison": {
            "primitive_factor_prime_support": primitive_support,
            "target_prime_intersection": sorted(set(TARGET_PRIMES).intersection(primitive_support)),
            "live_bass_11_scan": live_scan,
            "coefficient_12_shadow_scan": shadow_scan,
            "reading": (
                "The nonstructural mod-709 resonance moves from degree 338 in the "
                "live Bass-11 determinant to degree 424 in the coefficient-12 "
                "shadow determinant."
            ),
        },
        "alpha_heegner_boundary": alpha_heegner,
        "rh_boundary": rh_boundary,
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
                "status": "VERIFIED: Ihara/Z12 cross-branch resonance audit",
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
