#!/usr/bin/env python3
"""
K4 COMPONENTS ARE SPECIAL

Key discovery: The -1 Bargmann phase occurs for exactly 90 4-cliques.
These must be the 90 K4 components!

What makes them special?
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


def identify_k4_cliques():
    """
    The K4 components are 4-cliques {a,b,c,d} where:
    - All 4 are mutually non-collinear
    - They have exactly 4 COMMON neighbors (the center quad)

    Find these explicitly.
    """
    V = load_rays()
    lines = load_lines()

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # Non-collinearity
    noncol = defaultdict(set)
    for p in range(40):
        for q in range(40):
            if p != q and q not in col[p]:
                noncol[p].add(q)

    print("=" * 70)
    print("IDENTIFYING K4 COMPONENTS")
    print("=" * 70)

    # Find all 4-cliques
    cliques = []
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
                    cliques.append((a, b, c, d))

    print(f"Total 4-cliques: {len(cliques)}")

    # For each clique, compute common neighbors
    k4_cliques = []
    other_cliques = []

    for quad in cliques:
        a, b, c, d = quad
        common = col[a] & col[b] & col[c] & col[d]
        if len(common) == 4:
            k4_cliques.append((quad, tuple(sorted(common))))
        else:
            other_cliques.append((quad, len(common)))

    print(f"K4 cliques (4 common neighbors): {len(k4_cliques)}")
    print(f"Other cliques: {len(other_cliques)}")

    # Check Bargmann phase for K4 cliques
    print("\n" + "-" * 50)
    print("BARGMANN PHASES FOR K4 CLIQUES")
    print("-" * 50)

    k4_phases = defaultdict(int)
    for (quad, center), _ in zip(k4_cliques, range(10)):  # First 10
        a, b, c, d = quad
        B = inner(V, a, b) * inner(V, b, c) * inner(V, c, d) * inner(V, d, a)
        k = round(6 * np.angle(B) / np.pi) % 12
        print(f"  {quad} (center={center}): Bargmann k = {k}")

    for quad, center in k4_cliques:
        a, b, c, d = quad
        B = inner(V, a, b) * inner(V, b, c) * inner(V, c, d) * inner(V, d, a)
        k = round(6 * np.angle(B) / np.pi) % 12
        k4_phases[k] += 1

    print(f"\nAll K4 Bargmann phases:")
    for k, count in sorted(k4_phases.items()):
        print(f"  k={k}: {count}")

    # Check Bargmann phase for non-K4 cliques
    print("\n" + "-" * 50)
    print("BARGMANN PHASES FOR NON-K4 CLIQUES")
    print("-" * 50)

    other_phases = defaultdict(int)
    for quad, n_common in other_cliques:
        a, b, c, d = quad
        B = inner(V, a, b) * inner(V, b, c) * inner(V, c, d) * inner(V, d, a)
        k = round(6 * np.angle(B) / np.pi) % 12
        other_phases[k] += 1

    print(f"Non-K4 Bargmann phases:")
    for k, count in sorted(other_phases.items()):
        print(f"  k={k}: {count}")

    return k4_cliques, other_cliques


def analyze_what_makes_k4_special():
    """
    What geometric/algebraic property distinguishes K4 cliques?

    Hypothesis: The 4 common neighbors form a LINE (orthonormal basis).
    The outer quad is somehow "dual" to this line.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # Find a K4 component
    # We know {0,1,2,3} is one, with center {4,13,22,31}

    outer = (0, 1, 2, 3)
    center = (4, 13, 22, 31)

    print("\n" + "=" * 70)
    print("ANALYZING K4 COMPONENT {0,1,2,3}")
    print("=" * 70)

    print(f"\nOuter quad: {outer}")
    print(f"Center quad: {center}")

    # Check: is center a line?
    print("\nIs center {4,13,22,31} a line (mutually orthogonal)?")
    for p in center:
        for q in center:
            if p < q:
                z = inner(V, p, q)
                print(f"  <{p}|{q}> = {z:.6f}")

    # The center points should be mutually orthogonal!
    # That means center is a LINE in W33.

    # Find which line contains the center
    for i, L in enumerate(lines):
        if set(L) == set(center):
            print(f"\nCenter is line {i}: {L}")
            break

    # Now: what's the relationship between outer and center?
    print("\n" + "-" * 50)
    print("OUTER-CENTER RELATIONSHIP")
    print("-" * 50)

    print("\nInner products between outer and center:")
    for p in outer:
        row = []
        for q in center:
            z = inner(V, p, q)
            row.append(f"{abs(z):.3f}")
        print(f"  Point {p}: " + " ".join(row))

    # Each outer point should be collinear with some center points
    print("\nCollinearity structure:")
    for p in outer:
        cols = [q for q in center if q in col[p]]
        print(f"  Point {p} is collinear with center points: {cols}")


