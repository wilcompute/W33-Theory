#!/usr/bin/env python3
"""Passes 4997-4999: shared-line holography, canonical support-eight
cocircuits, and the 270-octahedron edge frame.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,gf2_rank_int,gf2_rank_matrix

O97=ROOT/'data/PART_W33_PASS4997_SHARED_LINE_HOLOGRAPHY.json'
O98=ROOT/'data/PART_W33_PASS4998_CANONICAL_SUPPORT8_COCIRCUITS.json'
O99=ROOT/'data/PART_W33_PASS4999_OCTAHEDRAL_EDGE_FRAME.json'

def bits(indices):
    m=0
    for i in indices:m|=1<<int(i)
    return m

def main()->int:
    b=build_base();H=b['H36'];E=b['E'];ei=b['ei'];Q=b['Q'];spreads=b['spreads'];iso=b['iso_ds_sp']
    tri_masks=b['tri_masks'];residual=b['residual'];pair_to_res=b['pair_to_res'];T=b['tritangents'];M=b['M'];G27=b['G27']

    # --------------------------------------------------------------- Pass4997
    edge_line=[]
    for a,c in E:
        z=spreads[iso[a]]&spreads[iso[c]]
        assert len(z)==1;edge_line.append(next(iter(z)))
    def project(mask):
        out=0;x=mask
        while x:
            lb=x&-x;k=lb.bit_length()-1;out^=1<<edge_line[k];x^=lb
        return out
    tri_img=[project(m) for m in tri_masks]
    assert len(set(tri_img))==1080 and {m.bit_count() for m in tri_img}=={3}
    tri_centers=Counter();tri_ind=True
    for m in tri_img:
        V=[i for i in range(40) if m>>i&1]
        tri_ind &= all(not Q.has_edge(*e) for e in itertools.combinations(V,2))
        tri_centers[sum(all(Q.has_edge(c,v) for v in V) for c in range(40) if c not in V)]+=1
    assert tri_ind and tri_centers==Counter({0:1080})

    sq_img=[project(m) for m,V in residual]
    sq_mult=Counter(sq_img)
    assert len(sq_mult)==270 and Counter(sq_mult.values())==Counter({3:270}) and {m.bit_count() for m in sq_mult}=={4}
    sq_ind=True
    for m in sq_mult:
        V=[i for i in range(40) if m>>i&1]
        sq_ind &= all(not Q.has_edge(*e) for e in itertools.combinations(V,2))
    assert sq_ind
    overlap4=Counter()
    for i,j in itertools.combinations(range(36),2):
        z=spreads[i]&spreads[j]
        if len(z)==4:overlap4[bits(z)]+=1
    assert len(overlap4)==270 and set(overlap4)==set(sq_mult) and Counter(overlap4.values())==Counter({1:270})

    AQ=nx.to_numpy_array(Q,nodelist=range(40),dtype=np.uint8)
    rankQ=gf2_rank_matrix(AQ);rtri=gf2_rank_int(tri_img);rsq=gf2_rank_int(sq_mult.keys())
    assert (rankQ,rtri,rsq)==(10,40,30)
    for m in sq_mult:
        v=np.array([(m>>i)&1 for i in range(40)],dtype=np.uint8)
        assert not np.any((AQ@v)%2)
    out97={
      'pass':4997,'map':'each H36 edge -> the unique W33 line shared by its two one-overlap spreads',
      'triangle_image':{'source_sigma_even_A3':1080,'distinct_images':1080,'weight':3,
        'Q43_independent':True,'common_center_census':{'0':1080},'span_rank_F2':40,
        'identification':'exactly the 1080 zero-center independent Q(4,3) triads'},
      'residual_square_image':{'source_residual_A4':810,'distinct_images':270,'multiplicity_per_image':3,'weight':4,
        'Q43_independent':True,'span_rank_F2':30,
        'identification':'exactly the 270 size-four intersections of W33 spread pairs with overlap four'},
      'Q43_binary_adjacency_code':{'length':40,'dimension':10,'square_image_equals_orthogonal_complement':True},
      'induced_quotient':{'source':'triangle boundary span / square boundary span','source_dimension':30,
        'target':'F2^40 / square-image span = dual functional space of the [40,10,12] Q43 adjacency code',
        'target_dimension':10,'surjective':True,'kernel_dimension':20},
      'theorem':'The shared-line projection sends the 1080 sigma-even H36 triangle checks bijectively to the zero-center independent triads of Q(4,3), and sends the 810 residual squares three-to-one onto the 270 four-line intersections of overlap-4 W33 spread pairs. The residual-square image is exactly the 30-dimensional orthogonal complement of the Q43 binary adjacency code, inducing a canonical 30 -> 10 quotient with 20-dimensional kernel.',
      'boundary':'The 20-dimensional kernel and 10-dimensional quotient are exact binary carriers; no identification with unrelated real irreducibles is made here.'}
    O97.write_text(json.dumps(out97,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass4998
    AT=nx.Graph();AT.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
    star=[frozenset(j for j,t in enumerate(T) if x in t) for x in range(27)]
    assert {len(s) for s in star}=={5}
    support8=set()
    for a,c in G27.edges():
        assert len(star[a]&star[c])==1
        s=star[a]^star[c];assert len(s)==8
        Hs=AT.subgraph(s)
        assert sorted(len(cc) for cc in nx.connected_components(Hs))==[4,4]
        assert all(AT.subgraph(cc).number_of_edges()==6 for cc in nx.connected_components(Hs))
        support8.add(frozenset(s))
    assert len(support8)==135
    K4=set()
    for clique in nx.find_cliques(AT):
        if len(clique)>=4:
            for q in itertools.combinations(clique,4):K4.add(frozenset(q))
    assert len(K4)==135
    paired=set()
    K4s=sorted(K4,key=lambda s:tuple(sorted(s)))
    for i,j in itertools.combinations(range(len(K4s)),2):
        A,B=K4s[i],K4s[j]
        if A&B:continue
        if any(AT.has_edge(a,c) for a in A for c in B):continue
        paired.add(A|B)
    assert len(paired)==135 and paired==support8
    out98={
      'pass':4998,'tritangent_intersection_graph':'srg(45,12,3,3)','K4_subgraphs':135,
      'canonical_minimum_family':{'size':135,'support_size':8,
        'indexing':'135 intersecting pairs of cubic-surface lines',
        'support_geometry':'2 K4: two disjoint tritangent K4s with no cross edges',
        'equivalent_description':'symmetric difference of the two five-tritangent stars through an intersecting cubic-line pair'},
      'exhaustion_inside_mean_zero_V20':{'all_disjoint_nonadjacent_K4_pairs':135,'equal_to_star_difference_family':True,
        'reason':'a support-eight eigenvalue-3 vector at the minimum bound must split as two four-vertex components; the only connected four-vertex graph with eigenvalue3 is K4'},
      'theorem':'The 135 cubic-line star differences are not merely examples of minimum eight-sensor failures: they are exactly the pure-tritangent mean-zero support-eight cocircuits. Each support induces 2K4 in the tritangent SRG, and every pair of nonadjacent disjoint K4s arises this way.',
      'boundary':'This exhausts the pure V20/tritangent minimum family. Mixed line+tritangent support-eight cocircuits, if any, are not classified here.'}
    O98.write_text(json.dumps(out98,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass4999
    O=np.zeros((270,360),dtype=np.uint8)
    for r,(bp,items) in enumerate(sorted(pair_to_res.items())):
        m=0
        for q,V in items:m^=q
        assert m.bit_count()==12
        x=m
        while x:
            lb=x&-x;O[r,lb.bit_length()-1]=1;x^=lb
    assert set(map(int,O.sum(1)))=={12} and set(map(int,O.sum(0)))=={9}
    rankR=int(np.linalg.matrix_rank(O.astype(float)));rank2=gf2_rank_matrix(O);assert (rankR,rank2)==(120,90)
    Gram=O@O.T
    off=Counter(int(Gram[i,j]) for i,j in itertools.combinations(range(270),2));assert off==Counter({0:31995,3:4320})
    eig=np.linalg.eigvalsh(Gram.astype(float));spec=Counter()
    for x in eig:
        z=int(round(float(x)));assert abs(float(x)-z)<1e-7;spec[z]+=1
    assert spec==Counter({0:150,18:84,36:15,54:20,108:1})
    X=nx.Graph();X.add_nodes_from(range(270))
    for i,j in itertools.combinations(range(270),2):
        if Gram[i,j]==3:X.add_edge(i,j)
    assert set(dict(X.degree()).values())=={32}
    cn=Counter((X.has_edge(i,j),len(set(X.neighbors(i))&set(X.neighbors(j)))) for i,j in itertools.combinations(range(270),2))
    assert cn==Counter({(False,4):21060,(False,0):10125,(False,8):810,(True,10):4320})
    out99={
      'pass':4999,'incidence':'270 tritangent-pair octahedra x 360 H36 edges','shape':[270,360],
      'row_weight':12,'column_weight':9,'real_rank':120,'GF2_rank':90,
      'pair_intersections':{'share_0_edges':31995,'share_3_edges':4320},
      'squared_singular_spectrum':{'108':1,'54':20,'36':15,'18':84,'0':150},
      'share3_graph':{'vertices':270,'degree':32,'edges':4320,
        'common_neighbor_profile':{'adjacent_10':4320,'nonadjacent_0':10125,'nonadjacent_4':21060,'nonadjacent_8':810},
        'strongly_regular':False},
      'theorem':'The 270 octahedra form a highly structured edge-measurement frame on the 360 H36 coordinates: every octahedron uses12 edges, every edge lies in9 octahedra, the real incidence rank is120 and binary rank90, and the nonzero squared singular values are 108^1,54^20,36^15,18^84. Two octahedra share either zero or three H36 edges.',
      'boundary':'The ranks120 and90 coincide with other project carrier dimensions, but no cross-carrier intertwiner is inferred from dimension alone.'}
    O99.write_text(json.dumps(out99,indent=2,sort_keys=True)+'\n')
    return 0

if __name__=='__main__':raise SystemExit(main())
