\
#!/usr/bin/env python3
"""
Phase-aware loop realization v2 for N12_58 2T cycles inside W33 four-center triad graph.

v2 predicate:
- delta=2 -> triad holonomy must be 9 (mod 12)
- delta=6 -> triad holonomy must be 3 (mod 12)
- delta=0 -> transition requires same triad holonomy
- delta=4 -> transition requires different triad holonomy

This script reproduces:
- phase_aware_v2_2T_cycle_witness_walks.csv
- phase_aware_v2_run_summary.json
"""
from __future__ import annotations
import itertools, json
from collections import defaultdict
from pathlib import Path
import pandas as pd

ROOT = Path("repo_extract/data")  # adjust if running elsewhere
W33_LINE_MAP = ROOT / "_workbench/02_geometry/W33_line_phase_map.csv"
TRIAD_TABLE = Path("w33_four_center_triads_with_ray_holonomy.csv")  # expects v1 table present
EDGE_AUDIT = ROOT / "_n12/n12_58_flip_delta_audit_all_edges.csv"
CYCLES = ROOT / "_n12/n12_58_2t_holonomy_nontrivial_cycles.csv"

def support_to_mask(supp):
    m=0
    for x in supp:
        m |= 1<<int(x)
    return m

def build_collinearity(lines):
    col = {p:set() for p in range(40)}
    for L in lines:
        for a,b in itertools.combinations(sorted(L),2):
            col[a].add(b); col[b].add(a)
    return col

def centers_of_triad(col, tri):
    a,b,c=tri
    return set(col[a]) & set(col[b]) & set(col[c])

