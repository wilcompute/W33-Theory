#!/usr/bin/env python3
"""Pass 4797 — explicit cube-triality <-> F4/E6 GQ(4,2) crosswalk.

The source is the 45-point quotient of the 135 dependency cubes (Pass4782).
The target is the independently reconstructed F4-normalizer compiler quotient
of BT167/168.  NetworkX VF2 supplies an explicit point isomorphism; we then
verify that it maps all 27 maximal K5 lines and hence all 270 triangles.

BT169 already supplies an explicit GAP line-preserving crosswalk from the F4
quotient to the older W33 center-quad/E6 quotient.  Thus this pass fills the
missing first leg.  It does NOT identify either 51840 extension (central Sp vs
outer PGSp), and it does not revive the old tomotope=192 count identification.
"""
from __future__ import annotations
import hashlib,itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
from w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import quotient_adjacency,five_cliques

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4797_CUBE_F4_E6_CROSSWALK.json'

def cube_quotient():
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
    non=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]]
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
    _,G,F=build_groups(pts,pidx,lines);G=set(G)
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    def ac(i,g):return cidx[frozenset(ar(r,g) for r in cubes[i])]
    H=[g for g in G if ac(0,g)==0];assert len(H)==192
    fixed=[i for i in range(135) if all(ac(i,g)==i for g in H)];assert len(fixed)==3
    B0=frozenset(fixed)
    blocks=sorted({frozenset(ac(i,g) for i in B0) for g in G},key=lambda B:tuple(sorted(B)));assert len(blocks)==45
    cube_to_block={c:i for i,B in enumerate(blocks) for c in B}
    mult=Counter()
    for i,j in itertools.combinations(range(135),2):
        if (um[i]&um[j]).bit_count()==4:
            a,b=cube_to_block[i],cube_to_block[j]
            if a!=b:mult[tuple(sorted((a,b)))]+=1
    assert len(mult)==270 and set(mult.values())=={3}
    Q=nx.Graph();Q.add_nodes_from(range(45));Q.add_edges_from(mult)
    lines45=sorted((frozenset(C) for C in nx.find_cliques(Q)),key=lambda C:tuple(sorted(C)))
    assert len(lines45)==27 and {len(C) for C in lines45}=={5}
    triangles45=sorted({tuple(sorted(T)) for C in lines45 for T in itertools.combinations(C,3)})
    assert len(triangles45)==270
    return Q,lines45,triangles45

def main()->int:
    source,src_lines,src_triangles=cube_quotient()
    fad,_=quotient_adjacency();target=nx.Graph();target.add_nodes_from(range(45))
    target.add_edges_from((i,j) for i in range(45) for j in range(i+1,45) if fad[i][j])
    tgt_lines=sorted((frozenset(C) for C in five_cliques(fad)),key=lambda C:tuple(sorted(C)))
    assert len(tgt_lines)==27
    GM=nx.algorithms.isomorphism.GraphMatcher(source,target)
    mapping=next(GM.isomorphisms_iter(),None);assert mapping is not None and len(mapping)==45
    mp=[mapping[i] for i in range(45)]
    assert len(set(mp))==45
    assert all(source.has_edge(i,j)==target.has_edge(mp[i],mp[j]) for i in range(45) for j in range(i+1,45))
    mapped_lines={frozenset(mp[v] for v in C) for C in src_lines}
    assert mapped_lines==set(tgt_lines)
    tgt_triangles={tuple(sorted(T)) for C in tgt_lines for T in itertools.combinations(sorted(C),3)}
    mapped_triangles={tuple(sorted(mp[v] for v in T)) for T in src_triangles}
    assert len(tgt_triangles)==270 and mapped_triangles==tgt_triangles
    digest=hashlib.sha256(','.join(map(str,mp)).encode()).hexdigest()
    out={'pass':4797,
      'source':'Pass4782 dependency-cube W(D4)-triality 45 quotient',
      'target':'BT167/168 F4-normalizer compiler GQ(4,2) quotient',
      'point_count':45,'line_count':27,'triangle_count':270,
      'point_mapping_source_to_f4':mp,'mapping_sha256':digest,
      'adjacency_preserved':True,'all_27_K5_lines_preserved':True,'all_270_triangles_preserved':True,
      'existing_second_leg':'BT169 gives an explicit GAP line-preserving F4 quotient -> W33 center-quad/E6 quotient crosswalk',
      'theorem':'The dependency-cube triality quotient and the compiler F4-normalizer quotient are explicitly isomorphic as 45-point/27-line GQ(4,2) incidence geometries. The witness lifts to a bijection of all 270 triangle residues; composing with BT169 anchors the new triangle router to the older center-quad/E6 carrier.',
      'tomotope_boundary':'The bridge is through the F4/E6 GQ(4,2) quotient. The project already has a separate tomotope-H obstruction: the equality 192=|W(D4)|=tomotope flag count does not identify the tomotope with this cube stabilizer. No such identification is claimed.',
      'extension_boundary':'The 45-point quotient action forgets centers/outer sheets. This is not an identification of the central Sp(4,3) extension with the PGSp outer extension.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
