#!/usr/bin/env python3
"""Attempt to find an E8 embedding for W33 by spectral embedding + ICP-style matching.

Produces diagnostics and writes PART_CVII_e8_embedding_attempt.json on success/failure.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# --- Build W33 vertices (projective points PG(3, F3))
F = 3


def canonical_rep(v):
    # v is tuple of ints mod 3
    for i in range(4):
        if v[i] % F != 0:
            inv = None
            # find multiplicative inverse mod 3
            a = v[i] % F
            if a == 1:
                inv = 1
            elif a == 2:
                inv = 2
            else:
                inv = 0
            return tuple(((x * inv) % F) for x in v)
    return None


# generate all nonzero vectors in F3^4
all_vectors = []
for a in range(F):
    for b in range(F):
        for c in range(F):
            for d in range(F):
                if (a, b, c, d) != (0, 0, 0, 0):
                    all_vectors.append((a, b, c, d))

reps = set()
for v in all_vectors:
    cr = canonical_rep(v)
    if cr:
        reps.add(cr)

vertices = sorted(list(reps))
assert len(vertices) == 40


# symplectic form: x1*y2 - x2*y1 + x3*y4 - x4*y3 (mod 3)
def symp(x, y):
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F


# adjacency
n = len(vertices)
A = np.zeros((n, n), dtype=int)
edges = []
for i, vi in enumerate(vertices):
    for j, vj in enumerate(vertices):
        if i < j:
            if symp(vi, vj) == 0:
                A[i, j] = A[j, i] = 1
                edges.append((i, j))

m = len(edges)
print(f"W33: n={n}, edges={m}")
# verify SRG properties
deg = A.sum(axis=1)
print("degree min,max:", deg.min(), deg.max())

# eigen decomposition
vals, vecs = np.linalg.eigh(A.astype(float))
# sort descending
idx = np.argsort(vals)[::-1]
vals = vals[idx]
vecs = vecs[:, idx]
print("top eigenvalues:", vals[:10])

# choose 8-dimensional embedding: pick 8 eigenvectors from the eigenspace of eigenvalue 2 if available.
# find indices of eigenvalues near 2 (within tol)
idxs_2 = [i for i, v in enumerate(vals) if abs(v - 2.0) < 1e-6]
if len(idxs_2) >= 8:
    chosen = idxs_2[:8]
else:
    # fallback: take the top 8 non-trivial after removing the first eigenvector (12)
    chosen = list(range(1, 9))

X = vecs[:, chosen]
# optionally scale columns to unit variance
X = X - X.mean(axis=0)
X = X / (X.std(axis=0) + 1e-12)
print("X shape:", X.shape)

# collect oriented edge vectors (i<j) as one set of 240 vectors, choose a consistent orientation
E = []
for i, j in edges:
    v = X[i] - X[j]
    # normalize
    nv = np.linalg.norm(v)
    if nv > 0:
        E.append(v / nv)
E = np.vstack(E)  # shape (240, 8)
print("Edge vectors shape:", E.shape)

# --- build E8 root set
# Type 1: permutations of (±1, ±1, 0,0,0,0,0,0)
E8 = []
import itertools

for i in range(8):
    for j in range(i + 1, 8):
        for si in (-1, 1):
            for sj in (-1, 1):
                r = [0] * 8
                r[i] = si
                r[j] = sj
                E8.append(tuple(r))

# Type 2: (±1/2)^8 with even number of minus signs
for signs in itertools.product([-1, 1], repeat=8):
    if sum(1 for s in signs if s < 0) % 2 == 0:
        r = tuple(s * 0.5 for s in signs)
        E8.append(r)

# ensure 240 roots
E8 = np.array(E8, dtype=float)
assert E8.shape[0] == 240
# normalize
E8 = E8 / np.linalg.norm(E8, axis=1, keepdims=True)
print("E8 roots shape:", E8.shape)

# ICP-like iterative closest point between E (N x 8) and E8 (N x 8)
try:
    from scipy.optimize import linear_sum_assignment
    from scipy.spatial import cKDTree
except Exception:
    print("scipy required: install 'scipy' in your venv (pip install scipy)")
    raise

A_mat = E.copy()
B_mat = E8.copy()

# We'll attempt to find orthogonal R that maps A_mat -> B_mat with bijection via iterative NN matching


def orthogonal_procrustes(A, B):
    # Solve min_R ||A R - B||_F s.t. R^T R = I
    # A, B: (N, d)
    M = A.T @ B
    U, s, Vt = np.linalg.svd(M)
    R = U @ Vt
    # ensure det(R)=1 (proper rotation)
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    return R


# initial random shuffle correspondence
perm = np.arange(B_mat.shape[0])
np.random.seed(0)
np.random.shuffle(perm)

R = np.eye(8)
prev_score = 0
best = {"R": R, "matches": 0, "errors": None}

tol = 1e-6
for it in range(200):
    # map A via R
    A_mapped = A_mat @ R
    # nearest neighbor from A_mapped to B_mat
    tree = cKDTree(B_mat)
    dists, idx = tree.query(A_mapped, k=1)
    # create tentative matched arrays
    B_match = B_mat[idx]
    # compute new R via procrustes
    R_new = orthogonal_procrustes(A_mat, B_match)
    # compute score
    A_mapped_new = A_mat @ R_new
    dists_new = np.linalg.norm(A_mapped_new - B_match, axis=1)
    matches = np.sum(dists_new < 1e-6)
    mean_err = float(dists_new.mean())
    if matches > best["matches"] or (
        matches == best["matches"] and mean_err < (best["errors"] or 1e9)
    ):
        best = {"R": R_new.copy(), "matches": int(matches), "errors": float(mean_err)}
    if matches > prev_score:
        prev_score = matches
        R = R_new
    else:
        # small improvement? keep and continue
        R = R_new
    if it % 10 == 0:
        print(f"it={it} matches={matches} mean_err={mean_err:.3e}")
    # early break if near perfect
    if matches >= 230 and mean_err < 1e-6:
        break

print("Best matches:", best["matches"], "mean_err:", best["errors"])

# Final evaluation: compute exact bijection greedily to avoid collisions
A_mapped_final = A_mat @ best["R"]
# build cost matrix using squared distances
cost = np.linalg.norm(A_mapped_final[:, None, :] - B_mat[None, :, :], axis=2)
row_ind, col_ind = linear_sum_assignment(cost)
assigned_dist = cost[row_ind, col_ind]
matches_final = np.sum(assigned_dist < 1e-6)
print(
    "Assignment matches (dist<1e-6):",
    int(matches_final),
    "mean assigned dist:",
    float(assigned_dist.mean()),
)

out = {
    "n_vertices": int(n),
    "n_edges": int(m),
    "embedding_dim": 8,
    "icp_matches": int(best["matches"]),
    "icp_mean_err": float(best["errors"]),
    "assignment_matches": int(matches_final),
    "assignment_mean_err": float(assigned_dist.mean()),
}

(Path.cwd() / "PART_CVII_e8_embedding_attempt.json").write_text(
    json.dumps(out, indent=2)
)
print("Wrote PART_CVII_e8_embedding_attempt.json")
print(json.dumps(out, indent=2))
