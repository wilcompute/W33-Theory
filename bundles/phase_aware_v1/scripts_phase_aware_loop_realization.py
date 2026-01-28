#!/usr/bin/env python3
"""Phase-aware 2T-loop realization in the W33 four-center triad graph.

Phase constraint used (derived from Z12 triad holonomy):
  - if delta == 2, require triad_holonomy_z12 == 9
  - if delta == 6, require triad_holonomy_z12 == 3
  - delta in {0,4} unconstrained (reserved)

Objective:
  - minimize number of cover-12 triads used along the closed walk (per cycle)

Inputs:
  - w33 geometry CSV
  - rays CSV
  - n12 2T cycles CSV
  - n12 flip delta edge audit CSV (provides per-step delta + support)
  - w33_to_n12_mapping.csv (provides per-point n12_mask)

Outputs:
  - phase_aware_2T_cycle_witness_walks.csv
  - phase_aware_run_summary.json
"""

import argparse
import itertools
import json
from collections import Counter

import numpy as np
import pandas as pd

ALL12 = (1 << 12) - 1
OMEGA = np.exp(2j * np.pi / 12)


def parse_c(s: str) -> complex:
    return complex(str(s).replace("i", "j"))


def quantize_phase(z: complex) -> int:
    ang = np.angle(z)
    if ang < 0:
        ang += 2 * np.pi
    return int(np.round(ang / (2 * np.pi / 12))) % 12


def popcount(x: int) -> int:
    return bin(x).count("1")


def parse_cycle_nodes(s: str):
    return [int(x) for x in str(s).split("-")]


def parse_support_masks(s: str):
    masks = []
    for part in str(s).split("|"):
        m = 0
        for tok in part.strip().split():
            m |= 1 << int(tok)
        masks.append(m)
    return masks


