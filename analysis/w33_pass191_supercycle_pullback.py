#!/usr/bin/env python3
"""Pass 191: the 27+6+3 obstruction and native completion fibre.

The S3 completion controller runs on 4320 ordered paths.  The chiral
program produced two canonical PSp(4,3)-sets whose product has exactly
that size: the 120 octahedron AXES (Pass 169: the second-shell supports,
three per line) and the 36 DOUBLE-SIXES (Pass 188: the dodecad
components of the pentad shell).  Exhaustive computation refutes the
initial transitive-product conjecture and replaces it with a sharper theorem:

1. THE OBSTRUCTION.  The 4320 = 120 x 36 pairs split into three orbits
   of sizes 3240, 720, 360, equivalently subdegrees 27+6+3 over an axis.
   Thus this product is not the controller's transitive path carrier.

2. THE NATIVE COMPLETION FIBRE.  The axis stabilizer has order 216 and
   acts on the distinguished three double-sixes through full S3, with
   kernel 36.  This is a genuine degree-three S3/C2 fibre over each axis.

3. THE CONTROLLER BOUNDARY.  The native three-set has the controller's
   abstract completion type, but it lives over 120 axes.  The full
   4320-product has the right cardinality and the wrong orbit structure;
   no controller-carrier identification is claimed.
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    orbit_count,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass161_gq42_ihara_inheritance import (
    small_generating_set,
    support_graph,
)
from analysis.w33_pass168_second_shell_scheme import gq42_lines

OUT = ROOT / "data" / "w33_pass191_supercycle_pullback.json"
BRIDGE = ROOT / "data" / "w33_s3_completion_probe_bridge.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)

    # ---- the 120 axes (second-shell supports of the address tower) ----
    octads, graph45 = support_graph(adjacency)
    octad_index = {s: n for n, s in enumerate(octads)}
    lines45 = gq42_lines(graph45)
    incidence45 = np.zeros((27, 45), dtype=np.int64)
    for row, line in enumerate(lines45):
        for p in line:
            incidence45[row, p] = 1
    trade45 = generic_saturated_kernel(incidence45)
    _, shell240 = staged_minimal_shell(trade45)
    shell240 = [np.asarray(v, dtype=np.int64) for v in shell240]
    axes = sorted(
        {frozenset(np.flatnonzero(v).tolist()) for v in shell240},
        key=sorted,
    )
    checks["axes_120"] = len(axes) == 120
    axis_index = {a: n for n, a in enumerate(axes)}

    # ---- the 36 double-sixes (dodecad components of the route shell) ----
    incidence40 = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence40[row, p] = 1
    route = generic_saturated_kernel(incidence40.T)
    _, shell432 = staged_minimal_shell(route, bounds=(4, 6, 8, 10))
    shell432 = [np.asarray(v, dtype=np.int64) for v in shell432]
    line_index = {line: n for n, line in enumerate(lines)}

    def line_perm(perm):
        return [
            line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)
        ]

    shell_keys432 = {
        tuple(int(x) for x in v): n for n, v in enumerate(shell432)
    }
    gen_maps432 = []
    for g in two_gens:
        lp = line_perm(g)
        table = []
        for v in shell432:
            image = np.empty(40, dtype=np.int64)
            for src in range(40):
                image[lp[src]] = v[src]
            table.append(shell_keys432[tuple(int(x) for x in image)])
        gen_maps432.append(table)
    tables432 = []
    for mapping in gen_maps432:
        arr = np.asarray(mapping, dtype=np.int64)
        tables432.append((arr[:, None] * 432 + arr[None, :]).reshape(-1))
    labels = np.full(432 * 432, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(432 * 432):
        if labels[start] >= 0:
            continue
        labels[start] = orbital_count
        stack = [start]
        while stack:
            current = stack.pop()
            for table in tables432:
                image = int(table[current])
                if labels[image] < 0:
                    labels[image] = orbital_count
                    stack.append(image)
        orbital_count += 1
    label_grid = labels.reshape(432, 432)
    # Pass 188's crown is the unique union of the two transpose directed
    # valency-five orbitals.  Require that characterization here instead of
    # taking the first candidate.
    directed_five = []
    for o in range(orbital_count):
        matrix = (label_grid == o).astype(np.int64)
        row_index = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        if int(matrix[row_index].sum()) == 5 and not bool(
            np.array_equal(matrix, matrix.T)
        ):
            directed_five.append((o, matrix))
    checks["unique_transpose_crown_pair"] = (
        len(directed_five) == 2
        and np.array_equal(directed_five[0][1].T, directed_five[1][1])
    )
    target = directed_five[0][1] + directed_five[1][1]

    seen = np.zeros(432, dtype=bool)
    dodecads = []
    for start in range(432):
        if seen[start]:
            continue
        component = {start}
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for nxt in np.flatnonzero(target[current]):
                if not seen[nxt]:
                    seen[nxt] = True
                    component.add(int(nxt))
                    stack.append(int(nxt))
        if len(component) > 1:
            dodecads.append(frozenset(component))
    checks["thirty_six_double_sixes"] = len(dodecads) == 36 and all(
        len(d) == 12 for d in dodecads
    )
    dodecads = sorted(dodecads, key=sorted)
    dodecad_index = {d: n for n, d in enumerate(dodecads)}

    # ---- actions ----
    def axis_map(perm):
        return [
            axis_index[
                frozenset(
                    octad_index[frozenset(perm[x] for x in octads[o])]
                    for o in axes[a]
                )
            ]
            for a in range(120)
        ]

    def dodecad_map(perm):
        lp = line_perm(perm)
        table432 = {}
        out = []
        for d in dodecads:
            image = set()
            for i in d:
                img = np.empty(40, dtype=np.int64)
                for src in range(40):
                    img[lp[src]] = shell432[i][src]
                image.add(shell_keys432[tuple(int(x) for x in img)])
            out.append(dodecad_index[frozenset(image)])
        return out

    axis_maps = [axis_map(g) for g in two_gens]
    dodecad_maps = [dodecad_map(g) for g in two_gens]
    checks["axes_transitive"] = orbit_count(120, axis_maps) == 1
    checks["double_sixes_transitive"] = orbit_count(36, dodecad_maps) == 1

    # ---- the native product action on 4320 pairs ----
    product_tables = []
    for am, dm in zip(axis_maps, dodecad_maps):
        a = np.asarray(am, dtype=np.int64)
        d = np.asarray(dm, dtype=np.int64)
        product_tables.append((a[:, None] * 36 + d[None, :]).reshape(-1))
    unseen = set(range(4320))
    product_orbits = []
    while unseen:
        start = min(unseen)
        orbit = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            current = stack.pop()
            for table in product_tables:
                image = int(table[current])
                if image not in orbit:
                    orbit.add(image)
                    unseen.remove(image)
                    stack.append(image)
        product_orbits.append(frozenset(orbit))
    product_orbits.sort(key=len)
    product_orbit_sizes = [len(orbit) for orbit in product_orbits]
    checks["product_orbits_are_360_720_3240"] = product_orbit_sizes == [360, 720, 3240]

    suborbits_over_axis0 = [
        frozenset(pair % 36 for pair in orbit if pair // 36 == 0)
        for orbit in product_orbits
    ]
    subdegrees = [len(suborbit) for suborbit in suborbits_over_axis0]
    checks["double_six_subdegrees_over_axis_are_3_6_27"] = subdegrees == [3, 6, 27]

    # Stabilizer of one axis and its induced action on the distinguished
    # three-double-six suborbit.
    base_axis = axes[0]
    axis_stabilizer_dmaps = []
    for perm in group:
        image_axis = frozenset(
            octad_index[frozenset(perm[x] for x in octads[o])]
            for o in base_axis
        )
        if image_axis != base_axis:
            continue
        axis_stabilizer_dmaps.append(dodecad_map(perm))
    checks["axis_stabilizer_order_216"] = len(axis_stabilizer_dmaps) == 216

    special = sorted(suborbits_over_axis0[0])
    special_index = {double_six: i for i, double_six in enumerate(special)}
    special_images = []
    special_preserved = True
    for dodecad_action in axis_stabilizer_dmaps:
        image = tuple(special_index.get(dodecad_action[d], -1) for d in special)
        if -1 in image:
            special_preserved = False
        special_images.append(image)
    special_image_set = set(special_images)
    identity3 = tuple(range(3))
    checks["special_three_action_is_full_S3"] = (
        special_preserved
        and special_image_set == set(permutations(range(3)))
    )
    checks["special_three_action_kernel_36"] = (
        special_images.count(identity3) == 36
    )
    pair_stabilizer_orders = [25920 // size for size in product_orbit_sizes]
    checks["pair_stabilizer_orders_are_72_36_8"] = pair_stabilizer_orders == [72, 36, 8]

    # Exact arithmetic alignment with the committed controller certificate.
    bridge_alignment = {}
    if BRIDGE.exists():
        bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
        frontier = bridge.get("frontier_completion_surface", {})
        control = bridge.get("probe_control_surface", {})
        bridge_alignment = {
            "verified": bridge.get("verified"),
            "ordered_paths": frontier.get("ordered_nonlocal_paths"),
            "completions_per_path": frontier.get("completions_per_path"),
            "completion_incidences": frontier.get("completion_incidences"),
            "seed_action_size": frontier.get("seed_completion_action_size"),
            "runtime_slots": control.get("supercycle_runtime_slots"),
        }
    checks["controller_arithmetic_exact"] = bridge_alignment == {
        "verified": True,
        "ordered_paths": 4320,
        "completions_per_path": 3,
        "completion_incidences": 12960,
        "seed_action_size": 6,
        "runtime_slots": 51840,
    }

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass191.double_six_subdegrees.v3",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": {
            "carrier": "axes x double-sixes, 120 x 36 = 4320",
            "product_orbit_sizes": product_orbit_sizes,
            "double_six_subdegrees_over_an_axis": subdegrees,
            "pair_stabilizer_orders": pair_stabilizer_orders,
            "native_completion_fibre": (
                "the distinguished 3-suborbit is S3/C2; the axis "
                "stabilizer 216 acts through full S3 with kernel 36"
            ),
            "reading": (
                "the 4320-element product has the controller's cardinality "
                "but not a transitive orbit structure: it splits as "
                "120*(3+6+27).  The three special double-sixes over each "
                "axis do provide a native degree-three S3 fibre, but over "
                "120 axes rather than over 4320 ordered paths"
            ),
        },
        "controller_alignment": bridge_alignment,
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
