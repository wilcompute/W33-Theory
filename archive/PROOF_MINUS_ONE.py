#!/usr/bin/env python3
"""
THE PROOF: WHY K4 COMPONENTS HAVE BARGMANN PHASE = -1

THEOREM: For any K4 component in W33, the Bargmann 4-cycle around the
outer quad has phase exactly -1 (k=6 in Z_12).

PROOF:

Let the outer quad be P = {p_0, p_1, p_2, p_3} with rays V[p_i] in C^4.
Let the center quad be C = {c_0, c_1, c_2, c_3} with rays V[c_j].

FACT 1: The center C forms an ORTHONORMAL BASIS for C^4.
        (Mutual orthogonality = collinearity in W33)

FACT 2: Each outer point p_i is ORTHOGONAL to ALL center points.
        (Complete bipartite collinearity between P and C)
        This means: <p_i | c_j> = 0 for all i, j.

FACT 3: But each outer point is a UNIT VECTOR in C^4!
        So V[p_i] must lie in the NULL SPACE of the center basis.
        Since C spans C^4, the only null space is {0}.
        CONTRADICTION?

RESOLUTION: The center rays span a 3D subspace, not all of C^4!
            There IS a 1D null space.

Wait, that can't be right either. Center is 4 orthonormal vectors in C^4,
so they should span everything.

Let me reconsider...

Actually from the data: <p_i | c_j> = 0 for ALL pairs!
This means outer rays are orthogonal to ALL center rays.
But center spans C^4, so outer rays must be 0.
But outer rays are unit vectors.

This is impossible unless... I'm misreading the data.

Let me verify directly.
"""

from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(
    r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data"
)


def load_rays():
    df = pd.read_csv(
        ROOT
        / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
    )
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, row in df.iterrows():
        pid = int(row["point_id"])
        for i in range(4):
            V[pid, i] = complex(str(row[f"v{i}"]).replace(" ", ""))
    return V


def load_lines():
    df = pd.read_csv(ROOT / "_workbench/02_geometry/W33_line_phase_map.csv")
    return [tuple(map(int, str(row["point_ids"]).split())) for _, row in df.iterrows()]


def inner(V, p, q):
    return np.vdot(V[p], V[q])


def verify_structure():
    """
    Verify the K4 structure very carefully.
    """
    V = load_rays()
    lines = load_lines()

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("=" * 70)
    print("K4 STRUCTURE VERIFICATION")
    print("=" * 70)

    # The K4 component with outer {0,1,2,3}
    outer = [0, 1, 2, 3]

    # Find the center: points collinear with ALL of outer
    common = set(range(40))
    for p in outer:
        common &= col[p]
    common -= set(outer)

    print(f"\nOuter: {outer}")
    print(f"Points collinear with all of outer: {sorted(common)}")

    center = sorted(common)

    print(f"\nCenter: {center}")

    # Verify: center should be mutually orthogonal (collinear in W33)
    print("\nCenter inner products:")
    for i, c1 in enumerate(center):
        for c2 in center[i + 1 :]:
            z = inner(V, c1, c2)
            print(f"  <{c1}|{c2}> = {z:.6f} (|.|={abs(z):.6f})")

    # Verify: outer should be mutually NON-orthogonal (non-collinear in W33)
    print("\nOuter inner products:")
    for i, p1 in enumerate(outer):
        for p2 in outer[i + 1 :]:
            z = inner(V, p1, p2)
            print(f"  <{p1}|{p2}> = {z:.6f} (|.|={abs(z):.6f})")

    # Now the KEY: what are <outer | center>?
    print("\n" + "-" * 50)
    print("<OUTER | CENTER> MATRIX")
    print("-" * 50)

    for p in outer:
        row = []
        for c in center:
            z = inner(V, p, c)
            row.append(f"{z:.4f}")
        print(f"  p={p}: " + " ".join(row))

    # And check collinearity
    print("\nCollinearity (p,c):")
    for p in outer:
        col_list = [c for c in center if c in col[p]]
        print(f"  p={p} is collinear with: {col_list}")


