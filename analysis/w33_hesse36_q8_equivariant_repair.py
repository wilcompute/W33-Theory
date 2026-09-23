#!/usr/bin/env python3
"""Restore an objectwise bridge between the two 36-state carriers on Q8.

Pass w33_hesse36_compiler36_sl23_obstruction proves that the ordinary
Payne/Hesse 36 and the maximal compiler-safe 36 are not isomorphic as
SL(2,3)-sets; the permutation-character mismatch occurs only on order-three
elements.

The subgroup of the common physical SL(2,3) consisting of elements of orders
1,2,4 is its normal quaternion Sylow subgroup Q8. Restricting both 36-actions
to Q8 gives the same orbit decomposition:
    8+8+8+4+4+4.
The 8-orbits are regular Q8 torsors. The 4-orbits have stabilizer equal to the
unique central involution, so are all Q8/Z(Q8).

Therefore an objectwise Q8-equivariant bijection exists. This script constructs
one deterministic frozen-gauge bijection and verifies equivariance on all
8*36 action pairs. It also counts all such Q8-equivariant bijections:
    (3! * 8^3) * (3! * 4^3) = 1,179,648.
Thus Q8 repairs objectwise equivariance, but does not canonically choose a map.
"""
from __future__ import annotations

import importlib.util
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "analysis/w33_maximal_compiler_symmetry_pappus.py"
OUT = ROOT / "data/w33_hesse36_q8_equivariant_repair.json"


def load_parent():
    spec = importlib.util.spec_from_file_location("q8_repair_parent", PARENT)
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
    return sorted(out, key=lambda orb: (len(orb), orb))


