#!/usr/bin/env python3
"""
AUTOMORPHISM GROUP STUDY

The W33 structure has multiple levels of symmetry:
1. Incidence geometry automorphisms (preserving collinearity)
2. Phase-preserving automorphisms (also preserving Z_12 phases)
3. Ray realization automorphisms (unitary transformations preserving rays)

For physics interpretation, we need to understand what symmetries are intrinsic.

Known: The automorphism group of GQ(3,3) is related to PSU(4,2).
But our ray realization adds extra structure (phases).
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


def analyze_point_symmetries():
    """
    Look for symmetries among the 40 points.

    Key observation: Point 0 is special (standard basis e0).
    How many points have the same "neighborhood structure"?
    """
    V = load_rays()
    lines = load_lines()

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    print("=" * 70)
    print("POINT SYMMETRY ANALYSIS")
    print("=" * 70)

    # For each point, compute a "signature" based on phase distribution
    print("\nPhase distribution from each point to non-collinear neighbors:")

    signatures = {}
    for p in range(40):
        k_counts = defaultdict(int)
        for q in range(40):
            if q != p and q not in col[p]:
                z = inner(V, p, q)
                k = round(6 * np.angle(z) / np.pi) % 12
                k_counts[k] += 1
        sig = tuple(sorted(k_counts.items()))
        signatures[p] = sig

    # Group points by signature
    sig_groups = defaultdict(list)
    for p, sig in signatures.items():
        sig_groups[sig].append(p)

    print(f"\nFound {len(sig_groups)} distinct phase signatures:")
    for sig, pts in sorted(sig_groups.items(), key=lambda x: -len(x[1])):
        print(f"  {len(pts)} points: {pts[:10]}{'...' if len(pts) > 10 else ''}")
        print(f"    Signature: {dict(sig)}")


def check_coordinate_permutations():
    """
    Check if permuting coordinates preserves the structure.

    The standard basis is {0, 4, 5, 6} = {e0, e1, e2, e3}.
    Permuting e_i -> e_j should map W33 to itself.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("COORDINATE PERMUTATION SYMMETRY")
    print("=" * 70)

    # Standard basis points
    std_basis = {0: 0, 4: 1, 5: 2, 6: 3}
    print(f"Standard basis: point -> coordinate: {std_basis}")

    # Try permutation: e0 <-> e1
    P = np.array([[0, 1, 0, 0],
                  [1, 0, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]], dtype=np.complex128)

    print("\nApplying e0 <-> e1 (swap coordinates 0 and 1):")

    # Transform all rays
    V_new = (P @ V.T).T

    # Find matching: new ray -> original point
    matches = {}
    for p in range(40):
        for q in range(40):
            if np.allclose(V_new[p], V[q]) or np.allclose(V_new[p], -V[q]):
                matches[p] = q
                break

    print(f"  Found {len(matches)} matches out of 40")

    if len(matches) == 40:
        print("  This is an automorphism!")
        # Print the permutation
        print(f"  Permutation: {matches}")
    else:
        # Show unmatched
        unmatched = [p for p in range(40) if p not in matches]
        print(f"  Unmatched points: {unmatched[:10]}")


def check_phase_rotation():
    """
    Check if global phase rotation preserves structure.

    Multiply all rays by e^{i*theta}. This changes all phases by the same amount.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("GLOBAL PHASE ROTATION")
    print("=" * 70)

    # This is trivially an automorphism of the ray realization
    # (up to overall phase, which is unphysical)
    print("Global phase e^{i*theta} is a U(1) symmetry of the rays.")
    print("It shifts all k values by the same amount (mod 12).")
    print("So k -> k + delta (mod 12) is a symmetry.")


def find_unitary_automorphisms():
    """
    Search for unitary transformations U such that U*V maps rays to rays.

    This is the group of ray realization automorphisms.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("UNITARY AUTOMORPHISM SEARCH")
    print("=" * 70)

    # Strategy: An automorphism must map the standard basis line to SOME line.
    # The standard basis is line 17 = {0, 4, 5, 6}.
    # Any automorphism maps this to another orthonormal basis.

    # How many lines are orthonormal (i.e., their 4 points span C^4)?
    print("\nChecking which lines span C^4:")
    spanning_lines = []
    for i, L in enumerate(lines):
        M = V[list(L)]
        rank = np.linalg.matrix_rank(M)
        if rank == 4:
            spanning_lines.append(i)

    print(f"  {len(spanning_lines)} lines span C^4 (out of {len(lines)})")
    print(f"  These are: {spanning_lines[:20]}...")

    # Each spanning line could be the image of the standard basis.
    # But we also need the transformation to map ALL 40 points to themselves.

    # Let's try: take line 17 -> line 17 (identity)
    # and line 17 -> another spanning line, see if it extends.

    print("\nTrying to build automorphism from line 17 -> line 20:")
    L17 = list(lines[17])  # {0, 4, 5, 6}
    L20 = list(lines[20])  # {0, 22, 23, 24}

    # Build unitary mapping L17 -> L20 (preserving order)
    V17 = V[L17]  # 4x4 matrix, rows are the rays
    V20 = V[L20]

    # U such that U @ V17[i] = V20[i] (or a phase multiple)
    # Since V17 is orthonormal (columns of V17.T are orthonormal),
    # U = V20 @ V17^dag

    U = V20 @ V17.conj().T

    print(f"\nCandidate U (mapping line 17 -> line 20):")
    print(f"  U is {'unitary' if np.allclose(U @ U.conj().T, np.eye(4)) else 'NOT unitary'}")

    # Apply U to all rays
    V_transformed = (U @ V.T).T

    # Check if this maps rays to rays
    matches = {}
    for p in range(40):
        v_new = V_transformed[p]
        for q in range(40):
            if np.allclose(v_new, V[q], rtol=1e-5) or np.allclose(v_new, -V[q], rtol=1e-5):
                matches[p] = q
                break

    print(f"\n  Matches found: {len(matches)} / 40")
    if len(matches) == 40:
        print("  This IS an automorphism!")
    else:
        unmatched = [p for p in range(40) if p not in matches]
        print(f"  Unmatched: {unmatched[:10]}")


