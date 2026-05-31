#!/usr/bin/env python3
"""Canonicality of the Singer hexagon -> affine K4 completion.

This is the runnable fixed version of `w33_singer_hexagon_affine_completion_canonicality.py`.
The first version accidentally imported a non-exported helper before falling back
to `build_payload`; this version imports only the exported functions.

Previous verifier:
    The Singer quotient local-12 is natively the directed C6 side-codec of a
    reference Heawood hexagon. It becomes the affine directed-K4 codec only after
    completing the Fano triangle of point-vertices by the missing fourth affine
    point and choosing a cyclic orientation.

Main conclusions:
  1. For each hexagon, the set-level affine completion is canonical: the three
     Fano point vertices p,q,r determine the fourth affine point x=p+q+r.
  2. The seven completions are Singer-equivariant: applying the Singer generator
     to a hexagon sends its completion point to the completion point of the next
     hexagon.
  3. The directed C6 -> directed K4 bijection is not orientation-free. Reversing
     the cyclic orientation changes the pointwise bijection while preserving the
     same directed-K4 image set.
  4. The concrete toroidal rotation/Singer phase supplies a coherent orientation
     around all seven hexagons, making the seven local C6->K4 bijections
     Singer-equivariant.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from analysis.w33_concrete_singer_phase_cycles import (
    add3,
    apply_perm_to_cycle,
    build_payload as singer_build_payload,
    canonical_heawood,
    fano_line_from_pair,
)


def hex_point_vertices(hexagon, rev):
    return [v for v in hexagon if rev[v][0] == "P"]


def hex_line_vertices(hexagon, rev):
    return [v for v in hexagon if rev[v][0] == "L"]


def completion_point(hexagon, rev):
    pts = [rev[v][1] for v in hex_point_vertices(hexagon, rev)]
    assert len(pts) == 3
    return add3(add3(pts[0], pts[1]), pts[2])


def completion_affine_points(hexagon, rev):
    pts = [rev[v][1] for v in hex_point_vertices(hexagon, rev)]
    x = completion_point(hexagon, rev)
    return tuple(sorted(pts + [x]))


def hex_to_k4_bijection(hexagon, rev, orientation=1):
    """Build the oriented C6 side-codec -> directed K4-edge bijection."""
    h = tuple(hexagon if orientation == 1 else tuple(reversed(hexagon)))
    point_vertices = hex_point_vertices(h, rev)
    point_labels = {v: rev[v][1] for v in point_vertices}
    x = completion_point(h, rev)
    mapping = {}
    n = len(h)
    for i, lv in enumerate(h):
        if rev[lv][0] != "L":
            continue
        prev_v = h[(i - 1) % n]
        next_v = h[(i + 1) % n]
        assert rev[prev_v][0] == rev[next_v][0] == "P"
        p_prev = point_labels[prev_v]
        p_next = point_labels[next_v]
        third_v = next(v for v in point_vertices if v not in (prev_v, next_v))
        p_third = point_labels[third_v]
        assert rev[lv][1] == fano_line_from_pair(p_prev, p_next)
        mapping[(h, prev_v, lv)] = (p_prev, p_next)
        mapping[(h, next_v, lv)] = (p_next, p_prev)
        mapping[(h, lv, prev_v)] = (x, p_third)
        mapping[(h, lv, next_v)] = (p_third, x)
    return mapping


def canonical_directed_k4_edges(points):
    return {(a, b) for a in points for b in points if a != b}


def label_image_under_perm(label, gen, rev):
    source_vertex = next(i for i, item in rev.items() if item[0] == "P" and item[1] == label)
    target_vertex = gen[source_vertex]
    assert rev[target_vertex][0] == "P"
    return rev[target_vertex][1]


def transported_k4_edges(mapping, gen, target_hex, rev):
    out = {}
    for (_h, a, b), (u, v) in mapping.items():
        out[(target_hex, gen[a], gen[b])] = (label_image_under_perm(u, gen, rev), label_image_under_perm(v, gen, rev))
    return out


def reverse_orientation_mapping_relation(hexagon, rev):
    forward = hex_to_k4_bijection(hexagon, rev, orientation=1)
    reverse = hex_to_k4_bijection(hexagon, rev, orientation=-1)
    rev_hex = tuple(reversed(hexagon))
    reverse_normalized = {(hexagon, a, b): edge for (h, a, b), edge in reverse.items() if h == rev_hex}
    return {
        "same_image_edge_set": set(forward.values()) == set(reverse_normalized.values()),
        "pointwise_same": all(forward.get(k) == reverse_normalized.get(k) for k in forward),
        "pointwise_reversed_count": sum(1 for k, e in forward.items() if reverse_normalized.get(k) == (e[1], e[0])),
        "domain_size_forward": len(forward),
        "domain_size_reverse": len(reverse_normalized),
    }


def build_payload() -> dict:
    payload = singer_build_payload()
    gen = tuple(payload["selected_singer_generator"]["permutation_on_heawood_vertices"])
    system = tuple(tuple(c) for c in payload["base_toroidal_system"]["hexagons"])
    _pts, _lns, _idx, rev, _edges = canonical_heawood()

    hex_cycle = [tuple(c) for c in payload["selected_singer_generator"]["hexagon_cycle_cycles"]]
    if len(hex_cycle) != 7:
        h0 = system[0]
        hex_cycle = [h0]
        cur = h0
        for _ in range(6):
            cur = apply_perm_to_cycle(gen, cur)
            hex_cycle.append(cur)

    records = []
    for h in hex_cycle:
        cp = completion_point(h, rev)
        ap = completion_affine_points(h, rev)
        k4_edges = canonical_directed_k4_edges(ap)
        bij = hex_to_k4_bijection(h, rev, orientation=1)
        records.append({
            "hexagon": h,
            "point_vertices": [str(rev[v][1]) for v in hex_point_vertices(h, rev)],
            "line_vertices": [str(rev[v][1]) for v in hex_line_vertices(h, rev)],
            "completion_point": str(cp),
            "affine_completion": [str(x) for x in ap],
            "bijection_size": len(bij),
            "bijection_hits_all_directed_K4_edges": set(bij.values()) == k4_edges,
        })

    completion_equivariant = True
    bijection_equivariant = True
    for i, h in enumerate(hex_cycle):
        h_next = hex_cycle[(i + 1) % 7]
        if label_image_under_perm(completion_point(h, rev), gen, rev) != completion_point(h_next, rev):
            completion_equivariant = False
        transported = transported_k4_edges(hex_to_k4_bijection(h, rev, orientation=1), gen, h_next, rev)
        target = hex_to_k4_bijection(h_next, rev, orientation=1)
        if transported != target:
            bijection_equivariant = False

    reverse_relation = reverse_orientation_mapping_relation(hex_cycle[0], rev)
    completion_points = [r["completion_point"] for r in records]

    identities = {
        "seven_hexagons_in_singer_cycle": len(hex_cycle) == 7 and len(set(hex_cycle)) == 7,
        "completion_point_defined_for_each_hex": all(len(hex_point_vertices(h, rev)) == 3 and len(hex_line_vertices(h, rev)) == 3 for h in hex_cycle),
        "each_completion_gives_four_affine_points": all(len(set(r["affine_completion"])) == 4 for r in records),
        "each_oriented_bijection_hits_12_K4_edges": all(r["bijection_size"] == 12 and r["bijection_hits_all_directed_K4_edges"] for r in records),
        "completion_equivariant_under_singer": completion_equivariant,
        "oriented_bijection_equivariant_under_singer": bijection_equivariant,
        "orientation_reversal_changes_bijection_not_image_set": reverse_relation["same_image_edge_set"] and not reverse_relation["pointwise_same"],
        "completion_points_form_seven_point_cycle": len(set(completion_points)) == 7,
    }
    return {
        "theorem": "singer_hexagon_affine_completion_canonicality_fixed",
        "statement": "For each Singer hexagon, the affine completion point x=p+q+r is canonical and Singer-equivariant. The directed C6->K4 codec identification depends on a cyclic orientation, but the concrete Singer/toroidal phase supplies a coherent orientation making the bijections Singer-equivariant.",
        "hexagon_completion_records": records,
        "global_completion_summary": {
            "completion_points": completion_points,
            "completion_point_distribution": dict(Counter(completion_points)),
            "affine_completion_sets": [tuple(r["affine_completion"]) for r in records],
        },
        "equivariance": {
            "completion_equivariant_under_singer": completion_equivariant,
            "oriented_bijection_equivariant_under_singer": bijection_equivariant,
        },
        "orientation_dependence": reverse_relation,
        "interpretation": {
            "canonical_part": "The fourth affine point x=p+q+r is determined by the unordered set of three Fano point vertices of the hexagon; no orientation choice is needed.",
            "orientation_relative_part": "The bijection from directed C6 side-flags to directed K4 edges needs a cyclic orientation. Reversing the hexagon changes the pointwise bijection while preserving the same 12-edge image set.",
            "phase_resolution": "The concrete Singer generator gives a coherent cyclic orientation across all seven hexagons, so the seven local C6->K4 bridges are globally phase-compatible.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_singer_hexagon_affine_completion_canonicality_fixed.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
