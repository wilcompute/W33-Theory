#!/usr/bin/env python3
"""Passes4979-4983 — 45-port spread reader, local wreath gauge, Q43 Bianchi,
AG(2,3) completion obstruction, and the spread-geometric meaning of dual A3.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
O71=ROOT/'data/PART_W33_PASS4979_TRITANGENT_SPREAD_45_PORT_TRANSCEIVER.json'
O72=ROOT/'data/PART_W33_PASS4980_LOCAL_NINE_SPREAD_WREATH_GAUGE.json'
O73=ROOT/'data/PART_W33_PASS4981_Q43_TETRAHEDRAL_BIANCHI_H2.json'
O74=ROOT/'data/PART_W33_PASS4982_LOCAL_AG23_COMPLETION_OBSTRUCTION.json'
O75=ROOT/'data/PART_W33_PASS4983_DUAL_TRIANGLES_AS_EMPTY_SPREAD_TRIPLES.json'

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def compose_map(p,q):return tuple(q[p[i]] for i in range(len(p)))
def invperm(p):return tuple(p.index(i) for i in range(len(p)))
def parity3(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))&1
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S
def paired_closure(genA,genB,nA,nB):
    I=(tuple(range(nA)),tuple(range(nB)));S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(genA,genB):
            z=(comp(ga,a),comp(gb,b))
            if z not in S:S.add(z);D.append(z)
    return S
def gf2_rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def main()->int:
    # Cubic-surface carrier and 36 double-sixes.
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[tuple(si[add2(x,v) if polar(x,v) else x] for x in sing) for v in nons]
    gp=[];S={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g],27)
        if len(T)>len(S):gp.append(g);S=T
        if len(S)==25920:break
    assert len(S)==25920 and len(closure(gp+[trans[0]],27))==51840
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    p27=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    l27=[tuple(i for i,P in enumerate(p27) if x in P) for x in qp]
    G27=nx.Graph();G27.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(l27[i])&set(l27[j]):G27.add_edge(i,j)
    tritangents=sorted(t for t in itertools.combinations(range(27),3)
                      if all(G27.has_edge(*e) for e in itertools.combinations(t,2)))
    assert len(tritangents)==45
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G27)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G27.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):
            DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36;di={D:i for i,D in enumerate(DS)}
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    A36=nx.to_numpy_array(H36,nodelist=range(36),dtype=int)
    tri36=sorted(t for t in itertools.combinations(range(36),3)
                 if all(H36.has_edge(*e) for e in itertools.combinations(t,2)))
    steiner=sorted(t for t in tri36 if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    assert (len(tri36),len(steiner))==(1200,120);sti={t:i for i,t in enumerate(steiner)}

    # PSp action on double-sixes and Steiner triples.
    DP=[];SP=[]
    for g in gp:
        dp=tuple(di[frozenset(g[x] for x in D)] for D in DS);DP.append(dp)
        SP.append(tuple(sti[tuple(sorted(dp[i] for i in t))] for t in steiner))

    # Steiner association scheme -> 40 Q43 fibers and 36 W33 spreads.
    seen=set();orbits=[]
    for p in itertools.combinations(range(120),2):
        if p in seen:continue
        O={p};seen.add(p);Dq=deque([p])
        while Dq:
            a=Dq.popleft()
            for op in SP:
                b=tuple(sorted((op[a[0]],op[a[1]])))
                if b not in O:O.add(b);seen.add(b);Dq.append(b)
        orbits.append(sorted(O))
    R1,R2,R3,R4=sorted(orbits,key=len);assert list(map(len,(R1,R2,R3,R4)))==[120,1620,2160,3240]
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1)
    fibers=sorted([sorted(c) for c in nx.connected_components(FG)]);assert len(fibers)==40
    fi={x:i for i,F in enumerate(fibers) for x in F};pos={x:i for F in fibers for i,x in enumerate(F)}
    fiber_index={frozenset(F):i for i,F in enumerate(fibers)}
    Q=nx.Graph();Q.add_nodes_from(range(40))
    for a,b in R3:Q.add_edge(fi[a],fi[b])
    FP=[tuple(fiber_index[frozenset(op[x] for x in F)] for F in fibers) for op in SP]
    spreads=sorted([frozenset(c) for c in nx.find_cliques(nx.complement(Q)) if len(c)==10],
                   key=lambda s:tuple(sorted(s)));assert len(spreads)==36
    spi={S:i for i,S in enumerate(spreads)}
    SprP=[tuple(spi[frozenset(p[i] for i in S)] for S in spreads) for p in FP]

    # Full outer action and unique Pass4964 bridge.
    gout=trans[0]
    dpout=tuple(di[frozenset(gout[x] for x in D)] for D in DS)
    spout=tuple(sti[tuple(sorted(dpout[i] for i in t))] for t in steiner)
    fpout=tuple(fiber_index[frozenset(spout[x] for x in F)] for F in fibers)
    sprout=tuple(spi[frozenset(fpout[i] for i in S)] for S in spreads)
    ds_spr=paired_closure(DP+[dpout],SprP+[sprout],36,36);assert len(ds_spr)==51840
    stab0=[(a,b) for a,b in ds_spr if a[0]==0];fixed=[s for s in range(36) if all(b[s]==s for a,b in stab0)]
    assert len(fixed)==1
    bridge={}
    for a,b in ds_spr:
        d=a[0];s=b[fixed[0]]
        if d in bridge:assert bridge[d]==s
        bridge[d]=s
    assert len(bridge)==36

    # 4979: 45 tritangent selectors on the 36 spread/double-six carrier.
    M=np.array([[1 if len(set(T)&set(D))==2 else 0 for D in DS] for T in tritangents],dtype=int)
    meet_profile=Counter(tuple(sorted(Counter(len(set(T)&set(D)) for D in DS).items())) for T in tritangents)
    assert meet_profile==Counter({((0,12),(2,24)):45})
    assert set(map(int,M.sum(1)))=={24} and set(map(int,M.sum(0)))=={30}
    assert np.linalg.matrix_rank(M)==21
    J36=np.ones((36,36),dtype=int);I36=np.eye(36,dtype=int)
    assert np.array_equal(M.T@M,18*J36+12*I36+3*A36)
    rowgram=M@M.T
    rel=Counter((len(set(tritangents[i])&set(tritangents[j])),int(rowgram[i,j]))
                for i in range(45) for j in range(i+1,45))
    assert rel==Counter({(0,15):720,(1,18):270})

    Cq=np.zeros((36,40),dtype=int)
    for d in range(36):Cq[d,list(spreads[bridge[d]])]=1
    assert np.array_equal(Cq@Cq.T,4*J36+6*I36-3*A36)
    assert np.linalg.matrix_rank(Cq)==16
    assert np.array_equal(Cq@Cq.T+M.T@M,22*J36+18*I36)
    assert np.linalg.matrix_rank(np.vstack([Cq.T,M]))==36
    out71={'pass':4979,
      'tritangents':45,'spreads_double_sixes':36,
      'selector_incidence':{'shape':[45,36],'row_weight':24,'column_weight':30,'rank':21,
        'criterion':'a tritangent selects a spread iff the corresponding double-six contains exactly two of its three cubic lines',
        'per_tritangent_profile':{'selected_meet_2':24,'unselected_meet_0':12,'meet_1':0,'meet_3':0}},
      'Gram':{'tritangent_side_pair_counts':{'disjoint_tritangents_Gram15':720,'one_common_cubic_line_Gram18':270},
        'spread_side':'M^T M = 18J + 12I + 3A_H36','nonzero_sector':'1+20','dark_sector':'15',
        'squared_singular_values':{'720':1,'18':20}},
      'complementary_40_plus_45_readout':{
        'spread_line_channel':'C C^T = 4J + 6I - 3A_H36, rank 16 = 1+15',
        'identity':'18 I_36 = C C^T + M^T M - 22 J_36',
        'stacked_shape':[85,36],'stacked_rank':36},
      'theorem':'The 45 cubic-surface tritangents canonically define a 45x36 selector matrix on the Pass4964 spread carrier. Every tritangent selects exactly 24 spreads (and every spread is selected by 30 tritangents); the matrix has rank 21 and transmits precisely the 1+20 sector, killing the 15. Its Gram cancels the H36 adjacency term in the rank-16 spread-line channel, giving 18I=CC^T+M^TM-22J and a complete 40-line plus 45-tritangent readout of all 36 spread coordinates.',
      'boundary':'The 45 rows are exact finite selectors. Calling them physical ports requires a hardware realization of the two-line-in-double-six predicate.'}
    O71.write_text(json.dumps(out71,indent=2,sort_keys=True)+'\n')

    # 4980: stabilizer of one W33 line on its nine incident spreads.
    full_qs=paired_closure(FP+[fpout],SprP+[sprout],40,36);assert len(full_qs)==51840
    byline=defaultdict(list)
    for t in steiner:
        ss=tuple(sorted(bridge[d] for d in t));common=set.intersection(*(set(spreads[s]) for s in ss));assert len(common)==1
        byline[next(iter(common))].append(ss)
    q0=0;inc=sorted(s for s,S in enumerate(spreads) if q0 in S);assert len(inc)==9;ii={s:i for i,s in enumerate(inc)}
    parts=[tuple(sorted(ii[s] for s in trip)) for trip in byline[q0]];assert len(parts)==3
    stab=[(fq,fs) for fq,fs in full_qs if fq[q0]==q0];assert len(stab)==1296
    local=set(tuple(ii[fs[s]] for s in inc) for fq,fs in stab);assert len(local)==1296
    # Full setwise stabilizer of a 3+3+3 partition is S3 wr S3, order 6^4=1296.
    assert 6**4==1296
    out72={'pass':4980,'local_chart':{'base_W33_line':q0,'incident_spreads':9,'canonical_Steiner_partition':'3+3+3'},
      'full_group_line_stabilizer_order':1296,'induced_local_permutation_group_order':1296,
      'kernel_on_nine_spreads_order':1,'identified_local_group':'S3 wr S3 (full imprimitive wreath product in degree 9)',
      'compiler_consequence':{
        'canonical_unlabeled_three_blocks':True,'canonical_order_of_blocks':False,'canonical_order_inside_blocks':False,
        'raw_qutrit_coordinate_system_available_without_gauge_choice':False,
        'minimal_statement':'the finite substrate supplies an unlabeled 3x3 imprimitive chart; qutrit labels require gauge fixing'},
      'theorem':'The stabilizer of a W33 line in W(E6) has order 1296 and acts faithfully on the nine spreads through that line as the entire wreath product S3 wr S3. Thus the Pass4965 3+3+3 partition is canonical as an unlabeled block system, but neither the three blocks nor their three members carry canonical labels.',
      'boundary':'This is an exact finite symmetry obstruction to a canonical compiler labeling, not an obstruction to choosing and calibrating a gauge in hardware.'}
    O72.write_text(json.dumps(out72,indent=2,sort_keys=True)+'\n')

    # 4981: Q43 tetrahedral Bianchi and H2.
    Qbar=nx.complement(Q);Qbar.remove_edges_from(nx.selfloop_edges(Qbar));assert Qbar.number_of_edges()==540
    edges=sorted(tuple(sorted(e)) for e in Qbar.edges());ei={e:i for i,e in enumerate(edges)}
    triangles=sorted(t for t in itertools.combinations(range(40),3)
                     if all(Qbar.has_edge(*e) for e in itertools.combinations(t,2)))
    tetra=sorted(c for c in itertools.combinations(range(40),4)
                 if all(Qbar.has_edge(*e) for e in itertools.combinations(c,2)))
    assert (len(triangles),len(tetra))==(3240,9450)
    ti={t:i for i,t in enumerate(triangles)}
    d2=[]
    for t in triangles:
        bits=0
        for e in itertools.combinations(t,2):bits^=1<<ei[tuple(sorted(e))]
        d2.append(bits)
    rank2=gf2_rank(d2);assert rank2==501
    d3=[]
    for c in tetra:
        bits=0
        for t in itertools.combinations(c,3):bits^=1<<ti[tuple(sorted(t))]
        d3.append(bits)
    rank3=gf2_rank(d3);assert rank3==2739 and 3240-rank2-rank3==0

    r2=set(R2)
    def edgeperm(u,v):
        p=[None]*3
        for x in fibers[u]:
            ys=[y for y in fibers[v] if tuple(sorted((x,y))) in r2];assert len(ys)==1
            p[pos[x]]=pos[ys[0]]
        return tuple(p)
    transports={}
    for u,v in Qbar.edges():
        p=edgeperm(u,v);transports[(u,v)]=p;transports[(v,u)]=invperm(p)
    def hol(u,v,w):
        p=transports[(u,v)];p=compose_map(p,transports[(v,w)]);p=compose_map(p,transports[(w,u)]);return p
    curvature={t:parity3(hol(*t)) for t in triangles}
    assert Counter(curvature.values())==Counter({1:2160,0:1080})
    face_odd=Counter();bianchi_ok=0
    I3=(0,1,2)
    def seq(*ps):
        p=I3
        for q in ps:p=compose_map(p,q)
        return p
    for a,b,c,d in tetra:
        face_odd[sum(curvature[tuple(sorted(t))] for t in itertools.combinations((a,b,c,d),3))]+=1
        lhs=seq(hol(a,b,c),hol(a,c,d),hol(a,d,b))
        rhs=seq(transports[(a,b)],hol(b,c,d),transports[(b,a)])
        assert lhs==rhs;bianchi_ok+=1
    assert face_odd==Counter({2:6480,4:2700,0:270}) and bianchi_ok==9450
    out73={'pass':4981,'Q43_disjointness_clique_complex':{
        'vertices':40,'edges':540,'triangles':3240,'tetrahedra_K4':9450,
        'rank_triangle_to_edge_boundary_F2':501,'kernel_dimension_triangle_boundary':2739,
        'rank_tetrahedron_to_triangle_boundary_F2':2739,'H1_dimension_F2':0,'H2_dimension_F2_after_filling_K4':0},
      'curvature_Bianchi':{
        'flat_triangle_faces':1080,'reflection_triangle_faces':2160,
        'tetrahedra_by_number_of_reflection_faces':{'0':270,'2':6480,'4':2700},
        'all_tetrahedra_even_reflection_face_parity':True,
        'nonabelian_S3_Bianchi_identity_verified_tetrahedra':9450,
        'identity':'H_abc H_acd H_adb = P_ab H_bcd P_ba'},
      'theorem':'The 9450 K4 tetrahedra of the Q43 disjointness graph span the entire 2739-dimensional F2 kernel of the triangle boundary map. Consequently the clique 3-skeleton has H1=H2=0 over F2. The sign curvature obeys exact tetrahedral Bianchi parity (0,2,or4 reflection faces only), and the full S3 edge transports satisfy the nonabelian Bianchi identity on all 9450 tetrahedra.',
      'consequence':'The 2160 local reflection curvatures carry no residual F2 two-cycle charge once tetrahedra are included; both the flat H1 sector and the abelianized H2 curvature sector close locally.',
      'boundary':'Vanishing H1/H2 is over F2 for the stated clique 3-skeleton. It does not assert integral or higher-dimensional homology vanishes.'}
    O73.write_text(json.dumps(out73,indent=2,sort_keys=True)+'\n')

    # 4982: exactly 12 affine-plane completions of the fixed 3+3+3 class.
    groups=[list(p) for p in parts];A0,B0,C0=groups
    latin=[]
    for vals in itertools.product(range(3),repeat=9):
        L=np.array(vals,dtype=int).reshape(3,3)
        if not all(set(map(int,L[i,:]))=={0,1,2} for i in range(3)):continue
        if not all(set(map(int,L[:,j]))=={0,1,2} for j in range(3)):continue
        lineset=frozenset(frozenset((A0[i],B0[j],C0[int(L[i,j])])) for i in range(3) for j in range(3))
        latin.append(lineset)
    latin=set(latin);assert len(latin)==12
    for lineset in latin:
        LL=list(lineset);Dg=nx.Graph();Dg.add_nodes_from(range(9))
        for i,j in itertools.combinations(range(9),2):
            if not (LL[i]&LL[j]):Dg.add_edge(i,j)
        comps=list(nx.connected_components(Dg))
        assert sorted(map(len,comps))==[3,3,3] and set(dict(Dg.degree()).values())=={2}
    def act(p,ls):return frozenset(frozenset(p[x] for x in L) for L in ls)
    orbit={act(p,next(iter(latin))) for p in local};assert orbit==latin
    completion_stabilizer=1296//12;assert completion_stabilizer==108
    out74={'pass':4982,'fixed_local_partition':'the Pass4965/4980 3+3+3 parallel class on nine spreads',
      'AG23_completions':{
        'count':12,'construction':'the remaining nine affine lines are the triples of one of the 12 Latin squares of order 3',
        'each_completion_additional_parallel_classes':3,
        'local_S3_wr_S3_action_on_completions':'transitive','completion_stabilizer_order':108},
      'canonical_completion_exists':False,
      'group_order_obstruction':'S3 wr S3 has order1296, while the stabilizer of one AG(2,3) completion with the distinguished parallel class has order108; the 12 completions form one orbit',
      'theorem':'The canonical local 3+3+3 partition does not intrinsically complete to a unique affine plane AG(2,3). There are exactly 12 labeled AG(2,3) completions containing that parallel class, and the full local S3 wr S3 symmetry acts transitively on all 12. Choosing an affine/qutrit coordinate plane therefore breaks a 12-fold finite gauge ambiguity.',
      'boundary':'All 12 completions are equivalent under the local stabilizer. Extra physical structure could select one, but the bare W33/double-six incidence data does not.'}
    O74.write_text(json.dumps(out74,indent=2,sort_keys=True)+'\n')

    # 4983: spread-geometric characterization of the 1080 dual triangles.
    triple_inter=Counter()
    for t in tri36:
        ss=[spreads[bridge[d]] for d in t]
        common=set.intersection(*(set(s) for s in ss))
        triple_inter[len(common)]+=1
        assert (t in set(steiner))==(len(common)==1)
    assert triple_inter==Counter({0:1080,1:120})
    out75={'pass':4983,'H36_one_overlap_triangles':1200,
      'spread_triple_intersection_census':{'empty_common_W33_line':1080,'one_common_W33_line':120},
      'Steiner_characterization':'the 120 Steiner triangles are exactly the one-overlap spread triples with one common W33 line',
      'dual_A3_characterization':'the 1080 weight-three checks of K^perp are exactly the one-overlap spread triples with empty triple intersection (Pass4976 sigma-even class)',
      'theorem':'Under the unique Pass4964 double-six/spread bridge, the 1200 triangles of the H36 one-overlap graph split canonically by triple intersection: 120 Steiner triangles share exactly one W33 line, while the other 1080 share none. Combining this with Pass4976 identifies the complete dual weight-three shell of K with the empty-common-line spread triples.',
      'consequence':'The code-theoretic number A3(K^perp)=1080 is no longer merely an enumerator coefficient: it is the complement of the 120 local Steiner/one-common-line triangles inside the 1200 triangles of the 36-spread one-overlap graph.',
      'boundary':'This identifies the weight-three dual shell. It does not imply analogous single-predicate descriptions for all higher dual shells.'}
    O75.write_text(json.dumps(out75,indent=2,sort_keys=True)+'\n')

    print(json.dumps({'4979_rank':int(np.linalg.matrix_rank(M)),'4980_local_group':len(local),
      '4981':{'K4':len(tetra),'rank_d3':rank3,'H2':0,'Bianchi':bianchi_ok},
      '4982_AG23_completions':len(latin),'4983':dict(triple_inter)},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
