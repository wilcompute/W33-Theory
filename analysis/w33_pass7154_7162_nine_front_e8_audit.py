#!/usr/bin/env python3
"""Passes 7154--7162: nine-front closure packet.

Exact finite computations supporting:
7154 anchor-torus/rank stratification and coherent-color data;
7155 the normalized Gram state big cell inside PGL2(9);
7156 the missing geometric invariant inside S3 wr C2 (a Hamiltonian C6 in K3,3);
7157 higher-rank symplectic involution-pair geometry;
7158 the witness orbit as a homogeneous hexagon bundle G/C2 -> G/D12;
7159 the 23-column / 40-complement binary projective probe;
7160 exhaustive local [8,4,4] affine-flat puncture search;
7161 Construction-A and invariant 240+8 firewalls for the [248,6,51] code;
7162 an E8 audit: positive local Hamming interfaces versus rejected global 248 numerology.
"""
from __future__ import annotations

import itertools, json, math
from collections import Counter, defaultdict
from pathlib import Path

import w33_pass7130_7137_structural_attack as p
import w33_pass7138_7145_c2_normalform_matrix_quotient as q
import w33_pass7147_7153_pgl2_hexad_code_closure as h

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7154_7162_NINE_FRONT_E8_AUDIT.json'
TYPES=[(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)]
STATES=[(1,a,b,c) for a in range(1,9) for b in range(1,9) for c in range(1,9)]


def rank2_gf9(r):
    # reshape normalized row into [[1,a],[b,c]]
    return 1 if r[3]==p.gm(r[1],r[2]) else 2


def anchor_rank_degree_data():
    assert Counter(rank2_gf9(r) for r in STATES)==Counter({2:448,1:64})
    out={}
    for rep in TYPES:
        Gi=p.invmat9(q.canonical_anchor_G(rep))
        deg=[0]*512; byrank=[[0,0] for _ in range(512)]
        for i in range(512):
            ri=rank2_gf9(STATES[i])-1
            for j in range(i+1,512):
                if q.pair_value9(STATES[i],Gi,STATES[j])==0:
                    rj=rank2_gf9(STATES[j])-1
                    deg[i]+=1; deg[j]+=1
                    byrank[i][rj]+=1; byrank[j][ri]+=1
        joint=Counter((rank2_gf9(STATES[i]),deg[i]) for i in range(512))
        profiles={str(r):dict(sorted(Counter(tuple(byrank[i]) for i in range(512) if rank2_gf9(STATES[i])==r).items())) for r in (1,2)}
        out[str(rep)]={
            'conflict_edges':sum(deg)//2,
            'degree_distribution':dict(sorted(Counter(deg).items())),
            'rank_degree_distribution':{f'rank{r}_deg{d}':n for (r,d),n in sorted(joint.items())},
            'rank_neighbor_profile_histogram':profiles,
            'rank_partition_equitable':all(len(Counter(tuple(byrank[i]) for i in range(512) if rank2_gf9(STATES[i])==r))==1 for r in (1,2)),
        }
    return out


def pgl2_big_cell():
    sing=[r for r in STATES if rank2_gf9(r)==1]
    inv=[r for r in STATES if rank2_gf9(r)==2]
    assert len(sing)==64 and len(inv)==448
    # D=diag(1,-1) acts on normalized matrices by (1,a,b,c)->(1,a,-b,-c).
    def D(r): return (1,r[1],p.gn(r[2]),p.gn(r[3]))
    assert all(rank2_gf9(D(r))==2 for r in inv)
    seen=set(); orbs=[]
    for r in inv:
        if r in seen: continue
        o=frozenset((r,D(r))); assert len(o)==2
        seen.update(o); orbs.append(o)
    assert len(orbs)==224
    return {
      'normalized_state_space':'all 2x2 matrices [[1,a],[b,c]] with a,b,c in GF(9)^*',
      'total_states':512,'rank_one_boundary':64,'invertible_big_cell':448,
      'invertible_formula':'(q-1)^2(q-2) at q=9','rank_one_formula':'(q-1)^2 at q=9',
      'PGL2_9_order':720,'PGL2_over_C2_nodes':360,
      'big_cell_C2_orbits':224,'quotient_nodes_outside_big_cell':136,
      'interface':'The 448 invertible normalized rows inject as the all-entry-nonzero big cell of PGL2(9); quotienting by D gives 224 of the 360 PGL2(9)/<D> pair nodes.',
      'obstruction':'The full 512-state Gram graph cannot itself be a cover or relabeling of the 360-node involution quotient: 64 states are rank-one boundary matrices and 136 quotient cosets lie outside the all-entry-nonzero big cell.'
    }


