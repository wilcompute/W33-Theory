#!/usr/bin/env python3
"""Fingerprint the order-96 PSp stabilizer of a Heawood/spread C6.

The PSp-equivariance certificate proves that the 270 intrinsic Heawood execution
C6 components form one transitive PSp(4,3)-orbit.  Hence a C6 stabilizer has
order 25920/270 = 96.  Pass 1996 independently identifies the corresponding
full order-51840 stabilizer as D8 x S4 of order 192.

This script closes the actual PSp stabilizer in its degree-270 permutation
action using Schreier generators, computes its center, derived subgroup and
element-order spectrum, and compares that fingerprint with every index-two
kernel in D8 x S4.  This identifies the subgroup type without relying on the
coincidence 96 = |Aut(tomotope)|.

It also freezes a hard no-go: the published tomotope group has derived subgroup
order 48 and trivial center, while any index-two subgroup of D8 x S4 has derived
subgroup contained in (D8 x S4)' = C2 x A4 of order 24.  Therefore the C6
stabilizer cannot be the tomotope group even before the finer fingerprint is
read.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_multichart_atlas import w33, chart_web  # noqa: E402
from w33_heawood_spread_pair_270_bridge import connected_components  # noqa: E402
from w33_heawood_spread_pair_psp_equivariance import (  # noqa: E402
    GENERATOR_VECTORS,
    intrinsic_slot_graph,
    induced_chart_perm,
    induced_line_perm,
    map_slot_node,
    transvection_point_perm,
)

OUT = ROOT / "data" / "w33_heawood_spread_pair_stabilizer96_fingerprint.json"
PSP43_ORDER = 25920
TOMOTOPE_ORDER = 96
TOMOTOPE_DERIVED_ORDER = 48
TOMOTOPE_CENTER_ORDER = 1


def compose(p, q):
    """Permutation composition p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def identity(n):
    return tuple(range(n))


def closure(generators, degree):
    e = identity(degree)
    gens = tuple(dict.fromkeys(g for g in generators if g != e))
    group = {e}
    frontier = [e]
    while frontier:
        x = frontier.pop()
        for g in gens:
            y = compose(g, x)
            if y not in group:
                group.add(y)
                frontier.append(y)
    return group


def perm_order(p):
    seen = [False] * len(p)
    out = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        n = 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            n += 1
        out = math.lcm(out, n)
    return out


def commutator(a, b):
    return compose(compose(compose(a, b), inverse(a)), inverse(b))


def derived_subgroup(group, degree):
    # For a group this small (96), closing all pairwise commutators is cheap and
    # avoids any dependence on a particular small generating set.
    comms = {
        commutator(a, b)
        for a in group
        for b in group
    }
    return closure(comms, degree)


def fingerprint(group, degree):
    hist = Counter(perm_order(g) for g in group)
    center = [
        g for g in group
        if all(compose(g, h) == compose(h, g) for h in group)
    ]
    derived = derived_subgroup(group, degree)
    dhist = Counter(perm_order(g) for g in derived)
    return {
        "order": len(group),
        "center_order": len(center),
        "derived_order": len(derived),
        "abelianization_order": len(group) // len(derived),
        "element_order_histogram": {str(k): v for k, v in sorted(hist.items())},
        "derived_element_order_histogram": {
            str(k): v for k, v in sorted(dhist.items())
        },
    }


def actual_component_generators():
    points, lines = w33()
    charts, web, _ = chart_web(lines)
    slot_adj, _ = intrinsic_slot_graph(charts, web, lines)
    components = connected_components(slot_adj)
    assert len(components) == 270 and {len(C) for C in components} == {6}
    component_index = {frozenset(C): i for i, C in enumerate(components)}

    perms = []
    for v in GENERATOR_VECTORS:
        pperm = transvection_point_perm(points, v)
        lperm = induced_line_perm(lines, pperm)
        cperm = induced_chart_perm(charts, lperm)
        mapped_nodes = {node: map_slot_node(node, cperm) for node in slot_adj}
        cp = []
        for comp in components:
            image = frozenset(mapped_nodes[node] for node in comp)
            cp.append(component_index[image])
        cp = tuple(cp)
        assert sorted(cp) == list(range(270))
        perms.append(cp)
    return tuple(perms)


def schreier_stabilizer(generators, base=0):
    degree = len(generators[0])
    e = identity(degree)
    reps = {base: e}
    q = deque([base])

    # reps[x] sends base to x.
    while q:
        x = q.popleft()
        rx = reps[x]
        for g in generators:
            y = g[x]
            if y not in reps:
                reps[y] = compose(g, rx)
                assert reps[y][base] == y
                q.append(y)

    schreier = set()
    for x, rx in reps.items():
        for g in generators:
            y = g[x]
            s = compose(inverse(reps[y]), compose(g, rx))
            assert s[base] == base
            if s != e:
                schreier.add(s)

    H = closure(schreier, degree)
    assert all(h[base] == base for h in H)
    return H, reps, schreier


# ---------------------------------------------------------------------------
# Abstract D8 x S4 index-two kernels, represented faithfully on 8 points.

def d8_perm(i, j):
    """r^i s^j on a square, with s:x -> -x mod 4."""
    return tuple((i + ((-x) if j else x)) % 4 for x in range(4))


def parity_of_perm(p):
    inv = 0
    for i, j in combinations(range(len(p)), 2):
        inv ^= int(p[i] > p[j])
    return inv


def combined_perm(i, j, s4):
    d = d8_perm(i, j)
    return tuple(d) + tuple(4 + s4[k] for k in range(4))


