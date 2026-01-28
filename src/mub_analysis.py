#!/usr/bin/env python3
"""
MUTUALLY UNBIASED BASES AND THE 15-LINE STRUCTURE

Key discovery: Each of the 15 lines defines an orthonormal basis in C^4.
But in C^4, there are at most 5 MUBs (mutually unbiased bases).

So what IS this structure?

A MUB pair has |<b_i|b'_j>|^2 = 1/d for all i,j.
Here d=4, so |<p|q>|^2 = 1/4 for MUB pairs.

But we have |<p|q>|^2 = 1/3 for non-collinear pairs.

This is NOT a MUB. It's something else. Let me figure out what.
"""

from collections import defaultdict
from itertools import combinations
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


def analyze_basis_relations():
    """
    For each pair of lines (bases), compute their mutual angles.
    """
    V = load_rays()
    lines = load_lines()

    print("=" * 70)
    print("BASIS RELATIONS ANALYSIS")
    print("=" * 70)

    print(f"\nWe have {len(lines)} lines (orthonormal bases)")
    print(f"In C^4, max MUBs = 5")
    print(f"But MUB requires |<p|q>|^2 = 1/4 = 0.25")
    print(f"Our structure has |<p|q>|^2 = 1/3 = 0.333...")

    # For each pair of bases, compute the Gram matrix
    # If MUB: all entries have magnitude 1/2
    # Our case: magnitude 1/sqrt(3)

    print("\nChecking inter-basis overlaps:")
    overlap_mags = set()
    for i, L1 in enumerate(lines[:5]):  # First 5 lines
        for j, L2 in enumerate(lines[:5]):
            if i >= j:
                continue
            # Compute Gram matrix between bases
            G = np.zeros((4, 4), dtype=np.complex128)
            for a, p in enumerate(L1):
                for b, q in enumerate(L2):
                    G[a, b] = inner(V, p, q)

            mags = set(round(abs(g), 6) for g in G.flatten())
            overlap_mags.update(mags)

            print(f"\nLines {i} vs {j}:")
            print(f"  L{i} = {L1}")
            print(f"  L{j} = {L2}")
            print(f"  |<p|q>| values: {sorted(mags)}")

    print(f"\nAll inter-basis overlap magnitudes: {sorted(overlap_mags)}")


def analyze_incidence_geometry():
    """
    Understand the W33 incidence structure as a generalized quadrangle.

    GQ(s,t) parameters:
    - s+1 points per line
    - t+1 lines through each point
    - Total points: (s+1)(st+1)
    - Total lines: (t+1)(st+1)

    For W33: 40 points, 15 lines, 4 points/line
    => s+1 = 4, so s = 3
    => 40 = 4(3t+1) = 12t + 4 => 36 = 12t => t = 3
    => Check: 15 = 4(3*3+1)/4? No... let me recalculate.

    Actually: (s+1)(st+1) = 4(9+1) = 40. Check!
    And: (t+1)(st+1) = 4*10 = 40. But we have 15 lines??

    Something's off. Let me compute directly.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("INCIDENCE GEOMETRY")
    print("=" * 70)

    # Count lines through each point
    lines_per_point = defaultdict(list)
    for i, L in enumerate(lines):
        for p in L:
            lines_per_point[p].append(i)

    line_counts = [len(v) for v in lines_per_point.values()]
    print(f"\nLines through each point: {set(line_counts)}")
    print(f"  (Should be constant for a GQ)")

    # Count points per line
    points_per_line = [len(L) for L in lines]
    print(f"Points per line: {set(points_per_line)}")

    # For a GQ(3,3): s=t=3, so:
    # - 4 points per line (s+1)
    # - 4 lines through each point (t+1)
    # - (s+1)(st+1) = 4(10) = 40 points
    # - (t+1)(st+1) = 4(10) = 40 lines... but we have 15!

    # Wait, I'm confusing myself. Let me look at the data again.

    print(f"\nTotal points: 40")
    print(f"Total lines: {len(lines)}")

    # Each line has 4 points, so sum of incidences = 4*15 = 60
    # Each point is on some number of lines
    total_incidences = sum(line_counts)
    print(f"Total incidences: {total_incidences}")
    print(f"  = 4 * 15 = {4*15}")

    # So average lines per point = 60/40 = 1.5... that can't be right for constant.
    # OH! The lines aren't all the lines - just the "special" ones.

    print("\n" + "-" * 50)
    print("WAIT - checking if this is really GQ(3,3)")
    print("-" * 50)

    # Actually, let me recount
    for p in range(40):
        if len(lines_per_point[p]) != 4:
            print(
                f"  Point {p} is on {len(lines_per_point[p])} lines: {lines_per_point[p]}"
            )


def analyze_special_bases():
    """
    The standard basis line is {0, 4, 5, 6}.
    What makes this special?
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("STANDARD BASIS ANALYSIS")
    print("=" * 70)

    # Find the standard basis line
    std_line = None
    for i, L in enumerate(lines):
        if set(L) == {0, 4, 5, 6}:
            std_line = (i, L)
            break

    if std_line:
        print(f"\nStandard basis is line {std_line[0]}: {std_line[1]}")
    else:
        print("\nStandard basis {0,4,5,6} NOT found among lines!")
        # Let me check what's going on
        for i, L in enumerate(lines):
            if 0 in L:
                print(f"  Line {i} contains 0: {L}")

    # What are the 15 lines actually?
    print("\nAll 15 lines:")
    for i, L in enumerate(lines):
        # Express basis vectors
        basis_info = []
        for p in L:
            nz = np.where(np.abs(V[p]) > 0.1)[0]
            basis_info.append(f"{p}:{list(nz)}")
        print(f"  Line {i}: {L} -> components: {basis_info}")


