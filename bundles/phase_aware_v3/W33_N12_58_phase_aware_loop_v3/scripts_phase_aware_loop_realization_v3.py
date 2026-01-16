#!/usr/bin/env python3
"""Phase-aware loop realization v3 for N12_58 2T cycles inside W33 four-center triad graph.

v3 predicate (refines delta=0 and delta=4 using removed/added phase sums mod 8):

Node constraints (per step i, using the edge (u_i -> u_{i+1}) ):
- delta=2 -> triad holonomy must be 9 (mod 12)
- delta=6 -> triad holonomy must be 3 (mod 12)

Transition constraints (between triad at step i and triad at step i+1, using the *previous* edge's attributes):
- delta_prev = 0:
    - hol(prev) == hol(curr)
    - if removed_sum=add_sum=0: require hol(curr)=9
    - if removed_sum=add_sum=4: require hol(curr)=3
    - if removed_sum=add_sum=6: no extra constraint
- delta_prev = 4:
    - hol(prev) != hol(curr)
    - if (removed_sum,added_sum)=(6,2): require direction 3->9
    - if (removed_sum,added_sum)=(0,4): no direction constraint

The witness search is restricted to a single outer-quad component (K4) per cycle.

Outputs:
- phase_aware_v3_cycle_summary.csv
- phase_aware_v3_2T_cycle_witness_walks.csv
- phase_aware_v3_run_summary.json
"""

from __future__ import annotations

import itertools, math, json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path("work2/data")  # adjust if you place the repo elsewhere
W33_LINES = ROOT / "_workbench/02_geometry/W33_line_phase_map.csv"
RAY_FILE  = ROOT / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
EDGE_AUDIT = ROOT / "_n12/n12_58_flip_delta_audit_all_edges.csv"
CYCLES = ROOT / "_n12/n12_58_2t_holonomy_nontrivial_cycles.csv"

MAPPING_CSV = Path("w33_to_n12_mapping.csv")

FULL = (1<<12)-1
TWO_PI = 2*math.pi
STEP = TWO_PI/12

def quant12(angle: float) -> int:
    a = angle % TWO_PI
    return int(round(a/STEP)) % 12

def support_to_mask(supp):
    m=0
    for x in supp:
        m |= 1<<int(x)
    return m

def popcount(x: int) -> int:
    return int(bin(int(x)&0xFFFFFFFF).count("1"))

