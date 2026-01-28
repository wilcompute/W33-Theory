#!/usr/bin/env python3
"""
CLIFFORD ALGEBRA SEARCH

The universal -1 commutator screams Clifford algebra.

In Cl(n), generators satisfy: gamma_i * gamma_j = -gamma_j * gamma_i for i != j

The 4D complex space suggests Cl(4) or Cl(3,1).

Let me see if I can identify the Clifford structure explicitly.
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


def analyze_clifford_structure():
    """
    The Clifford algebra Cl(4,C) has generators gamma_0, gamma_1, gamma_2, gamma_3.

    The space C^4 is the spinor representation.

    Standard gamma matrices (Dirac representation):
    gamma_0 = [[I, 0], [0, -I]]
    gamma_i = [[0, sigma_i], [-sigma_i, 0]] for i=1,2,3

    Let's see if our rays have any relation to these.
    """
    V = load_rays()

    print("=" * 70)
    print("CLIFFORD STRUCTURE SEARCH")
    print("=" * 70)

    # Standard basis points: 0, 4, 5, 6
    # These are e_0, e_1, e_2, e_3
    basis_pts = [0, 4, 5, 6]

    print("\nStandard basis rays:")
    for p in basis_pts:
        print(f"  V[{p}] = {V[p]}")

    # The Dirac gamma matrices in 4D:
    # gamma_0 = diag(1, 1, -1, -1)
    # gamma_1 = [[0, sigma_1], [sigma_1, 0]]
    # etc.

    # But our standard basis is just e_0, e_1, e_2, e_3.
    # The Clifford action should mix these.

    # Alternative view: The 4 standard basis vectors span the spinor space.
    # A point like V[1] = (1/sqrt(3))(e_0 + ce_2 + de_3) is a superposition.

    # Let's look at the GROUP ACTION on these vectors.
    # What group preserves the inner product structure?

    print("\n" + "-" * 50)
    print("LOOKING FOR CLIFFORD ACTION")
    print("-" * 50)

    # The Clifford group acts on spinors.
    # For gamma matrices: gamma_i |psi> -> different spinor

    # Let me check: are there any transformations that
    # permute the 40 points while preserving inner products?

    # First, let's see what SU(4) orbit the points form.
    # If all 40 points are SU(4)-equivalent, they're on a single orbit.

    # Check: do all points have the same "norm pattern"?
    print("\nAnalyzing vector component patterns:")
    patterns = defaultdict(list)
    for p in range(40):
        # Pattern: which components are nonzero and what magnitudes
        nz = tuple(sorted(i for i in range(4) if abs(V[p, i]) > 0.01))
        mags = tuple(sorted(round(abs(V[p, i]), 4) for i in range(4)))
        patterns[(nz, mags)].append(p)

    print(f"Found {len(patterns)} distinct patterns:")
    for (nz, mags), pts in sorted(
        patterns.items(), key=lambda x: len(x[1]), reverse=True
    ):
        print(f"  Nonzero: {nz}, Mags: {mags} -> {len(pts)} points")
        if len(pts) <= 5:
            print(f"    Points: {pts}")


def analyze_symmetry_group():
    """
    What is the symmetry group of the 40-point configuration?

    It should be a subgroup of U(4) preserving:
    1. The 40 unit vectors
    2. The collinearity structure
    3. The inner product phases
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("SYMMETRY GROUP ANALYSIS")
    print("=" * 70)

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # The automorphism group of W33 (as incidence structure) is known.
    # For GQ(3,3), the automorphism group is related to PSU(4,2).

    # But we have EXTRA structure: the phases!
    # The phase-preserving automorphisms might be smaller.

    print("\nChecking for simple symmetries...")

    # Try: multiply all rays by e^{i*theta}. This is a global U(1).
    # Does this preserve the phase structure? Yes, trivially.

    # Try: permute coordinates. Does e_0 <-> e_1 preserve structure?
    P01 = np.array(
        [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.complex128
    )

    print("\nApplying coordinate swap P_{01} (e_0 <-> e_1):")
    # Check if this maps the 40 points to themselves
    V_transformed = (P01 @ V.T).T

    matches = []
    for p in range(40):
        v_new = V_transformed[p]
        # Find which original point this matches
        for q in range(40):
            if np.allclose(v_new, V[q]) or np.allclose(v_new, -V[q]):
                matches.append((p, q, np.allclose(v_new, -V[q])))
                break
        else:
            matches.append((p, None, None))

    unmatched = [m for m in matches if m[1] is None]
    print(f"  Unmatched points: {len(unmatched)}")
    if len(unmatched) < 10:
        for p, _, _ in unmatched:
            print(f"    Point {p}: {V[p]} -> {V_transformed[p]}")

    # Try: complex conjugation
    print("\nApplying complex conjugation:")
    V_conj = V.conj()

    matches_conj = []
    for p in range(40):
        v_new = V_conj[p]
        for q in range(40):
            if np.allclose(v_new, V[q], rtol=1e-5):
                matches_conj.append((p, q))
                break
            if np.allclose(v_new, -V[q], rtol=1e-5):
                matches_conj.append((p, q, "neg"))
                break
        else:
            matches_conj.append((p, None))

    conj_matches = [m for m in matches_conj if len(m) >= 2 and m[1] is not None]
    print(f"  Points with conjugate match: {len(conj_matches)}")


def analyze_projective_structure():
    """
    The 40 points in C^4 define 40 points in CP^3 (projective space).

    The incidence structure should be visible projectively.
    Lines in W33 correspond to lines in CP^3?
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("PROJECTIVE STRUCTURE")
    print("=" * 70)

    # In CP^3, a "line" (projective line) is a P^1 inside P^3.
    # Algebraically, it's the projectivization of a 2D subspace of C^4.

    # Do our W33 "lines" correspond to projective lines?
    # A W33 line has 4 collinear (orthogonal) points.
    # The span of 4 orthogonal unit vectors is all of C^4, not a 2D subspace!

    # So W33 lines are NOT projective lines.
    # Instead, a W33 line is a FRAME (complete orthonormal basis).

    print("\nW33 lines vs projective lines:")
    print("  A W33 line = an orthonormal frame = 4 points spanning C^4")
    print("  A P^3 line = a 2D subspace = P^1 inside P^3")
    print("  These are DIFFERENT objects!")

    # What IS the relationship?
    # The 4 points on a W33 line determine a distinguished basis.
    # Any linear combination is in the same C^4.
    # But as projective points, they're 4 distinct points in P^3.

    # Interesting: 4 generic points in P^3 span P^3 (no 3 on a line).
    # Our 4 points are special: they're mutually orthogonal.

    # In CP^3, orthogonal points w.r.t. standard Hermitian form
    # are "conjugate" or "polar" to each other.

    print("\nOrthogonality in CP^3:")
    print("  Two points p, q in CP^3 are 'orthogonal' if <v_p|v_q> = 0")
    print("  (where v_p, v_q are representative vectors)")
    print("  An orthonormal frame in C^4 -> 4 mutually orthogonal points in CP^3")


def analyze_triality():
    """
    The Z_3 factor suggests triality.

    In Spin(8), there are three 8-dimensional representations
    related by triality. The vector, spinor, and co-spinor.

    Does W33 have a triality structure?
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("TRIALITY INVESTIGATION")
    print("=" * 70)

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # For each point, count how many points have each Z_3 phase
    print("\nZ_3 phase distribution from point 0:")

    k3_count = defaultdict(int)
    for q in range(40):
        if q in col[0] or q == 0:
            continue
        z = inner(V, 0, q)
        k = round(6 * np.angle(z) / np.pi) % 12
        k3 = k % 3
        k3_count[k3] += 1

    print(f"  k mod 3 = 0: {k3_count[0]} points")
    print(f"  k mod 3 = 1: {k3_count[1]} points")
    print(f"  k mod 3 = 2: {k3_count[2]} points")

    # Do a few more reference points
    print("\nZ_3 distribution from other points:")
    for ref in [1, 4, 10]:
        k3_count = defaultdict(int)
        for q in range(40):
            if q in col[ref] or q == ref:
                continue
            z = inner(V, ref, q)
            k = round(6 * np.angle(z) / np.pi) % 12
            k3 = k % 3
            k3_count[k3] += 1
        print(
            f"  From {ref}: k3=0:{k3_count[0]}, k3=1:{k3_count[1]}, k3=2:{k3_count[2]}"
        )


def analyze_why_minus_one():
    """
    The deepest question: WHY is the Bargmann 4-cycle always -1?

    Let me think about this geometrically.

    The 4 points a, b, c, d form a "rectangle" in some sense:
    - {a,b} are kept fixed
    - c and d are swapped
    - All 4 are mutually non-collinear

    The Bargmann phase measures the "twist" around this rectangle.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("WHY -1? GEOMETRIC ANALYSIS")
    print("=" * 70)

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    # Look at the first K4 component: outer quad {0, 1, 2, 3}
    quad = [0, 1, 2, 3]

    print(f"\nAnalyzing quad {quad}:")

    # Build the 6 inner products (4 choose 2)
    print("\nInner products <p|q>:")
    for i, p in enumerate(quad):
        for q in quad[i + 1 :]:
            z = inner(V, p, q)
            k = round(6 * np.angle(z) / np.pi) % 12
            print(f"  <{p}|{q}> = {z:.6f}, k = {k}")

    # The Bargmann invariant for the whole quad (any 4-cycle)
    print("\nBargmann 4-cycles:")
    # There are 3 ways to pair up 4 points into 2 pairs
    pairings = [
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    ]

    for p1, p2 in pairings:
        a, b = p1
        c, d = p2
        # Bargmann cycle: a -> c -> b -> d -> a
        B = inner(V, a, c) * inner(V, c, b) * inner(V, b, d) * inner(V, d, a)
        print(f"  Pairing ({a},{b})|({c},{d}): B = {B:.6f}")

    # The KEY insight might be:
    # Any 4-cycle on 4 mutually non-collinear points gives phase -1.
    # This is because the points form a "twisted rectangle" in CP^3.

    print("\n" + "-" * 50)
    print("HYPOTHESIS: HOPF FIBRATION")
    print("-" * 50)
    print("""
    CP^3 is the base of the Hopf fibration S^7 -> CP^3.

    A "twisted rectangle" in CP^3 can have holonomy
    related to the Hopf invariant.

    The universal -1 might come from:
    - The fundamental group pi_1(SO(n)) = Z_2
    - A spin structure giving fermionic signs
    - The Hopf map S^3 -> S^2 which has pi_3(S^2) = Z

    Need to think more about this...
    """)


def main():
    analyze_clifford_structure()
    analyze_symmetry_group()
    analyze_projective_structure()
    analyze_triality()
    analyze_why_minus_one()


if __name__ == "__main__":
    main()
