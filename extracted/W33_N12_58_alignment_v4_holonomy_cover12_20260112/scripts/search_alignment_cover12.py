#!/usr/bin/env python3
"""Search for a high-scoring W33↔N12_58 bijection under the cover12 objective.

This script:
- Enforces the N12 block constraints (7 size-4 blocks land on W33 lines; 3 pairs land on collinear pairs).
- Uses randomized initialization + constrained annealing moves (within blocks/pairs/leftovers and occasional block swaps).
- Scores by: number of W33 four-center triads whose mapped N12 triple covers all 12 vertex symbols {0..9,a,b}.

Inputs (relative to repo root):
- data/_workbench/02_geometry/W33_line_phase_map.csv
- data/_n12/n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_20260109t134000z.csv
- data/_n12/n12_58_candidate_lines_from_size12_orbits_tau_cycle_sets_20260109t134000z.csv

Outputs: writes best mapping CSVs in the current working directory.
"""
from __future__ import annotations
import itertools, random, math, json
from collections import Counter
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
W33_LINES = ROOT / "data/_workbench/02_geometry/W33_line_phase_map.csv"
CAND_PTS = ROOT / "data/_n12/n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_20260109t134000z.csv"
CAND_LINES = ROOT / "data/_n12/n12_58_candidate_lines_from_size12_orbits_tau_cycle_sets_20260109t134000z.csv"

ALL_SYMBOLS=set("0123456789ab")

def sym_to_int(ch: str) -> int:
    if ch == "a": return 10
    if ch == "b": return 11
    return int(ch)

def point_symbol_set(members_str: str) -> set[str]:
    parts=[p.strip() for p in str(members_str).split(",") if p.strip()]
    s=set()
    for tri in parts:
        s |= set(tri)
    return s

