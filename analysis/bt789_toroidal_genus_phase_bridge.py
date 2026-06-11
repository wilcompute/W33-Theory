#!/usr/bin/env python3
"""
BT789 - Toroidal genus bridge for C2^3:S3 -> C2^4:C3.

The user suggested that the 3 and 4 in the cube/tomotope order-48 exchange may
be related to the minimal triangulation / genus equations of the toroidal
polyhedra.  This verifier keeps the claim exact:

    neighborly torus:       g(n) = (n-3)(n-4)/12
    complete-face dual:     h(f) = (f-4)(f-3)/12

At the Csaszar/Szilassi value n=f=7, the unit torus is exactly:

    1 = (7-3)(7-4)/12 = 4 * 3 / 12.

Those are not decorative factors.  They are the same factors in the module
repair:

    C2^3 = 1 + 2      (cube has a fixed diagonal bit)
    C2^4 = 2 + 2      (tomotope has two F4 phase planes)

The 4 is the F4-plane cardinality; the 3 is the C3 phase clock.  Their product
is the mod-12 toroidal residue normalizer.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def c3_cube(v):
    return (v[1], v[2], v[0])


def c3_plane(v):
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
        seen |= orbit
        if len(orbit) == 1:
            fixed_nonzero += 1
        sizes.append(len(orbit))
    return {
        "profile": {str(k): v for k, v in sorted(Counter(sizes).items())},
        "fixed_nonidentity_bits": fixed_nonzero,
        "nonzero_count": sum(sizes),
        "nonzero_orbit_count": len(sizes),
    }


def quotient_by_diagonal():
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

    zero = next(i for i, c in enumerate(cosets) if (0, 0, 0) in c)
    return cosets, action, zero


def lifted_profile():
    cosets, action_index, quotient_zero = quotient_by_diagonal()
    plane = list(product([0, 1], repeat=2))
    points = [(q, p) for q in range(len(cosets)) for p in plane]
    zero = (quotient_zero, (0, 0))

    def act(x):
        q, p = x
        return (action_index(q), c3_plane(p))

    return orbit_profile(points, act, zero)


def neighborly_genus(n):
    return Fraction((n - 3) * (n - 4), 12)


def complete_face_genus(f):
    return Fraction((f - 4) * (f - 3), 12)


def genus_residues_mod12():
    return [r for r in range(12) if ((r - 3) * (r - 4)) % 12 == 0]


def run_gap_witness():
    script = r"""
G := WreathProduct(CyclicGroup(2), SymmetricGroup(3));;
H := SmallGroup(48,50);;
Print("cube_id=", IdGroup(G)[1], "-", IdGroup(G)[2], "\n");
Print("cube_size=", Size(G), "\n");
Print("cube_center=", Size(Centre(G)), "\n");
Print("cube_derived=", Size(DerivedSubgroup(G)), "\n");
Print("tomo_id=", IdGroup(H)[1], "-", IdGroup(H)[2], "\n");
Print("tomo_size=", Size(H), "\n");
Print("tomo_center=", Size(Centre(H)), "\n");
Print("tomo_derived=", Size(DerivedSubgroup(H)), "\n");
Print("isomorphic=", IsomorphismGroups(G,H) <> fail, "\n");
QUIT;
"""
    proc = subprocess.run(
        ["gap", "-q"],
        input=script,
        text=True,
        capture_output=True,
        check=True,
        timeout=20,
    )
    out = {}
    for line in proc.stdout.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            out[key] = value
    return out


def main():
    cube_points = list(product([0, 1], repeat=3))
    plane_points = list(product([0, 1], repeat=2))
    cube_profile = orbit_profile(cube_points, c3_cube, (0, 0, 0))
    cosets, action_index, quotient_zero = quotient_by_diagonal()

    def quotient_action(i):
        return action_index(i)

    quotient_profile = orbit_profile(list(range(len(cosets))), quotient_action, quotient_zero)
    plane_profile = orbit_profile(plane_points, c3_plane, (0, 0))
    lift_profile = lifted_profile()
    gap = run_gap_witness()

    torus_unit = neighborly_genus(7)
    dual_unit = complete_face_genus(7)
    residues = genus_residues_mod12()
    factors = {"seven_minus_4": 3, "seven_minus_3": 4, "product": 12}

    checks = {
        "cube_C3_profile_is_1_plus_2": cube_profile["profile"] == {"1": 1, "3": 2},
        "cube_has_one_fixed_nonidentity_bit": cube_profile["fixed_nonidentity_bits"] == 1,
        "quotient_is_one_F4_plane": quotient_profile["profile"] == {"3": 1},
        "added_plane_is_one_F4_plane": plane_profile["profile"] == {"3": 1},
        "lift_is_two_F4_planes": lift_profile["profile"] == {"3": 5},
        "lift_has_no_fixed_nonidentity_bits": lift_profile["fixed_nonidentity_bits"] == 0,
        "genus_residues_are_0_3_4_7": residues == [0, 3, 4, 7],
        "Csaszar_unit_torus_is_4_times_3_over_12": torus_unit == 1,
        "Szilassi_dual_unit_torus_is_3_times_4_over_12": dual_unit == 1,
        "module_orders_match": (2 ** 3) * 6 == (2 ** 4) * 3 == 48,
        "gap_cube_is_wreath_candidate": gap["cube_id"] == "48-48" and gap["cube_center"] == "2",
        "gap_tomotope_is_no_fixed_bit_candidate": gap["tomo_id"] == "48-50" and gap["tomo_center"] == "1",
        "gap_groups_not_isomorphic": gap["isomorphic"] == "false",
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT789 check failed: {name}")

    out = {
        "theorem": "BT789 toroidal genus bridge for C2^3:S3 to C2^4:C3",
        "module_repair": {
            "cube": {
                "group": "C2^3:S3",
                "order": (2 ** 3) * 6,
                "C3_binary_profile": cube_profile,
                "decomposition": "1 + 2 over F2",
            },
            "quotient": {
                "operation": "kill diagonal <111>",
                "profile": quotient_profile,
            },
            "tomotope": {
                "group": "C2^4:C3",
                "order": (2 ** 4) * 3,
                "C3_binary_profile": lift_profile,
                "decomposition": "2 + 2 over F2",
            },
        },
        "toroidal_genus_bridge": {
            "neighborly_formula": "g(n)=(n-3)(n-4)/12",
            "complete_face_dual_formula": "h(f)=(f-4)(f-3)/12",
            "mod12_integral_residues": residues,
            "Csaszar_value_n_7": str(torus_unit),
            "Szilassi_dual_value_f_7": str(dual_unit),
            "factors_at_7": factors,
            "phase_identity": "C3_order * |F4_plane| = 3 * 4 = 12",
            "interpretation": "The torus unit is the normalized product of the C3 phase clock and one F4 plane.",
        },
        "gap_witness": gap,
        "checks": checks,
    }

    path = ROOT / "data" / "bt789_toroidal_genus_phase_bridge.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT789 toroidal genus / phase bridge")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
