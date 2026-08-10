#!/usr/bin/env python3
"""Pass 4769 — modular H^1 head/socle data for the invariant 810-flag graph.

Work directly in spanning-tree coordinates for H^1(Gamma;F2), dimension 5671.
For each PSp generator (and then the PGSp outer involution) construct the exact
binary action without materializing dense 5671x5671 matrices.  We compute:

* fixed-space dimensions = trivial socle dimensions;
* coinvariant dimensions = trivial head dimensions;
* whether the explicit apartment deck class lies in the augmentation subspace
  sum_g (g-1)H^1.

If the invariant deck vector lies in the augmentation subspace then no invariant
linear functional can take value one on it, so its trivial submodule cannot split
off as a direct summand.  This is the requested exact nonsplitting certificate;
we do not claim the complete Loewy series of the 5671-dimensional module.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4745_invariant_h1_character import build_flag_graph_and_group
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4769_MODULAR_H1_HEAD_SOCLE.json'

def add_basis(piv,x):
    y=int(x)
    while y:
        p=y.bit_length()-1
        if p in piv:y^=piv[p]
        else:piv[p]=y;return True
    return False

def reduce_basis(piv,x):
    y=int(x)
    while y:
        p=y.bit_length()-1
        if p in piv:y^=piv[p]
        else:break
    return y

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,flags,afi,edges,G,gens,outer=build_flag_graph_and_group()
    edges=sorted(tuple(sorted(e)) for e in edges);eset=set(edges)
    # deterministic BFS tree
    nbr=[[] for _ in range(810)]
    for u,v in edges:nbr[u].append(v);nbr[v].append(u)
    parent={0:None};order=[0];Q=deque([0])
    while Q:
        u=Q.popleft()
        for v in sorted(nbr[u]):
            if v not in parent:parent[v]=u;order.append(v);Q.append(v)
    assert len(parent)==810
    tree={tuple(sorted((v,parent[v]))) for v in order[1:]}
    cot=[e for e in edges if e not in tree];cidx={e:i for i,e in enumerate(cot)}
    n=len(cot);assert n==6480-810+1==5671

    def action_rows(g):
        p=[afi(i,g) for i in range(810)];q=[0]*810
        for i,j in enumerate(p):q[j]=i
        def preexpr(e):
            u,v=e;f=tuple(sorted((q[u],q[v])));assert f in eset
            j=cidx.get(f);return 0 if j is None else (1<<j)
        pot=[0]*810
        for v in order[1:]:
            u=parent[v];pot[v]=pot[u]^preexpr(tuple(sorted((u,v))))
        rows=[]
        for u,v in cot:rows.append(preexpr((u,v))^pot[u]^pot[v])
        return rows

    def fixed_and_aug(group_generators):
        fix={};aug={}
        for g in group_generators:
            rows=action_rows(g)
            cols=[0]*n
            for j,r in enumerate(rows):
                add_basis(fix,r^(1<<j))
                y=r
                while y:
                    b=y&-y;i=b.bit_length()-1;y^=b;cols[i]|=1<<j
            for i,c in enumerate(cols):add_basis(aug,c^(1<<i))
        return n-len(fix),n-len(aug),aug

    pfix,pcoin,paug=fixed_and_aug(gens)
    qfix,qcoin,qaug=fixed_and_aug(gens+[outer])

    # Reconstruct the exact Pass4713 deck cochain and put it in the same tree gauge.
    _,_,_,_,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    apartments=sorted(tuple(map(int,a)) for a in apartments);all40=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    flag_lifts=defaultdict(list)
    for ap in apartments:
        L=aline(ap);x=fib(ap);flag_lifts[(L,x)].append(ap)
    flags2=sorted(flag_lifts);assert flags2==flags
    aindex={a:i for i,a in enumerate(apartments)};findex={f:i for i,f in enumerate(flags)}
    lift_index={}
    for fi,f in enumerate(flags):
        for bit,ap in enumerate(sorted(flag_lifts[f])):lift_index[aindex[ap]]=(fi,bit)
    def aai(i,g):return aindex[tuple(sorted(g[x] for x in apartments[i]))]
    y=min(v for u,v in edges if u==0)
    lifts0=sorted(aindex[a] for a in flag_lifts[flags[0]]);liftsy=sorted(aindex[a] for a in flag_lifts[flags[y]])
    a0,ay=lifts0[0],liftsy[0]
    LE={tuple(sorted((aai(a0,g),aai(ay,g)))) for g in G}
    assert len(LE)==12960
    bybase=defaultdict(list)
    for a,b in LE:
        fa,ba=lift_index[a];fb,bb=lift_index[b];e=tuple(sorted((fa,fb)));bybase[e].append(ba^bb)
    alpha={e:next(iter(set(v))) for e,v in bybase.items() if len(v)==2 and len(set(v))==1}
    assert set(alpha)==eset
    pot=[0]*810
    for v in order[1:]:
        u=parent[v];pot[v]=pot[u]^alpha[tuple(sorted((u,v)))]
    deck=0
    for j,(u,v) in enumerate(cot):
        if alpha[(u,v)]^pot[u]^pot[v]:deck|=1<<j
    assert deck
    def apply(rows,x):
        y=0
        for j,r in enumerate(rows):
            if (r&x).bit_count()&1:y|=1<<j
        return y
    assert all(apply(action_rows(g),deck)==deck for g in gens+[outer])
    in_paug=reduce_basis(paug,deck)==0;in_qaug=reduce_basis(qaug,deck)==0

    out={'pass':4769,'module':{'field':'F2','dimension':n},
      'PSp':{'fixed_dimension_trivial_socle':pfix,'coinvariant_dimension_trivial_head':pcoin,'augmentation_dimension':n-pcoin,'deck_in_augmentation':in_paug},
      'PGSp':{'fixed_dimension_trivial_socle':qfix,'coinvariant_dimension_trivial_head':qcoin,'augmentation_dimension':n-qcoin,'deck_in_augmentation':in_qaug},
      'deck':{'tree_gauge_weight':deck.bit_count(),'nonzero':True,'PSp_fixed':True,'PGSp_fixed':True,
              'splits_as_trivial_direct_summand_under_PSp':not in_paug,
              'splits_as_trivial_direct_summand_under_PGSp':not in_qaug},
      'theorem':'Exact spanning-tree linear algebra computes the trivial head and socle dimensions of H^1(Gamma;F2). Membership of the invariant apartment deck vector in the augmentation subspace is the fail-closed splitting test: if it lies there, no invariant functional can retract H^1 onto the deck line.',
      'boundary':'This determines trivial head/socle data and the deck-line extension boundary, not the complete modular Loewy series or all simple composition factors.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
