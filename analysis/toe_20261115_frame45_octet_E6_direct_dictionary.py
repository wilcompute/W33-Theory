#!/usr/bin/env python3
"""Direct W33 apartment-component -> K4,4 octet -> E6 27/45 dictionary.

Prior art: BT766/Pass1536 already constructed 45 K4,4 octets;
TOE23 already found 45x36 components; TOE24 already matched them to
prior E6 tritangent supports by a Levi dual/XOR construction.
NEW scoped control: map each point-apartment hopping component DIRECTLY
to its 8-ray union and to existing BT1536's intrinsic octet (mod a
symplectic coordinate permutation); reconstruct the 27 cubic lines
as the 27 maximum K5 cliques of the 45-object disjoint-octet graph
and exhibit an EXPLICIT graph isomorphism to the classical a/b/c
blowup-of-P2 27-line labeling and its 30+15 tritangents.
All adjacency and incidence equalities are integer-exact checks.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from itertools import combinations,product
from pathlib import Path
import json,sys
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass1536_frame_dual_k44_code import build_geometry
OUT=ROOT/"data"/"toe_20261115_apartment_octet_e6_27_45_dictionary.json"

def rays_and_frames():
    def canon(v):
        v=tuple(int(x)%3 for x in v)
        pivot=next(x for x in v if x)
        return tuple((2 if pivot==2 else 1)*x%3 for x in v)
    pts=sorted({canon(x) for x in product(range(3),repeat=4) if any(x)})
    assert len(pts)==40
    def omega(a,b):
        return (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%3
    A=np.zeros((40,40),dtype=np.int16)
    for i,j in combinations(range(40),2):
        if omega(pts[i],pts[j])==0:A[i,j]=A[j,i]=1
    frames=[]
    for f in combinations(range(40),4):
        op=[(x,y) for x,y in combinations(range(4),2)
            if omega(pts[f[x]],pts[f[y]])!=0]
        if len(op)==2 and len({a for pair in op for a in pair})==4:
            frames.append(f)
    assert len(frames)==1620
    return pts,A,frames

def classical_27():
    G=nx.Graph()
    labels=(["a"+str(i) for i in range(6)]
            +["b"+str(i) for i in range(6)]
            +["c"+str(i)+str(j) for i,j in combinations(range(6),2)])
    G.add_nodes_from(labels)
    for i,j in product(range(6),repeat=2):
        if i!=j:G.add_edge("a"+str(i),"b"+str(j))
    for i,j in combinations(range(6),2):
        c=f"c{i}{j}"
        for t in (i,j):
            G.add_edge(c,"a"+str(t))
            G.add_edge(c,"b"+str(t))
        for k,l in combinations(range(6),2):
            if {i,j}.isdisjoint({k,l}):G.add_edge(c,f"c{k}{l}")
    assert len(G)==27 and G.number_of_edges()==135
    triads=set()
    for i,j in product(range(6),repeat=2):
        if i!=j:
            triads.add(tuple(sorted((f"a{i}",f"b{j}",f"c{min(i,j)}{max(i,j)}"))))
    for trio in combinations(list(combinations(range(6),2)),3):
        if len(set(sum((list(p) for p in trio),[])))==6:
            triads.add(tuple(sorted(f"c{i}{j}" for i,j in trio)))
    assert len(triads)==45
    return G,triads

def reproduce():
    pts,A,frames=rays_and_frames()
    F=np.zeros((1620,40),dtype=np.int16)
    for i,frame in enumerate(frames):F[i,list(frame)]=1
    ov=F@F.T
    flip=nx.from_numpy_array(ov==3)
    components=sorted((sorted(s) for s in nx.connected_components(flip)),key=lambda x:x[0])
    assert len(components)==45 and all(len(c)==36 for c in components)
    assert all(d==8 for _,d in flip.degree())

    prior=build_geometry()
    prior_pts=prior["points"]
    pidx={tuple(p):i for i,p in enumerate(prior_pts)}
    # Our omega pairs (coordinate 0,2), (1,3); Pass1536
    # uses Omega pairs (0,1), (2,3). Explicit coordinate interchange.
    def normalize(v):
        factor=2 if next(x for x in v if x)==2 else 1
        return tuple(factor*x%3 for x in v)
    pmap=[pidx[normalize((v[0],v[2],v[1],v[3]))] for v in pts]
    assert all((A[i,j]>0)==prior["graph"].has_edge(pmap[i],pmap[j])
               for i in range(40) for j in range(i+1,40))
    old_octets={frozenset(left+right) for left,right in prior["octets"]}
    assert len(old_octets)==45

    supports=[]
    witness_octets=[]
    standard=nx.cartesian_product(nx.line_graph(nx.complete_graph(4)),
                                   nx.line_graph(nx.complete_graph(4)))
    component_hist=Counter()
    for comp in components:
        S=tuple(sorted({p for idx in comp for p in frames[idx]}))
        assert len(S)==8
        H=nx.from_numpy_array(A[np.ix_(S,S)])
        assert nx.is_bipartite(H) and H.number_of_edges()==16
        side=nx.bipartite.sets(H)  # connected K4,4 gives unique bipartition
        left,right=(tuple(S[i] for i in sorted(part)) for part in side)
        assert len(left)==len(right)==4
        assert all(A[i,j]==0 for i,j in combinations(left,2))
        assert all(A[i,j]==0 for i,j in combinations(right,2))
        assert all(A[i,j]==1 for i in left for j in right)
        expected={frozenset(a+b) for a in combinations(left,2)
                  for b in combinations(right,2)}
        actual={frozenset(frames[i]) for i in comp}
        assert expected==actual and len(expected)==36
        component=flip.subgraph(comp)
        assert nx.is_isomorphic(component,standard)
        ev=Counter(int(round(z)) for z in np.linalg.eigvalsh(
            nx.to_numpy_array(component,nodelist=comp)))
        component_hist[tuple(sorted(ev.items()))]+=1
        prior_support=frozenset(pmap[i] for i in S)
        assert prior_support in old_octets
        supports.append(frozenset(S))
        witness_octets.append({"points":list(S),
                               "prior_BT1536_point_ids":sorted(prior_support),
                               "local_frame_count":36})
    assert len(set(supports))==45
    assert {frozenset(z["prior_BT1536_point_ids"]) for z in witness_octets}==old_octets
    assert len(component_hist)==1
    spec=dict(component_hist.most_common(1)[0][0])
    assert spec=={-4:4,-2:12,0:9,2:4,4:6,8:1}

    # Intrinsic 45-point graph: disjoint K4,4 octet supports.
    C=np.zeros((45,45),dtype=np.int16)
    intersection=Counter()
    for i,j in combinations(range(45),2):
        common=len(supports[i]&supports[j])
        intersection[common]+=1
        assert common in (0,2)
        if common==0:C[i,j]=C[j,i]=1
    assert intersection==Counter({2:720,0:270})
    assert np.array_equal(C.sum(axis=1),np.full(45,12))
    assert np.array_equal(C@C,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))
    graph45=nx.from_numpy_array(C)
    # Each of the 27 maximal 5-cliques is a cubic-surface LINE;
    # each of the 45 octets is a TRITANGENT incident with 3 lines.
    lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(graph45))
    assert len(lines)==27 and all(len(c)==5 for c in lines)
    T=np.zeros((45,27),dtype=np.int16)
    for j,clique in enumerate(lines):T[list(clique),j]=1
    assert np.array_equal(T.sum(axis=0),np.full(27,5))
    assert np.array_equal(T.sum(axis=1),np.full(45,3))
    incidence=T.T@T
    assert all(incidence[i,i]==5 for i in range(27))
    graph27=nx.from_numpy_array(incidence-5*np.eye(27,dtype=int))
    assert all(x==10 for _,x in graph27.degree())
    A27=nx.to_numpy_array(graph27,dtype=int)
    assert np.array_equal(A27@A27,5*np.eye(27,dtype=int)-4*A27+
                          5*np.ones((27,27),dtype=int))
    classical,triads=classical_27()
    gm=nx.isomorphism.GraphMatcher(graph27,classical)
    witness=next(gm.isomorphisms_iter(),None)
    assert witness is not None
    recovered={tuple(sorted(witness[j] for j in np.flatnonzero(T[i])))
               for i in range(45)}
    assert recovered==triads

    # Independently recover the known W33 point incidence 40x45 and
    # Schläfli 45x27 incidence, with no arbitrary E6 labels assumed.
    P=np.zeros((40,45),dtype=np.int16)
    for i,S in enumerate(supports):P[list(S),i]=1
    assert np.array_equal(P@P.T,
        8*np.eye(40,dtype=int)+np.ones((40,40),dtype=int)+2*A)
    assert np.array_equal(P.T@P,8*np.eye(45,dtype=int)+2*(np.ones((45,45),dtype=int)-np.eye(45,dtype=int)-C))
    # Each of the 27 E6 "lines" is a partition of all 40 W33 rays
    # into five pairwise disjoint K4,4 octets.
    assert np.array_equal(P@T,np.ones((40,27),dtype=int))
    assert np.array_equal(T@T.T,3*np.eye(45,dtype=int)+C)
    # Stronger all-walk obstruction for the unweighted tritangent
    # network C: every m-step propagation is still uniform!
    assert np.array_equal(C@T,3*T+np.ones((45,27),dtype=int))
    walk=np.eye(45,dtype=np.int64)
    for m in range(7):
        transfer=P.astype(np.int64)@walk@T.astype(np.int64)
        assert np.array_equal(transfer,12**m*np.ones((40,27),dtype=np.int64))
        walk=walk@C.astype(np.int64)
    rank_point=int(np.linalg.matrix_rank(P))
    rank_line=int(np.linalg.matrix_rank(T))
    P0=P.astype(float)-np.ones((40,45),dtype=float)/5
    T0=T.astype(float)-np.ones((45,27),dtype=float)/9
    assert np.allclose(P0@T0,0,atol=1e-12)
    assert rank_point==25 and rank_line==21
    assert np.linalg.matrix_rank(P0)==24 and np.linalg.matrix_rank(T0)==20
    # A tensor, not the naïve linear incidence composition, escapes
    # the rank-one obstruction while remaining symplectic-covariant:
    # Q[p,q,l]=sum_o P[p,o]*P[q,o]*T[o,l].
    # Every l partitions 40 points into five disjoint K4,4 octets.
    # Thus Q[p,q,l]=1 iff p and q belong to the same octet for l.
    tensor=np.einsum("pa,qa,al->pql",P,P,T,optimize=True).astype(np.int16)
    assert tensor.shape==(40,40,27) and set(np.unique(tensor))=={0,1}
    assert np.array_equal(tensor.sum(axis=2),3*(P@P.T))
    for line in range(27):
        block=tensor[:,:,line]
        assert np.array_equal(block,block.T)
        assert np.array_equal(block@block,8*block)
        assert int(np.trace(block))==40
        assert np.all(block.sum(axis=1)==8)
    for p in range(40):
        conditioned=tensor[p,:,:]
        assert np.all(conditioned[p,:]==1)
        assert np.linalg.matrix_rank(conditioned)==9
        columns=Counter(tuple(np.flatnonzero(conditioned[:,l])) for l in range(27))
        assert len(columns)==9 and set(columns.values())=={3}
        assert all(len(z)==8 and p in z for z in columns)
        for q in range(40):
            amount=int(tensor[p,q,:].sum())
            assert amount==(27 if p==q else 9 if A[p,q] else 3)
    assert np.array_equal(tensor.sum(axis=0),8*np.ones((40,27),dtype=int))
    # Check objectwise covariance against explicit transvections,
    # not just the 40/45/27 orbit counts.
    point_index={p:i for i,p in enumerate(pts)}
    octet_index={s:i for i,s in enumerate(supports)}
    line_index={frozenset(s):i for i,s in enumerate(lines)}
    def norm(v):
        v=tuple(int(x)%3 for x in v)
        fac=2 if next(x for x in v if x)==2 else 1
        return tuple(fac*x%3 for x in v)
    def form(a,b):
        return (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%3
    test_vectors=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
                  (1,1,0,0),(1,0,0,1),(1,0,1,0))
    for v in test_vectors:
        perm_p=[point_index[norm(tuple(p[k]+form(p,v)*v[k]
                                   for k in range(4)))] for p in pts]
        assert len(set(perm_p))==40
        perm_o=[octet_index[frozenset(perm_p[j] for j in S)] for S in supports]
        assert len(set(perm_o))==45
        perm_l=[line_index[frozenset(perm_o[k] for k in clique)] for clique in lines]
        assert len(set(perm_l))==27
        assert np.array_equal(tensor[np.ix_(perm_p,perm_p,perm_l)],tensor)
    # For every one of the 40 W33 point axes, derive the induced
    # order-three action on the 27 cubic line objects directly.
    # Its 9 three-cycles are EXACTLY the nine tritangent triples
    # (one per octet support containing the chosen W33 point).
    all_clocks=[]
    for ip,v in enumerate(pts):
        pp=[point_index[norm(tuple(w[k]+form(w,v)*v[k] for k in range(4)))]
            for w in pts]
        po=[octet_index[frozenset(pp[j] for j in S)] for S in supports]
        pl=tuple(line_index[frozenset(po[k] for k in line)] for line in lines)
        assert len(set(pl))==27
        cycle_groups=set()
        visited=set()
        for seed in range(27):
            if seed in visited:continue
            cyc=[];cur=seed
            while cur not in visited:
                visited.add(cur);cyc.append(cur);cur=pl[cur]
            assert cur==seed and len(cyc)==3
            cycle_groups.add(frozenset(cyc))
        assert len(cycle_groups)==9
        exact_tritangent_groups={
            frozenset(j for j,line in enumerate(lines) if a in line)
            for a,S in enumerate(supports) if ip in S
        }
        assert len(exact_tritangent_groups)==9
        assert cycle_groups==exact_tritangent_groups
        all_clocks.append(pl)
    def compose(g,h):
        return tuple(g[h[i]] for i in range(27))
    ident=tuple(range(27))
    def order_of(g):
        cur=ident
        for k in range(1,13):
            cur=compose(g,cur)
            if cur==ident:return k
        raise AssertionError("order > 12")
    assert all(order_of(g)==3 for g in all_clocks)
    pairs_by_relation=Counter()
    for i,j in combinations(range(40),2):
        c=(compose(all_clocks[i],all_clocks[j])==
           compose(all_clocks[j],all_clocks[i]))
        adjacent=bool(A[i,j])
        assert c==adjacent
        product_order=order_of(compose(all_clocks[i],all_clocks[j]))
        assert product_order==(3 if adjacent else 6)
        pairs_by_relation[(int(c),product_order)]+=1
    assert pairs_by_relation=={(1,3):240,(0,6):540}
    # The natural 45-dimensional permutation carrier decomposes into
    # 1 + 24 (visible from W33 point incidence) + 20 (from cubic lines).
    # Their common nontrivial sectors are orthogonal, not equivalent.
    return {
      "status":"PASS_EXACT_COMPONENT_OCTET_SCHLAFLI_DICTIONARY",
      "prior_art":"BT766 and Pass1536 already construct 45 K4,4 octets; TOE23 45x36 hopping components; TOE24 45 component-to-E6 tritangent bijection via dual XOR supports; this code provides a direct point-side octet equality and independently reconstructs cubic E6 27 lines from 45 disjoint-octet K5 cliques",
      "n_frames":len(frames),"components":len(components),
      "frame_count_per_component":36,
      "component_support_points":8,
      "component_graph":"J(4,2) Cartesian-product J(4,2)",
      "component_graph_spectrum":{str(k):v for k,v in spec.items()},
      "component_graph_triangle_count":96,
      "component_isomorphism_verified_all_45":True,
      "component_to_prior_BT1536_octets_exact_set_equality":True,
      "symplectic_coordinate_conversion":"(a,b,c,d)->(a,c,b,d)",
      "45_pair_octet_support_intersections":dict(intersection),
      "45_disjoint_support_SRG":[45,12,3,3],
      "45_SRG_identity":"C^2=9 I+3 J",
      "cubic_27_line_graph_SRG":[27,10,1,5],
      "cubic_27_intersection_graph_isomorphism":witness,
      "27_line_45_tritangent_incidence_degree":[5,3],
      "27_partitions_of_W33_40_points_into_five_disjoint_K44":True,
      "point_octet_times_octet_line_incidence":"P_40x45 @ T_45x27 = J_40x27",
      "tritangent_graph_on_lines_identity":"C_45x45 @ T_45x27 = 3T + J",
      "all_order_disjoint_octet_walk_obstruction":"P C^m T = 12^m J for every integer m >= 0",
      "walk_order_range_independently_integer_tested":[0,1,2,3,4,5,6],
      "rank_P":rank_point,"rank_T":rank_line,
      "centered_rank_P":24,"centered_rank_T":20,
      "centered_transfer_exactly_zero":True,
      "45_representation_decomposition":"1 + 24 (W33 point-incidence visible) + 20 (E6 line-incidence visible)",
      "naive_linear_observer_to_matter_obstruction":"Centered W33 point-octet incidence composed with centered E6 octet-line incidence is identically zero; nontrivial LINEAR 40-to-27 transfer needs phase/orientation, an operator insertion, or a different correspondence. The constructed native symmetric bilinear point-pair transfer bypasses this linear obstruction.",
      "two_point_conditioned_W33_to_E6_tensor_shape":[40,40,27],
      "two_point_conditional_E6_multiplicities":{"same_W33_point":27,"adjacent_W33_points":9,"nonadjacent_W33_points":3},
      "each_E6_line_40x40_pair_matrix_identity":"Q_l^2=8 Q_l and rank(Q_l)=5 (five K4,4 equivalence classes)",
      "each_W33_point_induces_nine_disjoint_E6_tritangent_triples":True,
      "all_40_point_conditioned_40x27_transfer_matrices_rank":9,
      "equivariant_symplectic_transvection_witnesses":len(test_vectors),
      "all_40_point_transvections_on_E6_lines_order":3,
      "all_40_point_transvections_orbit_type":"3^9, nine free 3-cycles",
      "each_40_point_nine_cycles_equal_its_nine_tritangent_triples":True,
      "W33_adjacency_iff_cubic_line_transvections_commute":True,
      "commuting_pair_count_and_product_order":{"240":3,"540":6},
      "all_780_pairs_checked":True,
      "operator_prior_art":"BT874/BT875 already showed a selected long-root transvection has 9 free orbits on the 27 matter shell and Z3 grading; this pass identifies ALL 40 projective symplectic point-axis transvection cycles with exact point-conditioned tritangent triples in the direct octet dictionary.",
      "operator_scope":"Finite permutation Weyl symmetry on 27 cubic lines, not continuous E6 gauge transformations, not autonomous physical time and not an energy-conserving Hamiltonian.",
      "bilinear_map":"Phi(x,y)_l = sum_{p,q} Q[p,q,l] x[p] y[q]",
      "quadratic_bridge_scope":"All checks are finite exact combinatorial incidence or explicit GF(3) transvection covariance; a symmetric bilinear map is not a physical matter coupling, energy scale, gauge generator, or Lorentzian dynamics.",
      "tritangent_types":{"a_i_b_j_c_ij":30,"three_pair_partition":15},
      "all_45_explicit_blowup_triads_match":True,
      "45_component_supports_in_our_point_indices":[sorted(x) for x in supports],
      "limitation":"Pure finite symplectic and cubic-surface graph geometry; no physical E6 gauge interaction, no new proof that 45 components or 45 octets exist, and no native frame-selection mechanism."
    }

if __name__=="__main__":
    record=reproduce()
    OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS",record["status"],record["45_disjoint_support_SRG"],
          record["cubic_27_line_graph_SRG"],flush=True)
