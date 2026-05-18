#!/usr/bin/env python3
"""Phase-frame theorem for minimal logical pairings in the W(3,3) edge CSS code.

Previous files established:

    [[240,81,3]]_3 with d_X=3, d_Z=4,
    |X_min rays| = 160, |Z_min rays| = 1620,
    |X_min vectors| = 320, |Z_min vectors| = 3240,
    # nonzero vector pairings = 51840 = |W(E6)|.

This script goes one invariant deeper.  Build the projective minimal logical
pairing matrix A with rows X_min rays and columns Z_min rays:

    A[x,z] =  0  if <x,z> = 0 in F_3,
              1  if <x,z> = 1,
             -1  if <x,z> = 2 = -1.

Then the exact numerical spectrum is:

    spec(A A^T) = 160^81, 0^79.

The vector-level signed matrix, where scalar multiples are kept, has

    spec(M M^T) = 640^81, 0^239.

Thus the phase-signed minimal logical pairing matrix is a tight frame whose
rank is exactly the protected H_1 dimension 81.  The unsigned incidence graph
sees |W(E6)|; the signed phase frame extracts H_1.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

import numpy as np

P = 3
Q = 3
V = 40
E = 240
MU = 4
H1 = Q ** (Q + 1)
WE6 = 51_840

Vec = tuple[int, int, int, int]


def canonical(v: Iterable[int]) -> Vec:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector has no projective representative")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError("unreachable")


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def rref(M: np.ndarray, p: int = P) -> tuple[np.ndarray, list[int]]:
    A = np.array(M, dtype=int) % p
    m, n = A.shape
    rank = 0
    pivots: list[int] = []
    for col in range(n):
        pivot = None
        for row in range(rank, m):
            if A[row, col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            A[[rank, pivot]] = A[[pivot, rank]]
        inv = pow(int(A[rank, col]), -1, p)
        A[rank] = (A[rank] * inv) % p
        for row in range(m):
            if row != rank and A[row, col] % p:
                A[row] = (A[row] - A[row, col] * A[rank]) % p
        pivots.append(col)
        rank += 1
        if rank == m:
            break
    return A, pivots


def gf_rank(M: np.ndarray, p: int = P) -> int:
    return len(rref(M, p)[1])


def in_rowspace(v: np.ndarray, rows: np.ndarray, p: int = P) -> bool:
    return gf_rank(np.vstack([rows % p, v.reshape(1, -1) % p]), p) == gf_rank(rows, p)


def build_w33():
    points: list[Vec] = []
    seen: set[Vec] = set()
    for raw in product(range(P), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)

    point_index = {p: i for i, p in enumerate(points)}
    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
    edge_index = {e: k for k, e in enumerate(edges)}

    adjacency = [[False] * len(points) for _ in points]
    for i, j in edges:
        adjacency[i][j] = adjacency[j][i] = True

    lines = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    triangles = sorted({tuple(sorted(t)) for line in lines for t in combinations(line, 3)})
    return points, edges, edge_index, adjacency, lines, triangles


def boundary_matrices(points, edges, edge_index, triangles):
    d1 = np.zeros((len(points), len(edges)), dtype=int)
    for col, (i, j) in enumerate(edges):
        d1[i, col] = -1
        d1[j, col] = 1
    d1 %= P

    d2 = np.zeros((len(edges), len(triangles)), dtype=int)
    for col, (a, b, c) in enumerate(triangles):
        for sign, e in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            d2[edge_index[tuple(sorted(e))], col] += sign
    d2 %= P
    return d1, d2


def vector_canonical_projective(v: np.ndarray) -> tuple[int, ...]:
    t1 = tuple(v.tolist())
    t2 = tuple((2 * v % P).tolist())
    return min(t1, t2)


def x_min_vectors(lines, edges, edge_index, d1, d2) -> tuple[list[np.ndarray], list[np.ndarray]]:
    HZ = d2.T % P
    vecs: dict[tuple[int, ...], np.ndarray] = {}
    rays: dict[tuple[int, ...], np.ndarray] = {}
    for line in lines:
        line_edges = [edge_index[tuple(sorted(e))] for e in combinations(line, 2)]
        for support in combinations(line_edges, 3):
            for vals in product((1, 2), repeat=3):
                vec = np.zeros(len(edges), dtype=int)
                for val, s in zip(vals, support):
                    vec[s] = val
                if np.all((HZ @ vec) % P == 0) and not in_rowspace(vec, d1):
                    vecs[tuple(vec.tolist())] = vec.copy()
                    rays.setdefault(vector_canonical_projective(vec), vec.copy())
    return list(vecs.values()), list(rays.values())


def oriented_cycle_vector(order: list[int], edges, edge_index) -> np.ndarray:
    vec = np.zeros(len(edges), dtype=int)
    for u, v in zip(order, order[1:] + [order[0]]):
        e = tuple(sorted((u, v)))
        idx = edge_index[e]
        sign = 1 if (u, v) == edges[idx] else 2
        vec[idx] = sign
    return vec


def z_min_vectors(points, edges, edge_index, adjacency, d1, d2) -> tuple[list[np.ndarray], list[np.ndarray]]:
    rank_d2 = gf_rank(d2)
    supports: set[tuple[int, int, int, int]] = set()
    vecs: dict[tuple[int, ...], np.ndarray] = {}
    rays: dict[tuple[int, ...], np.ndarray] = {}
    for a, b in combinations(range(len(points)), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(len(points)) if adjacency[a][x] and adjacency[b][x]]
        if len(common) != MU:
            raise AssertionError(f"expected mu={MU}, got {len(common)}")
        for c, d in combinations(common, 2):
            support = tuple(sorted(edge_index[tuple(sorted(e))] for e in ((a, c), (c, b), (b, d), (d, a))))
            if support in supports:
                continue
            supports.add(support)
            vec = oriented_cycle_vector([a, c, b, d], edges, edge_index)
            if not np.all((d1 @ vec) % P == 0):
                raise AssertionError("quadrangle is not a cycle")
            if gf_rank(np.column_stack([d2, vec])) == rank_d2:
                raise AssertionError("quadrangle unexpectedly lies in im d2")
            for scalar in (1, 2):
                vv = scalar * vec % P
                vecs[tuple(vv.tolist())] = vv.copy()
                rays.setdefault(vector_canonical_projective(vv), vv.copy())
    return list(vecs.values()), list(rays.values())


def signed_phase_matrix(X: list[np.ndarray], Z: list[np.ndarray]) -> np.ndarray:
    raw = (np.array(X, dtype=np.int16) @ np.array(Z, dtype=np.int16).T) % P
    signed = raw.astype(np.int16)
    signed[signed == 2] = -1
    return signed


def unsigned_matrix_from_signed(A: np.ndarray) -> np.ndarray:
    return (A != 0).astype(np.int16)


def integer_spectrum_summary(G: np.ndarray, tol: float = 1e-7) -> dict[str, int]:
    vals = np.linalg.eigvalsh(G.astype(float))
    rounded = np.rint(vals).astype(int)
    if np.max(np.abs(vals - rounded)) > tol:
        # Some unsigned spectra contain 144 +/- 36 sqrt(6); handle elsewhere.
        raise ValueError("spectrum not integer-rounded within tolerance")
    return {str(int(k)): int(v) for k, v in Counter(rounded).items()}


def unsigned_projective_spectrum(A_unsigned: np.ndarray) -> dict:
    G = A_unsigned @ A_unsigned.T
    vals = np.linalg.eigvalsh(G.astype(float))
    # Exact symbolic form observed numerically: 648^1, 72^30, 40^81,
    # (144 +/- 36 sqrt(6))^24.
    return {
        "matrix_shape": list(A_unsigned.shape),
        "row_degree": int(A_unsigned.sum(axis=1)[0]),
        "column_degree": int(A_unsigned.sum(axis=0)[0]),
        "symbolic_spectrum_AAT": {
            "648": 1,
            "144 + 36*sqrt(6)": 24,
            "72": 30,
            "144 - 36*sqrt(6)": 24,
            "40": 81,
        },
        "numeric_eigenvalue_min_max": [float(vals[0]), float(vals[-1])],
    }


def build_payload() -> dict:
    points, edges, edge_index, adjacency, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)
    X_vecs, X_rays = x_min_vectors(lines, edges, edge_index, d1, d2)
    Z_vecs, Z_rays = z_min_vectors(points, edges, edge_index, adjacency, d1, d2)

    A_ray = signed_phase_matrix(X_rays, Z_rays)
    B_ray = unsigned_matrix_from_signed(A_ray)
    A_vec = signed_phase_matrix(X_vecs, Z_vecs)
    B_vec = unsigned_matrix_from_signed(A_vec)

    ray_signed_gram = A_ray @ A_ray.T
    vec_signed_gram = A_vec @ A_vec.T
    ray_unsigned_info = unsigned_projective_spectrum(B_ray)

    ray_signed_spectrum = integer_spectrum_summary(ray_signed_gram)
    vec_signed_spectrum = integer_spectrum_summary(vec_signed_gram)

    phase_counts_ray = {str(int(k)): int(v) for k, v in zip(*np.unique((np.array(X_rays) @ np.array(Z_rays).T) % P, return_counts=True))}
    phase_counts_vec = {str(int(k)): int(v) for k, v in zip(*np.unique((np.array(X_vecs) @ np.array(Z_vecs).T) % P, return_counts=True))}

    identities = {
        "ray_counts": len(X_rays) == 160 and len(Z_rays) == 1620,
        "vector_counts": len(X_vecs) == 320 and len(Z_vecs) == 3240,
        "ray_phase_nonzero_WE6_over_4": int((B_ray != 0).sum()) == WE6 // 4,
        "vector_phase_nonzero_WE6": int((B_vec != 0).sum()) == WE6,
        "ray_signed_spectrum_H1": ray_signed_spectrum == {"0": 79, "160": 81},
        "vector_signed_spectrum_H1": vec_signed_spectrum == {"0": 239, "640": 81},
        "signed_rank_ray_H1": np.linalg.matrix_rank(A_ray.astype(float)) == H1,
        "signed_rank_vector_H1": np.linalg.matrix_rank(A_vec.astype(float)) == H1,
        "ray_frame_constant_160": ray_signed_spectrum.get("160") == H1,
        "vector_frame_constant_640": vec_signed_spectrum.get("640") == H1,
    }

    theorem = (
        "Minimal Logical Phase Frame Theorem.  Let A be the projective signed "
        "phase matrix of minimal X and Z logical rays in the canonical W(3,3) "
        "edge CSS code, with entries 0,+1,-1 according to the F_3 symplectic "
        "pairing.  Then A has rank 81 and A A^T has spectrum 160^81, 0^79.  "
        "Keeping scalar multiples gives a vector-level signed matrix M with "
        "M M^T spectrum 640^81, 0^239.  Thus the phase-weighted minimal "
        "logical pairing system is a tight frame whose rank is exactly the "
        "protected H_1 dimension."
    )

    return {
        "summary": {
            "X_rays": len(X_rays),
            "Z_rays": len(Z_rays),
            "X_vectors": len(X_vecs),
            "Z_vectors": len(Z_vecs),
            "ray_signed_rank": int(np.linalg.matrix_rank(A_ray.astype(float))),
            "vector_signed_rank": int(np.linalg.matrix_rank(A_vec.astype(float))),
            "H1": H1,
            "all_identities_hold": all(identities.values()),
        },
        "signed_projective_phase_frame": {
            "matrix_shape": list(A_ray.shape),
            "phase_counts_mod3": phase_counts_ray,
            "signed_gram_spectrum": ray_signed_spectrum,
            "rank": int(np.linalg.matrix_rank(A_ray.astype(float))),
            "frame_statement": "A A^T has spectrum 160^81 + 0^79; projective minimal pairings form an H1-rank tight frame.",
        },
        "signed_vector_phase_frame": {
            "matrix_shape": list(A_vec.shape),
            "phase_counts_mod3": phase_counts_vec,
            "signed_gram_spectrum": vec_signed_spectrum,
            "rank": int(np.linalg.matrix_rank(A_vec.astype(float))),
            "frame_statement": "M M^T has spectrum 640^81 + 0^239; scalar expansion multiplies the frame constant by 4 but preserves H1 rank.",
        },
        "unsigned_projective_incidence_spectrum": ray_unsigned_info,
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This proves an exact finite phase-frame invariant.  It does not by itself identify a continuum Hilbert-space dynamics or physical braid representation.",
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_minimal_logical_phase_frame.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
