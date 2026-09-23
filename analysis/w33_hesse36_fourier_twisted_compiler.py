#!/usr/bin/env python3
"""Exact 36-state phase-twisted compiler between the two Hesse carriers.

The ordinary Payne/Hesse 36 and maximal compiler-safe 36 are not isomorphic as
plain SL(2,3)-sets: their permutation characters differ on order-three
elements.  The orbit/stabilizer data exposes the exact repair.

Under G=SL(2,3):
  ordinary36 = three 4-orbits + one 24-orbit;
  safe36     = three 4-orbits + three 8-orbits.

The three 4-orbits have the same order-6 stabilizer on both sides and pair
objectwise.  The ordinary 24-orbit is regular G.  All three safe 8-orbits have
the same order-3 stabilizer H=<h>.  Therefore

    Reg(G) ~= Ind_H^G(1) + Ind_H^G(chi) + Ind_H^G(chi^2).

The intertwiner is literally the 3-point Fourier transform along every right
H-coset of G.  Equivalently, keep the safe 8-orbits as object sets but twist
their monomial actions by the three H characters 1,omega,omega^2.

This script constructs the full 36x36 compiler over Q(omega), checks rank 36,
orthogonal column norms 1^12 + 3^24, verifies the twisted target group law on
all 24^2 products, and proves the intertwining identity for all 24 group
elements exactly.

After multiplying the 24 Fourier columns by 1/sqrt(3), the compiler is unitary
over C.  The sqrt(3) normalization is not needed for the exact Q(omega)
intertwiner certificate.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "analysis"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

PARENT = ROOT / "analysis/w33_maximal_compiler_symmetry_pappus.py"
OUT = ROOT / "data/w33_hesse36_fourier_twisted_compiler.json"

from w33_exact_eisenstein import (  # noqa: E402
    ONE,
    ZERO,
    matrix_rank,
    omega_power,
    zero_matrix,
)


def load_parent():
    spec = importlib.util.spec_from_file_location("fourier_compiler_parent", PARENT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def permutation_order(perm):
    seen = [False] * len(perm)
    order = 1
    for start in range(len(perm)):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            length += 1
            current = perm[current]
        if length:
            order = math.lcm(order, length)
    return order


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def orbit_sets(perms, degree):
    unseen = set(range(degree))
    out = []
    while unseen:
        seed = min(unseen)
        orbit = {perm[seed] for perm in perms}
        out.append(tuple(sorted(orbit)))
        unseen -= orbit
    return sorted(out, key=lambda orbit: (len(orbit), orbit))


def set_key(S):
    return tuple(sorted(S))


def sparse_column_equal(left, right):
    return {
        row: exponent % 3 for row, exponent in left.items()
    } == {
        row: exponent % 3 for row, exponent in right.items()
    }


def main(write=True):
    p = load_parent()

    directions = (
        (0, 0, 1),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (1, 2, 2),
    )
    noncentral = directions[1:]

    def cyclic_subgroup(d):
        return frozenset((p.ID, d, p.hmul(d, d)))

    selected_subgroups = {cyclic_subgroup(d) for d in directions}

    aut216 = [
        (u, v)
        for u in p.H
        for v in p.H
        if p.hcomm(u, v) == p.ZC and len(p.gen_h(u, v)) == 27
    ]
    assert len(aut216) == 216

    common24 = []
    for uv in aut216:
        images = {
            frozenset(p.phi(uv, g) for g in subgroup)
            for subgroup in selected_subgroups
        }
        if images == selected_subgroups:
            common24.append(uv)
    assert len(common24) == 24

    def right_coset(g, d):
        return frozenset(p.hmul(g, h) for h in (p.ID, d, p.hmul(d, d)))

    ordinary36_set = set()
    for d in noncentral:
        ordinary36_set |= {right_coset(g, d) for g in p.H}
    ordinary36 = sorted(ordinary36_set, key=set_key)
    assert len(ordinary36) == 36
    ordinary_index = {line: i for i, line in enumerate(ordinary36)}

    order9 = set()
    for x in p.K:
        for y in p.K:
            subgroup = p.subgroup_generated((x, y))
            if len(subgroup) == 9:
                order9.add(subgroup)
    safe36 = sorted(
        (subgroup for subgroup in order9 if subgroup & p.D == {p.KID}),
        key=set_key,
    )
    assert len(safe36) == 36
    safe_index = {subgroup: i for i, subgroup in enumerate(safe36)}

    h_index = {g: i for i, g in enumerate(p.H)}
    records = []
    for uv in common24:
        hperm = tuple(h_index[p.phi(uv, g)] for g in p.H)
        ordinary_perm = tuple(
            ordinary_index[frozenset(p.phi(uv, g) for g in line)]
            for line in ordinary36
        )
        safe_perm = tuple(
            safe_index[frozenset((p.phi(uv, g), ext) for g, ext in subgroup)]
            for subgroup in safe36
        )
        records.append(
            {
                "uv": uv,
                "hperm": hperm,
                "order": permutation_order(hperm),
                "ordinary_perm": ordinary_perm,
                "safe_perm": safe_perm,
            }
        )

    hperm_to_group = {row["hperm"]: i for i, row in enumerate(records)}
    assert len(hperm_to_group) == 24
    multiplication = [
        [
            hperm_to_group[
                compose(records[left]["hperm"], records[right]["hperm"])
            ]
            for right in range(24)
        ]
        for left in range(24)
    ]
    identity = next(i for i, row in enumerate(records) if row["order"] == 1)
    inverses = [
        next(
            j
            for j in range(24)
            if multiplication[i][j] == identity
            and multiplication[j][i] == identity
        )
        for i in range(24)
    ]

    ordinary_perms = [row["ordinary_perm"] for row in records]
    safe_perms = [row["safe_perm"] for row in records]
    ordinary_orbits = orbit_sets(ordinary_perms, 36)
    safe_orbits = orbit_sets(safe_perms, 36)
    assert sorted(map(len, ordinary_orbits)) == [4, 4, 4, 24]
    assert sorted(map(len, safe_orbits)) == [4, 4, 4, 8, 8, 8]

    ordinary4 = [orbit for orbit in ordinary_orbits if len(orbit) == 4]
    ordinary24 = next(orbit for orbit in ordinary_orbits if len(orbit) == 24)
    safe4 = [orbit for orbit in safe_orbits if len(orbit) == 4]
    safe8 = [orbit for orbit in safe_orbits if len(orbit) == 8]

    # All three safe 8-orbits have the same C3 stabilizer.
    safe8_stabilizers = []
    for orbit in safe8:
        seed = min(orbit)
        stabilizer = tuple(
            i for i, perm in enumerate(safe_perms) if perm[seed] == seed
        )
        safe8_stabilizers.append(stabilizer)
    assert safe8_stabilizers[0] == safe8_stabilizers[1] == safe8_stabilizers[2]
    H3 = safe8_stabilizers[0]
    assert len(H3) == 3
    assert Counter(records[i]["order"] for i in H3) == {1: 1, 3: 2}

    h_identity = next(i for i in H3 if records[i]["order"] == 1)
    h_generator = min(i for i in H3 if records[i]["order"] == 3)
    h_square = multiplication[h_generator][h_generator]
    assert set((h_identity, h_generator, h_square)) == set(H3)
    h_by_exponent = {0: h_identity, 1: h_generator, 2: h_square}
    h_exponent = {value: key for key, value in h_by_exponent.items()}

    # The ordinary 24-orbit is the regular G-set.
    ordinary24_seed = min(ordinary24)
    group_to_source_point = [
        ordinary_perms[g][ordinary24_seed] for g in range(24)
    ]
    assert len(set(group_to_source_point)) == 24
    assert set(group_to_source_point) == set(ordinary24)

    # Right H3 cosets in G, with deterministic representatives.
    unseen = set(range(24))
    coset_representatives = []
    right_cosets = []
    while unseen:
        representative = min(unseen)
        coset = tuple(
            sorted(multiplication[representative][h] for h in H3)
        )
        coset_representatives.append(representative)
        right_cosets.append(coset)
        unseen -= set(coset)
    assert len(right_cosets) == 8
    assert all(len(coset) == 3 for coset in right_cosets)

    # Each safe 8-orbit is the same G/H3 coset action.  Record the chosen
    # representative for every safe target point.
    target_point_data = {}
    safe8_seeds = [min(orbit) for orbit in safe8]
    for character_index, seed in enumerate(safe8_seeds):
        local = {}
        for representative in coset_representatives:
            point = safe_perms[representative][seed]
            assert point not in local
            local[point] = representative
        assert set(local) == set(safe8[character_index])
        for point, representative in local.items():
            target_point_data[point] = (character_index, representative)
    assert len(target_point_data) == 24

    # Compiler T maps twisted-safe target coordinates to ordinary coordinates.
    # Store columns sparsely as row -> omega exponent.
    compiler_columns = [dict() for _ in range(36)]

    for character_index, seed in enumerate(safe8_seeds):
        for representative in coset_representatives:
            target = safe_perms[representative][seed]
            for h_exp in range(3):
                group_element = multiplication[representative][h_by_exponent[h_exp]]
                source = group_to_source_point[group_element]
                exponent = (-character_index * h_exp) % 3
                compiler_columns[target][source] = exponent

    # The three 4-orbits already agree objectwise as G-sets.
    objectwise_12 = {}
    for source_orbit, target_orbit in zip(ordinary4, safe4):
        source_seed = min(source_orbit)
        target_seed = min(target_orbit)
        local = {}
        for g in range(24):
            source = ordinary_perms[g][source_seed]
            target = safe_perms[g][target_seed]
            if source in local:
                assert local[source] == target
            local[source] = target
        assert set(local) == set(source_orbit)
        assert set(local.values()) == set(target_orbit)
        objectwise_12.update(local)
    assert len(objectwise_12) == 12

    for source, target in objectwise_12.items():
        compiler_columns[target][source] = 0

    assert Counter(len(column) for column in compiler_columns) == {1: 12, 3: 24}
    assert sum(len(column) for column in compiler_columns) == 84

    # Exact dense compiler over Q(omega), solely for rank certification.
    compiler = zero_matrix(36, 36)
    for target, column in enumerate(compiler_columns):
        for source, exponent in column.items():
            compiler[source][target] = omega_power(exponent)
    assert matrix_rank(compiler) == 36

    # Exact column Gram: 1 on objectwise columns, 3 on Fourier columns.
    gram_profile = Counter()
    for left in range(36):
        for right in range(36):
            value = ZERO
            common_rows = set(compiler_columns[left]) & set(compiler_columns[right])
            for row in common_rows:
                a = omega_power(compiler_columns[left][row]).conjugate()
                b = omega_power(compiler_columns[right][row])
                value = value + a * b
            if left == right:
                expected = ONE if len(compiler_columns[left]) == 1 else 3 * ONE
                assert value == expected
                gram_profile[str(int(expected.a))] += 1
            else:
                assert value == ZERO
    assert gram_profile == {"1": 12, "3": 24}

    # Twisted target monomial representation: safe permutation plus an H3
    # character phase on the three 8-orbits.
    target_phase_exponents = []
    for g in range(24):
        phases = [0] * 36
        perm = safe_perms[g]
        for target, (character_index, representative) in target_point_data.items():
            moved = perm[target]
            moved_character_index, moved_representative = target_point_data[moved]
            assert moved_character_index == character_index
            h = multiplication[inverses[moved_representative]][
                multiplication[g][representative]
            ]
            assert h in h_exponent
            phases[target] = (character_index * h_exponent[h]) % 3
        target_phase_exponents.append(tuple(phases))

    # Check target monomial representation law on every product.
    for left in range(24):
        for right in range(24):
            product = multiplication[left][right]
            p_left = safe_perms[left]
            p_right = safe_perms[right]
            p_product = safe_perms[product]
            e_left = target_phase_exponents[left]
            e_right = target_phase_exponents[right]
            e_product = target_phase_exponents[product]
            for target in range(36):
                assert p_left[p_right[target]] == p_product[target]
                assert (
                    e_right[target] + e_left[p_right[target]]
                ) % 3 == e_product[target]

    # Exact intertwining check, columnwise:
    # ordinary_perm(g) T = T twisted_safe(g).
    for g in range(24):
        source_perm = ordinary_perms[g]
        target_perm = safe_perms[g]
        phases = target_phase_exponents[g]
        for target in range(36):
            left_column = {
                source_perm[source]: exponent
                for source, exponent in compiler_columns[target].items()
            }
            right_column = {
                source: (exponent + phases[target]) % 3
                for source, exponent in compiler_columns[target_perm[target]].items()
            }
            assert sparse_column_equal(left_column, right_column)

    # Character equality after twisting.
    character_profile = Counter()
    for g, row in enumerate(records):
        source_trace = sum(
            1 for i, image in enumerate(ordinary_perms[g]) if i == image
        )
        target_trace = ZERO
        for target, image in enumerate(safe_perms[g]):
            if target == image:
                target_trace = target_trace + omega_power(
                    target_phase_exponents[g][target]
                )
        assert target_trace == source_trace * ONE
        character_profile[(row["order"], source_trace)] += 1

    expected_character_profile = Counter(
        {
            (1, 36): 1,
            (2, 12): 1,
            (3, 3): 8,
            (4, 0): 6,
            (6, 3): 8,
        }
    )
    assert character_profile == expected_character_profile

    serialized_columns = [
        [[source, exponent] for source, exponent in sorted(column.items())]
        for column in compiler_columns
    ]

    out = {
        "schema": "w33.hesse36_fourier_twisted_compiler.v1",
        "status": "PASS_EXACT_36D_FOURIER_TWISTED_SL23_COMPILER",
        "headline": (
            "The order-three Hesse36 obstruction admits an exact linear repair. "
            "The ordinary 24-state SL(2,3) orbit is the regular representation, "
            "while the three safe 8-state orbits share one C3 stabilizer H. "
            "Assigning those three orbits the three characters of H gives "
            "Ind_H^G(1) + Ind_H^G(chi) + Ind_H^G(chi^2) = Reg(G). A 3-point "
            "Fourier transform on each of the eight right H-cosets supplies the "
            "24D intertwiner; the other 12 states already pair objectwise. The "
            "result is an exact rank-36 Q(omega) compiler intertwining all 24 "
            "physical SL(2,3) elements."
        ),
        "group": {
            "G": "SL(2,3)",
            "order": 24,
            "ordinary_orbits": [4, 4, 4, 24],
            "safe_orbits": [4, 4, 4, 8, 8, 8],
            "common_safe8_stabilizer_order": 3,
            "common_safe8_stabilizer_group_indices": list(H3),
            "safe8_character_assignment": ["1", "chi", "chi^2"],
            "induction_identity": (
                "Reg(G) = direct_sum_{chi in dual(C3)} Ind_C3^G(chi)"
            ),
        },
        "compiler": {
            "dimension": 36,
            "coefficient_field": "Q(omega), omega^2+omega+1=0",
            "rank": 36,
            "nonzero_entry_count": 84,
            "column_support_profile": {"1": 12, "3": 24},
            "column_squared_norm_profile": {"1": 12, "3": 24},
            "normalized_complex_unitary": (
                "multiply the 24 Fourier columns by 1/sqrt(3); "
                "the 12 objectwise columns already have norm 1"
            ),
            "target_column_to_source_rows_and_omega_exponents": serialized_columns,
            "exact_intertwining_checks": 24,
            "exact_group_law_checks": 24 * 24 * 36,
        },
        "representation_character": {
            "twisted_target_equals_ordinary_source": True,
            "profile_by_element_order": [
                {"order": 1, "class_size": 1, "trace": 36},
                {"order": 2, "class_size": 1, "trace": 12},
                {"order": 3, "class_size": 8, "trace": 3},
                {"order": 4, "class_size": 6, "trace": 0},
                {"order": 6, "class_size": 8, "trace": 3},
            ],
            "untwisted_order3_trace_before": 9,
            "twisted_order3_trace_after": 3,
            "ordinary_order3_trace": 3,
        },
        "architecture_reading": (
            "The missing ternary completion is a character/Fourier layer, not a "
            "new 36-state routing geometry. Twelve states compile by a literal "
            "object map. The remaining twenty-four compile as eight C3 fibers, "
            "Fourier transformed into the three character-labelled safe sheets."
        ),
        "boundary": (
            "This proves a finite complex-linear SL(2,3) intertwiner after a "
            "specific C3 character twist of the safe carrier. It does not prove "
            "that this twist is dynamically selected by E8, a heterotic vacuum, "
            "or photonic hardware. The 1/sqrt(3) normalization needed for a unitary "
            "implementation is a standard complex normalization outside Q(omega)."
        ),
        "parents": [
            "data/w33_hesse36_compiler36_sl23_obstruction.json",
            "data/w33_hesse36_q8_equivariant_repair.json",
            "data/w33_maximal_compiler_symmetry_pappus.json",
        ],
        "checks": {
            "ordinary24_is_regular_SL23": True,
            "three_safe8_share_one_C3_stabilizer": True,
            "eight_right_C3_cosets": True,
            "three_character_induced_sum_constructed": True,
            "compiler_rank36_exact": True,
            "compiler_columns_orthogonal_exactly": True,
            "twisted_target_group_law_all_products": True,
            "intertwines_all_24_group_elements_exactly": True,
            "twisted_character_matches_source": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