def perm_mask(mask,perm):
    z=0
    for i in range(6):
        if (mask>>i)&1: z|=1<<perm[i]
    return z


def closure_perms(gens,n=6):
    ident=tuple(range(n)); G={ident}; front=[ident]
    while front:
        a=front.pop()
        for b in gens:
            c=tuple(a[b[i]] for i in range(n))
            if c not in G: G.add(c); front.append(c)
            c=tuple(b[a[i]] for i in range(n))
            if c not in G: G.add(c); front.append(c)
    return G


def hexad_cycle_obstruction():
    P9,sets,union,cm,triple_masks,outer,C,dual,shell,triple_pts,one,both,Aperm,Fperm=h.build_hexad()
    T0=tuple(i for i in range(6) if (triple_masks[0]>>i)&1)
    T1=tuple(i for i in range(6) if (triple_masks[1]>>i)&1)
    assert len(T0)==len(T1)==3 and set(T0).isdisjoint(T1)
    pa=tuple(sets.index(frozenset(Aperm[v] for v in T)) for T in sets)
    pf=tuple(sets.index(frozenset(Fperm[v] for v in T)) for T in sets)
    geom=closure_perms((pa,pf)); assert len(geom)==12
    # order-six rotation AF gives the geometrically selected Hamiltonian cycle.
    rot=tuple(pa[pf[i]] for i in range(6))
    z=tuple(range(6)); order=0
    while True:
        order+=1; z=tuple(rot[z[i]] for i in range(6))
        if z==tuple(range(6)): break
    assert order==6
    cycle=frozenset(tuple(sorted((i,rot[i]))) for i in range(6))
    assert len(cycle)==6 and all((a in T0)^(b in T0) for a,b in cycle)
    cross=frozenset(tuple(sorted((a,b))) for a in T0 for b in T1); assert len(cross)==9
    matching=cross-cycle; assert len(matching)==3
    assert all(sum(v in e for e in matching)==1 for v in range(6))
    # Exactly six perfect matchings of K3,3, hence six complementary Hamiltonian C6s.
    matchings=[]
    for perm in itertools.permutations(T1):
        M=frozenset(tuple(sorted((T0[i],perm[i]))) for i in range(3)); matchings.append(M)
    matchings=set(matchings); assert len(matchings)==6
    cycles={cross-M for M in matchings}; assert len(cycles)==6 and cycle in cycles
    outer_set=set(outer); assert len(outer_set)==72
    stab={g for g in outer_set if frozenset(tuple(sorted((g[a],g[b]))) for a,b in cycle)==cycle}
    assert len(stab)==12 and stab==geom
    orbit={frozenset(tuple(sorted((g[a],g[b]))) for a,b in cycle) for g in outer_set}; assert orbit==cycles
    return {
      'outer_pattern_group':'Aut(K3,3)=S3 wr C2','outer_order':72,
      'geometric_group':'D12=Aut(C6)','geometric_order':12,'index':6,
      'two_triples':[list(T0),list(T1)],'cross_graph':'K3,3',
      'perfect_matchings_of_K33':6,'hamiltonian_C6_complements':6,
      'selected_geometric_cycle_edges':[list(e) for e in sorted(cycle)],
      'selected_missing_perfect_matching':[list(e) for e in sorted(matching)],
      'theorem':'The code outer group remembers only K3,3 on the two witness triples; ambient geometry selects one of its six Hamiltonian C6s (equivalently one of six perfect matchings to delete). The selected C6 stabilizer inside S3 wr C2 is exactly the geometric D12.',
      'lifting_obstruction':'A code-outer automorphism lifts to the ambient hexad geometry iff it preserves the selected Hamiltonian C6/perfect-matching complement.'
    }