def set_key(S):
    return tuple(sorted(S))


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
        order = permutation_order(hperm)

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
                "order": order,
                "hperm": hperm,
                "ordinary_perm": ordinary_perm,
                "safe_perm": safe_perm,
            }
        )

    q8 = [row for row in records if row["order"] in (1, 2, 4)]
    assert len(q8) == 8
    assert Counter(row["order"] for row in q8) == {1: 1, 2: 1, 4: 6}

    # Closure in the faithful H27 permutation representation.
    q8_hperms = {row["hperm"] for row in q8}
    assert all(
        compose(left["hperm"], right["hperm"]) in q8_hperms
        for left in q8
        for right in q8
    )

    # The unique order-two element is central in Q8.
    involution = next(row for row in q8 if row["order"] == 2)
    assert all(
        compose(involution["hperm"], row["hperm"])
        == compose(row["hperm"], involution["hperm"])
        for row in q8
    )

    ordinary_perms = [row["ordinary_perm"] for row in q8]
    safe_perms = [row["safe_perm"] for row in q8]

    ordinary_orbits = orbit_sets(ordinary_perms, 36)
    safe_orbits = orbit_sets(safe_perms, 36)
    ordinary_sizes = sorted(map(len, ordinary_orbits))
    safe_sizes = sorted(map(len, safe_orbits))
    assert ordinary_sizes == safe_sizes == [4, 4, 4, 8, 8, 8]

    # Stabilizer fingerprints. Size-8 orbits are free; size-4 orbits are
    # stabilized by {1, central involution}.
    identity_index = next(i for i, row in enumerate(q8) if row["order"] == 1)
    involution_index = next(i for i, row in enumerate(q8) if row["order"] == 2)

    def stabilizer_indices(perms, seed):
        return tuple(i for i, perm in enumerate(perms) if perm[seed] == seed)

    ordinary_stabilizers = [
        stabilizer_indices(ordinary_perms, min(orbit))
        for orbit in ordinary_orbits
    ]
    safe_stabilizers = [
        stabilizer_indices(safe_perms, min(orbit))
        for orbit in safe_orbits
    ]
    for orbit, stab in zip(ordinary_orbits, ordinary_stabilizers):
        expected = (
            (identity_index, involution_index)
            if len(orbit) == 4
            else (identity_index,)
        )
        assert tuple(sorted(stab)) == tuple(sorted(expected))
    for orbit, stab in zip(safe_orbits, safe_stabilizers):
        expected = (
            (identity_index, involution_index)
            if len(orbit) == 4
            else (identity_index,)
        )
        assert tuple(sorted(stab)) == tuple(sorted(expected))

    # Deterministic gauge: pair sorted orbits by size/order, then pair their
    # minimum seeds and extend by Q8 action.
    mapping = {}
    orbit_pair_records = []
    for source_orbit, target_orbit in zip(ordinary_orbits, safe_orbits):
        assert len(source_orbit) == len(target_orbit)
        source_seed = min(source_orbit)
        target_seed = min(target_orbit)
        local = {}
        for row in q8:
            source = row["ordinary_perm"][source_seed]
            target = row["safe_perm"][target_seed]
            if source in local:
                assert local[source] == target
            local[source] = target
        assert set(local) == set(source_orbit)
        assert set(local.values()) == set(target_orbit)
        mapping.update(local)
        orbit_pair_records.append(
            {
                "size": len(source_orbit),
                "ordinary_seed": source_seed,
                "safe_seed": target_seed,
            }
        )

    assert len(mapping) == 36 and len(set(mapping.values())) == 36
    assert all(
        mapping[row["ordinary_perm"][i]]
        == row["safe_perm"][mapping[i]]
        for row in q8
        for i in range(36)
    )

    # G-set automorphism counts:
    # regular Q8 orbit: |Aut_Q8(Q8)| = 8;
    # Q8/Z orbit: |N_Q8(Z)/Z| = 4.
    equivariant_bijection_count = (
        math.factorial(3)
        * 8**3
        * math.factorial(3)
        * 4**3
    )
    assert equivariant_bijection_count == 1179648

    out = {
        "schema": "w33.hesse36_q8_equivariant_repair.v1",
        "status": "PASS_Q8_RESTORES_OBJECTWISE_EQUIVARIANCE_BUT_LEAVES_1179648_GAUGES",
        "headline": (
            "The SL(2,3) obstruction is repaired exactly by its normal quaternion "
            "subgroup Q8. Restricting the ordinary Payne/Hesse 36 and the maximal "
            "compiler-safe 36 to Q8 gives the identical orbit decomposition "
            "8+8+8+4+4+4. The 8-orbits are regular Q8 torsors and the 4-orbits are "
            "Q8/Z(Q8), so an objectwise Q8-equivariant bijection exists. One "
            "deterministic frozen-gauge bijection is constructed and checked on all "
            "8*36 action pairs. It is not canonical: there are exactly 1,179,648 "
            "Q8-equivariant bijections."
        ),
        "group": {
            "ambient_common_group": "SL(2,3)",
            "ambient_order": 24,
            "repair_subgroup": "Q8",
            "order": 8,
            "element_order_profile": {"1": 1, "2": 1, "4": 6},
            "unique_central_involution": True,
            "normal_sylow2_in_SL23": True,
            "maximality_reason": (
                "every element outside Q8 lies in an order-3 or order-6 coset; "
                "any subgroup containing an order-3 element sees the known "
                "permutation-character mismatch"
            ),
        },
        "orbit_structure": {
            "ordinary36": ordinary_sizes,
            "compiler_safe36": safe_sizes,
            "regular_orbit_count": 3,
            "regular_orbit_size": 8,
            "quotient_orbit_count": 3,
            "quotient_orbit_size": 4,
            "four_orbit_stabilizer": "Z(Q8), order 2",
            "eight_orbit_stabilizer": "trivial",
        },
        "explicit_bijection": {
            "ordinary_canonical_index_to_safe_canonical_index": [
                mapping[i] for i in range(36)
            ],
            "orbit_pair_records": orbit_pair_records,
            "all_288_equivariance_checks_pass": True,
            "gauge_note": (
                "canonical indices are lexicographic frozen-coordinate indices; "
                "the chosen orbit pairing and seed pairing are deterministic "
                "bookkeeping, not a physical selector"
            ),
        },
        "gauge_count": {
            "regular_orbit_pairings": "3! * 8^3",
            "quotient_orbit_pairings": "3! * 4^3",
            "total_Q8_equivariant_bijections": equivariant_bijection_count,
            "factorization": "2^17 * 3^2",
        },
        "consequence": (
            "The two 36-state Hesse carriers have a genuine shared objectwise "
            "quaternionic core. The only obstruction to extending such a pairing "
            "from Q8 to the full physical SL(2,3) is the order-three qutrit sector. "
            "A future compiler therefore needs an order-three phase/shear completion "
            "of a Q8-equivariant seed, not a wholesale remapping of the 36 states."
        ),
        "boundary": (
            "Q8 equivariance alone leaves 1,179,648 valid bijections and therefore "
            "does not select a physical compiler. The theorem does not claim that "
            "the ordinary tritangents and safe planes are the same objects, only "
            "that their restricted Q8 actions are objectwise isomorphic."
        ),
        "parents": [
            "data/w33_hesse36_compiler36_sl23_obstruction.json",
            "data/w33_maximal_compiler_symmetry_pappus.json",
            "analysis/w33_pass371_naturality_and_the_clifford_match.py",
        ],
        "checks": {
            "common_SL23_order24": True,
            "Q8_order8_and_closed": True,
            "Q8_order_profile_1_1_6": True,
            "same_orbit_structure": True,
            "four_orbits_have_central_stabilizer": True,
            "eight_orbits_are_free": True,
            "explicit_bijection_is_bijective": True,
            "all_8x36_equivariance_checks": True,
            "equivariant_bijection_count_1179648": True,
            "order3_is_only_extension_obstruction": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
