#!/usr/bin/env python3
"""Passes 7138--7145: C2 normal form, Gram gauge reduction, quotient geometry,
and three outside-box probes.

Exact finite statements are asserted directly.  The all-q quotient *spectrum* formula is
recorded only as a conjecture with exact/computational anchors q=3,5,7,9; all-q orbit counts,
degrees, involution geometry, and matrix-idempotent identifications are proved algebraically.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

import w33_pass7130_7137_structural_attack as p

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7138_7145_C2_NORMALFORM_MATRIX_QUOTIENT.json'

# Dual Lagrangian bases for the q=9 involution.  In this basis A=diag(I2,-I2)
# and B((u,w),(u',w')) = u.w' - w.u'.
E9=[[5,4,1,0],[1,5,0,1]]
F9=[[0,6,6,6],[0,6,8,8]]
# q=7: scale the projective involution A7 by 4=2^{-1}; same projective map.
E7=[[1,0,0,0],[0,0,1,0]]
F7=[[3,1,2,0],[2,0,1,1]]


def invp(M,q):
    n=len(M); A=[list(M[i])+[1 if i==j else 0 for j in range(n)] for i in range(n)]
    for c in range(n):
        k=next(i for i in range(c,n) if A[i][c]%q); A[c],A[k]=A[k],A[c]
        z=pow(A[c][c]%q,-1,q); A[c]=[x*z%q for x in A[c]]
        for i in range(n):
            if i!=c and A[i][c]%q:
                f=A[i][c]%q; A[i]=[(A[i][j]-f*A[c][j])%q for j in range(2*n)]
    return [r[n:] for r in A]


def norm2_9(v):
    if not any(v): return (0,0)
    z=p.INV[next(x for x in v if x)]
    return tuple(p.gm(z,x) for x in v)


def norm2_p(v,q):
    if not any(x%q for x in v): return (0,0)
    z=pow(next(x for x in v if x%q),-1,q)
    return tuple(x*z%q for x in v)


def cols_to_matrix(cols): return [[cols[j][i] for j in range(len(cols))] for i in range(len(cols[0]))]


def outer9(w,u): return (p.gm(w[0],u[0]),p.gm(w[0],u[1]),p.gm(w[1],u[0]),p.gm(w[1],u[1]))


def trace9_flat(X): return p.ga(X[0],X[3])


def canonical_anchor_G(rep):
    # matching-product coordinates are [g12*g34, g13*g42, g14*g23]=[x,y,z]
    x,y,z=rep
    return [[0,1,1,1],
            [2,0,z,p.gn(y)],
            [2,p.gn(z),0,x],
            [2,y,p.gn(x),0]]


def pair_value9(r,Gi,s):
    tmp=[p.gsum(p.gm(r[k],Gi[k][j]) for k in range(4)) for j in range(4)]
    return p.gn(p.gsum(p.gm(tmp[j],s[j]) for j in range(4)))


def quotient_from_graph(P,adj,perm):
    seen=set(); orbs=[]
    for v in range(len(P)):
        if v in seen: continue
        o=tuple(sorted(set([v,perm[v]]))); seen.update(o); orbs.append(o)
    eligible=[]; bad=[]
    for o in orbs:
        if len(o)==1 or o[1] not in adj[o[0]]: eligible.append(o)
        else: bad.append(o)
    edges=[]
    for i,oi in enumerate(eligible):
        for j in range(i+1,len(eligible)):
            oj=eligible[j]
            if any(v in adj[u] for u in oi for v in oj): edges.append((i,j))
    deg=[0]*len(eligible)
    for a,b in edges: deg[a]+=1; deg[b]+=1
    return orbs,eligible,bad,edges,deg


def canonical_prime_quotient(q):
    def norm(v):
        z=pow(next(x for x in v if x%q),-1,q); return tuple(x*z%q for x in v)
    P=sorted(set(norm(v) for v in itertools.product(range(q),repeat=4) if any(v)))
    I={x:i for i,x in enumerate(P)}
    def B(u,v): return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%q
    adj=[set() for _ in P]
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            if B(P[i],P[j])==0: adj[i].add(j); adj[j].add(i)
    perm={i:I[norm((P[i][0],P[i][1],-P[i][2]%q,-P[i][3]%q))] for i in range(len(P))}
    _,eligible,_,edges,_=quotient_from_graph(P,adj,perm)
    A=np.zeros((len(eligible),len(eligible)),dtype=np.int8)
    for i,j in edges: A[i,j]=A[j,i]=1
    ev=np.linalg.eigvalsh(A)
    clusters=Counter(round(float(x),7) for x in ev)
    return len(P),len(eligible),len(edges),clusters


def expected_spectrum(q):
    D=(2*q*q-7*q+9)*(2*q*q+q+1)
    ctr=(2*q*q+q+1)/4
    rad=D**0.5/4
    rows=[
      (q-1,(q+1)*(q*q-3*q+4)//4),
      (-(q+1),q*(q-3)*(q-1)//4),
      (-(q+3)/2,q*(q+1)//2),
      ((q-1)/2,(q-1)*(q+2)//2),
      (0,q*(q-3)//2),
      (-(q-1),q),
      (ctr-rad,1),(ctr+rad,1)]
    c=Counter()
    for val,m in rows:
        if m: c[round(float(val),7)]+=m
    return c


def colored_aut_count(M,kind):
    n=len(M); M2=M@M; G=nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1,n):
            if kind=='symmetric': col=int(M[i,j]*M2[i,j])
            else: col=abs(int(M2[i,j]))
            G.add_edge(i,j,c=col)
    em=nx.algorithms.isomorphism.categorical_edge_match('c',None)
    return sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G,G,edge_match=em).isomorphisms_iter())


def compose(a,b): return tuple(a[b[i]] for i in range(len(a)))


def main():
    P9,I9,adj9=p.build9(); W9=[P9[i] for i in p.S9]
    P7,I7,adj7=p.buildp(7); W7=[P7[i] for i in p.S7]

    # 7138: diagonal C2 normal form and transversal decomposition.
    M9=cols_to_matrix(E9+F9); M9i=p.invmat9(M9)
    D9=p.matmul9(M9i,p.matmul9(p.A9,M9))
    assert D9==[[1,0,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,2]]
    assert [[p.B9(E9[i],F9[j]) for j in range(2)] for i in range(2)]==[[1,0],[0,1]]
    coords9=[p.norm9(p.matvec9(M9i,v)) for v in W9]
    C9map={p.norm9(p.matvec9(M9i,P9[i])):i for i in range(820)}
    def flip9(c): return p.norm9((c[0],c[1],p.gn(c[2]),p.gn(c[3])))
    seen=set(); pairs9=[]; fixed9=[]
    for c in coords9:
        gi=C9map[c]
        if gi in seen: continue
        gj=C9map[flip9(c)]; o=tuple(sorted(set([gi,gj]))); seen.update(o)
        if len(o)==1: fixed9.append(o[0]); continue
        cc=p.norm9(p.matvec9(M9i,P9[o[0]]))
        u=norm2_9(cc[:2]); w=norm2_9(cc[2:])
        # normalize the whole point by the leading u coordinate, then read t*w0
        su=p.INV[next(x for x in cc[:2] if x)]
        ww=[p.gm(su,x) for x in cc[2:]]; t=next(x for x in ww if x)
        tc=min(t,p.gn(t)); pairs9.append((o,u,w,tc))
    assert fixed9==[80] and len(pairs9)==25 and len({(u,w) for _,u,w,_ in pairs9})==25
    left9=Counter(u for _,u,_,_ in pairs9); right9=Counter(w for _,_,w,_ in pairs9)

    A7s=[[4*x%7 for x in row] for row in p.A7]
    M7=cols_to_matrix(E7+F7); M7i=invp(M7,7)
    D7=p.matmul_p(M7i,p.matmul_p(A7s,M7,7),7)
    assert D7==[[1,0,0,0],[0,1,0,0],[0,0,6,0],[0,0,0,6]]
    assert [[p.Bp(E7[i],F7[j],7) for j in range(2)] for i in range(2)]==[[1,0],[0,1]]

    # 7139: exact 52-set Gram gauge reduction to eight 512-state clique cases.
    reps={p.canon3_9(t) for t in itertools.product(range(9),repeat=3)}
    anchor_types=sorted(r for r in reps if all(r) and p.gsum(r)!=0)
    assert anchor_types==[(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)]
    states=[(1,a,b,c) for a in range(1,9) for b in range(1,9) for c in range(1,9)]
    graph_stats={}
    for rep in anchor_types:
        Gi=p.invmat9(canonical_anchor_G(rep)); edges=0; deg=[0]*512
        for i in range(512):
            for j in range(i+1,512):
                if pair_value9(states[i],Gi,states[j])!=0:
                    edges+=1; deg[i]+=1; deg[j]+=1
        graph_stats[str(rep)]={'vertices':512,'edges':edges,'degree_min':min(deg),'degree_max':max(deg)}
    expected_edges={(1,1,2):116412,(1,1,3):116430,(1,1,4):116430,(1,1,5):116430,
                    (1,2,3):116421,(1,2,4):116421,(1,3,4):116430,(1,3,5):116430}
    assert all(graph_stats[str(k)]['edges']==v for k,v in expected_edges.items())
    anchors=[0,1,2,5]
    Gold=[[p.B9(W9[i],W9[j]) for j in anchors] for i in anchors]
    trip=(p.gm(Gold[0][1],Gold[2][3]),p.gm(Gold[0][2],Gold[3][1]),p.gm(Gold[0][3],Gold[1][2]))
    assert p.canon3_9(trip)==(1,3,5)
    Giold=p.invmat9(Gold); known_rows=[]
    for i in range(51):
        if i in anchors: continue
        r=tuple(p.B9(W9[i],W9[a]) for a in anchors); z=p.INV[r[0]]
        known_rows.append(tuple(p.gm(z,x) for x in r))
    assert len(set(known_rows))==47 and all(all(r) and r[0]==1 for r in known_rows)
    assert all(pair_value9(a,Giold,b)!=0 for a,b in itertools.combinations(known_rows,2))

    # 7140/7141: all-q quotient geometry; exact q=7,q=9 counts plus spectral anchors.
    g9={v:I9[p.norm9(p.matvec9(p.A9,P9[v]))] for v in range(820)}
    o9,e9,b9,qe9,qd9=quotient_from_graph(P9,adj9,g9)
    assert Counter(map(len,o9))==Counter({2:400,1:20})
    assert Counter(map(len,e9))==Counter({2:360,1:20}) and len(b9)==40 and len(qe9)==14500
    assert Counter(qd9[i] for i,o in enumerate(e9) if len(o)==1)==Counter({46:20})
    assert Counter(qd9[i] for i,o in enumerate(e9) if len(o)==2)==Counter({78:360})
    g7={v:I7[p.normp(p.matvec_p(p.A7,P7[v],7),7)] for v in range(400)}
    o7,e7,b7,qe7,qd7=quotient_from_graph(P7,adj7,g7)
    assert Counter(map(len,e7))==Counter({2:168,1:16}) and len(b7)==24 and len(qe7)==4180
    assert Counter(qd7[i] for i,o in enumerate(e7) if len(o)==1)==Counter({29:16})
    assert Counter(qd7[i] for i,o in enumerate(e7) if len(o)==2)==Counter({47:168})
    spectrum_anchors={}
    for q in (3,5,7):
        vv,nn,ee,spc=canonical_prime_quotient(q); assert spc==expected_spectrum(q)
        spectrum_anchors[str(q)]={'ambient_points':vv,'quotient_nodes':nn,'quotient_edges':ee,'spectrum':dict(sorted(spc.items()))}
    # q=9 uses GF(9), not Z/9.
    AQ=np.zeros((len(e9),len(e9)),dtype=np.int8)
    for i,j in qe9: AQ[i,j]=AQ[j,i]=1
    sp9=Counter(round(float(x),7) for x in np.linalg.eigvalsh(AQ)); assert sp9==expected_spectrum(9)
    spectrum_anchors['9']={'ambient_points':820,'quotient_nodes':380,'quotient_edges':14500,'spectrum':dict(sorted(sp9.items()))}

    # 7142: quadratic-character switching objects and exact extended automorphism upper bounds.
    def chi9(a): return 0 if a==0 else (1 if p.gp(a,4)==1 else -1)
    Q9=np.zeros((51,51),dtype=np.int64)
    for i in range(51):
        for j in range(51):
            if i!=j: Q9[i,j]=chi9(p.B9(W9[i],W9[j]))
    Q7=np.zeros((33,33),dtype=np.int64)
    for i in range(33):
        for j in range(33):
            if i!=j:
                a=p.Bp(W7[i],W7[j],7); Q7[i,j]=1 if pow(a,3,7)==1 else -1
    assert np.array_equal(Q9,Q9.T) and np.array_equal(Q7,-Q7.T)
    assert p.rank_mod(Q9,5)==51 and p.rank_mod(Q7,3)==32
    assert not np.array_equal(Q9@Q9,50*np.eye(51,dtype=np.int64))
    assert not np.array_equal(Q7@Q7,-32*np.eye(33,dtype=np.int64))
    assert colored_aut_count(Q9,'symmetric')==2 and colored_aut_count(Q7,'skew')==2
    pos9={v:i for i,v in enumerate(p.S9)}; pi9=[pos9[g9[v]] for v in p.S9]
    d9=[1]*51
    for j in range(1,51): d9[j]=int(Q9[pi9[0],pi9[j]]*Q9[0,j])
    assert all(Q9[pi9[i],pi9[j]]==d9[i]*d9[j]*Q9[i,j] for i in range(51) for j in range(51))
    pos7={v:i for i,v in enumerate(p.S7)}; pi7=[pos7[g7[v]] for v in p.S7]
    d7=[1]*33
    for j in range(1,33): d7[j]=int(-Q7[pi7[0],pi7[j]]*Q7[0,j])
    assert all(Q7[pi7[i],pi7[j]]==-d7[i]*d7[j]*Q7[i,j] for i in range(33) for j in range(33))

    # 7143: transversal carriers are rank-one trace-one idempotents in M2(Fq).
    idems9=[]
    for _,u,w,_ in pairs9:
        X=outer9(w,u); tr=p.ga(X[0],X[3]); Y=tuple(p.gm(p.INV[tr],x) for x in X)
        Ym=[[Y[0],Y[1]],[Y[2],Y[3]]]
        YY=p.matmul9(Ym,Ym); assert tuple(YY[0]+YY[1])==Y and trace9_flat(Y)==1
        idems9.append(Y)
    assert len(set(idems9))==25
    all_idem9=[]
    for a,b,c in itertools.product(range(9),repeat=3):
        d=p.ga(1,p.gn(a))
        if p.ga(p.gm(a,d),p.gn(p.gm(b,c)))==0: all_idem9.append((a,b,c,d))
    assert len(all_idem9)==90 # q(q+1)

    # 7144: semilinear <A,F> closure is dihedral of order 12 and produces a six-witness hexad.
    Fperm=tuple(I9[p.norm9(tuple(p.fr(x) for x in P9[v]))] for v in range(820))
    Aperm=tuple(g9[v] for v in range(820)); ident=tuple(range(820))
    group={ident}; front=[ident]
    while front:
        h=front.pop()
        for gen in (Aperm,Fperm):
            z=compose(gen,h)
            if z not in group: group.add(z); front.append(z)
    assert len(group)==12
    AF=compose(Aperm,Fperm); z=ident; order=0
    while True:
        order+=1; z=compose(AF,z)
        if z==ident: break
    assert order==6
    Sset=set(p.S9); witness_sets=[]
    for h in group:
        T=frozenset(h[v] for v in Sset)
        if T not in witness_sets: witness_sets.append(T)
    assert len(witness_sets)==6 and all(len(T)==51 for T in witness_sets)
    assert all(not any(v in adj9[u] for u,v in itertools.combinations(T,2)) for T in witness_sets)
    ints=[len(a&b) for a,b in itertools.combinations(witness_sets,2)]; assert Counter(ints)==Counter({4:15})
    union=set().union(*witness_sets); multiplicity=Counter(sum(v in T for T in witness_sets) for v in union)
    triple=sorted(v for v in union if sum(v in T for T in witness_sets)==3)
    assert len(union)==248 and multiplicity==Counter({1:192,2:54,3:2}) and triple==[50,80]
    assert Counter((50 in T,80 in T) for T in witness_sets)==Counter({(True,False):3,(False,True):3})

    # 7145: the hexad gives a D12-invariant binary [248,6,51] code with Gram I6 mod 2.
    masks=[sum(1<<v for v in T) for T in witness_sets]
    weights=Counter()
    for m in range(64):
        z=0
        for i in range(6):
            if (m>>i)&1: z^=masks[i]
        weights[z.bit_count()]+=1
    assert weights==Counter({0:1,51:6,94:15,129:18,133:2,156:9,160:6,179:6,194:1})
    integer_gram=[[len(witness_sets[i]&witness_sets[j]) for j in range(6)] for i in range(6)]
    assert integer_gram==[[51 if i==j else 4 for j in range(6)] for i in range(6)]

    out={
      'schema':'w33.pass7138_7145.c2_normalform_matrix_quotient.v1','status':'PASS',
      'boundary':'Exact finite symplectic/matrix/coding statements unless explicitly marked conjectural. No q=9 optimality, physics, particle, coupling, continuum, or hardware claim.',
      'pass_7138_eigenspace_transversal_normal_form':{
        'q9_basis_Eplus':E9,'q9_basis_Eminus_dual':F9,'normal_form':'A=diag(I2,-I2), B((u,w),(u_prime,w_prime))=u.w_prime-w.u_prime',
        'q9_witness_orbits':'1 fixed + 25 two-cycles','fixed_point':80,'distinct_selected_transversals':25,
        'left_endpoint_degree_multiset':dict(sorted(Counter(left9.values()).items())),'right_endpoint_degree_multiset':dict(sorted(Counter(right9.values()).items())),
        'geometric_statement':'Each nonfixed orbit lies on a unique transversal joining the two fixed generator lines; on a nonisotropic transversal the q-1 internal points split into (q-1)/2 C2 pairs t<->-t.'},
      'pass_7139_52set_gram_gauge_reduction':{
        'raw_off_diagonal_pairings':1326,'rank4_anchor_variables_before_projective_gauge':198,'canonical_nonzero_nondegenerate_anchor_types':anchor_types,
        'number_anchor_types':8,'normalized_row_state_space':512,'normalized_row_form':'(1,a,b,c), a,b,c in GF(9)^*',
        'continuous_field_variables_per_anchor_case':144,'target':'48-clique among 512 row states after fixing four anchors',
        'compatibility_graph_stats':graph_stats,'known_51_anchor_type':[1,3,5],'known_witness_remaining_clique':47,
        'scope':'This is an exact exhaustive reduction of any hypothetical 52-set to eight finite clique cases. No 48-clique impossibility is claimed.'},
      'pass_7140_allq_involution_theorem':{
        'theorem':'For odd q, a non-scalar projective involutory symplectic similitude with multiplier -1 has two 2D Lagrangian eigenspaces E+ and E-. Its fixed projective locus is two disjoint generator lines. A g-invariant partial ovoid contains at most one point from each fixed line; hence an odd-sized invariant partial ovoid contains exactly one fixed point.',
        'fixed_projective_points':'2(q+1)','nonfixed_orbits':'(q-1)(q+1)^2/2','self_adjacent_nonfixed_orbits':'(q^2-1)/2',
        'eligible_nonfixed_pair_orbits':'q(q^2-1)/2','nonisotropic_transversals':'q(q+1)','labels_per_transversal':'(q-1)/2'},
      'pass_7141_c2_quotient_graph':{
        'allq_selectable_nodes':'2(q+1) fixed weight-1 nodes + q(q^2-1)/2 eligible weight-2 nodes',
        'allq_degrees':{'fixed':'(q^2+q+2)/2','pair':'(2q^2-q+3)/2'},
        'allq_edge_counts':{'fixed_fixed':'(q+1)^2','fixed_pair':'q(q^2-1)','pair_pair':'q(q^2-1)(2q^2-q-1)/8'},
        'q7':{'nodes':184,'edges':4180,'degree_fixed':29,'degree_pair':47},'q9':{'nodes':380,'edges':14500,'degree_fixed':46,'degree_pair':78},
        'spectrum_formula_status':'CONJECTURE verified computationally at q=3,5,7,9; not promoted to all-q theorem',
        'candidate_spectrum_multiplicities':{
          'q-1':'(q+1)(q^2-3q+4)/4','-(q+1)':'q(q-3)(q-1)/4','-(q+3)/2':'q(q+1)/2',
          '(q-1)/2':'(q-1)(q+2)/2','0':'q(q-3)/2','-(q-1)':'q',
          'two_simple_roots':'2x^2-(2q^2+q+1)x+(2q^3-q^2-1)=0'},
        'anchors':spectrum_anchors},
      'pass_7142_quadratic_character_switching':{
        'q9':{'matrix':'symmetric Seidel','rank_Q':51,'conference':False,'switching_invariant_pair_color_aut_order':2,'extended_switching_group':'C2','known_involution_global_sign':1,'switch_signs':dict(Counter(d9))},
        'q7':{'matrix':'skew sign','rank_Q':32,'conference':False,'absolute_Q2_pair_color_aut_order':2,'extended_plusminus_switching_group':'C2','known_involution_global_sign':-1,'switch_signs':dict(Counter(d7))},
        'boundary':'The sign flip between q=1 and 3 mod 4 is finite-field quadratic-character algebra, not physical chirality.'},
      'pass_7143_rankone_idempotent_bridge':{
        'allq_statement':'A nonisotropic transversal ([u],[w]) has u.w !=0 and canonically determines E=w u^T/(u.w), a rank-one trace-one idempotent. Conversely every rank-one trace-one idempotent gives one such transversal.',
        'allq_idempotent_count':'q(q+1)','q9_all_idempotents':90,'q9_selected_distinct_idempotents':25,'q7_selected_transversals':16,
        'repo_interface':'This is a genuine M2(F_q) bridge to the earlier rank stratification, but not the same object as the full rank-one Fourier sector. At q=2 there are 6 trace-one rank-one idempotents versus 9 nonzero rank-one matrices; the 6 idempotents are rank-one and therefore are not the 6 units.'},
      'pass_7144_semilinear_D12_hexad':{
        'generators':['projective A','field Frobenius F'],'group_order':12,'product_AF_order':6,'group':'dihedral order 12',
        'orbit_of_witness_size':6,'each_set_size':51,'all_15_pair_intersections':4,'union_size':248,
        'union_point_multiplicity':dict(multiplicity),'triple_points':triple,'triple_point_memberships':'50 occurs in 3 sets, 80 occurs in the complementary 3; no hexad set contains both',
        'binary_pair_distance':94},
      'pass_7145_hexad_binary_code':{
        'length_after_puncturing_to_union':248,'dimension':6,'minimum_distance':51,
        'weight_enumerator':{str(k):v for k,v in sorted(weights.items())},
        'generator_integer_gram':'47 I_6 + 4 J_6','gram_eigenvalues':'71^1 + 47^5','gram_determinant':'71*47^5',
        'generator_gram_mod2':'I_6','interpretation':'Six D12-related partial-ovoid incidence words are linearly independent over F2 and pairwise distance 94.'}
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0

if __name__=='__main__': raise SystemExit(main())
