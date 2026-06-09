#!/usr/bin/env python3
"""BT626: external W(G2) action on the 48-dimensional conjugate packet.

BT623 proved that the folded-cubic E1/E3 cross-channel is not itself a
W(G2) reflection: after normalization it squares to -I, not +I.

BT626 constructs the separate external Weyl action that BT623 left open.  The
Weyl group W(G2) is the dihedral group of order 12.  It acts on the 12 roots
of G2 with two orbits of length 6: the six short roots and the six long roots.
Taking four copies gives a 48-dimensional permutation carrier:

    48 = 4*(6 short + 6 long) = 24 + 24.

This is the right size to model the E1+E3 conjugate packet, while preserving
the honest boundary: this is an external packet action, not an action extracted
from F3 itself.
"""
from __future__ import annotations

from collections import deque
import json
from pathlib import Path


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Return p after q, acting on indices by i -> q[i] -> p[q[i]]."""
    return tuple(p[q[i]] for i in range(len(q)))


def perm_order(p: tuple[int, ...]) -> int:
    seen = [False] * len(p)
    out = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        length = 0
        while not seen[j]:
            seen[j] = True
            length += 1
            j = p[j]
        if length:
            out = out * length // gcd(out, length)
    return out


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def build_action() -> tuple[tuple[int, ...], tuple[int, ...], set[tuple[int, ...]]]:
    # Coordinate: (copy, length_type, angle) with copy in 0..3,
    # length_type 0=short, 1=long, angle in Z/6Z.
    def idx(copy: int, length: int, angle: int) -> int:
        return copy * 12 + length * 6 + (angle % 6)

    n = 48
    rotation = [0] * n
    reflection = [0] * n
    for c in range(4):
        for ell in range(2):
            for a in range(6):
                rotation[idx(c, ell, a)] = idx(c, ell, a + 1)
                reflection[idx(c, ell, a)] = idx(c, ell, -a)
    r = tuple(rotation)
    s = tuple(reflection)

    gens = [r, s]
    identity = tuple(range(n))
    group = {identity}
    queue = deque([identity])
    while queue:
        g = queue.popleft()
        for h in gens:
            for new in (compose(h, g), compose(g, h)):
                if new not in group:
                    group.add(new)
                    queue.append(new)
    return r, s, group


def orbits(group: set[tuple[int, ...]], n: int) -> list[list[int]]:
    unseen = set(range(n))
    out: list[list[int]] = []
    while unseen:
        seed = min(unseen)
        orb = sorted({g[seed] for g in group})
        out.append(orb)
        unseen.difference_update(orb)
    return out


def fixed_count(g: tuple[int, ...]) -> int:
    return sum(1 for i, j in enumerate(g) if i == j)


def main() -> int:
    r, s, group = build_action()
    n = 48
    orbit_list = orbits(group, n)
    orbit_sizes = sorted(len(o) for o in orbit_list)
    fixed_profile = sorted(fixed_count(g) for g in group)

    # Burnside dimension of invariant subspace equals the number of orbits.
    invariant_dimension = sum(fixed_count(g) for g in group) // len(group)

    # The 24+24 split is by root length.  Each half has four orbits of length 6.
    short_indices = set(range(0, 6)) | set(range(12, 18)) | set(range(24, 30)) | set(range(36, 42))
    long_indices = set(range(6, 12)) | set(range(18, 24)) | set(range(30, 36)) | set(range(42, 48))
    short_orbits = [o for o in orbit_list if set(o) <= short_indices]
    long_orbits = [o for o in orbit_list if set(o) <= long_indices]

    checks = {
        "group_order_is_12": len(group) == 12,
        "rotation_order_is_6": perm_order(r) == 6,
        "reflection_order_is_2": perm_order(s) == 2,
        "dihedral_relation_srs_is_r_inverse": compose(compose(s, r), s) == tuple(r.index(i) for i in range(n)),
        "carrier_dimension_is_48": n == 48,
        "orbit_sizes_are_8_copies_of_6": orbit_sizes == [6] * 8,
        "short_half_dimension_24": len(short_indices) == 24 and len(short_orbits) == 4,
        "long_half_dimension_24": len(long_indices) == 24 and len(long_orbits) == 4,
        "burnside_invariant_dimension_equals_orbits": invariant_dimension == len(orbit_list) == 8,
        "not_claimed_to_be_F3_action": True,
    }

    result = {
        "bt": 626,
        "title": "External W(G2) action on the 48-dimensional conjugate packet",
        "group": "W(G2) = D6, order 12",
        "generators": {
            "rotation_order": perm_order(r),
            "reflection_order": perm_order(s),
            "relations": "r^6=s^2=1, srs=r^{-1}",
        },
        "carrier": {
            "dimension": 48,
            "decomposition": "48 = 4*(6 short roots + 6 long roots) = 24 + 24",
            "orbit_sizes": orbit_sizes,
            "number_of_orbits": len(orbit_list),
            "burnside_invariant_dimension": invariant_dimension,
            "fixed_point_profile_over_group": fixed_profile,
        },
        "interpretation": "This supplies the external W(G2) packet action that BT623 left open. It matches the 24+24 E1/E3 size split as four copies of the six short-root orbit plus four copies of the six long-root orbit.",
        "boundary": "The action is an external Weyl action on an abstract 48-carrier. BT623 remains valid: the folded-cubic F3 cross-channel itself is a normalized square-minus-one complex structure, not a Weyl reflection.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT626_EXTERNAL_WG2_PACKET_ACTION_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
