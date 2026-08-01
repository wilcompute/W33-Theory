#!/usr/bin/env python3
"""Prepare deterministic exact-dual-enumerator inputs for Pass 1876.

The 45 dual generators are ordered by the canonical six-line separator:
30 fiber rows followed by the 15 residual duad rows. The stabilizer of the
six-line pack in W(E6) has order 720 and induces the full S6 action on the
residual assignments, reducing 2^15 assignments to 156 orbits.
"""
from __future__ import annotations

import collections
import importlib.util
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "analysis" / "w33_pass1801_1805_common.py"
COMPRESSION = ROOT / "data" / "w33_pass1837_middle_layer_compression.json"
ROWS = ROOT / "data" / "w33_pass1876_rows45_hex.txt"
ORBITS = ROOT / "data" / "w33_pass1876_residual_orbits.txt"
SUMMARY = ROOT / "data" / "w33_pass1876_input_summary.json"


def load_common():
    spec = importlib.util.spec_from_file_location("w33_common", COMMON)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[i]] for i in range(len(left)))


def transport(mask: int, permutation: tuple[int, ...]) -> int:
    out = 0
    while mask:
        bit = (mask & -mask).bit_length() - 1
        out |= 1 << permutation[bit]
        mask &= mask - 1
    return out


def main() -> dict:
    common = load_common()
    geometry = common.build_geometry()
    compression = json.loads(COMPRESSION.read_text())
    fibers = [tuple(block) for block in compression["canonical_six_line_pack"]]
    residual = tuple(compression["residual_vertices"])
    fiber_sets = {frozenset(block) for block in fibers}
    residual_set = set(residual)

    generators = [tuple(action[4]) for action in geometry["acts"]]
    generators.append(tuple(geometry["outer"][4]))
    identity = tuple(range(45))
    group = {identity}
    queue = collections.deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            nxt = compose(generator, current)
            if nxt not in group:
                group.add(nxt)
                queue.append(nxt)
    assert len(group) == 51_840

    stabilizer = [
        permutation
        for permutation in group
        if {frozenset(permutation[v] for v in block) for block in fibers} == fiber_sets
    ]
    assert len(stabilizer) == 720
    assert all({permutation[v] for v in residual} == residual_set for permutation in stabilizer)

    residual_index = {vertex: i for i, vertex in enumerate(residual)}
    residual_permutations = {
        tuple(residual_index[permutation[vertex]] for vertex in residual)
        for permutation in stabilizer
    }
    assert len(residual_permutations) == 720

    unseen = set(range(1 << 15))
    orbits: list[tuple[int, int]] = []
    while unseen:
        representative = min(unseen)
        orbit = {transport(representative, permutation) for permutation in residual_permutations}
        unseen.difference_update(orbit)
        orbits.append((representative, len(orbit)))
    assert len(orbits) == 156
    assert sum(size for _, size in orbits) == 1 << 15

    ordered_rows = [vertex for block in fibers for vertex in block] + list(residual)
    assert len(ordered_rows) == 45
    row_lines = []
    for row in ordered_rows:
        mask = 0
        for edge in np.flatnonzero(geometry["K"][row]):
            mask |= 1 << int(edge)
        limbs = [(mask >> (64 * index)) & ((1 << 64) - 1) for index in range(4)]
        row_lines.append(" ".join(f"{limb:016x}" for limb in limbs))

    ROWS.write_text("\n".join(row_lines) + "\n")
    ORBITS.write_text("\n".join(f"{rep} {size}" for rep, size in orbits) + "\n")
    result = {
        "schema": "w33.pass1876.exact_dual_inputs.v1",
        "status": "PASS",
        "full_group_order": len(group),
        "six_line_pack_stabilizer_order": len(stabilizer),
        "residual_action_order": len(residual_permutations),
        "residual_orbit_count": len(orbits),
        "residual_assignment_total": sum(size for _, size in orbits),
        "fiber_rows": 30,
        "residual_rows": 15,
        "row_count": len(row_lines),
        "row_file": str(ROWS.relative_to(ROOT)),
        "orbit_file": str(ORBITS.relative_to(ROOT)),
        "boundary": "These are deterministic enumeration inputs; the exhaustive histogram is certified separately.",
    }
    SUMMARY.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    main()
