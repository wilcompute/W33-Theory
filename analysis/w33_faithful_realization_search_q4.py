#!/usr/bin/env python3
"""Execute Task 2: q=4 faithful ray realization probe.

Probes whether W(4) (85 points, 340 edges, 85 lines of size 5) admits a
faithful ray realization in C^5 where each line is an orthonormal basis.
Uses numerical optimization (BFGS) to minimize the orthogonality and
normalization errors.
"""

import itertools
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

# Add analysis to path for w33_master_audit
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_master_audit as audit


def solve_realization(q=4):
    pts, A, lines, B = audit._build(q)
    n = len(pts)
    n_lines = len(lines)
    dim = q + 1

    # We want n vectors in C^dim.
    # Represent as (n, dim, 2) real array for (real, imag)
    # Total variables: n * dim * 2

    # Pre-compute pairs that must be orthogonal
    ortho_pairs = []
    for line in lines:
        for i, j in itertools.combinations(line, 2):
            if i < j:
                ortho_pairs.append((i, j))
    ortho_pairs = sorted(list(set(ortho_pairs)))

    def objective(x):
        vecs = x.reshape((n, dim, 2))
        c_vecs = vecs[:, :, 0] + 1j * vecs[:, :, 1]

        # Normalization error
        norms = np.sum(np.abs(c_vecs) ** 2, axis=1)
        norm_err = np.sum((norms - 1.0) ** 2)

        # Orthogonality error
        # Dot product: v_i_conj . v_j
        err = 0.0
        for i, j in ortho_pairs:
            dot = np.vdot(c_vecs[i], c_vecs[j])
            err += np.abs(dot) ** 2

        return norm_err + err

    # Start with random vectors
    np.random.seed(42)
    x0 = np.random.normal(0, 1, (n, dim, 2))
    # Normalize initial
    for i in range(n):
        mag = np.linalg.norm(x0[i])
        if mag > 0:
            x0[i] /= mag

    x0 = x0.flatten()

    print(f"Starting optimization for W({q}) in C^{dim}...")
    print(f"Points: {n}, Lines: {n_lines}, Dimension: {dim}")
    print(f"Variables: {len(x0)}, Ortho pairs: {len(ortho_pairs)}")

    res = minimize(objective, x0, method="L-BFGS-B", options={"maxiter": 2000})

    final_err = res.fun
    print(f"Final error: {final_err:.6e}")

    if final_err < 1e-6:
        print(f"SUCCESS: Found a numerical realization for q={q}!")
        return True
    else:
        print(f"FAILURE: Optimization did not converge for q={q}.")
        return False


if __name__ == "__main__":
    print("--- Testing q=2 (provably impossible) ---")
    solve_realization(q=2)
    print("\n--- Testing q=3 (known to exist) ---")
    solve_realization(q=3)
    print("\n--- Testing q=4 (open question) ---")
    solve_realization(q=4)
