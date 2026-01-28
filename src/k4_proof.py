#!/usr/bin/env python3
"""
ALGEBRAIC PROOF: WHY K4 COMPONENTS HAVE BARGMANN PHASE = -1

Goal: Prove from first principles that the orthogonal dual structure
(outer P perpendicular to center C) implies Bargmann phase = -1.

Key facts to use:
1. Center C = {c0, c1, c2, c3} is an orthonormal basis of C^4
2. Each outer point p_i is orthogonal to ALL center points
3. Outer points have |<p_i|p_j>| = 1/sqrt(3) for i != j
4. Each p_i is a unit vector

The constraint: <p_i|c_j> = 0 for all i,j means the outer points
live in... wait, if they're orthogonal to a complete basis, they'd be zero!

That's wrong. Let me re-examine what "collinear with all of C" means.
"""

from collections import defaultdict
from itertools import combinations, permutations
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


def reexamine_k4_structure():
    """
    Wait - I need to recheck the K4 structure.

    If outer P is "collinear with" center C, that means each p is on
    SOME line containing SOME c. Not orthogonal!

    Let me verify the actual relationships.
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
    print("RE-EXAMINING K4 STRUCTURE")
    print("=" * 70)

    # K4 component: outer {0,1,2,3}, center {4,13,22,31}
    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print(f"\nOuter: {outer}")
    print(f"Center: {center}")

    # Check: is each outer point collinear with each center point?
    print("\nCollinearity (p in outer, c in center):")
    for p in outer:
        for c in center:
            is_col = c in col[p]
            ip = inner(V, p, c)
            print(f"  {p}-{c}: collinear={is_col}, <{p}|{c}>={ip:.6f}")

    # AH! "Collinear with" in W33 means ON THE SAME LINE.
    # Points on the same line are ORTHOGONAL in the ray realization!
    # So "collinear" = "orthogonal" in this context!


def verify_orthogonality_structure():
    """
    Verify: outer P is orthogonal to center C (because collinear = orthogonal).
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "=" * 70)
    print("ORTHOGONALITY VERIFICATION")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print("\nCenter is an orthonormal basis (points on same line):")
    for i, c1 in enumerate(center):
        for c2 in center[i + 1 :]:
            ip = inner(V, c1, c2)
            print(f"  <{c1}|{c2}> = {ip:.6f}")

    print("\nOuter-Center orthogonality (collinear pairs):")
    for p in outer:
        row = []
        for c in center:
            ip = inner(V, p, c)
            row.append(f"{abs(ip):.3f}")
        print(f"  Point {p} vs center: {row}")

    # Now the puzzle: if P is orthogonal to a COMPLETE basis C,
    # then P should be in the kernel... but that's {0}!
    #
    # Unless... the outer points are NOT all orthogonal to ALL center points.

    print("\nWait - checking which center points each outer is collinear with:")
    for p in outer:
        col_with_center = [c for c in center if c in col[p]]
        print(f"  Point {p} is collinear (orthogonal) with: {col_with_center}")


def detailed_line_analysis():
    """
    Look at which LINES contain each outer-center pair.
    """
    V = load_rays()
    lines = load_lines()

    # Build point-to-lines mapping
    pt_to_lines = defaultdict(list)
    for i, L in enumerate(lines):
        for p in L:
            pt_to_lines[p].append(i)

    print("\n" + "=" * 70)
    print("LINE STRUCTURE ANALYSIS")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print("\nLines through each outer point:")
    for p in outer:
        print(f"  Point {p}: lines {pt_to_lines[p]}")
        for li in pt_to_lines[p]:
            print(f"    Line {li}: {lines[li]}")

    print("\nLines through each center point:")
    for c in center:
        print(f"  Point {c}: lines {pt_to_lines[c]}")

    # Check: which line contains multiple outer points?
    print("\nLines containing multiple outer points:")
    for i, L in enumerate(lines):
        outer_in_L = [p for p in outer if p in L]
        if len(outer_in_L) >= 2:
            print(f"  Line {i}: {L} contains {outer_in_L}")


