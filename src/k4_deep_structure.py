#!/usr/bin/env python3
"""
K4 DEEP STRUCTURE ANALYSIS

Key observations so far:
1. All 40 points have DISTINCT phase signatures (no automorphisms preserve phases!)
2. K4 outer quad: all pairwise |<p|q>| = 1/sqrt(3)
3. K4 center quad: all pairwise |<c|c'>| = 0 (orthonormal basis!)
4. Outer points are ALL collinear with ALL center points (complete bipartite!)
5. Bargmann 4-cycle on outer always = -1

The critical insight: the phase structure k(p,q) on the outer quad satisfies
k(p,q) + k(q,p) = 0 mod 12 (antisymmetry)

For the quad {0,1,2,3}:
  k(0,*) = 0 for all (point 0 is the "gauge reference")
  k(1,2) = 9, k(2,1) = 3
  k(1,3) = 3, k(3,1) = 9
  k(2,3) = 9, k(3,2) = 3

So the non-trivial phases form a pattern: 3 and 9 appear in pairs.
3 = i (90 deg), 9 = -i (-90 deg)

This is the QUATERNION structure!
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


def analyze_quaternion_structure():
    """
    The phases 3 and 9 in Z_12 correspond to i and -i.

    In the quaternion algebra:
      1, i, j, k with i^2 = j^2 = k^2 = ijk = -1

    The pattern on {0,1,2,3}:
      - Point 0 is the "1" (all phases 0)
      - Points 1,2,3 are like i,j,k

    Let's check: do the phases satisfy quaternion relations?
    """
    V = load_rays()

    print("=" * 70)
    print("QUATERNION STRUCTURE")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    # Phase table
    k = {}
    for p in outer:
        for q in outer:
            if p != q:
                z = inner(V, p, q)
                k[(p,q)] = round(6 * np.angle(z) / np.pi) % 12

    print("\nPhase table k(p,q):")
    print("     ", end="")
    for q in outer:
        print(f"  {q}  ", end="")
    print()
    for p in outer:
        print(f"  {p} ", end="")
        for q in outer:
            if p == q:
                print("  -  ", end="")
            else:
                print(f"  {k[(p,q)]:2d} ", end="")
        print()

    # Convert to complex phases
    print("\nAs complex phases (w = e^{i*pi/6}):")
    print("  k=0: w^0 = 1")
    print("  k=3: w^3 = i")
    print("  k=6: w^6 = -1")
    print("  k=9: w^9 = -i")

    # The structure:
    # <1|2> has phase i (k=3)
    # <2|1> has phase -i (k=9)
    # This is the ORIENTATION of the edge 1-2!

    # In quaternion terms:
    # If we think of 0 as 1, and 1,2,3 as i,j,k:
    # <i|j> = ? (should relate to k)
    # <j|i> = -<i|j> in some sense

    print("\n" + "-" * 50)
    print("QUATERNION INTERPRETATION")
    print("-" * 50)

    # The magnitude |<p|q>| = 1/sqrt(3) for all non-equal pairs
    # The phase k(p,q) gives orientation

    # Check: ij = k, jk = i, ki = j
    # In phase terms: phase(1,2) "times" phase(2,3) should give phase(1,3)

    # Actually, phases ADD under multiplication
    # So: k(1,2) + k(2,3) should relate to k(1,3)

    print(f"\nk(1,2) + k(2,3) = {k[(1,2)]} + {k[(2,3)]} = {(k[(1,2)] + k[(2,3)]) % 12}")
    print(f"k(1,3) = {k[(1,3)]}")
    print(f"Difference: {(k[(1,2)] + k[(2,3)] - k[(1,3)]) % 12}")

    # For Bargmann cycle 1->2->3->1:
    # B = <1|2><2|3><3|1> = w^{k(1,2)+k(2,3)+k(3,1)}
    print(f"\nBargmann 3-cycle 1->2->3->1:")
    print(f"  k(1,2) + k(2,3) + k(3,1) = {k[(1,2)]} + {k[(2,3)]} + {k[(3,1)]} = {(k[(1,2)] + k[(2,3)] + k[(3,1)]) % 12}")


def analyze_all_k4_phase_patterns():
    """
    Look at the phase patterns across ALL 90 K4 components.
    Are they all the same? Or do they differ?
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
    print("K4 PHASE PATTERN CLASSIFICATION")
    print("=" * 70)

    # Find all K4s
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
                        k4_list.append((a,b,c,d))

    print(f"Found {len(k4_list)} K4 components")

    # For each K4, compute the canonical phase pattern
    # Pattern: 6 phases k(a,b), k(a,c), k(a,d), k(b,c), k(b,d), k(c,d)
    # But we need to account for gauge freedom!

    # Gauge-invariant: the 6 phases must sum appropriately
    # Actually, gauge freedom shifts ALL phases by same delta
    # So the DIFFERENCES are gauge-invariant

    patterns = defaultdict(list)
    for outer in k4_list:
        a, b, c, d = outer

        # Get all 6 phases
        phases = []
        for i, p in enumerate([a,b,c,d]):
            for q in [a,b,c,d][i+1:]:
                z = inner(V, p, q)
                k = round(6 * np.angle(z) / np.pi) % 12
                phases.append(k)

        # Canonical: sort
        canon = tuple(sorted(phases))
        patterns[canon].append(outer)

    print(f"\nFound {len(patterns)} distinct phase patterns:")
    for pat, k4s in sorted(patterns.items(), key=lambda x: -len(x[1])):
        print(f"  Pattern {pat}: {len(k4s)} K4s")
        if len(k4s) <= 3:
            for k4 in k4s:
                print(f"    {k4}")


