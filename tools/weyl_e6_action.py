#!/usr/bin/env python3
"""Analyze W(E6) action on E8 roots and connect to W33 edges.

Key question: Does W(E6) act transitively on 240 E8 roots?
If not, what are the orbits?

This will clarify the group-theoretic bijection.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_e8_roots():
    """Construct all 240 E8 roots."""
    roots = []

    # Type 1: (+-1, +-1, 0^6) permutations: 112 roots
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    r = [0.0] * 8
                    r[i], r[j] = s1, s2
                    roots.append(tuple(r))

    # Type 2: (+-1/2)^8 with even minus signs: 128 roots
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s * 0.5 for s in signs))

    return roots


def get_e6_simple_roots():
    """Get the 6 simple roots of E6 in the standard E8 embedding.

    Our E8 simple roots (standard D8 + half-spinor basis) give this Dynkin diagram:
        alpha_1 -- alpha_2 -- alpha_3 -- alpha_4 -- alpha_5 -- alpha_6
                                                       |
                                                       alpha_7 -- alpha_8
    Branch point at alpha_5.

    The E6 sub-diagram (Bourbaki nodes {1..6} of E8) corresponds to
    {alpha_3, alpha_4, alpha_5, alpha_6, alpha_7, alpha_8}:
        alpha_3 -- alpha_4 -- alpha_5 -- alpha_7 -- alpha_8
                                  |
                                  alpha_6
    """
    return [
        (0, 0, 1, -1, 0, 0, 0, 0),  # alpha_3
        (0, 0, 0, 1, -1, 0, 0, 0),  # alpha_4
        (0, 0, 0, 0, 1, -1, 0, 0),  # alpha_5  (branch point)
        (0, 0, 0, 0, 0, 1, -1, 0),  # alpha_6
        (0, 0, 0, 0, 0, 1, 1, 0),  # alpha_7
        (-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5),  # alpha_8
    ]


def construct_e6_roots():
    """Construct E6 roots as the orbit of the 6 simple roots under W(E6) reflections."""
    e8_roots = construct_e8_roots()
    e8_set = set(normalize_root(r) for r in e8_roots)
    simple = get_e6_simple_roots()

    # BFS: generate all E6 roots by reflecting simple roots
    e6_set = set()
    frontier = list(simple)
    for r in frontier:
        e6_set.add(normalize_root(r))

    while frontier:
        new_frontier = []
        for r in frontier:
            for alpha in simple:
                reflected = weyl_reflection(r, alpha)
                norm = normalize_root(reflected)
                if norm not in e6_set and norm in e8_set:
                    e6_set.add(norm)
                    new_frontier.append(reflected)
        frontier = new_frontier

    return [tuple(float(x) for x in r) for r in e6_set]


def weyl_reflection(root, alpha):
    """Reflect root in hyperplane orthogonal to alpha.

    Formula: s_alpha(r) = r - 2*(r.alpha)/(alpha.alpha) * alpha
    """
    r_dot_a = sum(root[i] * alpha[i] for i in range(8))
    a_dot_a = sum(alpha[i] * alpha[i] for i in range(8))

    result = tuple(root[i] - 2 * r_dot_a / a_dot_a * alpha[i] for i in range(8))
    return result


def normalize_root(r, tol=1e-6):
    """Normalize root to standard form for hashing."""
    # Round to avoid floating point issues
    return tuple(round(x, 6) for x in r)


def compute_weyl_orbit(start_root, generators, max_size=1000):
    """Compute orbit of start_root under Weyl reflections."""
    orbit = {normalize_root(start_root)}
    frontier = [start_root]

    while frontier and len(orbit) < max_size:
        current = frontier.pop()
        for gen in generators:
            reflected = weyl_reflection(current, gen)
            norm = normalize_root(reflected)
            if norm not in orbit:
                orbit.add(norm)
                frontier.append(reflected)

    return orbit


def analyze_e6_orbits_on_e8():
    """Analyze how W(E6) acts on E8 roots.

    Uses only the 6 simple E6 roots as reflection generators (sufficient
    to generate the full W(E6) group) and snaps to the E8 root lattice
    after each reflection to avoid floating-point drift.
    """
    print("=" * 70)
    print("W(E6) ACTION ON E8 ROOTS")
    print("=" * 70)

    e8_roots = construct_e8_roots()
    e6_simple = get_e6_simple_roots()
    e6_roots = construct_e6_roots()

    print(f"\nE8: {len(e8_roots)} roots")
    print(f"E6 simple roots: {len(e6_simple)}")
    print(f"E6 roots (generated): {len(e6_roots)}")

    # Build lookup for fast snapping
    import numpy as np

    e8_arr = np.array(e8_roots, dtype=np.float64)
    root_set = set(normalize_root(r) for r in e8_roots)

    def snap_to_e8(v):
        """Snap a vector to the nearest E8 root."""
        v_arr = np.array(v, dtype=np.float64)
        dists = np.sum((e8_arr - v_arr) ** 2, axis=1)
        j = np.argmin(dists)
        if dists[j] > 1e-8:
            return None
        return tuple(e8_arr[j])

    # Partition E8 roots into W(E6) orbits using BFS with simple root reflections
    print("\n" + "-" * 50)
    print("PARTITIONING E8 ROOTS BY W(E6) ORBITS")
    print("-" * 50)

    remaining = set(normalize_root(r) for r in e8_roots)
    orbits = []

    while remaining:
        rep = next(iter(remaining))
        rep_tuple = tuple(float(x) for x in rep)

        # BFS with lattice snapping
        orbit = {normalize_root(rep_tuple)}
        frontier = [rep_tuple]

        while frontier:
            new_frontier = []
            for r in frontier:
                for alpha in e6_simple:
                    reflected = weyl_reflection(r, alpha)
                    snapped = snap_to_e8(reflected)
                    if snapped is None:
                        continue
                    norm = normalize_root(snapped)
                    if norm not in orbit:
                        orbit.add(norm)
                        new_frontier.append(snapped)
            frontier = new_frontier

        orbit_in_remaining = orbit & remaining
        orbits.append(orbit_in_remaining)
        remaining -= orbit_in_remaining

    orbit_sizes = sorted([len(o) for o in orbits], reverse=True)
    print(f"\nNumber of W(E6) orbits on E8 roots: {len(orbits)}")
    print(f"Orbit sizes: {orbit_sizes}")
    print(f"Sum: {sum(orbit_sizes)}")

    expected = sorted([72] + [27] * 6 + [1] * 6, reverse=True)
    if orbit_sizes == expected:
        print("240 = 72 + 6x27 + 6x1  VERIFIED")
    else:
        print(f"WARNING: expected {expected}")

    return orbits


def compute_sp43_edge_orbits():
    """Verify that PSp(4,3) acts transitively on W33 edges."""
    print("\n" + "=" * 70)
    print("PSp(4,3) ACTION ON W33 EDGES (from earlier)")
    print("=" * 70)

    # We already computed this: PSp(4,3) has order 25920 and acts
    # transitively on 240 edges (single orbit)

    print(
        """
