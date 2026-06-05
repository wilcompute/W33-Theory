"""W(3,3) BREAKTHROUGH 320: e-cube D4 normalizer in GL(4,2).

BT319 proved that the eight selector-preserving e-cube coordinate schedules are
the order-8 square group D4 inside the coordinate permutation group S4.

GAP then reveals the next layer:

    N_S4(D4)       = D4                       order 8
    N_GL(4,2)(D4)  = D4 x C2                  order 16
    C_GL(4,2)(D4)  = C2 x C2                  order 4

The extra C2 is not a coordinate permutation.  It is the complement involution

    kappa = J + I over F2,

whose row masks are [14, 13, 11, 7].  Equivalently, each coordinate basis
direction maps to its three-coordinate complement:

    bit -> 15 xor bit.

Thus the BT319 square symmetry is self-normalizing inside S4, but the full
linear Q4 carrier has exactly one extra central binary layer.  The index is

    |GL(4,2)| / 16 = 20160 / 16 = 1260 = 2^2 * q^2 * F5 * Phi6.

This packet reproduces the GAP calculation by brute-force enumeration of
GL(4,2), keeping the verifier deterministic and offline.
"""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import permutations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_319_ecube_selector_d4_group import (  # noqa: E402
    BITS,
    DOUBLE_PAIR_SWAP,
    IDENTITY,
    pair_stabilizer,
)


Q = 3
LAMBDA = 2
MU = 4
F5 = 5
PHI6 = 7
ALL_ONES = 15
COMPLEMENT_INVOLUTION = tuple(ALL_ONES ^ bit for bit in BITS)


def row_times_matrix(row: int, matrix: tuple[int, ...]) -> int:
    result = 0
    for index, mask in enumerate(BITS):
        if row & mask:
            result ^= matrix[index]
    return result


