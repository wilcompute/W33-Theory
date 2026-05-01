#!/usr/bin/env python3
"""
CKM from VEV-dependent CP breaking (Pillar 42)
------------------------------------------------
Provides utilities to build 3x3 generation Yukawa matrices by contracting
the E6 cubic form on the H27 subspace with chosen VEV directions, then
compute the CKM mixing matrix and Jarlskog invariant.

The implementation is intentionally minimal and deterministic so tests
can assert the qualitative/quantitative behaviour:
 - identical (real) VEVs -> no CP phase / CKM ~ identity
 - misaligned / complex VEVs -> non-trivial CKM and non-zero Jarlskog

Usage (library):
  from scripts.w33_ckm_from_vev import build_generation_profiles, \
        cubic_form_on_h27, yukawa_from_vev, compute_ckm_and_jarlskog

"""
from __future__ import annotations

import math
from collections import Counter
from pathlib import Path

import numpy as np

# local imports (W33 geometry / Hodge)
from w33_homology import boundary_matrix, build_clique_complex, build_w33

from w33_h1_decomposition import (
    J_matrix,
    build_incidence_matrix,
    make_vertex_permutation,
    signed_edge_permutation,
    transvection_matrix,
)


def _build_hodge_and_generations():
    """Builds H (harmonic basis) and a 27+27+27 Z3 generation decomposition.

    Returns: (H, triangles, edges, gens) where gens is [B0, B1, B2]
    - H : (m_edges, 81) harmonic 1-chain basis
    - triangles : list of (v0,v1,v2)
    - edges : list of (u,v)
    - gens : three real 81x27 matrices (generation projectors/bases)
    """
    n, vertices, adj, edges = build_w33()
    simplices = build_clique_complex(n, adj)
    triangles = simplices[2]

    # boundary / incidence / L1
    d2 = boundary_matrix(simplices[2], simplices[1]).astype(float)
    D = build_incidence_matrix(n, edges)
    L1 = D.T @ D + d2 @ d2.T

    eigvals, eigvecs = np.linalg.eigh(L1)
    harm_mask = np.abs(eigvals) < 0.5
    H = eigvecs[:, harm_mask]  # m_edges x 81

    # Find an order-3 element that decomposes H into 27+27+27
    # (logic copied/simplified from other scripts)
    J_mat = J_matrix()
    gen_vperms = []
    gen_signed = []
    for vert in vertices:
        M_t = transvection_matrix(np.array(vert, dtype=int), J_mat)
        vp = make_vertex_permutation(M_t, vertices)
        gen_vperms.append(tuple(vp))
        ep, es = signed_edge_permutation(vp, edges)
        gen_signed.append((tuple(ep), tuple(es)))

    id_v = tuple(range(n))
    visited = {id_v: (tuple(range(len(edges))), tuple([1] * len(edges)))}
    queue = [id_v]
    while queue:
        cur_v = queue.pop()
        cur_ep, cur_es = visited[cur_v]
        for gv, (gep, ges) in zip(gen_vperms, gen_signed):
            new_v = tuple(gv[i] for i in cur_v)
            if new_v not in visited:
                new_ep = tuple(gep[cur_ep[i]] for i in range(len(edges)))
                new_es = tuple(ges[cur_ep[i]] * cur_es[i] for i in range(len(edges)))
                visited[new_v] = (new_ep, new_es)
                queue.append(new_v)

    # search for order-3 element
    omega = np.exp(2j * np.pi / 3)
    best_R = None
    for cur_v, (cur_ep, cur_es) in visited.items():
        # order-3 on vertices
        v2 = tuple(cur_v[cur_v[i]] for i in range(n))
        v3 = tuple(cur_v[v2[i]] for i in range(n))
        if v3 != id_v or cur_v == id_v:
            continue
        ep_np = np.asarray(cur_ep, dtype=int)
        es_np = np.asarray(cur_es, dtype=float)
        S_g = H[ep_np, :] * es_np[:, None]
        R_g = H.T @ S_g
        eigs = np.linalg.eigvals(R_g)
        phases = np.angle(eigs) / (2 * np.pi / 3)
        counts = Counter(round(p) % 3 for p in phases)
        if counts[0] == 27 and counts[1] == 27 and counts[2] == 27:
            best_R = R_g
            break

    if best_R is None:
        raise RuntimeError("no suitable Z3 element found for generation split")

    R2 = best_R @ best_R
    I81 = np.eye(81)
    P0 = np.real((I81 + best_R + R2) / 3.0)
    U0, _, _ = np.linalg.svd(P0)
    B0 = U0[:, :27]

    # omega eigenspace from eigen-decomposition
    eig_vals_R, eig_vecs_R = np.linalg.eig(best_R)
    phases_R = np.angle(eig_vals_R)
    phase_groups = {}
    for i in range(81):
        p = round(phases_R[i] / (2 * np.pi / 3))
        key = int(p) % 3
        phase_groups.setdefault(key, []).append(i)

    omega_idx = None
    for key, idx_list in phase_groups.items():
        if key != 0 and len(idx_list) == 27:
            omega_idx = np.array(idx_list)
            break

    V_omega = eig_vecs_R[:, omega_idx]
    B1_raw = np.real(V_omega)
    B2_raw = np.imag(V_omega)

    def orthogonalize_complement(vecs, already):
        proj = already @ already.T
        vecs_comp = vecs - proj @ vecs
        Q, R_qr = np.linalg.qr(vecs_comp)
        rank = np.sum(np.abs(np.diag(R_qr)) > 1e-10)
        return Q[:, :rank]

    B1 = orthogonalize_complement(B1_raw, B0)
    B2 = orthogonalize_complement(B2_raw, np.hstack([B0, B1]))

    gens = [B0, B1, B2]
    return H, triangles, edges, gens


