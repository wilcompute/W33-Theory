#!/usr/bin/env python3
"""Pass 4748 — genuine cross-fiber binary codes from the 3 K2,2 connection law.

The 2025 router edges split canonically into 135 disjoint 15-edge cells indexed
by (GQ packet, internal sheet coordinate).  Each cell contains:

  * three Petersen hot edges, one in each of the three GQ lines through packet p;
  * three cold K2,2 blocks, one for each pair of those lines, with four physical
    edges per block.

Thus each cell is the weighted six-coordinate incidence geometry of a triangle:
three vertex symbols of weight 1 and three edge symbols of weight 4.  We enumerate
all binary linear subspaces of F2^6 invariant under S3 on that triangle, compute
their weighted minimum distances, and lift the Pareto-optimal local codes to 135
disjoint cells.  This produces exact PGSp-invariant cross-fiber code families.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
from w33_pass4716_selected270_bundle_connection import build_bundle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4748_CROSSFIBER_ROUTER_CODE.json'

def gf2_rank(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def all_subspaces6():
    subs={frozenset([0])};front=[frozenset([0])]
    while front:
        S=front.pop()
        for v in range(1,64):
            if v in S:continue
            T=frozenset(set(S)|{x^v for x in S})
            if T not in subs:subs.add(T);front.append(T)
    assert len(subs)==2825
    return subs

def main():
    X=build_bundle();K5=X['K5'];projected=X['projected'];hot=X['hot'];cold=X['cold']
    _,_,_,_,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    rank_basis=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    fibers=defaultdict(list)
    for ap in apartments:fibers[fib(ap)].append(ap)
    support_to_s=defaultdict(list)
    for s,F in fibers.items():support_to_s[frozenset().union(*(set(ap) for ap in F))].append(s)
    packets=sorted(tuple(sorted(sidx[x] for x in S)) for S in support_to_s.values());assert packets==X['packets']
    packet_of={x:p for p,T in enumerate(packets) for x in T};coord={(p,x):i for p,T in enumerate(packets) for i,x in enumerate(T)}
    owner=[]
    for T in projected:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])

    # label every hot edge by (fiber, packet, coordinate)
    hot_label={};hot_by_cell=defaultdict(list)
    for u,v in hot:
        inter=set(selected[u])&set(selected[v]);assert len(inter)==1
        x=sidx[next(iter(inter))];p=packet_of[x];c=coord[(p,x)];assert owner[u]==owner[v] and p in K5[owner[u]]
        lab=(owner[u],p,c);assert lab not in hot_label.values();hot_label[(u,v)]=lab;hot_by_cell[(p,c)].append((u,v))
    assert len(hot_label)==405 and Counter(len(v) for v in hot_by_cell.values())==Counter({3:135})

    # label cold edges by quotient-edge + shared packet coordinate; each block has 4 edges
    cold_blocks=defaultdict(list)
    for u,v in cold:
        inter=set(selected[u])&set(selected[v]);assert len(inter)==1
        x=sidx[next(iter(inter))];p=packet_of[x];c=coord[(p,x)]
        a,b=sorted((owner[u],owner[v]));assert K5[a]&K5[b]=={p}
        cold_blocks[(a,b,p,c)].append((u,v))
    assert len(cold_blocks)==405 and set(map(len,cold_blocks.values()))=={4}

    # build 135 cells = three hot + three cold blocks = 15 physical edges
    cells={}
    for p in range(45):
        incident=sorted(i for i,S in enumerate(K5) if p in S);assert len(incident)==3
        for c in range(3):
            H=sorted(hot_by_cell[(p,c)]);assert len(H)==3
            B=[]
            for a,b in itertools.combinations(incident,2):
                E=sorted(cold_blocks[(min(a,b),max(a,b),p,c)]);assert len(E)==4;B.append(E)
            phys=set(H)
            for E in B:phys.update(E)
            assert len(phys)==15
            cells[(p,c)]={'fibers':incident,'hot':H,'blocks':B,'physical':sorted(phys)}
    all_edges=set(hot)|set(cold)
    counts=Counter(e for C in cells.values() for e in C['physical'])
    assert len(counts)==2025 and set(counts)==all_edges and set(counts.values())=={1}

    # S3 acts on triangle vertices (three fibers) and its three unordered pairs.
    perms=list(itertools.permutations(range(3)))
    pairs=[(0,1),(0,2),(1,2)];eidx={e:3+i for i,e in enumerate(pairs)}
    def act6(x,p):
        y=0
        for i in range(3):
            if (x>>i)&1:y|=1<<p[i]
        for i,(a,b) in enumerate(pairs):
            if (x>>(3+i))&1:y|=1<<eidx[tuple(sorted((p[a],p[b])))]
        return y
    weights=[1,1,1,4,4,4]
    def wt(x):return sum(weights[i] for i in range(6) if (x>>i)&1)
    inv=[]
    for S in all_subspaces6():
        if all(all(act6(x,p) in S for x in S) for p in perms):
            k=int(round(math.log2(len(S))));d=min((wt(x) for x in S if x),default=99)
            inv.append((k,d,S))
    assert len(inv)==25
    pairs_kd=sorted(set((k,d) for k,d,S in inv if k))
    pareto=[]
    for k,d in pairs_kd:
        if not any(k2>=k and d2>=d and (k2>k or d2>d) for k2,d2 in pairs_kd):pareto.append((k,d))
    assert pareto==[(1,15),(2,10),(3,7),(4,3),(5,2),(6,1)]

    # give one explicit basis per Pareto type and lift global parameters
    def basis(S):
        piv={};out=[]
        for x in sorted(S):
            y=x
            while y:
                p=y.bit_length()-1
                if p in piv:y^=piv[p]
                else:piv[p]=y;out.append(y);break
        return out
    rows=[]
    for k,d in pareto:
        S=next(S for kk,dd,S in inv if (kk,dd)==(k,d))
        B=basis(S);assert len(B)==k
        rows.append({'local_dimension':k,'weighted_distance':d,'basis_6bit':[format(x,'06b') for x in B],
                     'global_parameters':f'[2025,{135*k},{d}]_2','rate':(135*k)/2025,'K_times_d':135*k*d})

    # compare against uncoupled hot-cycle + cold-K2,2-repetition baseline
    baseline={'parameters':'[2025,567,4]_2','dimension':567,'distance':4,'rate':567/2025,'K_times_d':2268,
              'construction':'27 Petersen [15,6,5] cycle codes plus 405 independent [4,1,4] cold-block repetitions'}
    best=max(rows,key=lambda r:r['K_times_d'])
    assert (best['local_dimension'],best['weighted_distance'])==(3,7) and best['K_times_d']==2835

    out={'pass':4748,'cell_decomposition':{'cells':135,'physical_edges_per_cell':15,'partition_all_2025_edges':True,
      'symbolic_geometry':'triangle: 3 hot vertex symbols of physical weight 1 + 3 cold edge symbols of physical weight 4'},
      'S3_invariant_local_subspaces':{'count':25,'dimension_distance_pairs':pairs_kd,'Pareto':rows},
      'uncoupled_baseline':baseline,
      'dimension_distance_product_best':{'global_parameters':best['global_parameters'],'K_times_d':best['K_times_d'],'baseline_K_times_d':baseline['K_times_d'],'improves_this_specific_metric':best['K_times_d']>baseline['K_times_d']},
      'symmetry':'The construction is intrinsic in packet/fiber/coordinate incidence; PSp and the PGSp outer action permute the 135 cells and induce the triangle S3 action, so every listed S3-invariant local code lifts to a PGSp-invariant global code.',
      'theorem':'The 3K2,2 connection law canonically partitions all 2025 router edges into 135 fifteen-edge cross-fiber cells. Exhausting all S3-invariant binary local subspaces gives Pareto points (k,d_w)=(1,15),(2,10),(3,7),(4,3),(5,2),(6,1), hence exact PGSp-invariant global families [2025,135k,d_w]_2. The k=3 family [2025,405,7]_2 improves the simple K*d metric over the uncoupled [2025,567,4]_2 baseline, while lowering rate and raising distance.',
      'boundary':'Exact binary-code/symmetry result. K*d is only one explicit comparison metric; no universal coding optimum or physical fault-tolerance threshold is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
