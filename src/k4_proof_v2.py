#!/usr/bin/env python3
"""
K4 PROOF VERSION 2: Understanding the Constraint

Key observation from previous run:
- Point 0 = e0 (standard basis)
- For K4 containing 0: phases from 0 are all k=0
- The other 3 points have phases {3, 9} among themselves
- Pattern: 0 + 9 + 9 + 0 = 6 or 0 + 3 + 3 + 0 = 6

For general K4 (not containing 0):
- More varied phases, but still sum to 6

The key question: What algebraic constraint forces this?

HYPOTHESIS: The outer quad P, living in the orthogonal complement of center C,
must satisfy specific phase relationships due to the dimension constraint.
"""

import numpy as np
from pathlib import Path
import pandas as pd
from collections import defaultdict
from itertools import combinations, permutations

ROOT = Path(r"C:\Users\wiljd\OneDrive\Documents\GitHub\WilsManifold\claude_workspace\data")

def load_rays():
    df = pd.read_csv(ROOT / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv")
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, row in df.iterrows():
        pid = int(row['point_id'])
        for i in range(4):
            V[pid, i] = complex(str(row[f'v{i}']).replace(' ', ''))
    return V

def load_lines():
    df = pd.read_csv(ROOT / "_workbench/02_geometry/W33_line_phase_map.csv")
    return [tuple(map(int, str(row['point_ids']).split())) for _, row in df.iterrows()]

def inner(V, p, q):
    return np.vdot(V[p], V[q])


def understand_dimension_constraint():
    """
    KEY INSIGHT: The outer quad P lives in a COMPLEMENTARY space.

    Center C = {c0, c1, c2, c3} is an orthonormal basis.
    Each outer point p_i is orthogonal to ALL center points.

    BUT C spans all of C^4! So the orthogonal complement is {0}.

    This seems like a contradiction...

    RESOLUTION: The outer points are NOT in the orthogonal complement.
    They're each on a LINE with each center point.
    But each outer point is on a DIFFERENT line with each center point.

    So p0 is on:
    - Line L_0 with c0
    - Line L_1 with c1
    - Line L_2 with c2
    - Line L_3 with c3

    Each L_i has 4 points, including p0 and c_i.

    The constraint is that p0 must be ON all 4 of these lines.
    """
    V = load_rays()
    lines = load_lines()

    print("=" * 70)
    print("DIMENSION CONSTRAINT ANALYSIS")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    # For each outer point, identify its 4 lines (one per center point)
    print("\nLines through outer-center pairs:")
    for p in outer:
        print(f"\nPoint {p}:")
        for c in center:
            for i, L in enumerate(lines):
                if p in L and c in L:
                    others = [x for x in L if x != p and x != c]
                    print(f"  With center {c}: Line {i} = {L}")
                    print(f"    Other points on line: {others}")


def analyze_outer_subspace():
    """
    Let's look at the outer quad as vectors and understand their span.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("OUTER SUBSPACE ANALYSIS")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    # The outer vectors
    P = V[outer]  # 4x4 matrix

    print("\nOuter vectors as rows:")
    for i, p in enumerate(outer):
        print(f"  P[{i}] = V[{p}] = {V[p]}")

    # What's the rank of P?
    rank = np.linalg.matrix_rank(P)
    print(f"\nRank of outer matrix: {rank}")

    # The center vectors
    C = V[center]  # 4x4 matrix
    rank_c = np.linalg.matrix_rank(C)
    print(f"Rank of center matrix: {rank_c}")

    # Cross inner products
    print("\nP^dag C (should be zero if orthogonal):")
    PC = P @ C.conj().T
    print(PC)
    print(f"Max absolute value: {np.max(np.abs(PC))}")

    # Wait - let me check what P^dag C actually is
    # P^dag C has (i,j) entry = <p_i | c_j>
    # We already know these are zero!


def analyze_determinant_constraint():
    """
    HYPOTHESIS: The Bargmann invariant is related to a DETERMINANT.

    The Bargmann 4-cycle B = <a|b><b|c><c|d><d|a> around the outer quad.

    For a 4x4 matrix, det = sum over permutations with sign.
    Maybe B is related to a minor or subdeterminant?
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("DETERMINANT ANALYSIS")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    # Build Gram matrix
    G = np.zeros((4, 4), dtype=np.complex128)
    for i, p in enumerate(outer):
        for j, q in enumerate(outer):
            G[i, j] = inner(V, p, q)

    print("\nGram matrix G:")
    print(G)

    # Compute determinant
    det_G = np.linalg.det(G)
    print(f"\ndet(G) = {det_G}")
    print(f"|det(G)| = {abs(det_G)}")
    print(f"phase(det(G)) = {np.angle(det_G)} rad = {np.angle(det_G)/np.pi} pi")

    # The Bargmann is a product of 4 off-diagonal elements
    # Different from the determinant...

    # Let me try: compute the "permanent" analog for comparison
    # Bargmann for cycle 0->1->2->3->0 uses G[0,1], G[1,2], G[2,3], G[3,0]

    B_cycle = G[0,1] * G[1,2] * G[2,3] * G[3,0]
    print(f"\nBargmann (0->1->2->3): {B_cycle}")

    # Compare with determinant term for permutation (1,2,3,0):
    # det contribution: sign * G[0,1] * G[1,2] * G[2,3] * G[3,0]
    # Permutation (0,1,2,3) -> (1,2,3,0): this is a 4-cycle, sign = (-1)^3 = -1

    print(f"Permutation (1,2,3,0) sign = -1")
    print(f"Corresponding det term: {-B_cycle}")


def check_phase_sum_identity():
    """
    For all K4 components, the cycle sum is 6.

    Let's check if there's a GENERAL identity:
    sum of k_ij around a cycle = 6 (mod 12)

    when the 4 points form a K4 (have 4 common neighbors).
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
    print("PHASE SUM IDENTITY CHECK")
    print("=" * 70)

    # For each K4 component, compute ALL possible cycle orderings
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
                        k4_list.append((a, b, c, d))

    print(f"Found {len(k4_list)} K4 components")

    # Check all orderings for first 5 K4s
    print("\nCycle sums for different orderings:")
    for outer in k4_list[:5]:
        a, b, c, d = outer
        print(f"\n  K4 = {outer}:")

        # All 24 orderings (permutations)
        sums = set()
        for perm in permutations(outer):
            p0, p1, p2, p3 = perm
            k01 = round(6 * np.angle(inner(V, p0, p1)) / np.pi) % 12
            k12 = round(6 * np.angle(inner(V, p1, p2)) / np.pi) % 12
            k23 = round(6 * np.angle(inner(V, p2, p3)) / np.pi) % 12
            k30 = round(6 * np.angle(inner(V, p3, p0)) / np.pi) % 12
            total = (k01 + k12 + k23 + k30) % 12
            sums.add(total)

        print(f"    Distinct cycle sums: {sorted(sums)}")


def prove_from_orthogonality():
    """
    PROOF ATTEMPT:

    Given: K4 component with outer P = {p0, p1, p2, p3} and center C.
    Each p_i is orthogonal to all of C (since collinear = orthogonal).

    Let C = {e0, e1, e2, e3} be the standard basis (WLOG, by change of basis).

    Then each p_i is orthogonal to all e_j.
    But this means p_i = 0, contradiction!

    RESOLUTION: "Collinear" in W33 doesn't mean sharing ALL lines.
    Each outer point shares ONE line with each center point.
    The orthogonality is pairwise, not total.

    Actually wait - we verified that <p_i|c_j> = 0 for ALL i,j.
    How is this possible if C spans C^4?

    Let me re-examine...
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("ORTHOGONALITY PARADOX")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    # Check that center spans C^4
    C_matrix = V[center]  # 4x4 matrix
    rank_C = np.linalg.matrix_rank(C_matrix)
    print(f"Rank of center vectors: {rank_C}")

    if rank_C < 4:
        print("  Center does NOT span C^4!")
    else:
        print("  Center spans C^4.")

    # Check inner products
    print("\n<p_i|c_j> matrix:")
    IP = np.zeros((4, 4), dtype=np.complex128)
    for i, p in enumerate(outer):
        for j, c in enumerate(center):
            IP[i, j] = inner(V, p, c)
    print(IP)

    # Hmm, they ARE all zero. How?

    # Let me check: is center actually orthonormal?
    print("\n<c_i|c_j> matrix (should be I if orthonormal):")
    CC = np.zeros((4, 4), dtype=np.complex128)
    for i, c1 in enumerate(center):
        for j, c2 in enumerate(center):
            CC[i, j] = inner(V, c1, c2)
    print(CC)

    # AH! Center is NOT orthonormal (it's a W33 line, but those aren't the standard basis)


def understand_w33_lines():
    """
    W33 lines: points on the same line are ORTHOGONAL (in ray realization).

    But {4, 13, 22, 31} is NOT a W33 line! Let me verify.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("W33 LINE VERIFICATION")
    print("=" * 70)

    center = [4, 13, 22, 31]

    # Is {4, 13, 22, 31} a W33 line?
    for i, L in enumerate(lines):
        if set(L) == set(center):
            print(f"Center {center} IS line {i}")
            break
    else:
        print(f"Center {center} is NOT a W33 line!")

    # Let me check line 17 (the standard basis line)
    line_17 = lines[17]
    print(f"\nLine 17: {line_17}")

    # Check orthonormality of line 17
    print("Inner products on line 17:")
    for i, p in enumerate(line_17):
        for q in line_17[i+1:]:
            ip = inner(V, p, q)
            print(f"  <{p}|{q}> = {ip}")

    # Line 17 IS orthonormal (it's the standard basis {0, 4, 5, 6})!

    # So center {4, 13, 22, 31} is not orthonormal, but center points
    # are all collinear with each outer point on DIFFERENT lines.


def final_insight():
    """
    THE KEY INSIGHT:

    Center C = {4, 13, 22, 31} is the set of COMMON NEIGHBORS of outer P.
    This means each c in C is collinear with each p in P.
    Collinear means on the same W33 line, which means orthogonal in C^4.

    So <p_i | c_j> = 0 for all i, j.

    But C is NOT a W33 line itself! The center points are NOT mutually orthogonal.
    C has |<c_i|c_j>| = 1/sqrt(3) for i != j.

    The outer P is similar: |<p_i|p_j>| = 1/sqrt(3) for i != j.

    So we have two "cliques" P and C that are mutually orthogonal,
    but internally have equal-angle inner products.

    This is a very special configuration!
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("FINAL INSIGHT")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print("STRUCTURE:")
    print("  - Outer P = {0,1,2,3}: mutually NON-collinear, |<p|p'>| = 1/sqrt(3)")
    print("  - Center C = {4,13,22,31}: mutually NON-collinear, |<c|c'>| = 1/sqrt(3)")
    print("  - P x C: ALL pairs collinear, <p|c> = 0")
    print("\nThis is a BIPARTITE ORTHOGONALITY structure!")

    # Compute the phase structure explicitly
    print("\nPhase matrix k(p,c):")
    for p in outer:
        row = []
        for c in center:
            ip = inner(V, p, c)
            row.append(f"{ip:.3f}")
        print(f"  {p}: {row} (all zero)")

    # The constraint: P union C has 8 points, all in C^4
    # P is orthogonal to C (4x4 zero block)
    # So the 8 vectors span at most... C^4!

    print("\nCombined span:")
    all_8 = outer + center
    M = V[all_8]  # 8x4 matrix
    rank_8 = np.linalg.matrix_rank(M)
    print(f"  Rank of all 8 vectors: {rank_8}")


def main():
    understand_dimension_constraint()
    analyze_outer_subspace()
    analyze_determinant_constraint()
    check_phase_sum_identity()
    prove_from_orthogonality()
    understand_w33_lines()
    final_insight()

if __name__ == "__main__":
    main()
