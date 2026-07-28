#!/usr/bin/env python3
"""Pass 1191: exact 40-point PSp(4,3) rank-3 permutation module."""
from __future__ import annotations

from collections import deque
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1191_point_module_rank3.json"
Q = 3


def canon(x: tuple[int, ...]) -> tuple[int, ...]:
    x = tuple(a % Q for a in x)
    for a in x:
        if a:
            inv = 1 if a == 1 else 2
            return tuple((inv * b) % Q for b in x)
    raise ValueError("zero vector")


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % Q


def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def enumerate_group(generators: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for generator in generators:
            y = compose(generator, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return sorted(seen)


def orbit(seed: int, generators: list[tuple[int, ...]], allowed: set[int]) -> set[int]:
    seen = {seed}
    queue = deque([seed])
    while queue:
        x = queue.popleft()
        for generator in generators:
            y = generator[x]
            if y in allowed and y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def main() -> dict:
    points = sorted({
        canon(tuple(x))
        for x in product(range(Q), repeat=4)
        if any(x)
    })
    assert len(points) == 40
    index = {point: i for i, point in enumerate(points)}

    adjacency = [[0] * 40 for _ in range(40)]
    for i, x in enumerate(points):
        for j, y in enumerate(points):
            if i != j and symp(x, y) == 0:
                adjacency[i][j] = 1
    degrees = [sum(row) for row in adjacency]
    assert set(degrees) == {12}

    a2 = matmul(adjacency, adjacency)
    for i in range(40):
        for j in range(40):
            expected = 12 if i == j else (2 if adjacency[i][j] else 4)
            assert a2[i][j] == expected

    vectors = [
        (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
        (1, 1, 0, 0),
    ]
    generators = []
    for vector in vectors:
        permutation = []
        for point in points:
            scalar = symp(point, vector)
            image = tuple((point[i] + scalar * vector[i]) % Q for i in range(4))
            permutation.append(index[canon(image)])
        generators.append(tuple(permutation))

    group = enumerate_group(generators)
    assert len(group) == 25920
    stabilizer = [g for g in group if g[0] == 0]
    assert len(stabilizer) == 648

    stabilizer_generators = stabilizer  # small enough; direct orbit closure is deterministic.
    remaining = set(range(40))
    suborbits = []
    while remaining:
        seed = min(remaining)
        orb = orbit(seed, stabilizer_generators, remaining)
        suborbits.append(sorted(orb))
        remaining -= orb
    subdegrees = sorted(len(x) for x in suborbits)
    assert subdegrees == [1, 12, 27]

    # Exact ranks of the three spectral projectors from trace polynomials.
    tr_i = 40
    tr_a = sum(adjacency[i][i] for i in range(40))
    tr_a2 = sum(a2[i][i] for i in range(40))
    rank_12 = (tr_a2 + 2 * tr_a - 8 * tr_i) // 160
    rank_2 = -(tr_a2 - 8 * tr_a - 48 * tr_i) // 60
    rank_m4 = (tr_a2 - 14 * tr_a + 24 * tr_i) // 96
    # P12=(A-2I)(A+4I)/160; P2=-(A-12I)(A+4I)/60;
    # P-4=(A-12I)(A-2I)/96.
    assert [rank_12, rank_2, rank_m4] == [1, 24, 15]

    result = {
        "schema": "w33.pass1191.point_module_rank3.v1",
        "status": "PASS",
        "point_count": 40,
        "projective_group": "PSp(4,3)",
        "projective_group_order": len(group),
        "point_stabilizer_order": len(stabilizer),
        "point_stabilizer_subdegrees": subdegrees,
        "permutation_rank": len(subdegrees),
        "srg_parameters": [40, 12, 2, 4],
        "adjacency_spectrum": {"12": 1, "2": 24, "-4": 15},
        "point_permutation_module": "1 + 24 + 15",
        "irreducibility_reason": "A transitive rank-3 permutation character is multiplicity-free with three constituents; the adjacency eigenspaces have ranks 1,24,15.",
        "checks": {
            "forty_points": len(points) == 40,
            "psp_order_25920": len(group) == 25920,
            "stabilizer_order_648": len(stabilizer) == 648,
            "rank_three_subdegrees": subdegrees == [1, 12, 27],
            "module_1_24_15": [rank_12, rank_2, rank_m4] == [1, 24, 15],
        },
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1191 |PSp(4,3)|=25920 module=1+24+15")
    return result


if __name__ == "__main__":
    main()
