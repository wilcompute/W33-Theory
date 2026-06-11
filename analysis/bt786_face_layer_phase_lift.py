#!/usr/bin/env python3
"""
BT786 - The tomotope face layer is the phase-lift core.

BT783 found the real cube/tomotope obstruction:

    cube binary module:      C2^3 = 1 + 2
    tomotope binary module:  C2^4 = 2 + 2

BT784 then showed that the tomotope face count 16 is the only non-primitive
rank-32 stratum: it appears as two 8-packets, not as one rank-32 orbit.

BT786 closes those two observations together.  The two face 8-packets are the
raw phase double cover of the cube C2^3 core.  After killing the cube diagonal
fixed bit and adding a second irreducible F4 plane, the lifted 16-point face
layer has exactly the tomotope C3 module profile: five nonzero 3-cycles and no
fixed nonidentity bit.
"""
from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def c3_cube(v):
    """Cyclic coordinate rotation on F2^3."""
    return (v[1], v[2], v[0])


def c3_plane(v):
    """Order-3 irreducible action on F2^2."""
    a, b = v
    return (b, a ^ b)


def orbit_profile(points, action, zero):
    seen = set()
    sizes = []
    fixed_nonzero = 0
    for p in points:
        if p == zero or p in seen:
            continue
        orbit = set()
        x = p
        while x not in orbit:
            orbit.add(x)
            x = action(x)
        if len(orbit) == 1:
            fixed_nonzero += 1
        seen |= orbit
        sizes.append(len(orbit))
    return {
        "profile": {str(k): v for k, v in sorted(Counter(sizes).items())},
        "fixed_nonidentity_bits": fixed_nonzero,
        "nonzero_orbit_count": len(sizes),
        "nonzero_count": sum(sizes),
    }


def quotient_by_diagonal():
    """Return F2^3/<111> cosets and induced C3 action."""
    d = (1, 1, 1)
    cube = list(product([0, 1], repeat=3))
    coset_of = {}
    cosets = []
    for x in cube:
        if x in coset_of:
            continue
        y = tuple(x[i] ^ d[i] for i in range(3))
        coset = frozenset([x, y])
        idx = len(cosets)
        cosets.append(coset)
        for z in coset:
            coset_of[z] = idx

    def action(i):
        representative = next(iter(cosets[i]))
        return coset_of[c3_cube(representative)]

    return cosets, action


def quotient_profile():
    cosets, action_index = quotient_by_diagonal()
    points = list(range(len(cosets)))
    zero = next(i for i, c in enumerate(cosets) if (0, 0, 0) in c)

    def act(i):
        return action_index(i)

    return orbit_profile(points, act, zero)


def lifted_profile():
    """(F2^3/<111>) plus a second irreducible F2^2 plane."""
    cosets, action_index = quotient_by_diagonal()
    quotient_zero = next(i for i, c in enumerate(cosets) if (0, 0, 0) in c)
    plane = list(product([0, 1], repeat=2))
    points = [(q, p) for q in range(len(cosets)) for p in plane]
    zero = (quotient_zero, (0, 0))

    def act(x):
        q, p = x
        return (action_index(q), c3_plane(p))

    return orbit_profile(points, act, zero)


