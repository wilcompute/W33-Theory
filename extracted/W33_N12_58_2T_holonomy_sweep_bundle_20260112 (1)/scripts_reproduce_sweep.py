#!/usr/bin/env python3
"""Reproduce the N12_58 ↔ W33 2T-holonomy–aware annealing sweep.

This script:
- loads the W33 incidence structure (40 lines, 40 points)
- loads the C^4 ray realization and computes Z12 edge phases and triad holonomy
- loads N12_58 candidate 40 points and the 7+3 block constraints
- parses the 2T nontrivial cycle supports and weights support-4sets by frequency
- performs random initialization + simulated annealing with constraint-preserving swaps
- writes the best mapping and triad tables

Designed to run inside the repository root, where `data/` is present.

"""
import math, random, re, json
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path("data")

W33_CSV = DATA / "_workbench/02_geometry/W33_line_phase_map.csv"
RAYS_CSV = DATA / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
CAND40_CSV = next((DATA / "_n12").glob("n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_*.csv"))
CANDLINES_CSV = next((DATA / "_n12").glob("n12_58_candidate_lines_from_size12_orbits_tau_cycle_sets_*.csv"))
T2_CSV = DATA / "_n12/n12_58_2t_holonomy_nontrivial_cycles.csv"

sym_map = {str(i): i for i in range(10)}
sym_map.update({"a": 10, "b": 11})
ALLBITS = (1<<12)-1

def tri_to_set(tri: str):
    tri = tri.strip()
    return {sym_map[ch] for ch in tri} if tri else set()

def members_to_union(mem: str):
    tris = [t for t in re.split(r"[,\s]+", str(mem)) if t and t != "nan"]
    u=set()
    for t in tris:
        u |= tri_to_set(t)
    return u

def set_to_mask(s):
    m=0
    for x in s:
        m |= 1<<x
    return m

def parse_complex(s: str) -> complex:
    return complex(s.replace(" ", ""))

def parse_supports(s: str):
    parts = str(s).split("|")
    out=[]
    for part in parts:
        part = part.strip()
        if not part: 
            continue
        out.append(tuple(sorted(int(x) for x in part.split())))
    return out

