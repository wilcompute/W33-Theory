#!/usr/bin/env python3
"""Pass 4804 — upgrade the cube/F4 GQ(4,2) crosswalk to an equivariant intertwiner.

Pass4797 supplied an incidence isomorphism between the 45 dependency-cube
triality packets and the independent F4-normalizer compiler quotient.  Here we
retain the group actions.

Source: PSp(4,3) acts on the 45 three-cube packets; PGSp adds the genuine outer
C2 and has a faithful 51840-element projective action.
Target: the 51840-element compiler group is the *central* Sp(4,3) double cover.
Its action on the 45 F4 cosets has central kernel 2 and therefore image PSp of
order 25920.

After the Pass4797 point isomorphism m, conjugation p -> m p m^{-1} identifies
exactly the two 25920-element permutation images.  Thus the incidence map is
PSp-equivariant.  The two 51840 extensions remain different: the source PGSp
outer extension doubles the permutation image, whereas the central compiler Sp
extension does not.
"""
from __future__ import annotations
import itertools,json,hashlib
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
from w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import build_group,generator_set,mat_mul
from w33_BREAKTHROUGH_158_macro_tail_sieve import macro_tail_sieve_packet
from w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import closure_generated_by
from w33_BREAKTHROUGH_167_f4_e6_rank3_coset_quotient import left_cosets
from w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import quotient_adjacency,five_cliques
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4804_EQUIVARIANT_F4_E6_INTERTWINER.json'

def source_packet_action():
    pts,pidx,lines,A,_,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[tuple(C) for C in itertools.combinations(range(40),4) if not np.any(np.sum(A[:,C],axis=1)&1)]
    assert len(residues)==270;ridx={r:i for i,r in enumerate(residues)};rm=[sum(1<<x for x in r) for r in residues]
    cold=[set() for _ in residues]
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold[i].add(j);cold[j].add(i)
    tri=[]
    for a in range(270):
        for b in (x for x in cold[a] if x>a):
            for c in cold[a]&cold[b]:
                if c>b:tri.append((a,b,c))
    dep=[t for t in tri if rm[t[0]]^rm[t[1]]^rm[t[2]]==0];non=[t for t in tri if rm[t[0]]^rm[t[1]]^rm[t[2]]]
    assert len(dep)==len(non)==540
    ed={tuple(sorted(e)):i for i,t in enumerate(dep) for e in itertools.combinations(t,2)}
    en={tuple(sorted(e)):i for i,t in enumerate(non) for e in itertools.combinations(t,2)}
    adj=[set() for _ in range(1080)]
    for e in ed:
        a=ed[e];b=540+en[e];adj[a].add(b);adj[b].add(a)
    cubes=[];seen=set()
    for s in range(1080):
        if s in seen:continue
        st=[s];seen.add(s);V=[]
        while st:
            u=st.pop();V.append(u)
            for v in adj[u]:
                if v not in seen:seen.add(v);st.append(v)
        R=set()
        for u in V:R.update(dep[u] if u<540 else non[u-540])
        assert len(V)==8 and len(R)==6;cubes.append(frozenset(R))
    assert len(cubes)==135;cidx={C:i for i,C in enumerate(cubes)}
    _,G,F=build_groups(pts,pidx,lines);G=set(G);F=set(F);assert len(G)==25920 and len(F)==51840
    def ar(i,g):return ridx[tuple(sorted(g[x] for x in residues[i]))]
    def ac(i,g):return cidx[frozenset(ar(r,g) for r in cubes[i])]
    H=[g for g in G if ac(0,g)==0];assert len(H)==192
    fixed=[i for i in range(135) if all(ac(i,g)==i for g in H)];assert len(fixed)==3
    B0=frozenset(fixed)
    blocks=sorted({frozenset(ac(i,g) for i in B0) for g in G},key=lambda X:tuple(sorted(X)));assert len(blocks)==45
    bidx={B:i for i,B in enumerate(blocks)}
    def ab(i,g):return bidx[frozenset(ac(c,g) for c in blocks[i])]
    psp={tuple(ab(i,g) for i in range(45)) for g in G};outer={tuple(ab(i,g) for i in range(45)) for g in F}
    assert len(psp)==25920 and len(outer)==51840
    Q=nx.Graph();Q.add_nodes_from(range(45))
    # adjacency is the unique degree-12 packet relation reconstructed from cube intersections
    um=[]
    for C in cubes:
        u=0
        for r in C:u|=rm[r]
        um.append(u)
    mult=Counter()
    cube_to_block={c:i for i,B in enumerate(blocks) for c in B}
    for i,j in itertools.combinations(range(135),2):
        if (um[i]&um[j]).bit_count()==4:
            a,b=cube_to_block[i],cube_to_block[j]
            if a!=b:mult[tuple(sorted((a,b)))]+=1
    Q.add_edges_from(mult);assert Q.number_of_edges()==270 and set(dict(Q.degree()).values())=={12}
    return Q,psp,outer

