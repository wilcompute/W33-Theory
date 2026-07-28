#!/usr/bin/env python3
"""Pass 1196: exact short Ihara orbit classification and the W(E6) action boundary.

PSp(4,3) is generated projectively by symplectic transvections on the 40 points.
Primitive cycles of lengths 3 and 4 are classified exactly into group orbits.
The degree-5--40 census is supplied by Pass 1195, but individual orbit enumeration
at those astronomical sizes is deliberately not claimed.
"""
from __future__ import annotations

from collections import deque
from itertools import combinations
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1196_equivariant_ihara_orbit_boundary.json"

P = 3
J = np.array([
    [0, 1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, -1, 0],
], dtype=int) % P


def canon_vec(v: tuple[int, ...]) -> tuple[int, ...]:
    for x in v:
        if x % P:
            inv = 1 if x % P == 1 else 2
            return tuple((inv * y) % P for y in v)
    raise ValueError("zero vector")


def points() -> tuple[tuple[int, ...], ...]:
    pts = {canon_vec(tuple(v)) for v in np.ndindex(*(P,) * 4) if any(v)}
    assert len(pts) == 40
    return tuple(sorted(pts))


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return int(np.asarray(a, dtype=int) @ J @ np.asarray(b, dtype=int)) % P


def adjacency_matrix(pts: tuple[tuple[int, ...], ...]) -> np.ndarray:
    n = len(pts)
    A = np.zeros((n, n), dtype=np.uint8)
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    assert np.all(A.sum(axis=1) == 12)
    assert np.array_equal(A @ A, 8 * np.eye(40, dtype=int) - 2 * A + 4 * np.ones((40, 40), dtype=int))
    return A


def transvection_action(pts: tuple[tuple[int, ...], ...], v: tuple[int, ...]) -> np.ndarray:
    index = {x: i for i, x in enumerate(pts)}
    out = np.empty(40, dtype=np.uint8)
    vv = np.asarray(v, dtype=int)
    for i, x in enumerate(pts):
        xx = np.asarray(x, dtype=int)
        y = tuple((xx + symp(x, v) * vv) % P)
        out[i] = index[canon_vec(y)]
    return out


def compose(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a[b]


def projective_group(gens: tuple[np.ndarray, ...]) -> tuple[np.ndarray, ...]:
    identity = np.arange(40, dtype=np.uint8)
    seen = {identity.tobytes()}
    out = [identity]
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = compose(g, x)
            key = y.tobytes()
            if key not in seen:
                seen.add(key)
                out.append(y)
                queue.append(y)
    assert len(out) == 25920
    return tuple(out)


def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    n = len(cycle)
    rotations = [cycle[i:] + cycle[:i] for i in range(n)]
    rev = tuple(reversed(cycle))
    rotations += [rev[i:] + rev[:i] for i in range(n)]
    return min(rotations)


def enumerate_cycles(A: np.ndarray, length: int) -> tuple[tuple[int, ...], ...]:
    cycles: set[tuple[int, ...]] = set()
    n = len(A)
    def extend(path: list[int]) -> None:
        if len(path) == length:
            if A[path[-1], path[0]]:
                cycles.add(canonical_cycle(tuple(path)))
            return
        for y in np.flatnonzero(A[path[-1]]):
            y = int(y)
            if y not in path:
                extend(path + [y])
    for start in range(n):
        extend([start])
    return tuple(sorted(cycles))


def orbit_partition(objects: tuple[tuple[int, ...], ...], gens: tuple[np.ndarray, ...]) -> list[list[int]]:
    index = {x: i for i, x in enumerate(objects)}
    actions = []
    for g in gens:
        action = np.empty(len(objects), dtype=np.int32)
        for i, obj in enumerate(objects):
            image = canonical_cycle(tuple(int(g[x]) for x in obj))
            action[i] = index[image]
        actions.append(action)
    unseen = set(range(len(objects)))
    orbits = []
    while unseen:
        seed = min(unseen)
        orb = {seed}
        q = deque([seed])
        while q:
            x = q.popleft()
            for a in actions:
                y = int(a[x])
                if y not in orb:
                    orb.add(y)
                    q.append(y)
        unseen -= orb
        orbits.append(sorted(orb))
    return sorted(orbits, key=lambda o: (len(o), o[0]))


def main() -> dict[str, object]:
    pts = points()
    A = adjacency_matrix(pts)
    gens = tuple(transvection_action(pts, v) for v in pts)
    unique = {}
    for g in gens:
        unique[g.tobytes()] = g
    gens = tuple(unique.values())
    group = projective_group(gens)
    assert all(np.array_equal(A[np.ix_(g, g)], A) for g in gens)

    triangles = enumerate_cycles(A, 3)
    four_cycles = enumerate_cycles(A, 4)
    assert len(triangles) == 160
    assert len(four_cycles) == 1740

    tri_orbits = orbit_partition(triangles, gens)
    four_orbits = orbit_partition(four_cycles, gens)
    assert [len(o) for o in tri_orbits] == [160]
    assert sorted(len(o) for o in four_orbits) == [120, 1620]

    four_records = []
    for orb in four_orbits:
        rep = four_cycles[orb[0]]
        all_pair_adjacent = all(A[i, j] for i, j in combinations(rep, 2))
        kind = "line_internal_K4_cycle" if all_pair_adjacent else "GQ_apartment"
        expected = 120 if all_pair_adjacent else 1620
        assert len(orb) == expected
        four_records.append({
            "kind": kind,
            "orbit_size": len(orb),
            "stabilizer_order": len(group) // len(orb),
            "representative": list(rep),
        })

    result = {
        "schema": "w33.pass1196.equivariant_ihara_orbit_boundary.v1",
        "status": "PASS",
        "point_action": {
            "group": "PSp(4,3)",
            "generated_order": len(group),
            "degree": 40,
            "generator_family": "projective symplectic transvections",
            "graph_parameters": [40, 12, 2, 4],
        },
        "primitive_cycle_orbits": {
            "length_3": [{
                "kind": "line_triangle",
                "orbit_size": 160,
                "stabilizer_order": len(group) // 160,
                "representative": list(triangles[tri_orbits[0][0]]),
            }],
            "length_4": sorted(four_records, key=lambda x: x["orbit_size"]),
        },
        "checks": {
            "triangles_one_PSp_orbit": len(tri_orbits) == 1,
            "length4_two_PSp_orbits": len(four_orbits) == 2,
            "length4_split_120_plus_1620": sorted(len(o) for o in four_orbits) == [120, 1620],
            "apartment_stabilizer_16": any(x["kind"] == "GQ_apartment" and x["stabilizer_order"] == 16 for x in four_records),
        },
        "WE6_boundary": {
            "statement": "The honest 40-point graph action constructed here is PSp(4,3), order 25920. W(E6), order 51840, is an index-two phase/Weyl extension and is not promoted here to a second faithful point-graph action.",
            "consequence": "Primitive W33 graph cycles have PSp(4,3) orbit classes. A W(E6)-equivariant classification requires a separately specified phase-lifted carrier; doubling the group order alone does not create new graph automorphisms.",
            "large_length_policy": "Pass 1195 gives exact primitive counts through length 40. Individual orbit enumeration beyond length 4 is astronomically large and is not falsely claimed.",
        },
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "triangle_orbits": [len(o) for o in tri_orbits], "four_cycle_orbits": sorted(len(o) for o in four_orbits)}, indent=2))
    return result


if __name__ == "__main__":
    main()