def check_bargmann_formula():
    """
    The Bargmann phase for cycle a->b->c->d->a is:
      k(a,b) + k(b,c) + k(c,d) + k(d,a) mod 12

    This always equals 6 for K4 components.

    WHY? Let's see if there's a simple formula.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("BARGMANN FORMULA DERIVATION")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    # Get phase table
    k = {}
    for p in outer:
        for q in outer:
            if p != q:
                z = inner(V, p, q)
                k[(p,q)] = round(6 * np.angle(z) / np.pi) % 12

    # The antisymmetry: k(p,q) + k(q,p) = 0 mod 12
    # This means k(q,p) = -k(p,q) = 12 - k(p,q)

    print("\nAsymmetric phases s(p,q) = k(p,q) - k(q,p) mod 12:")
    s = {}
    for p in outer:
        for q in outer:
            if p < q:
                s[(p,q)] = (k[(p,q)] - k[(q,p)]) % 12
                print(f"  s({p},{q}) = {k[(p,q)]} - {k[(q,p)]} = {s[(p,q)]}")

    # The 4-cycle sum:
    # S = k(a,b) + k(b,c) + k(c,d) + k(d,a)
    #   = k(a,b) - k(c,b) + k(c,d) - k(a,d)     [using antisymmetry]
    #   = [k(a,b) - k(a,d)] + [k(c,d) - k(c,b)]

    print("\n" + "-" * 50)
    print("CYCLE DECOMPOSITION")
    print("-" * 50)

    for cyc in [[0,1,2,3], [0,1,3,2], [0,2,1,3]]:
        a, b, c, d = cyc
        S = (k[(a,b)] + k[(b,c)] + k[(c,d)] + k[(d,a)]) % 12

        # Alternative form
        term1 = (k[(a,b)] - k[(a,d)]) % 12  # Compare from a
        term2 = (k[(c,d)] - k[(c,b)]) % 12  # Compare from c

        print(f"\nCycle {a}->{b}->{c}->{d}:")
        print(f"  Direct: {k[(a,b)]}+{k[(b,c)]}+{k[(c,d)]}+{k[(d,a)]} = {S}")
        print(f"  Alt:    [{k[(a,b)]}-{k[(a,d)]}] + [{k[(c,d)]}-{k[(c,b)]}] = {term1} + {term2} = {(term1+term2)%12}")


def geometric_proof():
    """
    THE GEOMETRIC PROOF:

    The 4 outer points in C^4 determine a "projective quadrilateral" in CP^3.
    The Bargmann phase is the HOLONOMY around this quadrilateral.

    Key: The center points (orthonormal basis) give a FRAME in C^4.
    The outer points are expressed in this frame.

    The -1 comes from... let me think...
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("GEOMETRIC PROOF ATTEMPT")
    print("=" * 70)

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print(f"\nOuter: {outer}")
    print(f"Center: {center}")

    # Express outer in center basis
    # Each outer point p is collinear with all 4 center points
    # That means V[p] . V[c] = 0 for all c in center? No wait...

    print("\n<outer | center> matrix:")
    print("         ", end="")
    for c in center:
        print(f"   c={c}  ", end="")
    print()

    for p in outer:
        print(f"  p={p}: ", end="")
        for c in center:
            z = inner(V, p, c)
            print(f" {z:7.4f}", end="")
        print()

    # AH! The outer and center are NOT orthogonal!
    # The center is an orthonormal basis, but outer points are NOT in that span.

    # Actually wait - collinearity in W33 means orthogonality in C^4
    # So if p is collinear with c, then <p|c> = 0

    print("\nCollinearity check (p collinear with c => <p|c>=0):")
    for p in outer:
        for c in center:
            z = inner(V, p, c)
            is_col = c in col[p]
            print(f"  ({p},{c}): |<p|c>| = {abs(z):.4f}, collinear = {is_col}")


