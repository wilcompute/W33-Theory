#!/usr/bin/env python3
"""Pass 192: signed second-shell trades are W33 edges with an S4 lift.

Passes 182/185 identified the 120 unsigned second-shell supports with the
three axes on each of the 40 W33 lines.  This witness restores the signs:

1. SIGNED EDGE CODEC.  A signed trade has three positive and three negative
   binary-polar octads.  On its matched four-point line, the positive octads
   contain one unique two-point edge and the negative octads contain its
   complement.  This gives a PSp(4,3)-equivariant bijection

       240 signed trades  <->  40 lines x 6 edges.

2. THE S4 LIFT.  A line stabilizer H of order 648 acts on its six signed
   trades exactly as S4 acts on the six 2-subsets of a four-set.  The kernel
   has order 27, is abelian, and every nonidentity element has order three,
   proving the exact sequence 1 -> C3^3 -> H -> S4 -> 1.

3. AXIS QUOTIENT.  Pairing complementary edges gives the three axes.  The
   induced S4 -> S3 action agrees elementwise with the support action; its
   kernel in H has order 108.  Thus the three axes are S3/C2, while the six
   signed trades are S4/V4.  Neither six-set is a regular S3 torsor.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import json
import math
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

OUT = ROOT / "data" / "w33_pass192_signed_trade_edge_s4.json"
BRIDGE = ROOT / "data" / "w33_s3_completion_probe_bridge.json"


def permutation_order(perm):
    identity = tuple(range(len(perm)))
    current = tuple(perm)
    order = 1
    while current != identity:
        current = tuple(perm[current[i]] for i in range(len(perm)))
        order += 1
    return order


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    line_index = {line: i for i, line in enumerate(lines)}
    checks = {}

    octads, graph45 = support_graph(adjacency)
    octad_index = {octad: i for i, octad in enumerate(octads)}
    lines45 = gq42_lines(graph45)
    incidence45 = np.zeros((27, 45), dtype=np.int64)
    for row, line in enumerate(lines45):
        for point in line:
            incidence45[row, point] = 1
    trade = generic_saturated_kernel(incidence45)
    minimum, shell = staged_minimal_shell(trade)
    shell = [np.asarray(vector, dtype=np.int64) for vector in shell]
    checks["shell_240_norm_6"] = minimum == 6 and len(shell) == 240

    supports = [frozenset(np.flatnonzero(vector).tolist()) for vector in shell]
    supports120 = sorted(set(supports), key=sorted)
    support_index = {support: i for i, support in enumerate(supports120)}
    checks["unsigned_supports_120"] = len(supports120) == 120
    shell_keys = {
        tuple(int(value) for value in vector): i for i, vector in enumerate(shell)
    }

    generators, group = build_group(points, symplectic)
    two_gens = small_generating_set(group)
    checks["group_order_25920"] = len(group) == 25920

    def octad_map(perm):
        return [
            octad_index[frozenset(perm[point] for point in octad)]
            for octad in octads
        ]

    def shell_map_from_octads(mapping45):
        table = []
        for vector in shell:
            image = np.empty(45, dtype=np.int64)
            for source in range(45):
                image[mapping45[source]] = vector[source]
            table.append(shell_keys[tuple(int(value) for value in image)])
        return table

    generator_octad_maps = [octad_map(generator) for generator in two_gens]
    generator_shell_maps = [
        shell_map_from_octads(mapping) for mapping in generator_octad_maps
    ]

    # Recover the true four-valent orbital and its 40 three-support components.
    shell_matrix = np.array(shell, dtype=np.int64)
    gram = shell_matrix @ shell_matrix.T
    pair_tables = []
    for mapping in generator_shell_maps:
        array = np.asarray(mapping, dtype=np.int64)
        pair_tables.append((array[:, None] * 240 + array[None, :]).reshape(-1))
    labels = np.full(240 * 240, -1, dtype=np.int64)
    orbital_count = 0
    for start in range(240 * 240):
        if labels[start] >= 0:
            continue
        labels[start] = orbital_count
        stack = [start]
        while stack:
            current = stack.pop()
            for table in pair_tables:
                image = int(table[current])
                if labels[image] < 0:
                    labels[image] = orbital_count
                    stack.append(image)
        orbital_count += 1
    label_grid = labels.reshape(240, 240)
    four_matrix = None
    for orbital in range(orbital_count):
        matrix = (label_grid == orbital).astype(np.int64)
        row = int(np.flatnonzero(matrix.sum(axis=1) > 0)[0])
        column = int(np.flatnonzero(matrix[row])[0])
        if int(matrix[row].sum()) == 4 and int(gram[row, column]) == 0:
            four_matrix = matrix
    checks["true_four_valent_orbital_found"] = four_matrix is not None

    support_adjacency = [set() for _ in range(120)]
    for i in range(240):
        for j in np.flatnonzero(four_matrix[i]):
            a, b = support_index[supports[i]], support_index[supports[int(j)]]
            if a != b:
                support_adjacency[a].add(b)
                support_adjacency[b].add(a)
    seen = set()
    triangles = []
    for start in range(120):
        if start in seen:
            continue
        component = {start}
        stack = [start]
        seen.add(start)
        while stack:
            current = stack.pop()
            for image in support_adjacency[current]:
                if image not in seen:
                    seen.add(image)
                    component.add(image)
                    stack.append(image)
        triangles.append(tuple(sorted(component)))
    checks["forty_three_axis_components"] = (
        len(triangles) == 40 and all(len(triangle) == 3 for triangle in triangles)
    )

    # The constant-section profile assigns one W33 line to each component.
    matched_line = {}
    for triangle in triangles:
        candidates = []
        for line_id, line in enumerate(lines):
            if all(
                len(octads[octad] & line) == 2
                for support_id in triangle
                for octad in supports120[support_id]
            ):
                candidates.append(line_id)
        if len(candidates) == 1:
            matched_line[triangle] = candidates[0]
    checks["constant_section_bijection"] = (
        len(matched_line) == 40 and len(set(matched_line.values())) == 40
    )
    support_to_line = {
        support_id: matched_line[triangle]
        for triangle in triangles
        for support_id in triangle
    }

    def pairs_of_line(line):
        return sorted(
            (frozenset(pair) for pair in combinations(sorted(line), 2)),
            key=lambda pair: tuple(sorted(pair)),
        )

    def signed_pair_label(shell_id, line):
        vector = shell[shell_id]
        positive = [octad for octad in supports[shell_id] if vector[octad] == 1]
        negative = [octad for octad in supports[shell_id] if vector[octad] == -1]
        if len(positive) != 3 or len(negative) != 3:
            return None
        positive_pairs = [
            pair
            for pair in pairs_of_line(line)
            if all(pair <= octads[octad] for octad in positive)
        ]
        negative_pairs = [
            pair
            for pair in pairs_of_line(line)
            if all(pair <= octads[octad] for octad in negative)
        ]
        if len(positive_pairs) != 1 or len(negative_pairs) != 1:
            return None
        positive_pair, negative_pair = positive_pairs[0], negative_pairs[0]
        if positive_pair & negative_pair or positive_pair | negative_pair != line:
            return None
        return positive_pair

    signed_lines = [support_to_line[support_index[support]] for support in supports]
    edge_labels = [
        signed_pair_label(shell_id, lines[signed_lines[shell_id]])
        for shell_id in range(240)
    ]
    checks["all_signed_trade_edge_labels_total"] = all(
        label is not None for label in edge_labels
    )
    codec_bijective = True
    for line_id, line in enumerate(lines):
        local = [
            edge_labels[shell_id]
            for shell_id in range(240)
            if signed_lines[shell_id] == line_id
        ]
        if Counter(local) != Counter({pair: 1 for pair in pairs_of_line(line)}):
            codec_bijective = False
    checks["signed_codec_is_40_times_six_bijection"] = codec_bijective

    negation_cases = 0
    negation_ok = True
    for shell_id, vector in enumerate(shell):
        opposite = shell_keys[tuple(int(-value) for value in vector)]
        line = lines[signed_lines[shell_id]]
        negation_cases += 1
        if edge_labels[opposite] != line - edge_labels[shell_id]:
            negation_ok = False
    checks["sign_reversal_is_edge_complement_240_cases"] = (
        negation_ok and negation_cases == 240
    )

    equivariance_cases = 0
    equivariance_ok = True
    for generator, shell_mapping in zip(two_gens, generator_shell_maps):
        for shell_id in range(240):
            image_id = shell_mapping[shell_id]
            transported = frozenset(generator[point] for point in edge_labels[shell_id])
            equivariance_cases += 1
            if edge_labels[image_id] != transported:
                equivariance_ok = False
    checks["signed_edge_codec_equivariant_480_cases"] = (
        equivariance_ok and equivariance_cases == 480
    )

    # Full line-stabilizer action on one six-set.
    triangle0 = next(triangle for triangle, line_id in matched_line.items() if line_id == 0)
    line0 = lines[0]
    local_pairs = pairs_of_line(line0)
    local_pair_index = {pair: i for i, pair in enumerate(local_pairs)}
    local_shell_by_pair = {}
    for shell_id in range(240):
        if support_index[supports[shell_id]] in triangle0:
            local_shell_by_pair[edge_labels[shell_id]] = shell_id
    local_shell = [local_shell_by_pair[pair] for pair in local_pairs]
    checks["local_six_labels_all_edges"] = len(local_shell_by_pair) == 6

    line_points = sorted(line0)
    point_position = {point: i for i, point in enumerate(line_points)}
    line_stabilizer = [
        perm
        for perm in group
        if frozenset(perm[point] for point in line0) == line0
    ]
    checks["line_stabilizer_order_648"] = len(line_stabilizer) == 648

    image4_set = set()
    image6_set = set()
    image3_set = set()
    kernel4 = []
    kernel3_count = 0
    action_compatibility = True
    axis_order = sorted(triangle0)
    axis_position = {axis: i for i, axis in enumerate(axis_order)}
    pair_to_axis = {
        edge_labels[shell_id]: support_index[supports[shell_id]]
        for shell_id in local_shell
    }
    representative_pair = {
        axis: next(pair for pair, owner in pair_to_axis.items() if owner == axis)
        for axis in axis_order
    }
    identity4 = tuple(range(4))
    identity3 = tuple(range(3))

    for perm in line_stabilizer:
        mapping45 = octad_map(perm)
        rho4 = tuple(point_position[perm[point]] for point in line_points)
        image4_set.add(rho4)
        if rho4 == identity4:
            kernel4.append(tuple(perm))

        rho6 = []
        for shell_id in local_shell:
            vector = shell[shell_id]
            image = np.empty(45, dtype=np.int64)
            for source in range(45):
                image[mapping45[source]] = vector[source]
            image_id = shell_keys[tuple(int(value) for value in image)]
            rho6.append(local_shell.index(image_id))
        rho6 = tuple(rho6)
        image6_set.add(rho6)
        induced6 = tuple(
            local_pair_index[frozenset(perm[point] for point in pair)]
            for pair in local_pairs
        )
        if rho6 != induced6:
            action_compatibility = False

        support_action = []
        for axis in axis_order:
            image_support = frozenset(mapping45[octad] for octad in supports120[axis])
            support_action.append(axis_position[support_index[image_support]])
        support_action = tuple(support_action)
        image3_set.add(support_action)
        if support_action == identity3:
            kernel3_count += 1
        induced3 = tuple(
            axis_position[
                pair_to_axis[
                    frozenset(perm[point] for point in representative_pair[axis])
                ]
            ]
            for axis in axis_order
        )
        if support_action != induced3:
            action_compatibility = False

    checks["signed_action_equals_S4_on_two_subsets_648_cases"] = (
        action_compatibility
        and image4_set == set(permutations(range(4)))
        and len(image6_set) == 24
    )
    checks["axis_quotient_is_full_S3_with_kernel_108"] = (
        image3_set == set(permutations(range(3))) and kernel3_count == 108
    )

    identity40 = tuple(range(40))
    kernel_is_c3_cubed = (
        len(kernel4) == 27
        and all(
            permutation_order(element) == 3
            for element in kernel4
            if element != identity40
        )
        and all(
            compose(left, right) == compose(right, left)
            for left in kernel4
            for right in kernel4
        )
    )
    checks["line_kernel_is_elementary_abelian_C3_cubed"] = kernel_is_c3_cubed
    image_order_profile = Counter(permutation_order(perm) for perm in image4_set)
    checks["S4_order_profile_exact"] = image_order_profile == Counter(
        {1: 1, 2: 9, 3: 8, 4: 6}
    )

    bridge_alignment = {}
    if BRIDGE.exists():
        bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
        frontier = bridge.get("frontier_completion_surface", {})
        bridge_alignment = {
            "verified": bridge.get("verified"),
            "completions_per_path": frontier.get("completions_per_path"),
            "seed_action_size": frontier.get("seed_completion_action_size"),
        }
    checks["controller_three_and_six_scales_loaded"] = bridge_alignment == {
        "verified": True,
        "completions_per_path": 3,
        "seed_action_size": 6,
    }

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass192.signed_trade_edge_s4.v1",
        "status": "PASS" if all_pass else "FAIL",
        "signed_edge_codec": {
            "signed_trades": 240,
            "lines_times_edges": "40*6=240",
            "sign_reversal": "edge complement inside the matched four-point line",
            "equivariance_cases": equivariance_cases,
        },
        "line_stabilizer_exact_sequence": {
            "sequence": "1 -> C3^3 -> H_line -> S4 -> 1",
            "orders": [27, 648, 24],
            "S4_order_profile": {
                str(order): count for order, count in sorted(image_order_profile.items())
            },
        },
        "actions": {
            "six_signed_trades": "S4/V4, the six edges of a tetrahedron",
            "three_unsigned_axes": "S3/C2, complementary edge-pairs",
            "axis_kernel_in_line_stabilizer": 108,
        },
        "controller_boundary": {
            **bridge_alignment,
            "reading": (
                "the unframed three-completion type agrees with the axis "
                "S3/C2 action.  The six signed trades instead carry S4 on "
                "tetrahedral edges, not the regular S3 action; equal counts "
                "do not identify the framed actions"
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