def main():
    bt780 = json.load(open(ROOT / "data" / "bt780_rank32_suborbit_atlas_summary.json"))
    bt783 = json.load(open(ROOT / "data" / "bt783_cube_tomotope_obstruction.json"))
    bt784 = json.load(open(ROOT / "data" / "bt784_rank32_strata_map.json"))
    bt785 = json.load(open(ROOT / "data" / "bt785_eh_480_as_ten_48_packets.json"))

    sizes = bt780["suborbit_sizes"]
    size8_orbits = [i for i, s in enumerate(sizes) if s == 8]
    first_rows = {row["orbit"]: row for row in bt780["first_12_orbits"]}
    face_orbits = [
        i for i in size8_orbits
        if first_rows.get(i, {}).get("line_relation_multiset_to_base") == {"equal": 1, "one_side": 1}
        and first_rows.get(i, {}).get("base_target_point_overlap") == 5
    ]
    excluded_size8 = [i for i in size8_orbits if i not in face_orbits]
    face_layer_count = sum(sizes[i] for i in face_orbits)

    cube_points = list(product([0, 1], repeat=3))
    cube_profile = orbit_profile(cube_points, c3_cube, (0, 0, 0))
    quotient = quotient_profile()
    plane_profile = orbit_profile(list(product([0, 1], repeat=2)), c3_plane, (0, 0))
    lift = lifted_profile()

    checks = {
        "rank32_has_three_size8_packets": size8_orbits == [9, 10, 11],
        "face_layer_is_exactly_two_size8_packets": face_orbits == [9, 10],
        "third_size8_packet_is_not_face_layer": excluded_size8 == [11],
        "face_layer_count_is_tomotope_faces": face_layer_count == 16 == bt784["target_counts"]["faces"],
        "face_layer_has_no_primitive_16_orbit": "16" not in bt780["orbit_size_profile"],
        "cube_profile_matches_BT783": cube_profile["profile"] == bt783["cube_orientation_half"]["C3_nonzero_binary_orbit_profile"],
        "cube_has_one_fixed_nonidentity_bit": cube_profile["fixed_nonidentity_bits"] == 1,
        "quotient_kills_diagonal_to_one_F4_plane": quotient["profile"] == {"3": 1} and quotient["fixed_nonidentity_bits"] == 0,
        "new_plane_is_one_F4_plane": plane_profile["profile"] == {"3": 1} and plane_profile["fixed_nonidentity_bits"] == 0,
        "lift_profile_matches_tomotope_BT783": lift["profile"] == bt783["tomotope_derived_half"]["C3_nonzero_binary_orbit_profile"],
        "lift_has_no_fixed_nonidentity_bits": lift["fixed_nonidentity_bits"] == 0,
        "face_layer_times_C3_is_local_48": face_layer_count * 3 == bt785["local_packet_48"]["value"],
        "cube_core_times_S3_is_local_48": 8 * 6 == bt785["local_packet_48"]["value"],
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT786 check failed: {name}")

    out = {
        "theorem": "BT786 face-layer phase lift",
        "inputs": {
            "BT780_size8_orbits": size8_orbits,
            "BT783_cube_module": bt783["cube_orientation_half"]["module_decomposition_over_F2"],
            "BT783_tomotope_module": bt783["tomotope_derived_half"]["module_decomposition_over_F2"],
            "BT784_faces": bt784["target_counts"]["faces"],
            "BT785_local_packet": bt785["local_packet_48"]["value"],
        },
        "rank32_face_layer": {
            "face_orbits": face_orbits,
            "face_orbit_sizes": [sizes[i] for i in face_orbits],
            "excluded_size8_orbits": excluded_size8,
            "excluded_reason": {
                str(i): {
                    "relation": first_rows[i]["line_relation_multiset_to_base"],
                    "overlap": first_rows[i]["base_target_point_overlap"],
                }
                for i in excluded_size8
            },
            "face_layer_count": face_layer_count,
            "primitive_16_orbit_exists": False,
            "interpretation": "16 faces are a two-sheet 8+8 phase lift, not one primitive rank-32 orbit",
        },
        "module_lift": {
            "cube_C2_3_profile": cube_profile,
            "kill_diagonal_quotient_profile": quotient,
            "added_F4_plane_profile": plane_profile,
            "lifted_C2_4_profile": lift,
            "short_law": "C2^3=(1+2) -> C2^3/<111> + F4 = 2+2",
        },
        "packet_identity": {
            "cube_side": "8 cube binary bits * |S3| = 8*6 = 48",
            "tomotope_side": "16 face-layer bits * |C3| = 16*3 = 48",
            "W33_action": "480 = (k-r) * (16 faces * C3) = 10 * 48",
        },
        "checks": checks,
    }

    path = ROOT / "data" / "bt786_face_layer_phase_lift.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT786 face-layer phase lift")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