def main(seed: int = 0, samples: int = 2000, anneal_steps: int = 80000) -> None:
    random.seed(seed)

    # load W33
    df = pd.read_csv(W33_LINES)
    df["pts"] = df["point_ids"].astype(str).apply(lambda s: [int(x) for x in s.split()])
    lines = [set(pts) for pts in df["pts"]]
    points = sorted(set(p for L in lines for p in L))

    col = {p: set() for p in points}
    for L in lines:
        for a,b in itertools.combinations(sorted(L),2):
            col[a].add(b); col[b].add(a)
    noncol = {p: set(points)-{p}-col[p] for p in points}

    triads=[]
    for a in range(40):
        for b in [x for x in noncol[a] if x>a]:
            for c in [x for x in noncol[a].intersection(noncol[b]) if x>b]:
                triads.append((a,b,c))

    def centers(t):
        a,b,c=t
        return col[a].intersection(col[b]).intersection(col[c])

    special=[t for t in triads if len(centers(t))==4]

    # load N12 candidates
    cand=pd.read_csv(CAND_PTS)
    symset={row.point_id: point_symbol_set(row.members) for row in cand.itertuples(index=False)}
    n12_pts=list(cand["point_id"])

    cl=pd.read_csv(CAND_LINES)
    blocks=[tuple(str(s).split()) for s in cl["points"]]
    uniq=sorted(set(blocks), key=lambda b:(len(b), b))
    size4=[b for b in uniq if len(b)==4]
    size2=[b for b in uniq if len(b)==2]
    covered=set(itertools.chain.from_iterable(size4+size2))
    leftover=sorted(set(n12_pts)-covered)

    # enumerate 7-line partial spreads (disjointness cliques)
    line_disjoint=[set() for _ in range(40)]
    for i in range(40):
        for j in range(i+1,40):
            if lines[i].isdisjoint(lines[j]):
                line_disjoint[i].add(j); line_disjoint[j].add(i)

    def cliques7():
        out=set()
        def extend(clq, cand):
            if len(clq)==7:
                out.add(tuple(sorted(clq))); return
            for v in sorted(list(cand)):
                newcand={u for u in cand if u>v and u in line_disjoint[v]}
                extend(clq+[v], newcand)
        for v in range(40):
            extend([v], {u for u in line_disjoint[v] if u>v})
        return sorted(out)

    spreads=cliques7()

    def score(w2n):
        sc=0
        for a,b,c in special:
            u=symset[w2n[a]]|symset[w2n[b]]|symset[w2n[c]]
            if u==ALL_SYMBOLS:
                sc+=1
        return sc

    def random_valid_mapping(spread):
        used=set()
        w2n={}
        n2w={}
        blocks=size4.copy(); random.shuffle(blocks)
        lids=list(spread); random.shuffle(lids)
        for block,lid in zip(blocks,lids):
            pts=list(lines[lid]); random.shuffle(pts)
            lbls=list(block); random.shuffle(lbls)
            for p,lbl in zip(pts,lbls):
                w2n[p]=lbl; n2w[lbl]=p; used.add(p)
        pairs=size2.copy(); random.shuffle(pairs)
        for pair in pairs:
            lblA,lblB=pair
            unused=[p for p in points if p not in used]
            random.shuffle(unused)
            found=False
            for i,u in enumerate(unused):
                for v in unused[i+1:]:
                    if v in col[u]:
                        w2n[u]=lblA; w2n[v]=lblB
                        n2w[lblA]=u; n2w[lblB]=v
                        used.add(u); used.add(v)
                        found=True
                        break
                if found: break
            if not found:
                return None
        unused=[p for p in points if p not in used]
        if len(unused)!=6: return None
        lbls=leftover.copy(); random.shuffle(lbls); random.shuffle(unused)
        for p,lbl in zip(unused,lbls):
            w2n[p]=lbl; n2w[lbl]=p
        return w2n, n2w

    # pick best initial
    best_sc=-1
    best_w2n=None
    for _ in range(samples):
        spread=random.choice(spreads)
        res=random_valid_mapping(spread)
        if res is None: continue
        w2n,_=res
        sc=score(w2n)
        if sc>best_sc:
            best_sc=sc; best_w2n=w2n

    if best_w2n is None:
        raise RuntimeError("No valid mapping found")

    # constrained annealing: swap within blocks/pairs/leftovers + occasional block swap
    w2n=best_w2n.copy()
    n2w={lbl:p for p,lbl in w2n.items()}

    # group membership lists
    def refresh_groups():
        block_pts=[[n2w[lbl] for lbl in block] for block in size4]
        pair_pts=[[n2w[lbl] for lbl in pair] for pair in size2]
        lone_pts=[n2w[lbl] for lbl in leftover]
        return block_pts, pair_pts, lone_pts

    def swap_points(p,q):
        lp,lq=w2n[p],w2n[q]
        w2n[p],w2n[q]=lq,lp
        n2w[lp],n2w[lq]=q,p

    cur=score(w2n)
    best=(cur,w2n.copy())

    block_pts,pair_pts,lone_pts=refresh_groups()
    for t in range(anneal_steps):
        T=1.0*(1-t/anneal_steps)+0.01*(t/anneal_steps)
        r=random.random()
        if r<0.7:
            bi=random.randrange(len(size4))
            pts=block_pts[bi]
            p,q=random.sample(pts,2)
            swap_points(p,q)
        elif r<0.85:
            pi=random.randrange(len(size2))
            u,v=pair_pts[pi]
            swap_points(u,v)
        elif r<0.95:
            p,q=random.sample(lone_pts,2)
            swap_points(p,q)
        else:
            bi,bj=random.sample(range(len(size4)),2)
            pi=list(block_pts[bi]); pj=list(block_pts[bj])
            random.shuffle(pi); random.shuffle(pj)
            for p,q in zip(pi,pj):
                swap_points(p,q)

        new=score(w2n)
        delta=new-cur
        accept = delta>=0 or random.random()<math.exp(delta/max(T,1e-9))
        if accept:
            cur=new
            if cur>best[0]:
                best=(cur,w2n.copy())
            block_pts,pair_pts,lone_pts=refresh_groups()
        else:
            # revert by swapping back in reverse (repeat same move is annoying; simplest: reset to best)
            w2n=best[1].copy()
            n2w={lbl:p for p,lbl in w2n.items()}
            cur=best[0]
            block_pts,pair_pts,lone_pts=refresh_groups()

    best_sc,best_w2n=best
    out_w33=pd.DataFrame({"w33_point": list(range(40)), "n12_point": [best_w2n[p] for p in range(40)]})
    out_n12=pd.DataFrame({"n12_point": n12_pts, "w33_point": [n2w[lbl] for lbl in n12_pts]})
    out_w33.to_csv("best_w33_to_n12_mapping.csv", index=False)
    out_n12.to_csv("best_n12_to_w33_mapping.csv", index=False)
    print(json.dumps({"best_cover12_score": best_sc, "out_files": ["best_w33_to_n12_mapping.csv","best_n12_to_w33_mapping.csv"]}, indent=2))

if __name__ == "__main__":
    main()