def index_two_kernel_candidates():
    s4s = tuple(permutations(range(4)))
    rows = []
    type_names = {
        (1, 0, 0): "V4 x S4",
        (0, 1, 0): "C4 x S4",
        (1, 1, 0): "V4 x S4",
        (0, 0, 1): "D8 x A4",
        (1, 0, 1): "mixed fibre product with V4 D8-kernel",
        (0, 1, 1): "mixed fibre product with C4 D8-kernel",
        (1, 1, 1): "mixed fibre product with V4 D8-kernel",
    }
    for coeff in (
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
        (0, 0, 1),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    ):
        a, b, c = coeff
        K = set()
        for i in range(4):
            for j in range(2):
                for s4 in s4s:
                    bit = (a * (i % 2) + b * j + c * parity_of_perm(s4)) % 2
                    if bit == 0:
                        K.add(combined_perm(i, j, s4))
        assert len(K) == 96
        rows.append(
            {
                "character_coefficients_rotparity_reflection_s4sign": list(coeff),
                "structure_type": type_names[coeff],
                "fingerprint": fingerprint(K, 8),
            }
        )
    return rows


def comparable_key(fp):
    return (
        fp["center_order"],
        fp["derived_order"],
        fp["abelianization_order"],
        tuple(sorted(fp["element_order_histogram"].items())),
        tuple(sorted(fp["derived_element_order_histogram"].items())),
    )


def build_result():
    generators = actual_component_generators()
    H, reps, schreier = schreier_stabilizer(generators, base=0)
    actual = fingerprint(H, 270)
    candidates = index_two_kernel_candidates()

    matches = [
        row for row in candidates
        if comparable_key(row["fingerprint"]) == comparable_key(actual)
    ]
    matched_types = sorted({row["structure_type"] for row in matches})

    checks = {
        "PSp_cycle_orbit_is_270": len(reps) == 270,
        "Schreier_stabilizer_has_order_96": len(H) == 96,
        "orbit_stabilizer_matches_25920": len(reps) * len(H) == PSP43_ORDER,
        "full_stabilizer_prior_result_is_D8xS4_order192": 2 * len(H) == 192,
        "derived_order_at_most_D8xS4_derived_24": actual["derived_order"] <= 24,
        "tomotope_96_is_ruled_out_by_derived_order": (
            actual["derived_order"] != TOMOTOPE_DERIVED_ORDER
        ),
        "tomotope_96_is_not_identified_by_order": not (
            actual["derived_order"] == TOMOTOPE_DERIVED_ORDER
            and actual["center_order"] == TOMOTOPE_CENTER_ORDER
        ),
        "fingerprint_matches_an_index2_D8xS4_kernel": len(matches) >= 1,
        "fingerprint_selects_one_isomorphism_type": len(matched_types) == 1,
    }

    return {
        "schema": "w33.heawood-spread-pair-stabilizer96-fingerprint.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The PSp(4,3) stabilizer of one intrinsic Heawood execution C6 is "
            "closed explicitly as a 96-element permutation group. Its exact "
            "center/derived/order-spectrum fingerprint selects one index-two "
            "subgroup type inside the prior D8 x S4 full stabilizer and rules "
            "out the order-96 tomotope automorphism group structurally."
        ),
        "actual_stabilizer": {
            **actual,
            "degree": 270,
            "Schreier_generators_before_reduction": len(schreier),
            "orbit_size": len(reps),
            "matched_index2_kernel_types": matched_types,
            "matching_character_rows": [
                row["character_coefficients_rotparity_reflection_s4sign"]
                for row in matches
            ],
        },
        "candidate_index2_kernels_of_D8xS4": candidates,
        "tomotope_firewall": {
            "tomotope_order": TOMOTOPE_ORDER,
            "tomotope_center_order_repo_certified": TOMOTOPE_CENTER_ORDER,
            "tomotope_derived_order_repo_certified": TOMOTOPE_DERIVED_ORDER,
            "parent_derived_group": "(D8 x S4)' = C2 x A4, order 24",
            "reason": (
                "For H <= D8 x S4, H' <= (D8 x S4)'. Therefore the PSp "
                "index-two stabilizer has derived order at most 24, whereas "
                "the published tomotope group has derived order 48."
            ),
        },
        "prior_repo_inputs": {
            "PSp_order": PSP43_ORDER,
            "full_G_spread_pair_stabilizer": "D8 x S4, order 192 (Pass 1996)",
            "tomotope_group": (
                "IdGroup [96,227], derived subgroup [48,50] = C2^4:C3, "
                "center order 1 (Pass 1376 published-generator audit)"
            ),
        },
        "claim_boundary": [
            "The candidate-type identification uses the prior theorem that the full stabilizer is D8 x S4.",
            "Matching a unique index-two-kernel fingerprint identifies the abstract subgroup type inside that parent; it does not identify it with an unrelated order-96 controller.",
            "The tomotope equality is explicitly falsified, not suggested, by the derived-subgroup obstruction.",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "order": result["actual_stabilizer"]["order"],
        "center_order": result["actual_stabilizer"]["center_order"],
        "derived_order": result["actual_stabilizer"]["derived_order"],
        "element_order_histogram": result["actual_stabilizer"]["element_order_histogram"],
        "matched_index2_kernel_types": result["actual_stabilizer"]["matched_index2_kernel_types"],
        "matching_character_rows": result["actual_stabilizer"]["matching_character_rows"],
        "tomotope_isomorphic": not result["checks"]["tomotope_96_is_ruled_out_by_derived_order"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