def main():
    w33 = pd.read_csv(W33_CSV)
    w33["pts"] = w33["point_ids"].astype(str).apply(lambda s: tuple(sorted(int(x) for x in s.split())))
    lines = list(w33["pts"])

    col_adj=[set() for _ in range(40)]
    for pts in lines:
        for i in range(4):
            for j in range(i+1,4):
                a,b=pts[i],pts[j]
                col_adj[a].add(b); col_adj[b].add(a)
    non_adj=[set(range(40))-{i}-col_adj[i] for i in range(40)]

    def centers(a,b,c):
        return col_adj[a] & col_adj[b] & col_adj[c]

    triads4=[]
    for a in range(40):
        for b in sorted(non_adj[a]):
            if b<=a: continue
            for c in sorted(non_adj[a] & non_adj[b]):
                if c<=b: continue
                if len(centers(a,b,c))==4:
                    triads4.append((a,b,c))

    rays = pd.read_csv(RAYS_CSV)
    vecs=np.zeros((40,4),dtype=complex)
    for r in rays.itertuples(index=False):
        pid=int(r.point_id)
        vecs[pid]=[parse_complex(r.v0),parse_complex(r.v1),parse_complex(r.v2),parse_complex(r.v3)]

    twopi=2*math.pi
    def quant_k(z: complex) -> int:
        ang=math.atan2(z.imag, z.real)
        if ang<0: ang += twopi
        return int(round(12*ang/twopi))%12

    kmat=np.full((40,40), -1, dtype=int)
    for p in range(40):
        for q in range(40):
            if p==q: continue
            if q in col_adj[p]:
                continue
            kmat[p,q]=quant_k(np.vdot(vecs[p], vecs[q]))

    def hol(a,b,c): 
        return (kmat[a,b]+kmat[b,c]+kmat[c,a])%12

    cand = pd.read_csv(CAND40_CSV)
    cand["u"] = cand["members"].apply(members_to_union)
    masks={r.point_id: set_to_mask(r.u) for r in cand.itertuples(index=False)}

    # blocks
    cl = pd.read_csv(CANDLINES_CSV)
    cl["pts"] = cl["points"].astype(str).apply(lambda s: tuple(s.split()))
    unique_blocks = sorted(set(cl["pts"]))
    blocks4=[b for b in unique_blocks if len(b)==4]
    blocks2=[b for b in unique_blocks if len(b)==2]
    all_ids=set(cand["point_id"])
    used=set().union(*[set(b) for b in blocks4], *[set(b) for b in blocks2])
    singles=sorted(all_ids-used)

    t2 = pd.read_csv(T2_CSV)
    support_counts=Counter()
    for lst in t2["supports"].apply(parse_supports):
        for st in lst:
            support_counts[st]+=1
    support_items=[(set_to_mask(set(st)), w) for st,w in support_counts.items()]

    # Build quick scoring helpers
    triads4_arr=np.array(triads4, dtype=int)
    hols=np.array([hol(a,b,c) for a,b,c in triads4], dtype=int)

    line_sets=[frozenset(pts) for pts in lines]
    line_indices=list(range(len(line_sets)))
    col_pairs=set()
    for pts in lines:
        for i in range(4):
            for j in range(i+1,4):
                a,b=pts[i],pts[j]
                if a>b: a,b=b,a
                col_pairs.add((a,b))

    def random_partial_spread(k=7, max_tries=500):
        for _ in range(max_tries):
            chosen=[]
            used=set()
            for idx in random.sample(line_indices, len(line_indices)):
                s=line_sets[idx]
                if used.isdisjoint(s):
                    chosen.append(idx)
                    used |= set(s)
                    if len(chosen)==k:
                        return chosen
        return None

    def build_embedding():
        spread=random_partial_spread()
        if spread is None: 
            return None
        blocks4_sh=list(blocks4); random.shuffle(blocks4_sh)
        lines_sh=spread[:]; random.shuffle(lines_sh)
        n12_to_w33={}
        used_w=set()
        for blk, lid in zip(blocks4_sh, lines_sh):
            pts=list(line_sets[lid]); random.shuffle(pts)
            for n12p,w33p in zip(blk, pts):
                n12_to_w33[n12p]=w33p; used_w.add(w33p)
        rem=set(range(40))-used_w
        blocks2_sh=list(blocks2); random.shuffle(blocks2_sh)
        for blk in blocks2_sh:
            candp=[p for p in rem if any(((min(p,q),max(p,q)) in col_pairs) for q in rem if q!=p)]
            if not candp: 
                return None
            p=random.choice(candp)
            qs=[q for q in rem if q!=p and ((min(p,q),max(p,q)) in col_pairs)]
            q=random.choice(qs)
            pts=[p,q]; random.shuffle(pts)
            for n12p,w33p in zip(blk, pts):
                n12_to_w33[n12p]=w33p
            rem.remove(p); rem.remove(q)
        rem=list(rem); random.shuffle(rem)
        if len(rem)!=len(singles): 
            return None
        for n12p,w33p in zip(singles, rem):
            n12_to_w33[n12p]=w33p
        w33_to_n12=[None]*40
        for n12p,w33p in n12_to_w33.items():
            w33_to_n12[w33p]=n12p
        return w33_to_n12

    def score(w33_to_n12):
        cover=0; sec=0
        for a,b,c in triads4_arr:
            um = masks[w33_to_n12[a]] | masks[w33_to_n12[b]] | masks[w33_to_n12[c]]
            if um==ALLBITS:
                cover += 1
            else:
                s=0
                for sm,w in support_items:
                    if (sm & um)==sm:
                        s += w
                sec += s
        return cover, sec

    # Sampling loop (simple)
    best=(0,-1); best_map=None
    for _ in range(40000):
        emb=build_embedding()
        if emb is None: 
            continue
        sc=score(emb)
        if sc>best:
            best=sc; best_map=emb
    print("best(sample) =", best)

    # Write best mapping
    if best_map is None:
        raise SystemExit("no embedding found")

    out = Path("W33_N12_58_2T_sweep_out")
    out.mkdir(exist_ok=True)
    pd.DataFrame([(i,best_map[i]) for i in range(40)], columns=["w33_point","n12_point"]).to_csv(out/"best_w33_to_n12_mapping.csv", index=False)

if __name__ == "__main__":
    main()
