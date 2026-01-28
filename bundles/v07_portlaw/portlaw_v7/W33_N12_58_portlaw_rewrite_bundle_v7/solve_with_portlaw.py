#!/usr/bin/env python3
"""
Solve the five nontrivial N12_58 2T cycles using a port-law keyed by (delta, rem_idx, add_idx).

This script demonstrates the "rewrite":
- The original v3 solver used holonomy-based delta=0/4 transition rules (plus subtypes).
- Here we instead constrain transitions by the canonical K4 port label (matching index 0/1/2)
  and a port-law that depends ONLY on (delta, rem_idx, add_idx), where rem/add indices are computed
  directly from removed_pairs / added_pairs in the audit file.

Inputs:
- W33 incidence: data/_workbench/02_geometry/W33_line_phase_map.csv
- W33 rays:      data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv
- N12 points:    data/_n12/n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_*.csv
- flip audit:    data/_n12/n12_58_flip_delta_audit_all_edges.csv
- 2T cycles:     data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv
- A mapping:     CSV with columns (w33_point,n12_point)

Outputs:
- cycle_witness_portlaw_solver.csv
- port_law_reduced_key.json

Usage:
  python solve_with_portlaw.py --root /path/to/proj_data/data --mapping /path/to/best_w33_to_n12_mapping.csv --out ./out
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

SYM = {**{str(i): i for i in range(10)}, "a": 10, "b": 11}
INF = 10**9


def parse_complex(s: str) -> complex:
    return complex(str(s).replace(" ", ""))


def quant_k(z: complex) -> int:
    twopi = 2 * math.pi
    ang = math.atan2(z.imag, z.real)
    return int(round((12 * ang / twopi))) % 12


def parse_members(s: str):
    return [t.strip() for t in str(s).split(",") if t.strip()]


def tri_to_syms(tri: str):
    tri = tri.strip()
    return [SYM[ch] for ch in tri]


def syms_to_mask(syms):
    m = 0
    for s in syms:
        m |= 1 << s
    return m


def parse_support(s: str):
    return [int(x) for x in str(s).split()]


def pairs_from_field(field):
    if isinstance(field, (list, tuple)):
        pairs = list(field)
    else:
        s = str(field).strip()
        try:
            pairs = ast.literal_eval(s)
        except Exception:
            pairs = []
    pairs = [tuple(sorted((int(a), int(b)))) for a, b in pairs]
    return set(pairs)


def matching_index_from_pairs(support_list, pairs_field):
    pairs = pairs_from_field(pairs_field)
    s = sorted(support_list)
    s0, s1, s2, s3 = s
    match0 = {tuple(sorted((s0, s1))), tuple(sorted((s2, s3)))}
    match1 = {tuple(sorted((s0, s2))), tuple(sorted((s1, s3)))}
    match2 = {tuple(sorted((s0, s3))), tuple(sorted((s1, s2)))}
    if pairs == match0:
        return 0
    if pairs == match1:
        return 1
    if pairs == match2:
        return 2
    raise ValueError("Pairs do not match any canonical matching")


def matchings_for_P(P):
    p0, p1, p2, p3 = P
    return [((p0, p1), (p2, p3)), ((p0, p2), (p1, p3)), ((p0, p3), (p1, p2))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, required=True, help="Path to proj_data/data")
    ap.add_argument(
        "--mapping", type=str, required=True, help="CSV: w33_point,n12_point"
    )
    ap.add_argument("--out", type=str, required=True, help="Output directory")
    args = ap.parse_args()

    ROOT = Path(args.root)
    OUT = Path(args.out)
    OUT.mkdir(parents=True, exist_ok=True)

    # mapping
    df_map = pd.read_csv(args.mapping)
    w33_to_n12 = dict(
        zip(df_map["w33_point"].astype(int), df_map["n12_point"].astype(str))
    )

    # W33 incidence
    w33_csv = ROOT / "_workbench/02_geometry/W33_line_phase_map.csv"
    df = pd.read_csv(w33_csv)
    lines = [tuple(map(int, s.split())) for s in df["point_ids"].astype(str)]
    points = sorted({p for L in lines for p in L})
    col = {p: set() for p in points}
    for L in lines:
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = L[i], L[j]
                col[a].add(b)
                col[b].add(a)

    # four-center triads + center quads
    four_triads = []
    centers = []
    for a, b, c in itertools.combinations(points, 3):
        if (b in col[a]) or (c in col[a]) or (c in col[b]):
            continue
        cs = col[a] & col[b] & col[c]
        if len(cs) == 4:
            t = tuple(sorted((a, b, c)))
            four_triads.append(t)
            centers.append(tuple(sorted(cs)))
    tri_index = {t: i for i, t in enumerate(four_triads)}
    tri_cs = centers

    # adjacency (K4 components)
    pair_to_triads = defaultdict(list)
    for i, t in enumerate(four_triads):
        a, b, c = t
        for u, v in [(a, b), (a, c), (b, c)]:
            pair_to_triads[(min(u, v), max(u, v))].append(i)
    adj = [set() for _ in range(360)]
    for lst in pair_to_triads.values():
        if len(lst) > 1:
            for i in lst:
                adj[i].update(j for j in lst if j != i)
    adj_self = [list(adj[i]) + [i] for i in range(360)]
    assert all(len(adj[i]) == 3 for i in range(360))

    # outer quad and excluded point per triad index
    comp_to_triads = defaultdict(list)
    for t, cs in zip(four_triads, centers):
        comp_to_triads[cs].append(t)
    cs_to_P = {}
    cs_pair_to_match = {}
    cs_excl_by_triad = {}
    for cs, triads in comp_to_triads.items():
        P = sorted(set().union(*map(set, triads)))
        cs_to_P[cs] = tuple(P)
        ms = matchings_for_P(P)
        pair_to_idx = {}
        for midx, m in enumerate(ms):
            for pair in m:
                pair_to_idx[frozenset(pair)] = midx
        cs_pair_to_match[cs] = pair_to_idx
        for t in triads:
            exc = next(iter(set(P) - set(t)))
            cs_excl_by_triad[(cs, tri_index[t])] = exc

    def move_edge_idx(tp, tc):
        if tp == tc:
            return None
        cs = tri_cs[tp]
        if cs != tri_cs[tc]:
            return None
        x = cs_excl_by_triad[(cs, tp)]
        y = cs_excl_by_triad[(cs, tc)]
        return cs_pair_to_match[cs][frozenset((x, y))]

    # rays + holonomy (node constraint)
    ray_csv = (
        ROOT
        / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
    )
    df_r = pd.read_csv(ray_csv)
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, r in df_r.iterrows():
        pid = int(r["point_id"])
        V[pid] = [parse_complex(r[f"v{i}"]) for i in range(4)]
    edge_k = {}
    for p in points:
        for q in points:
            if p == q:
                continue
            if q in col[p]:
                continue
            edge_k[(p, q)] = quant_k(np.vdot(V[p], V[q]))
    tri_h = np.zeros(360, dtype=np.int8)
    for i, t in enumerate(four_triads):
        a, b, c = t
        tri_h[i] = (edge_k[(a, b)] + edge_k[(b, c)] + edge_k[(c, a)]) % 12
    assert set(tri_h.tolist()) == {3, 9}

    # candidate point masks
    cand_points = next(
        (ROOT / "_n12").glob(
            "n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_*.csv"
        )
    )
    df_cp = pd.read_csv(cand_points)
    point_mask = {}
    for _, r in df_cp.iterrows():
        pid = r["point_id"]
        sy = set()
        for tri in parse_members(r["members"]):
            sy.update(tri_to_syms(tri))
        point_mask[pid] = syms_to_mask(sorted(sy))

    # triad cover masks + cover12
    tri_mask = np.zeros(360, dtype=np.int32)
    for i, (a, b, c) in enumerate(four_triads):
        tri_mask[i] = (
            point_mask[w33_to_n12[a]]
            | point_mask[w33_to_n12[b]]
            | point_mask[w33_to_n12[c]]
        )
    cover12 = (tri_mask == 0xFFF).astype(np.int8)

    # flip audit with indices
    audit_csv = ROOT / "_n12/n12_58_flip_delta_audit_all_edges.csv"
    df_a = pd.read_csv(audit_csv)
    df_a["support_list"] = df_a["flip_support_4set"].apply(parse_support)
    df_a["rem_idx"] = df_a.apply(
        lambda r: matching_index_from_pairs(r["support_list"], r["removed_pairs"]),
        axis=1,
    )
    df_a["add_idx"] = df_a.apply(
        lambda r: matching_index_from_pairs(r["support_list"], r["added_pairs"]), axis=1
    )
    edge_dict = {}
    for _, r in df_a.iterrows():
        u = int(r["u"])
        v = int(r["v"])
        key = (min(u, v), max(u, v))
        edge_dict[key] = dict(
            delta=int(r["delta_from_nodes"]),
            support=tuple(map(int, str(r["flip_support_4set"]).split())),
            rem_idx=int(r["rem_idx"]),
            add_idx=int(r["add_idx"]),
        )

    # cycles
    cycles_csv = ROOT / "_n12/n12_58_2t_holonomy_nontrivial_cycles.csv"
    df_c = pd.read_csv(cycles_csv)
    cycle_defs = []
    for _, r in df_c.iterrows():
        nodes = [int(x) for x in str(r["cycle_nodes"]).split("-")]
        L = int(r["length"])
        edges = []
        for i in range(L):
            u, v = nodes[i], nodes[(i + 1) % L]
            edges.append({**edge_dict[(min(u, v), max(u, v))], "u": u, "v": v})
        cycle_defs.append(dict(L=L, edges=edges))

    # First solve with v3 holonomy transition rules to derive port-law (reduced key)
    def solve_v3_and_get_paths():
        results = []
        for cyc in cycle_defs:
            L = cyc["L"]
            edges = cyc["edges"]
            supp_masks = []
            deltas = []
            for e in edges:
                m = 0
                for s in e["support"]:
                    m |= 1 << s
                supp_masks.append(m)
                deltas.append(e["delta"])
            eligible = []
            for i in range(L):
                ok = (tri_mask & supp_masks[i]) == supp_masks[i]
                if deltas[i] == 2:
                    ok &= tri_h == 9
                elif deltas[i] == 6:
                    ok &= tri_h == 3
                eligible.append(ok)
            best_cost = INF
            best_path = None
            for t0 in np.where(eligible[0])[0]:
                cost = np.full(360, INF, dtype=np.int32)
                prev = [np.full(360, -1, dtype=np.int16) for _ in range(L)]
                cost[t0] = int(cover12[t0])
                for i in range(1, L):
                    next_cost = np.full(360, INF, dtype=np.int32)
                    dprev = deltas[i - 1]
                    active = np.where(cost < INF)[0]
                    for tp in active:
                        holp = int(tri_h[tp])
                        for tc in adj_self[tp]:
                            if not eligible[i][tc]:
                                continue
                            holc = int(tri_h[tc])
                            if dprev == 0 and holc != holp:
                                continue
                            if dprev == 4 and holc == holp:
                                continue
                            nc = int(cost[tp]) + int(cover12[tc])
                            if nc < next_cost[tc]:
                                next_cost[tc] = nc
                                prev[i][tc] = tp
                    cost = next_cost
                active = np.where(cost < INF)[0]
                for tL in active:
                    if t0 not in adj_self[tL]:
                        continue
                    dprev = deltas[L - 1]
                    holL = int(tri_h[tL])
                    hol0 = int(tri_h[t0])
                    if dprev == 0 and hol0 != holL:
                        continue
                    if dprev == 4 and hol0 == holL:
                        continue
                    ctot = int(cost[tL])
                    if ctot < best_cost:
                        path = [None] * L
                        path[L - 1] = int(tL)
                        ok = True
                        for k in range(L - 1, 0, -1):
                            path[k - 1] = int(prev[k][path[k]])
                            if path[k - 1] < 0:
                                ok = False
                                break
                        if ok and path[0] == t0:
                            best_cost = ctot
                            best_path = path
            if best_path is None:
                raise RuntimeError("No v3 path found")
            results.append(dict(cost=best_cost, path=best_path))
        return results

    v3_paths = solve_v3_and_get_paths()

    # Derive reduced port-law: key=(delta, rem_idx, add_idx) -> {allowed edge labels, allow stay}
    law = defaultdict(lambda: {"move_idxs": set(), "allow_stay": False})
    for cyc, solved in zip(cycle_defs, v3_paths):
        L = cyc["L"]
        edges = cyc["edges"]
        path = solved["path"]
        for i in range(L):
            e = edges[i]
            tp = path[i]
            tc = path[(i + 1) % L]
            key = (e["delta"], e["rem_idx"], e["add_idx"])
            d = law[key]
            if tp == tc:
                d["allow_stay"] = True
            else:
                midx = move_edge_idx(tp, tc)
                d["move_idxs"].add(int(midx))

    law_out = {
        str(k): {
            "delta": k[0],
            "rem_idx": k[1],
            "add_idx": k[2],
            "move_edge_idxs": sorted(list(v["move_idxs"])),
            "allow_stay": v["allow_stay"],
        }
        for k, v in law.items()
    }
    from utils.json_safe import dump_json

    dump_json(law_out, OUT / "port_law_reduced_key.json", indent=2)

    # Solve again using ONLY the port-law
    def solve_with_portlaw():
        results = []
        for cyc in cycle_defs:
            L = cyc["L"]
            edges = cyc["edges"]
            supp_masks = []
            deltas = []
            for e in edges:
                m = 0
                for s in e["support"]:
                    m |= 1 << s
                supp_masks.append(m)
                deltas.append(e["delta"])
            eligible = []
            for i in range(L):
                ok = (tri_mask & supp_masks[i]) == supp_masks[i]
                if deltas[i] == 2:
                    ok &= tri_h == 9
                elif deltas[i] == 6:
                    ok &= tri_h == 3
                eligible.append(ok)
            best_cost = INF
            best_path = None
            for t0 in np.where(eligible[0])[0]:
                cost = np.full(360, INF, dtype=np.int32)
                prev = [np.full(360, -1, dtype=np.int16) for _ in range(L)]
                cost[t0] = int(cover12[t0])
                for i in range(1, L):
                    next_cost = np.full(360, INF, dtype=np.int32)
                    eprev = edges[i - 1]
                    key = (eprev["delta"], eprev["rem_idx"], eprev["add_idx"])
                    rule = law_out.get(str(key), None)
                    allow_stay = True if rule is None else rule["allow_stay"]
                    allowed = (
                        set([0, 1, 2]) if rule is None else set(rule["move_edge_idxs"])
                    )
                    active = np.where(cost < INF)[0]
                    for tp in active:
                        for tc in adj_self[tp]:
                            if not eligible[i][tc]:
                                continue
                            if tp == tc:
                                if not allow_stay:
                                    continue
                            else:
                                midx = move_edge_idx(tp, tc)
                                if rule is not None and int(midx) not in allowed:
                                    continue
                            nc = int(cost[tp]) + int(cover12[tc])
                            if nc < next_cost[tc]:
                                next_cost[tc] = nc
                                prev[i][tc] = tp
                    cost = next_cost
                active = np.where(cost < INF)[0]
                e_last = edges[L - 1]
                key = (e_last["delta"], e_last["rem_idx"], e_last["add_idx"])
                rule = law_out.get(str(key), None)
                allow_stay = True if rule is None else rule["allow_stay"]
                allowed = (
                    set([0, 1, 2]) if rule is None else set(rule["move_edge_idxs"])
                )
                for tL in active:
                    if t0 not in adj_self[tL]:
                        continue
                    if tL == t0:
                        if not allow_stay:
                            continue
                    else:
                        midx = move_edge_idx(tL, t0)
                        if rule is not None and int(midx) not in allowed:
                            continue
                    ctot = int(cost[tL])
                    if ctot < best_cost:
                        path = [None] * L
                        path[L - 1] = int(tL)
                        ok = True
                        for k in range(L - 1, 0, -1):
                            path[k - 1] = int(prev[k][path[k]])
                            if path[k - 1] < 0:
                                ok = False
                                break
                        if ok and path[0] == t0:
                            best_cost = ctot
                            best_path = path
            if best_path is None:
                raise RuntimeError("No portlaw path found")
            results.append(dict(cost=best_cost, path=best_path))
        return results

    port_paths = solve_with_portlaw()

    # Export witness table
    rows = []
    for cyc_idx, (cyc, solved) in enumerate(zip(cycle_defs, port_paths)):
        L = cyc["L"]
        edges = cyc["edges"]
        path = solved["path"]
        for i in range(L):
            e = edges[i]
            idx = path[i]
            a, b, c = four_triads[idx]
            cs = tri_cs[idx]
            P = cs_to_P[cs]
            exc = cs_excl_by_triad[(cs, idx)]
            idx2 = path[(i + 1) % L]
            moved = int(idx2 != idx)
            midx = move_edge_idx(idx, idx2)
            rows.append(
                dict(
                    cycle_index=cyc_idx,
                    step=i,
                    u=e["u"],
                    v=e["v"],
                    delta=e["delta"],
                    rem_idx=e["rem_idx"],
                    add_idx=e["add_idx"],
                    support=" ".join(map(str, e["support"])),
                    triad_index=idx,
                    triad=f"{a} {b} {c}",
                    center_quad=" ".join(map(str, cs)),
                    outer_quad=" ".join(map(str, P)),
                    excluded_point=exc,
                    triad_hol_mod12=int(tri_h[idx]),
                    cover12=int(cover12[idx]),
                    moved_to_next=moved,
                    move_edge_matching_idx=(int(midx) if midx is not None else -1),
                )
            )
    pd.DataFrame(rows).to_csv(OUT / "cycle_witness_portlaw_solver.csv", index=False)

    # Summary
    summary = {
        "per_cycle_costs": [p["cost"] for p in port_paths],
        "total_cost": int(sum(p["cost"] for p in port_paths)),
        "cover12_count_360": int(cover12.sum()),
    }
    from utils.json_safe import dump_json

    dump_json(summary, OUT / "run_summary.json", indent=2)

    print("Wrote outputs to:", OUT)


if __name__ == "__main__":
    main()
