#!/usr/bin/env python3
"""
K4 PROOF V3: THE ALGEBRAIC PROOF

Key discovery from v2: Both outer P and center C have RANK 3.
Together they span C^4.

This means:
- P lies in a 3D subspace of C^4
- C lies in a DIFFERENT 3D subspace
- The intersection is a 2D subspace
- Together: 3 + 3 - 2 = 4 (full span)

Let me prove WHY this rank-3 structure forces the Bargmann phase = -1.
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


def find_null_vectors():
    """
    If P has rank 3, there's a vector n such that n.P = 0 (annihilates all of P).
    Similarly for C.

    These null vectors are KEY to understanding the structure.
    """
    V = load_rays()

    print("=" * 70)
    print("NULL VECTOR ANALYSIS")
    print("=" * 70)

    # K4 component: outer = {0,1,2,3}, center = {4,13,22,31}
    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    P = V[outer]  # 4x4, rank 3
    C = V[center]  # 4x4, rank 3

    # Find the null space of P^T (left null space of P)
    # n.P = 0 means n is in the left null space
    U_P, S_P, Vh_P = np.linalg.svd(P.T)
    null_P = Vh_P[-1]  # Last row of Vh is the null vector

    U_C, S_C, Vh_C = np.linalg.svd(C.T)
    null_C = Vh_C[-1]

    print(f"\nSingular values of P^T: {S_P}")
    print(f"Singular values of C^T: {S_C}")

    print(f"\nNull vector of P (annihilates outer quad):")
    print(f"  n_P = {null_P}")
    print(f"  |n_P| = {np.linalg.norm(null_P):.6f}")

    print(f"\nNull vector of C (annihilates center quad):")
    print(f"  n_C = {null_C}")
    print(f"  |n_C| = {np.linalg.norm(null_C):.6f}")

    # Verify: n_P . p_i = 0 for all outer points
    print("\nVerification n_P . outer = 0:")
    for i, p in enumerate(outer):
        dot = np.vdot(null_P, V[p])
        print(f"  n_P . V[{p}] = {dot:.6e}")

    print("\nVerification n_C . center = 0:")
    for i, c in enumerate(center):
        dot = np.vdot(null_C, V[c])
        print(f"  n_C . V[{c}] = {dot:.6e}")

    # KEY QUESTION: What's the relationship between n_P and n_C?
    print("\n" + "-" * 50)
    print("RELATIONSHIP BETWEEN NULL VECTORS")
    print("-" * 50)

    overlap = np.vdot(null_P, null_C)
    print(f"\n<n_P | n_C> = {overlap:.6f}")
    print(f"|<n_P | n_C>| = {abs(overlap):.6f}")

    # Are they orthogonal?
    if abs(abs(overlap) - 0) < 0.01:
        print("n_P and n_C are ORTHOGONAL!")
    elif abs(abs(overlap) - 1) < 0.01:
        print("n_P and n_C are PARALLEL (or anti-parallel)!")

    return null_P, null_C


def analyze_subspace_structure():
    """
    The outer quad P spans a 3D subspace.
    The center quad C spans a different 3D subspace.

    What's the geometry of their intersection?
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("SUBSPACE INTERSECTION")
    print("=" * 70)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    P = V[outer]  # 4x4
    C = V[center]  # 4x4

    # Find orthonormal bases for the column spaces
    # (The column space of P^T = row space of P = span of outer rays)
    U_P, S_P, _ = np.linalg.svd(P)
    basis_P = U_P[:, :3]  # First 3 columns span outer

    U_C, S_C, _ = np.linalg.svd(C)
    basis_C = U_C[:, :3]  # First 3 columns span center

    print(f"\nOuter span: 3D subspace with orthonormal basis (3 columns of U_P)")
    print(f"Center span: 3D subspace with orthonormal basis (3 columns of U_C)")

    # The intersection of two 3D subspaces in C^4 is at least 2D
    # dim(P inter C) = dim(P) + dim(C) - dim(P + C) = 3 + 3 - 4 = 2

    # Find the intersection explicitly
    # A vector v is in both spans if:
    # v = P @ a = C @ b for some a, b
    # => C^dag @ P @ a = C^dag @ C @ b

    # Alternative: Find vectors in span(P) that are orthogonal to null_C
    # (since null_C kills all of C, if v in span(C), then null_C . v = 0)

    _, _, Vh_C = np.linalg.svd(C.T)
    null_C = Vh_C[-1]  # Annihilates center

    # Project null_C onto span(P) to find what it looks like there
    # Actually, let's find the intersection more directly

    # Gram matrix for overlap
    # basis_P is 4x3, basis_C is 4x3
    # G = basis_P^dag @ basis_C is 3x3, its singular values tell overlap
    G = basis_P.conj().T @ basis_C
    print(f"\nGram matrix of subspace overlap: {G.shape}")

    U_G, S_G, Vh_G = np.linalg.svd(G)
    print(f"Singular values of Gram: {S_G}")

    # Singular values of 1 mean that direction is shared
    # Number of singular values = 1 gives intersection dimension
    n_shared = np.sum(S_G > 0.999)
    print(f"\nNumber of singular values ~= 1: {n_shared}")
    print(f"=> Intersection dimension: {n_shared}")

    # Find explicit basis for intersection
    # The shared directions are where S_G = 1
    for i, s in enumerate(S_G):
        if s > 0.9:
            # In P-basis, this is U_G[:, i]
            # In C-basis, this is Vh_G[i, :]
            v_in_P = basis_P @ U_G[:, i]
            v_in_C = basis_C @ Vh_G[i, :]
            print(f"\nShared direction {i} (S={s:.4f}):")
            print(f"  Via P: {v_in_P}")
            print(f"  Via C: {v_in_C}")
            print(f"  Diff:  {np.linalg.norm(v_in_P - v_in_C):.6e}")


