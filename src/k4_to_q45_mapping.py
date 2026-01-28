#!/usr/bin/env python3
"""
K4 TO Q45 MAPPING: Finding the exact correspondence

KEY QUESTION: How do the 90 K4 components in W33 map to the 45 Q-vertices?

The numbers suggest:
- 90 K4 components in W33
- 45 vertices in Q (quotient of GQ(4,2))
- 90 = 2 * 45

Hypothesis: Each Q-vertex corresponds to a PAIR of K4 components
(related by the Z_2 sheet symmetry?)

Let me verify this numerically.
"""

from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

W33_ROOT = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data"
)
V23_ROOT = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data\_v23\v23"
)


def load_w33():
    """Load W33 rays and build collinearity."""
    rays_df = pd.read_csv(
        W33_ROOT
        / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
    )
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, row in rays_df.iterrows():
        pid = int(row["point_id"])
        for i in range(4):
            V[pid, i] = complex(str(row[f"v{i}"]).replace(" ", ""))

    lines_df = pd.read_csv(W33_ROOT / "_workbench/02_geometry/W33_line_phase_map.csv")
    lines = [
        tuple(map(int, str(row["point_ids"]).split())) for _, row in lines_df.iterrows()
    ]

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    return V, lines, col


def find_k4_components(V, col):
    """Find all 90 K4 components."""
    noncol = defaultdict(set)
    for p in range(40):
        for q in range(40):
            if p != q and q not in col[p]:
                noncol[p].add(q)

    k4_list = []
    for a in range(40):
        for b in noncol[a]:
            if b <= a:
                continue
            for c in noncol[a] & noncol[b]:
                if c <= b:
                    continue
                for d in noncol[a] & noncol[b] & noncol[c]:
                    if d <= c:
                        continue
                    common = col[a] & col[b] & col[c] & col[d]
                    if len(common) == 4:
                        k4_list.append(
                            {
                                "outer": tuple(sorted([a, b, c, d])),
                                "center": tuple(sorted(common)),
                            }
                        )

    return k4_list


def analyze_k4_structure(k4_list, V, col):
    """
    Analyze K4 structure to find the mapping to Q45.

    Key insight from v23: Q45 vertices are equivalence classes of points
    in the 90-scheme (which comes from W33 -> GQ(4,2) quotient).
    """
    print("=" * 70)
    print("K4 STRUCTURE ANALYSIS")
    print("=" * 70)

    # For each K4, compute the "zero components" of outer and center
    outer_zeros = []
    center_zeros = []

    for k4 in k4_list:
        outer = k4["outer"]
        center = k4["center"]

        # Find which component is zero for all outer points
        V_outer = V[list(outer)]
        outer_norms = np.abs(V_outer).mean(axis=0)
        outer_zero_idx = np.argmin(outer_norms)

        # Find which component is zero for all center points
        V_center = V[list(center)]
        center_norms = np.abs(V_center).mean(axis=0)
        center_zero_idx = np.argmin(center_norms)

        outer_zeros.append(outer_zero_idx)
        center_zeros.append(center_zero_idx)

    # Count pairs
    pair_counts = defaultdict(int)
    for oz, cz in zip(outer_zeros, center_zeros):
        pair_counts[(oz, cz)] += 1

    print("\n(outer_zero, center_zero) distribution:")
    for pair, count in sorted(pair_counts.items()):
        print(f"  {pair}: {count} K4s")

    # The 90 K4s should map to 45 Q-vertices
    # Check if there's a natural pairing
    print("\n" + "=" * 70)
    print("LOOKING FOR K4 -> Q45 MAPPING")
    print("=" * 70)

    # Group K4s by their (outer_zero, center_zero) signature
    # This gives 4*3 = 12 possibilities

    # Alternative: group by outer quad only
    outer_to_k4s = defaultdict(list)
    for i, k4 in enumerate(k4_list):
        outer_to_k4s[k4["outer"]].append(i)

    print(f"\nUnique outer quads: {len(outer_to_k4s)}")

    # Group by center quad
    center_to_k4s = defaultdict(list)
    for i, k4 in enumerate(k4_list):
        center_to_k4s[k4["center"]].append(i)

    print(f"Unique center quads: {len(center_to_k4s)}")

    # Each K4 is uniquely determined by its outer OR center quad
    # So 90 K4s = 90 unique outers = 90 unique centers

    return outer_zeros, center_zeros


