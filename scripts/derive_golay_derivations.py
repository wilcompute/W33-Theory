#!/usr/bin/env python3
"""Symbolic derivation algebra for the Golay 24-dim Lie algebra.

This script redoes Test B from the conversation: not only compute the
dimensions (24 inner + 9 outer = 33) but also produce an explicit basis
and exhibit the canonical decomposition coming from the current-algebra
structure.

It prints a human-readable summary and saves the outer basis to a JSON
artifact for later inspection.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

try:
    # Prefer package-relative import when used as a module; fall back to
    # absolute import for direct script execution.
    from .w33_golay_lie_algebra import (
        build_golay_lie_algebra,
        _ad_matrices,
        _derivation_dims,
        _rank_mod_p,
    )
except Exception:  # pragma: no cover - fallback for direct script execution
    from scripts.w33_golay_lie_algebra import (
        build_golay_lie_algebra,
        _ad_matrices,
        _derivation_dims,
        _rank_mod_p,
    )

ROOT = Path(__file__).resolve().parents[1]


def compute_deriv_basis(alg) -> np.ndarray:
    """Return a matrix whose rows are a basis for Der(L) as 576-vectors.

    The linear system is the same as in ``_derivation_dims``; we simply
    compute the nullspace over F3 by Gaussian elimination.
    """
    # build equation matrix A as before
    rows = []
    for i in range(24):
        for j in range(24):
            entry = alg.bracket_c[i, j], alg.bracket_k[i, j]
    # reuse implementation from _derivation_dims by replicating the code block
    from scripts.w33_golay_lie_algebra import _bracket

    for i in range(24):
        for j in range(24):
            entry = _bracket(alg, i, j)
            if entry is None:
                continue
            k, c = entry
            for q in range(24):
                coeffs = np.zeros((24 * 24,), dtype=np.int64)
                coeffs[q * 24 + int(k)] = (coeffs[q * 24 + int(k)] + int(c)) % 3
                # sum_a D[a,i] * [a,j]
                for a in range(24):
                    aj = _bracket(alg, a, j)
                    if aj is not None and int(aj[0]) == q:
                        coeffs[a * 24 + int(i)] = (
                            coeffs[a * 24 + int(i)] - int(aj[1])
                        ) % 3
                # sum_a D[a,j] * [i,a]
                for a in range(24):
                    ia = _bracket(alg, i, a)
                    if ia is not None and int(ia[0]) == q:
                        coeffs[a * 24 + int(j)] = (
                            coeffs[a * 24 + int(j)] - int(ia[1])
                        ) % 3
                if np.any(coeffs):
                    rows.append(coeffs)
    A = np.stack(rows, axis=0) % 3  # shape (n_eq, 576)

    # perform Gaussian elimination to find nullspace basis
    M = A.copy()
    m, n = M.shape
    pivots = []
    r = 0
    for c in range(n):
        # pivot row
        piv = None
        for i in range(r, m):
            if M[i, c] != 0:
                piv = i
                break
        if piv is None:
            continue
        # swap
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), -1, 3)
        M[r, :] = (M[r, :] * inv) % 3
        for i in range(m):
            if i != r and M[i, c] != 0:
                factor = M[i, c]
                M[i, :] = (M[i, :] - factor * M[r, :]) % 3
        pivots.append(c)
        r += 1
        if r == m:
            break
    pivot_set = set(pivots)
    basis = []
    for col in range(n):
        if col in pivot_set:
            continue
        # set free variable col = 1, others 0, back-substitute
        vec = np.zeros((n,), dtype=np.int64)
        vec[col] = 1
        # each pivot row gives expression for pivot variable
        prow = 0
        for c in range(n):
            if prow < len(pivots) and pivots[prow] == c:
                # pivot at column c
                # the equation is x_c + sum_{j>c} M[prow,j]*x_j = 0
                val = 0
                for j in range(c + 1, n):
                    val = (val + M[prow, j] * vec[j]) % 3
                vec[c] = (-val) % 3
                prow += 1
        basis.append(vec)
    return np.stack(basis, axis=0)


def main():
    alg = build_golay_lie_algebra()
    ad = _ad_matrices(alg)
    dims = _derivation_dims(alg, ad)
    print("derivation dims:", dims)
    basis = compute_deriv_basis(alg)
    print("nullity basis shape", basis.shape)
    # separate inner vs outer
    inner = np.vstack([M.reshape(-1) for M in ad]) % 3
    rank_inner = _rank_mod_p(inner, 3)
    print("rank inner subspace", rank_inner)
    # find outer vectors (not in span of inner)
    # simple by checking linear independence when appended
    outer = []
    current = inner.copy()
    for v in basis:
        test = np.vstack((current, v))
        if _rank_mod_p(test, 3) > _rank_mod_p(current, 3):
            outer.append(v)
            current = test
    print("outer count", len(outer))
    # save outer basis
    outpath = ROOT / "committed_artifacts" / "golay_outer_deriv_basis.json"
    json.dump([v.tolist() for v in outer], open(outpath, "w"))
    print("saved outer basis to", outpath)

    # --- quick human classification of the outer derivations
    mats = [v.reshape((24, 24)) % 3 for v in outer]
    print("\nouter derivations summary:")
    for idx, M in enumerate(mats):
        nonzeros = np.argwhere(M != 0)
        grades = [divmod(r, 3)[0] for r, c in nonzeros]  # rough grouping
        print(f"  derivation {idx}: {len(nonzeros)} nonzeros; grades(approx)=", sorted(set(grades)))
        # count per grade-block
        block_counts = {}
        for r, c in nonzeros:
            g_r = r // 3
            g_c = c // 3
            block_counts.setdefault((g_r, g_c), 0)
            block_counts[(g_r, g_c)] += 1
        print("    block counts sample:", list(block_counts.items())[:5])
    print("\nFinished analysis of outer basis.")


if __name__ == "__main__":
    main()