def compute_determinant_formula():
    """
    The Bargmann invariant for 4 points can be written as a determinant.

    For points a, b, c, d with rays v_a, v_b, v_c, v_d:
    B = <a|b><b|c><c|d><d|a>

    This equals det(Gram(v_a, v_b, v_c, v_d)) under certain conditions...

    Actually, let me think about this differently.
    """
    V = load_rays()

    print("\n" + "=" * 70)
    print("DETERMINANT FORMULA")
    print("=" * 70)

    outer = [0, 1, 2, 3]

    P = V[outer]  # 4x4 matrix, rows are rays

    # Gram matrix G_ij = <v_i | v_j>
    G = P @ P.conj().T

    print("\nGram matrix of outer quad:")
    for i in range(4):
        row = " ".join(f"{G[i,j]:8.4f}" for j in range(4))
        print(f"  {row}")

    det_G = np.linalg.det(G)
    print(f"\ndet(G) = {det_G:.6f}")

    # The Bargmann invariant is a PRODUCT of off-diagonal elements
    # B = G[0,1] * G[1,2] * G[2,3] * G[3,0]
    B_01_12_23_30 = G[0, 1] * G[1, 2] * G[2, 3] * G[3, 0]
    print(f"\nB(0->1->2->3->0) = G[0,1]*G[1,2]*G[2,3]*G[3,0] = {B_01_12_23_30:.6f}")

    # What about the other cycle?
    B_01_13_32_20 = G[0, 1] * G[1, 3] * G[3, 2] * G[2, 0]
    print(f"B(0->1->3->2->0) = {B_01_13_32_20:.6f}")

    # There's a beautiful identity:
    # For a 4x4 Gram matrix with |G_ii| = 1, det(G) = 0 implies...

    print("\n" + "-" * 50)
    print("CHECKING GRAM MATRIX IDENTITIES")
    print("-" * 50)

    # The diagonal is all 1 (unit vectors)
    print("\nDiagonal of G:", [G[i, i] for i in range(4)])

    # Off-diagonal magnitudes
    print("\nOff-diagonal magnitudes:")
    for i in range(4):
        for j in range(i + 1, 4):
            print(f"  |G[{i},{j}]| = {abs(G[i,j]):.6f}")

    # Phases (in Z_12)
    print("\nOff-diagonal phases (k in Z_12):")
    for i in range(4):
        for j in range(i + 1, 4):
            k = round(6 * np.angle(G[i, j]) / np.pi) % 12
            print(f"  k[{i},{j}] = {k}")


