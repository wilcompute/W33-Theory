#!/usr/bin/env python3
"""Pass 4750 — residue dependency circuits versus the 1620 cold router edges.

Pass4742 found 540 weight-three dependencies on the 270 residue checks and showed
that their graph triangles partition all 1620 cold edges.  Here that statement is
made into an explicit binary chain complex

    F2^540 --d2--> F2^1620 --d1--> F2^270,

where d2 sends each free circuit generator to the three-edge boundary of its cold
triangle.  Since the 540 triangle supports are edge-disjoint, d2 has rank 540.
The resulting H1 dimension is computed exactly.

We also test the stronger tempting claim that d2 descends linearly from the actual
[270,240,3] dependency code.  It cannot: the 540 circuit words have linear
relations on residue coordinates, while their edge-disjoint boundary images are
independent.  This is an explicit chain-map no-go, not a count argument.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4750_RESIDUE_CIRCUIT_CHAIN_COMPLEX.json'

def gf2_rank_cols(cols):
    piv={}
    for x in cols:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def main():
    pts,pidx,lines,Astar,apartments,_apmasks,_H=geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(Astar[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270;rsets=[frozenset(x) for x in residues]
    cold=[];nbr=[set() for _ in range(270)]
    for a,b in itertools.combinations(range(270),2):
        if len(rsets[a]&rsets[b])==2:cold.append((a,b));nbr[a].add(b);nbr[b].add(a)
    assert len(cold)==1620 and set(map(len,nbr))=={12}
    eidx={e:i for i,e in enumerate(cold)}
    tris=[]
    for a in range(270):
        for b in sorted(x for x in nbr[a] if x>a):
            for c in sorted(x for x in (nbr[a]&nbr[b]) if x>b):
                T=(a,b,c)
                if len(rsets[a]|rsets[b]|rsets[c])==6:tris.append(T)
    assert len(tris)==540
    edge_use=Counter()
    for T in tris:
        for e in itertools.combinations(T,2):edge_use[tuple(sorted(e))]+=1
    assert len(edge_use)==1620 and set(edge_use.values())=={1}

    # circuit-coordinate columns in F2^270 and triangle-boundary columns in F2^1620
    Ccols=[];Bcols=[]
    for T in tris:
        cm=sum(1<<v for v in T);Ccols.append(cm)
        bm=0
        for e in itertools.combinations(T,2):bm|=1<<eidx[tuple(sorted(e))]
        Bcols.append(bm)
    rankC=gf2_rank_cols(Ccols);rankB=gf2_rank_cols(Bcols)
    assert rankB==540
    # d1 incidence rank for connected cold graph is 269; d1*d2=0 because every triangle has even degree at its vertices.
    d1cols=[(1<<u)|(1<<v) for u,v in cold];rankD1=gf2_rank_cols(d1cols);assert rankD1==269
    for T,bm in zip(tris,Bcols):
        parity=0
        x=bm
        while x:
            bit=x&-x;x^=bit;u,v=cold[bit.bit_length()-1];parity^=(1<<u)|(1<<v)
        assert parity==0
    h1=1620-rankD1-rankB;assert h1==811

    relations=540-rankC
    assert relations>0
    out={'pass':4750,
      'dependency_circuit_shell':{'vertices':270,'circuits':540,'circuit_word_span_rank':rankC,'linear_relations_among_540_circuit_words':relations},
      'cold_triangle_chain_complex':{'C2_dimension':540,'C1_dimension':1620,'C0_dimension':270,'rank_d2':rankB,'rank_d1':rankD1,'d1_d2_zero':True,'H1_dimension':h1,'triangle_boundaries_edge_disjoint':True},
      'descent_no_go':{'linear_map_from_span_of_dependency_circuit_words_sending_each_word_to_its_triangle_boundary_exists':False,
        'reason':f'the 540 residue circuit vectors have {relations} independent linear relations, whereas the 540 edge-boundary images are linearly independent'},
      'theorem':'The 540 minimum dependency circuits define an injective 2-boundary module inside the cold-router cycle space, yielding a canonical binary chain complex with H1 dimension 811. But this boundary assignment does not descend to a linear map from the dependency code itself; the relation spaces are incompatible.',
      'boundary':'Exact binary matroid/chain-complex theorem. The free circuit module is not identified with the [270,240,3] dependency code.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