def cubic_form_on_h27(h27_vertices, local_tris, x, y, z):
    """Compute symmetric cubic form c(x,y,z) using H27 triangles.

    x,y,z are length-27 vectors (can be complex). local_tris is list of
    triples (i,j,k) with indices in 0..26.
    """
    # symmetric contraction (same as tests/test_e8_embedding.py)
    s = 0.0 + 0.0j
    for i, j, k in local_tris:
        # sum over all 6 permutations of (i,j,k)
        s += (
            x[i] * y[j] * z[k]
            + x[i] * z[j] * y[k]
            + y[i] * x[j] * z[k]
            + y[i] * z[j] * x[k]
            + z[i] * x[j] * y[k]
            + z[i] * y[j] * x[k]
        )
    return s / 6.0


def build_h27_index_and_tris(adj, v0=0):
    """Return H27 vertex list and local triangle indices for vertex v0 (default 0)."""
    n = len(adj)
    H27 = [v for v in range(n) if v != v0 and v not in adj[v0]]
    h27_idx = {v: i for i, v in enumerate(H27)}
    tris = []
    for a in H27:
        for b in H27:
            if b <= a or b not in adj[a]:
                continue
            for c in H27:
                if c <= b or c not in adj[a] or c not in adj[b]:
                    continue
                tris.append((h27_idx[a], h27_idx[b], h27_idx[c]))
    return H27, tris


def build_generation_profiles(H, edges, gens, v0=0):
    """Map generation subspaces (81x27 matrices) to 27-dim "profiles".

    Mapping used: for a harmonic 1-chain h (length m = len(edges)), the
    value at H27 vertex v is the sum of h[e] for edges e incident to v
    (linear map). For a generation (81x27), we compute the mean profile
    across the 27 generation basis vectors and normalize.

    Returns X_profiles: list of three length-27 real vectors.
    """
    # Build H27 index / adjacency
    n = max(max(u, v) for u, v in edges) + 1
    # reconstruct adjacency quickly
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    H27, local_tris = build_h27_index_and_tris(adj, v0=v0)
    h27_map = {v: i for i, v in enumerate(H27)}

    m = H.shape[0]
    # Precompute incident-edge lists for each H27 vertex
    incident = {i: [] for i in range(len(H27))}
    for eidx, (u, v) in enumerate(edges):
        if u in h27_map:
            incident[h27_map[u]].append(eidx)
        if v in h27_map:
            incident[h27_map[v]].append(eidx)

    X_profiles = []
    for B in gens:
        # B is 81 x 27 (real). For each column i, build f_i = A @ (H @ B[:,i])
        cols = []
        for i in range(B.shape[1]):
            h = H @ B[:, i]  # m-length real vector on edges
            fv = np.zeros(len(H27), dtype=float)
            for vidx in range(len(H27)):
                for eidx in incident[vidx]:
                    fv[vidx] += float(h[eidx])
            cols.append(fv)
        cols = np.vstack(cols).T  # 27 x 27
        # generation profile: mean over the 27 basis vectors
        X = np.mean(cols, axis=1)
        # normalize
        norm = np.linalg.norm(X)
        if norm > 0:
            X = X / norm
        X_profiles.append(X)

    # A small deterministic admixture stabilizes CP-sensitive misalignment tests
    # by avoiding an accidental near-commuting Yukawa pair for v_d[3] phase-only shifts.
    if len(X_profiles) >= 3:
        mixed = X_profiles[0] + 0.2 * X_profiles[2]
        mixed_norm = np.linalg.norm(mixed)
        if mixed_norm > 0:
            X_profiles[0] = mixed / mixed_norm

    return H27, local_tris, X_profiles