def prove_minus_one():
    """
    THE PROOF:

    For a K4 component with outer P and center C:
    1. P has rank 3 (spans 3D subspace)
    2. C has rank 3 (spans 3D subspace)
    3. P and C are BIPARTITE ORTHOGONAL: every p in P is orthog to some c in C

    The key constraint: each p in P is orthogonal to exactly 1 point in C.
    This creates a MATCHING between P and C!

    Let's see if this matching determines the phase structure.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("THE PROOF: WHY K4 => -1")
    print("=" * 70)

    # Build collinearity
    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    print(f"\nOuter: {outer}")
    print(f"Center: {center}")

    # Find the matching: which outer is orthogonal to which center?
    print("\nOrthogonality matching (collinearity in W33):")
    matching = {}
    for p in outer:
        for c in center:
            z = inner(V, p, c)
            if abs(z) < 0.01:  # Orthogonal
                matching[p] = c
                print(f"  Outer {p} <-> Center {c} (orthogonal, collinear in W33)")

    # Each outer point is collinear with exactly ONE center point
    print(f"\nMatching: {matching}")

    # Now the key: the 3 non-matched center points form a FRAME for outer[p]
    # Outer p is a linear combo of the 3 centers it's NOT orthogonal to

    print("\n" + "-" * 50)
    print("EXPRESSING OUTER IN CENTER BASIS")
    print("-" * 50)

    for p in outer:
        matched_c = matching[p]
        other_c = [c for c in center if c != matched_c]

        # V[p] should be in span of other_c
        # Expand: V[p] = sum_{c in other_c} alpha_c * V[c]
        # The coefficient is alpha_c = <V[c] | V[p]> / <V[c] | V[c]> = <c|p>

        coeffs = {}
        for c in other_c:
            coeffs[c] = inner(V, c, p)

        # Verify
        v_reconstructed = sum(coeffs[c] * V[c] for c in other_c)
        error = np.linalg.norm(V[p] - v_reconstructed)

        print(f"\nOuter {p} (matched to {matched_c}):")
        print(f"  Coefficients: {[(c, f'{coeffs[c]:.4f}') for c in other_c]}")
        print(f"  Reconstruction error: {error:.6e}")

        # The coefficients are <c|p> which have phases k(c,p)
        for c in other_c:
            k = round(6 * np.angle(coeffs[c]) / np.pi) % 12
            print(f"    k({c},{p}) = {k}")


def analyze_phase_constraints():
    """
    The phases k(p,q) for non-collinear pairs satisfy constraints.

    For K4: outer P, center C
    - k(p,c) for p in P, c not matched to p
    - k(p,p') for p,p' in P

    The Bargmann phase is sum of 4 k's around a cycle.
    Let's see how the constraints force sum = 6.
    """
    V = load_rays()
    lines = load_lines()

    print("\n" + "=" * 70)
    print("PHASE CONSTRAINT ANALYSIS")
    print("=" * 70)

    col = defaultdict(set)
    for L in lines:
        for p in L:
            col[p].update(L)
            col[p].discard(p)

    outer = [0, 1, 2, 3]
    center = [4, 13, 22, 31]

    # Full phase table
    print("\nPhase table k(p,q) for outer quad:")
    print("     ", end="")
    for q in outer:
        print(f"  {q}  ", end="")
    print()

    phases = {}
    for p in outer:
        print(f"  {p} ", end="")
        for q in outer:
            if p == q:
                print("  -  ", end="")
            else:
                z = inner(V, p, q)
                k = round(6 * np.angle(z) / np.pi) % 12
                phases[(p, q)] = k
                print(f"  {k:2d} ", end="")
        print()

    # The ANTISYMMETRY: k(p,q) + k(q,p) = 0 (mod 12)
    print("\nAntisymmetry check k(p,q) + k(q,p) mod 12:")
    for p in outer:
        for q in outer:
            if p < q:
                s = (phases[(p, q)] + phases[(q, p)]) % 12
                print(
                    f"  k({p},{q}) + k({q},{p}) = {phases[(p,q)]} + {phases[(q,p)]} = {s} mod 12"
                )

    # For a cycle a->b->c->d->a:
    # Bargmann = k(a,b) + k(b,c) + k(c,d) + k(d,a)

    print("\n" + "-" * 50)
    print("ALL HAMILTONIAN CYCLES")
    print("-" * 50)

    # All 3 distinct Hamiltonian cycles (up to orientation)
    cycles = [
        [0, 1, 2, 3],  # 0-1-2-3-0
        [0, 1, 3, 2],  # 0-1-3-2-0
        [0, 2, 1, 3],  # 0-2-1-3-0
    ]

    for cyc in cycles:
        a, b, c, d = cyc
        s = (phases[(a, b)] + phases[(b, c)] + phases[(c, d)] + phases[(d, a)]) % 12
        print(
            f"Cycle {a}->{b}->{c}->{d}->{a}: {phases[(a,b)]}+{phases[(b,c)]}+{phases[(c,d)]}+{phases[(d,a)]} = {s}"
        )

    # KEY: All cycles give 6!
    # WHY?

    print("\n" + "-" * 50)
    print("WHY ALL CYCLES GIVE 6")
    print("-" * 50)

    # Decompose: k(a,b) = (k(a,b) + k(b,a))/2 + (k(a,b) - k(b,a))/2
    # But k(a,b) + k(b,a) = 0, so k(b,a) = -k(a,b) = 12 - k(a,b)

    # For cycle a->b->c->d->a:
    # S = k(a,b) + k(b,c) + k(c,d) + k(d,a)

    # Key insight: the 6 edges split into 3 pairs: (ab,cd), (ac,bd), (ad,bc)
    # These are the 3 perfect matchings of K4!

    print("\nPerfect matching structure:")
    matchings = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]

    for e1, e2 in matchings:
        k1 = phases[e1]
        k2 = phases[e2]
        s = (k1 + k2) % 12
        print(f"  Matching {e1},{e2}: k{e1}={k1}, k{e2}={k2}, sum={s}")

    # A Hamiltonian cycle uses 2 matchings!
    # Cycle 0-1-2-3-0 uses edges (0,1), (1,2), (2,3), (3,0)
    #   = matching (0,1)(2,3) and matching (0,3)(1,2)
    # Wait, that's not quite right...

    # Actually, edges are: 01, 12, 23, 30
    # Pairs by opposite: (01,23) and (12,30)
    # Not matching-based...

    print("\nEdge pairs in cycle 0-1-2-3-0:")
    print(f"  Opposite edges: (01,23) and (12,30)")
    print(
        f"  k(0,1) + k(2,3) = {phases[(0,1)]} + {phases[(2,3)]} = {(phases[(0,1)] + phases[(2,3)]) % 12}"
    )
    print(
        f"  k(1,2) + k(3,0) = {phases[(1,2)]} + {phases[(3,0)]} = {(phases[(1,2)] + phases[(3,0)]) % 12}"
    )


def verify_on_all_k4s():
    """
    Verify the -1 = phase 6 on ALL 90 K4 components.
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
    print("VERIFICATION ON ALL 90 K4s")
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
                        k4_list.append(((a, b, c, d), tuple(sorted(common))))

    print(f"Found {len(k4_list)} K4 components")

    # For each K4, verify Bargmann = 6 for ALL 24 orderings
    all_correct = True
    for outer, center in k4_list:
        a, b, c, d = outer
        for perm in permutations(outer):
            p0, p1, p2, p3 = perm
            z = (
                inner(V, p0, p1)
                * inner(V, p1, p2)
                * inner(V, p2, p3)
                * inner(V, p3, p0)
            )
            k = round(6 * np.angle(z) / np.pi) % 12
            if k != 6:
                print(f"FAIL: K4 {outer}, perm {perm}, k={k}")
                all_correct = False

    if all_correct:
        print(
            "SUCCESS: ALL K4 components, ALL orderings give Bargmann phase = 6 (= -1)"
        )

    return all_correct


def main():
    null_P, null_C = find_null_vectors()
    analyze_subspace_structure()
    compute_determinant_formula()
    prove_minus_one()
    analyze_phase_constraints()
    verify_on_all_k4s()


if __name__ == "__main__":
    main()
