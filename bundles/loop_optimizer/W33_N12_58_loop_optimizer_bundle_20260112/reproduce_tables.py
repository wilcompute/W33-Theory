#!/usr/bin/env python3
"""Find W33 line-graph cycles whose Z8-scaled determinant-phase delta multiset matches N12_58 2T cycles.

Inputs:
- W33 line incidence: data/_workbench/02_geometry/W33_line_phase_map.csv
- W33 C4 rays:        data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv
- N12 2T cycles:      data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv

Construction:
1) For each W33 line (4 points), build a 4x4 basis matrix B from the four rays (gauge-fixed per ray).
2) Compute det(B) (unit complex), quantize arg(det) to Z12 phase k12 in {0..11}.
3) Reduce to k8 = k12 mod 8.
4) For adjacent lines L,M (share a point), define delta(L,M) = 2*min((k8(M)-k8(L)) mod 8, (k8(L)-k8(M)) mod 8).
   This yields even deltas in {0,2,4,6,8}. We restrict matching to {0,2,4,6} to mirror the N12 delta multisets.

Search:
For each N12 cycle length k and delta multiset, do a backtracking search for a simple k-cycle in the W33 line graph
whose step-delta multiset matches exactly.

Outputs:
- w33_line_det_phase_labels.csv
- w33_line_graph_edge_deltas_z8_scaled.csv
- w33_matching_cycles_for_n12_2t_delta_multisets.csv
"""
import ast
import cmath
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

W33_LINES = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
W33_RAYS  = ROOT / "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
N12_2T    = ROOT / "data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv"

ALL_DELTAS_ALLOWED = {0,2,4,6}

def parse_c(s: str) -> complex:
    return complex(str(s).replace("j","j"))

def gauge_fix(v: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    for comp in v:
        if abs(comp) > tol:
            phase = comp/abs(comp)
            return v/phase
    return v

def det_phase_z12(B: np.ndarray) -> int:
    det = np.linalg.det(B)
    if abs(det) == 0:
        raise ValueError("singular basis matrix")
    detu = det/abs(det)
    ang = cmath.phase(detu) % (2*math.pi)
    return int(round(ang/(2*math.pi)*12)) % 12

def delta_z8_scaled(k8a: int, k8b: int) -> int:
    d = (k8b - k8a) % 8
    d = min(d, (-d) % 8)  # 0..4
    return 2*d  # {0,2,4,6,8}

def main() -> None:
    lines_df = pd.read_csv(W33_LINES)
    lines_df["pts"] = lines_df["point_ids"].astype(str).apply(lambda s: tuple(sorted(int(x) for x in s.split())))
    lines = {int(r.line_id): r.pts for r in lines_df.itertuples(index=False)}

    rays_df = pd.read_csv(W33_RAYS)
    vec_by_point = {}
    for r in rays_df.itertuples(index=False):
        p = int(r.point_id)
        v = np.array([parse_c(r.v0), parse_c(r.v1), parse_c(r.v2), parse_c(r.v3)], dtype=np.complex128)
        vec_by_point[p] = gauge_fix(v)

    # line labels
    k12 = {}
    k8  = {}
    for lid, pts in lines.items():
        B = np.column_stack([vec_by_point[p] for p in pts])
        k12[lid] = det_phase_z12(B)
        k8[lid]  = k12[lid] % 8

    # line adjacency via shared points
    pt_to_lines = defaultdict(list)
    for lid, pts in lines.items():
        for p in pts:
            pt_to_lines[p].append(lid)
    adj = {lid:set() for lid in lines}
    for p, lids in pt_to_lines.items():
        for i in range(len(lids)):
            for j in range(i+1, len(lids)):
                a,b = lids[i], lids[j]
                adj[a].add(b); adj[b].add(a)

    # edge deltas
    edge_delta = {}
    for a in adj:
        for b in adj[a]:
            if a < b:
                edge_delta[(a,b)] = delta_z8_scaled(k8[a], k8[b])

    # load target cycles
    tdf = pd.read_csv(N12_2T)
    targets = []
    for r in tdf.itertuples(index=False):
        deltas = ast.literal_eval(r.delta_multiset)
        targets.append((r.cycle_nodes, int(r.length), deltas))

    # helper: backtracking search
    def find_cycle(k: int, deltas: list[int], tries: int = 20000, budget: int = 10_000_000):
        tgt = Counter(deltas)
        explored = 0
        nodes = list(adj.keys())

        # neighbor list filtered to allowed deltas
        neigh = {}
        for u in nodes:
            lst = []
            for v in adj[u]:
                d = edge_delta[(min(u,v), max(u,v))]
                if d in ALL_DELTAS_ALLOWED:
                    lst.append((v,d))
            neigh[u] = lst

        # rarity heuristic
        rarity = {d:1/(1+sum(1 for v in edge_delta.values() if v==d)) for d in ALL_DELTAS_ALLOWED}
        for u in neigh:
            neigh[u].sort(key=lambda x: rarity[x[1]], reverse=True)

        best = None

        def dfs(start, path, used, rem):
            nonlocal explored, best
            if explored >= budget:
                return False
            m = len(path)
            remaining_edges = k - (m-1)  # includes closing edge
            if sum(rem.values()) != remaining_edges:
                return False
            if m == k:
                u = path[-1]
                for v,d in neigh[u]:
                    if v == start and rem.get(d,0) > 0:
                        rem[d] -= 1
                        if all(rem[x]==0 for x in rem):
                            best = path + [start]
                            rem[d] += 1
                            return True
                        rem[d] += 1
                return False
            u = path[-1]
            for v,d in neigh[u]:
                if v in used: 
                    continue
                if rem.get(d,0) <= 0:
                    continue
                explored += 1
                rem[d] -= 1
                used.add(v); path.append(v)
                if dfs(start, path, used, rem):
                    return True
                path.pop(); used.remove(v)
                rem[d] += 1
                if explored >= budget:
                    break
            return False

        import random
        for _ in range(tries):
            s = random.choice(nodes)
            rem = Counter(tgt)
            if dfs(s, [s], {s}, rem):
                return best
            if explored >= budget:
                break
        return None

    rows = []
    for name,k,deltas in targets:
        cyc = find_cycle(k, deltas)
        rows.append({"n12_cycle_nodes": name, "length": k, "w33_line_cycle": None if cyc is None else "-".join(map(str,cyc[:-1]))})
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "w33_matching_cycles_for_n12_2t_delta_multisets.csv", index=False)
    print(out)

if __name__ == "__main__":
    main()
