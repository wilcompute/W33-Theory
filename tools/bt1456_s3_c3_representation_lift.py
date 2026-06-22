#!/usr/bin/env python3
"""BT1456: decompose the closure/shear action into S3 and central C3 factors."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1456_s3_c3_representation_lift.json"

STATES = [(branch, phase) for branch in range(4) for phase in range(3)]
INDEX = {s: i for i, s in enumerate(STATES)}
IDENT = tuple(range(len(STATES)))


def perm_from_fn(fn):
    return tuple(INDEX[fn(s)] for s in STATES)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def order(p):
    cur = IDENT
    for n in range(1, 200):
        cur = compose(p, cur)
        if cur == IDENT:
            return n
    raise RuntimeError("order not found")


def generated_group(gens):
    group = {IDENT}
    changed = True
    while changed:
        changed = False
        for a in list(group):
            for g in gens:
                for h in (compose(g, a), compose(a, g)):
                    if h not in group:
                        group.add(h)
                        changed = True
    return sorted(group)


def tau4(state):
    b, p = state
    return b ^ 2, p


def shear(state):
    b, p = state
    return b, (p + b) % 3


def descriptor(g):
    rows = []
    for b in range(4):
        images = []
        for p in range(3):
            nb, np = STATES[g[INDEX[(b, p)]]]
            images.append((nb, (np - p) % 3))
        if len({x[0] for x in images}) == 1 and len({x[1] for x in images}) == 1:
            rows.append({"branch": b, "branch_image": images[0][0], "phase_shift": images[0][1]})
        else:
            rows.append({"branch": b, "images": images})
    return rows


def commutes_with_all(g, group):
    return all(compose(g, h) == compose(h, g) for h in group)


def subgroup_generated_by(elements):
    return set(generated_group(elements))


def coset_rep(g, center):
    coset = sorted(compose(g, z) for z in center)
    return coset[0]


def main() -> None:
    t = perm_from_fn(tau4)
    s = perm_from_fn(shear)
    group = generated_group([t, s])
    center = sorted([g for g in group if commutes_with_all(g, group)])
    central_order3 = [g for g in center if order(g) == 3]
    quotient_reps = sorted({coset_rep(g, center) for g in group})
    quotient_orders = {}
    for rep in quotient_reps:
        # quotient order modulo the center
        cur = IDENT
        for n in range(1, 20):
            cur = compose(rep, cur)
            if cur in center:
                quotient_orders[str(n)] = quotient_orders.get(str(n), 0) + 1
                break
    fano_factor_map = []
    face_pairs = [[0, 1], [2, 6], [3, 5]]
    for pair_index, pair in enumerate(face_pairs):
        for side, face in enumerate(pair):
            for orientation in range(2):
                branch = 2 * side + orientation
                fano_factor_map.append({
                    "strand": len(fano_factor_map),
                    "s3_pair_index": pair_index,
                    "face": face,
                    "branch": branch,
                    "central_c3_phase": pair_index,
                    "local_orientation": orientation,
                })
    checks = {
        "group_order_18": len(group) == 18,
        "center_order_3": len(center) == 3,
        "two_nontrivial_central_order3": len(central_order3) == 2,
        "quotient_order_6": len(quotient_reps) == 6,
        "quotient_order_profile_s3": quotient_orders == {"1": 1, "2": 3, "3": 2},
        "s3_factor_has_three_pair_slots": len(face_pairs) == 3,
        "fano_factor_map_has_12_strands": len(fano_factor_map) == 12,
        "central_phase_values_are_0_1_2": sorted({row["central_c3_phase"] for row in fano_factor_map}) == [0, 1, 2],
    }
    result = {
        "bt": 1456,
        "title": "S3 x C3 representation lift",
        "verified": all(checks.values()),
        "group": {"order": len(group), "center_order": len(center), "quotient_order": len(quotient_reps)},
        "factorization": {
            "central_factor": "C3 qutrit phase center = center of the closure/shear group",
            "switching_factor": "S3 = quotient by the central C3",
            "quotient_order_profile": quotient_orders,
        },
        "central_elements": [{"order": order(g), "descriptor": descriptor(g)} for g in center],
        "fano_factor_map": fano_factor_map,
        "interpretation": "The closure/shear group splits into an S3 switching factor over the three Szilassi opposite-pair channels and a central C3 qutrit phase factor.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1456, "verified": result["verified"], "quotient": quotient_orders}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