From orbit_bijection.py:
- PSp(4,3) order: 25920
- Edge orbits: [240] (single orbit of size 240)

Key insight: PSp(4,3) acts TRANSITIVELY on 240 edges!
"""
    )


def find_bijection_strategy():
    """Determine the correct bijection strategy."""
    print("\n" + "=" * 70)
    print("BIJECTION STRATEGY")
    print("=" * 70)

    print(
        """
GROUPS AND ACTIONS:
1. W(E6) has order 51840
2. Sp(4,3) has order 51840
3. PSp(4,3) = Sp(4,3)/{+/-I} has order 25920
4. PSp(4,3) is isomorphic to W(E6)/center, but W(E6) center is trivial!

RESOLUTION:
W(E6) ~ Sp(4,3), not PSp(4,3).
The group we computed acting on PG(3,3) is PSp(4,3) of order 25920.
This is an INDEX 2 subgroup of the full W(E6).

FOR THE BIJECTION:
- If W(E6) has 2 orbits on E8 roots (sizes a, b with a+b=240)
- And PSp(4,3) has 1 orbit on W33 edges (size 240)
- Then the bijection combines the two W(E6) orbits into one PSp(4,3) orbit

Alternatively:
- The 240 W33 edges might correspond to a DIFFERENT 240-element W(E6) set
- Not the E8 roots themselves, but derived from them
"""
    )


def check_alternative_240_sets():
    """Look for other 240-element sets related to E6/E8."""
    print("\n" + "=" * 70)
    print("ALTERNATIVE 240-ELEMENT SETS")
    print("=" * 70)

    e8_roots = construct_e8_roots()
    e6_roots = construct_e6_roots()

    print(f"E8 roots: {len(e8_roots)}")
    print(f"E6 roots: {len(e6_roots)}")

    # Positive roots
    e8_positive = [
        r
        for r in e8_roots
        if any(x > 0.01 for x in r)
        and (
            r[0] > 0.01
            or (r[0] == 0 and r[1] > 0.01)
            or (r[0] == 0 and r[1] == 0 and any(x > 0.01 for x in r))
        )
    ]
    print(f"E8 positive roots: {len(e8_positive)} (should be 120)")

    # E8 root pairs (root, -root)
    print(f"E8 root pairs: {len(e8_roots)//2} = 120")

    # E6 acts on E8/E7 etc
    # W(E6) order 51840 = 2^7 * 3^4 * 5

    # 51840 / 240 = 216 (stabilizer order for transitive action)
    # 51840 / 120 = 432
    # 51840 / 72 = 720

    print("\nPossible orbit sizes for W(E6) action:")
    for n in [72, 120, 240]:
        stab = 51840 // n
        print(f"  {n} elements: stabilizer order {stab}")

    # The 240 edges have PSp(4,3) stabilizer of order 25920/240 = 108
    print(f"\nPSp(4,3) edge stabilizer: 25920/240 = {25920//240}")


def main():
    # Analyze orbits
    orbits = analyze_e6_orbits_on_e8()

    # Compare with W33
    compute_sp43_edge_orbits()

    # Strategy
    find_bijection_strategy()

    # Alternatives
    check_alternative_240_sets()

    # Save results
    results = {
        "e6_orbits_on_e8": [len(o) for o in orbits],
        "psp43_edge_orbits": [240],
        "conclusion": "W(E6) has multiple orbits on E8, PSp(4,3) is transitive on edges",
    }

    out_path = ROOT / "artifacts" / "weyl_e6_action.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n\nWrote {out_path}")


if __name__ == "__main__":
    main()
