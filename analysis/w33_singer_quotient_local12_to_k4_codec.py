#!/usr/bin/env python3
"""Singer quotient local-12 versus affine K4 codec.

Previous theorem extracted a concrete Singer C7 phase for the Csaszar/Szilassi
system and showed:

    84 directed hexagon-edge flags = 12 orbits of length 7.

This verifier identifies the 12 quotient states more precisely.

Main points:
  1. A reference Szilassi hexagon is a cross-section for the Singer action: each
     of the 12 Singer flag orbits meets it exactly once.
  2. Natively, the quotient 12 is the directed-edge/side codec of one Heawood
     hexagon C6: six boundary incidences times two directions.
  3. This native C6 codec is not the same graph as the affine K4 directed-edge
     codec.  They share the abstract form 6 carriers * 2 orientations, but their
     endpoint graphs differ: C6 has six degree-2 endpoints, K4 has four degree-3
     endpoints.
  4. A reference Heawood hexagon is a Fano triangle: three Fano points and their
     three pairwise joining Fano lines.  Adding the missing fourth affine point
     x=p+q+r completes it to AG(2,2).  After choosing the cyclic orientation of
     the hexagon, there is a natural bijection from the 12 directed hexagon
     flags to the 12 directed K4 edges.

So the correct statement is:
    Singer quotient local-12 is canonically a directed C6 side-codec.  It becomes
    the affine directed-K4 codec only after choosing the Fano-triangle completion
    and cyclic orientation supplied by the reference hexagon.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from analysis.w33_concrete_singer_phase_cycles import (
    build_payload as singer_payload,
    flag_orbits,
    flags_for_system,
    fano_line_from_pair,
    add3,
)


def canonical_directed_k4_edges(points):
    return {(a, b) for a in points for b in points if a != b}


def local_hex_directed_flags(hexagon):
    out = set()
    n = len(hexagon)
    for i in range(n):
        a, b = hexagon[i], hexagon[(i + 1) % n]
        out.add((hexagon, a, b))
        out.add((hexagon, b, a))
    return out


def endpoint_degree_directed_edges(edges):
    deg = Counter()
    undirected = set()
    for a, b in edges:
        deg[a] += 1
        undirected.add(tuple(sorted((a, b))))
    return deg, undirected


def build_hex_to_k4_bijection(ref_hex, rev):
    """Map directed Heawood hex flags on one Fano triangle to directed K4 edges.

    The reference hexagon alternates point-line-point-line-... .  Its three point
    vertices are a Fano triangle.  The missing affine point x is the F2-sum of
    those three point labels.  For each Fano line side L connecting consecutive
    triangle points p_i -> p_{i+1}, the two directed point-to-line flags map to
    the two directed triangle edges.  The two directed line-to-point flags map to
    the two directed edges in the parallel complementary pair through x.
    """
    point_vertices = [v for v in ref_hex if rev[v][0] == "P"]
    line_vertices = [v for v in ref_hex if rev[v][0] == "L"]
    point_labels = {v: rev[v][1] for v in point_vertices}
    line_labels = {v: rev[v][1] for v in line_vertices}
    missing = add3(add3(point_labels[point_vertices[0]], point_labels[point_vertices[1]]), point_labels[point_vertices[2]])
    k4_points = sorted(list(point_labels.values()) + [missing])

    # For each line vertex, find the two adjacent point vertices in the cyclic hexagon.
    n = len(ref_hex)
    mapping = {}
    for i, lv in enumerate(ref_hex):
        if rev[lv][0] != "L":
            continue
        prev_v = ref_hex[(i - 1) % n]
        next_v = ref_hex[(i + 1) % n]
        assert rev[prev_v][0] == rev[next_v][0] == "P"
        p_prev = point_labels[prev_v]
        p_next = point_labels[next_v]
        third_v = next(v for v in point_vertices if v not in (prev_v, next_v))
        p_third = point_labels[third_v]
        # Check this Heawood line is exactly the Fano join of adjacent points.
        assert line_labels[lv] == fano_line_from_pair(p_prev, p_next)
        # Point->line gives the directed triangle side.
        mapping[(ref_hex, prev_v, lv)] = (p_prev, p_next)
        mapping[(ref_hex, next_v, lv)] = (p_next, p_prev)
        # Line->point gives the complementary parallel edge through the missing point.
        mapping[(ref_hex, lv, prev_v)] = (missing, p_third)
        mapping[(ref_hex, lv, next_v)] = (p_third, missing)
    return mapping, k4_points, missing


def build_payload() -> dict:
    p = singer_payload()
    gen = tuple(p["selected_singer_generator"]["permutation_on_heawood_vertices"])
    system = tuple(tuple(c) for c in p["base_toroidal_system"]["hexagons"])
    # Reconstruct label dictionary from previous payload labels.
    # Easier: parse from concrete payload's point/line labels by importing canonical data indirectly through records.
    # The selected payload does not expose rev directly, so rebuild from labels present in hexagon_records.
    from analysis.w33_concrete_singer_phase_cycles import canonical_heawood
    _pts, _lns, _idx, rev, _edges = canonical_heawood()

    orbits = flag_orbits(gen, system)
    ref_hex = system[0]
    cross_section = []
    for orb in orbits:
        hits = [f for f in orb if f[0] == ref_hex]
        cross_section.append(hits)

    local_flags = local_hex_directed_flags(ref_hex)
    cross_flags = {hits[0] for hits in cross_section if len(hits) == 1}

    # Native C6 directed-edge structure.
    c6_edges = {(a, b) for _h, a, b in local_flags}
    c6_deg, c6_undir = endpoint_degree_directed_edges(c6_edges)

    # Abstract K4 directed-edge structure from affine completion of the Fano triangle.
    bijection, k4_points, missing = build_hex_to_k4_bijection(ref_hex, rev)
    k4_edges = canonical_directed_k4_edges(k4_points)
    image_edges = set(bijection.values())
    k4_deg, k4_undir = endpoint_degree_directed_edges(k4_edges)

    # Carrier-level comparison: both have 6 unoriented carriers and reversal involution.
    carrier_match = len(c6_undir) == len(k4_undir) == 6 and len(c6_edges) == len(k4_edges) == 12
    native_graph_degree_distributions = {
        "C6_endpoint_outdegree_distribution": dict(Counter(c6_deg.values())),
        "K4_endpoint_outdegree_distribution": dict(Counter(k4_deg.values())),
    }

    identities = {
        "singer_orbits_12_size7": len(orbits) == 12 and set(len(o) for o in orbits) == {7},
        "reference_hex_cross_section_once_each": all(len(hits) == 1 for hits in cross_section) and len(cross_flags) == 12,
        "cross_section_equals_local_hex_flags": cross_flags == local_flags,
        "native_local_codec_is_directed_C6": len(c6_edges) == 12 and len(c6_undir) == 6 and dict(Counter(c6_deg.values())) == {2: 6},
        "k4_codec_has_12_directed_edges": len(k4_edges) == 12 and len(k4_undir) == 6 and dict(Counter(k4_deg.values())) == {3: 4},
        "native_C6_not_graph_isomorphic_to_K4_by_degree": dict(Counter(c6_deg.values())) != dict(Counter(k4_deg.values())),
        "hex_to_k4_bijection_after_affine_completion": len(bijection) == 12 and image_edges == k4_edges,
        "carrier_level_6_times_2_match": carrier_match,
    }

    return {
        "theorem": "singer_quotient_local12_to_k4_codec",
        "statement": "The Singer quotient of the 84 flags is natively the 12 directed side-flags of a reference Heawood hexagon. This local C6 codec is not intrinsically the same as the affine K4 directed-edge codec, but a reference Fano-triangle completion gives a bijection between them.",
        "singer_quotient": {
            "orbit_count": len(orbits),
            "orbit_size_distribution": dict(Counter(len(o) for o in orbits)),
            "reference_hexagon": ref_hex,
            "cross_section_size": len(cross_flags),
            "sample_cross_section_flags": [(str(f[0]), f[1], f[2]) for f in sorted(cross_flags)[:12]],
        },
        "native_C6_codec": {
            "directed_edges": sorted(c6_edges),
            "directed_edge_count": len(c6_edges),
            "undirected_carriers": sorted(c6_undir),
            "endpoint_degree_distribution": dict(Counter(c6_deg.values())),
        },
        "affine_K4_completion": {
            "triangle_point_labels": [str(rev[v][1]) for v in ref_hex if rev[v][0] == "P"],
            "missing_fourth_affine_point": str(missing),
            "k4_points": [str(x) for x in k4_points],
            "directed_edge_count": len(k4_edges),
            "endpoint_degree_distribution": dict(Counter(k4_deg.values())),
            "bijection_sample": {str(k): str(v) for k, v in list(bijection.items())[:12]},
        },
        "comparison": {
            "shared_abstract_form": "both are 6 carriers times 2 orientations/sides",
            "native_difference": "C6 endpoint graph has six degree-2 vertices; K4 endpoint graph has four degree-3 vertices",
            "correct_bridge": "a Fano-triangle affine completion plus cyclic orientation turns the local C6 side-codec into the affine K4 directed-edge codec by a bijection, not by native graph equality",
            "degree_distributions": native_graph_degree_distributions,
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_singer_quotient_local12_to_k4_codec.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