def normp(v,q0):
    z=pow(next(x for x in v if x%q0),-1,q0); return tuple(x*z%q0 for x in v)


def higher_rank_replay(q0=3,n=3):
    pts=sorted(set(normp(v,q0) for v in itertools.product(range(q0),repeat=2*n) if any(v)))
    I={v:i for i,v in enumerate(pts)}
    def B(x,y):
        return sum(x[i]*y[n+i]-x[n+i]*y[i] for i in range(n))%q0
    def Dv(x): return normp(x[:n]+tuple((-x[n+i])%q0 for i in range(n)),q0)
    perm=[I[Dv(x)] for x in pts]
    seen=set(); fixed=[]; eligible=[]; bad=[]
    for i in range(len(pts)):
        if i in seen: continue
        j=perm[i]; o=tuple(sorted(set((i,j)))); seen.update(o)
        if len(o)==1: fixed.append(o)
        elif B(pts[o[0]],pts[o[1]])!=0: eligible.append(o)
        else: bad.append(o)
    pg=(q0**n-1)//(q0-1)
    assert len(fixed)==2*pg
    assert len(eligible)==q0**(n-1)*(q0**n-1)//2
    # Pair conflict is exactly the union of the B(X,Y)=0 and B(X,DY)=0 channels.
    checked=0
    for a,b in itertools.combinations(eligible,2):
        x=pts[a[0]]; y=pts[b[0]]; dy=pts[perm[b[0]]]
        law=(B(x,y)==0 or B(x,dy)==0)
        geom=any(B(pts[i],pts[j])==0 for i in a for j in b)
        assert law==geom; checked+=1
    return {
      'finite_replay':{'q':q0,'n':n,'projective_points':len(pts),'fixed_points':len(fixed),'eligible_pair_nodes':len(eligible),'self_conflicting_pair_nodes':len(bad),'pair_pairs_checked':checked},
      'allq_fixed_points':'2*(q^n-1)/(q-1)',
      'allq_nonisotropic_transversals':'q^(n-1)*(q^n-1)/(q-1)',
      'allq_eligible_pair_nodes':'q^(n-1)*(q^n-1)/2',
      'allq_labels_per_transversal':'(q-1)/2',
      'two_channel_law':'For D(u,w)=(u,-w), two eligible D-orbits conflict iff B(X,Y)=0 or B(X,DY)=0. In coordinates this is the factorization (s u.w_prime)^2-(t u_prime.w)^2.',
      'scope':'This all-q counting/factorization theorem holds in W(2n-1,q) for odd q. The special PGL2(q) Schreier identification is rank-two (n=2) structure and is not asserted in higher rank.'
    }


def homogeneous_hexagon_bundle():
    G=6886425600; H=2; K=12
    total=G//H; base=G//K
    assert base*6==total
    return {
      'ambient_group':'PΓSp(4,9)','G_order':G,'witness_stabilizer_order':H,'hexad_stabilizer_order':K,
      'total_witnesses_in_orbit':total,'hexad_base_size':base,'fiber_size':6,
      'homogeneous_map':'G/C2 -> G/D12','fiber_model':'D12/C2, the six vertices of a hexagon',
      'fiber_cycle_relation':'The order-six AF element supplies a canonical C6 on every fiber by G-transport.',
      'consequence':'The witness orbit is a G-equivariant homogeneous hexagon bundle, not merely an unstructured partition into six-sets.'
    }


