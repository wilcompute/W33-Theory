#!/usr/bin/env python3
"""
Fit diagonal left/right scalings so that diag(L) * M * diag(R) ≈ experimental
CKM magnitudes using alternating least squares.

Writes `data/ckm_fitted_scalings.json` with the fitted scalings and diagnostics.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np


def als_fit(M: np.ndarray, E: np.ndarray, max_iters: int = 1000, tol: float = 1e-12):
    n = M.shape[0]
    r = np.ones(n, dtype=float)
    l = np.ones(n, dtype=float)
    prev_err = None
    for it in range(max_iters):
        # update left scales l
        for i in range(n):
            numer = np.sum(M[i, :] * r * E[i, :])
            denom = np.sum((M[i, :] * r) ** 2)
            l[i] = numer / denom if denom > 0 else 0.0
        l = np.maximum(l, 1e-16)

        # update right scales r
        for j in range(n):
            numer = np.sum(M[:, j] * l * E[:, j])
            denom = np.sum((M[:, j] * l) ** 2)
            r[j] = numer / denom if denom > 0 else 0.0
        r = np.maximum(r, 1e-16)

        A = np.diag(l) @ M @ np.diag(r)
        err = float(np.linalg.norm(A - E))
        if prev_err is not None and abs(prev_err - err) < tol:
            return l, r, A, err, it + 1
        prev_err = err

    A = np.diag(l) @ M @ np.diag(r)
    err = float(np.linalg.norm(A - E))
    return l, r, A, err, max_iters


def main():
    p = Path("data/ckm_from_grams.json")
    if not p.exists():
        print("ERROR: data/ckm_from_grams.json not found; run scripts/ckm_from_grams.py first")
        return 1

    d = json.loads(p.read_text(encoding="utf-8"))
    M = np.array(d["overlap_matrix"], dtype=float)
    exp = np.array(d.get("experimental", []), dtype=float)
    if exp.size != M.size:
        # fallback PDG-like magnitudes (approx)
        exp = np.array(
            [[0.97373, 0.2243, 0.00382], [0.221, 0.987, 0.041], [0.008, 0.0388, 1.013]],
            dtype=float,
        )

    initial_err = float(np.linalg.norm(M - exp))

    L, R, A, final_err, iters = als_fit(M, exp, max_iters=2000, tol=1e-12)

    out = {
        "left_scales": L.tolist(),
        "right_scales": R.tolist(),
        "scaled_matrix": A.tolist(),
        "initial_error": initial_err,
        "final_error": final_err,
        "iterations": int(iters),
    }

    Path("data/ckm_fitted_scalings.json").write_text(json.dumps(out, indent=2))
    print("Wrote data/ckm_fitted_scalings.json")
    print(f"initial_err={initial_err:.6f}, final_err={final_err:.6f}, iters={iters}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
