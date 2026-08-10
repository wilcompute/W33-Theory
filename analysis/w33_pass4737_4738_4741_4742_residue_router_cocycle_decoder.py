#!/usr/bin/env python3
"""Passes 4737, 4738, 4741, 4742: resolve the 270 involution residues much further.

4737  Compute the full PSp(4,3) orbital algebra on the 270 four-line residues.
      The action has rank 12, with subdegrees
        1,12,16,48,16,6,24,96,12,12,24,3.
      The share-two-lines orbital is connected of degree 12 and diameter FOUR
      (correcting the earlier exploratory diameter-3 note), with exact spectrum
        12^1, 8^15, 2^84, (-1)^64, (-4)^60, (-6)^6,
        (1+sqrt(13))^20, (1-sqrt(13))^20.
      The centralizer algebra has dimension 12 and center dimension 9, so over C
      the permutation module has nine inequivalent constituents, exactly one
      with multiplicity two.  Most importantly, the share-two-lines graph is
      PSp-equivariantly IDENTICAL to Pass 4716's cold selected270 router.  A
      degree-3 orbital gives its 27 Petersen hot fibers exactly.

4738  Replace the old 'two order-96 extensions differ' statement by an explicit
      normalizer-quotient twist.  For K=C_PSp(h), |K|=48, the residue stabilizer
      H is N_PSp(K), |H|=96, so H/K=C2 is the sheet character.  If t is an
      outer involution stabilizing a support-12 triangle and h is the outer
      order-4 root, then n=t^{-1}h is the NONTRIVIAL element of H/K:
        t^2=n^2=1, h=tn, nt=h^{-1}.
      Thus the two PGSp extensions differ by the unique normalizer twist.  The
      obstruction is a C2 torsor/normalizer class; no spurious H^2 claim is made.

4741  The 27 Petersen fibers are an exact optimal parity-check schedule: each
      contains ten pairwise-disjoint residues partitioning all forty lines, and
      all 270 residues are partitioned by the 27 fibers.  Since each W33 line
      occurs in 27 checks, depth >=27, hence the schedule is optimal.  The
      270 checks span rank 30, so no strict PSp-invariant proper check subset can
      replace them (the 270 checks are one orbit), while a non-equivariant basis
      needs only 30 checks.  The H10=[40,10,12] coset-leader census is exact
      through radius 6; at weight six exactly 18,480 syndrome classes are
      doubletons, one for each complementary 6+6 partition of the forty
      weight-12 H10 words, and there are no triple collisions.

4742  The dependency code on the 270 checks is [270,240,3].  Its complete
      minimum shell consists of 540 weight-3 dependencies.  Every dependency
      triple is three residue checks with pairwise two-line intersections and
      six-line union; the 540 triangles partition all 1,620 cold edges exactly
      once.  This is a binary-matroid circuit geometry with 270 points, 540
      3-circuits, six circuits through each point.  Tempting 540=540 is also
      falsified: its circuit-triangle stabilizer and the support/root-triangle
      stabilizer both have order 48 but different element-order censuses, hence
      they are not conjugate PSp subgroups and not the same G-set.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

from w33_pass4495_4502_distance_prism_reconstruction import (
    geometry, compose_perm, build_line_perm, perm_group, transvection3, J3,
)
from w33_pass4716_selected270_bundle_connection import build_bundle
from w33_pass4721_4724_support12_involution_square_root_cover import (
    build_groups, thickening, permute_mask, inverse_perm, fixed_mask,
    act_triangle, conjugate,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4737_4738_4741_4742_RESIDUE_ROUTER.json"


def gf2_basis(vals):
    piv = {}
    out = []
    for x in vals:
        y = int(x)
        while y:
            p = y.bit_length() - 1
            if p in piv:
                y ^= piv[p]
            else:
                piv[p] = y
                out.append(y)
                break
    return out


def order_perm(p):
    seen = set(); o = 1
    for i in range(len(p)):
        if i in seen: continue
        j = i; n = 0
        while j not in seen:
            seen.add(j); n += 1; j = p[j]
        o = math.lcm(o, n)
    return o


def mask_of(S):
    return sum(1 << i for i in S)


def main():
    pts,pidx,lines,Astar,apartments,_apmasks,_H = geometry()
    Astar = np.asarray(Astar,dtype=np.uint8)
    assert len(lines)==40 and len(apartments)==1620

    # Reconstruct the 270 minimum dual words independently from ker(A_*).
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(Astar[:,C],axis=1)&1):
            residues.append(tuple(C))
    assert len(residues)==270
    rsets=[frozenset(r) for r in residues]
    rmasks=[mask_of(r) for r in residues]
    ridx={r:i for i,r in enumerate(residues)}
    rmask_idx={m:i for i,m in enumerate(rmasks)}

    gens,inner,full=build_groups(pts,pidx,lines)
    ident=tuple(range(40))
    assert len(inner)==25920 and len(full)==51840
    def act_r(i,p): return ridx[tuple(sorted(p[x] for x in residues[i]))]

    # Unique four-fixed involution for every residue.
    four_inv={}
    invs=[]
    for p in inner:
        if p!=ident and compose_perm(p,p)==ident:
            invs.append(p); f=fixed_mask(p)
            if f.bit_count()==4: four_inv[f]=p
    assert len(invs)==315 and len(four_inv)==270
    assert set(four_inv)==set(rmasks)

    # ------------------------------------------------------------------ 4737
    H0=[p for p in inner if act_r(0,p)==0]
    assert len(H0)==96
    unseen=set(range(270)); orbits=[]
    while unseen:
        x=min(unseen); O={act_r(x,p) for p in H0}; orbits.append(sorted(O)); unseen-=O
    subdegrees=[len(O) for O in orbits]
    assert subdegrees==[1,12,16,48,16,6,24,96,12,12,24,3]
    orb_of={x:k for k,O in enumerate(orbits) for x in O}
    trans={}
    for p in inner:
        x=act_r(0,p)
        if x not in trans: trans[x]=p
    def rel(a,b):
        q=inverse_perm(trans[a]); return orb_of[act_r(b,q)]

    # Full orbital intersection tensor and its center.
    rank=len(orbits); P=np.zeros((rank,rank,rank),dtype=int)
    for k,O in enumerate(orbits):
        y=O[0]
        for z in range(270): P[rel(0,z),rel(z,y),k]+=1
    eq=[]
    for j in range(rank):
        for k in range(rank):
            eq.append([int(P[i,j,k]-P[j,i,k]) for i in range(rank)])
    center_dim=rank-sp.Matrix(eq).rank()
    assert center_dim==9
    noncomm=sum(not np.array_equal(P[i,j,:],P[j,i,:]) for i in range(rank) for j in range(i+1,rank))
    assert noncomm==39

    # Cold relation = residues sharing exactly two W33 lines.
    coldR=nx.Graph(); coldR.add_nodes_from(range(270))
    for a,b in itertools.combinations(range(270),2):
        if len(rsets[a]&rsets[b])==2: coldR.add_edge(a,b)
    assert set(dict(coldR.degree()).values())=={12} and nx.is_connected(coldR)
    dist=nx.single_source_shortest_path_length(coldR,0)
    ds=Counter(dist.values())
    assert ds==Counter({0:1,1:12,2:67,3:160,4:30})
    ev=np.linalg.eigvalsh(nx.to_numpy_array(coldR,dtype=float))
    ectr=Counter(round(float(x),8) for x in ev)
    target={12.0:1,8.0:15,2.0:84,-1.0:64,-4.0:60,-6.0:6,
            round(1+math.sqrt(13),8):20,round(1-math.sqrt(13),8):20}
    assert ectr==Counter(target)

    # Intrinsic hot relation: disjoint residues whose involution product is in
    # the 45-class fixing sixteen W33 lines.
    hotR=nx.Graph(); hotR.add_nodes_from(range(270))
    for a,b in itertools.combinations(range(270),2):
        if rsets[a]&rsets[b]: continue
        ga=four_inv[rmasks[a]]; gb=four_inv[rmasks[b]]
        z=compose_perm(ga,gb)
        if order_perm(z)==2 and fixed_mask(z).bit_count()==16:
            hotR.add_edge(a,b)
    assert set(dict(hotR.degree()).values())=={3}
    fibers=[frozenset(C) for C in nx.connected_components(hotR)]
    assert len(fibers)==27 and {len(C) for C in fibers}=={10}
    assert all(nx.is_isomorphic(hotR.subgraph(C),nx.petersen_graph()) for C in fibers)

    # Reconstruct Pass-4716 selected270 objects, then prove a PSp-equivariant
    # identification by equality of point stabilizers inside the SAME group.
    all40=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    rep=lambda x:min(int(x),int(x)^all40)
    def fib(ap):
        z=0
        for i in ap:z^=cols[i]
        return rep(z)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),
                             rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(ap) for ap in apartments}); assert len(selected)==270
    sidx={S:i for i,S in enumerate(selected)}
    def act_s(i,p):
        S=selected[i]
        T=tuple(sorted(rep(permute_mask(m,p)) for m in S))
        return sidx[T]
    Hs={p for p in inner if act_s(0,p)==0}; assert len(Hs)==96
    fixed_res=[i for i in range(270) if all(act_r(i,p)==i for p in Hs)]
    assert len(fixed_res)==1
    base_r=fixed_res[0]
    phi={}
    for p in inner:
        a=act_r(base_r,p); b=act_s(0,p)
        assert a not in phi or phi[a]==b
        phi[a]=b
    assert len(phi)==len(set(phi.values()))==270

    X=build_bundle(); coldS={tuple(sorted(e)) for e in X['cold']}; hotS={tuple(sorted(e)) for e in X['hot']}
    mapped_cold={tuple(sorted((phi[a],phi[b]))) for a,b in coldR.edges()}
    mapped_hot={tuple(sorted((phi[a],phi[b]))) for a,b in hotR.edges()}
    assert mapped_cold==coldS and mapped_hot==hotS

    # ------------------------------------------------------------------ 4738
    g=four_inv[rmasks[0]]
    roots=[p for p in full if p not in inner and compose_perm(p,p)==g]
    roots4=[p for p in roots if fixed_mask(p).bit_count()==4]
    assert len(roots)==8 and len(roots4)==2
    h=roots4[0]
    K={p for p in inner if compose_perm(p,h)==compose_perm(h,p)}
    Hres={p for p in inner if act_r(0,p)==0}
    assert len(K)==48 and len(Hres)==96 and K<Hres
    # Enumerate the normalizer exactly.
    Nrm={a for a in inner if {conjugate(a,k) for k in K}==K}
    assert Nrm==Hres

    # Reconstruct the two support-12 triangles above residue 0.
    th=[thickening(ap,lines) for ap in apartments]; tm=[mask_of(t) for t in th]
    nbr=[[] for _ in range(1620)]
    for i in range(1620):
        for j in range(i+1,1620):
            if not (tm[i]&tm[j]): nbr[i].append(j);nbr[j].append(i)
    comps=[];seen=set()
    for s in range(1620):
        if s in seen:continue
        C={s};Q=deque([s]);seen.add(s)
        while Q:
            u=Q.popleft()
            for v in nbr[u]:
                if v not in seen:seen.add(v);C.add(v);Q.append(v)
        comps.append(tuple(sorted(C)))
    cres=[]
    for C in comps:
        u=0
        for i in C:u|=tm[i]
        cres.append(all40^u)
    ci=[i for i,r in enumerate(cres) if r==rmasks[0]]; assert len(ci)==2
    tri=frozenset(tm[i] for i in comps[ci[0]])
    Tfull={p for p in full if act_triangle(tri,p)==tri}
    Cfull={p for p in full if compose_perm(p,h)==compose_perm(h,p)}
    assert len(Tfull)==len(Cfull)==96 and Tfull&Cfull==K and Tfull!=Cfull
    candidates=[]
    for t in Tfull-inner:
        n=compose_perm(inverse_perm(t),h)
        if order_perm(t)==2 and n in Hres and n not in K and order_perm(n)==2:
            if compose_perm(t,n)==h and compose_perm(n,t)==inverse_perm(h):
                candidates.append((t,n))
    assert candidates
    t,n=candidates[0]
    assert conjugate(n,h)==inverse_perm(h)

    # ------------------------------------------------------------------ 4741
    # The hot Petersen fibers are ten mutually disjoint 4-checks each.
    for C in fibers:
        assert all(not (rsets[a]&rsets[b]) for a,b in itertools.combinations(C,2))
        assert len(set().union(*(rsets[a] for a in C)))==40
    assert set().union(*fibers)==set(range(270))
    line_rep=Counter(i for r in residues for i in r); assert set(line_rep.values())=={27}
    assert len(gf2_basis(rmasks))==30

    # H10 rowspace and exact leader census through weight 6.
    Arows=[sum(int(Astar[i,j])<<j for j in range(40)) for i in range(40)]
    hb=gf2_basis(Arows); assert len(hb)==10
    hwords=[]
    for m in range(1<<10):
        x=0
        for i,b in enumerate(hb):
            if (m>>i)&1:x^=b
        hwords.append(x)
    hwe=Counter(x.bit_count() for x in hwords)
    assert hwe==Counter({0:1,12:40,16:135,20:672,24:135,28:40,40:1})
    w12=[x for x in hwords if x.bit_count()==12]
    # Weight-six collisions are exactly complementary halves of weight-12 words.
    edges=set()
    for c in w12:
        S=[i for i in range(40) if (c>>i)&1]
        for T in itertools.combinations(S,6):
            a=mask_of(T); b=c^a
            if a<b: edges.add((a,b))
    assert len(edges)==40*math.comb(12,6)//2==18480
    deg=Counter()
    for a,b in edges:deg[a]+=1;deg[b]+=1
    assert set(deg.values())=={1}  # no triple collision
    leaders={i:math.comb(40,i) for i in range(6)}
    leaders[6]=math.comb(40,6)-18480

    # ------------------------------------------------------------------ 4742
    dep3=[]
    for i,j in itertools.combinations(range(270),2):
        k=rmask_idx.get(rmasks[i]^rmasks[j])
        if k is not None and j<k:dep3.append((i,j,k))
    assert len(dep3)==540
    edge_use=Counter()
    for T in dep3:
        assert len(set().union(*(rsets[i] for i in T)))==6
        assert {len(rsets[a]&rsets[b]) for a,b in itertools.combinations(T,2)}=={2}
        for e in itertools.combinations(T,2):edge_use[tuple(sorted(e))]+=1
    assert set(edge_use)=={tuple(sorted(e)) for e in coldR.edges()}
    assert set(edge_use.values())=={1}
    dep_rank=270-len(gf2_basis(rmasks)); assert dep_rank==240
    T0=frozenset(dep3[0])
    Sdep={p for p in inner if frozenset(act_r(i,p) for i in T0)==T0}
    assert len(Sdep)==48
    dep_orders=Counter(order_perm(p) for p in Sdep)
    root_orders=Counter(order_perm(p) for p in K)
    assert dep_orders==Counter({1:1,2:19,3:8,4:12,6:8})
    assert root_orders==Counter({1:1,2:7,3:8,4:24,6:8})
    assert dep_orders!=root_orders

    out={
      'passes':[4737,4738,4741,4742],
      '4737_orbital_router':{
        'action_rank':12,'subdegrees':subdegrees,'orbital_algebra_center_dimension':center_dim,
        'noncommuting_unordered_orbital_pairs':noncomm,
        'cold_graph':{'degree':12,'edges':coldR.number_of_edges(),'diameter':4,
                      'distance_shell':[1,12,67,160,30],
                      'spectrum':{'12':1,'8':15,'2':84,'-1':64,'-4':60,'-6':6,
                                  '1+sqrt(13)':20,'1-sqrt(13)':20}},
        'hot_graph':{'degree':3,'edges':hotR.number_of_edges(),'components':27,
                     'component':'Petersen','vertices_per_component':10},
        'selected270_identification':{'PSp_equivariant':True,'cold_edges_match_exactly':True,
                                      'hot_edges_match_exactly':True,'stabilizers_equal':True},
      },
      '4738_normalizer_twist':{
        'K_order':48,'H_order':96,'normalizer_equals_residue_stabilizer':True,
        'quotient':'N_PSp(K)/K = C2','triangle_extension_order':96,'root_extension_order':96,
        'intersection_order':48,'explicit_relations':['t^2=1','n^2=1','h=t n','n t=h^{-1}'],
        'interpretation':'The PGSp extension mismatch is the unique nontrivial normalizer-quotient twist, not an asserted H^2 class.'
      },
      '4741_decoder':{
        'independent_check_rank':30,'redundant_checks':270,'strict_PSp_check_orbit':270,
        'optimal_rounds':27,'checks_per_round':10,'round_support_lines':40,
        'lower_bound_rounds':27,'PSp_equivariant_round_system':True,
        'H10':'[40,10,12]','leader_census_through_6':{str(k):v for k,v in leaders.items()},
        'weight6_doubleton_syndromes':18480,'weight6_triple_collisions':0,
      },
      '4742_dependency_topology':{
        'dependency_code':'[270,240,3]','minimum_words':540,'circuit_size':3,
        'circuits_through_each_check':6,'cold_edges_partitioned_once':1620,
        'circuit_triangle_stabilizer_order':48,'root_triangle_stabilizer_order':48,
        'circuit_stabilizer_order_census':dict(sorted(dep_orders.items())),
        'root_stabilizer_order_census':dict(sorted(root_orders.items())),
        'same_540_G_set':False,
      },
      'boundary':'All identifications above are exact finite/group/code statements.  The selected270 bridge is an explicit PSp-equivariant bijection, not a spectral/count inference.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