def target_compiler_action():
    tail=macro_tail_sieve_packet();forbidden=[tuple(tuple(x for x in row) for row in item['matrix']) for item in tail['forbidden_macros']]
    N=closure_generated_by(forbidden);assert len(N)==1152
    gens,_=generator_set(include_inverses=True);elems,_,_,_=build_group(gens);assert len(elems)==51840
    reps,cosets,e2c=left_cosets(elems,N);assert len(reps)==45
    # All central-cover elements, projected to the degree-45 coset action.
    image=set()
    for h in elems:
        image.add(tuple(e2c[mat_mul(reps[i],h)] for i in range(45)))
    assert len(image)==25920  # central kernel of order two
    A,_=quotient_adjacency();Q=nx.Graph();Q.add_nodes_from(range(45));Q.add_edges_from((i,j) for i in range(45) for j in range(i+1,45) if A[i][j])
    return Q,image

def conjugate_perm(p,m):
    # m maps source vertices -> target vertices.
    q=[None]*45
    for i in range(45):q[m[i]]=m[p[i]]
    return tuple(q)

def main()->int:
    src,src_psp,src_outer=source_packet_action();tgt,tgt_psp=target_compiler_action()
    GM=nx.algorithms.isomorphism.GraphMatcher(src,tgt);mpd=next(GM.isomorphisms_iter(),None);assert mpd is not None
    m=tuple(mpd[i] for i in range(45));assert len(set(m))==45
    conj={conjugate_perm(p,m) for p in src_psp};assert conj==tgt_psp
    conj_outer={conjugate_perm(p,m) for p in src_outer};assert len(conj_outer)==51840 and tgt_psp < conj_outer
    # The central compiler extension has 51840 matrices but only 25920 permutations;
    # the outer PGSp extension has 51840 distinct degree-45 permutations.
    digest=hashlib.sha256(','.join(map(str,m)).encode()).hexdigest()
    out={'pass':4804,'degree':45,'point_mapping_sha256':digest,
      'source_PSp_permutation_image_order':len(src_psp),'target_compiler_permutation_image_order':len(tgt_psp),
      'PSp_images_conjugate_exactly':True,'source_PGSp_outer_image_order':len(src_outer),
      'compiler_Sp_matrix_group_order':51840,'compiler_Sp_degree45_image_order':25920,'compiler_central_kernel_order':2,
      'outer_extension_degree45_image_order':51840,
      'theorem':'The Pass4797 dependency-cube/F4 GQ(4,2) crosswalk can be chosen PSp-equivariantly: conjugating by the explicit 45-point map sends the complete 25920-element source PSp permutation image exactly onto the compiler quotient image. The central Sp(4,3) and outer PGSp extensions remain sharply separated on the same 45-set.',
      'extension_firewall':'Central Sp(4,3): 51840 matrices -> 25920 degree-45 permutations with kernel 2. Outer PGSp: 51840 distinct degree-45 permutations. Equality of orders is not an extension identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
