#!/usr/bin/env python3
"""Correct the failed 27x8 guess: 216 hemisystem lines are Schlaefli edges.

The earlier signed-five-minima audit found 16 projective hemisystem sums above
each of the 27 orthogonal five-frames, not 8, and each hemisystem line appeared
above two frames.  This script resolves that obstruction exactly:

    27 * 16 / 2 = 216.

The 27 frames have intersection graph GQ(2,4), SRG(27,10,1,5).  Its complement
is the Schlaefli graph SRG(27,16,10,8).  We prove that the two owner frames of
each hemisystem line are *exactly* one Schlaefli edge, giving a PSp(4,3)-
equivariant bijection

    {216 hemisystem eigenlines}  <-->  E(Schlaefli).

We also construct the older repo H27/Schlaefli graph on Heisenberg coordinates
(u,z), find an explicit graph isomorphism to the 27-frame carrier, and freeze
the coordinate map.
"""
from __future__ import annotations

import itertools
import json
from collections import defaultdict, deque, Counter
from pathlib import Path

import w33_20260828_trade_lattice_minimum_gq45 as trade
import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260831_hemisystem_eigenframe_576 as hemi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260831_HEMISYSTEM_SCHLAFLI_EDGE_BIJECTION.json'
ALL=frozenset(range(40))


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def neg(v): return tuple(-x for x in v)
def canon_vec(v):
    i=next(k for k,x in enumerate(v) if x)
    return tuple(v) if v[i]>0 else neg(v)
def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))
def transform_vec(p,v):
    w=[0]*len(v)
    for i,z in enumerate(v):w[p[i]]=z
    return tuple(w)

def srg(G):
    deg={len(x) for x in G}; la=set(); mu=set()
    for i,j in itertools.combinations(range(len(G)),2):
        c=len(G[i]&G[j]); (la if j in G[i] else mu).add(c)
    return [len(G),sorted(deg),sorted(la),sorted(mu)]

def canon_pair(T):
    C=ALL-T;a,b=tuple(sorted(T)),tuple(sorted(C))
    return (a,b) if a<b else (b,a)


def find_isomorphism(A,B):
    n=len(A); assert len(B)==n
    # Fix vertex 0 -> 0; both graphs are vertex-transitive, so no generality lost.
    mp={0:0}; used={0}
    def candidates(v):
        out=[]
        for w in range(n):
            if w in used: continue
            ok=True
            for x,y in mp.items():
                if ((x in A[v]) != (y in B[w])): ok=False;break
            if ok: out.append(w)
        return out
    def rec():
        if len(mp)==n:return True
        unm=[v for v in range(n) if v not in mp]
        scored=[]
        for v in unm:
            c=candidates(v); scored.append((len(c),v,c))
        _,v,cand=min(scored,key=lambda x:(x[0],x[1]))
        for w in cand:
            mp[v]=w;used.add(w)
            if rec():return True
            used.remove(w);del mp[v]
        return False
    assert rec()
    return tuple(mp[i] for i in range(n))


def h27_schlafli():
    F=[(a,b) for a in range(3) for b in range(3)]
    V=[(u,z) for u in F for z in range(3)]
    ix={x:i for i,x in enumerate(V)}
    def det(u,v): return (u[0]*v[1]-u[1]*v[0])%3
    def coc(u,v): return (-det(u,v))%3
    H=[set() for _ in V]
    for i,(u,z) in enumerate(V):
        for v in F:
            if v==(0,0):continue
            up=((u[0]+v[0])%3,(u[1]+v[1])%3)
            zp=(z+coc(u,v))%3
            j=ix[(up,zp)];H[i].add(j)
    assert all(len(x)==8 for x in H)
    # Complete 9-partite graph minus H27.
    S=[set() for _ in V]
    for i,(u,z) in enumerate(V):
        for j,(v,t) in enumerate(V):
            if i!=j and u!=v and j not in H[i]:S[i].add(j)
    assert srg(S)==[27,[16],[10],[8]]
    return V,H,S