def main():
    w33 = pd.read_csv(W33_LINE_MAP)
    w33["pts"] = w33["point_ids"].astype(str).apply(lambda s: tuple(int(x) for x in s.split()))
    lines = [set(p) for p in w33["pts"]]
    col = build_collinearity(lines)
    noncol = {p: set(range(40)) - {p} - col[p] for p in range(40)}

    # enumerate all four-center triads and group by center-quad -> outer quad -> 4 triads (K4 component)
    four_center=[]
    for a in range(40):
        for b in range(a+1,40):
            if b not in noncol[a]: 
                continue
            for c in range(b+1,40):
                if c in noncol[a] and c in noncol[b]:
                    C = centers_of_triad(col,(a,b,c))
                    if len(C)==4:
                        four_center.append((a,b,c, tuple(sorted(C))))
    cent_to_tri=defaultdict(list)
    for a,b,c,C in four_center:
        cent_to_tri[C].append(tuple(sorted((a,b,c))))
    outer_to_tri=defaultdict(list)
    for C,tris in cent_to_tri.items():
        outer=tuple(sorted(set().union(*map(set,tris))))
        for tri in tris:
            outer_to_tri[outer].append(tri)

    tri_tbl=pd.read_csv(TRIAD_TABLE)
    tri_info={}
    for r in tri_tbl.itertuples(index=False):
        tri=tuple(sorted(int(x) for x in str(r.w33_points).split()))
        tri_info[tri]={
            "triad_index": int(r.triad_index),
            "hol": int(r.holonomy_z12),
            "cover_mask": int(r.cover_mask),
            "cover12": bool(r.cover12),
            "cover_size": int(r.cover_size),
            "missing_symbols": None if pd.isna(r.missing_symbols) else str(r.missing_symbols),
        }

    # audit edges dict
    audit=pd.read_csv(EDGE_AUDIT)
    aud={}
    for r in audit.itertuples(index=False):
        key=tuple(sorted((int(r.u),int(r.v))))
        aud[key]={"support": tuple(int(x) for x in str(r.flip_support_4set).split()),
                  "delta": int(r.delta_from_pair_phase_diff_mod8)}

    cycles=pd.read_csv(CYCLES)

    def cycle_steps(row):
        nodes=[int(x) for x in row.cycle_nodes.split('-')]
        n=len(nodes)
        supp_list=[[int(x) for x in part.split()] for part in row.supports.split('|')]
        steps=[]
        for i in range(n):
            u=nodes[i]; v=nodes[(i+1)%n]
            a=aud[tuple(sorted((u,v)))]
            supp=a["support"]
            assert set(supp)==set(supp_list[i])
            steps.append({"u":u,"v":v,"support":supp,"support_mask":support_to_mask(supp),"delta":a["delta"]})
        return steps

    def solve_cycle(steps):
        n=len(steps)
        supp_masks=[st["support_mask"] for st in steps]
        deltas=[st["delta"] for st in steps]
        valid_per_step=[]
        for i in range(n):
            dm=deltas[i]
            req=None
            if dm==2: req=9
            elif dm==6: req=3
            sm=supp_masks[i]
            val=set()
            for tri,info in tri_info.items():
                if (info["cover_mask"] & sm) != sm:
                    continue
                if req is not None and info["hol"]!=req:
                    continue
                val.add(tri)
            valid_per_step.append(val)

        best=None
        best_wit=None
        for outer, comp_tris in outer_to_tri.items():
            comp_tris=[tuple(sorted(t)) for t in comp_tris]
            for s in comp_tris:
                if s not in valid_per_step[0]:
                    continue
                dp=[{} for _ in range(n)]
                init_cost = 1 if tri_info[s]["cover12"] else 0
                init_covsum = tri_info[s]["cover_size"]
                dp[0][s]=(init_cost, -init_covsum, None)
                for i in range(1,n):
                    dm_prev=deltas[i-1]
                    for prev,(cst,negcov,_) in dp[i-1].items():
                        for ttri in comp_tris:
                            if ttri not in valid_per_step[i]:
                                continue
                            if dm_prev==0 and tri_info[prev]["hol"]!=tri_info[ttri]["hol"]:
                                continue
                            if dm_prev==4 and tri_info[prev]["hol"]==tri_info[ttri]["hol"]:
                                continue
                            nc = cst + (1 if tri_info[ttri]["cover12"] else 0)
                            nn = negcov - tri_info[ttri]["cover_size"]
                            cur=dp[i].get(ttri)
                            if cur is None or (nc,nn) < (cur[0],cur[1]):
                                dp[i][ttri]=(nc,nn,prev)
                dm_last=deltas[-1]
                for last,(cst,negcov,_) in dp[n-1].items():
                    ok=True
                    if dm_last==0:
                        ok = tri_info[last]["hol"]==tri_info[s]["hol"]
                    elif dm_last==4:
                        ok = tri_info[last]["hol"]!=tri_info[s]["hol"]
                    if not ok:
                        continue
                    cand=(cst,negcov)
                    if best is None or cand < best:
                        best=cand
                        seq=[None]*n
                        seq[n-1]=last
                        cur=last
                        for j in range(n-1,0,-1):
                            cur_prev=dp[j][cur][2]
                            seq[j-1]=cur_prev
                            cur=cur_prev
                        best_wit={"outer_quad":outer,"triads":seq,"cost_cover12":cst,"cover_sum":-negcov}
        return best_wit

    rows=[]
    per_cycle={}
    outer_used={}
    total=0
    for idx,row in cycles.iterrows():
        steps=cycle_steps(row)
        sol=solve_cycle(steps)
        per_cycle[idx]=sol["cost_cover12"]
        outer_used[idx]=" ".join(map(str,sol["outer_quad"]))
        total += sol["cost_cover12"]
        seq=sol["triads"]
        n=len(seq)
        for i in range(n):
            tri=seq[i]; info=tri_info[tri]; st=steps[i]
            delta=st["delta"]
            req = (9 if delta==2 else (3 if delta==6 else None))
            nxt=seq[(i+1)%n]
            trans_ok=True
            if delta==0:
                trans_ok = tri_info[tri]["hol"]==tri_info[nxt]["hol"]
            elif delta==4:
                trans_ok = tri_info[tri]["hol"]!=tri_info[nxt]["hol"]
            rows.append({
                "cycle_index": idx,
                "cycle_length": n,
                "step": i,
                "n12_u": st["u"],
                "n12_v": st["v"],
                "support_mask": st["support_mask"],
                "support_symbols": " ".join(map(str,st["support"])),
                "delta": delta,
                "required_triadhol": req,
                "triad_index": info["triad_index"],
                "w33_points": " ".join(map(str,tri)),
                "triad_holonomy_z12": info["hol"],
                "phase_node_constraint_ok": (req is None) or (info["hol"]==req),
                "phase_transition_constraint_ok": trans_ok,
                "triad_cover12": info["cover12"],
                "triad_cover_size": info["cover_size"],
                "triad_missing_symbols": info["missing_symbols"],
                "outer_quad": " ".join(map(str,sol["outer_quad"])),
            })

    out_csv=Path("phase_aware_v2_2T_cycle_witness_walks.csv")
    pd.DataFrame(rows).to_csv(out_csv,index=False)

    summary={
        "phase_predicate_v2":{
            "delta2_requires_triadhol":9,
            "delta6_requires_triadhol":3,
            "delta0_requires_transition":"same triad holonomy",
            "delta4_requires_transition":"different triad holonomy"
        },
        "cycle_costs_cover12": per_cycle,
        "total_cover12_steps_across_5_cycles": total,
        "outer_quad_components_used": outer_used,
    }
    Path("phase_aware_v2_run_summary.json").write_text(json.dumps(summary,indent=2))

if __name__ == "__main__":
    main()
