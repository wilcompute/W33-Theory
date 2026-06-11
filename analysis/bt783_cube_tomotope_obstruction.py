#!/usr/bin/env python3
"""
BT783 - Execute the BT782 bridge test: quotient fails, obstruction found.

BT782 asked whether the tomotope derived half Gamma(T)' = C2^4:C3 is a
C2-extension of the orientation-preserving cube half Aut+(Q3)=C2^3:C3.

The answer is NO in the strongest useful sense:
  * Gamma(T)' has trivial center, hence no normal C2 subgroup.
  * Gamma(T)' has abelianization C3, hence no index-2 subgroup and no
    quotient of order 24.
  * Consequently Gamma(T)' / C2_chiral ~= Aut+(Q3) cannot exist.

The failure exposes the real bridge obstruction:
  cube binary module under C3:      F2^3 = 1 + 2  (one fixed diagonal bit)
  tomotope binary module under C3:  F2^4 = 2 + 2  (fixed-point-free)

So the bridge is not "add a central bit".  It is: kill the cube fixed diagonal
bit and replace it with a second irreducible F4 phase plane.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(g):
    out = [0] * len(g)
    for i, j in enumerate(g):
        out[j] = i
    return tuple(out)


def order(g):
    ident = tuple(range(len(g)))
    cur = g
    k = 1
    while cur != ident:
        cur = compose(g, cur)
        k += 1
    return k


def closure(gens, n):
    ident = tuple(range(n))
    group = {ident}
    q = deque([ident])
    while q:
        g = q.popleft()
        for h in gens:
            gh = compose(h, g)
            if gh not in group:
                group.add(gh)
                q.append(gh)
    return group


def derived_subgroup(group):
    elems = list(group)
    gens = set()
    for a in elems:
        ia = inverse(a)
        for b in elems:
            ib = inverse(b)
            gens.add(compose(compose(compose(ia, ib), a), b))
    return closure(list(gens), len(elems[0]))


def order_distribution(group):
    return {str(k): v for k, v in sorted(Counter(order(g) for g in group).items())}


def perm_from_cycles(n, cycles):
    p = list(range(n))
    for cyc in cycles:
        cyc = [x - 1 for x in cyc]
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            p[a] = b
    return tuple(p)


def build_tomotope_groups():
    r0 = perm_from_cycles(12, [(5, 10), (6, 9), (7, 12), (8, 11)])
    r1 = perm_from_cycles(12, [(1, 6), (2, 5), (3, 8), (4, 7)])
    r2 = perm_from_cycles(12, [(5, 9), (6, 10), (7, 11), (8, 12)])
    r3 = perm_from_cycles(12, [(5, 8), (6, 7), (9, 12), (10, 11)])
    gamma = closure([r0, r1, r2, r3], 12)
    d = derived_subgroup(gamma)
    core = derived_subgroup(d)
    assert len(gamma) == 96
    assert len(d) == 48
    assert len(core) == 16
    return gamma, d, core


def q3_perm(coord_perm, translation):
    p = []
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        ybits = [bits[coord_perm[i]] ^ translation[i] for i in range(3)]
        p.append(sum(ybits[i] << i for i in range(3)))
    return tuple(p)


def sign(pi):
    invs = sum(1 for i in range(3) for j in range(i + 1, 3) if pi[i] > pi[j])
    return -1 if invs % 2 else 1


def build_cube_groups():
    coord_perms = [(0, 1, 2), (1, 2, 0), (2, 0, 1),
                   (0, 2, 1), (2, 1, 0), (1, 0, 2)]
    aut_plus = {
        q3_perm(pi, b)
        for pi in coord_perms if sign(pi) == 1
        for b in product([0, 1], repeat=3)
    }
    translations = {q3_perm((0, 1, 2), b) for b in product([0, 1], repeat=3)}
    c3 = q3_perm((1, 2, 0), (0, 0, 0))
    assert len(aut_plus) == 24
    assert len(translations) == 8
    assert order(c3) == 3
    return aut_plus, translations, c3


def conjugate(g, x):
    return compose(compose(g, x), inverse(g))


def fixed_subgroup(core, c3):
    return {x for x in core if conjugate(c3, x) == x}


def nonzero_orbit_profile(core, c3, identity):
    seen = set()
    sizes = []
    for x in core:
        if x == identity or x in seen:
            continue
        orb = set()
        y = x
        while y not in orb:
            orb.add(y)
            y = conjugate(c3, y)
        seen |= orb
        sizes.append(len(orb))
    return {str(k): v for k, v in sorted(Counter(sizes).items())}


def main():
    gamma, tomo_d, tomo_core = build_tomotope_groups()
    cube_plus, cube_trans, cube_c3 = build_cube_groups()

    center_tomo_d = {g for g in tomo_d if all(compose(g, h) == compose(h, g) for h in tomo_d)}
    tomo_dd = derived_subgroup(tomo_d)
    cube_fixed = fixed_subgroup(cube_trans, cube_c3)
    # Pick any order-3 element in Gamma(T)' outside the binary core.
    tomo_c3 = next(g for g in tomo_d if order(g) == 3)
    tomo_fixed = fixed_subgroup(tomo_core, tomo_c3)

    assert len(center_tomo_d) == 1
    assert len(tomo_dd) == 16
    assert len(tomo_d) // len(tomo_dd) == 3
    assert len(cube_fixed) == 2       # identity + one diagonal bit
    assert len(tomo_fixed) == 1       # identity only: fixed-point-free

    out = {
        "theorem": "BT783 cube/tomotope bridge obstruction",
        "direct_BT782_sequence_exists": False,
        "failure_reasons": {
            "tomotope_derived_center_order": len(center_tomo_d),
            "normal_C2_subgroup_exists": False,
            "tomotope_derived_abelianization_order": len(tomo_d) // len(tomo_dd),
            "tomotope_derived_index2_subgroup_exists": False,
            "tomotope_derived_order24_quotient_exists": False
        },
        "cube_orientation_half": {
            "group": "Aut+(Q3) = C2^3:C3",
            "order": len(cube_plus),
            "order_distribution": order_distribution(cube_plus),
            "binary_core_order": len(cube_trans),
            "binary_core_order_distribution": order_distribution(cube_trans),
            "C3_fixed_binary_subgroup_order": len(cube_fixed),
            "C3_fixed_nonidentity_bits": len(cube_fixed) - 1,
            "C3_nonzero_binary_orbit_profile": nonzero_orbit_profile(cube_trans, cube_c3, tuple(range(8))),
            "module_decomposition_over_F2": "1 + 2"
        },
        "tomotope_derived_half": {
            "group": "Gamma(T)' = C2^4:C3",
            "order": len(tomo_d),
            "order_distribution": order_distribution(tomo_d),
            "binary_core_order": len(tomo_core),
            "binary_core_order_distribution": order_distribution(tomo_core),
            "C3_fixed_binary_subgroup_order": len(tomo_fixed),
            "C3_fixed_nonidentity_bits": len(tomo_fixed) - 1,
            "C3_nonzero_binary_orbit_profile": nonzero_orbit_profile(tomo_core, tomo_c3, tuple(range(12))),
            "module_decomposition_over_F2": "2 + 2"
        },
        "obstruction": {
            "short_form": "cube C3 fixes a diagonal binary bit; tomotope C3 fixes none",
            "module_exchange": "C2^3 = 1+2 must be converted to C2^4 = 2+2",
            "new_bridge_rule": "kill the cube fixed diagonal bit and insert a second irreducible F4 phase plane",
            "CE2_reading": "the missing bridge is a noncentral cocycle/phase plane, not a central C2 extension"
        }
    }

    path = ROOT / "data" / "bt783_cube_tomotope_obstruction.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT783 cube/tomotope obstruction")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