def main():
    pts,idx,lines=trade.geometry()
    N=[[0]*40 for _ in range(40)]
    for l,L in enumerate(lines):
        for p in L:N[l][p]=1
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]
    sig=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        z=tuple(sum(cols[p][l] for p in S) for l in range(40));sig[z].append(S)
    pairs=sorted(tuple(sorted((tuple(v[0]),tuple(v[1])))) for v in sig.values() if len(v)==2)
    assert len(pairs)==45
    mins=[]
    for a,b in pairs:
        v=tuple(1 if i in b else -1 if i in a else 0 for i in range(40));assert dot(v,v)==8
        mins.append(v)
    Orth=[set() for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if dot(mins[i],mins[j])==0:Orth[i].add(j);Orth[j].add(i)
    frames=set()
    def rec(pre,cand):
        if len(pre)==5:frames.add(tuple(pre));return
        for i in sorted(cand):rec(pre+[i],{j for j in cand if j>i and j in Orth[i]})
    rec([],set(range(45)));frames=sorted(frames);assert len(frames)==27
    findex={frozenset(C):i for i,C in enumerate(frames)}

    BG=[set() for _ in range(27)]
    for i,j in itertools.combinations(range(27),2):
        if set(frames[i])&set(frames[j]):BG[i].add(j);BG[j].add(i)
    assert srg(BG)==[27,[10],[1],[5]]
    SG=[set(range(27))-{i}-BG[i] for i in range(27)]
    assert srg(SG)==[27,[16],[10],[8]]
    sg_edges={tuple((i,j)) for i in range(27) for j in SG[i] if i<j};assert len(sg_edges)==216

    # Signed sums and *unique frame ownership* (global sign quotient handled by set).
    owners=defaultdict(set); local=[set() for _ in range(27)]
    for fi,C in enumerate(frames):
        for mask in range(32):
            coeff=[-1 if (mask>>j)&1 else 1 for j in range(5)]
            v=tuple(sum(coeff[j]*mins[C[j]][k] for j in range(5)) for k in range(40))
            if all(abs(x)==1 for x in v):
                z=canon_vec(v);local[fi].add(z);owners[z].add(fi)
    assert {len(x) for x in local}=={16}
    assert Counter(len(x) for x in owners.values())==Counter({2:216})
    owner_edges={tuple(sorted(x)) for x in owners.values()}
    assert owner_edges==sg_edges

    # Independent 432 two-ovoid orbit -> 216 projective eigenlines.
    gens=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*base.form(x,v)%3
                y=base.norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idx[y])
            gens.append(tuple(p))
    gg=[gens[i] for i in (18,62,77,10)];G=base.closure(gg,40);assert len(G)==25920
    orbit={frozenset(g[x] for x in hemi.T0) for g in G};assert len(orbit)==432
    hlines={canon_vec(tuple(1 if i in T else -1 for i in range(40))) for T in orbit};assert len(hlines)==216
    assert set(owners)==hlines

    # Equivariance under a generating set: action on minima -> frames, and on
    # hemisystem vectors -> owner Schlaefli edges.
    min_index={canon_vec(v):i for i,v in enumerate(mins)}
    def act_min(g,i):return min_index[canon_vec(transform_vec(g,mins[i]))]
    def act_frame(g,fi):return findex[frozenset(act_min(g,i) for i in frames[fi])]
    for g in gg:
        for z,oo in owners.items():
            gz=canon_vec(transform_vec(g,z))
            assert owners[gz]=={act_frame(g,i) for i in oo}

    # Stabilizer arithmetic becomes structural, not numerical coincidence.
    V0=0
    Hv=[g for g in G if act_frame(g,V0)==V0];assert len(Hv)==960
    e0=min(sg_edges)
    He=[g for g in G if {act_frame(g,e0[0]),act_frame(g,e0[1])}==set(e0)];assert len(He)==120
    z0=next(z for z,o in owners.items() if tuple(sorted(o))==e0)
    Hz=[g for g in G if canon_vec(transform_vec(g,z0))==z0];assert len(Hz)==120
    assert set(He)==set(Hz)

    # Explicit isomorphism to the repo's older H27/Schlaefli coordinate graph.
    HV,H27,HS=h27_schlafli()
    iso=find_isomorphism(SG,HS)
    assert all(((j in SG[i])==(iso[j] in HS[iso[i]])) for i in range(27) for j in range(27))
    coord_map={str(i):[list(HV[iso[i]][0]),HV[iso[i]][1]] for i in range(27)}

    out={
      'schema':'w33.20260831.hemisystem-schlafli-edge-bijection.v1','status':'PASS',
      'base':{'frames':27,'GQ24Graph':[27,10,1,5],'SchlafliGraph':[27,16,10,8],
              'SchlafliEdges':216,'frameStabilizerOrder':960},
      'hemisystem':{'projectiveLines':216,'validLinesPerFrame':16,'ownerFramesPerLine':2,
                    'ownerPairsExactlySchlafliEdges':True,'lineStabilizerOrder':120,
                    'edgeStabilizerEqualsLineStabilizer':True},
      'equivariant':{'testedGenerators':4,'ownerMapEquivariant':True},
      'H27CoordinateBridge':{'explicitGraphIsomorphism':True,'frameToHeisenbergCoordinate':coord_map,
        'H27Degree':8,'SchlafliDegree':16,'packetStructure':'9 base u values x 3 central z values'},
      'correctedIdentity':'216 = 27*16/2: hemisystem eigenlines are edges of the 27-vertex Schlaefli graph, not an 8-sheeted bundle over its vertices.',
      'theorem':'The 216 projective W33 hemisystem eigenlines are PSp(4,3)-equivariantly identical to the 216 edges of the Schlaefli graph on the 27 orthogonal five-frames. The vertex stabilizer has order 960 and the edge/hemisystem-line stabilizer has order 120. An explicit isomorphism identifies this 27-carrier with the older H27/Schlaefli Heisenberg coordinates.',
      'boundary':'Exact finite-geometry identification. The H27 coordinate bridge is graph-theoretic/equivariant at the PSp generating action level; it does not identify a hemisystem line with a physical qutrit gate.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','identity':'216=27*16/2','owners':2,'vertexStab':960,
      'edgeStab':120,'H27Iso':True},sort_keys=True))

if __name__=='__main__':main()
