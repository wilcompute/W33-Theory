#!/usr/bin/env python3
"""Corrected outer-involution / observer Q3 bridge.

Supersedes the first bridge runner by keeping W33 point ids as integers until
serialization.  It proves four exact statements:
  * complement(W33[Fix(D)]) is Q3 for D=diag(2,2,1,1);
  * the four fixed spreads form a K4 and the 12 fixed four-intersection edges
    split as 6 K4 edges + 6 exchanged-endpoint loops in the orbit quotient;
  * the eight stochastic observer states are the affine chart x0=1 ~= F2^3;
  * an explicit bit labelling identifies the two Q3 realizations and embeds the
    observer cube as a facet of the already-certified Q4 temporal router.
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
from w33_heawood_spread_pair_psp_equivariance import induced_line_perm, induced_spread_perm  # noqa: E402
from w33_heawood_spread_pair_pgsp_equivariance import MULTIPLIER_TWO, matrix_point_perm  # noqa: E402
from w33_marcelis_observer_quotient_dynamics import build_result as build_observer  # noqa: E402

OUT = ROOT / "data" / "w33_outer_cube_observer_bridge.json"


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def inv_cycles(perm):
    seen, out = set(), []
    for i in range(len(perm)):
        if i in seen:
            continue
        j = perm[i]
        assert perm[j] == i
        cyc = (i,) if i == j else tuple(sorted((i, j)))
        seen.update(cyc)
        out.append(cyc)
    return tuple(sorted(out))


def four_cycle_faces(vertices, edges):
    faces = []
    for S in combinations(vertices, 4):
        es = [tuple(sorted(e)) for e in combinations(S, 2) if tuple(sorted(e)) in edges]
        deg = Counter(x for e in es for x in e)
        if len(es) == 4 and set(deg.values()) == {2}:
            faces.append(tuple(sorted(S)))
    return tuple(sorted(faces))


def build_result():
    points, lines = w33()
    pperm = matrix_point_perm(points, MULTIPLIER_TWO)
    lperm = induced_line_perm(lines, pperm)
    fixed = tuple(i for i, j in enumerate(pperm) if i == j)
    fixed_set = set(fixed)
    fixed_lines = tuple(i for i, j in enumerate(lperm) if i == j)
    assert len(fixed) == 8 and len(fixed_lines) == 6

    full_lines = tuple(sorted(tuple(sorted(lines[i])) for i in fixed_lines if set(lines[i]) <= fixed_set))
    assert len(full_lines) == 2
    A, B = full_lines
    assert len(A) == len(B) == 4 and set(A).isdisjoint(B) and set(A) | set(B) == fixed_set

    col = set()
    for L in lines:
        col.update(tuple(sorted(e)) for e in combinations(L, 2))
    fixed_col = {e for e in col if set(e) <= fixed_set}
    assert len(fixed_col) == 16
    cross = {e for e in fixed_col if (e[0] in A) != (e[1] in A)}
    assert len(cross) == 4
    deg = Counter(x for e in cross for x in e)
    assert all(deg[p] == 1 for p in fixed)

    cube_edges = {tuple(sorted(e)) for e in combinations(fixed, 2)} - fixed_col
    assert len(cube_edges) == 12
    match = {}
    for a in A:
        bs = [b for b in B if tuple(sorted((a, b))) in cross]
        assert len(bs) == 1
        match[a] = bs[0]
    even = ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0))
    label = {}
    for a, v in zip(A, even):
        label[a] = v
        label[match[a]] = tuple(1 - x for x in v)
    q3_edges = {
        tuple(sorted((a, b))) for a, b in combinations(fixed, 2)
        if hamming(label[a], label[b]) == 1
    }
    assert q3_edges == cube_edges
    faces = four_cycle_faces(fixed, cube_edges)
    assert len(faces) == 6

    spreads = enumerate_spreads(lines)
    sperm = induced_spread_perm(spreads, lperm)
    scycles = inv_cycles(sperm)
    assert len(spreads) == 36 and Counter(map(len, scycles)) == {1: 4, 2: 16}
    sid = {s: oi for oi, cyc in enumerate(scycles) for s in cyc}
    fixed_spreads = tuple(c[0] for c in scycles if len(c) == 1)
    four_edges = {
        tuple(sorted((a, b))) for a, b in combinations(range(36), 2)
        if len(set(spreads[a]) & set(spreads[b])) == 4
    }
    assert len(four_edges) == 270
    k4 = {tuple(sorted(e)) for e in combinations(fixed_spreads, 2)}
    assert len(k4) == 6 and k4 <= four_edges
    swapped_internal = {tuple(sorted(c)) for c in scycles if len(c) == 2 and tuple(sorted(c)) in four_edges}
    assert len(swapped_internal) == 6

    seen, edge_orbits = set(), []
    for e in sorted(four_edges):
        if e in seen:
            continue
        image = tuple(sorted((sperm[e[0]], sperm[e[1]])))
        orbit = tuple(sorted({e, image}))
        seen.update(orbit)
        edge_orbits.append(orbit)
    assert Counter(map(len, edge_orbits)) == {1: 12, 2: 129}
    buckets = defaultdict(list)
    fixed_types = Counter()
    for orb in edge_orbits:
        a, b = orb[0]
        qa, qb = sid[a], sid[b]
        key = tuple(sorted((qa, qb)))
        buckets[key].append(orb)
        if len(orb) == 1:
            fixed_types["loop_from_exchanged_spreads" if qa == qb else "edge_between_fixed_spreads"] += 1
    loops = [k for k in buckets if k[0] == k[1]]
    assert fixed_types == {"edge_between_fixed_spreads": 6, "loop_from_exchanged_spreads": 6}
    assert len(loops) == 6

    observer = build_observer()["n3_one_step_model"]
    stochastic = {
        r["macrostate"] for r in observer["rows"] if r["conditional_entropy_bits"] > 0
    }
    expected = {"1" + "".join(map(str, t)) for t in product((0, 1), repeat=3)}
    assert stochastic == expected

    # IMPORTANT repair: integer ids internally; stringify only for JSON below.
    fixed_to_observer = {p: "1" + "".join(map(str, label[p])) for p in fixed}
    assert set(fixed_to_observer.values()) == stochastic
    observer_q3 = {
        tuple(sorted((fixed_to_observer[a], fixed_to_observer[b]))) for a, b in cube_edges
    }
    expected_observer_q3 = {
        tuple(sorted((a, b))) for a, b in combinations(stochastic, 2)
        if hamming(a[1:], b[1:]) == 1
    }
    assert observer_q3 == expected_observer_q3

    q4 = json.loads((ROOT / "data" / "PART_W33_PASS5468_5475_SIMPLEX_STABILISER_IS_WF4.json").read_text(encoding="utf-8"))
    assert q4["pass_5470"]["knight_is_Q4"] and q4["pass_5470"]["vertices"] == 16 and q4["pass_5470"]["edges"] == 32
    observer_to_facet = {m: "0" + m[1:] for m in sorted(stochastic)}
    facet = set(observer_to_facet.values())
    facet_edges = {tuple(sorted((a, b))) for a, b in combinations(facet, 2) if hamming(a, b) == 1}
    assert len(facet) == 8 and len(facet_edges) == 12

    checks = {
        "outer_fixed_points_are_two_disjoint_four_point_lines": True,
        "fixed_collinearity_is_two_K4s_plus_perfect_matching": True,
        "fixed_collinearity_complement_is_explicit_Q3": q3_edges == cube_edges,
        "Q3_has_8_vertices_12_edges_6_square_faces": len(fixed) == 8 and len(cube_edges) == 12 and len(faces) == 6,
        "four_fixed_spreads_form_K4_in_four_intersection_graph": len(k4) == 6,
        "six_swapped_spread_orbits_are_internal_four_intersection_edges": len(swapped_internal) == 6,
        "spread_quotient_has_12_fixed_edge_orbits_split_6_plus_6": sum(fixed_types.values()) == 12,
        "stochastic_observer_sector_is_affine_F2_cubed": stochastic == expected,
        "fixed_Q3_is_explicitly_isomorphic_to_observer_affine_cube": observer_q3 == expected_observer_q3,
        "observer_cube_embeds_as_Q4_facet": len(facet_edges) == 12,
        "prior_temporal_router_certificate_says_knight_is_Q4": q4["pass_5470"]["knight_is_Q4"] is True,
    }

    return {
        "schema": "w33.outer-cube-observer-bridge.v2",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": "The outer involution exposes an intrinsic Q3 as complement(W33[Fix(D)]); the stochastic Schubert chart x0=1 is a second F2^3 cube, and an explicit gauge-fixed isomorphism welds both to a Q4 router facet.",
        "outer_fixed_cube": {
            "fixed_point_ids": list(fixed),
            "fully_fixed_line_ids": list(i for i in fixed_lines if set(lines[i]) <= fixed_set),
            "eigenspace_point_blocks": [list(A), list(B)],
            "W33_collinearity_edges_on_fixed_points": len(fixed_col),
            "cross_collinearity_perfect_matching": [list(e) for e in sorted(cross)],
            "complement_Q3_edges": [list(e) for e in sorted(cube_edges)],
            "Q3_bit_labels": {str(p): "".join(map(str, label[p])) for p in fixed},
            "Q3_square_faces": [["".join(map(str, label[p])) for p in f] for f in faces],
            "graph_identity": "complement(W33[Fix(D)]) = K4,4 - perfect_matching ~= Q3",
        },
        "spread_orbit_quotient": {
            "spread_orbit_count": len(scycles),
            "spread_orbit_size_histogram": {str(k): v for k, v in sorted(Counter(map(len, scycles)).items())},
            "fixed_spread_ids": list(fixed_spreads),
            "fixed_spread_K4_edges": [list(e) for e in sorted(k4)],
            "swapped_orbit_internal_edges": [list(e) for e in sorted(swapped_internal)],
            "four_intersection_edge_orbits": len(edge_orbits),
            "edge_orbit_size_histogram": {str(k): v for k, v in sorted(Counter(map(len, edge_orbits)).items())},
            "fixed_edge_types": dict(sorted(fixed_types.items())),
            "quotient_loop_count": len(loops),
            "quotient_underlying_edge_keys": len(buckets),
            "quotient_parallel_multiplicity_histogram": {str(k): v for k, v in sorted(Counter(len(v) for v in buckets.values()).items())},
            "lifted_edge_mass": sum(map(len, edge_orbits)),
            "reading": "Six fixed C6s are the K4 edges on four fixed spreads; six more are internal edges of spread 2-cycles and become quotient loops.",
        },
        "observer_affine_cube": {
            "stochastic_macrostates": sorted(stochastic),
            "projective_split": "PG(3,2) = AG(3,2) disjoint_union PG(2,2) = 8 + 7",
            "affine_chart": "x0=1; tail (x1,x2,x3) in F2^3",
            "fixed_point_to_observer_macrostate": {str(k): v for k, v in fixed_to_observer.items()},
            "observer_Q3_edges": [list(e) for e in sorted(observer_q3)],
            "dynamics_boundary": "Q3 is the coordinate/Hamming graph on the stochastic macrostates, not the support graph of all observer transitions.",
        },
        "Q4_facet_weld": {
            "prior_certificate": "data/PART_W33_PASS5468_5475_SIMPLEX_STABILISER_IS_WF4.json#pass_5470",
            "prior_Q4_vertices": 16,
            "prior_Q4_edges": 32,
            "observer_macrostate_to_Q4_facet_vertex": observer_to_facet,
            "facet_vertex_count": len(facet),
            "facet_edge_count": len(facet_edges),
        },
        "claim_boundary": [
            "The fixed-point Q3 is intrinsic after choosing the declared outer involution; its bit labels are not canonical.",
            "The observer Q3 uses the ordered Marcelis gauge and Hamming adjacency on AG(3,2).",
            "The cross-Q3 and Q4-facet welds are explicit combinatorial/controller dictionaries, not hidden-variable reductions of quantum mechanics.",
            "Quotient loops record exchanged spread endpoints and are not self-incidence in the original simple graph.",
        ],
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": r["status"],
        "fixed_graph": r["outer_fixed_cube"]["graph_identity"],
        "fixed_edge_types": r["spread_orbit_quotient"]["fixed_edge_types"],
        "parallel_hist": r["spread_orbit_quotient"]["quotient_parallel_multiplicity_histogram"],
        "observer_states": len(r["observer_affine_cube"]["stochastic_macrostates"]),
    }, indent=2, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
