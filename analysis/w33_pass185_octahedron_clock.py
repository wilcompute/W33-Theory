#!/usr/bin/env python3
"""Pass 185: the octahedron clock -- a native degree-three S3 fibre.

The S3 completion admission controller postulates a three-completion
fibre with seed action S3 (order 6) over each ordered path.  Pass 182
gave every LINE of W(3,3) a canonical octahedron whose three axes are the
three pair-partitions of the line.  This witness certifies the geometric
fibre and aligns it with the controller's arithmetic:

1. THE DEGREE-THREE SET.  The line stabilizer (order 648) acts on its
   three axes with FULL image S3 (surjective onto the pair-partition
   action).  The axes form the transitive S3-set S3/C2, not an S3 torsor:
   the action kernel has order 108 and an axis stabilizer has order 216.

2. THE INTRINSIC MAP.  The constant-section rule (Pass 182) supplies the
   line of each octahedron with no group input; the composite
   line -> octahedron -> axis-fibre is PSp(4,3)-equivariant by
   construction, verified on both stored generators for all 40 lines and
   all 120 axes.

3. THE CONTROLLER ALIGNMENT.  From the committed S3 bridge data:
   4320 ordered paths x 3 completions = 12960 incidences with seed
   completion action of order 6 = |S3| -- the same fibre shape the axis
   degree-three S3-set realizes geometrically (recorded alignment; no identification
   of the 4320-path carrier is claimed).
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
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

OUT = ROOT / "data" / "w33_pass185_octahedron_clock.json"
BRIDGE = ROOT / "data" / "w33_s3_completion_probe_bridge.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    octads, graph = support_graph(adjacency)
    lines45 = gq42_lines(graph)
    incidence45 = np.zeros((27, 45), dtype=np.int64)
    for row, line in enumerate(lines45):
        for p in line:
            incidence45[row, p] = 1
    trade = generic_saturated_kernel(incidence45)
    _, shell = staged_minimal_shell(trade)
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    checks["shell_240"] = len(shell) == 240

    sup_of = [frozenset(np.flatnonzero(v).tolist()) for v in shell]
    sup120 = sorted(set(sup_of), key=sorted)
    sup_index = {s: n for n, s in enumerate(sup120)}

    # the octahedra via the group orbital (as in Pass 169/182)
    generators, group = build_group(points, symplectic)
    checks["group_order"] = len(group) == 25920
    two_gens = small_generating_set(group)
    octad_index = {s: n for n, s in enumerate(octads)}
    shell_keys = {tuple(int(x) for x in v): n for n, v in enumerate(shell)}
    shell_matrix = np.array(shell, dtype=np.int64)
    gram = shell_matrix @ shell_matrix.T

    def shell_map(perm):
        mapping45 = [
            octad_index[frozenset(perm[x] for x in octads[s])] for s in range(45)
        ]
        table = []
        for v in shell:
            image = np.empty(45, dtype=np.int64)
            for src in range(45):
                image[mapping45[src]] = v[src]
            table.append(shell_keys[tuple(int(x) for x in image)])
        return table

    gen_maps = [shell_map(g) for g in two_gens]
    tables = []
    for mapping in gen_maps:
        arr = np.asarray(mapping, dtype=np.int64)
        tables.append((arr[:, None] * 240 + arr[None, :]).reshape(-1))
    labels = np.full(240 * 240, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(240 * 240):
        if labels[start] >= 0:
            continue
        labels[start] = orbital_count
        stack = [start]
        while stack:
            current = stack.pop()
            for table in tables:
                image = int(table[current])
                if labels[image] < 0:
                    labels[image] = orbital_count
                    stack.append(image)
        orbital_count += 1
    label_grid = labels.reshape(240, 240)
    four_matrix = None
    for o in range(orbital_count):
        matrix = (label_grid == o).astype(np.int64)
        row_index = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        col = int(np.flatnonzero(matrix[row_index])[0])
        if int(matrix[row_index].sum()) == 4 and int(gram[row_index, col]) == 0:
            four_matrix = matrix
    checks["four_valent_found"] = four_matrix is not None

    adj_true = [set() for _ in range(120)]
    for i in range(240):
        for j in np.flatnonzero(four_matrix[i]):
            a = sup_index[sup_of[i]]
            b = sup_index[sup_of[int(j)]]
            if a != b:
                adj_true[a].add(b)
                adj_true[b].add(a)
    seen = [False] * 120
    triangles = []
    for start in range(120):
        if seen[start]:
            continue
        component = {start}
        stack = [start]
        seen[start] = True
        while stack:
            current = stack.pop()
            for nxt in adj_true[current]:
                if not seen[nxt]:
                    seen[nxt] = True
                    component.add(nxt)
                    stack.append(nxt)
        triangles.append(tuple(sorted(component)))
    checks["forty_triangles"] = len(triangles) == 40

    # intrinsic line of each triangle: the constant-section rule
    def matched_line(tri):
        for ln, line in enumerate(lines):
            good = True
            for si in tri:
                for o in sup120[si]:
                    if len(octads[o] & line) != 2:
                        good = False
                        break
                if not good:
                    break
            if good:
                return ln
        return None

    matches = {tri: matched_line(tri) for tri in triangles}
    checks["constant_section_total"] = all(v is not None for v in matches.values())
    checks["constant_section_bijective"] = len(set(matches.values())) == 40

    # 1. the degree-three S3-set: one line stabilizer acting on its axes
    tri0 = next(tri for tri, ln in matches.items() if ln == 0)
    line0 = lines[0]
    stabilizer = [perm for perm in group if frozenset(perm[x] for x in line0) == line0]
    checks["line_stabilizer_648"] = len(stabilizer) == 648

    tri_supports = [sup120[i] for i in tri0]

    def support_image(perm, support):
        mapping = frozenset(
            octad_index[frozenset(perm[x] for x in octads[o])] for o in support
        )
        return mapping

    axis_perms = set()
    axis_perm_counts = Counter()
    for perm in stabilizer:
        images = [support_image(perm, s) for s in tri_supports]
        axis_perm = tuple(tri_supports.index(img) for img in images)
        axis_perms.add(axis_perm)
        axis_perm_counts[axis_perm] += 1
    identity_axis_perm = tuple(range(3))
    checks["axis_action_is_full_S3"] = axis_perms == set(permutations(range(3)))
    checks["axis_action_kernel_108"] = axis_perm_counts[identity_axis_perm] == 108
    checks["axis_stabilizer_216_with_image_C2"] = (
        sum(count for perm, count in axis_perm_counts.items() if perm[0] == 0) == 216
        and sum(1 for perm in axis_perms if perm[0] == 0) == 2
    )

    # Pair-partition equivariance on both generators and all 120 axes.
    def partition_of_axis(support, line):
        line_sorted = sorted(line)
        partitions = [
            frozenset([frozenset(line_sorted[:2]), frozenset(line_sorted[2:])]),
            frozenset(
                [
                    frozenset([line_sorted[0], line_sorted[2]]),
                    frozenset([line_sorted[1], line_sorted[3]]),
                ]
            ),
            frozenset(
                [
                    frozenset([line_sorted[0], line_sorted[3]]),
                    frozenset([line_sorted[1], line_sorted[2]]),
                ]
            ),
        ]
        matches_here = []
        for partition in partitions:
            pair1, pair2 = tuple(partition)
            count = sum(
                1
                for o in support
                if len(octads[o] & set(pair1)) == 2 or len(octads[o] & set(pair2)) == 2
            )
            if count == 6:
                matches_here.append(partition)
        return matches_here[0] if len(matches_here) == 1 else None

    axis_labels = {}
    all_lines_distinct = True
    for tri, line_id in matches.items():
        labels_here = [
            partition_of_axis(sup120[support], lines[line_id]) for support in tri
        ]
        if None in labels_here or len(set(labels_here)) != 3:
            all_lines_distinct = False
        for support, label in zip(tri, labels_here):
            axis_labels[sup120[support]] = label
    checks["all_40_lines_carry_three_distinct_partitions"] = (
        all_lines_distinct and len(axis_labels) == 120
    )

    line_index = {frozenset(line): i for i, line in enumerate(lines)}
    triangle_for_line = {line_id: tri for tri, line_id in matches.items()}
    dictionary_cases = 0
    axis_cases = 0
    equivariant = True
    for generator in two_gens:
        for tri, line_id in matches.items():
            image_line = frozenset(generator[x] for x in lines[line_id])
            image_line_id = line_index[image_line]
            image_tri = triangle_for_line[image_line_id]
            image_supports = {sup120[support] for support in image_tri}
            dictionary_cases += 1
            for support_id in tri:
                support = sup120[support_id]
                image_support = support_image(generator, support)
                axis_cases += 1
                if image_support not in image_supports:
                    equivariant = False
                    continue
                transported = frozenset(
                    frozenset(generator[x] for x in pair)
                    for pair in axis_labels[support]
                )
                if axis_labels[image_support] != transported:
                    equivariant = False
    checks["partition_labels_equivariant_240_cases"] = (
        equivariant and dictionary_cases == 80 and axis_cases == 240
    )

    # 2. controller alignment from committed data
    alignment = {}
    if BRIDGE.exists():
        bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
        chk = bridge.get("checks", {})
        frontier = bridge.get("frontier_completion_surface", {})
        control = bridge.get("probe_control_surface", {})
        alignment = {
            "bridge_verified": bridge.get("verified") is True,
            "bridge_checks_pass": bool(chk) and all(bool(v) for v in chk.values()),
            "ordered_paths": frontier.get("ordered_nonlocal_paths"),
            "completions_per_path": frontier.get("completions_per_path"),
            "completion_incidences": frontier.get("completion_incidences"),
            "seed_completion_action_size": frontier.get(
                "seed_completion_action_size"
            ),
            "runtime_slots": control.get("supercycle_runtime_slots"),
        }
        checks["controller_bridge_exact"] = alignment == {
            "bridge_verified": True,
            "bridge_checks_pass": True,
            "ordered_paths": 4320,
            "completions_per_path": 3,
            "completion_incidences": 12960,
            "seed_completion_action_size": 6,
            "runtime_slots": 51840,
        }
    else:
        checks["controller_bridge_exact"] = False

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass185.octahedron_clock.v2",
        "status": "PASS" if all_pass else "FAIL",
        "degree_three_s3_set": {
            "line_stabilizer_order": 648,
            "axis_action_image": "S3 (order 6, full)",
            "action_kernel_order": 108,
            "axis_stabilizer_order": 216,
            "image_axis_stabilizer": "C2 (order 2)",
            "homogeneous_space": "S3/C2, hence not an S3 torsor",
            "axis_labels": "the three pair-partitions of the line",
            "equivariant": bool(equivariant),
            "dictionary_generator_cases": dictionary_cases,
            "axis_generator_cases": axis_cases,
        },
        "alignment": {
            "geometric_fibre": "40 lines x 3 axes (x2 trades) = 240",
            "controller_fibre": "4320 ordered paths x 3 completions = 12960",
            "seed_action": "|S3| = 6 on both sides",
            **alignment,
            "honest_scope": (
                "the degree-three axis S3-set gives the controller's "
                "postulated three-completion fibre a native geometric model per "
                "line; the 4320-path carrier itself is not identified "
                "with an octahedron object here"
            ),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
