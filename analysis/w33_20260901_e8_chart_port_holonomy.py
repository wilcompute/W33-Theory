#!/usr/bin/env python3
"""Corrected port-gauge holonomy on the 27 E8 completion charts.

The 2026-09-01 completion theorem gives 45 selected D4+D4 packets and 27
five-packet completion charts.  A first attempt to import Pass4795's global
C3 orientation onto this carrier fails for a structural reason: in the native
polar-pair/sentinel degree-45 action, the PSp(4,3) stabilizer of a packet has
order 576 and induces the FULL S3 on the three completion charts through that
packet.  Thus there is no PSp-invariant cyclic orientation sheet on this
specific 45-set.

The correct compiler datum is the stronger one already familiar from the
port-matching lane: choose a full ordering of the three incident chart ports at
each packet.  Then every group element has a unique local S3 correction
sigma_g(p), and the corrections obey the exact nonabelian cocycle law

    sigma_{ab}(p) = sigma_a(b.p) o sigma_b(p).

After this gauge is fixed, each packet has 24 order-three global elements that
fix it and induce the chosen positive 3-cycle on its ports.  Deterministically
choosing one per packet yields local triality rotations.  Four of them, at
packet indices [0,9,11,33], generate the full order-25920 PSp action.

On the 27-chart overlap graph (135 edges), the 45 packet triangles have trivial
three-step holonomy.  A spanning tree leaves 109 fundamental cycles; after
transport to one base chart their holonomies generate exactly the full chart
stabilizer of order 960.

This is therefore a finite chart compiler with an S3^45 correction cocycle,
not a global C3 orientation compiler.  Pass4795's C3-oriented residue/cube
45-action is a different / outer-twisted degree-45 realization and is not
silently identified with this one.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path

import w33_20260829_216_clifford_torsor_nogo as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_E8_CHART_PORT_HOLONOMY.json'


def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))

def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)

def orderp(p): return base.porder(p)

def closure_pairs(gens):
    e45=tuple(range(45));e27=tuple(range(27));S={(e45,e27)};D=deque([(e45,e27)])
    while D:
        a,b=D.popleft()
        for g,h in gens:
            z=(compose(g,a),compose(h,b))
            if z not in S:S.add(z);D.append(z)
    return sorted(S)

def closure27(gens,limit=25920):
    e=tuple(range(27));S={e};D=deque([e])
    while D:
        a=D.popleft()
        for g in gens:
            z=compose(g,a)
            if z not in S:
                S.add(z);D.append(z)
                assert len(S)<=limit
    return S

def s3_comp(a,b): return tuple(a[b[i]] for i in range(3))

def build():
    pts,idx,_lines,N=base.geometry();supports,_=base.supports_from_N(N)
    adj=[set() for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):adj[i].add(j);adj[j].add(i)
    charts=[C for C in itertools.combinations(range(45),5)
            if all(v in adj[u] for u,v in itertools.combinations(C,2))]
    assert len(charts)==27
    cidx={frozenset(C):i for i,C in enumerate(charts)}
    incident={p:tuple(sorted(i for i,C in enumerate(charts) if p in C)) for p in range(45)}
    assert {len(v) for v in incident.values()}=={3}

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[tuple(si[frozenset(p[x] for x in S)] for S in supports) for p in gens40]
    chosen=(18,62,77,10)
    genpairs=[]
    for gi in chosen:
        g45=gens45[gi]
        g27=tuple(cidx[frozenset(g45[x] for x in C)] for C in charts)
        genpairs.append((g45,g27))
    G=closure_pairs(genpairs);assert len(G)==25920
    return supports,charts,incident,genpairs,G


def main():
    _supports,charts,incident,genpairs,G=build()
    ports={p:incident[p] for p in range(45)}

    def sigma(g45,g27,p):
        target=g45[p];pos={c:i for i,c in enumerate(ports[target])}
        return tuple(pos[g27[c]] for c in ports[p])

    # Native local image is S3, not C3.
    local_profiles=[]
    for p in range(45):
        H=[g for g in G if g[0][p]==p]
        assert len(H)==576
        image={sigma(g45,g27,p) for g45,g27 in H}
        kernel=[g for g in H if sigma(g[0],g[1],p)==(0,1,2)]
        assert len(image)==6 and len(kernel)==96
        local_profiles.append((len(H),len(image),len(kernel)))
    assert set(local_profiles)=={(576,6,96)}

    # Exact nonabelian cocycle check on all 4*25920*45 generator compositions.
    cocycle_checks=0
    for a45,a27 in genpairs:
        for b45,b27 in G:
            ab45,ab27=compose(a45,b45),compose(a27,b27)
            for p in range(45):
                lhs=sigma(ab45,ab27,p)
                rhs=s3_comp(sigma(a45,a27,b45[p]),sigma(b45,b27,p))
                assert lhs==rhs;cocycle_checks+=1
    assert cocycle_checks==4*25920*45

    cyc=(1,2,0)
    rotations=[];candidate_counts=[]
    for p in range(45):
        C=[g for g in G if g[0][p]==p and sigma(g[0],g[1],p)==cyc
           and orderp(g[0])==3 and orderp(g[1])==3]
        assert len(C)==24
        C=sorted(C);rotations.append(C[0]);candidate_counts.append(len(C))
    assert set(candidate_counts)=={24}

    # Four deterministic packet rotations generate all PSp on the charts.
    selected=[];H={tuple(range(27))};growth=[];packet_ids=[]
    for p,g in enumerate(rotations):
        trial=closure27(selected+[g[1]])
        if len(trial)>len(H):
            selected.append(g[1]);H=trial;packet_ids.append(p);growth.append(len(H))
        if len(H)==25920:break
    assert packet_ids==[0,9,11,33]
    assert growth==[3,9,288,25920]

    # Chart overlap graph.  Every adjacent pair shares one packet; each packet
    # gives one triangle of its three incident charts.
    edge_packet={}
    nbr=[set() for _ in range(27)]
    for a,b in itertools.combinations(range(27),2):
        common=set(charts[a])&set(charts[b])
        if common:
            assert len(common)==1
            p=next(iter(common));edge_packet[(a,b)]=p;nbr[a].add(b);nbr[b].add(a)
    assert len(edge_packet)==135 and {len(x) for x in nbr}=={10}
    for p in range(45):
        a,b,c=incident[p]
        r=rotations[p][1]
        assert r[a] in (b,c) and r[b] in (a,c) and r[c] in (a,b)
        assert compose(r,compose(r,r))==tuple(range(27))

    # Deterministic spanning tree rooted at chart 0, storing transport words as
    # actual group elements in the generated packet-rotation group.
    root=0;parent={root:None};transport={root:tuple(range(27))};tree_edges=set();D=deque([root])
    while D:
        u=D.popleft()
        for v in sorted(nbr[u]):
            if v in parent:continue
            p=edge_packet[tuple(sorted((u,v)))];r=rotations[p][1]
            rr=r
            if rr[u]!=v:
                rr=compose(r,r);assert rr[u]==v
            parent[v]=u;transport[v]=compose(rr,transport[u])
            tree_edges.add(tuple(sorted((u,v))));D.append(v)
    assert len(parent)==27 and len(tree_edges)==26

    cycles=[]
    for e,p in sorted(edge_packet.items()):
        if e in tree_edges:continue
        u,v=e;r=rotations[p][1]
        rr=r if r[u]==v else compose(r,r)
        assert rr[u]==v
        # base -> u -> v -> base
        h=compose(inv(transport[v]),compose(rr,transport[u]))
        assert h[root]==root
        cycles.append(h)
    assert len(cycles)==135-26==109
    profile=Counter(orderp(h) for h in cycles)
    assert profile==Counter({1:15,2:25,3:5,4:14,5:25,6:25})
    hol=closure27(cycles,limit=960);assert len(hol)==960
    chart_stab={g27 for _g45,g27 in G if g27[root]==root}
    assert len(chart_stab)==960 and hol==chart_stab

    # Full port gauge removes all local correction ambiguity: only identity has
    # zero correction at every packet.
    zero=[]
    for g45,g27 in G:
        if all(sigma(g45,g27,p)==(0,1,2) for p in range(45)):zero.append((g45,g27))
    assert len(zero)==1

    out={
      'schema':'w33.20260901.e8-chart-port-holonomy.v1','status':'PASS',
      'carrier':{'packets':45,'completionCharts':27,'chartOverlapEdges':135,
                 'incidentChartsPerPacket':3},
      'correctionToPriorOrientationRead':{
        'polarPairPacketActionLocalImage':'S3','packetStabilizerOrder':576,
        'localKernelOrder':96,'globalPSpCyclicOrientationSheet':False,
        'olderPass4795Carrier':'residue/cube degree-45 realization has C3 local image',
        'boundary':'the two degree-45 graph realizations are not silently identified as the same PSp G-set; an outer twist can preserve the graph while changing the inner action'},
      'portGauge':{
        'datum':'full ordering of the three incident completion-chart ports at every packet',
        'localCorrectionGroup':'S3^45','cocycleChecks':cocycle_checks,
        'nonabelianCocycleLaw':'sigma_ab(p)=sigma_a(b.p) o sigma_b(p)',
        'zeroCorrectionElements':1},
      'packetTriality':{
        'order3CandidatesPerPacket':24,'deterministicGeneratorPacketIds':packet_ids,
        'generatedGroupGrowth':growth,'generatedChartGroupOrder':25920},
      'holonomy':{
        'packetTriangles':45,'packetTriangleHolonomy':'identity',
        'spanningTreeEdges':26,'fundamentalCycles':109,
        'fundamentalCycleOrderProfile':{str(k):v for k,v in sorted(profile.items())},
        'baseChartHolonomyGroupOrder':len(hol),
        'baseChartStabilizerOrder':len(chart_stab),
        'holonomyEqualsFullChartStabilizer':True},
      'theorem':'After a full three-port gauge is fixed on the polar-pair packet carrier, local order-three packet rotations give an exact chart compiler: four deterministic rotations generate PSp(4,3), and the 109 fundamental cycle holonomies generate exactly the full order-960 stabilizer of a base completion chart. The correction data form an exact S3^45 nonabelian cocycle.',
      'boundary':'There is no global C3 orientation sheet on this native 45-action. The compiler is port-gauge dependent, and no optical or dynamical interpretation is asserted.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','localImage':'S3','cocycleChecks':cocycle_checks,
      'packetsGeneratingPSp':packet_ids,'holonomy':len(hol),'chartStabilizer':len(chart_stab)},sort_keys=True))

if __name__=='__main__':main()
