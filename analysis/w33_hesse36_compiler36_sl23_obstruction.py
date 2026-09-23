#!/usr/bin/env python3
"""Exact no-go for identifying the two natural 36-object Hesse carriers.

Carrier A (ordinary36): the 36 noncentral GQ(2,4) address lines, i.e. the
right cosets of the four selected noncentral H27 directions in the fixed
physical Clifford gauge.

Carrier B (safe36): the 36 maximal C3^2 subgroups of
K=H27_address x C3_external on which the regular address module and landed
operator module restrict isomorphically.

The fixed-center H27 automorphism group has order 216. Exactly 24 of those
automorphisms preserve the five selected GQ directions (center + four
noncentral lines); this is the physical split complement SL(2,3).

Under that common order-24 group:
  ordinary36 orbit sizes = 24+4+4+4
  safe36 orbit sizes     = 8+8+8+4+4+4

The permutation characters differ only on the two order-3 conjugacy classes:
  class order 1: 36 vs 36
  order 2:       12 vs 12
  order 3:        3 vs  9   <-- obstruction
  order 4:        0 vs  0
  order 6:        3 vs  3

Therefore no SL(2,3)-equivariant bijection exists between the two 36-sets.
The count 36=12x3 on both sides is real but not an objectwise symmetry
identification. The obstruction is concentrated exactly on the qutrit
order-three shear classes.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "analysis/w33_maximal_compiler_symmetry_pappus.py"
OUT = ROOT / "data/w33_hesse36_compiler36_sl23_obstruction.json"


def load_parent():
    spec = importlib.util.spec_from_file_location("compiler36_parent", PARENT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def permutation_order(p):
    seen = [False] * len(p)
    order = 1
    for start in range(len(p)):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            length += 1
            current = p[current]
        if length:
            order = math.lcm(order, length)
    return order


def orbit_sizes(permutations, degree):
    unseen = set(range(degree))
    sizes = []
    while unseen:
        seed = next(iter(unseen))
        orbit = {p[seed] for p in permutations}
        sizes.append(len(orbit))
        unseen -= orbit
    return sorted(sizes)


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(right)))


def inverse(permutation):
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def main(write=True):
    p = load_parent()

    directions = (
        (0, 0, 1),  # center
        (0, 1, 1),  # omega X
        (1, 0, 1),  # omega Z
        (1, 1, 0),  # Z X
        (1, 2, 2),  # omega^2 Z X^2
    )
    noncentral = directions[1:]

    def cyclic_subgroup(d):
        return frozenset((p.ID, d, p.hmul(d, d)))

    selected_subgroups = {cyclic_subgroup(d) for d in directions}
    assert len(selected_subgroups) == 5

    # Full fixed-center automorphism group Aut_z(H27), order 216.
    aut216 = [
        (u, v)
        for u in p.H
        for v in p.H
        if p.hcomm(u, v) == p.ZC and len(p.gen_h(u, v)) == 27
    ]
    assert len(aut216) == 216

    # Physical split complement: exactly those automorphisms preserving the
    # five selected GQ lines through the address identity.
    common24 = []
    for uv in aut216:
        images = {
            frozenset(p.phi(uv, g) for g in subgroup)
            for subgroup in selected_subgroups
        }
        if images == selected_subgroups:
            common24.append(uv)
    assert len(common24) == 24

    # Ordinary36: right cosets of the four selected noncentral directions.
    def right_coset(g, d):
        return frozenset(p.hmul(g, h) for h in (p.ID, d, p.hmul(d, d)))

    ordinary36 = set()
    for d in noncentral:
        ordinary36 |= {right_coset(g, d) for g in p.H}
    assert len(ordinary36) == 36
    ordinary36 = list(ordinary36)
    ordinary_index = {line: i for i, line in enumerate(ordinary36)}

    # Safe36: maximal order-nine subgroups avoiding D=[K,K].
    order9 = set()
    for x in p.K:
        for y in p.K:
            subgroup = p.subgroup_generated((x, y))
            if len(subgroup) == 9:
                order9.add(subgroup)
    safe36 = [subgroup for subgroup in order9 if subgroup & p.D == {p.KID}]
    assert len(safe36) == 36
    safe_index = {subgroup: i for i, subgroup in enumerate(safe36)}

    def ordinary_perm(uv):
        image = []
        for line in ordinary36:
            moved = frozenset(p.phi(uv, g) for g in line)
            assert moved in ordinary_index
            image.append(ordinary_index[moved])
        return tuple(image)

    def safe_perm(uv):
        image = []
        for subgroup in safe36:
            moved = frozenset((p.phi(uv, g), ext) for g, ext in subgroup)
            assert moved in safe_index
            image.append(safe_index[moved])
        return tuple(image)

    ordinary_perms = [ordinary_perm(uv) for uv in common24]
    safe_perms = [safe_perm(uv) for uv in common24]

    # Identify group-element order from its exact action on H27.
    h_index = {g: i for i, g in enumerate(p.H)}
    h_perms = [
        tuple(h_index[p.phi(uv, g)] for g in p.H)
        for uv in common24
    ]

    profile = Counter()
    per_element = []
    for hperm, operm, sperm in zip(h_perms, ordinary_perms, safe_perms):
        order = permutation_order(hperm)
        fixed_ordinary = sum(i == j for i, j in enumerate(operm))
        fixed_safe = sum(i == j for i, j in enumerate(sperm))
        profile[(order, fixed_ordinary, fixed_safe)] += 1
        per_element.append(
            {
                "order": order,
                "ordinary36_fixed": fixed_ordinary,
                "safe36_fixed": fixed_safe,
            }
        )

    expected_profile = Counter(
        {
            (1, 36, 36): 1,
            (2, 12, 12): 1,
            (3, 3, 9): 8,
            (4, 0, 0): 6,
            (6, 3, 3): 8,
        }
    )
    assert profile == expected_profile

    ordinary_orbits = orbit_sizes(ordinary_perms, 36)
    safe_orbits = orbit_sizes(safe_perms, 36)
    assert ordinary_orbits == [4, 4, 4, 24]
    assert safe_orbits == [4, 4, 4, 8, 8, 8]

    # A G-set bijection would force equality of permutation characters.
    character_equal = all(
        row["ordinary36_fixed"] == row["safe36_fixed"]
        for row in per_element
    )
    assert character_equal is False

    mismatch_orders = sorted(
        {
            row["order"]
            for row in per_element
            if row["ordinary36_fixed"] != row["safe36_fixed"]
        }
    )
    assert mismatch_orders == [3]

    # Element order alone merges distinct conjugacy classes in SL(2,3).
    # Compute the actual seven classes so the order-three obstruction is not
    # over-described as one size-eight class.
    group = set(h_perms)
    identity = tuple(range(27))
    assert len(group) == 24 and identity in group
    fixed_by_element = {
        hperm: (sum(i == j for i, j in enumerate(operm)),
                sum(i == j for i, j in enumerate(sperm)))
        for hperm, operm, sperm in zip(h_perms, ordinary_perms, safe_perms)
    }
    unseen = set(group)
    conjugacy_classes = []
    while unseen:
        representative = min(unseen)
        class_set = {
            compose(compose(g, representative), inverse(g)) for g in group
        }
        assert class_set <= group
        conjugacy_classes.append(class_set)
        unseen -= class_set
    conjugacy_classes.sort(
        key=lambda cls: (permutation_order(next(iter(cls))), len(cls), min(cls))
    )
    assert len(conjugacy_classes) == 7
    conjugacy_profile = []
    order_labels = Counter()
    for cls in conjugacy_classes:
        representative = min(cls)
        order = permutation_order(representative)
        fixed_pairs = {fixed_by_element[element] for element in cls}
        assert len(fixed_pairs) == 1
        fixed_ordinary, fixed_safe = next(iter(fixed_pairs))
        order_labels[order] += 1
        label = f"{order}{chr(64 + order_labels[order])}"
        conjugacy_profile.append(
            {
                "class_label": label,
                "element_order": order,
                "class_size": len(cls),
                "ordinary36_fixed": fixed_ordinary,
                "compiler_safe36_fixed": fixed_safe,
                "character_mismatch": fixed_ordinary != fixed_safe,
            }
        )
    assert Counter((row["element_order"], row["class_size"])
                   for row in conjugacy_profile) == Counter(
        {(1, 1): 1, (2, 1): 1, (3, 4): 2, (4, 6): 1, (6, 4): 2}
    )
    assert [row["class_size"] for row in conjugacy_profile
            if row["element_order"] == 3] == [4, 4]
    assert all(row["character_mismatch"] == (row["element_order"] == 3)
               for row in conjugacy_profile)

    out = {
        "schema": "w33.hesse36_compiler36_sl23_obstruction.v2",
        "status": "PASS_HESSE36_COMPILER36_COMMON_SL23_EQUIVARIANT_BIJECTION_OBSTRUCTED_AT_ORDER3",
        "headline": (
            "The two natural 36=12x3 Hesse carriers are not the same physical "
            "SL(2,3)-set. Under the exact common order-24 split complement, the "
            "ordinary Payne/Hesse 36 has orbits 24+4+4+4 while the 36 maximal "
            "compiler-safe C3^2 planes have orbits 8+8+8+4+4+4. Their permutation "
            "characters agree on every element order except 3, where the fixed-point "
            "counts are 3 versus 9. Thus no common-SL(2,3)-equivariant objectwise "
            "bijection exists; the obstruction is concentrated on both size-four "
            "order-three conjugacy classes."
        ),
        "common_group": {
            "description": (
                "fixed-center H27 automorphisms preserving the five selected "
                "GQ(2,4) directions through the identity"
            ),
            "order": 24,
            "identification": "SL(2,3), the physical split complement in Clifford648",
            "parent_fixed_center_automorphism_order": 216,
        },
        "carriers": {
            "ordinary36": {
                "count": 36,
                "definition": (
                    "right cosets of the four selected noncentral H27 directions; "
                    "the 36 ordinary Payne/Hesse address lines"
                ),
                "orbit_sizes_under_common_SL23": ordinary_orbits,
            },
            "compiler_safe36": {
                "count": 36,
                "definition": (
                    "maximal order-nine C3^2 subgroups of H27 x C3_external "
                    "avoiding the characteristic commutator line"
                ),
                "orbit_sizes_under_common_SL23": safe_orbits,
            },
        },
        "permutation_character_profile": [
            {
                "element_order": order,
                "element_count": count,
                "ordinary36_fixed": fixed_ordinary,
                "compiler_safe36_fixed": fixed_safe,
            }
            for (order, fixed_ordinary, fixed_safe), count in sorted(profile.items())
        ],
        "conjugacy_class_profile": conjugacy_profile,
        "obstruction": {
            "permutation_characters_equal": False,
            "mismatch_element_orders": mismatch_orders,
            "order3_element_count": 8,
            "order3_conjugacy_class_sizes": [4, 4],
            "order3_fixed_points_ordinary36": 3,
            "order3_fixed_points_compiler_safe36": 9,
            "equivariant_bijection_exists": False,
            "interpretation": (
                "the repeated 36=12x3 Hesse factorization survives as a structural "
                "parallel, but its phase lift and compiler-center lift respond "
                "differently on both qutrit order-three shear/transvection classes"
            ),
        },
        "boundary": (
            "This is a no-go only for an objectwise bijection equivariant under "
            "the exact common physical SL(2,3) complement. It does not rule out "
            "a smaller-subgroup pairing, a Fourier/induced transform between the "
            "two permutation modules, or a symmetry-changing compiler."
        ),
        "parents": [
            "analysis/w33_maximal_compiler_symmetry_pappus.py",
            "analysis/w33_address_operator_h27_roles.py",
            "docs/PAYNE_HESSE_PACKET_DICTIONARY.md",
        ],
        "checks": {
            "fixed_center_aut_order216": True,
            "common_physical_complement_order24": True,
            "ordinary36_preserved": True,
            "compiler_safe36_preserved": True,
            "ordinary_orbits_24_4_4_4": True,
            "safe_orbits_8_8_8_4_4_4": True,
            "character_mismatch_only_order3": True,
            "order3_sector_is_two_classes_of_four": True,
            "no_SL23_equivariant_bijection": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
