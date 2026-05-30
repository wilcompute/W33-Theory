#!/usr/bin/env python3
"""Qutrit projective projection fiber tower.

This verifies the geometric version of the recursion

    N_n = 9 N_(n-1) + 4

by projecting higher n-qutrit projective Pauli spaces onto the n=2 W33 base.

For q=3, the n-qutrit projective Pauli space is PG(2n-1,3), with

    N_n = (3^(2n)-1)/2.

Project PG(2n-1,3) -> PG(3,3) by forgetting the last 2(n-2) coordinates.
The map is undefined on the projective kernel PG(2n-5,3).  Off the kernel,
each of the 40 base points has exactly 3^(2n-4) points in its fiber.

Therefore:

    n=3: 364 = 40*9  + 4
    n=4: 3280 = 40*81 + 40
    n=5: 29524 = 40*729 + 364

This makes the 9-adic shell exact: higher qutrit Pauli geometries are affine
fiber towers over W33, with the previous lower-level projective space as kernel.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

q = 3
base_n = 2
base_dim = 2 * base_n
base_points = 40


def normalize(v):
    v = tuple(x % q for x in v)
    if not any(v):
        raise ValueError("zero")
    i = next(i for i, x in enumerate(v) if x)
    inv = 1 if v[i] == 1 else 2
    return tuple((inv * x) % q for x in v)


def projective_points(vector_dim: int):
    return sorted({normalize(v) for v in itertools.product(range(q), repeat=vector_dim) if any(v)})


def N(n: int) -> int:
    return (q ** (2 * n) - 1) // (q - 1)


def projection_to_base(point, n: int):
    head = point[:base_dim]
    if not any(head):
        return None
    return normalize(head)


def fiber_stats(n: int):
    pts = projective_points(2 * n)
    base = projective_points(base_dim)
    counts = Counter()
    kernel = 0
    for p in pts:
        b = projection_to_base(p, n)
        if b is None:
            kernel += 1
        else:
            counts[b] += 1
    return {
        "n": n,
        "total_points": len(pts),
        "base_points_hit": len(counts),
        "fiber_size_distribution": dict(Counter(counts.values())),
        "kernel_points": kernel,
        "expected_fiber_size": q ** (2 * n - 4),
        "expected_kernel_size": N(n - base_n) if n > base_n else 0,
        "identity": f"{N(n)} = 40*{q ** (2*n-4)} + {N(n-base_n) if n > base_n else 0}" if n > base_n else "base",
    }


def build_payload() -> dict:
    stats = {n: fiber_stats(n) for n in range(2, 6)}
    identities = {
        "base_pg33_has_40_points": stats[2]["total_points"] == 40,
        "n3_projection_364_equals_40_times_9_plus_4": stats[3]["total_points"] == 364 and stats[3]["fiber_size_distribution"] == {9: 40} and stats[3]["kernel_points"] == 4,
        "n4_projection_3280_equals_40_times_81_plus_40": stats[4]["total_points"] == 3280 and stats[4]["fiber_size_distribution"] == {81: 40} and stats[4]["kernel_points"] == 40,
        "n5_projection_29524_equals_40_times_729_plus_364": stats[5]["total_points"] == 29524 and stats[5]["fiber_size_distribution"] == {729: 40} and stats[5]["kernel_points"] == 364,
        "kernel_is_previous_tower_level": all(stats[n]["kernel_points"] == N(n - 2) for n in range(3, 6)),
        "fiber_size_is_9_power": all(list(stats[n]["fiber_size_distribution"].keys()) == [q ** (2*n-4)] for n in range(3, 6)),
    }
    return {
        "theorem": "qutrit_projection_fiber_tower",
        "projection": "PG(2n-1,3) -> PG(3,3) by forgetting the last 2(n-2) coordinates",
        "fiber_law": "N_n = 40*3^(2n-4) + N_(n-2) for n>=3",
        "stats": stats,
        "structural_reading": {
            "n3": "PG(5,3) is 40 affine 9-fibers over W33 plus a kernel PG(1,3) of 4 points",
            "n4": "PG(7,3) is 40 affine 81-fibers over W33 plus a kernel PG(3,3) of 40 points",
            "general": "higher qutrit Pauli shells are W33-indexed affine 9-adic fibers plus a lower qutrit kernel",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_qutrit_projection_fiber_tower.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
