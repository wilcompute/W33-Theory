#!/usr/bin/env python3
"""Outer-involution / Schubert-observer cube bridge.

This certificate deliberately connects three independently certified pieces of the
repository without identifying them merely because their cardinalities agree:

1. the multiplier-two outer involution D=diag(2,2,1,1) on W(3,3);
2. the eight-point stochastic open Schubert cell x0=1 in the Marcelis observer
   quotient PG(3,4)->PG(3,2);
3. the already-certified Q4 temporal router.

The new exact statement is that the complement of the W33 collinearity graph on
the eight fixed points of D is Q3.  The same Q3 has a gauge-fixed coordinate
realization on the eight stochastic observer macrostates, because x0=1 is the
affine chart AG(3,2)=F2^3.  Appending one frozen bit embeds that cube as a facet
of the repo-certified Q4.  The graph isomorphisms are explicit; the final
cross-model identification is coordinate/gauge dependent and is not claimed to
be canonical physics.

A second result records the quotient of the 36-spread four-intersection graph by
the same involution.  The four individually fixed spreads form a K4, hence all
six of their pairs are fixed C6 objects.  Six additional fixed edges arise from
spread 2-cycles whose two endpoints themselves form a four-intersection pair.
Those six become loops in the orbit quotient.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_multichart_atlas import w33  # noqa: E402
from w33_heawood_spread_pair_270_bridge import enumerate_spreads  # noqa: E402
from w33_heawood_spread_pair_psp_equivariance import (  # noqa: E402
    induced_line_perm,
    induced_spread_perm,
)
from w33_heawood_spread_pair_pgsp_equivariance import (  # noqa: E402
    MULTIPLIER_TWO,
    matrix_point_perm,
)
from w33_marcelis_observer_quotient_dynamics import build_result as build_observer  # noqa: E402

OUT = ROOT / "data" / "w33_outer_cube_observer_bridge.json"


def cycles_of_involution(perm):
    seen = set()
    out = []
    for i in range(len(perm)):
        if i in seen:
            continue
        j = perm[i]
        assert perm[j] == i
        if j == i:
            cyc = (i,)
        else:
            cyc = tuple(sorted((i, j)))
        seen.update(cyc)
        out.append(cyc)
    return tuple(sorted(out))


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def edge_set(vertices, predicate):
    return {
        tuple(sorted((a, b)))
        for a, b in combinations(vertices, 2)
        if predicate(a, b)
    }


def induced_cycle4_faces(vertices, edges):
    faces = []
    for S in combinations(vertices, 4):
        es = [e for e in combinations(S, 2) if tuple(sorted(e)) in edges]
        deg = Counter()
        for a, b in es:
            deg[a] += 1
            deg[b] += 1
        if len(es) == 4 and set(deg.values()) == {2}:
            faces.append(tuple(sorted(S)))
    return tuple(sorted(faces))


def build_result():
    points, lines = w33()
    pperm = matrix_point_perm(points, MULTIPLIER_TWO)
    lperm = induced_line_perm(lines, pperm)

    fixed_points = tuple(i for i, j in enumerate(pperm) if i == j)
    fixed_lines = tuple(i for i, j in enumerate(lperm) if i == j)
    assert len(fixed_points) == 8
    assert len(fixed_lines) == 6

    fixed_point_set = set(fixed_points)
    fully_fixed_lines = tuple(
        li for li in fixed_lines if set(lines[li]) <= fixed_point_set
    )
    assert len(fully_fixed_lines) == 2
    eigenspace_blocks = tuple(
        tuple(sorted(lines[li])) for li in fully_fixed_lines
    )
    eigenspace_blocks = tuple(sorted(eigenspace_blocks))
    A, B = eigenspace_blocks
    assert len(A) == len(B) == 4
    assert set(A).isdisjoint(B)
    assert set(A) | set(B) == fixed_point_set

    col_edges_all = set()
    for L in lines:
        for a, b in combinations(L, 2):
            col_edges_all.add(tuple(sorted((a, b))))
    fixed_col_edges = {
        e for e in col_edges_all if e[0] in fixed_point_set and e[1] in fixed_point_set
    }
    assert len(fixed_col_edges) == 16

    within_A = edge_set(A, lambda a, b: tuple(sorted((a, b))) in fixed_col_edges)
    within_B = edge_set(B, lambda a, b: tuple(sorted((a, b))) in fixed_col_edges)
    cross_col = {
        e for e in fixed_col_edges
        if (e[0] in A and e[1] in B) or (e[0] in B and e[1] in A)
    }
    assert len(within_A) == len(within_B) == 6
    assert len(cross_col) == 4

    cross_degree = Counter()
    for a, b in cross_col:
        cross_degree[a] += 1
        cross_degree[b] += 1
    assert all(cross_degree[p] == 1 for p in fixed_points)

    # The complement therefore has no edges inside A or B and all cross edges
    # except one perfect matching: the 4-crown graph, known to be Q3.  We do not
    # rely on the name; construct an explicit Hamming-cube labelling.
    fixed_vertices = tuple(sorted(fixed_points))
    complete_fixed = {tuple(sorted(e)) for e in combinations(fixed_vertices, 2)}
    cube_edges = complete_fixed - fixed_col_edges
    assert len(cube_edges) == 12

    match = {}
    for a in A:
        candidates = [b for b in B if tuple(sorted((a, b))) in cross_col]
        assert len(candidates) == 1
        match[a] = candidates[0]
    assert len(set(match.values())) == 4

    even_bits = ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0))
    cube_label = {}
    for a, bits in zip(A, even_bits):
        cube_label[a] = bits
        cube_label[match[a]] = tuple(1 - x for x in bits)
    assert len(cube_label) == 8

    expected_hamming_edges = edge_set(
        fixed_vertices,
        lambda a, b: hamming(cube_label[a], cube_label[b]) == 1,
    )
    assert expected_hamming_edges == cube_edges
    cube_faces = induced_cycle4_faces(fixed_vertices, cube_edges)
    assert len(cube_faces) == 6

    # Spread quotient under the same involution.
    spreads = enumerate_spreads(lines)
    sperm = induced_spread_perm(spreads, lperm)
    spread_cycles = cycles_of_involution(sperm)
    assert len(spreads) == 36
    assert Counter(map(len, spread_cycles)) == {1: 4, 2: 16}
    spread_orbit_id = {
        s: oi for oi, cyc in enumerate(spread_cycles) for s in cyc
    }
    fixed_spreads = tuple(c[0] for c in spread_cycles if len(c) == 1)

    four_edges = {
        tuple(sorted((a, b)))
        for a, b in combinations(range(len(spreads)), 2)
        if len(set(spreads[a]) & set(spreads[b])) == 4
    }
    assert len(four_edges) == 270
    fixed_spread_K4_edges = {
        tuple(sorted((a, b))) for a, b in combinations(fixed_spreads, 2)
    }
    assert fixed_spread_K4_edges <= four_edges
    assert len(fixed_spread_K4_edges) == 6

    swapped_pair_edges = {
        tuple(sorted(cyc)) for cyc in spread_cycles
        if len(cyc) == 2 and tuple(sorted(cyc)) in four_edges
    }
    assert len(swapped_pair_edges) == 6

    seen_edges = set()
    edge_orbits = []
    for e in sorted(four_edges):
        if e in seen_edges:
            continue
        a, b = e
        image = tuple(sorted((sperm[a], sperm[b])))
        orbit = tuple(sorted({e, image}))
        seen_edges.update(orbit)
        edge_orbits.append(orbit)
    assert len(edge_orbits) == 141
    assert Counter(map(len, edge_orbits)) == {1: 12, 2: 129}

    quotient_buckets = defaultdict(list)
    fixed_edge_types = Counter()
    for orbit in edge_orbits:
        a, b = orbit[0]
        qa, qb = spread_orbit_id[a], spread_orbit_id[b]
        qedge = tuple(sorted((qa, qb)))
        quotient_buckets[qedge].append(orbit)
        if len(orbit) == 1:
            if qa == qb:
                fixed_edge_types["loop_from_exchanged_spreads"] += 1
            else:
                fixed_edge_types["edge_between_fixed_spreads"] += 1

    quotient_parallel_hist = Counter(len(v) for v in quotient_buckets.values())
    quotient_loop_keys = tuple(sorted(k for k in quotient_buckets if k[0] == k[1]))
    assert fixed_edge_types == {
        "edge_between_fixed_spreads": 6,
        "loop_from_exchanged_spreads": 6,
    }
    assert len(quotient_loop_keys) == 6
    assert sum(len(orbit) for orbit in edge_orbits) == 270

    # Observer cube: the exact stochastic sector is the affine chart x0=1,
    # hence has coordinates (x1,x2,x3) in F2^3.
    observer = build_observer()
    model = observer["n3_one_step_model"]
    stochastic = {
        row["macrostate"]
        for row in model["rows"]
        if row["conditional_entropy_bits"] > 0
    }
    expected_stochastic = {
        "1" + "".join(map(str, tail)) for tail in product((0, 1), repeat=3)
    }
    assert stochastic == expected_stochastic

    fixed_to_observer = {
        str(p): "1" + "".join(map(str, cube_label[p]))
        for p in fixed_vertices
    }
    assert set(fixed_to_observer.values()) == stochastic
    observer_cube_edges = {
        tuple(sorted((fixed_to_observer[a], fixed_to_observer[b])))
        for a, b in cube_edges
    }
    expected_observer_cube_edges = {
        tuple(sorted((a, b)))
        for a, b in combinations(stochastic, 2)
        if hamming(a[1:], b[1:]) == 1
    }
    assert observer_cube_edges == expected_observer_cube_edges

    # Q4 facet weld: append a frozen leading bit.  The existing repo certificate
    # independently proves that the 4x4 toroidal knight graph is Q4.
    q4_cert = json.loads(
        (ROOT / "data" / "PART_W33_PASS5468_5475_SIMPLEX_STABILISER_IS_WF4.json")
        .read_text(encoding="utf-8")
    )
    assert q4_cert["pass_5470"]["knight_is_Q4"] is True
    assert q4_cert["pass_5470"]["vertices"] == 16
    assert q4_cert["pass_5470"]["edges"] == 32
    observer_to_q4_facet = {m: "0" + m[1:] for m in sorted(stochastic)}
    q4_facet_vertices = set(observer_to_q4_facet.values())
    q4_facet_edges = {
        tuple(sorted((a, b)))
        for a, b in combinations(q4_facet_vertices, 2)
        if hamming(a, b) == 1
    }
    assert len(q4_facet_vertices) == 8 and len(q4_facet_edges) == 12

    checks = {
        "outer_fixed_points_are_two_disjoint_four_point_lines": True,
        "fixed_collinearity_is_two_K4s_plus_perfect_matching": True,
        "fixed_collinearity_complement_is_explicit_Q3": expected_hamming_edges == cube_edges,
        "Q3_has_8_vertices_12_edges_6_square_faces": (
            len(fixed_vertices) == 8 and len(cube_edges) == 12 and len(cube_faces) == 6
        ),
        "four_fixed_spreads_form_K4_in_four_intersection_graph": len(fixed_spread_K4_edges) == 6,
        "six_swapped_spread_orbits_are_internal_four_intersection_edges": len(swapped_pair_edges) == 6,
        "spread_quotient_has_12_fixed_edge_orbits_split_6_plus_6": fixed_edge_types == {
            "edge_between_fixed_spreads": 6,
            "loop_from_exchanged_spreads": 6,
        },
        "stochastic_observer_sector_is_affine_F2_cubed": stochastic == expected_stochastic,
        "fixed_Q3_is_explicitly_isomorphic_to_observer_affine_cube": observer_cube_edges == expected_observer_cube_edges,
        "observer_cube_embeds_as_Q4_facet": len(q4_facet_edges) == 12,
        "prior_temporal_router_certificate_says_knight_is_Q4": q4_cert["pass_5470"]["knight_is_Q4"] is True,
    }

    return {
        "schema": "w33.outer-cube-observer-bridge.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The multiplier-two outer involution contains a literal cubical residue: "
            "on its eight fixed W33 points, the complement of collinearity is Q3. "
            "The eight stochastic Marcelis observer states form the affine chart "
            "x0=1 ~= F2^3, giving an explicit gauge-fixed Q3-to-Q3 bridge, and that "
            "cube embeds as a facet of the previously certified Q4 temporal router."
        ),
        "outer_fixed_cube": {
            "fixed_point_ids": list(fixed_vertices),
            "fully_fixed_line_ids": list(fully_fixed_lines),
            "eigenspace_point_blocks": [list(A), list(B)],
            "W33_collinearity_edges_on_fixed_points": len(fixed_col_edges),
            "cross_collinearity_perfect_matching": [list(e) for e in sorted(cross_col)],
            "complement_Q3_edges": [list(e) for e in sorted(cube_edges)],
            "Q3_bit_labels": {str(p): "".join(map(str, cube_label[p])) for p in fixed_vertices},
            "Q3_square_faces": [
                ["".join(map(str, cube_label[p])) for p in face]
                for face in cube_faces
            ],
            "graph_identity": "complement(W33[Fix(D)]) = K4,4 - perfect_matching ~= Q3",
        },
        "spread_orbit_quotient": {
            "spread_orbit_count": len(spread_cycles),
            "spread_orbit_size_histogram": {str(k): v for k, v in sorted(Counter(map(len, spread_cycles)).items())},
            "fixed_spread_ids": list(fixed_spreads),
            "fixed_spread_K4_edges": [list(e) for e in sorted(fixed_spread_K4_edges)],
            "swapped_orbit_internal_edges": [list(e) for e in sorted(swapped_pair_edges)],
            "four_intersection_edge_orbits": len(edge_orbits),
            "edge_orbit_size_histogram": {str(k): v for k, v in sorted(Counter(map(len, edge_orbits)).items())},
            "fixed_edge_types": dict(sorted(fixed_edge_types.items())),
            "quotient_loop_count": len(quotient_loop_keys),
            "quotient_underlying_edge_keys": len(quotient_buckets),
            "quotient_parallel_multiplicity_histogram": {str(k): v for k, v in sorted(quotient_parallel_hist.items())},
            "lifted_edge_mass": sum(len(orbit) for orbit in edge_orbits),
            "reading": (
                "The six both-fixed C6s are exactly the six edges of the K4 on the "
                "four fixed spreads.  The six exchanged C6s are internal edges of "
                "six 2-cycles of spreads and therefore appear as loops after quotienting."
            ),
        },
        "observer_affine_cube": {
            "stochastic_macrostates": sorted(stochastic),
            "projective_split": "PG(3,2) = AG(3,2) disjoint_union PG(2,2) = 8 + 7",
            "affine_chart": "x0=1; tail (x1,x2,x3) in F2^3",
            "fixed_point_to_observer_macrostate": fixed_to_observer,
            "observer_Q3_edges": [list(e) for e in sorted(observer_cube_edges)],
            "dynamics_boundary": (
                "Q3 here is the coordinate/Hamming graph on the eight stochastic "
                "macrostates, not a claim that every nonzero observer transition is a cube edge."
            ),
        },
        "Q4_facet_weld": {
            "prior_certificate": "data/PART_W33_PASS5468_5475_SIMPLEX_STABILISER_IS_WF4.json#pass_5470",
            "prior_Q4_vertices": q4_cert["pass_5470"]["vertices"],
            "prior_Q4_edges": q4_cert["pass_5470"]["edges"],
            "observer_macrostate_to_Q4_facet_vertex": observer_to_q4_facet,
            "facet_vertex_count": len(q4_facet_vertices),
            "facet_edge_count": len(q4_facet_edges),
        },
        "claim_boundary": [
            "The Q3 on fixed W33 points is intrinsic once the declared outer involution is fixed; the bit labels are a chosen graph isomorphism.",
            "The Q3 on x0=1 uses the declared ordered-coordinate Marcelis gauge and Hamming adjacency on affine coordinates.",
            "The bridge between the two Q3 realizations is explicit but not claimed to be canonical under the full symmetry groups.",
            "The Q4 facet weld is a combinatorial/controller bridge, not evidence that an outer involution physically creates a spatial cube.",
            "The spread orbit quotient is a looped multigraph quotient; quotient loops record exchanged endpoints rather than self-incidence in the original simple graph.",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "fixed_cube": result["outer_fixed_cube"]["graph_identity"],
        "spread_fixed_edge_types": result["spread_orbit_quotient"]["fixed_edge_types"],
        "quotient_parallel_histogram": result["spread_orbit_quotient"]["quotient_parallel_multiplicity_histogram"],
        "observer_stochastic_states": len(result["observer_affine_cube"]["stochastic_macrostates"]),
        "q4_facet_edges": result["Q4_facet_weld"]["facet_edge_count"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
