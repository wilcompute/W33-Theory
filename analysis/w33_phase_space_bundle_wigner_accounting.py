#!/usr/bin/env python3
"""
Pass 62: the local qutrit phase spaces glue into one 360-state bundle, and the
local Wigner fuel has a concrete nine-point ledger.

Pass 61 proved that every defect center carries a local affine plane AG(2,3):
nine ground-state optima, twelve neighbor-lines, and four defect-line
parallel classes. This witness asks what happens when those forty local planes
are moved by the machine's projective runtime group.

  BUNDLE THEOREM. The nine ground states at one center generate a single
  360-state orbit under PSp(4,3): forty fibers times nine local phase points.
  The stabilizer of one ground has order 72, so the orbit-stabilizer count is
  25920/72 = 360. Its action on the full bundle has rank 15 with subdegrees
  [1,3,4,8,8,24x8,72,72]. This is the same fiber cardinality as the Gross/
  Hudson two-qutrit stabilizer atlas: 40 Lagrangian bases times 9 states.

  GLUING SPECTRUM. The bundle is not forty disconnected copies. Pairwise
  intersections of lit sets are governed by the relation between centers:
  same-center pairs all intersect in 5, collinear centers split at
  0,2,3,8, and non-collinear centers split at 1,2,4,6. This is the measured
  transport interface between local phase spaces.

  WIGNER ACCOUNTING. On each local nine-point plane, the qutrit Strange state
  has Wigner values {-1/3 once, +1/6 eight times}. Hence the local negative
  mass is 1/3, the positive mass is 4/3, the L1 norm is 5/3, and the mana is
  log(5/3). The affine symmetry can move the negative site to any of the nine
  local ground states; globally there are 360 possible negative-site placements
  on the bundle.

Honest scope: the 360-bundle, rank, subdegrees, and gluing spectrum are exact
finite computations. The Hudson atlas statement is a cardinal/fiber bridge to
the repo's committed two-qutrit Wigner atlas, not an explicit Hilbert-vector
labeling of every ground state. The Wigner table is the existing qutrit Gross
Wigner machinery applied to the local Hesse plane.
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_contextuality_is_the_fuel as fuel  # noqa: E402
import w33_ground_affine_plane as gap  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_tax_orbits as orb  # noqa: E402


def _center_of_lit(lit, lines):
    fails = [li for li, line in enumerate(lines) if sum(1 for p in line if p in lit) != 1]
    if len(fails) != 4:
        return None
    common = set(lines[fails[0]])
    for li in fails[1:]:
        common &= set(lines[li])
    return next(iter(common)) if len(common) == 1 else None


def _center_zero_ground_states():
    triads, nb, _ = gap.four_centric_triads(3)
    grounds = []
    for triad, common_perp in triads:
        if all(point in nb for point in common_perp):
            grounds.append(frozenset(set(triad) | (set(nb) - set(common_perp))))
    return grounds, triads, nb


def _affine_facts_from_grounds(grounds, nb, star, lines):
    unlits = [tuple(sorted(set(nb) - ground)) for ground in grounds]
    star_line = {}
    for li in star:
        for point in lines[li]:
            if point != 0:
                star_line[point] = li
    pair_ints = {
        len(set(a) & set(b)) for i, a in enumerate(unlits) for b in unlits[i + 1 :]
    }
    per_line = {count for count in Counter(point for unlit in unlits for point in unlit).values()}
    transversal = all(
        sorted(Counter(star_line[point] for point in unlit).values()) == [1, 1, 1, 1]
        for unlit in unlits
    )
    same_class = {
        sum(1 for unlit in unlits if u in unlit and v in unlit)
        for i, u in enumerate(sorted(nb))
        for v in sorted(nb)[i + 1 :]
        if star_line[u] == star_line[v]
    }
    diff_class = {
        sum(1 for unlit in unlits if u in unlit and v in unlit)
        for i, u in enumerate(sorted(nb))
        for v in sorted(nb)[i + 1 :]
        if star_line[u] != star_line[v]
    }
    lit_intersections = {
        len(a & b) for i, a in enumerate(grounds) for b in grounds[i + 1 :]
    }
    return {
        "q": 3,
        "n_grounds": len(grounds),
        "unlit_size": sorted({len(unlit) for unlit in unlits}),
        "pairwise_co_unlit": sorted(pair_ints),
        "line_size_on_grounds": sorted(per_line),
        "unlit_transversal_of_defect_lines": bool(transversal),
        "same_class_co_unlit": sorted(same_class),
        "diff_class_co_unlit": sorted(diff_class),
        "ground_lit_pairwise_intersection": sorted(lit_intersections),
    }


def _orbit(seeds, gens):
    orbit = set(seeds)
    frontier = list(seeds)
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = frozenset(g[i] for i in x)
                if y not in orbit:
                    orbit.add(y)
                    nxt.append(y)
        frontier = nxt
    return orbit


def _stabilizer_subdegrees(seed, orbit, group):
    stabilizer = [g for g in group if frozenset(g[i] for i in seed) == seed]
    ordered = sorted(orbit, key=lambda s: tuple(sorted(s)))
    index = {ground: i for i, ground in enumerate(ordered)}
    unvisited = set(range(len(ordered)))
    subdegrees = []
    while unvisited:
        start = next(iter(unvisited))
        seen = {start}
        frontier = [start]
        while frontier:
            nxt = []
            for x in frontier:
                for g in stabilizer:
                    image = frozenset(g[i] for i in ordered[x])
                    y = index[image]
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            frontier = nxt
        unvisited -= seen
        subdegrees.append(len(seen))
    return sorted(subdegrees), len(stabilizer)


def _gluing_spectrum(orbit, lines, adjacency):
    ordered = sorted(orbit, key=lambda s: tuple(sorted(s)))
    centers = {ground: _center_of_lit(ground, lines) for ground in ordered}
    spectrum = Counter()
    for i, left in enumerate(ordered):
        for right in ordered[i + 1 :]:
            ca, cb = centers[left], centers[right]
            if ca == cb:
                relation = "same"
            elif adjacency[ca][cb]:
                relation = "collinear"
            else:
                relation = "noncollinear"
            spectrum[(relation, len(left & right))] += 1
    rows = [
        {"relation": relation, "intersection": intersection, "count": count}
        for (relation, intersection), count in sorted(spectrum.items())
    ]
    return rows


def _wigner_accounting():
    _, operators = fuel.phase_point_operators()

    def state(vector):
        v = np.array(vector, complex)
        v = v / np.linalg.norm(v)
        return np.outer(v, v.conj())

    strange = fuel.wigner(state([0, 1, -1]), operators)
    stabilizer = fuel.wigner(state([1, 0, 0]), operators)
    values = {f"{q},{p}": round(float(value), 12) for (q, p), value in sorted(strange.items())}
    negatives = [site for site, value in values.items() if value < -1e-9]
    positives = [site for site, value in values.items() if value > 1e-9]
    l1_norm = sum(abs(float(value)) for value in strange.values())
    stabilizer_l1 = sum(abs(float(value)) for value in stabilizer.values())
    return {
        "phase_point_count": len(values),
        "values": values,
        "negative_sites": negatives,
        "positive_site_count": len(positives),
        "negative_mass": round(-sum(value for value in strange.values() if value < 0), 12),
        "positive_mass": round(sum(value for value in strange.values() if value > 0), 12),
        "l1_norm": round(l1_norm, 12),
        "mana_ln": round(math.log(l1_norm), 12),
        "expected_mana_ln_5_over_3": round(math.log(5 / 3), 12),
        "stabilizer_l1_norm": round(stabilizer_l1, 12),
        "statement": (
            "one local phase point carries Wigner value -1/3 and the other eight carry +1/6; "
            "the negative site can be moved to any local ground state by the affine symmetry"
        ),
    }


def build_certificate():
    pts, adjacency, lines, symplectic = audit._build(3)
    gens, group = orb.build_group(pts, symplectic)
    center0_grounds, triads, nb = _center_zero_ground_states()
    ground_orbit = _orbit(center0_grounds, gens)
    centers = [_center_of_lit(ground, lines) for ground in ground_orbit]
    fiber_sizes = sorted(Counter(centers).values())
    subdegrees, stabilizer_order = _stabilizer_subdegrees(center0_grounds[0], ground_orbit, group)
    spectrum = _gluing_spectrum(ground_orbit, lines, adjacency)

    star = [li for li, line in enumerate(lines) if 0 in line]
    facts = _affine_facts_from_grounds(center0_grounds, nb, star, lines)
    local_grounds = center0_grounds
    ok = (
        facts["n_grounds"] == 9
        and facts["unlit_size"] == [4]
        and facts["pairwise_co_unlit"] == [1]
        and facts["line_size_on_grounds"] == [3]
        and facts["unlit_transversal_of_defect_lines"]
        and facts["same_class_co_unlit"] == [0]
        and facts["diff_class_co_unlit"] == [1]
    )
    local_intersections = sorted(
        {len(a & b) for i, a in enumerate(local_grounds) for b in local_grounds[i + 1 :]}
    )
    all_centers = sorted(set(centers)) == list(range(len(pts)))
    wigner = _wigner_accounting()

    checks = [
        ("center_0_has_9_ground_states", len(center0_grounds) == 9),
        ("ground_orbit_has_360_states", len(ground_orbit) == 360),
        ("bundle_has_40_fibers_of_9", all_centers and fiber_sizes == [9] * 40),
        ("stabilizer_order_72", stabilizer_order == 72),
        ("rank_15_subdegree_profile", len(subdegrees) == 15 and subdegrees == [1, 3, 4, 8, 8, 24, 24, 24, 24, 24, 24, 24, 24, 72, 72]),
        ("local_affine_plane_still_ok", ok and facts["n_grounds"] == 9),
        ("local_ground_sets_are_equidistant_5", local_intersections == [5]),
        ("wigner_has_one_negative_site", len(wigner["negative_sites"]) == 1),
        ("wigner_l1_is_5_over_3", abs(wigner["l1_norm"] - 5 / 3) < 1e-9),
    ]
    all_ok = all(ok for _, ok in checks)
    return {
        "pass": 62,
        "title": "Global qutrit phase-space bundle and Wigner fuel accounting",
        "bundle": {
            "group_order_on_points": len(group),
            "seed_center_ground_count": len(center0_grounds),
            "orbit_size": len(ground_orbit),
            "fiber_count": len(set(centers)),
            "fiber_sizes": fiber_sizes,
            "stabilizer_order": stabilizer_order,
            "rank_on_bundle": len(subdegrees),
            "subdegrees": subdegrees,
            "hudson_atlas_cardinality": {
                "lagrangian_bases": 40,
                "states_per_lagrangian": 9,
                "total_stabilizer_states": 360,
                "bridge_scope": "cardinal and fiber law; no explicit Hilbert-vector labeling claimed",
            },
        },
        "local_affine_plane": {
            "center_0_ground_count": len(local_grounds),
            "local_pair_intersections": local_intersections,
            "four_centric_triads": len(triads),
            "affine_plane_checks": facts,
        },
        "gluing_spectrum": spectrum,
        "wigner_accounting": {
            **wigner,
            "local_negative_site_choices": 9,
            "global_negative_site_choices": len(ground_orbit),
            "tax_vs_wigner_meters": (
                "the contextuality tax is 4/40 = 1/10 of contexts; the local Wigner "
                "fuel is one negative phase point of mass 1/3 with L1 norm 5/3"
            ),
        },
        "checks": [{"name": name, "pass": bool(ok)} for name, ok in checks],
        "all_pass": bool(all_ok),
        "summary": (
            "Pass 62 glues the forty local AG(2,3) tax planes into one 360-state bundle: "
            "40 centers times 9 grounds, a single PSp(4,3) orbit with stabilizer order 72, "
            "rank 15, and subdegrees [1,3,4,8,8,24x8,72,72]. The gluing spectrum records how "
            "lit-set intersections depend on center relation: same-center pairs have intersection "
            "5; collinear centers split at 0,2,3,8; non-collinear centers split at 1,2,4,6. "
            "This has the same fiber cardinality as the two-qutrit Hudson stabilizer atlas "
            "(40 Lagrangian bases times 9 states). Locally, the qutrit Strange-state Wigner table "
            "has one value -1/3 and eight values +1/6, giving negative mass 1/3, L1 norm 5/3, "
            "and mana log(5/3); the negative site can be placed on any local ground, hence 360 "
            "global negative-site placements. Honest: exact finite bundle computation; Hudson "
            "statement is cardinal/fiber, not an explicit Hilbert-vector labeling."
        ),
        "sources": [
            "analysis/w33_ground_affine_plane.py (Pass 61 local AG(2,3) law)",
            "analysis/w33_tax_orbits.py (PSp(4,3) point action and 360-orbit seed)",
            "analysis/w33_contextuality_is_the_fuel.py (Gross qutrit Wigner machinery and Strange state)",
        ],
    }


def main():
    cert = build_certificate()
    print("== Pass 62: global phase-space bundle and Wigner fuel accounting ==\n")
    for check in cert["checks"]:
        print(f"  [{'PASS' if check['pass'] else 'FAIL'}]  {check['name']}")
    print("\n[bundle]")
    print(
        "  orbit size {orbit_size} = {fiber_count} fibers x 9; stabilizer {stabilizer_order}; "
        "rank {rank_on_bundle}".format(**cert["bundle"])
    )
    print(f"  subdegrees: {cert['bundle']['subdegrees']}")
    print("\n[gluing spectrum]")
    for row in cert["gluing_spectrum"]:
        print(f"  {row['relation']:12s} intersection {row['intersection']}: {row['count']}")
    wigner = cert["wigner_accounting"]
    print("\n[Wigner accounting]")
    print(
        f"  negative sites {wigner['negative_sites']}; positive sites {wigner['positive_site_count']}; "
        f"L1 {wigner['l1_norm']}; mana {wigner['mana_ln']}"
    )
    print("\n" + cert["summary"])
    with open("data/w33_phase_space_bundle_wigner_accounting.json", "w") as fh:
        json.dump(cert, fh, indent=2)
    print("\nwrote data/w33_phase_space_bundle_wigner_accounting.json")
    return 0 if cert["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
