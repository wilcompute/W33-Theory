#!/usr/bin/env python3
"""Find parity proofs in the Witting (40-ray) configuration.

Parity proof criteria (KS-style):
- Choose an odd number of bases (tetrads)
- Each ray appears in an even number of chosen bases

We compute all 4-cliques (tetrads) from the 40 Witting rays, then solve
A x = 0 (mod 2) with sum(x) = 1 (mod 2).
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    """Construct the 40 Witting rays (projective classes) in C^4.

    Based on standard construction used in prior tools.
    """
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)

    rays = []

    # 4 basis states
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)

    # 36 states in 4 groups of 9
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)

    return rays


def orthogonal(v1, v2, tol=1e-8):
    return abs(np.vdot(v1, v2)) < tol


def find_tetrads(rays):
    """Find all orthonormal bases (tetrads) among the 40 rays."""
    n = len(rays)
    tetrads = []

    # Precompute orthogonality matrix
    ortho = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if orthogonal(rays[i], rays[j]):
                ortho[i, j] = ortho[j, i] = True

    # Find 4-cliques
    for a, b, c, d in combinations(range(n), 4):
        if (
            ortho[a, b]
            and ortho[a, c]
            and ortho[a, d]
            and ortho[b, c]
            and ortho[b, d]
            and ortho[c, d]
        ):
            tetrads.append((a, b, c, d))

    return tetrads


def gf2_rref(M, b=None):
    """Row-reduce M (mod 2). If b provided, reduce augmented system."""
    M = M.copy() % 2
    if b is not None:
        b = b.copy() % 2

    rows, cols = M.shape
    pivot_cols = []
    r = 0

    for c in range(cols):
        if r >= rows:
            break
        # Find pivot
        pivot = None
        for rr in range(r, rows):
            if M[rr, c] == 1:
                pivot = rr
                break
        if pivot is None:
            continue
        # Swap
        if pivot != r:
            M[[r, pivot]] = M[[pivot, r]]
            if b is not None:
                b[[r, pivot]] = b[[pivot, r]]
        # Eliminate
        for rr in range(rows):
            if rr != r and M[rr, c] == 1:
                M[rr, :] ^= M[r, :]
                if b is not None:
                    b[rr] ^= b[r]
        pivot_cols.append(c)
        r += 1

    return M, b, pivot_cols


def gf2_solve(M, b):
    """Solve M x = b over GF(2). Returns one solution and nullspace basis."""
    rows, cols = M.shape
    M_rref, b_rref, pivots = gf2_rref(M, b)
    pivots = list(pivots)
    free_cols = [c for c in range(cols) if c not in pivots]

    # Check consistency
    for r in range(rows):
        if not M_rref[r].any() and b_rref[r] == 1:
            return None, []

    # Particular solution: set free vars = 0
    x0 = np.zeros(cols, dtype=np.uint8)
    for r, c in enumerate(pivots):
        x0[c] = b_rref[r]

    # Nullspace basis vectors
    basis = []
    for fc in free_cols:
        v = np.zeros(cols, dtype=np.uint8)
        v[fc] = 1
        for r, pc in enumerate(pivots):
            if M_rref[r, fc] == 1:
                v[pc] ^= 1
        basis.append(v)

    return x0, basis


def find_min_weight_solution(x0, basis, max_enum=1 << 24):
    """Find a low-weight solution in affine space x0 + span(basis)."""
    d = len(basis)
    if d == 0:
        return x0, int(x0.sum())

    # If dimension small enough, brute force all combos
    if d <= 20:
        best = None
        best_w = 10**9
        for mask in range(1 << d):
            x = x0.copy()
            for i in range(d):
                if (mask >> i) & 1:
                    x ^= basis[i]
            w = int(x.sum())
            if w < best_w:
                best_w = w
                best = x.copy()
        return best, best_w

    # Otherwise, use meet-in-the-middle on first 12 dims
    split = min(12, d)
    left = basis[:split]
    right = basis[split:]

    left_map = {}
    for mask in range(1 << len(left)):
        x = np.zeros_like(x0)
        for i in range(len(left)):
            if (mask >> i) & 1:
                x ^= left[i]
        w = int(x.sum())
        if x.tobytes() not in left_map or w < left_map[x.tobytes()][0]:
            left_map[x.tobytes()] = (w, mask, x)

    best = None
    best_w = 10**9
    for mask in range(1 << len(right)):
        x = x0.copy()
        for i in range(len(right)):
            if (mask >> i) & 1:
                x ^= right[i]
        # Try combining with any left vector (just take minimal weight for each left)
        # Here we just combine with zero-left for a baseline; further optimization can be done if needed
        w = int(x.sum())
        if w < best_w:
            best_w = w
            best = x.copy()

    return best, best_w


def main():
    print("Witting parity proof search")
    print("=" * 40)

    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)

    print(f"Rays: {len(rays)}")
    print(f"Tetrads (bases): {len(tetrads)}")

    # Build incidence matrix A (40 x B)
    B = len(tetrads)
    A = np.zeros((40, B), dtype=np.uint8)
    for j, base in enumerate(tetrads):
        for r in base:
            A[r, j] = 1

    # Add sum constraint: sum(x)=1
    A_ext = np.vstack([A, np.ones((1, B), dtype=np.uint8)])
    b = np.zeros(41, dtype=np.uint8)
    b[-1] = 1

    x0, basis = gf2_solve(A_ext, b)
    if x0 is None:
        print("No parity proof found (unexpected).")
        return

    print(f"Nullspace dimension (with parity): {len(basis)}")

    sol, weight = find_min_weight_solution(x0, basis)
    if sol is None:
        print("Failed to find a solution.")
        return

    chosen = [j for j in range(B) if sol[j] == 1]
    print(f"Found parity proof with {len(chosen)} bases")

    # Verify even counts
    counts = (A @ sol) % 2
    ok_even = counts.sum() == 0
    ok_odd = (sol.sum() % 2) == 1

    print(f"Even count per ray: {ok_even}")
    print(f"Odd number of bases: {ok_odd}")

    # Save results
    result = {
        "rays": len(rays),
        "bases": len(tetrads),
        "parity_bases_count": int(len(chosen)),
        "chosen_bases": chosen,
        "bases": [list(map(int, b)) for b in tetrads],
        "even_per_ray": bool(ok_even),
        "odd_bases": bool(ok_odd),
        "nullspace_dim": len(basis),
    }

    out_path = ROOT / "artifacts" / "witting_parity_proof.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