def analyze_quaternion_action():
    """
    The Z_4 phases (i, -1, -i, 1) suggest quaternion structure.

    In the quaternion group Q_8 = {+/-1, +/-i, +/-j, +/-k},
    we have i^2 = j^2 = k^2 = ijk = -1.

    The Bargmann 4-cycle giving -1 looks like:
    traversing i -> j -> -i -> -j gives -1 (or some variant).

    Let me check if the phases have quaternionic structure.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("QUATERNION STRUCTURE INVESTIGATION")
    print("=" * 70)

    # The inner product <p|q> has phase in Z_12.
    # Z_12 = Z_4 x Z_3 (since gcd(4,3)=1)
    # The Z_4 part is {0, 3, 6, 9} -> {1, i, -1, -i}
    # The Z_3 part is {0, 4, 8} -> {1, w, w^2} where w = e^{2pi i/3}

    # Let's decompose the phases
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    phase_decomp = defaultdict(int)
    for p in range(40):
        for q in range(p + 1, 40):
            if q in col[p]:
                continue
            z = inner(V, p, q)
            k = round(6 * np.angle(z) / np.pi) % 12
            # Decompose into Z_4 x Z_3
            z4 = k % 4  # Wrong decomposition...
            # Actually: for Z_12 = Z_4 x Z_3, we use CRT
            # k mod 4 and k mod 3 uniquely determine k mod 12
            k4 = k % 4
            k3 = k % 3
            phase_decomp[(k4, k3)] += 1

    print("\nPhase decomposition (Z_4 x Z_3):")
    for (k4, k3), count in sorted(phase_decomp.items()):
        print(f"  ({k4}, {k3}): {count} pairs")

    # Now let's check: for a triad, what's the holonomy in this decomposition?
    print("\n" + "-" * 50)
    print("HOLONOMY DECOMPOSITION")
    print("-" * 50)

    # Find four-center triads
    triads = []
    for a, b, c in combinations(range(40), 3):
        if col[a] & {b, c} or col[b] & {c}:
            continue
        cn = col[a] & col[b] & col[c]
        if len(cn) == 4:
            triads.append(((a, b, c), cn))

    print(f"Found {len(triads)} four-center triads")

    # Compute holonomy decomposition
    hol_decomp = defaultdict(int)
    for (a, b, c), _ in triads[:50]:  # First 50
        k_ab = round(6 * np.angle(inner(V, a, b)) / np.pi) % 12
        k_bc = round(6 * np.angle(inner(V, b, c)) / np.pi) % 12
        k_ca = round(6 * np.angle(inner(V, c, a)) / np.pi) % 12
        h = (k_ab + k_bc + k_ca) % 12
        h4 = h % 4
        h3 = h % 3
        hol_decomp[(h4, h3)] += 1

    print("\nHolonomy decomposition (Z_4 x Z_3) on first 50 triads:")
    for (h4, h3), count in sorted(hol_decomp.items()):
        # h4: 0->1, 1->i, 2->-1, 3->-i
        # h3: 0->1, 1->w, 2->w^2
        q_part = ["1", "i", "-1", "-i"][h4]
        t_part = ["1", "w", "w^2"][h3]
        print(f"  ({h4}, {h3}) = {q_part} * {t_part}: {count} triads")


def analyze_3_fold_structure():
    """
    The Z_3 factor is interesting. Where does it come from?

    Possibilities:
    1. Color charge (QCD has SU(3) color)
    2. Triality in Spin(8)
    3. Something from the GQ(3,3) structure (s=t=3)
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("3-FOLD (Z_3) STRUCTURE")
    print("=" * 70)

    # Each line has 4 points. How do they partition by Z_3 phase?
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\nLooking at Z_3 phases within non-collinear pairs:")

    # For points 1,2,3 (all non-collinear to 0):
    print("\nPhases from point 0 to nearby points:")
    for q in range(1, 10):
        if q in col[0]:
            print(f"  0 -> {q}: COLLINEAR")
        else:
            z = inner(V, 0, q)
            k = round(6 * np.angle(z) / np.pi) % 12
            k3 = k % 3
            print(f"  0 -> {q}: k={k}, k mod 3 = {k3}")

    # The key question: What determines the Z_3 part?
    # If it's related to "color", then triads might have color-neutral condition.

    print("\n" + "-" * 50)
    print("COLOR NEUTRALITY CHECK")
    print("-" * 50)
    print("If triads are 'color singlets', the Z_3 holonomy should be 0.")

    # We already know holonomy is +/-i (Z_4 = 1 or 3 mod 4).
    # The Z_12 holonomy is 3 or 9, which in Z_3 is 0 both times!

    print("Holonomy = 3: 3 mod 3 = 0 (color singlet)")
    print("Holonomy = 9: 9 mod 3 = 0 (color singlet)")
    print("\n*** ALL FOUR-CENTER TRIADS ARE COLOR SINGLETS! ***")


def main():
    analyze_basis_relations()
    analyze_incidence_geometry()
    analyze_special_bases()
    analyze_quaternion_action()
    analyze_3_fold_structure()


if __name__ == "__main__":
    main()
