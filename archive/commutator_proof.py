#!/usr/bin/env python3
"""
WHY IS THE BARGMANN 4-CYCLE ALWAYS -1?

This is the central mystery. Let me work through this algebraically.

The Bargmann 4-cycle for a move swapping c->d while keeping {a,b} fixed:
    <c|a><a|d><d|b><b|c> = -1/9

Note: The VALUE is -1/9, not -1. The PHASE is -1.
Since all magnitudes are 1/3, and 4 inner products multiply: (1/3)^4... wait no.

Actually: |<p|q>| = 1/sqrt(3) for all non-collinear pairs.
So the magnitude is (1/sqrt(3))^4 = 1/9. Check!

The phase being exactly pi (i.e., -1) is the deep fact.

Let me prove this algebraically.
"""

import numpy as np
from pathlib import Path
import pandas as pd
from collections import defaultdict

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

# =============================================================================
# ALGEBRAIC INVESTIGATION
# =============================================================================

def analyze_inner_products():
    """
    Look at the actual structure of inner products.

    Key insight: If we normalize so |<p|q>| = 1, what phases appear?
    """
    V = load_rays()
    lines = load_lines()

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("="*70)
    print("INNER PRODUCT PHASE STRUCTURE")
    print("="*70)

    # Collect all inner products, normalized
    phases = []
    for p in range(40):
        for q in range(p+1, 40):
            if q in col[p]:
                continue
            z = inner(V, p, q)
            phase = np.angle(z)
            phases.append((p, q, z, phase))

    # Group by phase
    phase_groups = defaultdict(list)
    for p, q, z, phase in phases:
        k = round(6 * phase / np.pi) % 12
        phase_groups[k].append((p, q, z))

    print(f"\nTotal non-collinear pairs: {len(phases)}")
    print("\nPhase distribution (k in Z_12):")
    for k in sorted(phase_groups.keys()):
        print(f"  k={k}: {len(phase_groups[k])} pairs")

    return phase_groups

def analyze_specific_triads():
    """
    Look at specific triads to understand the pattern.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "="*70)
    print("SPECIFIC TRIAD ANALYSIS")
    print("="*70)

    # Take the first K4 component: outer quad = {0, 1, 2, 3}
    # All four are mutually non-collinear and share center = {4, 13, 22, 31}
    outer = [0, 1, 2, 3]

    print(f"\nOuter quad: {outer}")
    print("Checking mutual non-collinearity...")
    for i, p in enumerate(outer):
        for q in outer[i+1:]:
            print(f"  {p},{q}: collinear={q in col[p]}, <{p}|{q}>={inner(V, p, q):.6f}")

    # Common neighbors
    cn = col[outer[0]]
    for p in outer[1:]:
        cn = cn & col[p]
    print(f"Common neighbors (center quad): {sorted(cn)}")

    # Compute all inner products in this 4-set
    print("\nInner product matrix for {0,1,2,3}:")
    for p in outer:
        row = []
        for q in outer:
            if p == q:
                row.append("  1.000  ")
            else:
                z = inner(V, p, q)
                row.append(f"{z.real:+.3f}{z.imag:+.3f}j")
        print("  " + " ".join(row))

    # Now let's trace through a Bargmann cycle
    print("\n" + "-"*50)
    print("BARGMANN CYCLE TRACE: {0,1,2} -> {0,1,3}")
    print("-"*50)
    print("Swapping 2->3 while keeping {0,1}")
    print("Cycle: <2|0><0|3><3|1><1|2>")

    z20 = inner(V, 2, 0)
    z03 = inner(V, 0, 3)
    z31 = inner(V, 3, 1)
    z12 = inner(V, 1, 2)

    print(f"  <2|0> = {z20:.6f}")
    print(f"  <0|3> = {z03:.6f}")
    print(f"  <3|1> = {z31:.6f}")
    print(f"  <1|2> = {z12:.6f}")

    product = z20 * z03 * z31 * z12
    print(f"\nProduct = {product:.6f}")
    print(f"Magnitude = {abs(product):.6f} (should be 1/9 = {1/9:.6f})")
    print(f"Phase = {np.angle(product):.6f} rad = {np.angle(product)/np.pi:.6f} pi")

    # THE KEY QUESTION: Why is this phase always pi?
    # Let's look at the phase contributions
    print("\n" + "-"*50)
    print("PHASE DECOMPOSITION")
    print("-"*50)
    k20 = round(6 * np.angle(z20) / np.pi) % 12
    k03 = round(6 * np.angle(z03) / np.pi) % 12
    k31 = round(6 * np.angle(z31) / np.pi) % 12
    k12 = round(6 * np.angle(z12) / np.pi) % 12

    print(f"  k(2,0) = {k20}")
    print(f"  k(0,3) = {k03}")
    print(f"  k(3,1) = {k31}")
    print(f"  k(1,2) = {k12}")
    print(f"  Sum mod 12 = {(k20 + k03 + k31 + k12) % 12}")

def analyze_algebraic_constraint():
    """
    The real question: What algebraic constraint forces the Bargmann phase = -1?

    For an equiangular tight frame in C^d with |<p|q>| = c for all p != q,
    there are known constraints from the Welch bound and SIC-POVM theory.

    But the universal -1 commutator is stronger. Let me look for it.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "="*70)
    print("ALGEBRAIC CONSTRAINT ANALYSIS")
    print("="*70)

    # Let's check: is there a simple relation between <a|b><b|c><c|a>?
    # The triad holonomy is either +i or -i.
    # And the 4-cycle is always -1/9.

    # Hypothesis: The rays form a SIC-POVM or related structure.
    #
    # In dimension 4, a SIC-POVM has 16 vectors, not 40.
    # But W33 has 40 points.
    #
    # However, 40 = 4 * 10, and the lines are special...

    print("\nChecking line structure:")
    for i, L in enumerate(lines):
        print(f"  Line {i}: {L}")
        # Check: are points on a line orthogonal?
        for j, p in enumerate(L):
            for q in L[j+1:]:
                z = inner(V, p, q)
                print(f"    <{p}|{q}> = {z:.6f}")

    print("\n" + "-"*50)
    print("KEY OBSERVATION")
    print("-"*50)
    print("""
    Points on the same line are ORTHOGONAL (<p|q> = 0).

    This means the 4 points on each line form an orthonormal basis of C^4!

    There are 15 lines, each giving an orthonormal basis.
    These are related to MUTUALLY UNBIASED BASES (MUBs)!

    In C^4, there are at most 5 MUBs. We have 15 lines...
    So this is not a standard MUB configuration.

    But the structure is similar: equiangular frames with orthogonality constraints.
    """)

    # Let's verify: do lines give orthonormal bases?
    print("\nVerifying orthonormality on lines:")
    for i, L in enumerate(lines[:3]):  # Check first 3
        print(f"\nLine {i}: {L}")
        # Build Gram matrix
        G = np.zeros((4, 4), dtype=np.complex128)
        for j, p in enumerate(L):
            for k, q in enumerate(L):
                G[j, k] = inner(V, p, q)
        # Should be identity
        print(f"  Gram matrix (should be I_4):")
        print(f"    Max off-diagonal: {np.max(np.abs(G - np.eye(4))):.2e}")