def analyze_gram_matrix():
    """
    Study the Gram matrix of the outer quad to understand its structure.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("GRAM MATRIX ANALYSIS")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    # Build Gram matrix
    G = np.zeros((4, 4), dtype=np.complex128)
    for i, p in enumerate(outer):
        for j, q in enumerate(outer):
            G[i, j] = inner(V, p, q)

    print("\nGram matrix G[i,j] = <outer[i]|outer[j]>:")
    print("       0          1          2          3")
    for i in range(4):
        row = " ".join(f"{G[i,j].real:+.4f}{G[i,j].imag:+.4f}j" for j in range(4))
        print(f"  {i}: {row}")

    # Key phases
    print("\nPhases k (in Z_12) for off-diagonal:")
    for i in range(4):
        for j in range(i + 1, 4):
            z = G[i, j]
            k = round(6 * np.angle(z) / np.pi) % 12
            print(f"  ({i},{j}): k = {k}")

    # Compute all Bargmann 4-cycles on this Gram matrix
    print("\nBargmann 4-cycles (using Gram matrix entries):")
    for perm in [(0, 1, 2, 3), (0, 1, 3, 2), (0, 2, 1, 3)]:
        a, b, c, d = perm
        B = G[a, b] * G[b, c] * G[c, d] * G[d, a]
        k = round(6 * np.angle(B) / np.pi) % 12
        print(f"  {a}->{b}->{c}->{d}->{a}: B = {B:.6f}, k = {k}")


def algebraic_proof_attempt():
    """
    Attempt to prove the -1 algebraically.

    Setup:
    - Let C = {c0, c1, c2, c3} be the center, an orthonormal basis
    - Let P = {p0, p1, p2, p3} be the outer quad
    - Each p_i is a unit vector in C^4
    - |<p_i|p_j>| = 1/sqrt(3) for i != j

    Key question: What constraints do we have on the p_i?

    From earlier output: each p_i is collinear with ALL center points.
    That means each p_i is orthogonal to SOME center point on each line through p_i.

    Wait, that's not quite right either. Let me think more carefully.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "=" * 70)
    print("ALGEBRAIC PROOF ATTEMPT")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    # Each outer point p is collinear with ALL 4 center points
    # Collinear means on the same LINE
    # Points on same line are ORTHOGONAL
    # So <p|c> = 0 for all p in outer, c in center??

    print("\nChecking <p|c> for all p in outer, c in center:")
    all_zero = True
    for p in outer:
        for c in center:
            ip = inner(V, p, c)
            if abs(ip) > 1e-10:
                all_zero = False
                print(f"  <{p}|{c}> = {ip:.6f} (NONZERO!)")

    if all_zero:
        print("  All inner products are zero!")

    # If all <p|c> = 0, and C is a complete orthonormal basis,
    # then each p must be... in the orthogonal complement of C?
    # But C spans all of C^4, so the orthogonal complement is {0}!

    # This is a contradiction. So NOT all <p|c> = 0.

    print("\n" + "-" * 50)
    print("RESOLUTION: Rechecking 'common neighbors'")
    print("-" * 50)

    # Let me re-verify: center = common_neighbors(outer)
    common = col[outer[0]]
    for p in outer[1:]:
        common = common & col[p]
    print(f"\nCommon neighbors of {outer}: {sorted(common)}")

    # So center points are collinear with EACH outer point individually
    # That means for each pair (p, c), they're on SOME line together

    print("\nFor each (p, c), finding the line they share:")
    for p in outer:
        for c in center:
            shared_lines = []
            for i, L in enumerate(lines):
                if p in L and c in L:
                    shared_lines.append(i)
            if shared_lines:
                print(f"  ({p}, {c}): shared lines {shared_lines}")
            else:
                print(f"  ({p}, {c}): NO SHARED LINE!")


