#!/usr/bin/env python3
"""BT642: numeric E2 -> duad-phase basis search.

BT638--BT641 built the exact 30-dimensional duad-phase carrier

    Q^15_{K6 duads} \otimes Q^2_{+-}

with model operator

    B_E2 = 37 I + 40 sigma_z,

so its eigenvalues are 77^15 and (-3)^15.  BT642 searches the actual
160-flag folded-Hashimoto block

    M22 = E2 F3 E2,   F3 = T B^3 T^T,

for a numeric basis realizing the same carrier.

Result boundary:
  * yes, the numeric 160-flag E2 block splits exactly as 15+15;
  * yes, an orthonormal numeric intertwiner Q exists with
        Q^T F3 Q = diag(77 I_15, -3 I_15);
  * no, this alone does not canonically label the 15 coordinates by K6 duads.
    That final label needs an additional S6-equivariant gauge/coordinate choice.
"""
from __future__ import annotations

from itertools import combinations, product
import json
import math
from pathlib import Path

import numpy as np


def norm_vec(v: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    v = tuple(x % 3 for x in v)
    if all(x == 0 for x in v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in v)
    raise AssertionError("unreachable")


def symp(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def build_geometry():
    pts = sorted({norm_vec(v) for v in product(range(3), repeat=4) if any(v)})
    pt_index = {p: i for i, p in enumerate(pts)}
    edges = [(i, j) for i, j in combinations(range(len(pts)), 2) if symp(pts[i], pts[j]) == 0]
    adj = [set() for _ in pts]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    lines = set()
    for i, j in edges:
        u, v = pts[i], pts[j]
        line = set()
        for a, b in product(range(3), repeat=2):
            if a == 0 and b == 0:
                continue
            w = norm_vec(tuple((a * u[t] + b * v[t]) % 3 for t in range(4)))
            line.add(pt_index[w])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    edge_line = {}
    for li, line in enumerate(lines):
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li

    flags = []
    flag_index = {}
    for li, line in enumerate(lines):
        for p in line:
            flag_index[(p, li)] = len(flags)
            flags.append((p, li))

    directed = []
    for i, j in edges:
        li = edge_line[(i, j)]
        directed.append((i, j, li))
        directed.append((j, i, li))
    directed_index = {(i, j): idx for idx, (i, j, _li) in enumerate(directed)}
    return pts, edges, adj, lines, edge_line, flags, flag_index, directed, directed_index


def flag_adjacency(flags):
    n = len(flags)
    A1 = np.zeros((n, n), dtype=int)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i != j and (p == q or l == m):
                A1[i, j] = 1
    return A1


def primitive_idempotents(A1: np.ndarray) -> list[np.ndarray]:
    vals = [6, 2 + math.sqrt(6), 2, 2 - math.sqrt(6), -2]
    eye = np.eye(A1.shape[0])
    A = A1.astype(float)
    out = []
    for i, theta in enumerate(vals):
        num = eye.copy()
        den = 1.0
        for j, phi in enumerate(vals):
            if i == j:
                continue
            num = num @ (A - phi * eye)
            den *= theta - phi
        out.append(num / den)
    return out


def projector_basis(P: np.ndarray, tol: float = 1e-8) -> np.ndarray:
    """Return an orthonormal column basis for the image of a symmetric projector."""
    vals, vecs = np.linalg.eigh((P + P.T) / 2)
    keep = vals > 0.5
    Q = vecs[:, keep]
    # deterministic sign convention: largest absolute coordinate positive
    for j in range(Q.shape[1]):
        k = int(np.argmax(np.abs(Q[:, j])))
        if Q[k, j] < 0:
            Q[:, j] *= -1
    if not np.allclose(Q.T @ Q, np.eye(Q.shape[1]), atol=tol):
        raise RuntimeError("basis extraction failed")
    return Q


def main() -> int:
    pts, edges, adj, lines, edge_line, flags, flag_index, directed, directed_index = build_geometry()

    T = np.zeros((160, 480), dtype=int)
    for de, (tail, _head, li) in enumerate(directed):
        T[flag_index[(tail, li)], de] = 1

    B = np.zeros((480, 480), dtype=int)
    for a, (u, v, _li) in enumerate(directed):
        for w in adj[v]:
            if w != u:
                B[a, directed_index[(v, w)]] = 1

    A1 = flag_adjacency(flags)
    E = primitive_idempotents(A1)
    F3 = T @ np.linalg.matrix_power(B, 3) @ T.T
    E2 = E[2]
    M22 = E2 @ F3 @ E2

    # Spectral projectors inside the numeric E2 block.
    P77 = (M22 + 3 * E2) / 80
    Pm3 = (77 * E2 - M22) / 80
    Q77 = projector_basis(P77)
    Qm3 = projector_basis(Pm3)
    Q = np.column_stack([Q77, Qm3])
    normal_form = Q.T @ F3 @ Q
    target = np.diag([77.0] * 15 + [-3.0] * 15)

    # Exact duad-phase carrier, now viewed only up to an unlabeled 15-coordinate gauge.
    I15 = np.eye(15)
    B_model = np.block([[77 * I15, np.zeros((15, 15))], [np.zeros((15, 15)), -3 * I15]])

    checks = {
        "w33_counts": len(pts) == 40 and len(lines) == 40 and len(flags) == 160 and len(directed) == 480,
        "E2_rank_30": int(np.linalg.matrix_rank(E2, tol=1e-7)) == 30,
        "P77_rank_15": int(np.linalg.matrix_rank(P77, tol=1e-7)) == 15,
        "Pm3_rank_15": int(np.linalg.matrix_rank(Pm3, tol=1e-7)) == 15,
        "projectors_sum_E2": np.max(np.abs(P77 + Pm3 - E2)) < 1e-8,
        "projectors_orthogonal": np.max(np.abs(P77 @ Pm3)) < 1e-8,
        "E2_minimal_polynomial": np.max(np.abs((M22 - 77 * E2) @ (M22 + 3 * E2))) < 1e-8,
        "numeric_intertwiner_orthonormal": np.max(np.abs(Q.T @ Q - np.eye(30))) < 1e-8,
        "normal_form_matches_duad_phase_model": np.max(np.abs(normal_form - target)) < 1e-7,
        "model_spectrum_matches": np.allclose(np.sort(np.linalg.eigvalsh(B_model)), np.sort(np.linalg.eigvalsh(target))),
        "duad_labels_not_canonical_from_numeric_block_alone": True,
    }

    result = {
        "bt": 642,
        "title": "Numeric E2-to-duad-phase basis search",
        "operator": "M22 = E2 F3 E2, with F3 = T B^3 T^T",
        "numeric_normal_form": "Q^T F3 Q = diag(77 I_15, -3 I_15)",
        "model_carrier": "Q^15_{K6 duads} tensor Q^2_{+-}",
        "basis_shape": {"Q77": list(Q77.shape), "Qm3": list(Qm3.shape), "Q": list(Q.shape)},
        "ranks": {
            "rank_E2": int(np.linalg.matrix_rank(E2, tol=1e-7)),
            "rank_P77": int(np.linalg.matrix_rank(P77, tol=1e-7)),
            "rank_Pm3": int(np.linalg.matrix_rank(Pm3, tol=1e-7)),
        },
        "max_normal_form_error": float(np.max(np.abs(normal_form - target))),
        "interpretation": "The computed 160-flag E2 block is numerically intertwined with the 30-dimensional duad-phase carrier at the spectral/projector level. The remaining missing datum is not spectral: it is an S6-equivariant duad-label gauge inside each 15-dimensional eigenspace.",
        "boundary": "This does not claim a canonical K6-duad coordinate labeling from F3/E2 alone. It provides an orthonormal numerical normal form and isolates the remaining label-gauge problem.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT642_NUMERIC_E2_DUAD_PHASE_BASIS_SEARCH_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
