#!/usr/bin/env python3
"""Pass 4780 — the 135 dependency cubes carry literal D4 Weyl triality.

The stabilizer of one Pass4758 cube has order 192.  On the cube's six residue
vertices its image is S4 in the six-edge action of a tetrahedron; the pointwise
kernel is C2^3.  A complement of order 24 is found explicitly, certifying
H_cube = 2^3:S4 = W(D4).  The cube stabilizer fixes exactly a three-cube packet.
Its PSp packet normalizer extends W(D4) by C3 and its PGSp normalizer by S3,
giving a literal triality tower.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import perm_group

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4780_D4_CUBE_TRIALITY.json'

def orderp(p):
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
    non=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]!=0]
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
        assert len(V)==8
        R=set()
        for u in V:R.update(dep[u] if u<540 else non[u-540])
        assert len(R)==6;cubes.append(frozenset(R))
    assert len(cubes)==135;cidx={C:i for i,C in enumerate(cubes)}

    _,G,F=build_groups(pts,pidx,lines);assert (len(G),len(F))==(25920,51840)
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    def ac(i,g):return cidx[frozenset(ar(r,g) for r in cubes[i])]
    C0=cubes[0];H=[g for g in G if ac(0,g)==0];assert len(H)==192
    six=sorted(C0);pos={r:i for i,r in enumerate(six)}
    def p6(g):return tuple(pos[ar(r,g)] for r in six)
    im={p6(g) for g in H};ker=[g for g in H if p6(g)==tuple(range(6))]
    assert len(im)==24 and len(ker)==8
    assert Counter(orderp(p) for p in im)==Counter({2:9,3:8,4:6,1:1})
    assert Counter(orderp(g) for g in ker)==Counter({2:7,1:1})
    # The cold graph on the six vertices is the octahedron L(K4).
    ec=sum(1 for a,b in itertools.combinations(six,2) if b in cold[a]);assert ec==12

    # Find an actual S4 complement in H.
    comp=None;HL=list(H)
    for a in HL:
        if orderp(p6(a)) not in (3,4):continue
        for b in HL:
            if orderp(p6(b))!=2:continue
            qim=perm_group([p6(a),p6(b)],n=6,limit=25)
            if len(qim)!=24:continue
            K=perm_group([a,b],n=40,limit=193)
            if len(K)==24 and all(k not in ker or k==tuple(range(40)) for k in K):comp=K;break
        if comp is not None:break
    assert comp is not None

    fixed=[i for i in range(135) if all(ac(i,g)==i for g in H)];assert len(fixed)==3
    B=frozenset(fixed)
    stabP=[g for g in G if frozenset(ac(i,g) for i in B)==B]
    stabF=[g for g in F if frozenset(ac(i,g) for i in B)==B]
    assert (len(stabP),len(stabF))==(576,1152)
    bpos={x:i for i,x in enumerate(sorted(B))}
    def pb(g):return tuple(bpos[ac(x,g)] for x in sorted(B))
    imP={pb(g) for g in stabP};imF={pb(g) for g in stabF}
    assert len(imP)==3 and Counter(orderp(p) for p in imP)==Counter({3:2,1:1})
    assert len(imF)==6 and Counter(orderp(p) for p in imF)==Counter({2:3,3:2,1:1})
    assert {g for g in stabP if pb(g)==tuple(range(3))}==set(H)
    assert {g for g in stabF if pb(g)==tuple(range(3))}==set(H)

    out={'pass':4780,'cube':{'count':135,'residues_per_cube':6,'triangle_incidence_component':'Q3'},
      'cube_stabilizer':{'order':192,'six_residue_image_order':24,'image':'S4 on the six edges of a tetrahedron',
        'kernel_order':8,'kernel':'C2^3','split_complement_order':24,'structure':'2^3:S4 = W(D4)'},
      'triality_packet':{'cubes_fixed_by_WD4':3,'PSp_packet_stabilizer':576,'PSp_quotient':'C3',
        'PGSp_packet_stabilizer':1152,'PGSp_quotient':'S3'},
      'theorem':'A dependency cube has stabilizer W(D4)=2^3:S4. Three cubes form its canonical triality packet: PSp supplies the cyclic triality C3, while the outer PGSp coset completes it to S3.',
      'boundary':'Exact permutation-group theorem. The D4/triality labels refer to the certified Weyl-group structure, not a count analogy.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