def mask_to_symbols(mask: int) -> str:
    syms = []
    for i in range(12):
        if (mask >> i) & 1:
            syms.append("a" if i == 10 else "b" if i == 11 else str(i))
    return " ".join(syms)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w33_csv", required=True)
    ap.add_argument("--rays_csv", required=True)
    ap.add_argument("--n12_cycles_csv", required=True)
    ap.add_argument("--n12_audit_edges_csv", required=True)
    ap.add_argument("--w33_to_n12_mapping_csv", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    w33 = pd.read_csv(args.w33_csv)
    rays = pd.read_csv(args.rays_csv)
    cycles = pd.read_csv(args.n12_cycles_csv)
    audit = pd.read_csv(args.n12_audit_edges_csv)
    mapping = pd.read_csv(args.w33_to_n12_mapping_csv)

    # point masks
    w33_mask = {
        int(r.w33_point): int(r.n12_mask) for r in mapping.itertuples(index=False)
    }

    # vectors
    vecs = {}
    for r in rays.itertuples(index=False):
        pid = int(r.point_id)
        v = np.array(
            [parse_c(r.v0), parse_c(r.v1), parse_c(r.v2), parse_c(r.v3)],
            dtype=np.complex128,
        )
        vecs[pid] = v

    # lines
    lines = {}
    for r in w33.itertuples(index=False):
        lid = int(r.line_id)
        pts = tuple(int(x) for x in str(r.point_ids).split())
        lines[lid] = pts

    # collinearity
    col = {p: set() for p in range(40)}
    for pts in lines.values():
        for a, b in itertools.combinations(pts, 2):
            col[a].add(b)
            col[b].add(a)

    # four-center triads list
    def centers(a, b, c):
        return col[a] & col[b] & col[c]

    four_center = []
    for a in range(40):
        for b in range(a + 1, 40):
            if b in col[a]:
                continue
            for c in range(b + 1, 40):
                if c in col[a] or c in col[b]:
                    continue
                ctr = centers(a, b, c)
                if len(ctr) == 4:
                    four_center.append((a, b, c))
    # edge phases for noncollinear oriented pairs
    noncol = {p: set(range(40)) - {p} - col[p] for p in range(40)}
    k_edge = {}
    for p in range(40):
        vp = vecs[p]
        for q in noncol[p]:
            ip = np.vdot(vp, vecs[q])
            k_edge[(p, q)] = quantize_phase(ip)

    # triad holonomy and triad masks
    triad_pts = [tuple(t) for t in four_center]
    triad_h = []
    triad_mask = []
    for a, b, c in triad_pts:
        triad_h.append((k_edge[(a, b)] + k_edge[(b, c)] + k_edge[(c, a)]) % 12)
        triad_mask.append(w33_mask[a] | w33_mask[b] | w33_mask[c])

    # build adjacency (share 2 points)
    pair_to = []
    for idx, (a, b, c) in enumerate(triad_pts):
        for u, v in ((a, b), (a, c), (b, c)):
            key = tuple(sorted((u, v)))
            pair_to.setdefault(key, []).append(idx)
    adj = [set() for _ in range(len(triad_pts))]
    for key, lst in pair_to.items():
        if len(lst) > 1:
            for i in lst:
                for j in lst:
                    if i != j:
                        adj[i].add(j)

    # audit edge dict (delta, support)
    edge_delta = {}
    edge_support = {}
    for r in audit.itertuples(index=False):
        u = int(r.u)
        v = int(r.v)
        d = int(r.delta_from_nodes)
        sm = 0
        for tok in str(r.flip_support_4set).split():
            sm |= 1 << int(tok)
        key = (min(u, v), max(u, v))
        edge_delta[key] = d
        edge_support[key] = sm

    # per cycle: build deltas/supports, then solve minimal cover12 closed walk
    def solve_cycle(supp_masks, deltas):
        L = len(supp_masks)
        # allowed triads per step
        allowed = []
        for S, d in zip(supp_masks, deltas):
            req = []
            for t in range(len(triad_pts)):
                if (triad_mask[t] & S) != S:
                    continue
                if d == 2 and triad_h[t] != 9:
                    continue
                if d == 6 and triad_h[t] != 3:
                    continue
                req.append(t)
            if not req:
                return None
            allowed.append(req)
        cost = [1 if triad_mask[t] == ALL12 else 0 for t in range(len(triad_pts))]
        INF = 10**9
        best = None
        best_path = None
        for start in allowed[0]:
            dp = [{start: cost[start]}]
            prev = [{start: None}]
            for s in range(1, L):
                cur = {}
                cur_prev = {}
                for j in allowed[s]:
                    bestp = None
                    bestv = INF
                    for i in adj[j]:
                        if i in dp[s - 1]:
                            v = dp[s - 1][i] + cost[j]
                            if v < bestv:
                                bestv = v
                                bestp = i
                    if bestp is not None:
                        cur[j] = bestv
                        cur_prev[j] = bestp
                if not cur:
                    break
                dp.append(cur)
                prev.append(cur_prev)
            if len(dp) < L:
                continue
            last = [j for j in dp[L - 1] if start in adj[j]]
            if not last:
                continue
            jmin = min(last, key=lambda j: dp[L - 1][j])
            v = dp[L - 1][jmin]
            if best is None or v < best:
                best = v
                path = [None] * L
                path[L - 1] = jmin
                for s in range(L - 1, 0, -1):
                    path[s - 1] = prev[s][path[s]]
                best_path = path
        if best is None:
            return None
        return best, best_path

    out_rows = []
    per_cycle = {}
    total = 0
    for idx, row in cycles.iterrows():
        nodes = parse_cycle_nodes(row.cycle_nodes)
        supp = parse_support_masks(row.supports)
        L = int(row.length)
        deltas = []
        for j in range(L):
            key = (min(nodes[j], nodes[(j + 1) % L]), max(nodes[j], nodes[(j + 1) % L]))
            deltas.append(edge_delta[key])
            # assert support matches
            assert edge_support[key] == supp[j]
        res = solve_cycle(supp, deltas)
        assert res is not None, f"cycle {idx} infeasible"
        cost, path = res
        per_cycle[int(idx)] = int(cost)
        total += int(cost)
        for s in range(L):
            t = path[s]
            out_rows.append(
                dict(
                    cycle_index=int(idx),
                    cycle_length=L,
                    step=s,
                    support_mask=int(supp[s]),
                    support_symbols=mask_to_symbols(int(supp[s])),
                    delta=int(deltas[s]),
                    required_triadhol=(
                        9 if deltas[s] == 2 else 3 if deltas[s] == 6 else None
                    ),
                    triad_index=int(t),
                    w33_points=" ".join(map(str, triad_pts[t])),
                    triad_holonomy_z12=int(triad_h[t]),
                    triad_cover12=bool(triad_mask[t] == ALL12),
                    triad_cover_size=int(popcount(triad_mask[t])),
                    triad_missing_symbols=(
                        mask_to_symbols(ALL12 ^ int(triad_mask[t]))
                        if triad_mask[t] != ALL12
                        else ""
                    ),
                )
            )
    df = pd.DataFrame(out_rows)
    df.to_csv(f"{args.outdir}/phase_aware_2T_cycle_witness_walks.csv", index=False)
    summary = dict(
        phase_constraints={
            "delta==2": "triad_holonomy_z12==9",
            "delta==6": "triad_holonomy_z12==3",
            "delta in {0,4}": "unconstrained",
        },
        per_cycle_min_cover12_steps=per_cycle,
        total_min_cover12_steps=int(total),
    )
    from utils.json_safe import dump_json

    dump_json(summary, f"{args.outdir}/phase_aware_run_summary.json", indent=2)
    print("total min cover12 steps:", total, "per cycle:", per_cycle)


if __name__ == "__main__":
    main()
