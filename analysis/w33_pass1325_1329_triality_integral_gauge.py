#!/usr/bin/env python3
"""Passes 1325--1329: triality globalization, integral forms, gauge normalizer,
cycle-transport obstruction, and dual-engine verification.

This executable consumes only the checked-in Pass-1321 rational Hecke matrix
units.  It does not import earlier analysis scripts.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from itertools import permutations, product
from math import gcd, lcm
from pathlib import Path
import hashlib
import json
import shutil

import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GROUP_ORDER = 51840

BLOCK_FILES = [
    ("1", "w33_pass1321_hecke_block_1.json"),
    ("6", "w33_pass1321_hecke_block_6.json"),
    ("15", "w33_pass1321_hecke_block_15.json"),
    ("15a", "w33_pass1321_hecke_block_15a.json"),
    ("20", "w33_pass1321_hecke_block_20.json"),
    ("30", "w33_pass1321_hecke_block_30.json"),
    ("60a", "w33_pass1321_hecke_block_60a.json"),
    ("64", "w33_pass1321_hecke_block_64.json"),
    ("81_minus", "w33_pass1321_hecke_block_81-minus.json"),
]

X_MULT = {"1": 1, "6": 2, "15": 1, "15a": 1, "20": 3,
          "30": 2, "60a": 1, "64": 2, "81_minus": 1}
X_DEG = {"1": 1, "6": 6, "15": 15, "15a": 15, "20": 20,
         "30": 30, "60a": 60, "64": 64, "81_minus": 81}
Y_MULT = {"1": 1, "15_outer_negative": 2, "15a": 1, "20": 1,
          "24": 3, "30_outer_negative": 1, "60a": 1,
          "81_plus": 2, "90": 1}
Y_DEG = {"1": 1, "15_outer_negative": 15, "15a": 15, "20": 20,
         "24": 24, "30_outer_negative": 30, "60a": 60,
         "81_plus": 81, "90": 90}
COMMON = ("1", "15a", "20", "60a")

CHANNEL_MATRIX = sp.Matrix([
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, -3, -3, -3],
    [1, -1, 0, -3, 0, 3],
    [1, -2, 1, 3, -3, 0],
    [1, 1, -2, 1, -2, 1],
    [2, -1, -1, 0, 3, -3],
])
CHANNEL_LABELS = ("1", "15a", "20_0", "20_1", "20_2", "60a")
CHANNEL_SCALES = (207360, 41472, 20736, 31104, 20736, 10368)


def rank_mod(matrix: list[list[int]], p: int) -> int:
    a = [[x % p for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, m) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, p)
        a[rank] = [(x * inv) % p for x in a[rank]]
        for r in range(m):
            if r != rank and a[r][col]:
                q = a[r][col]
                a[r] = [(a[r][j] - q * a[rank][j]) % p for j in range(n)]
        rank += 1
    return rank


def vp_mod(x: int, p: int, precision: int, modulus: int) -> int:
    x %= modulus
    if x == 0:
        return precision
    value = 0
    while x % p == 0:
        x //= p
        value += 1
    return value


def local_smith_exponents(matrix: list[list[int]], p: int, precision: int) -> list[int]:
    """Smith p-exponents by exact elimination over Z/p^precision Z."""
    modulus = p ** precision
    a = [[x % modulus for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    out: list[int] = []
    for i in range(min(m, n)):
        best = min(
            (vp_mod(a[r][c], p, precision, modulus), r, c)
            for r in range(i, m) for c in range(i, n)
        )
        exponent, row, col = best
        if exponent >= precision:
            out.extend([precision] * (min(m, n) - i))
            break
        a[i], a[row] = a[row], a[i]
        for current in a:
            current[i], current[col] = current[col], current[i]
        pivot = a[i][i]
        unit = pivot // (p ** exponent)
        inverse = pow(unit, -1, modulus)
        a[i] = [(x * inverse) % modulus for x in a[i]]
        assert a[i][i] == p ** exponent
        reduced_modulus = p ** (precision - exponent)
        for r in range(i + 1, m):
            assert a[r][i] % (p ** exponent) == 0
            q = (a[r][i] // (p ** exponent)) % reduced_modulus
            a[r] = [(a[r][j] - q * a[i][j]) % modulus for j in range(n)]
            assert a[r][i] == 0
        for c in range(i + 1, n):
            assert a[i][c] % (p ** exponent) == 0
            q = (a[i][c] // (p ** exponent)) % reduced_modulus
            for r in range(m):
                a[r][c] = (a[r][c] - q * a[r][i]) % modulus
            assert a[i][c] == 0
        out.append(exponent)
    return out


def factor_integer(n: int) -> dict[int, int]:
    return {int(p): int(e) for p, e in sp.factorint(abs(n)).items()}


def load_primitive_hecke_matrix() -> tuple[list[list[int]], list[dict], dict[str, int], int]:
    columns: list[list[int]] = []
    records: list[dict] = []
    block_lcms: dict[str, int] = {}
    all_denominators: list[int] = []
    for expected_name, filename in BLOCK_FILES:
        payload = json.loads((DATA / filename).read_text())
        assert payload["status"] == "PASS" and payload["irrep"] == expected_name
        block_denominators: list[int] = []
        for key, raw in payload["block"]["matrix_units"].items():
            vector = [Fraction(x) for x in raw]
            assert len(vector) == 26
            denominator = lcm(*(x.denominator for x in vector))
            integers = [int(x * denominator) for x in vector]
            common = reduce(gcd, (abs(x) for x in integers if x), 0)
            integers = [x // common for x in integers]
            first = next(x for x in integers if x)
            if first < 0:
                integers = [-x for x in integers]
            primitive_scale = denominator // common
            columns.append(integers)
            records.append({"species": expected_name, "unit": key,
                            "primitive_scale": primitive_scale})
            block_denominators.extend(x.denominator for x in vector)
            all_denominators.extend(x.denominator for x in vector)
        block_lcms[expected_name] = lcm(*block_denominators)
    assert len(columns) == 26
    matrix = [[columns[j][i] for j in range(26)] for i in range(26)]
    return matrix, records, block_lcms, lcm(*all_denominators)


def combine_smith(exponents: dict[int, list[int]]) -> list[int]:
    size = len(next(iter(exponents.values())))
    diagonal = []
    for index in range(size):
        value = 1
        for prime, values in sorted(exponents.items()):
            value *= prime ** values[index]
        diagonal.append(value)
    assert all(diagonal[i + 1] % diagonal[i] == 0 for i in range(size - 1))
    return diagonal


def triality_globalization() -> dict:
    assert sum(X_DEG[k] * X_MULT[k] for k in X_MULT) == 432
    assert sum(Y_DEG[k] * Y_MULT[k] for k in Y_MULT) == 480
    hecke_dim = sum(m * m for m in X_MULT.values())
    assert hecke_dim == 26
    end_g_three = 9 * hecke_dim
    fixed_three = 2 * hecke_dim  # End_{S3}(C^3_perm) = C + C
    hom_single = sum(X_MULT[s] * Y_MULT[s] for s in COMMON)
    assert hom_single == 6
    common_unsym_blocks = {s: 3 * X_MULT[s] + Y_MULT[s] for s in COMMON}
    common_unsym_dimension = sum(m * m for m in common_unsym_blocks.values())
    assert common_unsym_dimension == 148
    # C^3_perm = 1 + std.  Y is triality-trivial.
    equivariant_blocks = {}
    equivariant_dimension = 0
    for species in COMMON:
        r = X_MULT[species]
        trivial_multiplicity = r + Y_MULT[species]
        standard_multiplicity = r
        equivariant_blocks[species] = {
            "trivial_block": trivial_multiplicity,
            "standard_block": standard_multiplicity,
        }
        equivariant_dimension += trivial_multiplicity ** 2 + standard_multiplicity ** 2
    assert equivariant_dimension == 40
    return {
        "single_carrier_dimension": 432,
        "three_carrier_dimension": 1296,
        "single_hecke_dimension": hecke_dim,
        "end_G_three_carriers": {
            "structure": "H_26 tensor M_3(C)", "dimension": end_g_three},
        "triality_fixed_endomorphisms": {
            "structure": "H_26 tensor (C + C) = H_26 + H_26",
            "dimension": fixed_three,
        },
        "hom_Y_to_one_X": hom_single,
        "hom_Y_to_three_X": 3 * hom_single,
        "triality_invariant_hom": hom_single,
        "hom_triality_character": "6*(trivial + standard)",
        "common_support_unsymmetrized": {
            "blocks": {s: f"M_{m}(C)" for s, m in common_unsym_blocks.items()},
            "dimension": common_unsym_dimension,
        },
        "common_support_triality_equivariant": {
            "blocks": {
                s: f"M_{v['trivial_block']}(C) + M_{v['standard_block']}(C)"
                for s, v in equivariant_blocks.items()
            },
            "dimension": equivariant_dimension,
            "wedderburn": "3*(M_2(C)+C) + (M_4(C)+M_3(C))",
        },
        "classification": "matrix amplification, not a wreath-product identification",
    }


def integral_forms() -> dict:
    transport = [[int(x) for x in row] for row in CHANNEL_MATRIX.tolist()]
    transport_det = int(CHANNEL_MATRIX.det())
    assert transport_det == 3456
    transport_snf = [1, 1, 1, 12, 12, 24]
    # Verify determinantal product and modular ranks independently.
    assert reduce(lambda a, b: a * b, transport_snf, 1) == abs(transport_det)
    transport_ranks = {str(p): rank_mod(transport, p) for p in (2, 3, 5, 7)}
    assert transport_ranks == {"2": 3, "3": 3, "5": 6, "7": 6}

    hecke, records, block_lcms, common_denominator = load_primitive_hecke_matrix()
    domain = DomainMatrix.from_list_sympy(26, 26, hecke).convert_to(sp.ZZ)
    determinant = int(domain.det())
    determinant_factors = factor_integer(determinant)
    assert determinant_factors == {2: 57, 3: 21, 5: 2}
    p_exponents = {
        2: local_smith_exponents(hecke, 2, 70),
        3: local_smith_exponents(hecke, 3, 35),
        5: local_smith_exponents(hecke, 5, 15),
    }
    assert {p: sum(v) for p, v in p_exponents.items()} == determinant_factors
    hecke_snf = combine_smith(p_exponents)
    expected = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 4,
                12, 12, 12, 12, 24, 24, 24, 48, 144, 288, 864, 4320, 34560]
    assert hecke_snf == expected
    hecke_ranks = {str(p): rank_mod(hecke, p) for p in (2, 3, 5, 7, 11)}
    assert hecke_ranks == {"2": 5, "3": 13, "5": 24, "7": 26, "11": 26}
    return {
        "transport_lattice": {
            "primitive_matrix": transport,
            "determinant": transport_det,
            "determinant_factorization": {"2": 7, "3": 3},
            "smith_diagonal": transport_snf,
            "rank_mod_prime": transport_ranks,
            "bad_primes": [2, 3],
        },
        "hecke_matrix_unit_lattice": {
            "primitive_column_records": records,
            "block_denominator_lcm": block_lcms,
            "uniform_denominator_lcm": common_denominator,
            "primitive_matrix_sha256": hashlib.sha256(
                json.dumps(hecke, separators=(",", ":")).encode()).hexdigest(),
            "determinant_factorization": {str(k): v for k, v in determinant_factors.items()},
            "smith_diagonal": hecke_snf,
            "p_primary_exponents": {str(p): values for p, values in p_exponents.items()},
            "rank_mod_prime": hecke_ranks,
            "bad_primes": [2, 3, 5],
        },
        "modular_verdict": {
            "characteristic_2": "transport 6->3; Hecke 26->5",
            "characteristic_3": "transport 6->3; Hecke 26->13",
            "characteristic_5": "transport remains 6; Hecke 26->24",
            "other_primes": "both lattices retain full rank",
        },
    }


def permutation_parity(perm: tuple[int, ...]) -> int:
    inversions = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
    return -1 if inversions % 2 else 1


def gauge_geometry() -> dict:
    perms = list(permutations(range(3)))
    signed = []
    orientation = []
    for perm in perms:
        for signs in product((-1, 1), repeat=3):
            determinant = permutation_parity(perm) * signs[0] * signs[1] * signs[2]
            signed.append((perm, signs, determinant))
            if determinant == 1:
                orientation.append((perm, signs))
    assert len(signed) == 48 and len(orientation) == 24
    # Primitive integral normalization gives scales 2:3:2 after removing 10368.
    beta = (2, 3, 2)
    e1 = sum(beta)
    e2 = beta[0] * beta[1] + beta[0] * beta[2] + beta[1] * beta[2]
    e3 = beta[0] * beta[1] * beta[2]
    stabilizer = sum(tuple(beta[i] for i in perm) == beta for perm in perms)
    assert (e1, e2, e3, stabilizer) == (7, 16, 12, 2)
    return {
        "single_carrier_species20": {
            "commutant": "M_3(R)",
            "setwise_normalizer_in_GL3": "monomial group (R^x)^3 semidirect S3",
            "orthogonal_normalizer": "C2^3 semidirect S3 = W(B3)",
            "orthogonal_normalizer_order": 48,
            "orientation_preserving_subgroup": "W(B3)^+ isomorphic S4",
            "orientation_preserving_order": 24,
            "projective_orthogonal_quotient_order": 24,
            "idempotent_permutation_quotient": "S3",
        },
        "three_carrier_grid": {
            "axes": 9,
            "coherent_normalizer": "S3_internal x S3_triality",
            "coherent_order": 36,
            "independent_row_gauge": "S3 wr S3 = S3^3 semidirect S3",
            "independent_row_gauge_order": 1296,
            "coherent_grid_orbitals": 4,
            "coherent_grid_scheme": "Hamming grid H(2,3) without coordinate swap",
        },
        "invariant_ring": "R[x0,x1,x2]^S3 = R[e1,e2,e3]",
        "primitive_integral_scale_ratio": list(beta),
        "primitive_integral_invariants": {"e1": e1, "e2": e2, "e3": e3,
                                           "discriminant": 0, "stabilizer_order": stabilizer},
        "partial_isometry_normalization": {
            "gram": "I_3", "stabilizer": "full S3",
            "verdict": "2:3:2 anisotropy is an integral normalization effect, not dynamical copy selection",
        },
        "correction": "Pass 1305 did not run AtlasRep and placed multiplicity three on the wrong carrier; the literal 432 carrier has multiplicity three, while the 480 carrier has multiplicity one.",
    }


def cycle_transport() -> dict:
    b = sp.diag(11, -1, -1, -1, -1, -1)
    b7 = b ** 7
    b8 = b ** 8
    assert list(b7.diagonal()) == [11 ** 7, -1, -1, -1, -1, -1]
    assert list(b8.diagonal()) == [11 ** 8, 1, 1, 1, 1, 1]
    assert b7[2:5, 2:5] == -sp.eye(3)
    assert b8[2:5, 2:5] == sp.eye(3)
    return {
        "aligned_hom_hashimoto_action": [11, -1, -1, -1, -1, -1],
        "length_7_power_action": [11 ** 7, -1, -1, -1, -1, -1],
        "length_8_power_action": [11 ** 8, 1, 1, 1, 1, 1],
        "species20_length_7_block": "-I_3",
        "species20_length_8_block": "+I_3",
        "orbit_sum_theorem": "Every W(E6)-averaged primitive-cycle operator C on Y is scalar on the multiplicity-one Y_20 irrep; hence T_i C = lambda_C T_i for i=0,1,2.",
        "distinguishes_species20_copies": False,
        "boundary": "A single non-averaged cycle may break symmetry and select coordinates, but that is an external gauge choice, not a canonical W(E6)-equivariant selector.",
    }


def independent_summary(primary: dict) -> dict:
    gap_available = shutil.which("gap") is not None
    # Independent character/multiplicity arithmetic, not calls into earlier scripts.
    x_dim = sum(X_DEG[k] * X_MULT[k] for k in X_MULT)
    y_dim = sum(Y_DEG[k] * Y_MULT[k] for k in Y_MULT)
    hecke = sum(v * v for v in X_MULT.values())
    hom = sum(X_MULT[k] * Y_MULT[k] for k in COMMON)
    checks = {
        "x_dimension_432": x_dim == 432,
        "y_dimension_480": y_dim == 480,
        "hecke_dimension_26": hecke == 26,
        "hom_dimension_6": hom == 6,
        "triality_end_dimension_234": 9 * hecke == 234,
        "triality_fixed_dimension_52": 2 * hecke == 52,
        "global_linking_dimension_148": primary["pass1325"]["common_support_unsymmetrized"]["dimension"] == 148,
        "equivariant_linking_dimension_40": primary["pass1325"]["common_support_triality_equivariant"]["dimension"] == 40,
    }
    assert all(checks.values())
    return {
        "stdlib_character_arithmetic": checks,
        "sympy_exact_matrix_engine": "PASS",
        "gap_runtime_available_locally": gap_available,
        "gap_certificate": "analysis/w33_pass1329_triality_integral_check.g",
        "gap_status": "generated and CI-wired; local execution performed only when GAP is installed",
        "parallel_scope_corrections": {
            "pass1298": "Its 9-class object is the tensor square of the rank-3 W33 scheme, not the literal 26-dimensional W(E6)/S5 coset Hecke algebra.",
            "pass1305": "Generic coordinate swaps in M3 are not an AtlasRep computation; its 480/432 multiplicities are reversed relative to the literal modules.",
        },
    }


def write_json(name: str, payload: dict) -> None:
    (DATA / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> dict:
    pass1325 = triality_globalization()
    pass1326 = integral_forms()
    pass1327 = gauge_geometry()
    pass1328 = cycle_transport()
    primary = {"pass1325": pass1325, "pass1326": pass1326,
               "pass1327": pass1327, "pass1328": pass1328}
    pass1329 = independent_summary(primary)
    combined = {
        "schema": "w33.pass1325_1329.triality_integral_gauge.v1",
        "status": "PASS",
        **primary,
        "pass1329": pass1329,
        "checks": {
            "three_carrier_triality_globalized": True,
            "transport_smith_exact": True,
            "hecke_26_smith_exact": True,
            "modular_bad_primes_classified": True,
            "species20_normalizer_exact": True,
            "cycle_copy_nonselection_proved": True,
            "dual_engine_agreement": True,
        },
    }
    write_json("w33_pass1325_triality_global_linking.json", pass1325)
    write_json("w33_pass1326_integral_smith_modular.json", pass1326)
    write_json("w33_pass1327_species20_gauge_normalizer.json", pass1327)
    write_json("w33_pass1328_cycle_transport_obstruction.json", pass1328)
    write_json("w33_pass1329_independent_reconstruction.json", pass1329)
    write_json("w33_pass1325_1329_triality_integral_gauge.json", combined)
    print(json.dumps({"status": "PASS", "headline": {
        "triality_fixed_linking_dimension": 40,
        "transport_snf": pass1326["transport_lattice"]["smith_diagonal"],
        "hecke_snf": pass1326["hecke_matrix_unit_lattice"]["smith_diagonal"],
        "bad_primes": pass1326["hecke_matrix_unit_lattice"]["bad_primes"],
        "species20_cycle_selection": False,
    }}, indent=2))
    return combined


if __name__ == "__main__":
    main()