def main():
    # --- W33 lines / collinearity
    lines_df = pd.read_csv(W33_LINES)
    lines = [tuple(sorted(int(x) for x in str(s).split())) for s in lines_df["point_ids"]]
    col = {p:set() for p in range(40)}
    for L in lines:
        for a,b in itertools.combinations(L,2):
            col[a].add(b); col[b].add(a)

    # --- rays
    rays_df = pd.read_csv(RAY_FILE)
    vec = np.zeros((40,4), dtype=np.complex128)
    for r in rays_df.itertuples(index=False):
        pid=int(r.point_id)
        vec[pid,0]=complex(str(r.v0))
        vec[pid,1]=complex(str(r.v1))
        vec[pid,2]=complex(str(r.v2))
        vec[pid,3]=complex(str(r.v3))

    # oriented k_mod12 on noncollinear pairs
    k12 = np.full((40,40), -1, dtype=np.int8)
    for p in range(40):
        for q in range(40):
            if p==q or (q in col[p]): 
                continue
            ip = np.vdot(vec[p], vec[q])
            if abs(ip) < 1e-8:
                continue
            k12[p,q] = quant12(np.angle(ip))

    # mapping masks
    mp = pd.read_csv(MAPPING_CSV)
    mask_arr = np.zeros(40, dtype=np.int32)
    for r in mp.itertuples(index=False):
        mask_arr[int(r.w33_point)] = int(r.n12_mask)

    # --- four-center triads and info
    tri_info={}
    outer_to_tri={}
    for a,b,c in itertools.combinations(range(40),3):
        if (b in col[a]) or (c in col[a]) or (c in col[b]):
            continue
        centers = col[a].intersection(col[b]).intersection(col[c])
        if len(centers)!=4:
            continue
        outer = tuple(sorted(centers))
        hol = (int(k12[a,b])+int(k12[b,c])+int(k12[c,a])) % 12
        cover_mask = int(mask_arr[a] | mask_arr[b] | mask_arr[c])
        cover_size = popcount(cover_mask)
        tri = (a,b,c)
        tri_info[tri]={
            "outer": outer,
            "hol": hol,
            "cover_mask": cover_mask,
            "cover_size": cover_size,
            "cover12": (cover_mask==FULL),
        }
        outer_to_tri.setdefault(outer, []).append(tri)
    assert len(tri_info)==360

    # --- audit edges
    audit = pd.read_csv(EDGE_AUDIT)
    aud={}
    for r in audit.itertuples(index=False):
        key=tuple(sorted((int(r.u),int(r.v))))
        supp=tuple(int(x) for x in str(r.flip_support_4set).split())
        aud[key]={
            "support": supp,
            "support_mask": support_to_mask(supp),
            "delta": int(r.delta_from_pair_phase_diff_mod8),
            "rem_sum": int(r.removed_phase_sum_mod8),
            "add_sum": int(r.added_phase_sum_mod8),
        }

    cycles = pd.read_csv(CYCLES)

    def cycle_steps(row):
        nodes=[int(x) for x in row.cycle_nodes.split('-')]
        supp_list=[[int(x) for x in part.split()] for part in row.supports.split('|')]
        n=len(nodes)
        steps=[]
        for i in range(n):
            u=nodes[i]; v=nodes[(i+1)%n]
            a=aud[tuple(sorted((u,v)))]
            assert set(a["support"])==set(supp_list[i])
            steps.append(a)
        return steps

    # v3 rules
    R0 = {0: 9, 4: 3, 6: None}
    Dir = {(6,2): "3->9", (0,4): None}

    def solve_cycle(steps):
        n=len(steps)
        req_hol=[None]*n
        for i,st in enumerate(steps):
            if st["delta"]==2: req_hol[i]=9
            elif st["delta"]==6: req_hol[i]=3

        best=None; best_path=None; best_outer=None
        for outer, comp_tris in outer_to_tri.items():
            allowed=[]
            for i,st in enumerate(steps):
                sm=st["support_mask"]; rh=req_hol[i]
                vals=[]
                for tri in comp_tris:
                    info=tri_info[tri]
                    if (info["cover_mask"] & sm) != sm:
                        continue
                    if rh is not None and info["hol"]!=rh:
                        continue
                    vals.append(tri)
                if not vals:
                    allowed=None; break
                allowed.append(vals)
            if allowed is None: 
                continue

            for start in allowed[0]:
                dp=[{} for _ in range(n)]
                info0=tri_info[start]
                dp[0][start]=(1 if info0["cover12"] else 0, -info0["cover_size"], None)
                ok=True
                for i in range(1,n):
                    prev_edge=steps[i-1]
                    dm=prev_edge["delta"]; rem=prev_edge["rem_sum"]; add=prev_edge["add_sum"]
                    for prev,(cst,negcov,_) in dp[i-1].items():
                        prev_info=tri_info[prev]
                        for cur in allowed[i]:
                            cur_info=tri_info[cur]
                            if dm==0:
                                if prev_info["hol"]!=cur_info["hol"]:
                                    continue
                                req=R0.get(rem,None)
                                if req is not None and cur_info["hol"]!=req:
                                    continue
                            elif dm==4:
                                if prev_info["hol"]==cur_info["hol"]:
                                    continue
                                d=Dir.get((rem,add), None)
                                if d=="3->9" and not (prev_info["hol"]==3 and cur_info["hol"]==9):
                                    continue
                            nc = cst + (1 if cur_info["cover12"] else 0)
                            nn = negcov - cur_info["cover_size"]
                            curbest=dp[i].get(cur)
                            if curbest is None or (nc,nn) < (curbest[0],curbest[1]):
                                dp[i][cur]=(nc,nn,prev)
                    if not dp[i]:
                        ok=False; break
                if not ok:
                    continue

                last_edge=steps[-1]
                dm=last_edge["delta"]; rem=last_edge["rem_sum"]; add=last_edge["add_sum"]
                for last,(cst,negcov,_) in dp[n-1].items():
                    last_info=tri_info[last]; start_info=tri_info[start]
                    close_ok=True
                    if dm==0:
                        if last_info["hol"]!=start_info["hol"]:
                            close_ok=False
                        else:
                            req=R0.get(rem,None)
                            if req is not None and start_info["hol"]!=req:
                                close_ok=False
                    elif dm==4:
                        if last_info["hol"]==start_info["hol"]:
                            close_ok=False
                        else:
                            d=Dir.get((rem,add), None)
                            if d=="3->9" and not (last_info["hol"]==3 and start_info["hol"]==9):
                                close_ok=False
                    if not close_ok:
                        continue
                    cand=(cst,negcov)
                    if best is None or cand < best:
                        best=cand; best_outer=outer
                        path=[None]*n
                        cur=last
                        for i in range(n-1,-1,-1):
                            path[i]=cur
                            cur=dp[i][cur][2]
                        best_path=path
        return best, best_outer, best_path

    cycle_summary=[]
    witness_rows=[]
    for ci,row in cycles.iterrows():
        steps = cycle_steps(row)
        best, outer, path = solve_cycle(steps)
        if best is None:
            raise RuntimeError(f"No witness for cycle index {ci}")
        cycle_summary.append({
            "cycle_index": int(ci),
            "length": int(row.length),
            "cycle_nodes": row.cycle_nodes,
            "best_cover12_steps": int(best[0]),
            "best_sum_cover_size": int(-best[1]),
            "outer_quad": " ".join(map(str,outer)),
        })
        for i,(st,tri) in enumerate(zip(steps,path)):
            info=tri_info[tri]
            witness_rows.append({
                "cycle_index": int(ci),
                "step": int(i),
                "delta": int(st["delta"]),
                "rem_sum": int(st["rem_sum"]),
                "add_sum": int(st["add_sum"]),
                "support": " ".join(map(str,st["support"])),
                "triad": f"{tri[0]} {tri[1]} {tri[2]}",
                "triad_hol": int(info["hol"]),
                "cover_size": int(info["cover_size"]),
                "cover12": int(info["cover12"]),
            })

    pd.DataFrame(cycle_summary).to_csv("phase_aware_v3_cycle_summary.csv", index=False)
    pd.DataFrame(witness_rows).to_csv("phase_aware_v3_2T_cycle_witness_walks.csv", index=False)

    with open("phase_aware_v3_run_summary.json","w") as f:
        json.dump({"R0":R0,"Dir":{str(k):v for k,v in Dir.items()}, "cycle_summary":cycle_summary}, f, indent=2)

if __name__=="__main__":
    main()