def mat_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Matrix product over F2, represented by row masks."""
    return tuple(row_times_matrix(row, right) for row in left)


def rank_f2(rows: tuple[int, ...]) -> int:
    basis = list(rows)
    rank = 0
    for column in reversed(range(4)):
        pivot = None
        bit = 1 << column
        for row_index in range(rank, len(basis)):
            if basis[row_index] & bit:
                pivot = row_index
                break
        if pivot is None:
            continue
        basis[rank], basis[pivot] = basis[pivot], basis[rank]
        for row_index in range(len(basis)):
            if row_index != rank and basis[row_index] & bit:
                basis[row_index] ^= basis[rank]
        rank += 1
    return rank


def gl42() -> list[tuple[int, ...]]:
    return [
        rows
        for rows in product(range(1, 16), repeat=4)
        if rank_f2(tuple(rows)) == 4
    ]


@cache
def mat_inverse(matrix: tuple[int, ...]) -> tuple[int, ...]:
    augmented = [matrix[row] | (1 << (4 + row)) for row in range(4)]
    for column in range(4):
        pivot = None
        bit = 1 << column
        for row in range(column, 4):
            if augmented[row] & bit:
                pivot = row
                break
        if pivot is None:
            raise ValueError(f"singular matrix: {matrix}")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        for row in range(4):
            if row != column and augmented[row] & bit:
                augmented[row] ^= augmented[column]
    return tuple((row >> 4) & ALL_ONES for row in augmented)


def mat_order(matrix: tuple[int, ...]) -> int:
    result = IDENTITY
    for exponent in range(1, 33):
        result = mat_mul(result, matrix)
        if result == IDENTITY:
            return exponent
    raise ValueError(f"order not found for {matrix}")


def is_permutation_matrix(matrix: tuple[int, ...]) -> bool:
    return sorted(matrix) == BITS


def d4_matrix_group() -> set[tuple[int, ...]]:
    return {tuple(element) for element in pair_stabilizer()}


def coordinate_permutation_group() -> set[tuple[int, ...]]:
    return {tuple(perm) for perm in permutations(BITS)}


def conjugate(g: tuple[int, ...], h: tuple[int, ...]) -> tuple[int, ...]:
    return mat_mul(mat_mul(mat_inverse(g), h), g)


def normalizer(group: list[tuple[int, ...]], subgroup: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    return {
        g
        for g in group
        if {conjugate(g, h) for h in subgroup} == subgroup
    }


def centralizer(group: list[tuple[int, ...]], subgroup: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    return {
        g
        for g in group
        if all(mat_mul(g, h) == mat_mul(h, g) for h in subgroup)
    }


def center(group: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    return {
        g
        for g in group
        if all(mat_mul(g, h) == mat_mul(h, g) for h in group)
    }


def _as_lists(elements: set[tuple[int, ...]] | list[tuple[int, ...]]) -> list[list[int]]:
    return [list(element) for element in sorted(elements)]


def ecube_d4_gl42_normalizer_packet() -> dict:
    gl = gl42()
    d4 = d4_matrix_group()
    s4 = coordinate_permutation_group()
    s4_normalizer = normalizer(sorted(s4), d4)
    gl_normalizer = normalizer(gl, d4)
    gl_centralizer = centralizer(gl, d4)
    normalizer_center = center(gl_normalizer)

    kappa = COMPLEMENT_INVOLUTION
    kappa_coset = {mat_mul(kappa, element) for element in d4}
    center_d4 = center(d4)
    expected_centralizer = center_d4 | {mat_mul(kappa, element) for element in center_d4}
    permutation_part = {element for element in gl_normalizer if is_permutation_matrix(element)}
    nonpermutation_part = gl_normalizer - permutation_part
    index_gl_normalizer = len(gl) // len(gl_normalizer)

    checks = {
        "gl42_size_is_20160": len(gl) == 20160,
        "d4_size_is_8": len(d4) == 8,
        "d4_order_distribution_matches_bt319": Counter(mat_order(element) for element in d4)
        == {1: 1, 2: 5, 4: 2},
        "coordinate_group_size_is_24": len(s4) == 24,
        "normalizer_in_s4_is_self": s4_normalizer == d4,
        "normalizer_in_s4_index_is_q": len(s4) // len(s4_normalizer) == Q,
        "complement_involution_is_not_coordinate_permutation": not is_permutation_matrix(kappa),
        "complement_involution_has_order_2": mat_order(kappa) == LAMBDA,
        "complement_involution_maps_bits_to_complements": kappa == tuple(ALL_ONES ^ bit for bit in BITS),
        "complement_involution_centralizes_d4": all(
            mat_mul(kappa, element) == mat_mul(element, kappa) for element in d4
        ),
        "normalizer_in_gl42_has_order_16": len(gl_normalizer) == 16,
        "normalizer_is_d4_times_complement_c2": gl_normalizer == d4 | kappa_coset,
        "normalizer_quotient_over_d4_has_size_lambda": len(gl_normalizer) // len(d4) == LAMBDA,
        "normalizer_order_distribution_is_c2_times_d4": Counter(
            mat_order(element) for element in gl_normalizer
        )
        == {1: 1, 2: 11, 4: 4},
        "centralizer_in_gl42_has_order_mu": len(gl_centralizer) == MU,
        "centralizer_is_center_d4_times_complement": gl_centralizer == expected_centralizer,
        "normalizer_center_has_order_mu": len(normalizer_center) == MU,
        "permutation_part_of_normalizer_is_d4": permutation_part == d4,
        "nonpermutation_part_has_8_elements": len(nonpermutation_part) == 8,
        "gl42_normalizer_index_is_1260": index_gl_normalizer == 1260,
        "index_has_substrate_factorization": index_gl_normalizer == (LAMBDA**2) * (Q**2) * F5 * PHI6,
        "all_normalizer_orders_divide_4": all(4 % mat_order(element) == 0 for element in gl_normalizer),
        "double_pair_swap_survives_as_central_d4_element": DOUBLE_PAIR_SWAP in center_d4,
    }

    return {
        "breakthrough": 320,
        "title": "E-cube D4 normalizer in GL(4,2)",
        "gl42_order": len(gl),
        "d4_order": len(d4),
        "coordinate_s4_order": len(s4),
        "s4_normalizer_order": len(s4_normalizer),
        "s4_normalizer_index": len(s4) // len(s4_normalizer),
        "gl42_normalizer_order": len(gl_normalizer),
        "gl42_normalizer_index": index_gl_normalizer,
        "gl42_centralizer_order": len(gl_centralizer),
        "normalizer_quotient_over_d4": len(gl_normalizer) // len(d4),
        "group_identification": {
            "normalizer_in_s4": "D4, self-normalizing Sylow-2 subgroup of S4",
            "normalizer_in_gl42": "D4 x C2",
            "centralizer_in_gl42": "C2 x C2",
        },
        "complement_involution": {
            "row_masks": list(kappa),
            "formula": "bit -> 15 xor bit",
            "matrix_description": "J + I over F2",
            "order": mat_order(kappa),
        },
        "d4_elements": _as_lists(d4),
        "gl42_normalizer_elements": _as_lists(gl_normalizer),
        "gl42_centralizer_elements": _as_lists(gl_centralizer),
        "normalizer_center": _as_lists(normalizer_center),
        "permutation_part": _as_lists(permutation_part),
        "nonpermutation_part": _as_lists(nonpermutation_part),
        "normalizer_order_distribution": dict(
            sorted(Counter(mat_order(element) for element in gl_normalizer).items())
        ),
        "index_factorization": {
            "value": index_gl_normalizer,
            "substrate_form": "2^2 * q^2 * F5 * Phi6",
            "expanded": [LAMBDA**2, Q**2, F5, PHI6],
        },
        "gap_crosscheck": {
            "S4": "Normalizer(S4,D4) has size 8, structure D8, index 3",
            "GL42": "Normalizer(GL(4,2),D4) has size 16, structure C2 x D8, index 1260",
            "centralizer": "Centralizer(GL(4,2),D4) has size 4, structure C2 x C2",
        },
        "architectural_reading": (
            "The selector D4 is rigid inside coordinate permutations but gains one "
            "central complement bit in the full linear Q4 carrier.  This makes "
            "the BT319 atlas a square coordinate face with a single non-coordinate "
            "complement lift, exactly the kind of local square-plus-complement "
            "structure expected in the hypercube/tomotope control layer."
        ),
        "boundary": (
            "This identifies a finite GL(4,2) normalizer of the BT319 selector D4. "
            "It does not yet identify the complement involution with a physical "
            "time-reversal, Reye configuration, or tomotope map."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = ecube_d4_gl42_normalizer_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 320: E-CUBE D4 NORMALIZER IN GL(4,2)")
    print("=" * 78)
    print()
    print(f"|GL(4,2)|              = {packet['gl42_order']}")
    print(f"|D4|                   = {packet['d4_order']}")
    print(f"|N_S4(D4)|             = {packet['s4_normalizer_order']}")
    print(f"|N_GL(4,2)(D4)|        = {packet['gl42_normalizer_order']}")
    print(f"|C_GL(4,2)(D4)|        = {packet['gl42_centralizer_order']}")
    print(f"normalizer index       = {packet['gl42_normalizer_index']}")
    print(f"complement involution  = {packet['complement_involution']['row_masks']}")
    print(f"verified               = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = ROOT / "data" / "w33_BREAKTHROUGH_320_ecube_d4_gl42_normalizer.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