def analyze_dual_structure():
    """
    The K4 component structure:
    - Center quad C = 4 mutually orthogonal points (a line)
    - Outer quad P = 4 points, each collinear with all of C

    This is like a "hypercube" structure in the incidence geometry!
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "=" * 70)
    print("DUAL STRUCTURE ANALYSIS")
    print("=" * 70)

    # For each line, find its "perpendicular" quad
    print("\nFor each line (center), find points collinear with ALL of them:")

    k4_found = []
    for i, center in enumerate(lines[:10]):  # First 10 lines
        # Find points collinear with all center points
        perp = set(range(40))
        for c in center:
            perp &= col[c]
        perp -= set(center)  # Remove the center itself

        print(f"\nLine {i}: {center}")
        print(f"  Points collinear with all: {sorted(perp)}")

        # Check if perp forms a clique in non-collinearity
        if len(perp) >= 4:
            perp_list = sorted(perp)
            # Check mutual non-collinearity
            noncol_pairs = 0
            col_pairs = 0
            for p, q in combinations(perp_list, 2):
                if q in col[p]:
                    col_pairs += 1
                else:
                    noncol_pairs += 1
            print(
                f"  Among perp: {noncol_pairs} non-collinear pairs, {col_pairs} collinear pairs"
            )

            if col_pairs == 0 and len(perp) == 4:
                print(f"  *** OUTER QUAD FOUND: {perp_list}")
                k4_found.append((tuple(perp_list), center))

    print(f"\n*** Found {len(k4_found)} K4 components from first 10 lines ***")


def prove_minus_one_algebraically():
    """
    Attempt to prove the -1 phase for K4 components.

    For a K4 component with center C = {c0, c1, c2, c3} (orthonormal basis)
    and outer P = {p0, p1, p2, p3}:

    Each pi is a superposition in the C basis:
        p_i = sum_j alpha_{ij} c_j

    The phases must be related...
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("ALGEBRAIC PROOF ATTEMPT")
    print("=" * 70)

    # Use component {0,1,2,3} with center {4,13,22,31}
    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print(f"\nOuter: {outer}, Center: {center}")

    # Express each outer point in center basis
    # <c_j | p_i> = coefficient of c_j in p_i
    print("\nExpansion coefficients <center|outer>:")
    alpha = np.zeros((4, 4), dtype=np.complex128)
    for i, p in enumerate(outer):
        for j, c in enumerate(center):
            alpha[i, j] = inner(V, c, p)

    print("      c=4      c=13     c=22     c=31")
    for i, p in enumerate(outer):
        row = " ".join(f"{alpha[i,j]:.4f}" for j in range(4))
        print(f"p={p}: {row}")

    # The key: what's the structure of alpha?
    print("\nMagnitude of alpha coefficients:")
    for i in range(4):
        mags = [abs(alpha[i, j]) for j in range(4)]
        print(f"  Row {i}: {[f'{m:.4f}' for m in mags]}")

    # Each outer point should have |alpha| = 0 for one center, 1 for another,
    # and some intermediate for the rest... let me see.

    print("\n" + "-" * 50)
    print("KEY OBSERVATION")
    print("-" * 50)

    # The pattern: each outer point is orthogonal to exactly one center point
    # (because they're collinear in W33!)

    for i, p in enumerate(outer):
        zeros = [j for j in range(4) if abs(alpha[i, j]) < 0.01]
        nonzeros = [j for j in range(4) if abs(alpha[i, j]) > 0.01]
        print(
            f"  Outer {p}: orthogonal to center indices {zeros}, nonzero at {nonzeros}"
        )


def main():
    identify_k4_cliques()
    analyze_what_makes_k4_special()
    analyze_dual_structure()
    prove_minus_one_algebraically()


if __name__ == "__main__":
    main()
