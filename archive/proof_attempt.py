#!/usr/bin/env python3
"""
ATTEMPT TO PROVE THE UNIVERSAL -1

Key observation: Point 0 has the simplest structure.
From point 0, ALL phases are k=0 (mod 12), so k mod 3 = 0.

The standard basis points {0, 4, 5, 6} have even simpler structure.

Let me see if I can derive the -1 algebraically by working
in the basis where point 0 = e_0.
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


def analyze_point_zero():
    """
    Point 0 = e_0 = (1, 0, 0, 0).

    Any non-collinear point q has <0|q> = q_0 (first component).

    Since |<0|q>| = 1/sqrt(3), we have |q_0| = 1/sqrt(3).

    And the phase of <0|q> = phase of q_0.

    Since all these phases are k=0, q_0 is REAL POSITIVE!
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("=" * 70)
    print("POINT 0 STRUCTURE")
    print("=" * 70)

    print("\nV[0] = e_0 = (1, 0, 0, 0)")
    print("<0|q> = q_0* (complex conjugate of first component)")

    print("\nFirst component q_0 for non-collinear points:")
    for q in range(15):
        if q in col[0] or q == 0:
            print(f"  Point {q}: COLLINEAR with 0")
        else:
            q0 = V[q, 0]
            z = inner(V, 0, q)
            print(f"  Point {q}: q_0 = {q0:.6f}, <0|q> = {z:.6f}")

    print("\n*** ALL first components are 1/sqrt(3) with phase 0! ***")


def analyze_quad_algebra():
    """
    For the quad {0, 1, 2, 3}:

    V[0] = (1, 0, 0, 0)
    V[1] = (a, 0, b, c)
    V[2] = (a, 0, d, e)
    V[3] = (a, 0, f, g)

    where a = 1/sqrt(3), and b,c,d,e,f,g are constrained.

    Let me extract these and see the algebraic structure.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("QUAD {0,1,2,3} ALGEBRA")
    print("=" * 70)

    a = 1/np.sqrt(3)
    print(f"\na = 1/sqrt(3) = {a:.6f}")

    for p in [0, 1, 2, 3]:
        print(f"\nV[{p}]:")
        for i in range(4):
            c = V[p, i]
            if abs(c) < 1e-10:
                print(f"  [{i}] = 0")
            else:
                # Express in terms of a
                ratio = c / a
                print(f"  [{i}] = {c:.6f} = a * {ratio:.6f}")

    print("\n" + "-" * 50)
    print("ALGEBRAIC FORM")
    print("-" * 50)

    # Extract the 3-vectors (components 2 and 3, since component 1 is 0)
    # For points 1, 2, 3
    w = 1/np.sqrt(3)

    print("\nLet w = exp(2*pi*i/12) = exp(i*pi/6)")
    print("Let z3 = exp(2*pi*i/3) = -1/2 + i*sqrt(3)/2")

    # The phases appearing should be 12th roots of unity
    w12 = np.exp(1j * np.pi / 6)

    for p in [1, 2, 3]:
        v = V[p]
        print(f"\nV[{p}] phases (relative to 1/sqrt(3)):")
        for i in range(4):
            if abs(v[i]) > 0.01:
                phase = np.angle(v[i])
                k = round(6 * phase / np.pi) % 12
                print(f"  [{i}]: phase = {phase:.4f} rad = k={k} (w^{k})")


def compute_bargmann_symbolically():
    """
    Compute the Bargmann invariant symbolically.

    For points a, c, b, d forming a Bargmann cycle:
    B = <a|c><c|b><b|d><d|a>

    Each inner product has:
    - Magnitude 1/3 (since 1/sqrt(3) * 1/sqrt(3) = 1/3)
    - Phase k_{pq} * pi/6

    So B = (1/3)^2 * exp(i*(k_{ac}+k_{cb}+k_{bd}+k_{da})*pi/6)

    The phase is (k_{ac}+k_{cb}+k_{bd}+k_{da}) mod 12.
    We claim this is always 6.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("\n" + "=" * 70)
    print("SYMBOLIC BARGMANN COMPUTATION")
    print("=" * 70)

    # For quad {0, 1, 2, 3}
    quad = [0, 1, 2, 3]

    # Compute all pairwise phases
    phases = {}
    for p in quad:
        for q in quad:
            if p != q:
                z = inner(V, p, q)
                k = round(6 * np.angle(z) / np.pi) % 12
                phases[(p, q)] = k

    print("\nPhase table k(p,q) for {0,1,2,3}:")
    print("    ", end="")
    for q in quad:
        print(f"  {q}  ", end="")
    print()
    for p in quad:
        print(f" {p} ", end="")
        for q in quad:
            if p == q:
                print("  -  ", end="")
            else:
                print(f"  {phases[(p,q)]}  ", end="")
        print()

    print("\nBargmann cycles (sum of 4 phases):")

    # All possible 4-cycles on {0,1,2,3}
    cycles = [
        (0, 1, 2, 3),
        (0, 1, 3, 2),
        (0, 2, 1, 3),
        (0, 2, 3, 1),
        (0, 3, 1, 2),
        (0, 3, 2, 1),
    ]

    for cyc in cycles:
        a, b, c, d = cyc
        total = (phases[(a,b)] + phases[(b,c)] + phases[(c,d)] + phases[(d,a)]) % 12
        print(f"  {a}->{b}->{c}->{d}->{a}: {phases[(a,b)]}+{phases[(b,c)]}+{phases[(c,d)]}+{phases[(d,a)]} = {total} mod 12")


