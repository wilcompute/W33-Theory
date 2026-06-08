#!/usr/bin/env python3
"""
BT544: Witting-Reye-Toroidal Tomotope Collapse Theorem.

This is the next bridge requested across four repo themes:

  * Tomotope: 192 flags, f-vector (4,12,16,8), 7 toroidal Csaszar/Szilassi axes.
  * Toroidal polyhedra: Csaszar/Szilassi share the K7 edge carrier, C(7,2)=21.
  * Witting polytope: 40 rays in CP^3, tight-frame constant 40/4=10.
  * Reye configuration: (12_4,16_3), 48 incidences, local Witting neighborhoods.

Main new observation:

  The Levi graph of a concrete Reye (12_4,16_3) model has cycle rank

      beta_1 = 48 - (12+16) + 1 = 21 = C(7,2),

  exactly the toroidal K7 edge carrier of the Csaszar/Szilassi pair.

  Then the 40 local Reye neighborhoods of the Witting configuration give

      40 * 48 = 1920 = 10 * 192,

  so the Witting local-Reye stack collapses to exactly ten tomotope flag packets.
  The factor 10 is the Witting tight-frame constant 40/4.

  Under the tomotope split 192 = 24 + 168, the ten-packet lift gives

      10*24  = 240,
      10*168 = 1680 = 7*240 = 2*840,

  where 840 = 40*21 is the total Reye cycle-rank stack.  Thus the cycle-rank
  stack is one Csaszar/Szilassi half of the ten-frame toroidal shell, while each
  toroidal dual axis carries a full 240-object Witting/E8/W33 root shell across
  the ten-frame collapse.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx


# W33 / substrate constants.
Q = 3
MU = 4
K = 12
ANTI = 16
V_W33 = 40
PHI6 = 7
G1 = 21
E8_ROOTS = 240
WITTING_RAYS = 40
WITTING_DIM = 4
WITTING_FRAME_CONSTANT = WITTING_RAYS // WITTING_DIM

# Tomotope / codec constants from the antipodal Q4 quotient theorem.
TOMOTOPE_F_VECTOR = (4, 12, 16, 8)
TOMOTOPE_FLAGS = 192
TETRA_AXIS_FLAGS = 24
TOROIDAL_AXIS_COUNT = 7
TOROIDAL_AXIS_FLAGS_PER_TOMOTOPE = 24  # two endpoints times 12 local flags
TOROIDAL_FLAGS_PER_TOMOTOPE = TOROIDAL_AXIS_COUNT * TOROIDAL_AXIS_FLAGS_PER_TOMOTOPE
LOCAL_CODEC_FLAGS = 12

# A concrete Latin/cyclic Reye model with 4 triads of 3 points.
# Points are (triad, phase) in {0,1,2,3} x F3.
# Lines are:
#   4 intra-triad lines, plus
#   12 cross-triad Latin lines, indexed by an omitted triad m and phase t.
# The offsets below were found by exact search and then frozen.  They make the
# incidence structure linear: no pair of points lies on more than one line.
OFFSETS = {
    (0, 1): 2, (0, 2): 1, (0, 3): 0,
    (1, 0): 2, (1, 2): 1, (1, 3): 1,
    (2, 0): 1, (2, 1): 1, (2, 3): 1,
    (3, 0): 2, (3, 1): 0, (3, 2): 0,
}


def reye_points() -> list[tuple[int, int]]:
    return [(a, b) for a in range(MU) for b in range(Q)]


def reye_lines() -> list[dict]:
    lines: list[dict] = []

    # Four intra-triad lines.
    for a in range(MU):
        lines.append({
            "kind": "intra_triad",
            "label": f"I{a}",
            "points": frozenset((a, b) for b in range(Q)),
        })

    # Twelve cross-triad lines: omit one triad and choose one phase.
    for omitted in range(MU):
        for t in range(Q):
            pts = frozenset(
                (a, (t + OFFSETS[(omitted, a)]) % Q)
                for a in range(MU)
                if a != omitted
            )
            lines.append({
                "kind": "cross_triad",
                "label": f"C{omitted}_{t}",
                "omitted_triad": omitted,
                "phase": t,
                "points": pts,
            })
    return lines


def build_reye_levi_graph() -> nx.Graph:
    g = nx.Graph()
    for p in reye_points():
        g.add_node(("P",) + p, bipartite="point")
    for i, line in enumerate(reye_lines()):
        node = ("L", i)
        g.add_node(node, bipartite="line", kind=line["kind"], label=line["label"])
        for p in line["points"]:
            g.add_edge(("P",) + p, node)
    return g


def pair_linearity_profile(lines: list[dict]) -> Counter:
    pair_counts: Counter = Counter()
    for line in lines:
        for a, b in itertools.combinations(sorted(line["points"]), 2):
            pair_counts[(a, b)] += 1
    return Counter(pair_counts.values())


def main() -> dict:
    lines = reye_lines()
    graph = build_reye_levi_graph()
    point_nodes = [n for n, data in graph.nodes(data=True) if data.get("bipartite") == "point"]
    line_nodes = [n for n, data in graph.nodes(data=True) if data.get("bipartite") == "line"]

    reye_point_count = len(point_nodes)
    reye_line_count = len(line_nodes)
    reye_incidences = graph.number_of_edges()
    reye_cycle_rank = graph.number_of_edges() - graph.number_of_nodes() + nx.number_connected_components(graph)

    line_kind_counts = Counter(line["kind"] for line in lines)
    point_degree_counts = Counter(dict(graph.degree(point_nodes)).values())
    line_degree_counts = Counter(dict(graph.degree(line_nodes)).values())
    pair_profile = pair_linearity_profile(lines)

    # Exact Reye checks.
    assert reye_point_count == K == 12
    assert reye_line_count == ANTI == 16
    assert reye_incidences == K * MU == ANTI * Q == 48
    assert point_degree_counts == Counter({MU: K})
    assert line_degree_counts == Counter({Q: ANTI})
    assert line_kind_counts == Counter({"cross_triad": K, "intra_triad": MU})
    assert pair_profile == Counter({1: ANTI * 3})  # each of the 16 lines has C(3,2)=3 unique pairs
    assert nx.is_connected(graph)
    assert reye_cycle_rank == G1 == 21

    # Tomotope/Witting/Reye collapse checks.
    assert TOMOTOPE_FLAGS == MU * reye_incidences == 192
    assert WITTING_FRAME_CONSTANT == 10
    witting_local_reye_incidences = WITTING_RAYS * reye_incidences
    assert witting_local_reye_incidences == WITTING_FRAME_CONSTANT * TOMOTOPE_FLAGS == 1920

    # Tomotope split from the antipodal codec quotient.
    assert TETRA_AXIS_FLAGS + TOROIDAL_FLAGS_PER_TOMOTOPE == TOMOTOPE_FLAGS
    assert TETRA_AXIS_FLAGS == 2 * LOCAL_CODEC_FLAGS
    assert TOROIDAL_FLAGS_PER_TOMOTOPE == TOROIDAL_AXIS_COUNT * 2 * LOCAL_CODEC_FLAGS == 168

    ten_tetra_flags = WITTING_FRAME_CONSTANT * TETRA_AXIS_FLAGS
    ten_toroidal_flags = WITTING_FRAME_CONSTANT * TOROIDAL_FLAGS_PER_TOMOTOPE
    assert ten_tetra_flags == E8_ROOTS
    assert ten_toroidal_flags == PHI6 * E8_ROOTS == 1680

    witting_local_reye_cycle_rank_stack = WITTING_RAYS * reye_cycle_rank
    assert witting_local_reye_cycle_rank_stack == 840
    assert ten_toroidal_flags == 2 * witting_local_reye_cycle_rank_stack

    per_axis_across_ten = WITTING_FRAME_CONSTANT * TOROIDAL_AXIS_FLAGS_PER_TOMOTOPE
    assert per_axis_across_ten == E8_ROOTS

    per_endpoint_across_ten = WITTING_FRAME_CONSTANT * LOCAL_CODEC_FLAGS
    cs_endpoint_total = PHI6 * per_endpoint_across_ten
    sz_endpoint_total = PHI6 * per_endpoint_across_ten
    assert per_endpoint_across_ten == 120
    assert cs_endpoint_total == sz_endpoint_total == witting_local_reye_cycle_rank_stack
    assert cs_endpoint_total + sz_endpoint_total == ten_toroidal_flags

    checks = {
        "reye_points_12": reye_point_count == 12,
        "reye_lines_16": reye_line_count == 16,
        "reye_incidences_48": reye_incidences == 48,
        "reye_degrees_12_4_16_3": point_degree_counts == Counter({4: 12}) and line_degree_counts == Counter({3: 16}),
        "reye_line_split_4_plus_12": line_kind_counts == Counter({"intra_triad": 4, "cross_triad": 12}),
        "reye_pair_linearity": pair_profile == Counter({1: 48}),
        "reye_levi_connected": nx.is_connected(graph),
        "reye_cycle_rank_is_K7_edges": reye_cycle_rank == 21,
        "tomotope_flags_are_four_reye_incidence_packets": TOMOTOPE_FLAGS == 4 * reye_incidences,
        "witting_local_reye_stack_is_ten_tomotopes": witting_local_reye_incidences == 10 * TOMOTOPE_FLAGS,
        "ten_tetra_axis_slices_are_E8_roots": ten_tetra_flags == E8_ROOTS,
        "ten_toroidal_slices_are_seven_E8_shells": ten_toroidal_flags == 7 * E8_ROOTS,
        "one_toroidal_axis_across_ten_is_one_E8_shell": per_axis_across_ten == E8_ROOTS,
        "cs_half_equals_reye_cycle_stack": cs_endpoint_total == witting_local_reye_cycle_rank_stack,
        "sz_half_equals_reye_cycle_stack": sz_endpoint_total == witting_local_reye_cycle_rank_stack,
    }

    results = {
        "theorem": "BT544 Witting-Reye-Toroidal Tomotope Collapse Theorem",
        "reye_model": {
            "points": reye_point_count,
            "lines": reye_line_count,
            "incidences": reye_incidences,
            "point_degree_profile": dict(point_degree_counts),
            "line_degree_profile": dict(line_degree_counts),
            "line_kind_profile": dict(line_kind_counts),
            "pair_linearity_profile": dict(pair_profile),
            "levi_graph_nodes": graph.number_of_nodes(),
            "levi_graph_edges": graph.number_of_edges(),
            "levi_graph_connected": nx.is_connected(graph),
            "levi_graph_cycle_rank": reye_cycle_rank,
            "cycle_rank_reading": "21 = C(7,2), the K7 edge carrier shared by the Csaszar/Szilassi toroidal pair",
        },
        "collapse_law": {
            "one_reye_incidence_packet": reye_incidences,
            "tomotope_flags": TOMOTOPE_FLAGS,
            "tomotope_as_reye_packets": "192 = 4 * 48",
            "witting_local_reye_stack": witting_local_reye_incidences,
            "witting_frame_constant": WITTING_FRAME_CONSTANT,
            "witting_stack_as_tomotope_packets": "40 * 48 = 10 * 192",
        },
        "tomotope_flag_split": {
            "one_packet_total": TOMOTOPE_FLAGS,
            "tetrahedral_axis_flags": TETRA_AXIS_FLAGS,
            "toroidal_axis_flags_total": TOROIDAL_FLAGS_PER_TOMOTOPE,
            "one_toroidal_axis_flags": TOROIDAL_AXIS_FLAGS_PER_TOMOTOPE,
            "formula": "192 = 24 + 168 = 24 + 7*(2*12)",
        },
        "ten_frame_lift": {
            "ten_tetrahedral_flags": ten_tetra_flags,
            "ten_tetrahedral_reading": "240 = E8 roots = Witting vertices = W33 edges",
            "ten_toroidal_flags": ten_toroidal_flags,
            "ten_toroidal_reading": "1680 = 7 * 240, one full 240-shell per toroidal Csaszar/Szilassi axis",
            "per_toroidal_axis_across_ten": per_axis_across_ten,
            "per_endpoint_across_ten": per_endpoint_across_ten,
            "cs_endpoint_total": cs_endpoint_total,
            "sz_endpoint_total": sz_endpoint_total,
            "reye_cycle_rank_stack": witting_local_reye_cycle_rank_stack,
            "half_shell_reading": "40 local Reye Levi cycle ranks give 840, exactly the Cs half and exactly the Sz half of the ten-frame toroidal shell",
        },
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT544_WITTING_REYE_TOROIDAL_TOMOTOPE_COLLAPSE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    return results


if __name__ == "__main__":
    main()