def gf2_rank(rows):
    rows=[r for r in rows if r]; rank=0
    for bit in reversed(range(6)):
        k=next((i for i in range(rank,len(rows)) if (rows[i]>>bit)&1),None)
        if k is None: continue
        rows[rank],rows[k]=rows[k],rows[rank]
        for i in range(len(rows)):
            if i!=rank and ((rows[i]>>bit)&1): rows[i]^=rows[rank]
        rank+=1
    return rank


def subspaces_dim3():
    subs=set()
    vec=list(range(1,64))
    for a,b,c in itertools.combinations(vec,3):
        if gf2_rank([a,b,c])<3: continue
        H=frozenset((0,a,b,c,a^b,a^c,b^c,a^b^c)); subs.add(H)
    assert len(subs)==1395
    return subs


def code_column_geometry():
    P9,sets,union,cm,triple_masks,outer,C,dual,shell,triple_pts,one,both,Aperm,Fperm=h.build_hexad()
    distinct=set(cm)
    singles={1<<i for i in range(6)}
    pairs={m for m in range(1,64) if m.bit_count()==2}
    triples=set(triple_masks)
    assert distinct==singles|pairs|triples and len(distinct)==23
    comp=set(range(1,64))-distinct; assert len(comp)==40
    assert Counter(m.bit_count() for m in comp)==Counter({3:18,4:15,5:6,6:1})
    # Orbit sizes on coordinates under the full code automorphism group are obtained from outer mask orbits times repeated-column multiplicities.
    unvisited=set(distinct); mask_orbits=[]
    outer_set=set(outer)
    while unvisited:
        x=next(iter(unvisited)); O={perm_mask(x,g) for g in outer_set}; assert O<=distinct
        unvisited-=O; mask_orbits.append(O)
    coord_orbits=sorted(sum(cm[m] for m in O) for O in mask_orbits)
    assert coord_orbits==[2,18,36,192]
    sums={0}
    for s in coord_orbits: sums|={x+s for x in list(sums)}
    assert 8 not in sums and 240 not in sums
    return distinct,comp,cm,outer_set,{
      'distinct_nonzero_column_types':23,'decomposition':'6 weight1 + 15 weight2 + 2 complementary weight3',
      'PG5_2_nonzero_points':63,'complement_size':40,
      'complement_weight_distribution':dict(sorted(Counter(m.bit_count() for m in comp).items())),
      'full_coordinate_group_orbit_sizes':coord_orbits,
      'no_full_AutC_invariant_8_subset':True,'no_full_AutC_invariant_240_subset':True,
      'warning':'The bare equality 63-23=40 does not identify the complement with W(3,3); a separate natural-form audit is required.'
    }


def alt_rows_from_mask(mask):
    rows=[0]*6; k=0
    for i in range(6):
        for j in range(i+1,6):
            if (mask>>k)&1:
                rows[i]|=1<<j; rows[j]|=1<<i
            k+=1
    return rows


def bil(rows,x,y):
    z=0
    for i in range(6):
        if (x>>i)&1: z^=rows[i]
    return (z&y).bit_count()&1


