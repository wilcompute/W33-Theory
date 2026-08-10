#!/usr/bin/env python3
"""Pass 4656 — a nontrivial C2 voltage class for the apartment double cover.

Pass4650 proved the homogeneous factorization

  1620 apartments -> 810 selected point-line flags -> 270 selected lines

with the first stage a regular C2 cover.  Here we choose a canonical connected
base graph: the labelled Schreier graph on the 810 flags for the five
deterministically selected W33 transvections.  The same generators act on the
1620 apartments, producing the lifted graph.  A sorted section of the two
apartment lifts over each flag gives an F2 voltage cochain.

The lift is connected, so the class cannot be a coboundary.  We additionally
exhibit a length-six closed base walk whose lifted endpoint is the opposite
sheet.  Hence the cocycle evaluates to one on an explicit cycle and represents
a nonzero class in H^1 of this canonical Schreier graph.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, perm_group, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4656_APARTMENT_C2_VOLTAGE_COHOMOLOGY_REGEN.json"


def inverse(p):
    q = [0] * len(p)
    for i,j in enumerate(p): q[j] = i
    return tuple(q)


def pmask(mask, p):
    y = 0
    x = int(mask)
    while x:
        b = x & -x; i = b.bit_length()-1; x ^= b
        y |= 1 << p[i]
    return y


def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_ = build_geometry()
    Astar = np.asarray(Astar,dtype=np.uint8)
    apartments = sorted(tuple(map(int,a)) for a in apartments)
    assert len(apartments) == 1620

    n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m |= 1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(n) for k in range(i+1,n) if Astar[i,k]]
    B9=rank_basis_int([cols[i]^cols[k] for i,k in edges]); V9=set(span(B9))
    assert len(B9)==9 and j in V9
    rep=lambda x:min(int(x),int(x)^j)

    def ap_fiber(ap):
        x=0
        for i in ap: x ^= cols[i]
        return rep(x)
    def ap_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        assert len(opp)==2
        s=rep(cols[opp[0][0]]^cols[opp[0][1]])
        t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        x=ap_fiber(ap)
        return tuple(sorted((s,t,x)))

    flag_lifts=defaultdict(list)
    for ap in apartments:
        L=ap_line(ap); x=ap_fiber(ap)
        assert x in L
        flag_lifts[(L,x)].append(ap)
    assert len(flag_lifts)==810 and Counter(map(len,flag_lifts.values()))==Counter({2:810})
    flags=sorted(flag_lifts); findex={f:i for i,f in enumerate(flags)}
    aps=apartments; aindex={a:i for i,a in enumerate(aps)}

    # Deterministic PSp generating set: add transvections exactly when the
    # generated line-permutation group grows.
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    chosen=[]
    for vi,p in enumerate(candidates):
        trial=perm_group(gens+[p])
        if len(trial)>len(G):
            gens.append(p); chosen.append(vi); G=trial
        if len(G)==25920: break
    assert len(G)==25920 and len(gens)==5
    assert chosen == [0,1,4,5,13]

    def act_v(x,g): return rep(pmask(rep(x),g))
    def act_line(L,g): return tuple(sorted(act_v(x,g) for x in L))
    def act_flag(f,g):
        L,x=f; return (act_line(L,g),act_v(x,g))
    def act_ap(ap,g): return tuple(sorted(g[i] for i in ap))

    fg=[]; ag=[]
    for g in gens:
        pf=tuple(findex[act_flag(f,g)] for f in flags)
        pa=tuple(aindex[act_ap(a,g)] for a in aps)
        fg.append(pf); ag.append(pa)
        assert all(pf[i]!=i for i in range(810))

    # Sorted local section identifies lift bit 0/1.
    lift_index={}
    for fi,f in enumerate(flags):
        pair=sorted(aindex[a] for a in flag_lifts[f])
        for bit,ai in enumerate(pair): lift_index[ai]=(fi,bit)

    # Labelled Schreier edges: each order-three generator contributes 810
    # undirected triangle edges, so 5*810=4050 labelled edges.
    volt=Counter(); labelled_edges=[]
    adj=[set() for _ in flags]
    for gi,(pf,pa) in enumerate(zip(fg,ag)):
        seen=set()
        for fi in range(810):
            fj=pf[fi]
            e=(min(fi,fj),max(fi,fj))
            if e in seen: continue
            seen.add(e); labelled_edges.append((gi,*e)); adj[fi].add(fj); adj[fj].add(fi)
            ai0=sorted(aindex[a] for a in flag_lifts[flags[fi]])[0]
            aj=pa[ai0]
            fj2,b=lift_index[aj]
            assert fj2==fj
            volt[b]+=1
        assert len(seen)==810
    assert len(labelled_edges)==4050
    assert volt==Counter({0:3414,1:636})

    # Connected base and lift.
    def reachable(start,neighbors):
        seen={start}; Q=deque([start])
        while Q:
            u=Q.popleft()
            for v in neighbors(u):
                if v not in seen: seen.add(v); Q.append(v)
        return seen
    base_seen=reachable(0,lambda u:adj[u]); assert len(base_seen)==810
    inv_ag=[inverse(p) for p in ag]
    lift_seen=reachable(0,lambda u:[p[u] for p in ag+inv_ag]); assert len(lift_seen)==1620
    b1=4050-810+1; assert b1==3241

    # Gauge by a spanning tree; count nonzero cotree coordinates in one
    # explicit representative.  Build section bits h recursively along tree.
    parent=[None]*810; parent_edge=[None]*810; parent[0]=0; Q=deque([0])
    edge_lookup=defaultdict(list)
    for gi,u,v in labelled_edges:
        edge_lookup[frozenset((u,v))].append(gi)
    while Q:
        u=Q.popleft()
        for v in sorted(adj[u]):
            if parent[v] is None:
                parent[v]=u; parent_edge[v]=min(edge_lookup[frozenset((u,v))]); Q.append(v)
    assert all(x is not None for x in parent)

    # Determine directed voltage alpha_g(u) using local lift bit 0.
    alpha={}
    for gi,(pf,pa) in enumerate(zip(fg,ag)):
        for u in range(810):
            ai0=sorted(aindex[a] for a in flag_lifts[flags[u]])[0]
            v,b=lift_index[pa[ai0]]
            assert v==pf[u]
            alpha[(gi,u,v)]=b
            # inverse-directed value equals alpha on reverse edge over F2.
    h=[0]*810
    order=[0]; Q=deque([0])
    while Q:
        u=Q.popleft()
        for v in sorted(adj[u]):
            if parent[v]==u:
                gi=parent_edge[v]
                # choose the correct orientation of the generator edge.
                if fg[gi][u]==v: a=alpha[(gi,u,v)]
                elif fg[gi][v]==u: a=alpha[(gi,v,u)]
                else: raise AssertionError
                h[v]=h[u]^a; order.append(v); Q.append(v)
    nonzero_cotree=0
    tree_pairs={frozenset((v,parent[v])) for v in range(1,810)}
    for gi,u,v in labelled_edges:
        if fg[gi][u]==v: a=alpha[(gi,u,v)]
        elif fg[gi][v]==u: a=alpha[(gi,v,u)]
        else: raise AssertionError
        gauged=a^h[u]^h[v]
        if frozenset((u,v)) in tree_pairs and gi==parent_edge[u if parent[u]==v else v]:
            assert gauged==0
        elif gauged: nonzero_cotree+=1
    assert nonzero_cotree==918

    # Explicit shortest monodromy witness: a closed flag word of length six
    # lifts from sheet 0 to sheet 1.  Search deterministically rather than rely
    # on a hard-coded object numbering.
    inv_fg=[inverse(p) for p in fg]
    ops=[(i,+1,fg[i],ag[i]) for i in range(5)] + [(i,-1,inv_fg[i],inv_ag[i]) for i in range(5)]
    f0=0; a0=sorted(aindex[a] for a in flag_lifts[flags[f0]])[0]
    target=sorted(aindex[a] for a in flag_lifts[flags[f0]])[1]
    start=(f0,a0); goal=(f0,target)
    prev={start:None}; how={}; Q=deque([start]);
    while Q and goal not in prev:
        f,a=Q.popleft()
        for gi,sg,pf,pa in ops:
            z=(pf[f],pa[a])
            if z not in prev:
                prev[z]=(f,a); how[z]=(gi,sg); Q.append(z)
    assert goal in prev
    word=[]; z=goal
    while prev[z] is not None:
        word.append(how[z]); z=prev[z]
    word=list(reversed(word)); assert len(word)==6
    assert word==[(3,1),(0,-1),(1,1),(2,-1),(4,1),(3,-1)]

    # Projected base walk closes; lifted endpoint toggles the C2 sheet.
    f,a=start; projected=[f]
    for gi,sg in word:
        idx=gi if sg==1 else gi
        pf=fg[idx] if sg==1 else inv_fg[idx]
        pa=ag[idx] if sg==1 else inv_ag[idx]
        f,a=pf[f],pa[a]; projected.append(f)
    assert f==f0 and a==target

    out={
      "pass":4656,
      "canonical_base":{"vertices":810,"labelled_edges":4050,"connected":True,"betti_1":3241,"generator_indices":chosen},
      "lift":{"vertices":1620,"connected":True,"deck_group":"C2"},
      "voltage":{"section":"sorted apartment pair over each flag","edge_values":{"0":3414,"1":636},"tree_gauged_nonzero_cotree_coordinates":918},
      "explicit_nonzero_cycle":{"length":6,"generator_word":[[i,s] for i,s in word],"projected_flag_indices":projected,"voltage_evaluation":1},
      "cohomology":{"group":"H^1(Schreier_810;F2)","dimension":3241,"deck_class_nonzero":True,"reason":"explicit closed base walk lifts to the opposite sheet"},
      "theorem":"On the canonical five-transvection Schreier graph of the 810 selected flags, the apartment C2 double cover has a nonzero voltage/cohomology class; an explicit length-six cycle evaluates to one.",
      "boundary":"Graph-cover cohomology for this canonical Schreier graph only; no optical phase is inferred."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
