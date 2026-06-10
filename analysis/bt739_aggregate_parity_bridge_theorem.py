#!/usr/bin/env python3
"""
BT739 - Parity-aggregate bridge: canonical rank vs orientation-gauge defect.

CONTEXT.  BT714/BT715 closed the BT708 completion target with a single
selected sheet (mask 1110, channel 011/far): rank 81, boundaryless, image =
Levi E4.  BT720 proved D4 x Fano orbit uniqueness for the 12 admissible
Type-A sheets.  BT739 asks the complementary question:

    What does the FULLY SYMMETRIC aggregate see?

Define the canonical parity-signed rectangle -> cycle matrix

    T[rect, cyc] = sum over the 24 valid lifts of rect landing on cyc of
                   sgn(mask),   sgn = +1 (weight-3 D4 mask), -1 (weight-2).

T is Sp(4,3)-equivariant: masks and parities are geometric, no orientation or
coordinate choice enters.  Compose with

    Z_chart : 2160 rect -> 240 charts          (equivariant)
    P81     : chart space -> chart81 sector    (exact polynomial in G=HH^T)
    O       : 1620 cycles -> 160 signed flags  (lex orientation GAUGE)

A floating-point pilot (BT709-local) found rank(P81 Z^T T O) = 78 = 81 - 3,
suggesting a "Fano defect 3 = q".  But PSp(4,3) = U4(2) has NO faithful
3-dimensional irrep and chart81 contains no trivial subrep (the chart action
is transitive), so a 3-dim equivariant kernel inside chart81 is impossible.
The resolution must be one of:

  (i)  rank(P81 Z^T T) = 81 in canonical cycle coordinates, and the drop to
       78 is an artifact of the orientation gauge O;
  (ii) the defect lives in the cycle-relation kernel ker(O), dim 1539.

BT739 computes everything EXACTLY (mod p = 1_000_003, same prime as BT713):

  R1. rank(Z^T T)            canonical chart -> cycle aggregate
  R2. rank(P81 Z^T T)        canonical aggregate restricted to chart81
  R3. rank(Z^T T O)          flag-coordinates aggregate (lex gauge)
  R4. rank(P81 Z^T T O)      flag-coordinates restricted to chart81
  R5. gauge sweep: R4 under random +-1 cycle orientation gauges
  R6. per-channel aggregates (BT713 residual channels 0,1,2) on chart81
  R7. per-parity aggregates (weight-3 only / weight-2 only) on chart81
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
import random

import numpy as np

P = 1_000_003


# ---------------------------------------------------------------------------
# W(3,3) substrate (BT696/BT699/BT713 conventions)
# ---------------------------------------------------------------------------

def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build():
    pts = points()
    adj = [[False] * 40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True

    lines = [tuple(q) for q in combinations(range(40), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40

    through = defaultdict(list)
    edge_line = {}
    for li, line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li

    centers = {}
    for x, y in combinations(range(40), 2):
        if not adj[x][y]:
            cs = tuple(sorted(c for c in range(40) if adj[x][c] and adj[y][c]))
            assert len(cs) == 4
            centers[tuple(sorted((x, y)))] = cs

    nonedges = [tuple(sorted((i, j))) for i, j in combinations(range(40), 2)
                if not adj[i][j]]
    nonedge_idx = {e: i for i, e in enumerate(nonedges)}
    assert len(nonedges) == 540

    flags = sorted((p, li) for li, line in enumerate(lines) for p in line)
    flag_idx = {f: i for i, f in enumerate(flags)}
    assert len(flags) == 160

    return adj, lines, through, edge_line, centers, nonedges, nonedge_idx, flag_idx


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x, c)))]
    lcy = edge_line[tuple(sorted((c, y)))]
    return [(x, lxc), (c, lxc), (c, lcy), (y, lcy)]


def xor_path_edges(paths):
    cnt = Counter()
    for path in paths:
        for e in path:
            cnt[e] ^= 1
    return frozenset(e for e, v in cnt.items() if v)


def is_simple_levi_8_cycle(edge_set) -> bool:
    if len(edge_set) != 8:
        return False
    deg = Counter()
    graph = defaultdict(list)
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        deg[a] += 1
        deg[b] += 1
        graph[a].append(b)
        graph[b].append(a)
    if len(deg) != 8 or any(d != 2 for d in deg.values()):
        return False
    start = next(iter(deg))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == 8


def oriented_row(edge_set, flag_idx):
    """BT713 lex orientation gauge: signed 160-vector for one Levi 8-cycle."""
    graph = defaultdict(list)
    edge_for = {}
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        graph[a].append(b)
        graph[b].append(a)
        edge_for[frozenset((a, b))] = (p, li)
    for u in graph:
        graph[u].sort()
    start = min(graph)
    prev = None
    cur = start
    nxt = graph[start][0]
    row = {}
    for _ in range(8):
        flag = edge_for[frozenset((cur, nxt))]
        sign = 1 if cur[0] == "p" else -1
        row[flag_idx[flag]] = sign
        prev, cur = cur, nxt
        if cur == start:
            break
        nxt = next(x for x in graph[cur] if x != prev)
    assert len(row) == 8
    return row


# ---------------------------------------------------------------------------
# Exact chart81 projector: P81 ~ (G-36)(G-18)(G-12)(G-6)G  (scalar irrelevant)
# ---------------------------------------------------------------------------

def chart_projector_mod_p(charts, nonedge_idx):
    H = np.zeros((240, 540), dtype=np.int64)
    for ci, (p, li, lj, A, B) in enumerate(charts):
        for x in A:
            for y in B:
                H[ci, nonedge_idx[tuple(sorted((x, y)))]] = 1
    assert set(H.sum(axis=1).tolist()) == {9}
    assert set(H.sum(axis=0).tolist()) == {4}
    G = (H @ H.T) % P
    Pm = np.eye(240, dtype=np.int64)
    for lam in (36, 18, 12, 6, 0):
        M = (G - lam * np.eye(240, dtype=np.int64)) % P
        Pm = (Pm @ M) % P
    return Pm, G


def rank_mod_p(M) -> int:
    """Dense Gaussian elimination over GF(P)."""
    A = [list(map(int, row)) for row in (np.asarray(M) % P)]
    nrows = len(A)
    ncols = len(A[0]) if nrows else 0
    rank = 0
    row = 0
    for col in range(ncols):
        piv = None
        for r in range(row, nrows):
            if A[r][col] % P:
                piv = r
                break
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        inv = pow(A[row][col], P - 2, P)
        A[row] = [(x * inv) % P for x in A[row]]
        for r in range(nrows):
            if r != row and A[r][col]:
                f = A[r][col]
                A[r] = [(x - f * y) % P for x, y in zip(A[r], A[row])]
        rank += 1
        row += 1
        if row == nrows:
            break
    return rank


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    adj, lines, through, edge_line, centers, nonedges, nonedge_idx, flag_idx = build()

    masks_w3 = {(1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1)}
    masks_w2 = {(1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1)}
    all_masks = masks_w3 | masks_w2

    charts = []
    for p in range(40):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(set(lines[li]) - {p}))
            B = tuple(sorted(set(lines[lj]) - {p}))
            charts.append((p, li, lj, A, B))
    assert len(charts) == 240

    cycle_id = {}
    # Signed rect -> cycle coefficient lists.
    T_entries = []           # full parity aggregate
    T_w3_entries = []        # weight-3 masks only (+1)
    T_w2_entries = []        # weight-2 masks only (-1 -> store +1; sign scalar)
    T_ch_entries = [[], [], []]  # per BT713 residual channel, parity-signed
    rect_chart = []          # chart index per rectangle

    for ci, (p, li, lj, A, B) in enumerate(charts):
        for aa in combinations(A, 2):
            for bb in combinations(B, 2):
                rect_edges = [tuple(sorted(e)) for e in [
                    (aa[0], bb[0]), (aa[1], bb[0]),
                    (aa[1], bb[1]), (aa[0], bb[1]),
                ]]
                assert all(not adj[x][y] for x, y in rect_edges)
                per_mask = defaultdict(list)
                for gauges in product(*(centers[e] for e in rect_edges)):
                    paths = [path_edges(x, y, g, edge_line)
                             for (x, y), g in zip(rect_edges, gauges)]
                    cycle = xor_path_edges(paths)
                    if is_simple_levi_8_cycle(cycle):
                        mask = tuple(1 if g == p else 0 for g in gauges)
                        assert mask in all_masks
                        per_mask[mask].append(cycle)
                assert set(per_mask) == all_masks
                row = Counter()
                row_w3 = Counter()
                row_w2 = Counter()
                row_ch = [Counter(), Counter(), Counter()]
                for mask, cycles in per_mask.items():
                    assert len(cycles) == 3
                    sgn = 1 if mask in masks_w3 else -1
                    # BT713 channel convention: sort the 3 lifts by cycle tuple.
                    for residual_index, cycle in enumerate(
                            sorted(cycles, key=lambda c: tuple(sorted(c)))):
                        cid = cycle_id.setdefault(cycle, len(cycle_id))
                        row[cid] += sgn
                        row_ch[residual_index][cid] += sgn
                        if sgn == 1:
                            row_w3[cid] += 1
                        else:
                            row_w2[cid] += 1
                T_entries.append(dict(row))
                T_w3_entries.append(dict(row_w3))
                T_w2_entries.append(dict(row_w2))
                for k in range(3):
                    T_ch_entries[k].append(dict(row_ch[k]))
                rect_chart.append(ci)

    n_rect = len(T_entries)
    n_cyc = len(cycle_id)
    assert n_rect == 2160
    assert n_cyc == 1620
    print(f"rectangles={n_rect}, unique Levi 8-cycles={n_cyc}")

    # Oriented cycle matrix O (lex gauge): 1620 x 160.
    O = np.zeros((n_cyc, 160), dtype=np.int64)
    for cycle, cid in cycle_id.items():
        for col, s in oriented_row(cycle, flag_idx).items():
            O[cid, col] = s
    rank_O = rank_mod_p(O)
    print(f"rank(O) = {rank_O}  (Levi cycle space dim, expect 81)")
    assert rank_O == 81

    # Z_chart^T T : 240 x 1620 aggregates (sum rect rows within each chart).
    def chart_aggregate(entries):
        N = np.zeros((240, n_cyc), dtype=np.int64)
        for r, row in enumerate(entries):
            ci = rect_chart[r]
            for cid, v in row.items():
                N[ci, cid] += v
        return N % P

    P81, G = chart_projector_mod_p(charts, nonedge_idx)
    rank_P81 = rank_mod_p(P81)
    print(f"rank(P81 mod p) = {rank_P81}  (expect 81; projector sanity)")
    assert rank_P81 == 81

    results = {}

    N_full = chart_aggregate(T_entries)
    r1 = rank_mod_p(N_full)
    r2 = rank_mod_p((P81 @ N_full) % P)
    NO_full = (N_full @ (O % P)) % P
    r3 = rank_mod_p(NO_full)
    r4 = rank_mod_p((P81 @ NO_full) % P)
    print(f"R1 rank(Z^T T)            = {r1}   (canonical, cycle coords)")
    print(f"R2 rank(P81 Z^T T)        = {r2}   (canonical, chart81 sector)")
    print(f"R3 rank(Z^T T O)          = {r3}   (lex gauge, flag coords)")
    print(f"R4 rank(P81 Z^T T O)      = {r4}   (lex gauge, chart81 sector)")
    results.update(R1=r1, R2=r2, R3=r3, R4=r4)

    # R5: orientation gauge sweep.
    rng = random.Random(20260610)
    gauge_ranks = []
    for trial in range(5):
        w = np.array([1 if rng.random() < 0.5 else P - 1 for _ in range(n_cyc)],
                     dtype=np.int64)
        NO_g = ((N_full * w[None, :]) % P @ (O % P)) % P
        gauge_ranks.append(rank_mod_p((P81 @ NO_g) % P))
    print(f"R5 gauge sweep ranks      = {gauge_ranks}")
    results["R5_gauge_sweep"] = gauge_ranks

    # R6: per-channel parity aggregates on chart81 (flag coords, lex gauge).
    ch_ranks = []
    for k in range(3):
        N_ch = chart_aggregate(T_ch_entries[k])
        NO_ch = (N_ch @ (O % P)) % P
        ch_ranks.append(rank_mod_p((P81 @ NO_ch) % P))
    print(f"R6 per-channel chart81    = {ch_ranks}")
    results["R6_per_channel"] = ch_ranks

    # R7: per-parity aggregates on chart81.
    par_ranks = {}
    N_par_mats = {}
    for name, entries in (("w3", T_w3_entries), ("w2", T_w2_entries)):
        N_par = chart_aggregate(entries)
        N_par_mats[name] = N_par
        NO_par = (N_par @ (O % P)) % P
        par_ranks[name] = rank_mod_p((P81 @ NO_par) % P)
    print(f"R7 per-parity chart81     = {par_ranks}")
    results["R7_per_parity"] = par_ranks

    # R8: UNSIGNED aggregate (w3 + w2, all lifts weight +1): is parity needed?
    N_unsigned = (N_par_mats["w3"] + N_par_mats["w2"]) % P
    r8_cycle = rank_mod_p((P81 @ N_unsigned) % P)
    NO_uns = (N_unsigned @ (O % P)) % P
    r8_flag = rank_mod_p((P81 @ NO_uns) % P)
    print(f"R8 unsigned chart81       = cycle:{r8_cycle} flag:{r8_flag}")
    results["R8_unsigned_cycle"] = r8_cycle
    results["R8_unsigned_flag"] = r8_flag

    print()
    print("=" * 70)
    print("BT739 VERDICT")
    print("=" * 70)
    if r2 == 81 and r4 < 81:
        print("Canonical aggregate is FULL RANK 81 on chart81 in cycle")
        print("coordinates; the float-pilot defect 78 was an artifact of the")
        print("lex orientation gauge O.  Representation theory enforced this:")
        print("PSp(4,3)=U4(2) has no 3-dim irrep and chart81 has no trivial")
        print("subrep, so no equivariant 3-dim kernel can exist.")
        verdict = "gauge_artifact"
    elif r2 < 81:
        print(f"Canonical aggregate has rank {r2} < 81 on chart81: a genuine")
        print("equivariant defect.  Kernel dim = " + str(81 - r2) + ".")
        verdict = "genuine_defect"
    else:
        print("Both canonical and gauge-composed aggregates are full rank 81.")
        verdict = "full_rank_everywhere"
    results["verdict"] = verdict

    out = {
        "theorem": "BT739 Parity-Aggregate Bridge: canonical rank vs gauge defect",
        "prime": P,
        "rectangles": n_rect,
        "unique_levi_8_cycles": n_cyc,
        "levi_beta1": 81,
        "chart81_dim": 81,
        **{k: (int(v) if isinstance(v, (int, np.integer)) else v)
           for k, v in results.items()},
        "float_pilot_rank": 78,
        "rep_theory_constraint": (
            "PSp(4,3)=U4(2) minimal nontrivial irrep dim is 5; chart action "
            "transitive => no trivial subrep in chart81 => no equivariant "
            "3-dim kernel possible"
        ),
    }
    with open("data/bt739_aggregate_parity_bridge.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt739_aggregate_parity_bridge.json")


if __name__ == "__main__":
    main()
