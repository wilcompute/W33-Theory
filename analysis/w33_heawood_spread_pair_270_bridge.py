#!/usr/bin/env python3
r"""Identify the 270 Heawood execution-slot cycles with 270 spread pairs.

The local Heawood quotient certificate groups the six neighbours of every W33
Q3 chart into three two-sheet execution slots.  If each local execution slot
(chart, local-Fano-line) is treated as a vertex and every chart-web edge joins
the corresponding endpoint slots, the resulting 1620-vertex slot graph is
2-regular.

Exact computation gives a much stronger global statement:

    slot graph = 270 disjoint copies of C6.

Independently, W(3,3) has 36 spreads.  Its C(36,2)=630 unordered spread pairs
split by intersection size as

    |S cap T| = 1 : 360 pairs
    |S cap T| = 4 : 270 pairs.

This script proves an object-level bijection, not merely a count match.  For
each slot C6, take the union of the two W33 axis lines of its six chart
vertices.  It is always a 12-line set, and it is exactly the symmetric
difference S triangle T of a unique spread pair with |S cap T|=4.  Around the
six-cycle, the chart vertices alternate between three axis-pairs entirely in
S\T and three axis-pairs entirely in T\S; each side partitions its six
exclusive spread lines into three pairs.

Thus the earlier size-270 spread-pair orbit and the new global Heawood-slot
cycle decomposition are the same finite objects under an explicit bijection.
No group-equivariance claim is made here; that requires a separate G-action
audit.
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
from w33_heawood_chart_fibre_quotient import (  # noqa: E402
    fano_lines,
    interface_line,
    point_pair_collinearity,
)

OUT = ROOT / "data" / "w33_heawood_spread_pair_270_bridge.json"


def enumerate_spreads(lines: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    """Exact-cover enumeration of the 36 spreads of W(3,3)."""
    line_sets = [set(L) for L in lines]
    point_to_lines: dict[int, list[int]] = defaultdict(list)
    for li, L in enumerate(line_sets):
        for p in L:
            point_to_lines[p].append(li)

    found: set[tuple[int, ...]] = set()

    def rec(chosen: list[int], covered: set[int]) -> None:
        if len(covered) == 40:
            assert len(chosen) == 10
            found.add(tuple(sorted(chosen)))
            return
        p = next(v for v in range(40) if v not in covered)
        for li in point_to_lines[p]:
            if line_sets[li].isdisjoint(covered):
                rec(chosen + [li], covered | line_sets[li])

    rec([], set())
    return tuple(sorted(found))


def execution_lines() -> tuple[tuple[int, int, int], ...]:
    return tuple(line for line in fano_lines() if 7 in line)


def slot_graph(charts, web, lines):
    """Graph on local execution slots; each chart contributes three slot nodes."""
    collinear_pairs = point_pair_collinearity(lines)
    local_lines = execution_lines()
    assert local_lines == ((1, 6, 7), (2, 5, 7), (3, 4, 7))
    slot_adj: dict[tuple[int, tuple[int, int, int]], set[tuple[int, tuple[int, int, int]]]] = defaultdict(set)

    for ci in range(len(charts)):
        for cj in web[ci]:
            if ci >= cj:
                continue
            left, _ = interface_line(ci, cj, charts, lines, collinear_pairs)
            right, _ = interface_line(cj, ci, charts, lines, collinear_pairs)
            a = (ci, left)
            b = (cj, right)
            slot_adj[a].add(b)
            slot_adj[b].add(a)

    assert len(slot_adj) == 540 * 3
    assert {len(nbrs) for nbrs in slot_adj.values()} == {2}
    return slot_adj


def connected_components(adj):
    seen = set()
    comps = []
    for root in sorted(adj):
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        comp = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in sorted(adj[u]):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        comps.append(tuple(sorted(comp)))
    return tuple(comps)


def cycle_order(component, adj):
    """Return one deterministic cyclic ordering of a degree-2 component."""
    C = set(component)
    start = min(component)
    first = min(adj[start] & C)
    order = [start, first]
    prev, cur = start, first
    while True:
        nxts = (adj[cur] & C) - {prev}
        assert len(nxts) == 1
        nxt = next(iter(nxts))
        if nxt == start:
            break
        order.append(nxt)
        prev, cur = cur, nxt
    assert len(order) == len(component)
    return tuple(order)


def build_result() -> dict:
    _points, lines = w33()
    charts, web, _trans = chart_web(lines)
    spreads = enumerate_spreads(lines)
    adj = slot_graph(charts, web, lines)
    components = connected_components(adj)

    component_size_hist = Counter(len(C) for C in components)
    component_edge_hist = Counter(
        sum(len(adj[u] & set(C)) for u in C) // 2 for C in components
    )

    spread_intersection_hist = Counter()
    four_pair_by_symdiff: dict[frozenset[int], tuple[int, int]] = {}
    for i, j in combinations(range(len(spreads)), 2):
        A, B = set(spreads[i]), set(spreads[j])
        r = len(A & B)
        spread_intersection_hist[r] += 1
        if r == 4:
            key = frozenset(A ^ B)
            assert len(key) == 12
            assert key not in four_pair_by_symdiff
            four_pair_by_symdiff[key] = (i, j)

    matched_pairs = set()
    side_hist = Counter()
    alternation_ok = 0
    partition_ok = 0
    samples = []

    for cid, C in enumerate(components):
        axis_lines = [li for chart_id, _slot in C for li in charts[chart_id]]
        axis_set = frozenset(axis_lines)
        assert len(axis_lines) == 12
        assert len(axis_set) == 12
        assert axis_set in four_pair_by_symdiff

        si, sj = four_pair_by_symdiff[axis_set]
        matched_pairs.add((si, sj))
        A, B = set(spreads[si]), set(spreads[sj])
        common = A & B
        Aonly, Bonly = A - B, B - A
        assert len(common) == 4 and len(Aonly) == len(Bonly) == 6
        assert Aonly | Bonly == set(axis_set)

        chart_side = {}
        A_pairs = []
        B_pairs = []
        for chart_id, _slot in C:
            axes = tuple(charts[chart_id])
            aset = set(axes)
            if aset <= Aonly:
                chart_side[chart_id] = "A"
                A_pairs.append(axes)
            elif aset <= Bonly:
                chart_side[chart_id] = "B"
                B_pairs.append(axes)
            else:
                raise AssertionError((cid, chart_id, axes, si, sj))
        side_hist[(len(A_pairs), len(B_pairs))] += 1

        if (
            len(A_pairs) == len(B_pairs) == 3
            and set(x for pair in A_pairs for x in pair) == Aonly
            and set(x for pair in B_pairs for x in pair) == Bonly
        ):
            partition_ok += 1

        ordered = cycle_order(C, adj)
        side_word = [chart_side[chart_id] for chart_id, _slot in ordered]
        if all(side_word[k] != side_word[(k + 1) % 6] for k in range(6)):
            alternation_ok += 1

        if cid < 8:
            samples.append({
                "cycle_id": cid,
                "spread_pair": [si, sj],
                "common_four_lines": sorted(common),
                "A_only_six_lines": sorted(Aonly),
                "B_only_six_lines": sorted(Bonly),
                "cycle_axis_union_12": sorted(axis_set),
                "cycle_order": [
                    {
                        "chart_id": chart_id,
                        "local_execution_line": list(slot),
                        "spread_side": chart_side[chart_id],
                        "axis_lines": list(charts[chart_id]),
                    }
                    for chart_id, slot in ordered
                ],
            })

    checks = {
        "w33_chart_web_is_540_degree6_1620": (
            len(charts) == 540
            and edge_count(web) == 1620
            and {len(n) for n in web} == {6}
        ),
        "w33_has_36_spreads": len(spreads) == 36,
        "spread_pair_intersections_are_360_at_1_and_270_at_4": (
            dict(sorted(spread_intersection_hist.items())) == {1: 360, 4: 270}
        ),
        "heawood_slot_graph_has_1620_degree2_vertices": (
            len(adj) == 1620 and {len(n) for n in adj.values()} == {2}
        ),
        "slot_graph_is_270_disjoint_C6": (
            len(components) == 270
            and component_size_hist == {6: 270}
            and component_edge_hist == {6: 270}
        ),
        "every_C6_axis_union_is_12_distinct_lines": all(
            len({li for chart_id, _slot in C for li in charts[chart_id]}) == 12
            for C in components
        ),
        "C6_axis_unions_biject_to_four_intersection_spread_symdiffs": (
            len(matched_pairs) == 270
            and len(four_pair_by_symdiff) == 270
            and matched_pairs == set(four_pair_by_symdiff.values())
        ),
        "each_C6_has_three_axis_pairs_from_each_spread_side": (
            side_hist == {(3, 3): 270}
        ),
        "each_side_three_pairs_partition_its_six_exclusive_lines": partition_ok == 270,
        "cycle_order_alternates_between_the_two_spread_sides": alternation_ok == 270,
    }

    return {
        "schema": "w33.heawood-spread-pair-270-bridge.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The 1620 local Heawood execution slots glue through the 540-chart "
            "web into 270 disjoint C6 cycles.  The 12 W33 axis lines carried by "
            "each C6 are exactly the symmetric difference of a unique pair of "
            "spreads meeting in four lines.  Hence the 270 Heawood-slot cycles "
            "and the repo's 270 four-intersection spread pairs are the same "
            "finite objects under an explicit bijection."
        ),
        "counts": {
            "charts": len(charts),
            "chart_web_edges": edge_count(web),
            "local_execution_slots": len(adj),
            "slot_cycles": len(components),
            "slot_cycle_length": 6,
            "spreads": len(spreads),
            "spread_pairs_total": len(spreads) * (len(spreads) - 1) // 2,
            "spread_pairs_intersection_1": spread_intersection_hist[1],
            "spread_pairs_intersection_4": spread_intersection_hist[4],
        },
        "object_dictionary": {
            "C6_to_spread_pair": (
                "Union the two W33 axis lines of the six chart vertices in the "
                "execution-slot C6.  The resulting 12-line set is S triangle T "
                "for one and only one spread pair with |S cap T|=4."
            ),
            "spread_pair_to_C6": (
                "For a four-intersection pair S,T, its 12-line symmetric "
                "difference occurs as exactly one execution-slot cycle axis union."
            ),
            "cycle_internal_law": (
                "The six chart vertices alternate A,B,A,B,A,B around C6. The "
                "three A charts partition S\\T into three axis pairs; the three "
                "B charts partition T\\S into three axis pairs."
            ),
        },
        "prior_repo_bridge": {
            "pass_1996": (
                "Pass 1996 identified the size-270 G-set with unordered pairs of "
                "spreads meeting in four lines. This certificate identifies the "
                "new Heawood execution-slot C6 objects with those same spread "
                "pairs by their literal 12-line symmetric differences, not by "
                "matching cardinalities."
            )
        },
        "samples": samples,
        "claim_boundary": [
            "This is an exact finite-set bijection. A separate automorphism audit is required before calling it a proved G-set isomorphism.",
            "The local numerical F2^3/Fano labels are gauge choices; the slot pairing, C6 components and 12-line symmetric-difference objects are the invariant content tested here.",
            "No cryptographic or physical-network security property follows from the 270-cycle identification by itself.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "slot_cycles": result["counts"]["slot_cycles"],
        "spread_pairs_intersection_4": result["counts"]["spread_pairs_intersection_4"],
        "bijection": result["checks"]["C6_axis_unions_biject_to_four_intersection_spread_symdiffs"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