def find_actual_center():
    """
    Let me find the ACTUAL center of the K4 containing {0,1,2,3}.

    In W33, each point is on 4 lines. The K4 structure means:
    - Outer: 4 mutually non-collinear points
    - Center: 4 points that are EACH collinear with ALL outer points
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "=" * 70)
    print("FINDING ACTUAL K4 CENTER")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    # For each outer point, which lines is it on?
    print("\nLines through each outer point:")
    for p in outer:
        p_lines = [L for L in lines if p in L]
        print(f"\nPoint {p} is on lines:")
        for L in p_lines:
            print(f"  {L}")

    # Find lines that contain pairs from outer
    print("\n" + "-" * 50)
    print("LINES CONTAINING OUTER PAIRS")
    print("-" * 50)

    from itertools import combinations

    for pair in combinations(outer, 2):
        p, q = pair
        shared_lines = [L for L in lines if p in L and q in L]
        if shared_lines:
            print(f"Pair ({p},{q}) share lines: {shared_lines}")
        else:
            print(f"Pair ({p},{q}) share NO lines (non-collinear)")

    # The K4 center should be: for each pair of non-collinear outer points,
    # there's a unique "third point" that's collinear with both?
    # No, that's not the K4 structure either...

    # Actually, the K4 structure in GQ(3,3):
    # Given 4 mutually non-collinear points (the outer quad),
    # there are exactly 4 points (the center) such that each center point
    # is collinear with ALL 4 outer points.

    # Let me verify this by intersection
    center_candidates = set(range(40)) - set(outer)
    for p in outer:
        center_candidates &= col[p]

    print(f"\nCenter (collinear with ALL of outer): {sorted(center_candidates)}")


def understand_collinearity():
    """
    The collinearity graph in W33.

    Two points are collinear if they're on a common line.
    A W33 line has 4 points, all mutually collinear.

    Non-collinear points have |<p|q>| = 1/sqrt(3).
    Collinear points have <p|q> = 0 (orthogonal).
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("COLLINEARITY = ORTHOGONALITY")
    print("=" * 70)

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # Check: collinear => orthogonal
    print("\nVerifying collinear => orthogonal:")
    for L in lines[:5]:
        print(f"\nLine {L}:")
        for i, p in enumerate(L):
            for q in L[i + 1 :]:
                z = inner(V, p, q)
                print(f"  <{p}|{q}> = {z:.6f}")

    # Check: non-collinear => |.| = 1/sqrt(3)
    print("\n" + "-" * 50)
    print("Non-collinear pairs:")
    count = 0
    for p in range(5):
        for q in range(p + 1, 10):
            if q not in col[p]:
                z = inner(V, p, q)
                print(f"  <{p}|{q}> = {z:.6f}, |.| = {abs(z):.4f}")
                count += 1
                if count >= 10:
                    break
        if count >= 10:
            break


def the_actual_proof():
    """
    THE ACTUAL PROOF

    Given the K4 structure:
    - Outer P = {0,1,2,3}: mutually NON-collinear, so |<p|q>| = 1/sqrt(3)
    - Center C = {4,13,22,31}: mutually COLLINEAR (on a line), so <c|c'> = 0

    Each outer point p is collinear with ALL center points, so <p|c> = 0 for all c.

    KEY INSIGHT: The center forms an orthonormal basis for C^4!
    So every vector can be written in this basis.

    But outer points are ORTHOGONAL to the entire center basis...
    That's only possible if outer points are ZERO, which contradicts unit norm.

    Let me check the data again.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "=" * 70)
    print("THE ACTUAL PROOF")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    # Find center
    center_set = set(range(40))
    for p in outer:
        center_set &= col[p]
    center = sorted(center_set - set(outer))

    print(f"Outer: {outer}")
    print(f"Center: {center}")

    # Print the actual rays
    print("\nOuter rays:")
    for p in outer:
        print(f"  V[{p}] = {V[p]}")

    print("\nCenter rays:")
    for c in center:
        print(f"  V[{c}] = {V[c]}")

    # Check if center is orthonormal
    print("\nCenter orthogonality:")
    C = V[center]
    G_center = C @ C.conj().T
    print(f"Gram matrix of center:")
    for i in range(4):
        row = " ".join(f"{G_center[i,j]:8.4f}" for j in range(4))
        print(f"  {row}")

    # Check <outer | center>
    print("\n<outer | center>:")
    for p in outer:
        for c in center:
            z = inner(V, p, c)
            print(f"  <{p}|{c}> = {z:.6f}")

    # AH! The issue: center might not be on the SAME line!
    # Let me check if center is mutually collinear
    print("\nIs center {" + ",".join(map(str, center)) + "} a line?")
    for line in lines:
        if set(line) == set(center):
            print(f"  YES! Line {line}")
            break
    else:
        print("  NO! Center is NOT a single line.")
        print("  Checking pairwise collinearity:")
        for i, c1 in enumerate(center):
            for c2 in center[i + 1 :]:
                is_col = c2 in col[c1]
                z = inner(V, c1, c2)
                print(f"    ({c1},{c2}): collinear={is_col}, <.> = {z:.4f}")


def main():
    verify_structure()
    find_actual_center()
    understand_collinearity()
    the_actual_proof()


if __name__ == "__main__":
    main()
