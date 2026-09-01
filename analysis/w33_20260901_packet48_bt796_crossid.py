#!/usr/bin/env python3
"""Cross-identify the new 45x48 packet/K3,3 flag shell with BT796's 2160 slots.

The packet-globalization certificate leaves a smallest packet-stabilizer orbit
of size 48 on the 360 Schlaefli K3,3 witnesses.  Hence the corresponding flag
relation has 45*48 = 2160 elements and pair stabilizer order 12.  BT796 already
owns a transitive 2160-element PSp(4,3) G-set: (skew W33-line pair, common
isotropic transversal), also with stabilizer order 12.

This script does the objectwise test that the shared count alone cannot do:
  * build both 2160 G-sets under the same four deterministic PSp generators;
  * compute the stabilizer of one packet-48 flag;
  * find a BT796 slot fixed by that exact subgroup;
  * propagate it equivariantly and verify a 2160-point bijection;
  * compare stabilizer element-order profiles and transfer BT796's canonical
    transversal-line label onto the packet-48 flags.

If the fixed slot exists and the propagated map is bijective, the two
transitive G-sets are isomorphic, not merely equinumerous.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

import networkx as nx

import w33_20260829_216_clifford_torsor_nogo as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_20260901_PACKET48_BT796_CROSSID.json'


def comp(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def porder(p):
    seen=set(); out=1
    for i in range(len(p)):
        if i in seen: continue
        j=i; n=0
        while j not in seen:
            seen.add(j); n+=1; j=p[j]
        out=math.lcm(out,n)
    return out


def closure_triple(g40, g45, g27):
    I=(tuple(range(40)),tuple(range(45)),tuple(range(27)))
    G={I}; D=deque([I])
    while D:
        a,b,c=D.popleft()
        for x,y,z in zip(g40,g45,g27):
            h=(comp(x,a),comp(y,b),comp(z,c))
            if h not in G:
                G.add(h);D.append(h)
    assert len(G)==25920
    return list(G)


def build():
    pts,idx,wlines,N=base.geometry(); supports,_=base.supports_from_N(N)
    si={S:i for i,S in enumerate(supports)}
    li={frozenset(L):i for i,L in enumerate(wlines)}

    # GQ(2,4) charts on the 45 packet/octets.
    padj=[set() for _ in range(45)]
    for a,b in itertools.combinations(range(45),2):
        if supports[a].isdisjoint(supports[b]):
            padj[a].add(b);padj[b].add(a)
    charts=sorted(tuple(sorted(C)) for C in itertools.combinations(range(45),5)
                  if all(v in padj[u] for u,v in itertools.combinations(C,2)))
    assert len(charts)==27
    cidx={frozenset(C):i for i,C in enumerate(charts)}
    CG=nx.Graph();CG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if set(charts[a])&set(charts[b]):CG.add_edge(a,b)
    K33=[]
    for S in itertools.combinations(range(27),6):
        H=CG.subgraph(S)
        if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
            A,B=nx.algorithms.bipartite.sets(H)
            if len(A)==len(B)==3:K33.append(frozenset(S))
    assert len(K33)==360
    kidx={K:i for i,K in enumerate(K33)}

    # Same deterministic four generators as the obstruction/packet certificates.
    all40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for q in pts:
                z=alpha*base.form(q,v)%3
                y=base.norm(tuple((q[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            all40.append(tuple(p))
    chosen=(18,62,77,10)
    g40=[all40[i] for i in chosen]
    g45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in g40]
    g27=[tuple(cidx[frozenset(p[x] for x in C)] for C in charts) for p in g45]
    G=closure_triple(g40,g45,g27)

    # Induced line action of the same group.
    def line_perm(p):
        return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    gl=[line_perm(p) for p in g40]
    line_of={a:line_perm(a) for a,_b,_c in G}

    # Packet-0 stabilizer orbit of size 48 on K33 witnesses.
    incident=[frozenset(i for i,C in enumerate(charts) if p in C) for p in range(45)]
    H576=[z for z in G if z[1][0]==0];assert len(H576)==576
    def actK(pc,K):return kidx[frozenset(pc[x] for x in K)]
    unseen=set(range(360));orbs=[]
    while unseen:
        k=min(unseen); O={actK(pc,K33[k]) for _p40,_p45,pc in H576}
        unseen-=O;orbs.append(sorted(O))
    O48=next(O for O in orbs if len(O)==48)
    assert all(len(incident[0]&K33[k])==0 for k in O48)
    newbase=(0,O48[0])

    # Full 2160 packet-48 flag orbit.
    newflags=set()
    for _p40,p45,p27 in G:
        newflags.add((p45[newbase[0]],actK(p27,K33[newbase[1]])))
    assert len(newflags)==2160
    nf=sorted(newflags); nfi={x:i for i,x in enumerate(nf)}

    # BT796 slots = (skew W33-line pair, one of four common transversals).
    line_sets=[set(L) for L in wlines]
    skew=[(i,j) for i,j in itertools.combinations(range(40),2) if not (line_sets[i]&line_sets[j])]
    skidx={frozenset(x):i for i,x in enumerate(skew)}
    trans=[]
    for a,b in skew:
        tv=tuple(k for k in range(40) if k not in (a,b) and line_sets[k]&line_sets[a] and line_sets[k]&line_sets[b])
        assert len(tv)==4;trans.append(tv)
    slots=[(s,t) for s,tv in enumerate(trans) for t in tv]
    assert len(slots)==2160
    sli={x:i for i,x in enumerate(slots)}

    def act_slot(lp,slot):
        s,t=slot;a,b=skew[s]
        return (skidx[frozenset((lp[a],lp[b]))],lp[t])

    # Exact stabilizer of the packet-48 base flag, represented on W33 lines.
    Hnew=[]
    for p40,p45,p27 in G:
        if p45[newbase[0]]==newbase[0] and actK(p27,K33[newbase[1]])==newbase[1]:
            Hnew.append(line_of[p40])
    assert len(Hnew)==12
    newprof={str(k):v for k,v in sorted(Counter(porder(x) for x in Hnew).items())}

    # Find BT796 slots fixed by the *same subgroup*.  Any such slot has exactly
    # Hnew as stabilizer because all BT796 slot stabilizers have order 12.
    fixed=[slot for slot in slots if all(act_slot(lp,slot)==slot for lp in Hnew)]
    assert fixed
    oldbase=fixed[0]
    Hold=[]
    for p40,_p45,_p27 in G:
        lp=line_of[p40]
        if act_slot(lp,oldbase)==oldbase:Hold.append(lp)
    assert set(Hold)==set(Hnew) and len(Hold)==12
    oldprof={str(k):v for k,v in sorted(Counter(porder(x) for x in Hold).items())}

    # Propagate the base match equivariantly. Hnew-fixity guarantees well-definedness.
    equiv={}
    for p40,p45,p27 in G:
        x=(p45[newbase[0]],actK(p27,K33[newbase[1]]))
        y=act_slot(line_of[p40],oldbase)
        if x in equiv: assert equiv[x]==y
        else: equiv[x]=y
    assert len(equiv)==2160 and len(set(equiv.values()))==2160

    # Transfer BT796's canonical transversal line to the new flags.
    mult=Counter(y[1] for y in equiv.values())
    assert Counter(mult.values())=={54:40}
    support_line_intersections=Counter()
    k33_line_relation=Counter()
    for (p,k),(_s,t) in equiv.items():
        support_line_intersections[len(set(wlines[t])&set(supports[p]))]+=1
        # How often does the transferred line occur as a W33 line-coordinate of
        # the six completion charts in the K33 witness? Charts themselves are
        # packet factorizations, so record the only canonical point-level test:
        # membership of the four line points in the union of their 5 octets.
        union=set().union(*(supports[q] for c in K33[k] for q in charts[c]))
        k33_line_relation[len(set(wlines[t])&union)]+=1

    return dict(pts=pts,wlines=wlines,supports=supports,charts=charts,K33=K33,
                g40=g40,g45=g45,g27=g27,G=G,nf=nf,newbase=newbase,slots=slots,
                equiv=equiv,newprof=newprof,oldprof=oldprof,fixed=fixed,
                support_hist=support_line_intersections,k33_line_hist=k33_line_relation)


def main():
    D=build()
    out={
      'schema':'w33.20260901.packet48-bt796-crossid.v1','status':'PASS',
      'packet48FlagCount':2160,'bt796SlotCount':2160,'groupOrder':25920,
      'pairStabilizerOrder':12,
      'packet48StabilizerOrderProfile':D['newprof'],
      'bt796MatchedSlotStabilizerOrderProfile':D['oldprof'],
      'bt796SlotsFixedByPacket48BaseStabilizer':len(D['fixed']),
      'explicitEquivariantBijectionVerified':True,
      'transversalLineMultiplicityProfile':{'54':40},
      'packetSupportVsTransferredLineIntersectionHistogram':{str(k):v for k,v in sorted(D['support_hist'].items())},
      'k33ChartUnionVsTransferredLineIntersectionHistogram':{str(k):v for k,v in sorted(D['k33_line_hist'].items())},
      'theorem':('The 45x48 smallest packet/K3,3 flag relation and BT796\'s 540x4 chart-transversal slots are isomorphic as PSp(4,3)-sets. The proof is objectwise: the exact order-12 stabilizer of a packet-48 flag fixes a BT796 slot, and propagating that match under all 25,920 group elements gives a well-defined bijection of all 2,160 objects.'),
      'boundary':('This is an isomorphism of finite PSp(4,3) G-sets. The transferred transversal label is canonical only after the explicit base-slot match; no optical, spacetime, or dynamical interpretation is asserted.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','fixedSlots':len(D['fixed']),'profile':D['newprof'],
                      'supportHist':out['packetSupportVsTransferredLineIntersectionHistogram']},sort_keys=True))

if __name__=='__main__':main()
