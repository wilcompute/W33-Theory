#!/usr/bin/env python3
"""Recompute v5 'phase interference' summary from the v3 bundle contents.

Inputs (default):
- /mnt/data/W33_N12_58_phase_aware_bundle_v3_20260112.zip

Outputs (current working directory):
- per_cycle_partition_functions_and_adjusted.csv
- best_delta_phase_maps_by_lambda.json
"""
import zipfile, json, math, cmath, itertools, numpy as np, pandas as pd
from io import BytesIO

BUNDLE="/mnt/data/W33_N12_58_phase_aware_bundle_v3_20260112.zip"
LAM_GRID=[0.0,0.2,0.5,1.0]
VALS=[1, -1, 1j, -1j]
DELTAS=[0,2,4,6]

def load_v3():
    with zipfile.ZipFile(BUNDLE) as z:
        triads=pd.read_csv(BytesIO(z.read('W33_N12_58_phase_aware_loop_v3/w33_four_center_triads_with_ray_holonomy.csv')))
        witness=pd.read_csv(BytesIO(z.read('W33_N12_58_phase_aware_loop_v3/phase_aware_v3_2T_cycle_witness_walks.csv')))
    return triads, witness

def build_adjacency(triads: pd.DataFrame):
    pts=triads[['a','b','c']].astype(int).values
    pair_to={}
    for i,(a,b,c) in enumerate(pts):
        a,b,c=sorted((a,b,c))
        for p in [(a,b),(a,c),(b,c)]:
            pair_to.setdefault(p,[]).append(i)
    adj=[set() for _ in range(len(triads))]
    for lst in pair_to.values():
        for i in lst:
            for j in lst:
                if i!=j: adj[i].add(j)
    return [sorted(s) for s in adj]

def transition_ok(hol, prev_t, cur_t, prev_edge):
    d=int(prev_edge['delta']); r=int(prev_edge['rem_sum']); a=int(prev_edge['add_sum'])
    hprev=int(hol[prev_t]); hcur=int(hol[cur_t])
    if d==0:
        if hprev!=hcur: return False
        if r==0 and a==0: return hcur==9
        if r==4 and a==4: return hcur==3
        return True
    if d==4:
        if hprev==hcur: return False
        if r==6 and a==2: return (hprev==3 and hcur==9)
        return True
    return True

def node_ok(hol, t, delta):
    h=int(hol[t])
    if delta==2: return h==9
    if delta==6: return h==3
    return True

def partition_function_cycle(triad_adj, triads, steps, cand_list, lam):
    hol=triads['hol_mod12'].astype(int).values
    cover12=triads['cover12'].astype(int).values
    phase=np.array([cmath.exp(2j*math.pi*h/12) for h in hol])
    w = phase * np.exp(-lam*cover12)
    cover_mask=triads['cover_mask'].astype(int).values

    cand_sets=[set(c) for c in cand_list]
    total=0+0j
    for t0 in cand_list[0]:
        dp={t0: w[t0]}
        for i in range(1,len(steps)):
            prev_edge=steps[i-1]
            cand=cand_sets[i]
            new={}
            for prev_t,val in dp.items():
                for cur_t in triad_adj[prev_t]:
                    if cur_t not in cand:
                        continue
                    if not transition_ok(hol, prev_t, cur_t, prev_edge):
                        continue
                    new[cur_t]=new.get(cur_t,0+0j)+val*w[cur_t]
            dp=new
            if not dp:
                break
        if not dp:
            continue
        last_edge=steps[-1]
        for t_last,val in dp.items():
            if t0 not in triad_adj[t_last]:
                continue
            if not transition_ok(hol, t_last, t0, last_edge):
                continue
            total += val
    return total

def main():
    triads, witness = load_v3()
    triad_adj=build_adjacency(triads)
    hol=triads['hol_mod12'].astype(int).values
    cover_mask=triads['cover_mask'].astype(int).values

    cycles={}
    for cid, grp in witness.groupby('cycle_index'):
        grp=grp.sort_values('step')
        cycles[int(cid)] = grp[['support_mask','delta','rem_sum','add_sum']].astype(int).to_dict('records')

    cand_per={}
    for cid, steps in cycles.items():
        cand=[]
        for st in steps:
            sm=int(st['support_mask']); d=int(st['delta'])
            idx=np.nonzero((cover_mask & sm)==sm)[0]
            idx=[i for i in idx if node_ok(hol,i,d)]
            cand.append(idx)
        cand_per[cid]=cand

    delta_seq={cid:[s['delta'] for s in cycles[cid]] for cid in sorted(cycles)}

    records=[]
    best_records=[]
    for lam in LAM_GRID:
        Zc={cid: partition_function_cycle(triad_adj, triads, cycles[cid], cand_per[cid], lam) for cid in sorted(cycles)}
        best=-1; bestm=None; bestadj=None
        for comb in itertools.product(VALS, repeat=4):
            fmap=dict(zip(DELTAS, comb))
            adjZ=[]
            for cid in sorted(cycles):
                g=1+0j
                for d in delta_seq[cid]:
                    g*=fmap[d]
                adjZ.append(Zc[cid]*g)
            score=abs(sum(adjZ))
            if score>best:
                best=score; bestm=fmap; bestadj=adjZ
        upper=sum(abs(Zc[cid]) for cid in sorted(cycles))
        best_records.append({
            "lambda": lam,
            "best_abs_sum": float(best),
            "upper_bound_sum_abs": float(upper),
            "delta_phase_map_raw": {str(k): [float(complex(v).real), float(complex(v).imag)] for k,v in bestm.items()},
        })
        for cid in sorted(cycles):
            z=Zc[cid]
            g=1+0j
            for d in delta_seq[cid]:
                g*=bestm[d]
            zadj=z*g
            records.append({
                "lambda": lam,
                "cycle_index": cid,
                "Z_real": float(z.real),
                "Z_imag": float(z.imag),
                "Z_abs": float(abs(z)),
                "Z_arg_deg": float(math.degrees(cmath.phase(z))),
                "Z_adj_real": float(zadj.real),
                "Z_adj_imag": float(zadj.imag),
                "Z_adj_abs": float(abs(zadj)),
                "Z_adj_arg_deg": float(math.degrees(cmath.phase(zadj))),
            })
    pd.DataFrame(records).to_csv("per_cycle_partition_functions_and_adjusted.csv", index=False)
    from utils.json_safe import dump_json
    dump_json(best_records, "best_delta_phase_maps_by_lambda.json", indent=2)

if __name__=="__main__":
    main()