def find_the_constraint():
    """
    What constraint forces the Bargmann phase = -1?

    For 4 unit vectors v_a, v_b, v_c, v_d in C^4:
    - All pairwise |<v_i|v_j>| = 1/sqrt(3)
    - The 4 vectors span a 3D subspace

    This is NOT a generic configuration!
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("THE CONSTRAINT")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    P = V[outer]

    # Gram matrix
    G = P @ P.conj().T

    print("\nGram matrix:")
    for i in range(4):
        row = " ".join(f"{G[i,j]:8.4f}" for j in range(4))
        print(f"  {row}")

    # Structure of G:
    # G_ii = 1 (unit vectors)
    # |G_ij| = 1/sqrt(3) for i != j

    # The Gram matrix G has determinant 0 (rank 3)
    det_G = np.linalg.det(G)
    print(f"\ndet(G) = {det_G:.6f}")

    # Eigenvalues
    eigs = np.linalg.eigvalsh(G)
    print(f"Eigenvalues: {eigs}")

    # One eigenvalue is 0 (rank 3)
    # The other 3 should sum to trace(G) = 4

    print(f"\nSum of positive eigenvalues: {sum(e for e in eigs if e > 0.01):.4f}")
    print(f"Trace of G: {np.trace(G):.4f}")

    # Key: the constraint is det(G) = 0
    # This forces a relationship between the off-diagonal elements

    print("\n" + "-" * 50)
    print("DET(G) = 0 CONSTRAINT")
    print("-" * 50)

    # For a 4x4 matrix with 1s on diagonal and |g_ij| = m for i != j:
    # det = ... (some formula involving the phases)

    # Let me denote G_ij = m * e^{i*phi_ij} for i != j
    # where m = 1/sqrt(3)

    m = 1 / np.sqrt(3)
    print(f"\nm = 1/sqrt(3) = {m:.6f}")
    print(f"m^2 = 1/3 = {m**2:.6f}")

    # The phases
    phi = {}
    for i in range(4):
        for j in range(4):
            if i != j:
                phi[(i,j)] = np.angle(G[i,j])
                k = round(6 * phi[(i,j)] / np.pi) % 12
                print(f"  phi[{i},{j}] = {phi[(i,j)]:.4f} rad = k={k}")


def algebraic_identity():
    """
    Try to find the algebraic identity that explains -1.

    For 4 vectors in a 3D subspace:
    v_0 = (1, 0, 0, 0) in some basis
    v_1, v_2, v_3 in the same 3D subspace

    There's a linear dependency: a_0*v_0 + a_1*v_1 + a_2*v_2 + a_3*v_3 = 0
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("ALGEBRAIC IDENTITY")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    P = V[outer]  # 4x4

    # Find the linear dependency
    # a @ P = 0 where a is a 4-vector
    U, S, Vh = np.linalg.svd(P.T)
    null = Vh[-1]  # Last row of Vh is null vector

    print(f"\nNull vector (linear dependency):")
    print(f"  a = {null}")

    # Verify: a @ P = 0
    check = null @ P
    print(f"  a @ P = {check}")
    print(f"  |a @ P| = {np.linalg.norm(check):.6e}")

    # The coefficients a_i give: sum_i a_i * v_i = 0
    # So: a_0*v_0 = -(a_1*v_1 + a_2*v_2 + a_3*v_3)

    print(f"\nLinear dependency: sum_i a_i * V[outer[i]] = 0")
    for i, p in enumerate(outer):
        print(f"  a[{i}] = {null[i]:.4f}")

    # Now: the Bargmann invariant
    # B = <0|1><1|2><2|3><3|0>

    # Using the dependency: V[0] = -(a_1/a_0)*V[1] - (a_2/a_0)*V[2] - (a_3/a_0)*V[3]

    # <0|1> = <V[0]|V[1]> = ...
    # This is getting complicated. Let me try a different approach.

    print("\n" + "-" * 50)
    print("PHASE FROM DETERMINANT")
    print("-" * 50)

    # The key identity: for a matrix M, det(M) gives phase info
    # Our Gram matrix G has det = 0, but we can extract sub-info

    G = P @ P.conj().T

    # The Bargmann 4-cycle is:
    # B = G[0,1] * G[1,2] * G[2,3] * G[3,0]

    B = G[0,1] * G[1,2] * G[2,3] * G[3,0]
    print(f"\nBargmann = G[0,1]*G[1,2]*G[2,3]*G[3,0] = {B:.6f}")
    print(f"Phase of Bargmann: {np.angle(B) / np.pi:.4f} * pi")

    # Compare to other products
    alt1 = G[0,1] * G[1,3] * G[3,2] * G[2,0]
    alt2 = G[0,2] * G[2,1] * G[1,3] * G[3,0]
    print(f"\nAlt cycle 0->1->3->2->0: {alt1:.6f}")
    print(f"Alt cycle 0->2->1->3->0: {alt2:.6f}")

    # The PRODUCT of all three?
    prod = B * alt1 * alt2
    print(f"\nProduct of all 3 cycles: {prod:.6f}")


def main():
    analyze_quaternion_structure()
    analyze_all_k4_phase_patterns()
    check_bargmann_formula()
    geometric_proof()
    find_the_constraint()
    algebraic_identity()

if __name__ == "__main__":
    main()