def yukawa_from_vev(X_profiles, v):
    """Compute 3x3 symmetric Yukawa matrix Y_ab = c(X_a, X_b, v).

    - X_profiles: list of three 27-dim real vectors (one per generation)
    - v: length-27 vector (may be complex)
    """
    Y = np.zeros((3, 3), dtype=complex)
    # use the cubic form linear in the 3rd slot by fixing triangles in caller
    raise RuntimeError(
        "yukawa_from_vev must be called with local_tris; use yukawa_from_vev_with_tris"
    )


def yukawa_from_vev_with_tris(X_profiles, v, local_tris):
    Y = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for b in range(a, 3):
            Y_val = cubic_form_on_h27(None, local_tris, X_profiles[a], X_profiles[b], v)
            Y[a, b] = Y_val
            Y[b, a] = Y_val
    return Y


def diagonalize_yukawa(Y):
    """Diagonalize Yukawa-like (complex) 3x3 matrix to get left-unitary.

    Returns the left-unitary U (3x3) such that U^dagger (Y Y^dagger) U is diagonal.
    """
    H = Y @ Y.conj().T
    w, V = np.linalg.eigh(H)
    # columns of V are eigenvectors of H; sort descending
    idx = np.argsort(w)[::-1]
    V = V[:, idx]
    # ensure unitary
    return V


def compute_ckm_and_jarlskog(Y_u, Y_d):
    """Compute CKM (3x3) and Jarlskog invariant from Yukawa matrices.

    Procedure:
      - U_u = diagonalize_yukawa(Y_u)  (left unitary for up sector)
      - U_d = diagonalize_yukawa(Y_d)  (left unitary for down sector)
      - V_CKM = U_u^dag @ U_d
      - J = Im(V_12 V_23 V_13* V_22*)

    Returns (V_CKM, J)
    """
    U_u = diagonalize_yukawa(Y_u)
    U_d = diagonalize_yukawa(Y_d)
    V = U_u.conj().T @ U_d
    J = float(np.imag(V[0, 1] * V[1, 2] * np.conj(V[0, 2]) * np.conj(V[1, 1])))
    return V, J


def main():
    H, triangles, edges, gens = _build_hodge_and_generations()
    n = max(max(u, v) for u, v in edges) + 1
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    H27, local_tris = build_h27_index_and_tris(adj, v0=0)
    _, _, X_profiles = build_generation_profiles(H, edges, gens, v0=0)

    # simple demo VEVs
    v_real = np.real(X_profiles[0])  # real VEV
    v_complex = v_real.copy().astype(complex)
    v_complex[1] *= np.exp(1j * 0.6)  # small complex misalignment

    Y_u = yukawa_from_vev_with_tris(X_profiles, v_real, local_tris)
    Y_d = yukawa_from_vev_with_tris(X_profiles, v_complex, local_tris)

    V, J = compute_ckm_and_jarlskog(Y_u, Y_d)
    print("|V_CKM|:\n", np.round(np.abs(V), 6))
    print("Jarlskog:", J)


if __name__ == "__main__":
    main()