def find_the_pattern():
    """
    Let's look at the actual vectors more carefully.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("VECTOR PATTERN ANALYSIS")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print("\nOuter vectors:")
    for p in outer:
        print(f"  V[{p}] = {V[p]}")

    print("\nCenter vectors:")
    for c in center:
        print(f"  V[{c}] = {V[c]}")

    # Notice: V[0] = (1,0,0,0), V[4] = (0,1,0,0)
    # These are standard basis vectors!
    # They're on the same line (line 17: {0,4,5,6})

    print("\nStandard basis line (line 17):")
    print("  {0, 4, 5, 6} = {e0, e1, e2, e3}")

    # So 0 and 4 are both in outer... wait, 4 is in CENTER, not outer.
    # Let me recheck.

    print(f"\n0 in outer: {0 in outer}")
    print(f"4 in center: {4 in center}")

    # Point 0 (e0) is in outer
    # Point 4 (e1) is in center
    # They're on the same line, so they're orthogonal: <0|4> = <e0|e1> = 0

    print(f"\n<0|4> = <e0|e1> = {inner(V, 0, 4)}")


def compute_bargmann_algebraically():
    """
    Let's work out the Bargmann invariant explicitly using vector components.

    For the K4 component with outer {0,1,2,3} and center {4,13,22,31}:

    The Bargmann 4-cycle around outer:
    B = <0|1><1|2><2|3><3|0>

    Let me compute this using the explicit vectors.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("EXPLICIT BARGMANN COMPUTATION")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    print("\nExplicit vectors (normalized):")
    for p in outer:
        v = V[p]
        # Print in a nice form
        terms = []
        for i in range(4):
            if abs(v[i]) > 0.01:
                terms.append(f"e{i}*({v[i]:.4f})")
        print(f"  v_{p} = " + " + ".join(terms))

    print("\nInner products:")
    ips = {}
    for i, p in enumerate(outer):
        for j, q in enumerate(outer):
            if i < j:
                z = inner(V, p, q)
                ips[(p, q)] = z
                print(f"  <{p}|{q}> = {z:.6f}")

    # Compute Bargmann
    B = ips[(0, 1)] * ips[(1, 2)] * ips[(2, 3)] * inner(V, 3, 0)
    print(f"\nBargmann B = <0|1><1|2><2|3><3|0>")
    print(
        f"  = {ips[(0,1)]:.4f} * {ips[(1,2)]:.4f} * {ips[(2,3)]:.4f} * {inner(V,3,0):.4f}"
    )
    print(f"  = {B:.6f}")
    print(f"  Phase: {np.angle(B):.6f} rad = {np.angle(B)/np.pi:.6f} pi")

    # Now let's trace through WHY this is -1
    print("\n" + "-" * 50)
    print("PHASE TRACKING")
    print("-" * 50)

    # Each inner product has phase k*pi/6 for some k
    # B phase = sum of k values (mod 12)

    total_k = 0
    for (p, q), z in sorted(ips.items()):
        k = round(6 * np.angle(z) / np.pi) % 12
        print(f"  <{p}|{q}>: phase k = {k}")
        total_k += k

    # Also need <3|0>
    z30 = inner(V, 3, 0)
    k30 = round(6 * np.angle(z30) / np.pi) % 12
    print(f"  <3|0>: phase k = {k30}")

    print(f"\n  Total phase k = {(total_k + k30) % 12}")
    print(f"  (Phase -1 corresponds to k=6)")


def check_general_constraint():
    """
    Is there a general constraint that forces sum(k) = 6 mod 12?

    Let's check multiple K4 components.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    noncol = defaultdict(set)
    for p in range(40):
        for q in range(40):
            if p != q and q not in col[p]:
                noncol[p].add(q)

    print("\n" + "=" * 70)
    print("CHECKING MULTIPLE K4 COMPONENTS")
    print("=" * 70)

    # Find K4 components
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
                        k4_list.append(((a, b, c, d), tuple(sorted(common))))

    print(f"Found {len(k4_list)} K4 components")

    # For each, analyze the phase structure
    print("\nPhase structure of first 10 K4 components:")
    for outer, center in k4_list[:10]:
        a, b, c, d = outer

        # Compute all 6 pairwise phases
        phases = {}
        for p, q in combinations(outer, 2):
            z = inner(V, p, q)
            k = round(6 * np.angle(z) / np.pi) % 12
            phases[(p, q)] = k
            phases[(q, p)] = (-k) % 12  # Hermitian: <q|p> = <p|q>*

        # The Bargmann cycle a->b->c->d->a
        cycle_k = phases[(a, b)] + phases[(b, c)] + phases[(c, d)] + phases[(d, a)]
        cycle_k = cycle_k % 12

        print(f"\n  Outer {outer}:")
        print(f"    Pairwise k: {phases}")
        print(f"    Cycle sum: {cycle_k}")


def main():
    reexamine_k4_structure()
    verify_orthogonality_structure()
    detailed_line_analysis()
    analyze_gram_matrix()
    algebraic_proof_attempt()
    find_the_pattern()
    compute_bargmann_algebraically()
    check_general_constraint()


if __name__ == "__main__":
    main()