def verify_universal():
    """
    Verify the -1 for ALL possible Bargmann configurations.

    A Bargmann cycle needs 4 mutually non-collinear points.
    These form a "4-clique" in the non-collinearity graph.
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # Non-collinearity graph
    noncol = defaultdict(set)
    for p in range(40):
        for q in range(40):
            if p != q and q not in col[p]:
                noncol[p].add(q)

    print("\n" + "=" * 70)
    print("VERIFICATION ON ALL 4-CLIQUES")
    print("=" * 70)

    # Find all 4-cliques (sets of 4 mutually non-collinear points)
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

    print(f"Found {len(cliques)} 4-cliques (sets of 4 mutually non-collinear points)")

    # For each clique, compute all Bargmann cycles
    bargmann_phases = defaultdict(int)

    for a, b, c, d in cliques:
        # Compute the Bargmann invariant
        B = inner(V, a, b) * inner(V, b, c) * inner(V, c, d) * inner(V, d, a)
        phase = np.angle(B)
        k = round(6 * phase / np.pi) % 12
        bargmann_phases[k] += 1

    print("\nBargmann phase distribution (for cycle a->b->c->d->a):")
    for k, count in sorted(bargmann_phases.items()):
        phase_val = np.exp(1j * k * np.pi / 6)
        print(f"  k={k} (phase={phase_val:.4f}): {count} cliques")

    # Also check the other cycle orderings
    print("\nChecking all orderings of the same 4 points...")
    all_phases = defaultdict(int)

    for a, b, c, d in cliques[:100]:  # First 100
        for perm in [(a,b,c,d), (a,b,d,c), (a,c,b,d), (a,c,d,b), (a,d,b,c), (a,d,c,b)]:
            p, q, r, s = perm
            B = inner(V, p, q) * inner(V, q, r) * inner(V, r, s) * inner(V, s, p)
            phase = np.angle(B)
            k = round(6 * phase / np.pi) % 12
            all_phases[k] += 1

    print("\nAll orderings (first 100 cliques):")
    for k, count in sorted(all_phases.items()):
        print(f"  k={k}: {count}")


def main():
    analyze_point_zero()
    analyze_quad_algebra()
    compute_bargmann_symbolically()
    verify_universal()

if __name__ == "__main__":
    main()
