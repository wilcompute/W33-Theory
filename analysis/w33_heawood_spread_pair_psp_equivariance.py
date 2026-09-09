#!/usr/bin/env python3
"""Exact PSp(4,3)-equivariance audit for the 270 Heawood/spread bridge.

The companion certificate ``w33_heawood_spread_pair_270_bridge.py`` proved an
object-level bijection between

  * the 270 C6 components of the intrinsic Heawood execution-slot graph, and
  * the 270 unordered pairs of W(3,3) spreads meeting in four lines,

by sending a C6 to the unique spread pair whose symmetric difference is the
12-line union of the six chart axes in that cycle.

This file upgrades that finite-set bijection to an equivariant statement for
the projective symplectic group PSp(4,3).  We reuse the eight explicit
symplectic transvections already used by ``bt980_aut_action_on_homology.py``.
For each generator we induce its permutations on W33 points, lines, the 540 Q3
charts, intrinsic two-sheet execution slots, C6 components and the 36 spreads.
The audit checks generator-by-generator that the C6 -> spread-pair map commutes
with the action.

The resulting action on the 270 cycles is transitive.  Using the established
|PSp(4,3)| = 25920 gives a cycle stabilizer of order 96.

Claim boundary: this proves PSp(4,3)-equivariance.  Pass 1996 uses a full
order-51840 extension and obtains a full-G stabilizer of order 192.  We do not
claim full-G equivariance here until an explicit outer generator is audited.
The order 96 also occurs as the tomotope symmetry order elsewhere in the repo;
that numerical collision is recorded only as a research lead, not a group
isomorphism.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
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
    interface_line,
    point_pair_collinearity,
)
from w33_heawood_spread_pair_270_bridge import (  # noqa: E402
    connected_components,
    enumerate_spreads,
)

OUT = ROOT / "data" / "w33_heawood_spread_pair_psp_equivariance.json"
PSP43_ORDER = 25920
GENERATOR_VECTORS = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
    (1, 1, 0, 0),
    (1, 0, 1, 0),
    (0, 1, 0, 1),
    (1, 1, 1, 1),
)


def canon_f3(v):
    row = tuple(int(x) % 3 for x in v)
    for x in row:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in row)
    raise ValueError("zero vector")


def symplectic_form(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def transvection_point_perm(points, v):
    index = {p: i for i, p in enumerate(points)}
    out = []
    for p in points:
        lam = symplectic_form(p, v)
        image = tuple((p[i] + lam * v[i]) % 3 for i in range(4))
        out.append(index[canon_f3(image)])
    assert sorted(out) == list(range(len(points)))
    return tuple(out)


def induced_line_perm(lines, point_perm):
    index = {tuple(sorted(L)): i for i, L in enumerate(lines)}
    out = []
    for L in lines:
        image = tuple(sorted(point_perm[p] for p in L))
        assert image in index
        out.append(index[image])
    assert sorted(out) == list(range(len(lines)))
    return tuple(out)


def induced_chart_perm(charts, line_perm):
    index = {tuple(sorted(c)): i for i, c in enumerate(charts)}
    out = []
    for a, b in charts:
        image = tuple(sorted((line_perm[a], line_perm[b])))
        assert image in index
        out.append(index[image])
    assert sorted(out) == list(range(len(charts)))
    return tuple(out)


def intrinsic_slot_graph(charts, web, lines):
    """Gauge-free execution slots encoded by their two neighboring charts.

    The local Fano names used in the fibre certificate are Gray-gauge labels.
    The actual slot is intrinsic: it is the unordered pair of chart-web
    neighbours lying over one execution line.  This representation makes the
    group audit independent of local F2^3 label choices.
    """
    collinear_pairs = point_pair_collinearity(lines)
    grouped_by_chart = {}
    node_for_directed_edge = {}

    for ci in range(len(charts)):
        groups = defaultdict(list)
        for cj in sorted(web[ci]):
            local_line, _shared = interface_line(
                ci, cj, charts, lines, collinear_pairs
            )
            groups[local_line].append(cj)
        assert len(groups) == 3
        assert {len(v) for v in groups.values()} == {2}
        pairs = tuple(sorted(tuple(sorted(v)) for v in groups.values()))
        grouped_by_chart[ci] = pairs
        for pair in pairs:
            node = (ci, pair)
            for cj in pair:
                node_for_directed_edge[(ci, cj)] = node

    adj = defaultdict(set)
    for ci in range(len(charts)):
        for cj in web[ci]:
            if ci >= cj:
                continue
            a = node_for_directed_edge[(ci, cj)]
            b = node_for_directed_edge[(cj, ci)]
            adj[a].add(b)
            adj[b].add(a)

    assert len(adj) == 1620
    assert {len(nbrs) for nbrs in adj.values()} == {2}
    return dict(adj), grouped_by_chart


def component_to_spread_pair(components, charts, spreads):
    four_pair_by_symdiff = {}
    spread_intersection_hist = Counter()
    for i, j in combinations(range(len(spreads)), 2):
        A, B = set(spreads[i]), set(spreads[j])
        r = len(A & B)
        spread_intersection_hist[r] += 1
        if r == 4:
            key = frozenset(A ^ B)
            assert len(key) == 12
            assert key not in four_pair_by_symdiff
            four_pair_by_symdiff[key] = tuple(sorted((i, j)))

    mapping = {}
    for cid, comp in enumerate(components):
        axis_union = frozenset(
            li for chart_id, _pair in comp for li in charts[chart_id]
        )
        assert len(axis_union) == 12
        assert axis_union in four_pair_by_symdiff
        mapping[cid] = four_pair_by_symdiff[axis_union]

    assert len(set(mapping.values())) == 270
    return mapping, four_pair_by_symdiff, spread_intersection_hist


def induced_spread_perm(spreads, line_perm):
    index = {tuple(sorted(S)): i for i, S in enumerate(spreads)}
    out = []
    for S in spreads:
        image = tuple(sorted(line_perm[li] for li in S))
        assert image in index
        out.append(index[image])
    assert sorted(out) == list(range(len(spreads)))
    return tuple(out)


def map_slot_node(node, chart_perm):
    ci, neighbour_pair = node
    return (
        chart_perm[ci],
        tuple(sorted(chart_perm[cj] for cj in neighbour_pair)),
    )


def build_result():
    points, lines = w33()
    charts, web, trans_hist = chart_web(lines)
    spreads = enumerate_spreads(lines)
    slot_adj, grouped_by_chart = intrinsic_slot_graph(charts, web, lines)
    components = connected_components(slot_adj)
    assert len(components) == 270
    assert {len(C) for C in components} == {6}

    component_index = {frozenset(C): i for i, C in enumerate(components)}
    cycle_to_pair, _by_symdiff, spread_hist = component_to_spread_pair(
        components, charts, spreads
    )

    generator_rows = []
    component_perms = []
    all_slot_graph_preserved = True
    all_bijection_equivariant = True
    all_chart_web_preserved = True

    for v in GENERATOR_VECTORS:
        pperm = transvection_point_perm(points, v)
        lperm = induced_line_perm(lines, pperm)
        cperm = induced_chart_perm(charts, lperm)
        sperm = induced_spread_perm(spreads, lperm)

        chart_ok = all(
            {cperm[x] for x in web[ci]} == set(web[cperm[ci]])
            for ci in range(len(charts))
        )
        all_chart_web_preserved &= chart_ok

        mapped_nodes = {node: map_slot_node(node, cperm) for node in slot_adj}
        assert set(mapped_nodes.values()) == set(slot_adj)
        slot_graph_ok = all(
            mapped_nodes[vtx] in slot_adj[mapped_nodes[u]]
            for u, nbrs in slot_adj.items()
            for vtx in nbrs
        )
        all_slot_graph_preserved &= slot_graph_ok

        comp_perm = []
        equivariant = True
        for cid, comp in enumerate(components):
            image = frozenset(mapped_nodes[node] for node in comp)
            assert image in component_index
            cid2 = component_index[image]
            comp_perm.append(cid2)

            si, sj = cycle_to_pair[cid]
            expected_pair = tuple(sorted((sperm[si], sperm[sj])))
            if cycle_to_pair[cid2] != expected_pair:
                equivariant = False
        assert sorted(comp_perm) == list(range(270))
        component_perms.append(tuple(comp_perm))
        all_bijection_equivariant &= equivariant

        generator_rows.append(
            {
                "transvection_vector": list(v),
                "chart_web_preserved": chart_ok,
                "intrinsic_slot_graph_preserved": slot_graph_ok,
                "cycle_spread_bijection_equivariant": equivariant,
                "cycle_fixed_points": sum(i == j for i, j in enumerate(comp_perm)),
            }
        )

    # Exact orbit of one cycle under the declared PSp generating set.
    seen = {0}
    q = deque([0])
    while q:
        c = q.popleft()
        for perm in component_perms:
            d = perm[c]
            if d not in seen:
                seen.add(d)
                q.append(d)
    orbit_size = len(seen)
    stabilizer_order = PSP43_ORDER // orbit_size

    checks = {
        "W33_is_40_points_40_lines": len(points) == 40 and len(lines) == 40,
        "chart_web_is_540_degree6_1620": (
            len(charts) == 540
            and trans_hist == {4: 540}
            and edge_count(web) == 1620
            and {len(n) for n in web} == {6}
        ),
        "W33_has_36_spreads": len(spreads) == 36,
        "spread_pairs_split_360_at_1_and_270_at_4": (
            dict(sorted(spread_hist.items())) == {1: 360, 4: 270}
        ),
        "intrinsic_slot_graph_is_1620_degree2": (
            len(slot_adj) == 1620 and {len(n) for n in slot_adj.values()} == {2}
        ),
        "intrinsic_slot_graph_is_270_C6": (
            len(components) == 270 and {len(C) for C in components} == {6}
        ),
        "cycle_to_four_intersection_spread_pair_is_bijective": (
            len(set(cycle_to_pair.values())) == 270
        ),
        "eight_declared_transvections_act": len(generator_rows) == 8,
        "all_generators_preserve_chart_web": all_chart_web_preserved,
        "all_generators_preserve_intrinsic_slot_graph": all_slot_graph_preserved,
        "all_generators_commute_with_cycle_spread_bijection": all_bijection_equivariant,
        "PSp_generator_orbit_on_cycles_is_all_270": orbit_size == 270,
        "PSp_cycle_stabilizer_order_is_96": stabilizer_order == 96,
    }

    return {
        "schema": "w33.heawood-spread-pair-psp-equivariance.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The explicit C6-to-spread-pair bijection is PSp(4,3)-equivariant. "
            "Each of the eight symplectic transvection generators preserves the "
            "intrinsic two-sheet execution-slot graph and commutes with the map "
            "from a C6 to the unique four-intersection spread pair having the same "
            "12-line symmetric difference. The PSp orbit of one cycle has all "
            "270 cycles, so the PSp stabilizer has order 96."
        ),
        "counts": {
            "PSp43_order_from_prior_certified_repo_result": PSP43_ORDER,
            "transvection_generators": len(GENERATOR_VECTORS),
            "charts": len(charts),
            "intrinsic_execution_slots": len(slot_adj),
            "C6_components": len(components),
            "spreads": len(spreads),
            "four_intersection_spread_pairs": spread_hist[4],
            "PSp_orbit_of_one_C6": orbit_size,
            "PSp_C6_stabilizer_order": stabilizer_order,
        },
        "generator_audit": generator_rows,
        "equivariant_dictionary": {
            "slot_representation": (
                "A local execution slot is represented intrinsically as "
                "(chart, unordered pair of the two neighbouring charts lying "
                "over that slot), avoiding Gray-gauge F2^3 names."
            ),
            "C6_to_spread_pair": (
                "Union the six chart-axis pairs in the C6. The resulting 12 "
                "lines are S triangle T for a unique spread pair with |S cap T|=4."
            ),
            "equivariance_equation": (
                "For every declared PSp generator g and every cycle C, "
                "Phi(g.C) = g.Phi(C)."
            ),
        },
        "prior_repo_bridge": {
            "bt980": (
                "The eight transvection vectors are the explicit PSp(4,3) "
                "generators already used in analysis/bt980_aut_action_on_homology.py."
            ),
            "pass_1996": (
                "Pass 1996 independently proved that the 270 four-intersection "
                "spread pairs form the size-270 full-G G-set with stabilizer "
                "order 192 = D8 x S4."
            ),
        },
        "new_leads_not_claims": [
            "The PSp stabilizer order 96 equals the tomotope symmetry order used elsewhere in the architecture; no isomorphism is claimed without a stabilizer-structure audit.",
            "The ratio 192/96=2 is consistent with the PSp action being the index-two projective symplectic part of the full-G Pass-1996 action; an explicit outer-generator audit is still required before promoting this certificate to full-G equivariance.",
        ],
        "claim_boundary": [
            "This certificate proves equivariance only for the PSp(4,3) action generated by the eight audited transvections.",
            "The order 25920 is imported from the already-certified PSp(4,3) action in the repo and is not rederived by closing all 25920 elements here.",
            "No tomotope-group identification follows from the common order 96 alone.",
            "No cryptographic or physical-security property follows from this finite G-set theorem by itself.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "cycles": result["counts"]["C6_components"],
                "PSp_orbit": result["counts"]["PSp_orbit_of_one_C6"],
                "PSp_stabilizer_order": result["counts"]["PSp_C6_stabilizer_order"],
                "equivariant": result["checks"]["all_generators_commute_with_cycle_spread_bijection"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
