#!/usr/bin/env python3
"""Passes 4992-4995: octahedral shell algebra, exact reader erasure distance,
residual C3 affine gauge, and the residual-square chain complex.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

from analysis.w33_pass4992_4999_common import build_base,build_group,gf2_rank_int,gf2_rank_matrix

ROOT=Path(__file__).resolve().parents[1]
O92=ROOT/'data/PART_W33_PASS4992_OCTAHEDRAL_SHELL_RADIUS_CORRELATIONS.json'
O93=ROOT/'data/PART_W33_PASS4993_EXACT_85_READER_ERASURE_DISTANCE.json'
O94=ROOT/'data/PART_W33_PASS4994_RESIDUAL_C3_AFFINE_GAUGE.json'
O95=ROOT/'data/PART_W33_PASS4995_OCTAHEDRAL_EQUATOR_CHAIN_COMPLEX.json'

def main()->int:
    b=build_base();H=b['H36'];E=b['E'];ei=b['ei'];M=b['M'];T=b['tritangents'];DS=b['DS']
    sigma=b['sigma'];steiner=b['steiner'];tri_masks=b['tri_masks'];pair_to_res=b['pair_to_res']

    # ------------------------------------------------------------------ Pass4992
    even_global=set();odd_global=set();odd_mult=Counter();a6=[];a9=[];a8=[];a12=[]
    oct_records=[]
    for bp,items in pair_to_res.items():
        a,bb=bp;U=[d for d in range(36) if M[a,d]==M[bb,d]==0]
        even=[];odd=[]
        for t in itertools.combinations(U,3):
            if not all(H.has_edge(*e) for e in itertools.combinations(t,2)):continue
            idx=[ei[tuple(sorted(e))] for e in itertools.combinations(t,2)]
            m=sum(1<<k for k in idx);par=sum(int(sigma[k]) for k in idx)&1
            if par==0:even.append(m);even_global.add(m)
            else:odd.append(m);odd_global.add(tuple(sorted(t)));odd_mult[tuple(sorted(t))]+=1
        eq=[m for m,_V in items]
        assert (len(even),len(odd),len(eq))==(4,4,3)
        assert all((x&y)==0 for x,y in itertools.combinations(even,2))
        assert all((x&y)==0 for x,y in itertools.combinations(odd,2))
        assert all((x&y)==0 for x,y in itertools.combinations(eq,2))
        z4=0;zodd=0;z3=0
        for x in even:z4^=x
        for x in odd:zodd^=x
        for x in eq:z3^=x
        assert z4==zodd==z3 and z4.bit_count()==12
        for x,y in itertools.combinations(even,2):a6.append(x^y)
        for C3 in itertools.combinations(even,3):
            z=0
            for x in C3:z^=x
            a9.append(z)
        for x,y in itertools.combinations(eq,2):a8.append(x^y)
        a12.append(z4);oct_records.append((even,eq,z4))
    assert len(even_global)==1080 and len(odd_global)==120
    assert set(odd_mult.values())=={9}
    assert (len(set(a6)),len(set(a9)),len(set(a8)),len(set(a12)))==(1620,1080,810,270)
    assert {x.bit_count() for x in a6}=={6} and {x.bit_count() for x in a9}=={9}
    assert {x.bit_count() for x in a8}=={8} and {x.bit_count() for x in a12}=={12}
    # delta=173 third-moment consequence: T3 <= -704, hence at most 188 positive A3 signs.
    # In an octahedron product p is negative only when the number of positive triangle signs is odd,
    # so at most 188 of the 270 octahedra can have p=-1.  This forces U12>=-106.  For the three
    # equator signs, product p gives minimum local sum -1 when p=+ and -3 when p=-, hence U4>=-646.
    out92={
      'pass':4992,'octahedra':270,
      'local_partitions':{'sigma_even_A3_faces':4,'sigma_odd_Steiner_faces':4,'residual_A4_equators':3,
        'all_three_partitions_cover_same_edges':12,
        'character_identity':'product_{4 even A3 faces} chi = product_{3 A4 equators} chi = chi(all12)'},
      'global_incidence':{'A3_even_unique':1080,'A3_even_oct_multiplicity':1,'Steiner_odd_unique':120,
        'Steiner_odd_oct_multiplicity':9,'A4_residual_unique':810,'A4_residual_oct_multiplicity':1},
      'octahedral_subshells':{'weight6_from_even_face_pairs':1620,'weight9_from_even_face_triples':1080,
        'weight8_from_equator_pairs':810,'weight12_full_octahedra':270,'all_words_distinct_within_each_reported_subshell':True},
      'local_character_algebra':{
        'triangle':'for r=sum(t_i), p=product(t_i): e2=(r^2-4)/2 and e3=p*r',
        'equator':'for s=sum(q_j), p=product(q_j): pair_sum=p*s',
        'shared_top_character':'p=product(t_1..t_4)=product(q_1..q_3)'},
      'delta173_consequence':{'third_moment_forces_T3_at_most':-704,'positive_A3_signs_at_most':188,
        'negative_oct_product_count_at_most':188,'restricted_weight12_sum_U12_at_least':-106,
        'residual_A4_equator_sum_U4_at_least':-646},
      'covering_radius':{'proved_interval':[134,173],'improved_here':False},
      'theorem':'The 270 tritangent-pair octahedra give a non-radial 4-triangle/3-equator shell algebra. Every octahedron has four edge-disjoint sigma-even A3 faces and three edge-disjoint residual A4 equators covering the same 12 edges, so their character products agree. The 1080 A3 checks are partitioned exactly once by the octahedra. For a hypothetical distance-173 coset the third-moment bound forces at most188 positive A3 signs, which in turn forces the octahedral weight-12 character sum to be at least -106 and the residual-equator A4 sum to be at least -646.',
      'boundary':'These are exact subshell constraints, but they do not yet control the complementary A4/A6/A8/A9/A12 shells strongly enough to improve the universal covering-radius upper bound 173.'}
    O92.write_text(json.dumps(out92,indent=2,sort_keys=True)+'\n')

    # ------------------------------------------------------------------ Pass4993
    G27=b['G27'];AT=nx.Graph();AT.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
    assert set(dict(AT.degree()).values())=={12}
    AAT=nx.to_numpy_array(AT,nodelist=range(45),dtype=int);A2=AAT@AAT
    assert {int(A2[i,j]) for i,j in AT.edges()}=={3}
    assert {int(A2[i,j]) for i,j in itertools.combinations(range(45),2) if not AT.has_edge(i,j)}=={3}
    N=np.zeros((27,45),dtype=int)
    for j,t in enumerate(T):
        for x in t:N[x,j]=1
    assert np.array_equal(N.T@N,3*np.eye(45,dtype=int)+AAT)
    supports=[]
    for a,bb in G27.edges():
        y=N[a]-N[bb]
        assert np.array_equal(AAT@y,3*y) and int(y.sum())==0
        s=tuple(map(int,np.flatnonzero(y)));assert len(s)==8;supports.append(s)
    assert len(supports)==135 and len(set(supports))==135
    # Exhaust the connected graph types on <=7 vertices.  A support component for an eigen-3
    # vector must itself have eigenvalue3.  Every such connected graph on <=7 vertices has 3 as
    # its Perron root; because a total support <=7 can have only one such component (the smallest
    # has four vertices), outside cancellation is impossible in the connected 45-vertex graph.
    atlas=nx.graph_atlas_g();eig3_types=[];eigm4_types=[]
    for g in atlas:
        n=g.number_of_nodes()
        if not (0<n<=7 and nx.is_connected(g)):continue
        ev=np.linalg.eigvalsh(nx.to_numpy_array(g,dtype=float))
        if np.any(np.isclose(ev,3.0,atol=1e-9)):
            assert np.isclose(max(ev),3.0,atol=1e-9);eig3_types.append((n,g.number_of_edges()))
        if np.any(np.isclose(ev,-4.0,atol=1e-9)):eigm4_types.append((n,g.number_of_edges()))
    assert min(n for n,e in eig3_types)==4 and not eigm4_types
    out93={
      'pass':4993,'reader':'R=[C^T;M], 85x36, rank36','exact_erasure_distance':8,
      'minimum_failure_witnesses':{'construction':'difference of the two 5-tritangent stars of an intersecting pair of cubic lines',
        'intersecting_cubic_line_pairs':135,'distinct_support8_witnesses':135,'tritangent_graph_eigenvalue':3},
      'lower_bound_proof':{
        'mean_zero_V20':'a support <=7 would have one connected induced support component with eigenvalue3; exhaustive graph-atlas classification through seven vertices shows 3 is always its Perron root, so the necessary outside-neighbor cancellation is impossible',
        'mean_zero_V15':'no connected simple graph on <=7 vertices has eigenvalue -4, so a nonzero line-side dark eigenvector cannot have support <=7',
        'nonzero_mean':'both raw blocks are nonzero. Their supports must dominate their degree-12 graphs because the affine eigen-equation has nonzero constant right-hand side. Three closed neighborhoods cover at most39 vertices, so each block needs at least4 support coordinates and the total is at least8.'},
      'guaranteed_erasure_tolerance':7,
      'theorem':'The 85-sensor line+tritangent reader has exact cocircuit/erasure distance 8. Every deletion of at most seven sensors retains rank36, while 135 explicit eight-tritangent deletions obtained from intersecting cubic-line star differences kill rank.',
      'boundary':'The 135 canonical witnesses are one explicit minimum family; this pass does not claim they exhaust every support-eight cocircuit orbit.'}
    O93.write_text(json.dumps(out93,indent=2,sort_keys=True)+'\n')

    # ------------------------------------------------------------------ Pass4994
    g=build_group(b);PF=g['PF'];PP=g['PP'];spreads=b['spreads'];Hw=b['Hw'];L=b['L']
    q0=0;inc=sorted(i for i,S in enumerate(spreads) if q0 in S);ii={s:i for i,s in enumerate(inc)}
    loc=Hw.subgraph(inc);base=[frozenset(ii[s] for s in c) for c in nx.find_cliques(loc) if len(c)==3];assert len(base)==3
    cross={frozenset((a,bb)) for a,bb in itertools.combinations(range(9),2) if not any(a in B and bb in B for B in base)}
    trs=[frozenset(t) for t in itertools.combinations(range(9),3) if all(frozenset(e) in cross for e in itertools.combinations(t,2))]
    comps=[]
    def bt(ch,rem):
        if not rem:
            if len(ch)==9:comps.append(frozenset(ch))
            return
        p=min(rem,key=lambda x:sum(1 for t in trs if x<=t and {frozenset(e) for e in itertools.combinations(t,2)}<=rem))
        for t in trs:
            es={frozenset(e) for e in itertools.combinations(t,2)}
            if p<=t and es<=rem:bt(ch+[t],rem-es)
    bt([],cross);comps=sorted(set(comps),key=lambda Cc:sorted(map(tuple,Cc)));assert len(comps)==12;ci={Cc:i for i,Cc in enumerate(comps)}
    def local(s):return tuple(ii[s[x]] for x in inc)
    stF=[(l,s) for l,s in PF if l[q0]==q0];stP=[(l,s) for l,s in PP if l[q0]==q0]
    LF={local(s) for l,s in stF};LP={local(s) for l,s in stP};assert (len(LF),len(LP))==(1296,648)
    def ac(Cc,p):return frozenset(frozenset(p[x] for x in t) for t in Cc)
    def cpact(p):return tuple(ci[ac(Cc,p)] for Cc in comps)
    Dg=nx.Graph();Dg.add_nodes_from(range(12))
    for i,j in itertools.combinations(range(12),2):
        if len(comps[i]&comps[j])==0:Dg.add_edge(i,j)
    packets=sorted([frozenset(c) for c in nx.connected_components(Dg)],key=lambda x:tuple(sorted(x)));assert list(map(len,packets))==[3,3,3,3]
    pi={B:i for i,B in enumerate(packets)}
    def packact(cp):return tuple(pi[frozenset(cp[i] for i in B)] for B in packets)
    psig={frozenset(q for q,Lq in enumerate(L) if p in Lq):p for p in range(40)}
    def pointperm(l):return tuple(psig[frozenset(l[q] for q,Lq in enumerate(L) if p in Lq)] for p in range(40))
    bp=sorted(L[q0]);bi={p:i for i,p in enumerate(bp)}
    # Recover the unique packet<->point equivariant bijection and choose packet0 / its point.
    pairedF=[];pairedP=[]
    for carrier,target in ((stF,pairedF),(stP,pairedP)):
        for l,s in carrier:
            p=local(s);cp=cpact(p);pk=packact(cp);pp=pointperm(l);pa=tuple(bi[pp[x]] for x in bp)
            target.append((l,s,cp,pk,pp,pa))
    eq=[]
    for bij in itertools.permutations(range(4)):
        if all(all(bij[pk[i]]==pa[bij[i]] for i in range(4)) for l,s,cp,pk,pp,pa in pairedF):eq.append(bij)
    assert len(eq)==1
    packet0=0;point_local=eq[0][packet0];point0=bp[point_local];trip=sorted(packets[packet0]);ti={c:i for i,c in enumerate(trip)}
    def image_on_trip(records):
        imgs=set();count=0
        for l,s,cp,pk,pp,pa in records:
            if pp[point0]!=point0:continue
            count+=1;assert pk[packet0]==packet0
            imgs.add(tuple(ti[cp[c]] for c in trip))
        return count,imgs
    nP,imgP=image_on_trip(pairedP);nF,imgF=image_on_trip(pairedF)
    assert nP==162 and len(imgP)==3 and all(sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2==0 for p in imgP)
    assert nF==324 and len(imgF)==6
    out94={
      'pass':4994,'base_line':q0,'base_line_points':4,'affine_completions':12,'canonical_packets':'4 packets x 3 completions',
      'chosen_point_reduces_to_one_packet':True,
      'PSp_point_line_stabilizer':{'order':162,'image_on_residual_triple':'C3=A3','image_order':3,'kernel_order':54,'transitive':True},
      'full_PGSp_point_line_stabilizer':{'order':324,'image_on_residual_triple':'S3','image_order':6,'kernel_order':54,'transitive':True},
      'outer_character':'S3/C3=C2. The PGSp/PSp outer coset is exactly permutation parity on the residual triple, matching the finite Witting phase sign of Pass4966.',
      'gauge_reading':'After a base-line point is chosen, the residual affine ambiguity is a canonical C3 torsor. The finite geometry canonically orients the transformation group up to the outer reflection, but does not distinguish one of the three completion states.',
      'theorem':'Choosing one of the four W33 points attached to a local completion packet reduces the 12-fold affine gauge to a three-state torsor. PSp acts on that triple exactly as C3, while adjoining the multiplier-minus-one outer coset gives S3. Thus the Witting outer sign is the reflection parity C2=S3/C3 of the residual qutrit gauge.',
      'boundary':'This identifies the finite permutation structure. It does not turn the outer sign into physical CP or supply a canonical choice of one of the three completion states.'}
    O94.write_text(json.dumps(out94,indent=2,sort_keys=True)+'\n')

    # ------------------------------------------------------------------ Pass4995
    residual_masks=[m for m,V in b['residual']]
    r1=35 # connected 36-vertex H36 incidence rank over F2
    rz=360-r1
    rs=gf2_rank_int(residual_masks);rt=gf2_rank_int(tri_masks);rcomb=gf2_rank_int(residual_masks+tri_masks)
    assert (rs,rt,rcomb,rz)==(294,324,324,325)
    freq=Counter()
    for m in residual_masks:
        x=m
        while x:
            lb=x&-x;freq[lb.bit_length()-1]+=1;x^=lb
    assert set(freq.values())=={9} and len(freq)==360
    out95={
      'pass':4995,'chain':'H36 vertices <- edges <- residual squares / sigma-even triangles','C0_vertices':36,'C1_edges':360,
      'edge_boundary_rank':35,'cycle_space_dimension':325,
      'residual_square_complex':{'C2':810,'d2_rank':294,'edge_incidence_per_square':4,'squares_per_edge':9,
        'H0':1,'H1':31,'H2':516,'Euler_characteristic':486},
      'sigma_even_triangle_complex':{'C2':1080,'d2_rank':324,'H0':1,'H1':1,'H2':756,'Euler_characteristic':756},
      'combined_triangle_square_complex':{'C2':1890,'d2_rank':324,'H0':1,'H1':1,'H2':1566,'Euler_characteristic':1566},
      'invariant_filtration':{'square_span':294,'triangle_dual_span_Kperp':324,'full_cycle_space':325,
        'triangle_mod_square_dimension':30,'cycle_mod_triangle_dimension':1},
      'interpretation':'The residual squares leave 31 binary one-cycle classes. Adding the sigma-even triangle checks kills exactly 30 of them, leaving the single switching-parity class. The 30-dimensional intermediate quotient is an exact new carrier; equality of its dimension with 15_p+15_l is not by itself an isomorphism.',
      'theorem':'The 810 residual A4 equators define a square 2-complex on H36 with H1 dimension31 and H2 dimension516 over F2. Their boundary span has rank294 inside the rank324 sigma-even triangle/dual-code span, which itself has codimension one in the 325-dimensional graph cycle space. Hence the exact filtration dimensions are 294 < 324 < 325, with quotients 30 and1.',
      'boundary':'The 30 quotient is not identified with the real twin dark15 Levi nullspace without an explicit equivariant map.'}
    O95.write_text(json.dumps(out95,indent=2,sort_keys=True)+'\n')
    return 0

if __name__=='__main__':raise SystemExit(main())