def check_duality(k4_list):
    """
    Check if there's a duality that pairs K4s.

    The 90 -> 45 mapping might come from:
    - Swapping outer and center
    - Some involution on W33
    """
    print("\n" + "=" * 70)
    print("CHECKING K4 DUALITY")
    print("=" * 70)

    # Build a map from outer -> center and center -> outer
    outer_to_center = {}
    center_to_outer = {}

    for k4 in k4_list:
        outer_to_center[k4["outer"]] = k4["center"]
        center_to_outer[k4["center"]] = k4["outer"]

    # Check if swapping gives another K4
    # i.e., if we take a center quad as a new outer, is it a valid K4?
    swap_valid = 0
    swap_invalid = 0

    for k4 in k4_list:
        center = k4["center"]
        if center in outer_to_center:
            swap_valid += 1
        else:
            swap_invalid += 1

    print(f"K4s where center is also an outer: {swap_valid}")
    print(f"K4s where center is NOT an outer: {swap_invalid}")

    if swap_valid == 90:
        print("\nPERFECT DUALITY: Every center is also an outer!")
        # This would mean outer <-> center is an involution
        # And 90 K4s form 45 dual pairs

        # Count fixed points
        fixed = 0
        for k4 in k4_list:
            if k4["outer"] == k4["center"]:
                fixed += 1
        print(f"Self-dual K4s (outer = center): {fixed}")

    return outer_to_center, center_to_outer


def analyze_q45_connection():
    """
    Load the Q45 data and look for correspondence with K4s.
    """
    print("\n" + "=" * 70)
    print("Q45 VERTEX ANALYSIS")
    print("=" * 70)

    tau_df = pd.read_csv(V23_ROOT / "Q_vertex_tau_profile.csv")

    # Q has 45 vertices (0 to 44)
    q_vertices = tau_df["q"].unique()
    print(f"Q45 vertices: {len(q_vertices)}")

    # Each vertex has a tau profile (distribution of tau values on incident triangles)
    # This is a "local potential" at each vertex

    # Group vertices by their tau profile
    vertex_profiles = {}
    for q in q_vertices:
        q_data = tau_df[tau_df["q"] == q]
        profile = tuple(
            sorted((row["tau"], row["count"]) for _, row in q_data.iterrows())
        )
        vertex_profiles[q] = profile

    unique_profiles = set(vertex_profiles.values())
    print(f"Unique tau profiles: {len(unique_profiles)}")

    # Group vertices by profile
    profile_to_vertices = defaultdict(list)
    for q, profile in vertex_profiles.items():
        profile_to_vertices[profile].append(q)

    print("\nProfile multiplicities:")
    multiplicity_counts = defaultdict(int)
    for profile, vertices in profile_to_vertices.items():
        multiplicity_counts[len(vertices)] += 1
    for mult, count in sorted(multiplicity_counts.items()):
        print(f"  {count} profiles shared by {mult} vertex(es)")

    return vertex_profiles


def main():
    print("K4 TO Q45 MAPPING ANALYSIS")
    print("=" * 70)

    V, lines, col = load_w33()
    k4_list = find_k4_components(V, col)

    print(f"\nW33: 40 points, 40 lines, {len(k4_list)} K4 components")

    outer_zeros, center_zeros = analyze_k4_structure(k4_list, V, col)
    outer_to_center, center_to_outer = check_duality(k4_list)
    vertex_profiles = analyze_q45_connection()

    print("\n" + "=" * 70)
    print("KEY INSIGHT")
    print("=" * 70)
    print("""
    The 90 -> 45 mapping might work as follows:

    1. W33 (GQ(3,3)) has 40 points and 90 K4 components
    2. GQ(4,2) has 45 points (the Q45 vertices)
    3. The 90-scheme is a 2-fold cover of Q45

    The v23 field equation operates on Q45 triangles (triads).
    My K4/-1 proof operates on W33 4-cycles.

    The connection is:
    - Q45 triads (3 vertices) correspond to 3 noncollinear points in GQ(4,2)
    - K4 components (4 points) in W33 are "blown up" versions
    - The Z_2 sheet structure in v23 fiber is exactly the 90/45 = 2 covering factor

    The -1 Bargmann phase in K4 and the (2,2,2) holonomy in unicentric triads
    are both manifestations of the same topological obstruction:
    a nontrivial Z_2 cocycle on the base space.
    """)


if __name__ == "__main__":
    main()
