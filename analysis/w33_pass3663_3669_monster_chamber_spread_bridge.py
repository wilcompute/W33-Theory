"""Passes 3663-3669: exact U4(2) A6-chamber / W33-spread bridge.

Prior-art boundary
------------------
* Passes 3635-3648 already own the 432 A5 subgroups, the 36 A6 chambers,
  their S6 normalizers, and the 36 K6,6 component census.
* Passes 1072/1079 already own the identification of the degree-36 spread
  action and its rank-three orbitals.

This verifier proves the missing OBJECTWISE statement: the normalizer of every
A6 chamber fixes one and only one W33 spread, producing a canonical equivariant
bijection.  It also identifies the two A5 six-sets in a chamber as the two
faithful degree-six actions exchanged by the exceptional outer automorphism of
S6.  No Monster-word embedding or physical M36 magic-ray identification is
claimed.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path
from typing import Iterable

import numpy as np

P = 3
J4 = np.array(
    [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]],
    dtype=np.int64,
) % P
GENERATOR_VECTORS = (
    (1, 1, 0, 1),
    (0, 1, 2, 2),
    (1, 2, 2, 2),
    (1, 2, 1, 2),
)
A5_REPRESENTATIVE_WORDS = (
    ("aDbaDaca", "ACDAdc"),
    ("aDbaDaca", "bDaDbDa"),
)


def canonical(v: Iterable[int]) -> tuple[int, ...]:
    a = np.array(tuple(v), dtype=np.int64) % P
    for x in a:
        if int(x):
            return tuple(int(y) for y in (a * pow(int(x), -1, P)) % P)
    raise ValueError("zero vector")


POINTS = sorted({canonical(v) for v in product(range(P), repeat=4) if any(v)})
POINT_INDEX = {v: i for i, v in enumerate(POINTS)}
IDENTITY = tuple(range(len(POINTS)))


def symplectic(x: Iterable[int], y: Iterable[int]) -> int:
    return int(
        np.array(tuple(x), dtype=np.int64)
        @ J4
        @ np.array(tuple(y), dtype=np.int64)
        % P
    )


def transvection(v: Iterable[int]) -> tuple[int, ...]:
    vv = np.array(tuple(v), dtype=np.int64) % P
    out = []
    for x in POINTS:
        xx = np.array(x, dtype=np.int64)
        yy = (xx + symplectic(x, vv) * vv) % P
        out.append(POINT_INDEX[canonical(yy)])
    return tuple(out)


def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def closure(
    generators: Iterable[tuple[int, ...]], cap: int | None = None
) -> frozenset[tuple[int, ...]]:
    gens = list(generators)
    moves = list(dict.fromkeys(gens + [inverse(g) for g in gens]))
    seen = {IDENTITY}
    queue = deque([IDENTITY])
    while queue:
        h = queue.popleft()
        for g in moves:
            x = compose(g, h)
            if x not in seen:
                seen.add(x)
                queue.append(x)
                if cap is not None and len(seen) > cap:
                    return frozenset(seen)
    return frozenset(seen)


def permutation_order(g: tuple[int, ...]) -> int:
    seen = [False] * len(g)
    answer = 1
    for i in range(len(g)):
        if seen[i]:
            continue
        j = i
        cycle = 0
        while not seen[j]:
            seen[j] = True
            j = g[j]
            cycle += 1
        answer = lcm(answer, cycle)
    return answer


def conjugate(g: tuple[int, ...], h: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(g, h), inverse(g))


def conjugate_subgroup(
    g: tuple[int, ...], h: frozenset[tuple[int, ...]]
) -> frozenset[tuple[int, ...]]:
    return frozenset(conjugate(g, x) for x in h)


def subgroup_orbit(
    seed: frozenset[tuple[int, ...]], generators: Iterable[tuple[int, ...]]
) -> frozenset[frozenset[tuple[int, ...]]]:
    moves = list(generators)
    seen = {seed}
    queue = deque([seed])
    while queue:
        h = queue.popleft()
        for g in moves:
            k = conjugate_subgroup(g, h)
            if k not in seen:
                seen.add(k)
                queue.append(k)
    return frozenset(seen)


def commutator(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(compose(inverse(a), inverse(b)), a), b)


def normal_closure(
    seeds: Iterable[tuple[int, ...]], ambient_generators: Iterable[tuple[int, ...]]
) -> frozenset[tuple[int, ...]]:
    ambient_generators = list(ambient_generators)
    h = closure(seeds)
    while True:
        augmented = list(h)
        for g in ambient_generators:
            augmented.extend(conjugate(g, x) for x in h)
        k = closure(augmented)
        if k == h:
            return h
        h = k


def cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen = [False] * len(p)
    parts = []
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        size = 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            size += 1
        parts.append(size)
    return tuple(sorted(parts, reverse=True))


# The abstract W33/U4(2) carrier.
A = np.array(
    [
        [int(i != j and symplectic(x, y) == 0) for j, y in enumerate(POINTS)]
        for i, x in enumerate(POINTS)
    ],
    dtype=np.int64,
)
G4 = [transvection(v) for v in GENERATOR_VECTORS]
GROUP = closure(G4)
WORD_MOVES = {
    "a": G4[0],
    "b": G4[1],
    "c": G4[2],
    "d": G4[3],
    "A": inverse(G4[0]),
    "B": inverse(G4[1]),
    "C": inverse(G4[2]),
    "D": inverse(G4[3]),
}


def evaluate_word(word: str) -> tuple[int, ...]:
    h = IDENTITY
    for symbol in reversed(word):
        h = compose(WORD_MOVES[symbol], h)
    return h


# The 40 GQ lines and all 36 spreads.
line_set: set[frozenset[int]] = set()
for i in range(40):
    for j in range(i + 1, 40):
        if A[i, j]:
            common = set(np.flatnonzero(A[i] * A[j]))
            line = frozenset({i, j} | common)
            assert len(line) == 4
            line_set.add(line)
LINES = sorted(line_set, key=lambda line: tuple(sorted(line)))
LINE_INDEX = {line: i for i, line in enumerate(LINES)}
LINES_BY_POINT = {p: [i for i, line in enumerate(LINES) if p in line] for p in range(40)}

spread_accumulator: list[frozenset[int]] = []


def enumerate_spreads(chosen: list[int], covered: frozenset[int]) -> None:
    if len(covered) == 40:
        spread_accumulator.append(frozenset(chosen))
        return
    uncovered = [p for p in range(40) if p not in covered]
    point = min(
        uncovered,
        key=lambda p: sum(not (LINES[i] & covered) for i in LINES_BY_POINT[p]),
    )
    for line_index in LINES_BY_POINT[point]:
        if not (LINES[line_index] & covered):
            enumerate_spreads(
                chosen + [line_index], covered | LINES[line_index]
            )


enumerate_spreads([], frozenset())
SPREADS = sorted(set(spread_accumulator), key=lambda spread: tuple(sorted(spread)))


def act_line(g: tuple[int, ...], line_index: int) -> int:
    return LINE_INDEX[frozenset(g[p] for p in LINES[line_index])]


def act_spread(g: tuple[int, ...], spread: frozenset[int]) -> frozenset[int]:
    return frozenset(act_line(g, line_index) for line_index in spread)


# Reconstruct the two A5 orbits and the 36 A6 chambers from Pass 3635-3648.
A5_REPS = [
    closure(evaluate_word(word) for word in pair)
    for pair in A5_REPRESENTATIVE_WORDS
]
A5_ORBITS = [subgroup_orbit(h, G4) for h in A5_REPS]
A5S = sorted(A5_ORBITS[0] | A5_ORBITS[1], key=lambda h: tuple(sorted(h)))
A5_INDEX = {h: i for i, h in enumerate(A5S)}
A5_CLASS = {h: (0 if h in A5_ORBITS[0] else 1) for h in A5S}

A5_ADJ = [set() for _ in A5S]
D10_EDGES = []
for i, h in enumerate(A5S):
    for j in range(i + 1, len(A5S)):
        if len(h & A5S[j]) == 10:
            D10_EDGES.append((i, j))
            A5_ADJ[i].add(j)
            A5_ADJ[j].add(i)

COMPONENTS = []
seen_vertices: set[int] = set()
for root in range(len(A5S)):
    if root in seen_vertices:
        continue
    stack = [root]
    seen_vertices.add(root)
    component = []
    while stack:
        u = stack.pop()
        component.append(u)
        for v in A5_ADJ[u]:
            if v not in seen_vertices:
                seen_vertices.add(v)
                stack.append(v)
    COMPONENTS.append(sorted(component))


def first_a5_generators(
    h: frozenset[tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    involutions = [x for x in h if permutation_order(x) == 2]
    threes = [x for x in h if permutation_order(x) == 3]
    for a in involutions:
        for b in threes:
            if permutation_order(compose(a, b)) == 5:
                return a, b
    raise AssertionError("A5 generator pair missing")


A5_GENERATORS = {h: first_a5_generators(h) for h in A5S}
A6_GENERATORS: dict[frozenset[tuple[int, ...]], tuple[tuple[int, ...], ...]] = {}
for component in COMPONENTS:
    edge = next((u, v) for u in component for v in A5_ADJ[u] if u < v)
    generators = (*A5_GENERATORS[A5S[edge[0]]], *A5_GENERATORS[A5S[edge[1]]])
    h = closure(generators)
    A6_GENERATORS[h] = generators
A6S = sorted(A6_GENERATORS, key=lambda h: tuple(sorted(h)))
A6_INDEX = {h: i for i, h in enumerate(A6S)}

# Representative chamber, exact S6 normalizer, and its unique fixed spread.
A6_0 = A6S[0]
A6_0_GENERATORS = A6_GENERATORS[A6_0]
NORMALIZER_0 = frozenset(
    g
    for g in GROUP
    if all(conjugate(g, h) in A6_0 for h in A6_0_GENERATORS)
)
OUTER_ELEMENT = next(g for g in NORMALIZER_0 if g not in A6_0)
NORMALIZER_GENERATORS = (*A6_0_GENERATORS, OUTER_ELEMENT)
NORMALIZER_CLOSURE = closure(NORMALIZER_GENERATORS)
DERIVED_0 = normal_closure(
    [commutator(a, b) for a in NORMALIZER_GENERATORS for b in NORMALIZER_GENERATORS],
    NORMALIZER_GENERATORS,
)
FIXED_SPREADS = [
    spread for spread in SPREADS if all(act_spread(g, spread) == spread for g in NORMALIZER_0)
]
assert len(FIXED_SPREADS) == 1
SPREAD_0 = FIXED_SPREADS[0]
SPREAD_STABILIZER_0 = frozenset(
    g for g in GROUP if act_spread(g, SPREAD_0) == SPREAD_0
)

# Transport the unique fixed spread equivariantly through the 36 A6 chambers.
A6_TO_SPREAD: dict[frozenset[tuple[int, ...]], frozenset[int]] = {A6_0: SPREAD_0}
queue = deque([A6_0])
while queue:
    h = queue.popleft()
    spread = A6_TO_SPREAD[h]
    for g in G4:
        k = conjugate_subgroup(g, h)
        transported = act_spread(g, spread)
        assert k in A6_INDEX
        if k in A6_TO_SPREAD:
            assert A6_TO_SPREAD[k] == transported
        else:
            A6_TO_SPREAD[k] = transported
            queue.append(k)
MAPPED_SPREADS = [A6_TO_SPREAD[h] for h in A6S]

# Objectwise intersection dictionary and complementary rank-three graphs.
PAIR_DICTIONARY = Counter()
GRAPH_12 = np.zeros((36, 36), dtype=np.int64)
GRAPH_18 = np.zeros((36, 36), dtype=np.int64)
for i, h in enumerate(A6S):
    for j in range(i + 1, 36):
        subgroup_intersection = len(h & A6S[j])
        spread_intersection = len(MAPPED_SPREADS[i] & MAPPED_SPREADS[j])
        PAIR_DICTIONARY[(subgroup_intersection, spread_intersection)] += 1
        if subgroup_intersection == 12:
            GRAPH_12[i, j] = GRAPH_12[j, i] = 1
        elif subgroup_intersection == 18:
            GRAPH_18[i, j] = GRAPH_18[j, i] = 1
        else:
            raise AssertionError("unexpected A6 intersection")
I36 = np.eye(36, dtype=np.int64)
J36 = np.ones((36, 36), dtype=np.int64)

# The exceptional S6 double-six in one chamber.
LOCAL_A5 = [i for i, h in enumerate(A5S) if h <= A6_0]
LOCAL_SIDES = [
    [i for i in LOCAL_A5 if A5_CLASS[A5S[i]] == class_index]
    for class_index in (0, 1)
]
LOCAL_INTERSECTIONS = Counter()
for i, j in combinations(LOCAL_A5, 2):
    LOCAL_INTERSECTIONS[
        (A5_CLASS[A5S[i]], A5_CLASS[A5S[j]], len(A5S[i] & A5S[j]))
    ] += 1


def act_a5_index(g: tuple[int, ...], i: int) -> int:
    return A5_INDEX[conjugate_subgroup(g, A5S[i])]


SIDE_ACTIONS = []
for side in LOCAL_SIDES:
    position = {a5_index: i for i, a5_index in enumerate(side)}
    actions = [
        tuple(position[act_a5_index(g, a5_index)] for a5_index in side)
        for g in NORMALIZER_0
    ]
    SIDE_ACTIONS.append(actions)
OUTER_CYCLE_CENSUS = Counter(
    (cycle_type(left), cycle_type(right))
    for left, right in zip(SIDE_ACTIONS[0], SIDE_ACTIONS[1])
)

checks = {
    "w33_points_40": len(POINTS) == 40,
    "w33_lines_40": len(LINES) == 40,
    "w33_srg_40_12_2_4": np.array_equal(A @ A, 8 * np.eye(40, dtype=np.int64) - 2 * A + 4 * np.ones((40, 40), dtype=np.int64)),
    "u42_order_25920": len(GROUP) == 25_920,
    "spreads_36": len(SPREADS) == 36,
    "spread_intersections_1_4": Counter(len(a & b) for a, b in combinations(SPREADS, 2)) == Counter({1: 360, 4: 270}),
    "a5_two_orbits_216": [len(x) for x in A5_ORBITS] == [216, 216],
    "a5_total_432": len(A5S) == 432,
    "d10_edges_1296": len(D10_EDGES) == 1_296,
    "a6_chambers_36": len(A6S) == 36 and all(len(h) == 360 for h in A6S),
    "normalizer_order_720": len(NORMALIZER_0) == len(NORMALIZER_CLOSURE) == 720,
    "normalizer_derived_is_a6": DERIVED_0 == A6_0,
    "unique_normalizer_fixed_spread": len(FIXED_SPREADS) == 1,
    "normalizer_equals_spread_stabilizer": NORMALIZER_0 == SPREAD_STABILIZER_0,
    "equivariant_bijection_36": len(A6_TO_SPREAD) == 36 and len(set(MAPPED_SPREADS)) == 36,
    "intersection_dictionary": PAIR_DICTIONARY == Counter({(18, 1): 360, (12, 4): 270}),
    "order12_graph_srg_36_15_6_6": set(map(int, GRAPH_12.sum(axis=1))) == {15} and np.array_equal(GRAPH_12 @ GRAPH_12, 9 * I36 + 6 * J36),
    "order18_graph_srg_36_20_10_12": set(map(int, GRAPH_18.sum(axis=1))) == {20} and np.array_equal(GRAPH_18 @ GRAPH_18, 8 * I36 - 2 * GRAPH_18 + 12 * J36),
    "complementary_orbitals": np.array_equal(GRAPH_12 + GRAPH_18, J36 - I36),
    "double_six_sizes": [len(side) for side in LOCAL_SIDES] == [6, 6],
    "same_side_a4_cross_side_d10": sum(v for (a, b, n), v in LOCAL_INTERSECTIONS.items() if a == b and n == 12) == 30 and sum(v for (a, b, n), v in LOCAL_INTERSECTIONS.items() if a != b and n == 10) == 36,
    "two_faithful_degree6_actions": len(set(SIDE_ACTIONS[0])) == len(set(SIDE_ACTIONS[1])) == 720,
    "outer_transposition_triple_transposition_swap": OUTER_CYCLE_CENSUS[((2, 1, 1, 1, 1), (2, 2, 2))] == 15 and OUTER_CYCLE_CENSUS[((2, 2, 2), (2, 1, 1, 1, 1))] == 15,
    "outer_threecycle_doublethreecycle_swap": OUTER_CYCLE_CENSUS[((3, 1, 1, 1), (3, 3))] == 40 and OUTER_CYCLE_CENSUS[((3, 3), (3, 1, 1, 1))] == 40,
    "outer_sixcycle_321_swap": OUTER_CYCLE_CENSUS[((6,), (3, 2, 1))] == 120 and OUTER_CYCLE_CENSUS[((3, 2, 1), (6,))] == 120,
}
assert all(checks.values()), [name for name, value in checks.items() if not value]

cycle_census_json = {
    ".".join(map(str, left)) + " -> " + ".".join(map(str, right)): count
    for (left, right), count in sorted(OUTER_CYCLE_CENSUS.items())
}
result = {
    "schema": "w33.pass3663_3669.monster_chamber_spread_bridge.v1",
    "status": "PASS_EXACT_OBJECTWISE_BRIDGE",
    "checks": checks,
    "prior_art_boundary": {
        "already_known": [
            "Passes 3635-3648: 432 A5 subgroups, 36 A6 chambers, S6 normalizers, 36 K6,6 components",
            "Passes 1072/1079 and BT813: degree-36 spread action, subdegrees 1+15+20, and rank-three orbital graph",
        ],
        "new_here": [
            "canonical objectwise A6-chamber to spread bijection via equality of normalizer and spread stabilizer",
            "exact subgroup-intersection / spread-intersection dictionary",
            "A6 as the derived subgroup of the unique spread stabilizer",
            "explicit exceptional S6 outer-automorphism cycle-type certificate on the two A5 six-sets",
        ],
    },
    "carrier": {
        "group_order": len(GROUP),
        "points": len(POINTS),
        "lines": len(LINES),
        "spreads": len(SPREADS),
        "a5_subgroups": len(A5S),
        "a6_chambers": len(A6S),
    },
    "canonical_bijection": {
        "representative_normalizer_order": len(NORMALIZER_0),
        "representative_spread_stabilizer_order": len(SPREAD_STABILIZER_0),
        "normalizer_equals_stabilizer": NORMALIZER_0 == SPREAD_STABILIZER_0,
        "derived_subgroup_order": len(DERIVED_0),
        "derived_subgroup_is_a6": DERIVED_0 == A6_0,
        "fixed_spreads": len(FIXED_SPREADS),
        "image_size": len(set(MAPPED_SPREADS)),
        "equivariant_under_generators": True,
    },
    "intersection_dictionary": {
        "A6_intersection_18__spread_intersection_1": 360,
        "A6_intersection_12__spread_intersection_4": 270,
        "order12_relation": {
            "srg": [36, 15, 6, 6],
            "spectrum": {"15": 1, "3": 15, "-3": 20},
        },
        "order18_relation": {
            "srg": [36, 20, 10, 12],
            "spectrum": {"20": 1, "2": 20, "-4": 15},
        },
    },
    "exceptional_s6_double_six": {
        "a5_orbits_in_chamber": [6, 6],
        "within_orbit_intersection": "A4 of order 12",
        "cross_orbit_intersection": "D10 of order 10",
        "cross_intersection_graph": "K6,6",
        "both_degree6_actions_faithful": True,
        "cycle_type_pair_census": cycle_census_json,
        "interpretation": "The two six-sets are the two faithful degree-six S6 actions exchanged by the exceptional outer automorphism.",
    },
    "monster_boundary": {
        "structural_use": "Any concrete 5B-containing U4(2) embedding in the Monster transports this complete 36-spread/A6-chamber carrier and its double-six local charts.",
        "not_proved": [
            "serialized Monster words for the subgroup",
            "a unique Monster class fusion",
            "an identification with the non-SRG 36 magic-ray orthogonality graph",
            "a Griess, VOA, or photonic multiplication law",
        ],
    },
}
semantic = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
result["semantic_sha256"] = sha256(semantic).hexdigest()

if __name__ == "__main__":
    out = Path("data/PART_3663_3669_MONSTER_CHAMBER_SPREAD_BRIDGE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS_3663_3669", result["semantic_sha256"])
    print(json.dumps(result, indent=2))
