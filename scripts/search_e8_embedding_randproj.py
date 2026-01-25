#!/usr/bin/env python3
"""Try many random 8D projections from the eigenvalue-2 eigenspace and run ICP-style matching.
Writes PART_CVII_e8_embedding_randproj.json with best result found.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import itertools
import time

# reuse construction from previous script
F = 3

def canonical_rep(v):
    for i in range(4):
        if v[i] % F != 0:
            a = v[i] % F
            inv = 1 if a==1 else 2
            return tuple(((x * inv) % F) for x in v)
    return None

all_vectors = [(a,b,c,d) for a in range(F) for b in range(F) for c in range(F) for d in range(F) if (a,b,c,d)!=(0,0,0,0)]
reps = set(canonical_rep(v) for v in all_vectors if canonical_rep(v))
vertices = sorted(list(reps))

def symp(x,y):
    return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2]) % F

n = len(vertices)
A = np.zeros((n,n), dtype=int)
edges = []
for i,vi in enumerate(vertices):
    for j,vj in enumerate(vertices):
        if i < j and symp(vi, vj) == 0:
            A[i,j] = A[j,i] = 1
            edges.append((i,j))

# eigenvectors
vals, vecs = np.linalg.eigh(A.astype(float))
idx = np.argsort(vals)[::-1]
vals = vals[idx]
vecs = vecs[:, idx]

# collect eigenspace for eigenvalue ~2
eig2_idx = [i for i,v in enumerate(vals) if abs(v-2.0) < 1e-6]
EIG2 = vecs[:, eig2_idx]  # shape 40 x 24
print('EIG2 shape', EIG2.shape)

# precompute normalized edge vectors function

def embedding_from_basis(basis):
    # basis: 24x8 projection matrix mapping to 8D; compute X = (EIG2 @ basis)
    X = EIG2 @ basis
    X = X - X.mean(axis=0)
    X = X / (X.std(axis=0) + 1e-12)
    E = []
    for (i,j) in edges:
        v = X[i] - X[j]
        nv = np.linalg.norm(v)
        if nv > 0:
            E.append(v / nv)
    return np.vstack(E)

# E8 roots (normalized)
E8 = []
for i in range(8):
    for j in range(i+1,8):
        for si in (-1,1):
            for sj in (-1,1):
                r=[0]*8; r[i]=si; r[j]=sj
                E8.append(tuple(r))
for signs in itertools.product([-1,1], repeat=8):
    if sum(1 for s in signs if s<0) % 2 == 0:
        E8.append(tuple(s*0.5 for s in signs))
E8 = np.array(E8, dtype=float)
E8 = E8 / np.linalg.norm(E8, axis=1, keepdims=True)

from scipy.spatial import cKDTree
from scipy.optimize import linear_sum_assignment

# ICP helpers

def orthogonal_procrustes(A, B):
    M = A.T @ B
    U, s, Vt = np.linalg.svd(M)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    return R

# search loop
best_res = None
start = time.time()
trials = 400
for t in range(trials):
    # random 24x8 matrix
    Rnd = np.random.normal(size=(EIG2.shape[1], 8))
    # orthonormalize columns via QR
    Q, _ = np.linalg.qr(Rnd)
    basis = Q[:, :8]
    A_mat = embedding_from_basis(basis)
    # ICP quick iterations
    R = np.eye(8)
    best_local_matches = 0
    best_local_err = 1e9
    treeB = cKDTree(E8)
    for it in range(60):
        A_mapped = A_mat @ R
        dists, idxs = treeB.query(A_mapped, k=1)
        B_match = E8[idxs]
        R_new = orthogonal_procrustes(A_mat, B_match)
        A_mapped_new = A_mat @ R_new
        d_new = np.linalg.norm(A_mapped_new - B_match, axis=1)
        matches = np.sum(d_new < 1e-6)
        mean_err = float(d_new.mean())
        if matches > best_local_matches or (matches == best_local_matches and mean_err < best_local_err):
            best_local_matches = int(matches)
            best_local_err = mean_err
            best_local_R = R_new.copy()
        R = R_new
        if matches >= 220 and mean_err < 1e-6:
            break
    # final assignment
    A_mapped_final = A_mat @ best_local_R
    cost = np.linalg.norm(A_mapped_final[:, None, :] - E8[None, :, :], axis=2)
    row_ind, col_ind = linear_sum_assignment(cost)
    assigned_dist = cost[row_ind, col_ind]
    matches_final = int(np.sum(assigned_dist < 1e-6))
    mean_assigned = float(assigned_dist.mean())
    if best_res is None or matches_final > best_res['matches'] or (matches_final == best_res['matches'] and mean_assigned < best_res['mean_err']):
        best_res = {
            'trial': t,
            'matches': matches_final,
            'mean_err': mean_assigned,
            'icp_matches': best_local_matches,
            'icp_mean_err': best_local_err
        }
    if t % 20 == 0:
        print(f"t={t} best matches so far={best_res['matches']} (trial {best_res['trial']})")

elapsed = time.time() - start
out = {'best': best_res, 'trials': trials, 'elapsed_seconds': elapsed}
Path('PART_CVII_e8_embedding_randproj.json').write_text(json.dumps(out, indent=2))
print('Wrote PART_CVII_e8_embedding_randproj.json')
print(json.dumps(out, indent=2))
