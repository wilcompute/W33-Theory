#!/usr/bin/env python3
"""C7-equivariant 84-state bridge from the PG(2,4) observer boundary to toroidal flags.

The affine/Fano horizon exposed the exact denominator

    84 = 4 * |PG(2,4)| = 4 * 21.

Earlier repo work independently constructed:

    84 toroidal flags = 12 Singer phases * 7 Singer steps,

and identified the local quotient 12 with the directed-edge codec of K4 after
a Fano-triangle affine completion.

This certificate closes that gap constructively.

1. Find a projective Singer cycle C21 acting regularly on PG(2,4).
2. Its C7 subgroup has exactly three orbits on the 21 boundary points.
3. Add one GF(4) anchor label a in the four-element additive group.  The resulting
   boundary codec has 21*4=84 states and twelve C7-orbits.
4. The quotient labels are

       (a,d) in GF(4) x GF(4)^*,

   because C21/C7 ~= C3 ~= GF(4)^*.  Map (a,d) to the directed K4 edge

       a -> a+d.

   These 12 labels are exactly AGL(1,4), which acts sharply transitively on the
   12 directed edges of K4 and is isomorphic to A4.
5. Use the repo's concrete Singer-toroidal system and its local C6->K4 completion
   to match each quotient edge to one toroidal local flag, then lift the map
   around the C7 orbit.  This gives an explicit C7-equivariant bijection between
   all 84 boundary-codec states and all 84 toroidal flags.

The A4 quotient also matches the independently certified derived image

    H'/Z(H) ~= A4

of the order-96 Heawood cube-symmetry cover.

Choice boundary: a Singer generator, an orbit phase origin, and the affine K4
coordinate gauge are declared.  The result is an explicit equivariant codec,
not a claim that the identification is canonical under the full ambient groups.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
for p in (str(ROOT), str(ANALYSIS)):
    if p not in sys.path:
        sys.path.insert(0, p)

from w33_marcelis_gf4_trace_gauge import (  # noqa: E402
    canon_first_one,
    gf4_add,
    gf4_mul,
)
from w33_marcelis_observer_quotient_dynamics import projective_points  # noqa: E402
from w33_concrete_singer_phase_cycles import (  # noqa: E402
    apply_perm_to_flag,
    build_payload as toroidal_singer_payload,
    canonical_heawood,
    flags_for_system,
    perm_power,
)
from w33_singer_quotient_local12_to_k4_codec import build_hex_to_k4_bijection  # noqa: E402

OUT = ROOT / "data" / "w33_boundary_singer_toroidal_84_bridge.json"


def mat_vec3(M, v):
    out = []
    for r in range(3):
        x = 0
        for c in range(3):
            x = gf4_add(x, gf4_mul(M[r][c], v[c]))
        out.append(x)
    return tuple(out)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def perm_power_local(p, n):
    out = tuple(range(len(p)))
    for _ in range(n):
        out = compose(p, out)
    return out


def perm_order(p):
    e = tuple(range(len(p)))
    x = e
    for n in range(1, 1000):
        x = compose(p, x)
        if x == e:
            return n
    raise AssertionError("order bound exceeded")


def orbit(p, start):
    out = [start]
    cur = p[start]
    while cur != start:
        out.append(cur)
        cur = p[cur]
        if len(out) > len(p):
            raise AssertionError("bad orbit")
    return out


def projective_perm(points, M):
    index = {p: i for i, p in enumerate(points)}
    return tuple(index[canon_first_one(mat_vec3(M, p))] for p in points)


def find_singer21(points):
    # Search the 48 companion forms with nonzero constant term.  This avoids a
    # large GL(3,4) scan while still verifies the resulting action directly.
    hits = []
    for a0 in (1, 2, 3):
        for a1 in range(4):
            for a2 in range(4):
                M = ((0, 0, a0), (1, 0, a1), (0, 1, a2))
                p = projective_perm(points, M)
                if perm_order(p) == 21 and len(orbit(p, 0)) == 21:
                    hits.append((M, p))
    assert hits
    return min(hits, key=lambda item: item[0]), len(hits)


def gf4_pow_omega(k):
    x = 1
    for _ in range(k % 3):
        x = gf4_mul(2, x)
    return x


def perm_parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) & 1


def agl14_certificate():
    elems = {}
    for a in range(4):
        for d in (1, 2, 3):
            perm = tuple(gf4_add(gf4_mul(d, x), a) for x in range(4))
            elems[(a, d)] = perm
    assert len(set(elems.values())) == 12
    assert all(perm_parity(p) == 0 for p in elems.values())

    edge_image = {
        key: (p[0], p[1])
        for key, p in elems.items()
    }
    all_directed = {(a, b) for a in range(4) for b in range(4) if a != b}
    assert set(edge_image.values()) == all_directed
    assert len(set(edge_image.values())) == 12

    order_hist = Counter(perm_order(p) for p in elems.values())
    assert order_hist == {1: 1, 2: 3, 3: 8}
    return elems, edge_image, order_hist


def stringify_flag(flag):
    h, a, b = flag
    return {"hexagon": list(h), "from": a, "to": b}


def build_result() -> dict:
    boundary_points = projective_points(2)
    assert len(boundary_points) == 21
    (singer_matrix, g21), singer_companion_hits = find_singer21(boundary_points)
    assert perm_order(g21) == 21
    full_cycle = orbit(g21, 0)
    assert len(full_cycle) == 21
    exponent_of = {idx: k for k, idx in enumerate(full_cycle)}

    g7 = perm_power_local(g21, 3)
    assert perm_order(g7) == 7
    c7_orbits = []
    unseen = set(range(21))
    while unseen:
        start = min(unseen)
        o = orbit(g7, start)
        c7_orbits.append(tuple(o))
        unseen -= set(o)
    assert len(c7_orbits) == 3 and set(map(len, c7_orbits)) == {7}

    # Quotient coordinates.  If p=g21^k p0 then k mod 3 indexes the three C7
    # orbits.  Identify those residues with 1,omega,omega^2 in GF(4)^*.
    residue_direction = {r: gf4_pow_omega(r) for r in range(3)}
    assert set(residue_direction.values()) == {1, 2, 3}
    boundary_states = [(i, a) for i in range(21) for a in range(4)]
    assert len(boundary_states) == 84
    quotient_edge = {}
    quotient_key = {}
    for i, a in boundary_states:
        k = exponent_of[i]
        r = k % 3
        d = residue_direction[r]
        quotient_key[(i, a)] = (r, a)
        quotient_edge[(i, a)] = (a, gf4_add(a, d))
    assert len(set(quotient_key.values())) == 12
    assert set(quotient_edge.values()) == {(a, b) for a in range(4) for b in range(4) if a != b}

    agl, agl_edge, agl_order_hist = agl14_certificate()
    # (a,d) as affine map x->d*x+a sends the reference directed edge 0->1 to
    # a->a+d, exactly our quotient-edge coordinate.
    assert {agl_edge[(a, d)] for a in range(4) for d in (1, 2, 3)} == set(quotient_edge.values())

    # Concrete toroidal Singer system.
    tor = toroidal_singer_payload()
    assert tor["all_identities_hold"]
    tor_gen = tuple(tor["selected_singer_generator"]["permutation_on_heawood_vertices"])
    system = tuple(tuple(c) for c in tor["base_toroidal_system"]["hexagons"])
    ref_hex = system[0]
    all_toroidal_flags = flags_for_system(system)
    assert len(all_toroidal_flags) == 84

    _pts, _lns, _idx, rev, _edges = canonical_heawood()
    local_to_k4, k4_points, missing = build_hex_to_k4_bijection(ref_hex, rev)
    assert len(local_to_k4) == 12

    # Choose an affine F2^2~=GF(4) coordinate on the completed K4.  The missing
    # fourth point is origin; the three triangle points are mapped in their
    # cyclic order to 1,omega,omega^2.  Any such choice is an affine isomorphism;
    # recording it makes the gauge explicit.
    point_vertices = [v for v in ref_hex if rev[v][0] == "P"]
    point_labels = [rev[v][1] for v in point_vertices]
    assert len(point_labels) == 3 and missing not in point_labels
    k4_to_gf4 = {missing: 0}
    for lab, value in zip(point_labels, (1, 2, 3)):
        k4_to_gf4[lab] = value
    assert set(k4_to_gf4) == set(k4_points)
    assert set(k4_to_gf4.values()) == {0, 1, 2, 3}

    local_flag_to_edge = {
        flag: (k4_to_gf4[u], k4_to_gf4[v])
        for flag, (u, v) in local_to_k4.items()
    }
    assert len(local_flag_to_edge) == 12
    assert set(local_flag_to_edge.values()) == {(a, b) for a in range(4) for b in range(4) if a != b}
    edge_to_local_flag = {edge: flag for flag, edge in local_flag_to_edge.items()}
    assert len(edge_to_local_flag) == 12

    # Full 84-state equivariant lift.  Write exponent k=r+3m.  The quotient
    # edge chooses one local flag on the reference hexagon; m Singer steps lift
    # it to the matching toroidal flag.
    bridge = {}
    for state in boundary_states:
        i, a = state
        k = exponent_of[i]
        r = k % 3
        m = (k - r) // 3
        assert 0 <= m < 7
        edge = quotient_edge[state]
        f0 = edge_to_local_flag[edge]
        fm = apply_perm_to_flag(perm_power(tor_gen, m), f0, system)
        assert fm in all_toroidal_flags
        bridge[state] = fm
    assert len(bridge) == 84
    assert len(set(bridge.values())) == 84
    assert set(bridge.values()) == all_toroidal_flags

    # C7 equivariance is checked on every boundary state.
    equivariance_checks = 0
    for i, a in boundary_states:
        lhs = bridge[(g7[i], a)]
        rhs = apply_perm_to_flag(tor_gen, bridge[(i, a)], system)
        assert lhs == rhs
        equivariance_checks += 1
    assert equivariance_checks == 84

    # Twelve C7 orbits on each side.
    boundary_orbits = defaultdict(set)
    for state, key in quotient_key.items():
        boundary_orbits[key].add(state)
    assert len(boundary_orbits) == 12 and set(map(len, boundary_orbits.values())) == {7}

    central = json.loads((ROOT / "data" / "w33_stabilizer96_cube_central_cover.json").read_text(encoding="utf-8"))
    assert central["status"] == "PASS"
    assert "A4" in central["Heawood_stabilizer_cover"]["derived_image"]

    checks = {
        "pg24_boundary_has_21_points": len(boundary_points) == 21,
        "projective_singer_C21_regular": perm_order(g21) == 21 and len(full_cycle) == 21,
        "C7_subgroup_has_three_seven_cycles": len(c7_orbits) == 3 and set(map(len, c7_orbits)) == {7},
        "boundary_codec_has_84_states": len(boundary_states) == 84,
        "boundary_C7_quotient_has_12_states": len(boundary_orbits) == 12,
        "quotient_is_all_directed_K4_edges": set(quotient_edge.values()) == {(a, b) for a in range(4) for b in range(4) if a != b},
        "AGL14_is_A4_even_order12": len(set(agl.values())) == 12 and all(perm_parity(p) == 0 for p in agl.values()),
        "AGL14_sharply_transitive_on_directed_K4_edges": len(set(agl_edge.values())) == 12,
        "toroidal_flags_84": len(all_toroidal_flags) == 84,
        "full_bridge_is_bijection": len(bridge) == len(set(bridge.values())) == 84,
        "full_bridge_is_C7_equivariant_on_all_states": equivariance_checks == 84,
        "local_A4_matches_cube_cover_derived_image": "A4" in central["Heawood_stabilizer_cover"]["derived_image"],
    }

    sample_states = sorted(boundary_states)[:12]
    return {
        "schema": "w33.boundary-singer-toroidal-84-bridge.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The affine/Fano denominator 84 now has an explicit C7-equivariant toroidal realization. "
            "PG(2,4)xGF(4) has 84 states; a regular Singer C21 supplies a C7 with twelve size-7 "
            "orbits, the quotient is GF(4)xGF(4)^* = the 12 directed K4 edges = AGL(1,4)~=A4, "
            "and an explicit lift bijects all 84 states with the repo's 84 Singer-toroidal flags."
        ),
        "boundary_singer": {
            "PG24_points": len(boundary_points),
            "companion_Singer_candidates_found": singer_companion_hits,
            "selected_matrix": [list(row) for row in singer_matrix],
            "C21_order": perm_order(g21),
            "C7_generator_power": 3,
            "C7_orbit_count_on_PG24": len(c7_orbits),
            "C7_orbit_sizes": sorted(map(len, c7_orbits)),
            "quotient_residue_to_GF4_direction": {str(r): d for r, d in residue_direction.items()},
        },
        "local12": {
            "identity": "(PG(2,4)xGF(4))/C7 ~= GF(4)^* x GF(4)",
            "edge_map": "(a,d) -> directed K4 edge a -> a+d",
            "AGL14_order": len(agl),
            "AGL14_element_order_histogram": {str(k): v for k, v in sorted(agl_order_hist.items())},
            "AGL14_isomorphism": "AGL(1,4) acts as all 12 even permutations of four GF(4) points, hence A4",
            "cube_cover_match": central["Heawood_stabilizer_cover"]["derived_image"],
        },
        "toroidal_codec": {
            "flag_count": len(all_toroidal_flags),
            "reference_hexagon": list(ref_hex),
            "completed_K4_origin": str(missing),
            "K4_point_to_GF4": {str(k): v for k, v in k4_to_gf4.items()},
            "C7_equivariance_checks": equivariance_checks,
        },
        "explicit_bridge_sample": [
            {
                "boundary_point": list(boundary_points[i]),
                "GF4_anchor": a,
                "quotient_edge": list(quotient_edge[(i, a)]),
                "toroidal_flag": stringify_flag(bridge[(i, a)]),
            }
            for i, a in sample_states
        ],
        "spectral_bridge": {
            "denominator_identity": "84 = 4*|PG(2,4)| = |PG(2,4)xGF(4)|",
            "prior_coefficient": "rho_3=-1/84",
            "new_reading": "The inverse projective anti-correlation scale equals the cardinality of an explicit C7-equivariant boundary codec that is bijective with the 84 toroidal flags.",
        },
        "choice_boundary": [
            "The PG(2,4) Singer generator is chosen from a verified companion-matrix search.",
            "The C21/C7 residue classes are identified with GF(4)^* by a declared omega phase.",
            "The completed K4 is given a declared affine GF(4) coordinate gauge.",
            "The resulting 84-state map is exactly bijective and C7-equivariant, but no full ambient-group canonicity is claimed.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "C21": result["boundary_singer"]["C21_order"],
        "C7_orbits": result["boundary_singer"]["C7_orbit_count_on_PG24"],
        "local12_group": result["local12"]["AGL14_isomorphism"],
        "equivariance_checks": result["toroidal_codec"]["C7_equivariance_checks"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
