#!/usr/bin/env python3
"""Pass 4795 — the 8/9 triangle chirality is a global GQ(4,2) orientation torsor.

Reconstruct the Pass4782 45-point quotient and its 27 maximal K5 lines.  The
PSp point stabilizer acts on the three K5s through a point as C3, while PGSp
acts as S3.  Hence a cyclic orientation chosen at one point propagates
well-definedly to all 45 points under PSp; there are exactly two opposite
choices and the outer coset reverses them.

For cross-line residue triangles sharing one quotient point, the non-cold
paired orbitals 8 and 9 are exactly distinguished by this local cyclic sign.
The cold orbital 1 occurs with both signs, so the orientation is the chirality
bit only after the full-aut-invariant cold sector is removed.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4795_TRIANGLE_CHIRALITY_ORIENTATION.json'

def inv(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def ordp(p):
    seen=set();o=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;n=0
        while j not in seen:seen.add(j);n+=1;j=p[j]
        o=math.lcm(o,n)
    return o

def main()->int:
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270
    ridx={r:i for i,r in enumerate(residues)};rm=[sum(1<<x for x in r) for r in residues]
    cold=[set() for _ in range(270)]
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold[i].add(j);cold[j].add(i)
    tris=[]
    for a in range(270):
        for b in (x for x in cold[a] if x>a):
            for c in cold[a]&cold[b]:
                if c>b:tris.append((a,b,c))
    dep=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]==0]
    non=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]]
    assert len(dep)==len(non)==540
    ed={tuple(sorted(e)):i for i,t in enumerate(dep) for e in itertools.combinations(t,2)}
    en={tuple(sorted(e)):i for i,t in enumerate(non) for e in itertools.combinations(t,2)}
    adj=[set() for _ in range(1080)]
    for e in ed:
        a=ed[e];b=540+en[e];adj[a].add(b);adj[b].add(a)
    cubes=[];seen=set()
    for s in range(1080):
        if s in seen:continue
        Q=[s];seen.add(s);V=[]
        while Q:
            u=Q.pop();V.append(u)
            for v in adj[u]:
                if v not in seen:seen.add(v);Q.append(v)
        R=set()
        for u in V:R.update(dep[u] if u<540 else non[u-540])
        assert len(V)==8 and len(R)==6;cubes.append(frozenset(R))
    assert len(cubes)==135;cidx={C:i for i,C in enumerate(cubes)}
    um=[]
    for C in cubes:
        u=0
        for r in C:u|=rm[r]
        assert u.bit_count()==8;um.append(u)

    _,G,F=build_groups(pts,pidx,lines);G=set(G);F=set(F);assert (len(G),len(F))==(25920,51840)
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    def ac(i,g):return cidx[frozenset(ar(r,g) for r in cubes[i])]
    Hc=[g for g in G if ac(0,g)==0];assert len(Hc)==192
    fixed=[i for i in range(135) if all(ac(i,g)==i for g in Hc)];assert len(fixed)==3
    B0=frozenset(fixed)
    blocks=sorted({frozenset(ac(i,g) for i in B0) for g in G},key=lambda B:tuple(sorted(B)));assert len(blocks)==45
    bidx={B:i for i,B in enumerate(blocks)};cube_to_block={c:i for i,B in enumerate(blocks) for c in B};assert len(cube_to_block)==135
    def ab(i,g):return bidx[frozenset(ac(c,g) for c in blocks[i])]

    # Quotient SRG.
    mult=Counter()
    for i,j in itertools.combinations(range(135),2):
        if (um[i]&um[j]).bit_count()==4:
            a,b=cube_to_block[i],cube_to_block[j]
            if a!=b:mult[tuple(sorted((a,b)))]+=1
    assert len(mult)==270 and set(mult.values())=={3}
    Q45=nx.Graph();Q45.add_nodes_from(range(45));Q45.add_edges_from(mult)
    A45=nx.to_numpy_array(Q45,nodelist=range(45),dtype=int)
    assert np.array_equal(A45@A45,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))
    K5=sorted((frozenset(C) for C in nx.find_cliques(Q45)),key=lambda C:tuple(sorted(C)))
    assert len(K5)==27 and {len(C) for C in K5}=={5}
    kidx={K:i for i,K in enumerate(K5)}
    def ak(k,g):return kidx[frozenset(ab(v,g) for v in K5[k])]
    incident={p:sorted(k for k,K in enumerate(K5) if p in K) for p in range(45)}
    assert {len(v) for v in incident.values()}=={3}

    # Local stabilizer images: C3 inside PSp, S3 in PGSp.
    base=0;base_lines=incident[base];pos={k:i for i,k in enumerate(base_lines)}
    HP=[g for g in G if ab(base,g)==base]
    HF=[g for g in F if ab(base,g)==base]
    assert (len(HP),len(HF))==(576,1152)
    p3=lambda g:tuple(pos[ak(k,g)] for k in base_lines)
    imP={p3(g) for g in HP};imF={p3(g) for g in HF}
    assert len(imP)==3 and Counter(ordp(p) for p in imP)==Counter({1:1,3:2})
    assert len(imF)==6 and Counter(ordp(p) for p in imF)==Counter({1:1,2:3,3:2})

    # Propagate a base cyclic order under PSp.  C3 local image makes this well-defined.
    trans={}
    for g in G:
        p=ab(base,g)
        if p not in trans:trans[p]=g
    assert len(trans)==45
    orient={}
    for p,g in trans.items():
        cyc=tuple(ak(k,g) for k in base_lines)
        orient[p]={(cyc[0],cyc[1]),(cyc[1],cyc[2]),(cyc[2],cyc[0])}
        assert set(cyc)==set(incident[p])
    # PSp preserves; every outer element reverses.
    for g in G:
        for p in range(45):
            image={(ak(a,g),ak(b,g)) for a,b in orient[p]}
            assert image==orient[ab(p,g)]
    outer=next(iter(F-G))
    for p in range(45):
        image={(ak(a,outer),ak(b,outer)) for a,b in orient[p]}
        target=orient[ab(p,outer)]
        assert image=={(b,a) for a,b in target}

    # Rebuild residue triangles and their unique supporting K5.
    rtri=[]
    for r in range(270):
        C=[i for i,U in enumerate(cubes) if r in U];assert len(C)==3
        T=tuple(sorted({cube_to_block[i] for i in C}));assert len(T)==3
        rtri.append(T)
    tri_to_k={tuple(sorted(T)):k for k,K in enumerate(K5) for T in itertools.combinations(sorted(K),3)}
    assert len(tri_to_k)==270
    rk=[tri_to_k[tuple(T)] for T in rtri]

    # PSp residue orbitals.
    H=[g for g in G if ar(0,g)==0];unseen=set(range(270));orbs=[]
    while unseen:
        x=min(unseen);O=sorted({ar(x,h) for h in H});orbs.append(O);unseen-=set(O)
    assert [len(O) for O in orbs]==[1,12,16,48,16,6,24,96,12,12,24,3]
    oi={x:k for k,O in enumerate(orbs) for x in O};rt={}
    for g in G:
        x=ar(0,g)
        if x not in rt:rt[x]=g
    def rel(a,b):return oi[ar(b,inv(rt[a]))]

    # Cross-K5 one-point pairs: orientation sign separates 8/9 after removing cold 1.
    by_rel=Counter()
    for i in range(270):
        Si=set(rtri[i])
        for j in range(270):
            if i==j or rk[i]==rk[j]:continue
            common=Si&set(rtri[j])
            if len(common)!=1:continue
            p=next(iter(common));sgn='+' if (rk[i],rk[j]) in orient[p] else '-'
            by_rel[(rel(i,j),sgn)]+=1
    assert set(k for k,s in by_rel)=={1,8,9}
    assert by_rel[(1,'+')]==by_rel[(1,'-')]==1620
    s8={s for (k,s),n in by_rel.items() if k==8 and n};s9={s for (k,s),n in by_rel.items() if k==9 and n}
    assert len(s8)==len(s9)==1 and s8!=s9
    assert sum(n for (k,s),n in by_rel.items() if k==8)==3240
    assert sum(n for (k,s),n in by_rel.items() if k==9)==3240

    out={'pass':4795,
      'quotient':'GQ(4,2) point graph / SRG(45,12,3,3)',
      'local_lines_through_point':3,
      'PSp_point_stabilizer':576,'PSp_local_image':'C3',
      'PGSp_point_stabilizer':1152,'PGSp_local_image':'S3',
      'orientation_torsor':{'global_choices':2,'PSp_preserves_each':True,'outer_reverses':True},
      'cross_line_triangle_pair_counts':{f'{k}:{s}':n for (k,s),n in sorted(by_rel.items())},
      'chiral_orbitals':{'8_sign':next(iter(s8)),'9_sign':next(iter(s9)),'cold_orbital_1_uses_both_signs':True},
      'theorem':'The paired residue orbitals 8 and 9 carry a literal global orientation bit. PSp preserves either of two cyclic orientations of the three GQ lines through every quotient point; the outer coset reverses it. Among non-cold cross-line triangle pairs, the two orientation signs are exactly orbitals 8 and 9.',
      'boundary':'The orientation bit does not by itself distinguish cold orbital 1 from the chiral union: cold pairs occur equally in both local signs. Thus the full router needs the independent cold selector plus this orientation torsor; no H^2 claim is made.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
