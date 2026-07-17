#!/usr/bin/env python3
"""Equivariance obstruction for closed-form W33 relay selectors.

The 135-byte selector is exact and tiny, but could it be replaced by a fully
symmetry-equivariant formula?  A deterministic equivariant selector would have
to choose a relay fixed by the stabilizer of every nonlocal source/destination
pair.

This verifier builds an explicit symplectic subgroup of the W33 automorphism
group.  For the nonlocal pair (0,1), the ordered-pair stabilizer has order 24
inside this subgroup and acts transitively on the four common relays.  Therefore
no relay is fixed, and no deterministic selector can be invariant under this
local stabilizer.  The finite 135-byte choice vector is not an implementation
accident; it breaks a real local symmetry.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_uor_runtime_model import ROOT, point_id


DEFAULT_JSON = ROOT / "data" / "w33_selector_equivariance_obstruction.json"
DEFAULT_MD = ROOT / "docs" / "w33_selector_equivariance_obstruction.md"

J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) % 3 for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def is_symplectic(matrix: list[list[int]]) -> bool:
    transpose = [[matrix[j][i] for j in range(4)] for i in range(4)]
    return matmul(matmul(transpose, J), matrix) == J


def transvection(v: tuple[int, int, int, int], alpha: int = 1) -> list[list[int]]:
    jv = [v[1] % 3, (2 * v[0]) % 3, v[3] % 3, (2 * v[2]) % 3]
    return [[(int(i == j) + alpha * v[i] * jv[j]) % 3 for j in range(4)] for i in range(4)]


def normalize(v: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    for c in v:
        if c:
            inv = 1 if c == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    raise ValueError("zero vector has no projective normalization")


def matrix_perm(matrix: list[list[int]]) -> tuple[int, ...]:
    point_index = {p: i for i, p in enumerate(hn.POINTS)}
    out = []
    for point in hn.POINTS:
        image = tuple(
            sum(matrix[row][col] * point[col] for col in range(4)) % 3 for row in range(4)
        )
        out.append(point_index[normalize(image)])
    return tuple(out)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(right)))


def generators() -> list[tuple[int, ...]]:
    matrices = [transvection(v) for v in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]]
    matrices += [
        [[0, 2, 0, 0], [1, 0, 0, 0], [0, 0, 0, 2], [0, 0, 1, 0]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]],
    ]
    return [matrix_perm(matrix) for matrix in matrices if is_symplectic(matrix)]


def closure(gens: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    identity = tuple(range(40))
    group = {identity}
    queue: deque[tuple[int, ...]] = deque([identity])
    while queue:
        current = queue.popleft()
        for gen in gens:
            candidate = compose(current, gen)
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    return group


def orbit(points: list[int], perms: list[tuple[int, ...]]) -> list[int]:
    seen = set()
    queue = deque(points)
    while queue:
        item = queue.popleft()
        if item in seen:
            continue
        seen.add(item)
        for perm in perms:
            image = perm[item]
            if image not in seen:
                queue.append(image)
    return sorted(seen)


def build_payload() -> dict[str, Any]:
    gens = generators()
    group = closure(gens)
    pair = next(
        (0, dst)
        for dst in range(1, len(hn.POINTS))
        if hn.symplectic(hn.POINTS[0], hn.POINTS[dst]) != 0
    )
    relays = [hn.POINTS.index(relay) for relay in hn.multipath(hn.POINTS[pair[0]], hn.POINTS[pair[1]])]
    ordered_stabilizer = [
        perm for perm in group if perm[pair[0]] == pair[0] and perm[pair[1]] == pair[1]
    ]
    unordered_stabilizer = [
        perm for perm in group if {perm[pair[0]], perm[pair[1]]} == set(pair)
    ]
    ordered_orbit = orbit([relays[0]], ordered_stabilizer)
    unordered_orbit = orbit([relays[0]], unordered_stabilizer)
    fixed_relays = [
        relay for relay in relays if all(perm[relay] == relay for perm in ordered_stabilizer)
    ]
    checks = {
        "generators_are_symplectic": len(gens) == 7,
        "subgroup_nontrivial": len(group) == 576,
        "selected_pair_is_nonlocal": hn.symplectic(hn.POINTS[pair[0]], hn.POINTS[pair[1]]) != 0,
        "four_common_relays": len(relays) == 4,
        "ordered_stabilizer_order_24": len(ordered_stabilizer) == 24,
        "unordered_stabilizer_order_48": len(unordered_stabilizer) == 48,
        "ordered_stabilizer_transitive_on_relays": ordered_orbit == sorted(relays),
        "unordered_stabilizer_transitive_on_relays": unordered_orbit == sorted(relays),
        "no_fixed_relay": fixed_relays == [],
    }
    return {
        "schema": "w33.selector_equivariance_obstruction.v1",
        "theorem": "local stabilizer transitivity obstructs a deterministic equivariant W33 relay selector",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "subgroup": {
            "generator_count": len(gens),
            "order": len(group),
            "description": "explicit symplectic subgroup generated by transvections and block/Weyl elements",
            "boundary": "This subgroup is enough for the obstruction; the full PSp(4,3) action is not required.",
        },
        "nonlocal_pair": {
            "indices": list(pair),
            "points": [point_id(hn.POINTS[pair[0]]), point_id(hn.POINTS[pair[1]])],
            "common_relays": relays,
            "common_relay_points": [point_id(hn.POINTS[idx]) for idx in relays],
        },
        "stabilizer_action": {
            "ordered_pair_stabilizer_order": len(ordered_stabilizer),
            "unordered_pair_stabilizer_order": len(unordered_stabilizer),
            "ordered_orbit_on_relays": ordered_orbit,
            "unordered_orbit_on_relays": unordered_orbit,
            "fixed_relays": fixed_relays,
        },
        "checks": checks,
        "interpretation": (
            "A deterministic equivariant selector would have to choose a relay fixed by the "
            "ordered-pair stabilizer.  The stabilizer moves the four common relays "
            "transitively, so no such fixed relay exists.  The balanced selector must "
            "therefore carry finite symmetry-breaking state."
        ),
        "honesty_boundary": (
            "This is a local obstruction to full deterministic equivariance.  It does "
            "not rule out smaller canonical rules, randomized equivariant selectors, or "
            "equivariant selectors with extra gauge/orientation data."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    pair = payload["nonlocal_pair"]
    action = payload["stabilizer_action"]
    return f"""# W(3,3) Selector Equivariance Obstruction

The balanced selector is not obviously replaceable by a fully equivariant
closed-form one-relay rule.

For the nonlocal pair `{pair['indices']}` the four common relays are:

```text
{pair['common_relays']}
```

An explicit symplectic subgroup of order `{payload['subgroup']['order']}` has
an ordered-pair stabilizer of order `{action['ordered_pair_stabilizer_order']}`.
That stabilizer acts transitively on the four relays:

```text
orbit = {action['ordered_orbit_on_relays']}
fixed = {action['fixed_relays']}
```

So there is no relay fixed by the local stabilizer.  Any deterministic selector
that chooses one of the four relays must break this local symmetry or accept
extra orientation/gauge data.

Boundary: this obstructs full deterministic equivariance; it does not obstruct
the exact finite 135-byte selector, randomized rules, or rules with additional
gauge state.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)
    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    print(f"subgroup order: {payload['subgroup']['order']}")
    print(f"ordered stabilizer: {payload['stabilizer_action']['ordered_pair_stabilizer_order']}")
    print(f"relay orbit: {payload['stabilizer_action']['ordered_orbit_on_relays']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
