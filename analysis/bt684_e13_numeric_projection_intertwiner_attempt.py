#!/usr/bin/env python3
"""
BT684 — Numeric projection/intertwiner attempt for E1+E3 packets.

This is the first actual numeric test after BT681--BT683.

What it does:
  1. Rebuilds W(3,3) as the symplectic polar graph on PG(3,3).
  2. Builds the point-line Levi graph and its 160 flag-edge line graph X.
  3. Diagonalizes the Levi-flag adjacency A_X.
  4. Extracts the two 24-dimensional primitive sectors E1,E3 as the two
     multiplicity-24 eigenspaces.
  5. Uses the BT648 canonical 24-flag S4 carrier O0 as a first numeric carrier.
  6. Splits O0 into four 6-blocks and projects the carrier/block indicators into
     E1 and E3.

Result boundary:
  This is a genuine numeric projection diagnostic, but it is not yet a canonical
  intertwiner.  The BT648 orbit index order is assumed to match the canonical
  projective-point/line ordering used here.  The output is therefore an
  executable certificate of projection ranks and residuals, not a final theorem
  identifying a unique E1/E3 packet basis.
"""
from __future__ import annotations

from itertools import combinations
from collections import deque
import numpy as np

MOD = 3
O0 = [0,4,8,12,22,33,38,42,47,58,66,71,73,86,99,103,105,110,114,131,136,143,152,157]


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    v = tuple(x % 3 for x in v)
    for x in v:
        if x:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def projective_points():
    pts = set()
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    if (a,b,c,d) != (0,0,0,0):
                        pts.add(canon((a,b,c,d)))
    return sorted(pts)


def symp(x, y):
    # Standard alternating form on F3^4.
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_w33():
    pts = projective_points()
    n = len(pts)
    adj = np.zeros((n,n), dtype=int)
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i,j] = adj[j,i] = 1
    assert n == 40
    assert adj.sum(axis=1).tolist() == [12]*40
    return pts, adj


def build_lines(adj):
    lines = []
    for quad in combinations(range(40), 4):
        ok = True
        for i, j in combinations(quad, 2):
            if adj[i,j] == 0:
                ok = False
                break
        if ok:
            lines.append(tuple(quad))
    # Maximal K4 lines of GQ(3,3)
    assert len(lines) == 40
    edge_seen = {}
    for li, line in enumerate(lines):
        for e in combinations(line, 2):
            edge_seen[tuple(sorted(e))] = li
    assert len(edge_seen) == 240
    return sorted(lines)


def build_flag_line_graph(lines):
    flags = []
    point_to_lines = {p: [] for p in range(40)}
    for li, line in enumerate(lines):
        for p in line:
            point_to_lines[p].append(li)
    for p in range(40):
        for li in sorted(point_to_lines[p]):
            flags.append((p, li))
    assert len(flags) == 160
    A = np.zeros((160,160), dtype=float)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i < j and (p == q or l == m):
                A[i,j] = A[j,i] = 1.0
    assert np.all(A.sum(axis=1) == 6)
    return flags, A


def projector_for_eigenvalue(A, target, tol=1e-7):
    vals, vecs = np.linalg.eigh(A)
    mask = np.abs(vals - target) < tol
    V = vecs[:, mask]
    return vals[mask], V @ V.T


def projector_groups(A):
    vals, vecs = np.linalg.eigh(A)
    groups = []
    used = np.zeros_like(vals, dtype=bool)
    for i, val in enumerate(vals):
        if used[i]:
            continue
        mask = np.abs(vals - val) < 1e-7
        used |= mask
        groups.append((float(np.mean(vals[mask])), int(mask.sum()), vecs[:,mask] @ vecs[:,mask].T))
    groups.sort(key=lambda x: x[0], reverse=True)
    return groups


def rank_projected(P, vectors, tol=1e-7):
    M = np.column_stack([P @ v for v in vectors])
    s = np.linalg.svd(M, compute_uv=False)
    return int((s > tol).sum()), [float(x) for x in s]


def indicator(indices, n=160):
    v = np.zeros(n)
    v[list(indices)] = 1.0
    return v


def main() -> None:
    _, w_adj = build_w33()
    lines = build_lines(w_adj)
    flags, A = build_flag_line_graph(lines)
    groups = projector_groups(A)

    mults = [(round(ev, 12), m) for ev, m, _ in groups]
    assert [m for _, m in mults] == [1, 24, 30, 24, 81], mults

    sectors24 = [(ev, P) for ev, m, P in groups if m == 24]
    assert len(sectors24) == 2

    carrier_vec = indicator(O0)
    blocks = [O0[6*i:6*(i+1)] for i in range(4)]
    block_vecs = [indicator(b) for b in blocks]
    singleton_vecs = [indicator([i]) for i in O0]

    print("BT684 E1+E3 numeric projection/intertwiner attempt: COMPLETE")
    print(f"flag_count={len(flags)}")
    print(f"adjacency_eigenspaces={mults}")
    print("carrier=BT648_O0")
    print(f"carrier_size={len(O0)}")
    print("packet_blocks=4 blocks of 6 flags")

    found_full_four_block = False
    for idx, (ev, P) in enumerate(sectors24, start=1):
        carrier_norm = float(carrier_vec @ P @ carrier_vec)
        block_rank, block_svals = rank_projected(P, block_vecs)
        singleton_rank, singleton_svals = rank_projected(P, singleton_vecs)
        print(f"sector24_{idx}_eigenvalue={ev:.12f}")
        print(f"sector24_{idx}_carrier_projection_norm={carrier_norm:.12f}")
        print(f"sector24_{idx}_four_block_projection_rank={block_rank}")
        print(f"sector24_{idx}_singleton_projection_rank={singleton_rank}")
        print(f"sector24_{idx}_block_singular_values={[round(x,8) for x in block_svals]}")
        if block_rank == 4:
            found_full_four_block = True

    print(f"four_block_full_rank_seen={found_full_four_block}")
    print("canonical_intertwiner_found=False")
    print("boundary=nonzero/rank diagnostics only; canonical E1/E3 packet embedding remains open")


if __name__ == "__main__":
    main()
