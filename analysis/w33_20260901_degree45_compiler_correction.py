#!/usr/bin/env python3
"""Supersede two stale 2026-09-01 compiler/orientation readings.

1. On the native 45-point GQ(4,2) carrier the PSp point stabilizer has order
   576 and its image on the three incident K5 lines is S3, not C3.  The U4(2)
   table of marks has a unique index-45 action (checked by the companion GAP
   witness), so the older Pass4795 C3 local-image statement cannot describe a
   second transitive PSp 45-set.  It is retracted rather than outer-twisted.

2. Do not choose the lexicographically first local rotation at every packet.
   Build a generating set from the full local rotation pool, prune it to an
   irredundant basis, compute exact shortest words, then choose the shortest
   positive local rotation at each packet.  Those choices are used for the
   chart-loop holonomy test.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter,deque
from pathlib import Path

import w33_20260901_e8_chart_port_holonomy as old

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_DEGREE45_COMPILER_CORRECTION.json'


def closure(gens,limit=25920):
    e=tuple(range(27));S={e};D=deque([e])
    while D:
        a=D.popleft()
        for g in gens:
            z=old.compose(g,a)
            if z not in S:
                S.add(z);D.append(z)
                assert len(S)<=limit
    return S


def pinv(p):return old.inv(p)


def main():
    _supports,charts,incident,genpairs,G=old.build();assert len(G)==25920
    ports={p:incident[p] for p in range(45)}
    def sigma(g45,g27,p):
        target=g45[p];pos={c:i for i,c in enumerate(ports[target])}
        return tuple(pos[g27[c]] for c in ports[p])

    # The local image is S3 on every packet.
    profiles=[]
    for p in range(45):
        H=[g for g in G if g[0][p]==p];assert len(H)==576
        im={sigma(a,b,p) for a,b in H}
        ker=[g for g in H if sigma(g[0],g[1],p)==(0,1,2)]
        profiles.append((len(im),len(ker)))
    assert set(profiles)=={(6,96)}

    cyc=(1,2,0);candidates={}
    for p in range(45):
        C=[g for g in G if g[0][p]==p and sigma(g[0],g[1],p)==cyc
           and old.orderp(g[0])==3 and old.orderp(g[1])==3]
        C=sorted(C);assert len(C)==24;candidates[p]=C

    # Deterministically accumulate local rotations until they generate PSp.
    # Scan packet-major / permutation-major and add a rotation exactly when it
    # increases the generated subgroup.  Then prune redundant gates.
    selected=[];H={tuple(range(27))};growth=[];selected_packets=[]
    for p in range(45):
        for g in candidates[p]:
            if g[1] in H:continue
            trial=closure(selected+[g[1]])
            if len(trial)>len(H):
                selected.append(g[1]);selected_packets.append(p);H=trial;growth.append(len(H))
            if len(H)==25920:break
        if len(H)==25920:break
    assert len(H)==25920

    changed=True
    while changed:
        changed=False
        for i in range(len(selected)-1,-1,-1):
            trial=selected[:i]+selected[i+1:]
            if trial and len(closure(trial))==25920:
                del selected[i];del selected_packets[i];changed=True;break
    assert len(closure(selected))==25920

    # Exact BFS shortest words in the symmetric generating alphabet.
    alphabet=[]
    for i,g in enumerate(selected):
        alphabet.append((f'g{i}',g));alphabet.append((f'g{i}^-1',pinv(g)))
    e=tuple(range(27));dist={e:0};word={e:()};D=deque([e])
    while D:
        a=D.popleft()
        for label,g in alphabet:
            z=old.compose(g,a)
            if z not in dist:
                dist[z]=dist[a]+1;word[z]=word[a]+(label,);D.append(z)
    assert len(dist)==25920
    diameter=max(dist.values());mean=sum(dist.values())/len(dist)
    hist=Counter(dist.values())

    # Choose the shortest positive rotation at each packet; retain paired 45
    # action by looking it up in the already-enumerated group.
    by27={b:(a,b) for a,b in G};assert len(by27)==25920
    rotations=[];rotlens=[]
    for p in range(45):
        best=min(candidates[p],key=lambda g:(dist[g[1]],g[1],g[0]))
        rotations.append(best);rotlens.append(dist[best[1]])

    # Chart overlap graph and exact loop holonomy with the shortest rotations.
    edge_packet={};nbr=[set() for _ in range(27)]
    for a,b in itertools.combinations(range(27),2):
        common=set(charts[a])&set(charts[b])
        if common:
            assert len(common)==1;p=next(iter(common));edge_packet[(a,b)]=p
            nbr[a].add(b);nbr[b].add(a)
    assert len(edge_packet)==135 and {len(x) for x in nbr}=={10}
    root=0;parent={root:None};transport={root:e};tree=set();D=deque([root])
    while D:
        u=D.popleft()
        for v in sorted(nbr[u]):
            if v in parent:continue
            p=edge_packet[tuple(sorted((u,v)))];r=rotations[p][1]
            rr=r if r[u]==v else old.compose(r,r)
            assert rr[u]==v
            parent[v]=u;transport[v]=old.compose(rr,transport[u]);tree.add(tuple(sorted((u,v))));D.append(v)
    assert len(tree)==26
    cycles=[]
    for e0,p in sorted(edge_packet.items()):
        if e0 in tree:continue
        u,v=e0;r=rotations[p][1];rr=r if r[u]==v else old.compose(r,r);assert rr[u]==v
        h=old.compose(pinv(transport[v]),old.compose(rr,transport[u]));assert h[root]==root
        cycles.append(h)
    assert len(cycles)==109
    hol=closure(cycles,limit=960)
    chartstab={b for _a,b in G if b[root]==root};assert len(chartstab)==960
    assert hol==chartstab
    holprof=Counter(old.orderp(h) for h in cycles)

    # shortest words among base-chart stabilizer elements
    stabdist=[dist[g] for g in chartstab];loopdiam=max(stabdist);loopmean=sum(stabdist)/len(stabdist)

    out={
      'schema':'w33.20260901.degree45-compiler-correction.v1','status':'PASS',
      'orientationCorrection':{
        'nativePSpPacketStabilizerOrder':576,'localImage':'S3','localKernelOrder':96,
        'oldPass4795Claim':'PSp local image C3 and a global two-sheet cyclic orientation torsor',
        'oldPass4795ClaimRetracted':True,
        'reason':'The companion Table-of-Marks witness proves U4(2) has a unique index-45 action; the exact native action has S3 local image, so C3 cannot be a second transitive degree-45 PSp G-set.'},
      'compiler':{
        'candidatePositiveRotationsPerPacket':24,
        'initialIncreasingGateCount':len(growth),'initialGrowth':growth,
        'irredundantGateCount':len(selected),'gatePackets':selected_packets,
        'generatedGroupOrder':len(closure(selected)),
        'symmetricAlphabetSize':len(alphabet),
        'CayleyDiameter':diameter,'CayleyMeanDistance':mean,
        'distanceHistogram':{str(k):v for k,v in sorted(hist.items())},
        'shortestPositiveRotationLengthHistogram':{str(k):v for k,v in sorted(Counter(rotlens).items())},
        'baseChartShortestWordDiameter':loopdiam,'baseChartMeanShortestWord':loopmean},
      'holonomy':{
        'fundamentalCycles':109,'orderProfile':{str(k):v for k,v in sorted(holprof.items())},
        'generatedHolonomyOrder':len(hol),'baseChartStabilizerOrder':len(chartstab),
        'equalsFullChartStabilizer':True},
      'theorem':'A full S3 port gauge plus shortest positive packet rotations gives an exact finite compiler. The chosen local rotations generate all PSp(4,3), and the 109 fundamental chart loops generate exactly the order-960 base-chart stabilizer.',
      'boundary':'This supersedes the stale C3-sheet and lexicographic-gate readings. It is finite permutation-group compilation, not an optical/hardware gate count.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','localImage':'S3','gates':len(selected),'diameter':diameter,
      'shortestRotations':dict(sorted(Counter(rotlens).items())),'holonomy':len(hol),
      'holProfile':dict(sorted(holprof.items()))},sort_keys=True))

if __name__=='__main__':main()
