#!/usr/bin/env python3
"""Affine-completion atlases across the eight Singer/Sylow toroidal systems.

Previous result:
    For one concrete Singer/toroidal system, every Heawood hexagon has a
    canonical affine completion x=p+q+r, and the seven completions are
    Singer-equivariant.

This verifier globalizes that test across all eight toroidal seven-hexagon
systems in the Heawood orbit.

Questions tested:
  1. Does every one of the eight systems produce seven canonical affine
     completions?  Yes.
  2. Are the completion atlases the same for all eight systems, or different?
  3. How do they transform under GL(3,2) and under the Singer/Sylow assignment?

Key interpretation:
    A toroidal system is a Singer/Sylow phase choice.  Its seven hexagons each
    canonically complete a Fano triangle to an AG(2,2) chart.  The set of seven
    completions is an atlas invariant of that phase choice, and the eight atlases
    are permuted equivariantly by GL(3,2).
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

from analysis.w33_heawood_eight_systems_singer_sylow import (
    apply_perm_to_system,
    canonical_heawood,
    canonical_system,
    cyclic_subgroup,
    dual_edges,
    find_dual_to_heawood_isomorphism,
    heawood_collineations,
    orient_faces,
    perm_order,
    stabilizer,
    system_sylow7,
    dual_hexagons,
    FACES_UNORIENTED,
)
from analysis.w33_singer_hexagon_affine_completion_canonicality_fixed import (
    add3,
    completion_affine_points,
    completion_point,
)


def atlas_for_system(system, rev):
    records = []
    for h in system:
        cp = completion_point(h, rev)
        ap = completion_affine_points(h, rev)
        records.append({
            "hexagon": h,
            "completion_point": cp,
            "affine_completion": ap,
        })
    return tuple(sorted((r["hexagon"], r["completion_point"], r["affine_completion"]) for r in records))


def atlas_signature(atlas):
    # Forget the actual hexagon cycle ordering; keep the multiset of completion charts.
    return tuple(sorted((cp, ap) for _h, cp, ap in atlas))


def label_tuple_vecs(obj):
    if isinstance(obj, tuple) and obj and isinstance(obj[0], tuple):
        return tuple(str(x) for x in obj)
    return str(obj)


def build_payload() -> dict:
    pts, lns, idx, rev, he_edges = canonical_heawood()
    colls = heawood_collineations()
    oriented = orient_faces(FACES_UNORIENTED)
    iso = find_dual_to_heawood_isomorphism(dual_edges())
    base_dual = canonical_system(list(dual_hexagons(oriented).values()))
    base = canonical_system([[iso[x] for x in cyc] for cyc in base_dual])
    systems = sorted({apply_perm_to_system(g, base) for g in colls})

    atlases = {s: atlas_for_system(s, rev) for s in systems}
    signatures = {s: atlas_signature(a) for s, a in atlases.items()}
    unique_signatures = sorted(set(signatures.values()))

    # Sylow/Singer labels for systems.
    sylow_labels = {}
    for s in systems:
        stab = stabilizer(colls, s)
        sylow_labels[s] = system_sylow7(stab)

    # Equivariance: atlas(gS) == g atlas(S), interpreted by direct recomputation.
    # Since completion is defined by Fano point labels and g is a Heawood collineation,
    # compare by applying g to hexagons and to completion point labels via rev.
    def point_label_image(label, g):
        source = next(i for i, item in rev.items() if item[0] == "P" and item[1] == label)
        target = g[source]
        assert rev[target][0] == "P"
        return rev[target][1]

    equivariance_failures = 0
    signature_equivariance_failures = 0
    for g in colls:
        for s in systems:
            gs = apply_perm_to_system(g, s)
            transported_records = []
            for h, cp, ap in atlases[s]:
                gh = tuple(sorted([g[x] for x in h]))  # not cycle-canonical; used only for signature below
                gcp = point_label_image(cp, g)
                gap = tuple(sorted(point_label_image(x, g) for x in ap))
                transported_records.append((gcp, gap))
            transported_sig = tuple(sorted(transported_records))
            if transported_sig != signatures[gs]:
                signature_equivariance_failures += 1
                break
        if signature_equivariance_failures:
            break

    system_records = []
    for i, s in enumerate(systems):
        sig = signatures[s]
        completion_points = [cp for cp, _ap in sig]
        completion_point_counts = Counter(completion_points)
        affine_sets = [ap for _cp, ap in sig]
        point_membership = Counter(x for ap in affine_sets for x in ap)
        system_records.append({
            "system_index": i,
            "system": s,
            "signature_index": unique_signatures.index(sig),
            "completion_points": [str(x) for x in completion_points],
            "completion_point_distribution": {str(k): v for k, v in completion_point_counts.items()},
            "affine_completion_sets": [[str(x) for x in ap] for ap in affine_sets],
            "point_membership_in_affine_sets": {str(k): v for k, v in point_membership.items()},
            "sylow7_size": len(sylow_labels[s]),
        })

    signature_records = []
    for i, sig in enumerate(unique_signatures):
        systems_with_sig = [s for s in systems if signatures[s] == sig]
        point_membership = Counter(x for _cp, ap in sig for x in ap)
        signature_records.append({
            "signature_index": i,
            "system_count": len(systems_with_sig),
            "completion_points": [str(cp) for cp, _ap in sig],
            "affine_completion_sets": [[str(x) for x in ap] for _cp, ap in sig],
            "point_membership_distribution": dict(Counter(point_membership.values())),
        })

    identities = {
        "eight_systems": len(systems) == 8,
        "each_system_has_seven_completion_records": all(len(atlases[s]) == 7 for s in systems),
        "completion_points_are_seven_fano_points_each_system": all(len(set(cp for cp, _ap in signatures[s])) == 7 for s in systems),
        "each_affine_completion_has_four_points": all(len(ap) == 4 for sig in signatures.values() for _cp, ap in sig),
        "sylow_label_eight_distinct": len(set(sylow_labels.values())) == 8,
        "signature_equivariant_under_collineations": signature_equivariance_failures == 0,
        # Do not assume unique signatures: this is an empirical output.
    }

    return {
        "theorem": "eight_system_affine_completion_atlas",
        "statement": "Each of the eight Singer/Sylow toroidal systems has seven canonical affine completions. These completion atlases are permuted equivariantly by GL(3,2), and each system is still labeled by its unique Sylow-7/Singer subgroup.",
        "counts": {
            "systems": len(systems),
            "unique_atlas_signatures": len(unique_signatures),
            "signature_equivariance_failures": signature_equivariance_failures,
        },
        "system_records": system_records,
        "signature_records": signature_records,
        "interpretation": {
            "canonicality": "Every hexagon in every toroidal system canonically determines an AG(2,2) completion by x=p+q+r.",
            "phase_dependence": "The atlas belongs to the chosen Singer/Sylow toroidal phase system; GL(3,2) transports both system and atlas equivariantly.",
            "open_reading": "The number of distinct atlas signatures tells whether all eight Singer systems share one completion-atlas type or split into multiple atlas types; the data file records the exact classification.",
        },
        "identities": identities,
        "all_required_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_eight_system_affine_completion_atlas.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