def analyze_projection_structure():
    """
    Another approach: What if we think of points as rank-1 projectors?

    |p><p| is a projector. The inner product structure tells us about
    the trace of products: Tr(|p><p| |q><q|) = |<p|q>|^2.
    """
    V = load_rays()

    print("\n" + "="*70)
    print("PROJECTOR STRUCTURE")
    print("="*70)

    # Build projectors for first few points
    P = {}
    for i in range(5):
        P[i] = np.outer(V[i], V[i].conj())

    print("\nProjectors P_i = |i><i|:")
    for i in range(3):
        print(f"\nP_{i}:")
        for row in P[i]:
            print("  " + " ".join(f"{z.real:+.3f}" for z in row))

    # Check: P_i P_j for non-collinear i,j
    print("\nP_0 * P_1 (non-collinear):")
    PP = P[0] @ P[1]
    for row in PP:
        print("  " + " ".join(f"{z.real:+.3f}{z.imag:+.3f}j" for z in row))

    print(f"\nTr(P_0 P_1) = {np.trace(PP):.6f}")
    print(f"|<0|1>|^2 = {abs(inner(V, 0, 1))**2:.6f}")

def analyze_clifford_connection():
    """
    The universal -1 in the 4-cycle suggests Clifford algebra.

    In Cl(4) or Cl(3,1), the generators gamma_i satisfy:
        gamma_i gamma_j = -gamma_j gamma_i (i != j)

    This gives exactly the -1 anticommutator.

    Can we identify the C^4 rays with spinors?
    """
    V = load_rays()

    print("\n" + "="*70)
    print("CLIFFORD / SPINOR CONNECTION")
    print("="*70)

    # Standard basis points
    basis = [0, 4, 5, 6]
    print(f"\nStandard basis points: {basis}")
    for p in basis:
        print(f"  V[{p}] = {V[p]}")

    # These are just e_0, e_1, e_2, e_3
    # So we have a distinguished orthonormal basis.

    # The 36 non-basis points must be superpositions.
    # Let's look at their structure.
    print("\nNon-basis points (first 10):")
    for p in range(1, 11):
        if p in basis:
            continue
        # Express in terms of basis
        coeffs = [inner(V, b, p) for b in basis]
        nonzero = [(i, c) for i, c in enumerate(coeffs) if abs(c) > 1e-10]
        print(f"  Point {p}: " + ", ".join(f"e_{i}*({c:.4f})" for i, c in nonzero))

    print("\n" + "-"*50)
    print("HYPOTHESIS: SPINOR STATES")
    print("-"*50)
    print("""
    The 40 points might represent spinor states or Bloch vectors
    in a 4-dimensional spinor space.

    The standard basis {0, 4, 5, 6} = {e_0, e_1, e_2, e_3} are
    pure computational basis states.

    Other points are superpositions with specific phases.

    The -1 commutator arises from the FERMIONIC nature of spinors:
    swapping two fermions gives a -1 phase.

    The Z_12 phases might encode both:
    - Z_4: quaternionic phase (1, i, -1, -i) from SU(2) spinors
    - Z_3: color charge or triality from some other structure
    """)

def main():
    analyze_inner_products()
    analyze_specific_triads()
    analyze_algebraic_constraint()
    analyze_projection_structure()
    analyze_clifford_connection()

if __name__ == "__main__":
    main()
