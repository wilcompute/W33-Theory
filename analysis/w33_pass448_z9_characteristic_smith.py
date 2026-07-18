#!/usr/bin/env python3
"""Pass 448: exact 3-primary Smith decomposition for the flat Z/9 Heisenberg graph.

The p-adic elimination works over Z_p: at each level it removes every unit pivot
by invertible row/column operations, divides the remaining block by p, and
continues.  The pivot counts are the exact elementary-divisor multiplicities.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass448_z9_characteristic_smith.json"


def heisenberg_reduced_laplacian(modulus: int) -> np.ndarray:
    if modulus % 2 == 0:
        raise ValueError("odd modulus required")
    inv2 = pow(2, -1, modulus)
    elements = [
        (a, b, c)
        for a in range(modulus)
        for b in range(modulus)
        for c in range(modulus)
    ]
    index = {g: i for i, g in enumerate(elements)}
    section = [
        (a, b, 0)
        for a in range(modulus)
        for b in range(modulus)
        if (a, b) != (0, 0)
    ]
    n = len(elements)
    adjacency = np.zeros((n, n), dtype=np.int64)
    for i, (a, b, c) in enumerate(elements):
        for x, y, z in section:
            h = (
                (a + x) % modulus,
                (b + y) % modulus,
                (c + z + inv2 * (a * y - b * x)) % modulus,
            )
            adjacency[i, index[h]] = 1
    degree = modulus * modulus - 1
    if not np.array_equal(adjacency, adjacency.T):
        raise AssertionError("connection set is not inverse closed")
    if set(adjacency.sum(axis=1).tolist()) != {degree}:
        raise AssertionError("wrong degree")
    laplacian = degree * np.eye(n, dtype=np.int64) - adjacency
    return laplacian[:-1, :-1]


def padic_elementary_counts(matrix: np.ndarray, p: int, max_level: int) -> tuple[list[int], int]:
    """Return counts for exact p-exponents 0,1,... and unresolved remainder.

    Operations are performed modulo p^K, but every pivot is a p-adic unit, so
    they are invertible over Z_p and preserve p-primary Smith valuations.
    """
    modulus = p**max_level
    a = matrix.astype(np.int64, copy=True) % modulus
    counts: list[int] = []
    for _level in range(max_level):
        size = a.shape[0]
        rank_units = 0
        while rank_units < size:
            locations = np.argwhere((a[rank_units:, rank_units:] % p) != 0)
            if locations.size == 0:
                break
            i = rank_units + int(locations[0, 0])
            j = rank_units + int(locations[0, 1])
            if i != rank_units:
                a[[rank_units, i], :] = a[[i, rank_units], :]
            if j != rank_units:
                a[:, [rank_units, j]] = a[:, [j, rank_units]]

            inverse = pow(int(a[rank_units, rank_units]), -1, modulus)
            a[rank_units, :] = (a[rank_units, :] * inverse) % modulus

            factors = a[:, rank_units].copy()
            factors[rank_units] = 0
            a = (a - factors[:, None] * a[rank_units : rank_units + 1, :]) % modulus
            a[rank_units, rank_units + 1 :] = 0
            rank_units += 1

        counts.append(rank_units)
        remainder = a[rank_units:, rank_units:]
        if remainder.size == 0:
            return counts, 0
        if np.any(remainder % p):
            raise AssertionError("nondivisible entry survived unit elimination")
        modulus //= p
        a = (remainder // p) % modulus
    return counts, a.shape[0]


def valuation(counts: list[int]) -> int:
    return sum(exponent * multiplicity for exponent, multiplicity in enumerate(counts))


def weld_primary_components(size: int, components: dict[int, list[int]]) -> dict[str, int]:
    invariant_factors = [1] * size
    for prime, counts in components.items():
        exponents: list[int] = []
        for exponent, multiplicity in enumerate(counts):
            exponents.extend([exponent] * multiplicity)
        if len(exponents) != size:
            raise AssertionError((prime, len(exponents), size))
        for i, exponent in enumerate(sorted(exponents)):
            invariant_factors[i] *= prime**exponent
    return {str(k): v for k, v in sorted(Counter(invariant_factors).items()) if k > 1}


def build_payload() -> dict:
    field_matrix = heisenberg_reduced_laplacian(3)
    field_counts, field_remainder = padic_elementary_counts(field_matrix, 3, 6)

    ring_matrix = heisenberg_reduced_laplacian(9)
    ring_counts, ring_remainder = padic_elementary_counts(ring_matrix, 3, 10)

    matrix_tree_v3 = 12 * 3 + 6 * 3 + 270 * 2 + 216 * 2 + 224 * 4 - 6

    two_counts = [446, 6, 0, 60, 216]
    five_counts = [512, 216]
    full_group = weld_primary_components(
        728,
        {
            2: two_counts,
            3: ring_counts,
            5: five_counts,
        },
    )

    checks = {
        "field_control_reproduces_pass437": field_counts == [10, 8, 1, 7] and field_remainder == 0,
        "ring_dimension_728": sum(ring_counts) + ring_remainder == 728,
        "ring_resolved_before_level_10": ring_remainder == 0,
        "ring_mod3_rank_99": ring_counts[0] == 99,
        "ring_mod3_nullity_629": sum(ring_counts[1:]) == 629,
        "matrix_tree_valuation_matches": valuation(ring_counts) == matrix_tree_v3 == 1916,
        "exponent_six_gap_is_real": len(ring_counts) > 6 and ring_counts[6] == 0,
        "top_exponent_is_eight": len(ring_counts) == 9 and ring_counts[8] == 7,
        "full_weld_divisibility_chain": all(
            b % a == 0
            for a, b in zip(
                [int(k) for k, v in full_group.items() for _ in range(v)],
                [int(k) for k, v in full_group.items() for _ in range(v)][1:],
            )
        ),
    }

    return {
        "schema": "w33.pass448.z9_characteristic_smith.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "graph": {
            "group": "Heisenberg group over Z/9Z in symmetric-cocycle coordinates",
            "vertices": 729,
            "degree": 80,
            "reduced_laplacian_size": 728,
        },
        "field_control_q3": {
            "exact_3_exponent_counts": {str(i): c for i, c in enumerate(field_counts)},
            "expected_nonunit_counts": {"1": 8, "2": 1, "3": 7},
        },
        "z9_3_primary": {
            "exact_exponent_counts_including_units": {str(i): c for i, c in enumerate(ring_counts)},
            "critical_group_component": {
                "3": 154,
                "9": 162,
                "27": 80,
                "81": 10,
                "243": 205,
                "729": 0,
                "2187": 11,
                "6561": 7,
            },
            "total_3_adic_valuation": valuation(ring_counts),
        },
        "prime_to_characteristic_inputs": {
            "2_exponent_counts": {str(i): c for i, c in enumerate(two_counts)},
            "5_exponent_counts": {str(i): c for i, c in enumerate(five_counts)},
        },
        "full_critical_group_invariant_factors": full_group,
        "algorithm_boundary": (
            "This is an exact finite computation over Z_3, validated against the known q=3 field Smith group. "
            "It closes Z/9Z but is not yet a symbolic formula for every chain length."
        ),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 448 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
