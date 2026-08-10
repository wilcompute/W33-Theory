#!/usr/bin/env python3
"""Pass 4624 -- the maximal-partial-spread packet 45 is the protected/E6 45.

Pass 4622 produced 45 packets of three maximal size-8 partial spreads having a
common order-192 stabilizer.  Pass 4585 independently produced 45 protected
16-line supports, and Pass 4616 identified those supports equivariantly with
the center-quad/E6-tritangent 45.

This pass supplies the missing support-level map.  For each packet, take the
union of its three 8-line spreads (24 lines) and complement inside the 40 W33
lines.  The result is exactly one Pass4585 protected 16-line support.  The map
is PSp-equivariant and bijective on all 45 objects.
"""
from __future__ import annotations
import itertools, json
from collections import defaultdict, deque
from pathlib import Path
import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, transvection_matrix, norm3,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
from w33_pass4595_concrete_d4_triality_w33_lifts import max_generators, partial8

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4624_PACKET45_SUPPORT_E6_INTERTWINER.json'

def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def pair_group(gens):
    I=(tuple(range(40)),tuple(range(40)));S={I};Q=deque([I])
    while Q:
        a,b=Q.popleft()
        for x,y in gens:
            z=(compose(x,a),compose(y,b))
            if z not in S:S.add(z);Q.append(z)
    return S

def point_perm(M,pts,pidx):
    out=[]
    for p in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(p,dtype=int))%3
        out.append(pidx[norm3(tuple(map(int,y)))])
    return tuple(out)

def pmask(mask,p):
    y=0
    for i in range(len(p)):
        if (mask>>i)&1:y|=1<<p[i]
    return y

def main()->int:
    pts,pidx,lines,lidx,Apoint,Astar,_,aps,_=build_geometry()
    Astar=np.asarray(Astar,dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i,k in itertools.combinations(range(40),2) if Astar[i,k]])
    V=set(span(B9));rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in {rep(v) for v in V} if x and q(x)==0)
    MG=max_generators(singular,rep,q,polar);assert len(MG)==270

    gens=[];G={(tuple(range(40)),tuple(range(40)))}
    for v in pts:
        M=transvection_matrix(v);gp=point_perm(M,pts,pidx);gl=build_line_perm(M,pts,pidx,lines,lidx)
        trial=pair_group(gens+[(gp,gl)])
        if len(trial)>len(G):gens.append((gp,gl));G=trial
        if len(G)==25920:break
    assert len(G)==25920
    actX=lambda X,g:frozenset(rep(pmask(x,g[1])) for x in X)
    rem=set(MG);orbits=[]
    while rem:
        X=next(iter(rem));O={actX(X,g) for g in G};orbits.append(O);rem-=O
    O135=[O for O in orbits if len(O)==135][0]
    X=min(O135,key=lambda z:tuple(sorted(z)));H=[g for g in G if actX(X,g)==X]
    assert len(H)==192

    P8=partial8(lines);assert len(P8)==1755
    unext=[]
    for S in P8:
        used=set().union(*(set(lines[i]) for i in S))
        if not any(used.isdisjoint(lines[k]) for k in range(40) if k not in S):unext.append(S)
    assert len(unext)==135
    actS=lambda S,g:tuple(sorted(g[1][i] for i in S))
    fixed=[S for S in unext if all(actS(S,g)==S for g in H)]
    assert len(fixed)==3 and len(set().union(*(set(S) for S in fixed)))==24
    U0=frozenset(set(range(40))-set().union(*(set(S) for S in fixed)))
    assert len(U0)==16

    # Independent Pass4585 support construction from apartment fibers.
    fibers=defaultdict(list)
    for ap in aps:
        x=0
        for i in ap:x^=cols[int(i)]
        fibers[rep(x)].append(tuple(map(int,ap)))
    support_to_s=defaultdict(list)
    for s,F in fibers.items():
        U=frozenset().union(*(set(ap) for ap in F));support_to_s[U].append(s)
    assert len(support_to_s)==45 and all(len(v)==3 for v in support_to_s.values())
    assert U0 in support_to_s

    actU=lambda U,g:frozenset(g[1][i] for i in U)
    support_orbit={actU(U0,g) for g in G}
    assert len(support_orbit)==45 and support_orbit==set(support_to_s)
    support_stab=[g for g in G if actU(U0,g)==U0]
    assert len(support_stab)==576
    # H is the common pointwise packet stabilizer; its normalizer/support stabilizer
    # is the 576 group from Pass4622.
    assert set(H).issubset(set(support_stab)) and len(support_stab)//len(H)==3

    old=json.loads((ROOT/'data/PART_W33_PASS4616_EXPLICIT_45_E6_INTERTWINER.json').read_text())
    assert old['equivariant_bijection_size']==45 and old['common_stabilizer_order']==576
    out={
      'pass':4624,
      'source':{'maximal_size8_partial_spreads':135,'spreads_per_packet':3,'packet_count':45,'common_H_order':192},
      'map':'packet {S1,S2,S3} -> complement in the 40 W33 lines of S1 union S2 union S3',
      'representative':{'union_size':24,'complement_size':16,'complement_is_Pass4585_support':True},
      'equivariance':{'PSp_order':25920,'support_orbit_size':45,'support_stabilizer_order':576,'H_index_in_support_stabilizer':3,'all_45_supports_hit':True},
      'composition_with_Pass4616':'45 packet complements = 45 protected supports = center-quad/E6-tritangent 45 by the frozen Pass4616 intertwiner',
      'theorem':'The Pass4622 stabilizer-packet quotient and Pass4585 protected-support quotient are the same PSp 45-carrier: the explicit equivariant map is the 16-line complement of the union of the packet three maximal 8-line partial spreads. Composing with Pass4616 identifies this carrier with the center-quad/E6-tritangent 45.',
      'boundary':'Exact finite support/G-set theorem only; E6 denotes the already certified cubic-surface carrier, not a physical field identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
