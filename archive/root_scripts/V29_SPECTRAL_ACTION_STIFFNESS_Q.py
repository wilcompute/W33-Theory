#!/usr/bin/env python3
"""
V29 — Dirac–Kähler spectral-action stiffness on curvature subspace im(d1).

Computes the Hessian (stiffness) matrix Q on a gauge-fixed basis of C^1 potentials
whose curvatures span im(d1) ⊂ C^2 for the W(3,3) 2-skeleton:

  - Build W(3,3) graph (40 vertices, 240 edges), and all triangles (160).
  - Build coboundaries d0: C^0→C^1 and d1: C^1→C^2 (untwisted).
  - Build Dirac–Kähler D on C^0⊕C^1⊕C^2 (N=440).
  - Use the spectral action S(A)=log det(I + D_A^2/Λ^2) with Λ=4 by default,
    where the U(1) connection enters via head-edge holonomies in the d0 block.
  - Choose an orthonormal basis {f_i} of im(d1) using eigenvectors of L2=d1 d1^T,
    and minimum-norm potentials w_i solving d1 w_i = f_i:
        w_i = (1/λ) d1^T f_i  (λ=4 on W(3,3))
  - Form the full Hessian Q_ij = ∂^2 S / ∂t_i ∂t_j |_{0} for A = Σ t_i w_i.

Outputs:
  - Q.npy and Q.csv in the output directory
  - summary JSON (diag mean/std, offdiag rms/max, eigenvalue stats)
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Compute Dirac–Kähler spectral-action stiffness Q on im(d1).")
    ap.add_argument("--Lambda", type=float, default=4.0, help="Spectral-action cutoff Λ (default: 4.0)")
    ap.add_argument("--out-dir", type=Path, default=Path("V29_output_q_stiffness"), help="Output directory")
    ap.add_argument(
        "--validate",
        type=int,
        default=0,
        help="Run finite-difference validation on N random (i,j) pairs (0 disables).",
    )
    ap.add_argument("--fd-eps", type=float, default=1e-4, help="Finite-difference step ε (default: 1e-4)")
    ap.add_argument("--seed", type=int, default=0, help="RNG seed (default: 0)")
    return ap.parse_args()


def _canon(v: Tuple[int, int, int, int], mod: int) -> Tuple[int, int, int, int]:
    for a in v:
        if a % mod != 0:
            inv = 1 if a % mod == 1 else 2
            return tuple((inv * x) % mod for x in v)
    raise ValueError("zero vector")


def _omega(x: Tuple[int, int, int, int], y: Tuple[int, int, int, int], mod: int) -> int:
    x1, x2, x3, x4 = x
    y1, y2, y3, y4 = y
    return (x1 * y3 - x3 * y1 + x2 * y4 - x4 * y2) % mod


def build_w33_core(mod: int = 3) -> Tuple[int, np.ndarray, List[Tuple[int, int]], List[Tuple[int, int, int]]]:
    pts = sorted({_canon(v, mod) for v in itertools.product(range(mod), repeat=4) if any(v)})
    nV = len(pts)
    A = np.zeros((nV, nV), dtype=np.int8)
    for i, x in enumerate(pts):
        for j in range(i + 1, nV):
            if _omega(x, pts[j], mod) == 0:
                A[i, j] = A[j, i] = 1

    edges = [(i, j) for i in range(nV) for j in range(i + 1, nV) if A[i, j]]
    edge_index = {e: k for k, e in enumerate(edges)}

    nbrs = [set(np.nonzero(A[i])[0]) for i in range(nV)]
    tri: List[Tuple[int, int, int]] = []
    for i in range(nV):
        for j in range(i + 1, nV):
            if A[i, j]:
                for k in nbrs[i].intersection(nbrs[j]):
                    if k > j:
                        tri.append((i, j, int(k)))
    return nV, A, edges, tri


def build_d0_d1(
    nV: int, edges: List[Tuple[int, int]], triangles: List[Tuple[int, int, int]]
) -> Tuple[np.ndarray, sp.csr_matrix, sp.csr_matrix, np.ndarray, np.ndarray]:
    nE = len(edges)
    nF = len(triangles)

    tails = np.array([u for (u, v) in edges], dtype=int)
    heads = np.array([v for (u, v) in edges], dtype=int)

    row = np.repeat(np.arange(nE), 2)
    col = np.empty(2 * nE, dtype=int)
    dat = np.empty(2 * nE, dtype=float)
    col[0::2] = tails
    dat[0::2] = -1.0
    col[1::2] = heads
    dat[1::2] = +1.0
    d0 = sp.csr_matrix((dat, (row, col)), shape=(nE, nV))

    edge_index = {e: k for k, e in enumerate(edges)}
    row2: List[int] = []
    col2: List[int] = []
    dat2: List[float] = []
    for tidx, (i, j, k) in enumerate(triangles):
        row2 += [tidx, tidx, tidx]
        col2 += [edge_index[(j, k)], edge_index[(i, k)], edge_index[(i, j)]]
        dat2 += [1.0, -1.0, 1.0]
    d1 = sp.csr_matrix((dat2, (row2, col2)), shape=(nF, nE))

    D = sp.bmat(
        [
            [sp.csr_matrix((nV, nV)), d0.T, sp.csr_matrix((nV, nF))],
            [d0, sp.csr_matrix((nE, nE)), d1.T],
            [sp.csr_matrix((nF, nV)), d1, sp.csr_matrix((nF, nF))],
        ],
        format="csr",
    ).toarray()
    return D, d0, d1, tails, heads


def spectral_action_logdet(D: np.ndarray, Lambda: float) -> float:
    N = D.shape[0]
    K = np.eye(N, dtype=D.dtype) + (D @ D) / (Lambda**2)
    c, lower = la.cho_factor(K, check_finite=False)
    diag = np.diag(c) if not lower else np.diag(c)
    # cho_factor returns triangular factor in-place; diag is positive real
    return float(2.0 * np.sum(np.log(diag.real)))


def main() -> None:
    args = _parse_args()
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    nV, A, edges, tri = build_w33_core(mod=3)
    nE = len(edges)
    nF = len(tri)
    if (nV, nE, nF) != (40, 240, 160):
        raise RuntimeError(f"Unexpected sizes: (V,E,F)=({nV},{nE},{nF}) expected (40,240,160)")

    D, d0, d1, tails, heads = build_d0_d1(nV, edges, tri)
    N = D.shape[0]
    offE = nV

    Lambda = float(args.Lambda)
    K0 = np.eye(N) + (D @ D) / (Lambda**2)
    c_fac, lower = la.cho_factor(K0, check_finite=False)
    K0_inv = la.cho_solve((c_fac, lower), np.eye(N), check_finite=False)

    # Orthonormal basis of im(d1) via L2 eigenvectors
    L2 = (d1 @ d1.T).toarray()
    evals, evecs = np.linalg.eigh(L2)
    pos = np.where(evals > 1e-9)[0]
    if pos.size != 120:
        raise RuntimeError(f"Expected rank(L2)=120; got {pos.size}")
    lam = float(evals[pos[0]])
    if not np.allclose(evals[pos], lam, atol=1e-8, rtol=0.0):
        raise RuntimeError("Expected flat positive spectrum for L2")
    F_basis = evecs[:, pos]  # (160×120)
    W = (d1.T @ F_basis) / lam  # (240×120) with d1 W = F_basis
    n = W.shape[1]

    # term1: Tr(K0^{-1} K2) part
    S_mat = D @ K0_inv + K0_inv @ D
    s_e = S_mat[offE + np.arange(nE), heads]
    diag_v_head = np.diag(K0_inv)[heads]
    t_e = diag_v_head - s_e

    diag_term = W.T @ (t_e[:, None] * W)
    block_term = np.zeros((n, n))
    for v in range(nV):
        ev = np.where(heads == v)[0]
        if ev.size == 0:
            continue
        K_v = K0_inv[offE + ev[:, None], offE + ev]
        Wv = W[ev, :]
        block_term += Wv.T @ (K_v @ Wv)
    term1 = (2.0 / (Lambda**2)) * (block_term + diag_term)

    # term2: Tr(A_i A_j), A_i = K0^{-1} R1_i, R1_i=(Ehat_i D + D Ehat_i)/Lambda^2
    D_csr = sp.csr_matrix(D)
    A_list: List[np.ndarray] = []
    for i in range(n):
        w = W[:, i]
        rows = np.concatenate([heads, offE + np.arange(nE)])
        cols = np.concatenate([offE + np.arange(nE), heads])
        dat = np.concatenate([w, -w])
        Ehat = sp.csr_matrix((dat, (rows, cols)), shape=(N, N))
        R1 = (Ehat @ D_csr + D_csr @ Ehat) * (1.0 / (Lambda**2))
        Ai = (K0_inv @ R1.toarray()).astype(np.float64, copy=False)
        A_list.append(Ai)

    m = N * N
    G2 = np.zeros((n, n), dtype=np.float64)
    bs = 10
    for i0 in range(0, n, bs):
        i1 = min(n, i0 + bs)
        U = np.stack([A_list[i].reshape(m) for i in range(i0, i1)], axis=0)
        for j0 in range(i0, n, bs):
            j1 = min(n, j0 + bs)
            V = np.stack([A_list[j].T.reshape(m) for j in range(j0, j1)], axis=0)
            block = (U @ V.T).astype(np.float64, copy=False)
            G2[i0:i1, j0:j1] = block
            if j0 != i0:
                G2[j0:j1, i0:i1] = block.T

    Q = term1 + G2

    np.save(out_dir / "Q.npy", Q)
    np.savetxt(out_dir / "Q.csv", Q, delimiter=",")

    diag = np.diag(Q)
    off = Q - np.diag(diag)
    eig = np.linalg.eigvalsh(Q)
    summary = {
        "Lambda": Lambda,
        "sizes": {"V": int(nV), "E": int(nE), "F": int(nF), "N": int(N), "rank_im_d1": int(n)},
        "Q": {
            "diag_mean": float(np.mean(diag)),
            "diag_std": float(np.std(diag)),
            "offdiag_rms": float(np.sqrt(np.mean(off * off))),
            "offdiag_max_abs": float(np.max(np.abs(off))),
        },
        "eig": {
            "min": float(np.min(eig)),
            "max": float(np.max(eig)),
            "mean": float(np.mean(eig)),
            "std": float(np.std(eig)),
        },
    }

    # Optional finite-difference validation for a few random entries
    if args.validate:
        rng = np.random.default_rng(int(args.seed))
        eps = float(args.fd_eps)

        # Prebuild edge incidence for twisted D(A): only +1 head entries are phased.
        base_d0 = d0.toarray()  # (240×40)
        head_mask = np.zeros_like(base_d0)
        head_mask[np.arange(nE), heads] = 1.0
        tail_mask = np.zeros_like(base_d0)
        tail_mask[np.arange(nE), tails] = 1.0

        def build_D_twisted(a_edges: np.ndarray) -> np.ndarray:
            phase = np.exp(1j * a_edges)[:, None]
            d0A = (-1.0 * tail_mask) + (phase * head_mask)
            D0 = np.zeros((N, N), dtype=np.complex128)
            D0[0:nV, offE : offE + nE] = d0A.T
            D0[offE : offE + nE, 0:nV] = np.conjugate(d0A)
            # d1 blocks unchanged (real)
            d1_dense = d1.toarray()
            D0[offE : offE + nE, offE + nE :] = d1_dense.T
            D0[offE + nE :, offE : offE + nE] = d1_dense
            return D0

        def S_of_coeffs(coeffs: np.ndarray) -> float:
            Dtw = build_D_twisted(coeffs)
            return spectral_action_logdet(Dtw, Lambda)

        base = np.zeros(nE, dtype=float)
        S0 = S_of_coeffs(base)

        abs_errs: List[float] = []
        rel_errs: List[float] = []
        for _ in range(int(args.validate)):
            i = int(rng.integers(0, n))
            j = int(rng.integers(0, n))
            wi = W[:, i]
            wj = W[:, j]

            if i == j:
                Sp = S_of_coeffs(base + eps * wi)
                Sm = S_of_coeffs(base - eps * wi)
                fd = (Sp - 2.0 * S0 + Sm) / (eps * eps)
            else:
                Spp = S_of_coeffs(base + eps * wi + eps * wj)
                Spm = S_of_coeffs(base + eps * wi - eps * wj)
                Smp = S_of_coeffs(base - eps * wi + eps * wj)
                Smm = S_of_coeffs(base - eps * wi - eps * wj)
                fd = (Spp - Spm - Smp + Smm) / (4.0 * eps * eps)

            an = float(Q[i, j])
            abs_err = float(abs(fd - an))
            rel_err = float(abs_err / max(1e-12, abs(an)))
            abs_errs.append(abs_err)
            rel_errs.append(rel_err)

        summary["finite_difference_validation"] = {
            "pairs": int(args.validate),
            "eps": eps,
            "abs_err_max": float(np.max(abs_errs)),
            "abs_err_mean": float(np.mean(abs_errs)),
            "rel_err_max": float(np.max(rel_errs)),
            "rel_err_mean": float(np.mean(rel_errs)),
        }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Wrote: {out_dir / 'Q.npy'}")
    print(f"Wrote: {out_dir / 'Q.csv'}")
    print(f"Wrote: {out_dir / 'summary.json'}")
    print(f"Q diag mean:   {summary['Q']['diag_mean']}")
    print(f"Q diag std:    {summary['Q']['diag_std']}")
    print(f"Q offdiag rms: {summary['Q']['offdiag_rms']}")
    print(f"Q offdiag max: {summary['Q']['offdiag_max_abs']}")
    print(f"eig min/max:   {summary['eig']['min']} / {summary['eig']['max']}")


if __name__ == "__main__":
    main()

