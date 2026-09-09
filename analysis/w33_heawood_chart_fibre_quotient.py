#!/usr/bin/env python3
"""Exact Heawood/Fano fibre quotient carried by each W33 Q3 chart.

The 540-chart web does NOT contain a literal Heawood subgraph (the companion
Marcelis atlas proves that).  The correct bridge is local and quotient-like.

Each W33 chart is Q3 = Cay(F2^3,{e1,e2,e3}).  Its translation group therefore
has seven nonidentity elements, whose triples {a,b,a+b} form a Fano plane.
The incidence graph of those seven translation points and seven Fano lines is
a Heawood graph: a natural 14-vertex fibre over the chart.

The cube has an intrinsic antipode translation c=(1,1,1).  An adjacent chart
shares four vertices with the original chart.  Those four vertices are an
affine 2-plane in F2^3; its three nonzero translation stabilizers form a Fano
line containing c.  The six chart-web neighbours collapse 2-to-1 onto the
three Fano lines through c.  The other four Fano lines are nonincident buffer
slots.  Thus the exact local law is

    6 web neighbours -> 3 Heawood execution edges (two sheets each)
                      + 4 nonincident Heawood buffer lines.

This realizes the earlier BT1714 3-execution/4-buffer scheduler as a genuine
local fibre/quotient of the W33 hypercube chart layer, without claiming direct
graph inclusion or a globally canonical Fano labelling across all charts.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_multichart_atlas import w33, chart_web, edge_count  # noqa: E402

OUT = ROOT / "data" / "w33_heawood_chart_fibre_quotient.json"


def fano_lines() -> tuple[tuple[int, int, int], ...]:
    lines = {
        tuple(sorted((a, b, a ^ b)))
        for a, b in combinations(range(1, 8), 2)
        if a != b
    }
    return tuple(sorted(lines))


def point_pair_collinearity(lines):
    pairs = set()
    for line in lines:
        for a, b in combinations(line, 2):
            pairs.add(tuple(sorted((a, b))))
    return pairs


def cube_model(chart, lines, collinear_pairs):
    a, b = chart
    left, right = sorted(lines[a]), sorted(lines[b])
    vertices = tuple(sorted(set(left) | set(right)))
    assert len(vertices) == 8
    adj = {v: set() for v in vertices}
    antipode = {}
    for u in left:
        for v in right:
            pair = tuple(sorted((u, v)))
            if pair in collinear_pairs:
                antipode[u] = v
                antipode[v] = u
            else:
                adj[u].add(v)
                adj[v].add(u)
    assert {len(adj[v]) for v in vertices} == {3}
    assert len(antipode) == 8
    return vertices, adj, antipode


def deterministic_gray_address(chart, lines, collinear_pairs):
    """Deterministic Q3 labelling; intrinsic statements below are gauge-invariant."""
    vertices, adj, antipode = cube_model(chart, lines, collinear_pairs)
    origin = min(vertices)
    neighbours = sorted(adj[origin])
    assert len(neighbours) == 3
    addr = {origin: 0}
    for bit, vertex in zip((1, 2, 4), neighbours):
        addr[vertex] = bit
    for (bit_a, va), (bit_b, vb) in combinations(zip((1, 2, 4), neighbours), 2):
        common = (adj[va] & adj[vb]) - {origin}
        assert len(common) == 1
        addr[next(iter(common))] = bit_a ^ bit_b
    addr[antipode[origin]] = 7
    assert len(addr) == 8
    assert set(addr.values()) == set(range(8))
    for u in vertices:
        assert addr[antipode[u]] == (addr[u] ^ 7)
        for v in adj[u]:
            assert addr[u] ^ addr[v] in {1, 2, 4}
    return addr, antipode


def translate_set(values, displacement):
    return {x ^ displacement for x in values}


def interface_line(chart_id, neighbour_id, charts, lines, collinear_pairs):
    addr, _ = deterministic_gray_address(charts[chart_id], lines, collinear_pairs)
    v0 = set(addr)
    v1 = set(lines[charts[neighbour_id][0]]) | set(lines[charts[neighbour_id][1]])
    shared_vertices = v0 & v1
    assert len(shared_vertices) == 4
    shared_addresses = {addr[v] for v in shared_vertices}
    stabilizers = tuple(sorted(
        d for d in range(1, 8)
        if translate_set(shared_addresses, d) == shared_addresses
    ))
    assert len(stabilizers) == 3
    assert 7 in stabilizers
    assert stabilizers in fano_lines()
    return stabilizers, tuple(sorted(shared_addresses))


def build_result():
    _points, lines = w33()
    charts, web, trans_hist = chart_web(lines)
    collinear_pairs = point_pair_collinearity(lines)
    all_fano = fano_lines()
    execution_lines = tuple(line for line in all_fano if 7 in line)
    buffer_lines = tuple(line for line in all_fano if 7 not in line)

    assert execution_lines == ((1, 6, 7), (2, 5, 7), (3, 4, 7))
    assert len(buffer_lines) == 4

    local_rows = []
    global_line_slot_hist = Counter()
    complementary_sheet_checks = 0
    for ci in range(len(charts)):
        grouped = defaultdict(list)
        for cj in sorted(web[ci]):
            line, shared = interface_line(ci, cj, charts, lines, collinear_pairs)
            grouped[line].append({"neighbour": cj, "shared_addresses": list(shared)})
        assert set(grouped) == set(execution_lines)
        assert {len(rows) for rows in grouped.values()} == {2}
        for line, rows in grouped.items():
            global_line_slot_hist[line] += 1
            a = set(rows[0]["shared_addresses"])
            b = set(rows[1]["shared_addresses"])
            assert a.isdisjoint(b) and a | b == set(range(8))
            complementary_sheet_checks += 1
        if ci < 8:
            local_rows.append({
                "chart_id": ci,
                "axis_lines": list(charts[ci]),
                "canonical_heawood_point": 7,
                "execution_fano_lines": [list(x) for x in execution_lines],
                "buffer_fano_lines": [list(x) for x in buffer_lines],
                "two_sheet_interfaces": {
                    "-".join(map(str, line)): rows
                    for line, rows in sorted(grouped.items())
                },
            })

    directed_web_incidences = sum(len(n) for n in web)
    execution_slots = len(charts) * len(execution_lines)

    checks = {
        "chart_web_is_540_nodes_1620_edges_degree6": (
            len(charts) == 540
            and edge_count(web) == 1620
            and {len(n) for n in web} == {6}
        ),
        "every_chart_has_four_transversals": trans_hist == {4: 540},
        "local_translation_fano_has_7_points_7_lines": len(all_fano) == 7,
        "canonical_antipode_point_has_three_incident_lines": len(execution_lines) == 3,
        "four_nonincident_lines_are_buffers": len(buffer_lines) == 4,
        "six_neighbors_are_two_sheet_cover_of_three_execution_lines": (
            directed_web_incidences == 3240
            and execution_slots == 1620
            and directed_web_incidences == 2 * execution_slots
        ),
        "every_execution_slot_has_complementary_two_sheets": (
            complementary_sheet_checks == execution_slots
        ),
        "each_standard_execution_line_occurs_once_per_chart": (
            dict(global_line_slot_hist)
            == {(1, 6, 7): 540, (2, 5, 7): 540, (3, 4, 7): 540}
        ),
    }

    return {
        "schema": "w33.heawood-chart-fibre-quotient.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "Each of the 540 W33 Q3 charts carries a local Heawood fibre on the "
            "seven nonzero F2^3 translations and their seven Fano lines. The "
            "intrinsic antipode translation 111 selects one Heawood point. The "
            "six chart-web neighbours descend 2-to-1 onto its three incident "
            "Fano-line vertices; the other four Fano lines are nonincident buffer "
            "slots."
        ),
        "counts": {
            "charts": len(charts),
            "chart_web_edges": edge_count(web),
            "directed_chart_web_incidences": directed_web_incidences,
            "heawood_fibre_vertices_per_chart": 14,
            "fano_translation_points_per_chart": 7,
            "fano_lines_per_chart": 7,
            "execution_lines_through_antipode": 3,
            "buffer_lines_not_through_antipode": 4,
            "execution_slots_over_all_charts": execution_slots,
            "web_neighbour_sheets_per_execution_slot": 2,
        },
        "standard_local_fano": {
            "points": list(range(1, 8)),
            "lines": [list(line) for line in all_fano],
            "canonical_antipode_point": 7,
            "execution_lines": [list(line) for line in execution_lines],
            "buffer_lines": [list(line) for line in buffer_lines],
        },
        "sample_chart_fibres": local_rows,
        "bt1714_bridge": (
            "BT1714's 3 Heawood execution slots + 4 co-Heawood buffer slots now "
            "have a project-native local realization: the three Fano lines "
            "incident with the Q3 antipode translation versus the four "
            "nonincident Fano lines."
        ),
        "marcelis_bridge": (
            "Marcelis places Fano point/line data and harmonic cubes on the "
            "Heawood incidence graph. Here the same Fano incidence object arises "
            "from the translation algebra internal to every W33 cube chart. This "
            "is an incidence/fibre bridge, not a claim that his harmonic cross-"
            "ratio geometry has been reconstructed optically."
        ),
        "claim_boundary": [
            "The Heawood graph is a local 14-vertex fibre, not a subgraph of the 540-chart web.",
            "The numerical F2^3 labels depend on a deterministic Gray gauge, while the 3+4 incidence split and two-sheet quotient are intrinsic up to cube automorphism.",
            "No global identification of the seven Fano labels across all 540 chart fibres is asserted.",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "charts": result["counts"]["charts"],
        "execution_slots": result["counts"]["execution_slots_over_all_charts"],
        "two_sheet_degree": result["counts"]["web_neighbour_sheets_per_execution_slot"],
    }, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
