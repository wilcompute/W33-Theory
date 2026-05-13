#!/usr/bin/env python3
"""Part CCCCCXCVI: six-kernel subgroup bridge to tetrahedral edge action.

This module takes the induced six-slot tomotope action from
`data/tomotope_six_kernel_generator_alignment.json` and identifies the generated
subgroup as the standard `S4` action on the six edges of a tetrahedron.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from itertools import permutations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT_PATH = ROOT / "data" / "tomotope_six_kernel_generator_alignment.json"
OUT_PATH = ROOT / "data" / "tomotope_six_kernel_s4_edge_bridge.json"


def _compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def _inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    inv = [0] * len(p)
    for i, j in enumerate(p):
        inv[j] = i
    return tuple(inv)


def _cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen = [False] * len(p)
    lengths: list[int] = []
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        count = 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            count += 1
        lengths.append(count)
    return tuple(sorted(lengths, reverse=True))


def _closure(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    n = len(generators[0])
    identity = tuple(range(n))
    group: set[tuple[int, ...]] = {identity}
    frontier = [identity]
    while frontier:
        g = frontier.pop()
        for a in generators:
            h = _compose(a, g)
            if h not in group:
                group.add(h)
                frontier.append(h)
    return group


def _parse_slot_action(data: dict[str, Any]) -> dict[str, tuple[int, ...]]:
    actions = data["induced_slot_actions"]
    labels = [f"k{i}" for i in range(1, 7)]
    label_to_index = {label: idx for idx, label in enumerate(labels)}
    parsed: dict[str, tuple[int, ...]] = {}
    for name, image in actions.items():
        parsed[name] = tuple(label_to_index[label] for label in image)
    return parsed


def _tetrahedral_edge_action_group() -> set[tuple[int, ...]]:
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    edge_index = {edge: idx for idx, edge in enumerate(edges)}

    action: set[tuple[int, ...]] = set()
    for perm in permutations(vertices):
        image: list[int] = []
        for u, v in edges:
            uv = tuple(sorted((perm[u], perm[v])))
            image.append(edge_index[uv])
        action.add(tuple(image))
    return action


def _find_conjugator(
    group_g: set[tuple[int, ...]],
    group_h: set[tuple[int, ...]],
) -> tuple[int, ...] | None:
    if len(group_g) != len(group_h):
        return None
    n = len(next(iter(group_g)))
    for pi_raw in permutations(range(n)):
        pi = tuple(pi_raw)
        pi_inv = _inverse(pi)
        conj = {
            _compose(pi, _compose(g, pi_inv))
            for g in group_g
        }
        if conj == group_h:
            return pi
    return None


@dataclass(frozen=True)
class BridgeSummary:
    slot_count: int
    generated_group_order: int
    tetrahedral_edge_group_order: int
    action_is_transitive: bool
    conjugate_to_tetrahedral_edge_action: bool


def build_bridge() -> dict[str, Any]:
    alignment = json.loads(ALIGNMENT_PATH.read_text(encoding="utf-8"))
    slot_actions = _parse_slot_action(alignment)
    generators = list(slot_actions.values())

    generated_group = _closure(generators)
    tetra_group = _tetrahedral_edge_action_group()
    conjugator = _find_conjugator(generated_group, tetra_group)

    # Orbit on slots under generated group
    orbit = set()
    frontier = [0]
    while frontier:
        x = frontier.pop()
        if x in orbit:
            continue
        orbit.add(x)
        for g in generated_group:
            y = g[x]
            if y not in orbit:
                frontier.append(y)

    cycle_types: dict[str, int] = {}
    for g in generated_group:
        key = "-".join(map(str, _cycle_type(g)))
        cycle_types[key] = cycle_types.get(key, 0) + 1

    summary = BridgeSummary(
        slot_count=6,
        generated_group_order=len(generated_group),
        tetrahedral_edge_group_order=len(tetra_group),
        action_is_transitive=(len(orbit) == 6),
        conjugate_to_tetrahedral_edge_action=(conjugator is not None),
    )

    return {
        "summary": asdict(summary),
        "slot_generators": {k: list(v) for k, v in slot_actions.items()},
        "cycle_type_distribution": cycle_types,
        "canonical_bivector_slots": {
            "k1": "B01",
            "k2": "B02",
            "k3": "B03",
            "k4": "B12",
            "k5": "B13",
            "k6": "B23",
        },
        "conjugator_to_tetrahedral_edge_model": list(conjugator) if conjugator else None,
        "notes": (
            "The tomotope six-slot action generated by p0..p3 has order 24 and is "
            "conjugate in S6 to the standard S4 action on the six edges of a tetrahedron."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