def is_srg40(rows,pts,target):
    n=40; adj=[set() for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if bil(rows,pts[i],pts[j])==target:
                adj[i].add(j); adj[j].add(i)
    if any(len(a)!=12 for a in adj): return False
    for i in range(n):
        for j in range(i+1,n):
            c=len(adj[i]&adj[j]); want=2 if j in adj[i] else 4
            if c!=want: return False
    return True


def natural_form_audit(comp):
    pts=sorted(comp); nondeg=0; hits=[]
    for m in range(1<<15):
        rows=alt_rows_from_mask(m)
        if gf2_rank(rows)!=6: continue
        nondeg+=1
        # Orthogonality and nonorthogonality are the two most natural alternating-form relations.
        if is_srg40(rows,pts,0): hits.append({'form_mask':m,'relation':0})
        if is_srg40(rows,pts,1): hits.append({'form_mask':m,'relation':1})
    # number of nonsingular alternating 6x6 forms over F2 = |GL6(2)|/|Sp6(2)| = 8888320/1451520? exact enumeration is the certificate.
    return {'alternating_forms_tested':1<<15,'nondegenerate_alternating_forms':nondeg,'W33_parameter_hits':hits,'hit_count':len(hits),
            'scope':'Exhaustive over all alternating bilinear forms on the fixed F2^6 column-coordinate space, testing adjacency B=0 and B=1 on the 40-point complement. It does not exclude unrelated nonlinear graph structures.'}


def affine_hamming_flats(distinct,cm,outer_set):
    flats=set()
    for H in subspaces_dim3():
        for v in range(64):
            A=frozenset(v^x for x in H)
            if 0 in A or not A<=distinct: continue
            flats.add(A)
    good=[]; actual_subsets=0
    for A in sorted(flats,key=lambda z:sorted(z)):
        weights=Counter()
        words=set()
        for a in range(64):
            w=tuple(((a&c).bit_count()&1) for c in sorted(A)); words.add(w)
        for w in words: weights[sum(w)]+=1
        rank=int(round(math.log2(len(words))))
        assert rank==4 and weights==Counter({4:14,0:1,8:1})
        choices=math.prod(cm[c] for c in A); actual_subsets+=choices
        good.append((A,choices))
    # outer-group orbits of affine Hamming flats
    unseen={A for A,_ in good}; orbits=[]
    while unseen:
        A=next(iter(unseen))
        O={frozenset(perm_mask(c,g) for c in A) for g in outer_set}; O&=set(unseen)|{A}
        # full orbit among known flats
        Oall={frozenset(perm_mask(c,g) for c in A) for g in outer_set}; assert Oall<=flats
        unseen-=Oall; orbits.append(Oall)
    rep=sorted(next(iter(good))[0]) if good else []
    return {
      'distinct_type_affine_3flats':len(flats),
      'outer_S3wrC2_orbits':len(orbits),
      'orbit_sizes':sorted(len(O) for O in orbits),
      'all_punctures_are_extended_Hamming_8_4_4':True if flats else False,
      'representative_column_masks':rep,
      'actual_coordinate_8subsets_count':actual_subsets,
      'interpretation':'Each contained affine 3-flat is an 8-column puncturing whose row code is RM(1,3), equivalently the binary extended Hamming [8,4,4] code. Repeated coordinate multiplicities give the counted actual coordinate subsets.',
    }


def construction_A_firewall(cm,outer_set):
    # exact 64-word enumerator from the column multiset
    W=Counter()
    for a in range(64):
        wt=sum(mult for c,mult in cm.items() if ((a&c).bit_count()&1))
        W[wt]+=1
    gram=[[sum(mult for c,mult in cm.items() if ((c>>i)&1) and ((c>>j)&1))%2 for j in range(6)] for i in range(6)]
    assert gram==[[1 if i==j else 0 for j in range(6)] for i in range(6)]
    return {
      'code':'[248,6,51]_2','weight_enumerator':{str(k):v for k,v in sorted(W.items())},
      'generator_gram_mod2':'I6','self_orthogonal':False,'self_dual':False,
      'contains_odd_weight_words':any(k%2 for k in W if k),'doubly_even':False,
      'Construction_A_global_E8_claim':'REJECTED',
      'reason':'The code is not self-orthogonal and has odd weights, so its standard binary Construction-A lattice is not the Type-II self-dual code-lattice mechanism that produces E8 from the extended Hamming [8,4,4] code.'
    }


def e8_root_audit(hamming):
    roots=[]
    # doubled coordinates: type D8 roots (±2,±2,0^6), plus half-integer roots (±1^8) with even parity.
    for i,j in itertools.combinations(range(8),2):
        for a in (-2,2):
            for b in (-2,2):
                v=[0]*8; v[i]=a; v[j]=b; roots.append(tuple(v))
    for signs in itertools.product((-1,1),repeat=8):
        if sum(s<0 for s in signs)%2==0: roots.append(tuple(signs))
    assert len(roots)==240 and len(set(roots))==240 and all(sum(x*x for x in r)==8 for r in roots)
    # rank over Q is visibly 8; verify with an integer Gaussian elimination helper on first independent roots.
    def rankQ(rows):
        from fractions import Fraction
        A=[[Fraction(x) for x in r] for r in rows]; m=len(A); n=8; rr=0
        for c in range(n):
            k=next((i for i in range(rr,m) if A[i][c]),None)
            if k is None: continue
            A[rr],A[k]=A[k],A[rr]; z=A[rr][c]; A[rr]=[x/z for x in A[rr]]
            for i in range(m):
                if i!=rr and A[i][c]:
                    f=A[i][c]; A[i]=[A[i][j]-f*A[rr][j] for j in range(n)]
            rr+=1
            if rr==n: break
        return rr
    assert rankQ(roots)==8
    return {
      'E8_root_count':240,'root_span_rank':8,'adjoint_dimension_identity':'248 = 240 one-dimensional root spaces + 8-dimensional Cartan subalgebra',
      'code_length':248,
      'global_240_plus_8_split_status':'NO CANONICAL CODE-AUTOMORPHISM-INVARIANT SPLIT: coordinate orbit sizes are 192,36,18,2 and no union has size 8 or 240.',
      'direct_Construction_A_status':'REJECTED for the full [248,6,51] code (not self-orthogonal; odd weights).',
      'local_Hamming_interface_status':'POSITIVE' if hamming['distinct_type_affine_3flats'] else 'NONE FOUND',
      'local_interface':'When an 8-column affine 3-flat exists, puncturing to those coordinates gives the extended Hamming [8,4,4] code, whose standard Construction A yields E8. This is a local puncturing interface, not an identification of the 248 coordinates with the 248-dimensional E8 adjoint representation.',
      'boundary':'The equality 248=dim(E8) remains numerology unless supplemented by a Lie bracket/root-Cartan action. The finite tests here explicitly separate the positive local Hamming/E8 lattice interface from the rejected global adjoint identification.'
    }


def main():
    a7154=anchor_rank_degree_data()
    a7155=pgl2_big_cell()
    a7156=hexad_cycle_obstruction()
    a7157=higher_rank_replay()
    a7158=homogeneous_hexagon_bundle()
    distinct,comp,cm,outer_set,a7159=code_column_geometry()
    form_audit=natural_form_audit(comp); a7159['natural_alternating_form_W33_audit']=form_audit
    a7160=affine_hamming_flats(distinct,cm,outer_set)
    a7161=construction_A_firewall(cm,outer_set)
    a7162=e8_root_audit(a7160)
    out={
      'schema':'w33.pass7154_7162.nine_front_e8_audit.v1','status':'PASS',
      'boundary':'Exact finite algebra/code/geometry computations. The unresolved q=9 48-clique decision remains separate; no alpha(W(3,9))=51 claim is made here. E8 statements are restricted to root counts, code-lattice interfaces, and explicit obstructions; no particle or physical identification.',
      'pass_7154_anchor_torus_rank_coherent_data':a7154,
      'pass_7155_gram_PGL2_big_cell_interface':a7155,
      'pass_7156_code_geometry_lifting_obstruction':a7156,
      'pass_7157_higher_rank_involution_pair_theorem':a7157,
      'pass_7158_witness_orbit_hexagon_bundle':a7158,
      'pass_7159_bonkers_23_plus_40_binary_projective_probe':a7159,
      'pass_7160_bonkers_local_Hamming_punctures':a7160,
      'pass_7161_bonkers_Construction_A_firewall':a7161,
      'pass_7162_E8_248_audit':a7162,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0

if __name__=='__main__': raise SystemExit(main())
