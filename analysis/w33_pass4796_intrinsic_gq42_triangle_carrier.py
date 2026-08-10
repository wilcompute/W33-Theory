#!/usr/bin/env python3
"""Pass 4796 — reconstruct the 270 triangle carrier from GQ(4,2) alone.

This script deliberately imports no W33 geometry.  It builds Q^-(5,2), takes its
45 totally singular lines as vertices of the GQ(4,2) point graph, and recovers
the 270 residue-sized objects as *all graph triangles*.  The 27 maximal K5s give
the 27 ten-triangle Petersen fibers.  The triangle hypergraph is lossless: its
45 coordinate-stars and original SRG are reconstructed from co-occurrence.

The full PSp orbital router needs one of the two global orientation choices from
Pass4795; that is an index-two decoration, not a return to the 40 W33 lines.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4796_INTRINSIC_GQ42_TRIANGLE_CARRIER.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1
def bits(x):return tuple((x>>i)&1 for i in range(6))
def rank_mod(M,p):
    A=[[int(x)%p for x in row] for row in M];r=0
    if not A:return 0
    for c in range(len(A[0])):
        s=next((i for i in range(r,len(A)) if A[i][c]),None)
        if s is None:continue
        A[r],A[s]=A[s],A[r];z=pow(A[r][c],-1,p);A[r]=[(z*x)%p for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]:
                z=A[i][c];A[i]=[(a-z*b)%p for a,b in zip(A[i],A[r])]
        r+=1
        if r==len(A):break
    return r

def main()->int:
    qpts=[x for x in range(1,64) if Qm(bits(x))==0];assert len(qpts)==27
    qlines=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qpts,2) if (a^b) in qpts});assert len(qlines)==45
    G=nx.Graph();G.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if set(qlines[i])&set(qlines[j]):G.add_edge(i,j)
    A=nx.to_numpy_array(G,nodelist=range(45),dtype=int)
    assert set(dict(G.degree()).values())=={12}
    assert np.array_equal(A@A,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))

    K5=sorted((frozenset(C) for C in nx.find_cliques(G)),key=lambda C:tuple(sorted(C)))
    assert len(K5)==27 and {len(C) for C in K5}=={5}
    assert Counter(v for C in K5 for v in C)==Counter({v:3 for v in range(45)})
    # Each graph edge lies on exactly one K5.
    assert Counter(tuple(sorted(e)) for C in K5 for e in itertools.combinations(C,2))==Counter({tuple(sorted(e)):1 for e in G.edges()})

    triangles=sorted({tuple(sorted(T)) for C in K5 for T in itertools.combinations(C,3)})
    assert len(triangles)==270
    graph_triangles={tuple(sorted(C)) for C in nx.enumerate_all_cliques(G) if len(C)==3}
    assert set(triangles)==graph_triangles
    tindex={T:i for i,T in enumerate(triangles)}
    supportK={tindex[T]:k for k,C in enumerate(K5) for T in itertools.combinations(sorted(C),3)}
    assert len(supportK)==270

    # Complement-duad model on each K5: C(5,3) <-> C(5,2).
    duad={i:tuple(sorted(K5[supportK[i]]-set(T))) for i,T in enumerate(triangles)}
    assert all(len(d)==2 for d in duad.values())
    assert len({(supportK[i],duad[i]) for i in range(270)})==270

    # Hot relation is intrinsic: same K5, triangle intersection exactly one.
    H=nx.Graph();H.add_nodes_from(range(270))
    for k,C in enumerate(K5):
        R=[i for i in range(270) if supportK[i]==k]
        assert len(R)==10
        for i,j in itertools.combinations(R,2):
            if len(set(triangles[i])&set(triangles[j]))==1:H.add_edge(i,j)
        assert nx.is_isomorphic(H.subgraph(R),nx.petersen_graph())
    assert H.number_of_edges()==405
    assert sorted(len(C) for C in nx.connected_components(H))==[10]*27

    # Lossless triangle lift: point stars are the 45 incidence rows of size 18.
    stars=[frozenset(i for i,T in enumerate(triangles) if v in T) for v in range(45)]
    assert len(set(stars))==45 and {len(S) for S in stars}=={18}
    # Two original vertices occur together in 3 triangle rows iff they were adjacent.
    rec=nx.Graph();rec.add_nodes_from(range(45))
    co=Counter()
    for T in triangles:
        for e in itertools.combinations(T,2):co[tuple(sorted(e))]+=1
    assert set(co.values())=={3} and set(co)=={tuple(sorted(e)) for e in G.edges()}
    rec.add_edges_from(co)
    assert nx.is_isomorphic(rec,G)

    incidence=np.zeros((45,270),dtype=np.uint8)
    for j,T in enumerate(triangles):incidence[list(T),j]=1
    ranks={str(p):rank_mod(incidence.tolist(),p) for p in (2,3,5)}

    out={'pass':4796,'base_model':'Q^-(5,2) / GQ(4,2)','quotient_points':45,'maximal_K5_lines':27,
      'lines_through_each_point':3,'triangles':270,'triangles_per_K5':10,'triangles_through_each_point':18,
      'triangle_to_complement_duad_bijection':True,
      'hot_relation':{'components':27,'component_graph':'Petersen','edges':405},
      'triangle_incidence_ranks':ranks,
      'lossless_reconstruction':{'45_point_stars_recovered':True,'SRG_edges_recovered_by_triangle_cooccurrence_3':True},
      'theorem':'The 270-object carrier and all 27 hot Petersen fibers are intrinsic to GQ(4,2): the objects are exactly the 270 graph triangles, equivalently the complement duads inside the 27 maximal K5 lines. The triangle hypergraph recovers the original 45-point SRG exactly.',
      'boundary':'The unoriented SRG determines the carrier and hot relation but not the PSp 8-versus-9 chirality label. The latter requires choosing one of the two global orientation sheets of Pass4795. No 40-line W33 coordinates are needed for this intrinsic reconstruction.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
