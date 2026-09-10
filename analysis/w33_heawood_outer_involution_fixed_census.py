#!/usr/bin/env python3
"""Fixed-object census for the multiplier-two outer involution on the 270 C6 G-set.

The full PGSp equivariance certificate closes the C6 <-> four-intersection
spread-pair dictionary under the outer similitude

    D = diag(2,2,1,1),   omega(Dx,Dy)=2 omega(x,y).

That certificate records 12 fixed C6 components.  Here we resolve what those
12 fixed objects mean on the spread side.  For an unordered spread pair
{S,T}, an involution can fix the pair in exactly two ways:

  * pointwise on the pair: D(S)=S and D(T)=T;
  * setwise by exchange:   D(S)=T and D(T)=S.

The script computes the complete cycle structure on W33 points, lines, spreads,
270 four-intersection spread pairs, and 270 intrinsic Heawood C6 components,
and verifies that the explicit equivariant dictionary carries fixed C6s to
exactly the fixed spread pairs with the same two-way classification.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_multichart_atlas import w33, chart_web  # noqa: E402
from w33_heawood_spread_pair_270_bridge import (  # noqa: E402
    connected_components,
    enumerate_spreads,
)
from w33_heawood_spread_pair_psp_equivariance import (  # noqa: E402
    component_to_spread_pair,
    induced_chart_perm,
    induced_line_perm,
    induced_spread_perm,
    intrinsic_slot_graph,
    map_slot_node,
)
from w33_heawood_spread_pair_pgsp_equivariance import (  # noqa: E402
    MULTIPLIER_TWO,
    matrix_point_perm,
)

OUT = ROOT / "data" / "w33_heawood_outer_involution_fixed_census.json"


def involution_cycle_histogram(perm):
    seen = set()
    hist = Counter()
    cycles = []
    for i in range(len(perm)):
        if i in seen:
            continue
        cyc = []
        j = i
        while j not in seen:
            seen.add(j)
            cyc.append(j)
            j = perm[j]
        hist[len(cyc)] += 1
        cycles.append(tuple(cyc))
    return hist, tuple(cycles)


def build_result():
    points, lines = w33()
    charts, web, _ = chart_web(lines)
    spreads = enumerate_spreads(lines)
    slot_adj, _ = intrinsic_slot_graph(charts, web, lines)
    components = connected_components(slot_adj)
    assert len(components) == 270 and {len(C) for C in components} == {6}
    component_index = {frozenset(C): i for i, C in enumerate(components)}

    cycle_to_pair, _by_symdiff, spread_hist = component_to_spread_pair(
        components, charts, spreads
    )
    pair_to_cycle = {pair: cid for cid, pair in cycle_to_pair.items()}
    assert len(pair_to_cycle) == 270

    pperm = matrix_point_perm(points, MULTIPLIER_TWO)
    lperm = induced_line_perm(lines, pperm)
    cperm = induced_chart_perm(charts, lperm)
    sperm = induced_spread_perm(spreads, lperm)

    mapped_nodes = {node: map_slot_node(node, cperm) for node in slot_adj}
    comp_perm = []
    for comp in components:
        image = frozenset(mapped_nodes[node] for node in comp)
        comp_perm.append(component_index[image])
    comp_perm = tuple(comp_perm)
    assert sorted(comp_perm) == list(range(270))

    four_pairs = tuple(sorted(pair_to_cycle))
    four_pair_index = {pair: i for i, pair in enumerate(four_pairs)}
    pair_perm = []
    for a, b in four_pairs:
        image = tuple(sorted((sperm[a], sperm[b])))
        assert image in four_pair_index
        pair_perm.append(four_pair_index[image])
    pair_perm = tuple(pair_perm)

    point_hist, point_cycles = involution_cycle_histogram(pperm)
    line_hist, line_cycles = involution_cycle_histogram(lperm)
    spread_cycle_hist, spread_cycles = involution_cycle_histogram(sperm)
    pair_cycle_hist, pair_cycles = involution_cycle_histogram(pair_perm)
    comp_cycle_hist, comp_cycles = involution_cycle_histogram(comp_perm)

    assert set(point_hist) <= {1, 2}
    assert set(line_hist) <= {1, 2}
    assert set(spread_cycle_hist) <= {1, 2}
    assert set(pair_cycle_hist) <= {1, 2}
    assert set(comp_cycle_hist) <= {1, 2}

    fixed_spreads = {i for i in range(len(spreads)) if sperm[i] == i}
    fixed_pairs = [pair for pair in four_pairs if tuple(sorted((sperm[pair[0]], sperm[pair[1]]))) == pair]
    fixed_components = [i for i in range(270) if comp_perm[i] == i]

    pair_classes = Counter()
    pair_rows = []
    for pair in fixed_pairs:
        a, b = pair
        if sperm[a] == a and sperm[b] == b:
            mode = "both_spreads_fixed"
        elif sperm[a] == b and sperm[b] == a:
            mode = "spreads_exchanged"
        else:
            raise AssertionError((pair, sperm[a], sperm[b]))
        pair_classes[mode] += 1
        cid = pair_to_cycle[pair]
        pair_rows.append(
            {
                "spread_pair": [a, b],
                "mode": mode,
                "cycle_id": cid,
                "cycle_is_fixed": comp_perm[cid] == cid,
                "shared_lines": sorted(set(spreads[a]) & set(spreads[b])),
                "symmetric_difference_lines": sorted(set(spreads[a]) ^ set(spreads[b])),
            }
        )

    fixed_pair_set = set(fixed_pairs)
    fixed_component_pair_set = {cycle_to_pair[cid] for cid in fixed_components}

    # Fixed lines can be sorted by whether the outer involution fixes all four
    # points on that line or swaps two point-pairs.  This gives a low-level
    # geometric fingerprint for the outer coset.
    fixed_line_modes = Counter()
    fixed_line_rows = []
    for li in [i for i in range(len(lines)) if lperm[i] == i]:
        L = tuple(lines[li])
        restricted = {p: pperm[p] for p in L}
        fixed_point_count = sum(restricted[p] == p for p in L)
        mode = f"fixed_points_{fixed_point_count}"
        fixed_line_modes[mode] += 1
        fixed_line_rows.append(
            {
                "line": li,
                "points": list(L),
                "fixed_points_on_line": fixed_point_count,
            }
        )

    checks = {
        "outer_is_involution_on_points": all(pperm[pperm[i]] == i for i in range(len(pperm))),
        "outer_is_involution_on_lines": all(lperm[lperm[i]] == i for i in range(len(lperm))),
        "outer_is_involution_on_spreads": all(sperm[sperm[i]] == i for i in range(len(sperm))),
        "outer_is_involution_on_four_pairs": all(pair_perm[pair_perm[i]] == i for i in range(len(pair_perm))),
        "outer_is_involution_on_C6": all(comp_perm[comp_perm[i]] == i for i in range(len(comp_perm))),
        "four_intersection_pair_count_is_270": spread_hist[4] == 270 and len(four_pairs) == 270,
        "fixed_C6_count_is_12": len(fixed_components) == 12,
        "fixed_pair_count_is_12": len(fixed_pairs) == 12,
        "fixed_C6_dictionary_equals_fixed_pair_dictionary": fixed_pair_set == fixed_component_pair_set,
        "every_fixed_pair_is_pointwise_fixed_or_exchanged": sum(pair_classes.values()) == len(fixed_pairs),
        "pair_and_C6_cycle_histograms_match": pair_cycle_hist == comp_cycle_hist,
        "all_fixed_pair_rows_map_to_fixed_cycles": all(row["cycle_is_fixed"] for row in pair_rows),
    }

    return {
        "schema": "w33.heawood-outer-involution-fixed-census.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The multiplier-two outer involution fixes exactly 12 of the 270 "
            "intrinsic Heawood C6 components, and full PGSp equivariance carries "
            "them to exactly the 12 setwise-fixed four-intersection spread pairs. "
            "Each fixed pair is classified exactly as two individually fixed "
            "spreads or as an exchanged spread pair."
        ),
        "outer_generator": {
            "matrix_mod3": [list(row) for row in MULTIPLIER_TWO],
            "similitude_multiplier": 2,
        },
        "cycle_histograms": {
            "W33_points": {str(k): v for k, v in sorted(point_hist.items())},
            "W33_lines": {str(k): v for k, v in sorted(line_hist.items())},
            "spreads": {str(k): v for k, v in sorted(spread_cycle_hist.items())},
            "four_intersection_spread_pairs": {str(k): v for k, v in sorted(pair_cycle_hist.items())},
            "Heawood_C6_components": {str(k): v for k, v in sorted(comp_cycle_hist.items())},
        },
        "fixed_objects": {
            "fixed_point_ids": [c[0] for c in point_cycles if len(c) == 1],
            "fixed_line_ids": [c[0] for c in line_cycles if len(c) == 1],
            "fixed_spread_ids": sorted(fixed_spreads),
            "fixed_C6_ids": fixed_components,
            "fixed_four_intersection_pair_count": len(fixed_pairs),
            "fixed_pair_modes": dict(sorted(pair_classes.items())),
            "fixed_line_modes": dict(sorted(fixed_line_modes.items())),
        },
        "fixed_line_rows": fixed_line_rows,
        "fixed_pair_rows": pair_rows,
        "interpretation": (
            "The outer C2 is not merely an abstract index-two extension. Its "
            "action has a concrete 12 + 129*2 decomposition on the 270 execution "
            "cycles, and equivariance identifies the same decomposition on the "
            "spread-pair geometry."
        ),
        "claim_boundary": [
            "Setwise-fixed spread pairs are separated from individually fixed spreads; the two notions are not conflated.",
            "The certificate concerns the declared multiplier-two outer similitude, not every involution in PGSp(4,3).",
            "No physical interpretation is assigned to the 12 fixed cycles without an additional hardware/measurement dictionary.",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "point_cycles": result["cycle_histograms"]["W33_points"],
        "line_cycles": result["cycle_histograms"]["W33_lines"],
        "spread_cycles": result["cycle_histograms"]["spreads"],
        "pair_cycles": result["cycle_histograms"]["four_intersection_spread_pairs"],
        "fixed_pair_modes": result["fixed_objects"]["fixed_pair_modes"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