def analyze_automorphism_orbit():
    """
    Look at the orbit of point 0 under likely automorphisms.

    If automorphisms act transitively, all 40 points are equivalent.
    If not, there are multiple orbits.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("AUTOMORPHISM ORBIT ANALYSIS")
    print("=" * 70)

    # Points on standard basis line: {0, 4, 5, 6}
    # These should be equivalent under coordinate permutations.

    # Let's check: are {0, 4, 5, 6} all equivalent?
    # They're all single-component vectors.

    print("\nStandard basis points:")
    for p in [0, 4, 5, 6]:
        nz = np.where(np.abs(V[p]) > 0.1)[0]
        print(f"  Point {p}: nonzero at component {nz[0]}")

    # What about the 36 other points?
    # They all have 3 nonzero components.

    print("\n3-component points (sample):")
    for p in [1, 2, 3, 7, 8, 9]:
        nz = np.where(np.abs(V[p]) > 0.1)[0]
        print(f"  Point {p}: nonzero at components {list(nz)}")

    # There are 4 patterns of 3-component support
    # (omit one coordinate). 36 / 4 = 9 points per pattern.


def count_automorphisms():
    """
    Estimate the size of the automorphism group.

    Known: |Aut(GQ(3,3))| = 51840 for the incidence structure.
    The phase structure might reduce this.
    """
    print("\n" + "=" * 70)
    print("AUTOMORPHISM GROUP SIZE")
    print("=" * 70)

    print("\nKnown facts about GQ(3,3) = W(3):")
    print("  - Aut(GQ(3,3)) = PSU(4,2) : Z_2")
    print("  - |PSU(4,2)| = 25920")
    print("  - |PSU(4,2) : Z_2| = 51840")

    print("\nOur ray realization adds phase structure.")
    print("Phase-preserving automorphisms form a subgroup.")
    print("Need to compute this subgroup explicitly.")


def study_k4_automorphisms():
    """
    How do automorphisms act on K4 components?

    If automorphisms are transitive on K4s, they're all equivalent.
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
    print("K4 COMPONENT CLASSIFICATION")
    print("=" * 70)

    # Find all K4 components
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

    print(f"Total K4 components: {len(k4_list)}")

    # For each K4, compute a "signature" based on phase structure
    print("\nClassifying K4 by phase signature:")

    k4_sigs = {}
    for outer, center in k4_list:
        # Phase signature: multiset of pairwise phases in outer
        phases = []
        for p, q in combinations(outer, 2):
            z = inner(V, p, q)
            k = round(6 * np.angle(z) / np.pi) % 12
            phases.append(k)
        sig = tuple(sorted(phases))
        k4_sigs[outer] = sig

    # Group by signature
    sig_groups = defaultdict(list)
    for outer, sig in k4_sigs.items():
        sig_groups[sig].append(outer)

    print(f"  Found {len(sig_groups)} distinct K4 phase signatures")
    for sig, outers in sorted(sig_groups.items(), key=lambda x: -len(x[1])):
        print(f"    Signature {sig}: {len(outers)} K4s")
        print(f"      Examples: {outers[:3]}")


def main():
    analyze_point_symmetries()
    check_coordinate_permutations()
    check_phase_rotation()
    find_unitary_automorphisms()
    analyze_automorphism_orbit()
    count_automorphisms()
    study_k4_automorphisms()

if __name__ == "__main__":
    main()
