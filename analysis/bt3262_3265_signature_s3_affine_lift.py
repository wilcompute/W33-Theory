#!/usr/bin/env python3
"""Passes 3262--3265: exact-cover signature S3 Fourier and affine-lift theorem.

This verifier uses only exact finite calculations.  It starts from the four local
K_{4,4,4} cell patterns in the complete 720-signature cover classification and
proves:

* the local signature alphabet has S3-orbit sizes 1+3+6+6 = 16;
* its permutation character is (16,2,1) and decomposes as 4*1 + 2*sgn + 5*std;
* its rational commutant has dimension 45 and exactly 45 orbitals;
* no affine S3 action on F_2^4 has orbit profile (1,3,6,6);
* an explicit linear action on F_2^5 does, and an equivariant 16-state encoding is given.

The four-bit obstruction is exhaustive: GL(4,2) has 20,160 elements and all 2,800
embedded S3 subgroups are classified by their orbit profiles on F_2^4.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import permutations, product
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Permutation = Tuple[int, int, int]
Matrix = Tuple[int, ...]  # binary row masks
Vector3 = Tuple[int, int, int]

S3: Tuple[Permutation, ...] = tuple(permutations(range(3)))
IDENTITY_4: Matrix = (1, 2, 4, 8)

PATTERN_SEEDS: Dict[str, Vector3] = {
    "T128": (2, 2, 2),
    "T120": (0, 3, 3),
    "T104": (1, 2, 3),
    "T96": (0, 2, 4),
}
EXPECTED_LOCAL_ORBIT_SIZES = (1, 3, 6, 6)


def inverse_permutation(p: Permutation) -> Permutation:
    out = [0, 0, 0]
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)  # type: ignore[return-value]


def compose_permutations(p: Permutation, q: Permutation) -> Permutation:
    """Return p after q."""
    return tuple(p[q[i]] for i in range(3))  # type: ignore[return-value]


def act_on_pattern(p: Permutation, x: Vector3) -> Vector3:
    pinv = inverse_permutation(p)
    return tuple(x[pinv[i]] for i in range(3))  # type: ignore[return-value]


def cycle_type(p: Permutation) -> Tuple[int, ...]:
    seen = [False] * 3
    lengths: List[int] = []
    for i in range(3):
        if seen[i]:
            continue
        j = i
        length = 0
        while not seen[j]:
            seen[j] = True
            length += 1
            j = p[j]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def build_local_alphabet() -> Tuple[List[Vector3], Dict[str, List[Vector3]]]:
    by_type: Dict[str, List[Vector3]] = {}
    omega: List[Vector3] = []
    for name, seed in PATTERN_SEEDS.items():
        orbit = sorted({act_on_pattern(p, seed) for p in S3})
        by_type[name] = orbit
        omega.extend(orbit)
    assert len(omega) == len(set(omega)) == 16
    assert tuple(sorted(len(v) for v in by_type.values())) == EXPECTED_LOCAL_ORBIT_SIZES
    return omega, by_type


def character_and_multiplicities(omega: Sequence[Vector3]) -> Dict[str, object]:
    classes: Dict[Tuple[int, ...], List[Permutation]] = defaultdict(list)
    for p in S3:
        classes[cycle_type(p)].append(p)

    class_order = ((1, 1, 1), (2, 1), (3,))
    fixed = []
    for ctype in class_order:
        p = classes[ctype][0]
        fixed.append(sum(act_on_pattern(p, x) == x for x in omega))
    assert fixed == [16, 2, 1]

    class_sizes = [1, 3, 2]
    irreducibles = {
        "trivial": [1, 1, 1],
        "sign": [1, -1, 1],
        "standard": [2, 0, -1],
    }
    multiplicities: Dict[str, int] = {}
    for name, chi in irreducibles.items():
        inner = sum(class_sizes[i] * fixed[i] * chi[i] for i in range(3))
        assert inner % 6 == 0
        multiplicities[name] = inner // 6
    assert multiplicities == {"trivial": 4, "sign": 2, "standard": 5}
    assert 4 * 1 + 2 * 1 + 5 * 2 == 16

    commutant_dimension = sum(m * m for m in multiplicities.values())
    assert commutant_dimension == 45
    return {
        "class_order": ["identity", "transposition", "three_cycle"],
        "class_sizes": class_sizes,
        "fixed_point_character": fixed,
        "irreducible_multiplicities": multiplicities,
        "commutant_dimension": commutant_dimension,
        "wedderburn_decomposition": "M4(Q) + M2(Q) + M5(Q)",
    }


def local_orbitals(omega: Sequence[Vector3]) -> Dict[str, object]:
    index = {x: i for i, x in enumerate(omega)}
    unseen: Set[Tuple[int, int]] = {(i, j) for i in range(16) for j in range(16)}
    orbitals: List[Set[Tuple[int, int]]] = []
    while unseen:
        pair = next(iter(unseen))
        orbital = {
            (
                index[act_on_pattern(p, omega[pair[0]])],
                index[act_on_pattern(p, omega[pair[1]])],
            )
            for p in S3
        }
        orbitals.append(orbital)
        unseen.difference_update(orbital)
    size_histogram = Counter(len(o) for o in orbitals)
    assert len(orbitals) == 45
    assert size_histogram == Counter({6: 41, 3: 3, 1: 1})
    assert sum(len(o) for o in orbitals) == 16 * 16
    return {
        "orbital_count": len(orbitals),
        "orbital_size_histogram": {str(k): v for k, v in sorted(size_histogram.items())},
    }


def rank_binary_rows(rows: Sequence[int], n: int) -> int:
    work = list(rows)
    rank = 0
    for col in range(n - 1, -1, -1):
        pivot = next((i for i in range(rank, len(work)) if (work[i] >> col) & 1), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> col) & 1):
                work[i] ^= work[rank]
        rank += 1
    return rank


def multiply_binary_matrices(a: Matrix, b: Matrix) -> Matrix:
    out: List[int] = []
    for row in a:
        value = 0
        for k in range(len(b)):
            if (row >> k) & 1:
                value ^= b[k]
        out.append(value)
    return tuple(out)


def apply_binary_matrix(matrix: Matrix, x: int) -> int:
    y = 0
    for i, row in enumerate(matrix):
        if (row & x).bit_count() & 1:
            y |= 1 << i
    return y


def matrix_power(matrix: Matrix, exponent: int, identity: Matrix) -> Matrix:
    out = identity
    base = matrix
    n = exponent
    while n:
        if n & 1:
            out = multiply_binary_matrices(out, base)
        base = multiply_binary_matrices(base, base)
        n //= 2
    return out


def matrix_order(matrix: Matrix, identity: Matrix, maximum: int = 64) -> int:
    current = identity
    for order in range(1, maximum + 1):
        current = multiply_binary_matrices(current, matrix)
        if current == identity:
            return order
    raise RuntimeError("matrix order exceeded bound")


def enumerate_gl4() -> List[Matrix]:
    return [
        tuple(rows)
        for rows in product(range(16), repeat=4)
        if rank_binary_rows(rows, 4) == 4
    ]


def orbit_profile(group: Iterable[Matrix], dimension: int) -> Tuple[int, ...]:
    elements = tuple(group)
    unseen = set(range(1 << dimension))
    sizes: List[int] = []
    while unseen:
        x = next(iter(unseen))
        orbit = {apply_binary_matrix(g, x) for g in elements}
        sizes.append(len(orbit))
        unseen.difference_update(orbit)
    return tuple(sorted(sizes))


def classify_s3_subgroups_gl4() -> Dict[str, object]:
    gl4 = enumerate_gl4()
    assert len(gl4) == 20160
    by_order: Dict[int, List[Matrix]] = defaultdict(list)
    for matrix in gl4:
        by_order[matrix_order(matrix, IDENTITY_4, maximum=15)].append(matrix)

    subgroups: Dict[Tuple[Matrix, ...], Set[Matrix]] = {}
    for r in by_order[3]:
        r_inv = multiply_binary_matrices(r, r)
        for s in by_order[2]:
            if multiply_binary_matrices(multiply_binary_matrices(s, r), s) != r_inv:
                continue
            group = {
                IDENTITY_4,
                r,
                r_inv,
                s,
                multiply_binary_matrices(s, r),
                multiply_binary_matrices(s, r_inv),
            }
            if len(group) == 6:
                subgroups[tuple(sorted(group))] = group

    profiles = Counter(orbit_profile(g, 4) for g in subgroups.values())
    expected = Counter(
        {
            (1, 1, 2, 3, 3, 6): 1680,
            (1, 1, 1, 1, 3, 3, 3, 3): 560,
            (1, 3, 3, 3, 6): 560,
        }
    )
    assert len(subgroups) == 2800
    assert profiles == expected
    assert EXPECTED_LOCAL_ORBIT_SIZES not in profiles

    return {
        "gl4_order": len(gl4),
        "s3_subgroup_count": len(subgroups),
        "orbit_profile_counts": {
            "+".join(map(str, profile)): count
            for profile, count in sorted(profiles.items())
        },
        "target_profile_present": False,
        "affine_four_bit_realization": False,
        "obstruction_reason": (
            "The signature action has one fixed point, so any affine realization is "
            "translation-conjugate to a linear action; no S3 subgroup of GL(4,2) has "
            "orbit profile 1+3+6+6."
        ),
    }


def gl2_natural_representation() -> Dict[Permutation, Matrix]:
    gl2 = [
        tuple(rows)
        for rows in product(range(4), repeat=2)
        if rank_binary_rows(rows, 2) == 2
    ]
    labels = (1, 2, 3)  # three nonzero vectors of F_2^2
    representation: Dict[Permutation, Matrix] = {}
    for p in S3:
        matches = [
            matrix
            for matrix in gl2
            if all(apply_binary_matrix(matrix, labels[i]) == labels[p[i]] for i in range(3))
        ]
        assert len(matches) == 1
        representation[p] = matches[0]
    return representation


def permutation_matrix_3(p: Permutation) -> Matrix:
    rows = [0, 0, 0]
    for i in range(3):
        rows[p[i]] |= 1 << i
    return tuple(rows)


def block_diagonal_3_plus_2(a: Matrix, b: Matrix) -> Matrix:
    return tuple(a) + tuple(row << 3 for row in b)


def explicit_five_bit_lift(omega: Sequence[Vector3], by_type: Dict[str, List[Vector3]]) -> Dict[str, object]:
    rho2 = gl2_natural_representation()
    rho5 = {
        p: block_diagonal_3_plus_2(permutation_matrix_3(p), rho2[p])
        for p in S3
    }

    identity_5: Matrix = (1, 2, 4, 8, 16)
    for p, matrix in rho5.items():
        assert rank_binary_rows(matrix, 5) == 5
        assert rho5[compose_permutations(p, inverse_permutation(p))] == identity_5

    r: Permutation = (1, 2, 0)
    s: Permutation = (0, 2, 1)
    r_matrix = rho5[r]
    s_matrix = rho5[s]
    assert matrix_power(r_matrix, 3, identity_5) == identity_5
    assert matrix_power(s_matrix, 2, identity_5) == identity_5
    assert multiply_binary_matrices(multiply_binary_matrices(s_matrix, r_matrix), s_matrix) == matrix_power(r_matrix, 2, identity_5)

    full_profile = orbit_profile(rho5.values(), 5)
    assert full_profile == (1, 1, 3, 3, 3, 3, 3, 3, 6, 6)

    nonzero_labels = (1, 2, 3)

    def position(x: Vector3, value: int) -> int:
        return x.index(value)

    def encode(x: Vector3) -> int:
        if x in by_type["T128"]:
            return 0
        if x in by_type["T120"]:
            i = position(x, 0)
            return 1 << i
        if x in by_type["T104"]:
            i = position(x, 1)
            j = position(x, 2)
            return (1 << j) | (nonzero_labels[i] << 3)
        if x in by_type["T96"]:
            i = position(x, 0)
            k = position(x, 4)
            first_three = 0b111 ^ (1 << k)
            return first_three | (nonzero_labels[i] << 3)
        raise ValueError(f"unknown signature state {x}")

    encoded = {x: encode(x) for x in omega}
    assert len(set(encoded.values())) == 16
    for p in S3:
        for x in omega:
            assert encoded[act_on_pattern(p, x)] == apply_binary_matrix(rho5[p], encoded[x])

    selected_profile = []
    remaining = set(encoded.values())
    while remaining:
        x = next(iter(remaining))
        orbit = {apply_binary_matrix(matrix, x) for matrix in rho5.values()}
        selected_profile.append(len(orbit))
        remaining.difference_update(orbit)
    assert tuple(sorted(selected_profile)) == EXPECTED_LOCAL_ORBIT_SIZES

    def rows_to_dense(matrix: Matrix, dimension: int) -> List[List[int]]:
        return [[(row >> j) & 1 for j in range(dimension)] for row in matrix]

    encoding_table = {
        ",".join(map(str, x)): format(code, "05b")
        for x, code in sorted(encoded.items())
    }
    return {
        "ambient_dimension": 5,
        "ambient_orbit_profile": list(full_profile),
        "selected_signature_orbit_profile": list(sorted(selected_profile)),
        "generator_r_three_cycle": rows_to_dense(r_matrix, 5),
        "generator_s_transposition": rows_to_dense(s_matrix, 5),
        "encoding_table": encoding_table,
        "equivariant": True,
        "minimal_affine_binary_dimension": 5,
        "information_bits": 4,
        "symmetry_overhead_bits": 1,
    }


def build_results() -> Dict[str, object]:
    omega, by_type = build_local_alphabet()
    character = character_and_multiplicities(omega)
    orbitals = local_orbitals(omega)
    obstruction = classify_s3_subgroups_gl4()
    lift = explicit_five_bit_lift(omega, by_type)

    assert character["commutant_dimension"] == 45
    assert orbitals["orbital_count"] == 45
    assert 45 * 16 == 720

    return {
        "pass_range": "3262-3265",
        "theorem": "Exact-cover signature S3 Fourier and five-bit affine-lift theorem",
        "source_boundary": (
            "The four cell-pattern seeds and 45-anchor/720-signature count are imported "
            "from the frozen complete exact-cover signature classification."
        ),
        "local_signature_types": {
            name: {
                "seed": list(PATTERN_SEEDS[name]),
                "orbit_size": len(states),
                "states": [list(x) for x in states],
            }
            for name, states in by_type.items()
        },
        "local_alphabet_size": len(omega),
        "anchor_count": 45,
        "global_signature_count": 720,
        "rank_degree_identity": "720 = 45 * 16 = dim(End_S3(Q^Omega)) * |Omega|",
        "character": character,
        "coherent_configuration": orbitals,
        "four_bit_affine_obstruction": obstruction,
        "five_bit_lift": lift,
        "claim_boundaries": [
            "The equality between the 45 anchor octets and the 45 local orbitals does not itself define a canonical bijection.",
            "The 16-state signature alphabet is not identified with the OA(16,3,4,2) port alphabet without an explicit intertwiner.",
            "A four-bit implementation remains possible with nonlinear lookup/permutation logic; only affine F_2 implementations are ruled out.",
        ],
        "checks": {
            "local_orbit_sizes": True,
            "character_decomposition": True,
            "commutant_rank_45": True,
            "all_gl4_s3_subgroups_classified": True,
            "four_bit_affine_no_go": True,
            "five_bit_equivariant_encoding": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, help="optional output JSON path")
    args = parser.parse_args()
    results = build_results()
    text = json.dumps(results, indent=2, sort_keys=True)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("PASS 6/6 exact signature-S3 affine-lift checks")


if __name__ == "__main__":
    main()
