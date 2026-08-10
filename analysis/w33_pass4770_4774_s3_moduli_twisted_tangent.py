#!/usr/bin/env python3
"""Passes 4770 and 4774 — exact gauge moduli of the GQ(4,2) S3 connection.

Key observation: the odd elements of S3 are exactly its three transpositions.
Therefore the requirement that every one of the 270 base-triangle holonomies be
a transposition depends ONLY on the sign quotient S3 -> C2.  We solve that
binary affine system exactly in spanning-tree gauge.

Once the sign connection is fixed, write each S3 voltage as r^a s^p with
r^3=s^2=1 and srs=r^-1.  The free A3 exponents form a rank-one F3 local system
twisted by the sign cocycle.  Quotienting even vertex gauge gives its exact
H^1.  When the binary sign solution is unique, connected gauge classes become
nonzero vectors of this twisted H^1 modulo F3^*={+/-1}, i.e. a projective-space
point set.  This is a complete classification modulo vertex gauge; quotienting
further by the 51,840 base automorphisms is left as a finite projective orbit
problem rather than falsely claimed solved.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
from w33_pass4716_selected270_bundle_connection import build_bundle,compose,invperm,orderperm

ROOT=Path(__file__).resolve().parents[1]
OUT0=ROOT/'data/PART_W33_PASS4770_S3_GAUGE_MODULI.json'
OUT4=ROOT/'data/PART_W33_PASS4774_TWISTED_F3_TANGENT.json'
ID=(0,1,2);S3=list(itertools.permutations(range(3)))

def parity(p):
    return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))&1

def rank2(rows,n):
    piv={}
    for x in rows:
        y=int(x)&((1<<n)-1)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def rank3(A):
    A=np.asarray(A,dtype=np.int64).copy()%3;r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]%3),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,3))%3
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%3
        r+=1
        if r==A.shape[0]:break
    return r

def gen_group(gs):
    G={ID};Q=deque([ID])
    while Q:
        x=Q.popleft()
        for g in gs:
            for y in (compose(g,x),compose(invperm(g),x)):
                if y not in G:G.add(y);Q.append(y)
    return G

def main():
    X=build_bundle();G=X['G45'];sig=X['sig'];tris=sorted(set(tuple(sorted(t)) for t in X['projected']))
    assert G.number_of_nodes()==45 and G.number_of_edges()==270 and len(tris)==270
    parent={0:None};order=[0];Q=deque([0])
    while Q:
        u=Q.popleft()
        for v in sorted(G[u]):
            if v not in parent:parent[v]=u;order.append(v);Q.append(v)
    tree={tuple(sorted((v,parent[v]))) for v in order[1:]}
    gauge={0:ID}
    for v in order[1:]:
        p=parent[v];gauge[v]=compose(sig[(p,v)],gauge[p])
    z={}
    for u,v in G.edges():
        z[(u,v)]=compose(invperm(gauge[v]),compose(sig[(u,v)],gauge[u]));z[(v,u)]=invperm(z[(u,v)])
    assert all(z[e]==ID for e in tree)
    cot=sorted(e for e in G.edges() if e not in tree);ci={e:i for i,e in enumerate(cot)};n=len(cot);assert n==226
    psol=0
    for i,e in enumerate(cot):
        if parity(z[e]):psol|=1<<i

    rows=[];aug=[]
    for T in tris:
        m=0
        for e in itertools.combinations(T,2):
            e=tuple(sorted(e))
            if e in ci:m^=1<<ci[e]
        rows.append(m);aug.append(m|(1<<n))
        assert ((m&psol).bit_count()&1)==1
    r=rank2(rows,n);ra=rank2(aug,n+1);assert r==ra
    sign_dim=n-r;sign_solutions=1<<sign_dim

    # The triangle condition is exactly the sign condition because every odd S3
    # element is a transposition.  For every fixed sign vector, each cotree edge
    # has three independent choices in the corresponding parity coset.
    raw_per_sign=3**n
    disconnected_per_sign=3 # one C2 assignment for each transposition
    connected_per_sign=raw_per_sign-disconnected_per_sign
    connected_raw=sign_solutions*connected_per_sign
    # Tree gauge is unique up to simultaneous global S3 conjugation. Burnside:
    # identity fixes 3^n assignments, each transposition fixes exactly one, and
    # 3-cycles fix none because every sign solution has odd triangle monodromy.
    gauge_orbits_per_sign=(raw_per_sign+3)//6
    connected_gauge_per_sign=gauge_orbits_per_sign-1
    connected_gauge=sign_solutions*connected_gauge_per_sign

    # Exhaust the Hamming-radius-one same-sign moves from the selected cover.
    radius1=0;radius1_conn=0
    orig=[z[e] for e in cot]
    for i,e in enumerate(cot):
        p=parity(orig[i])
        for w in S3:
            if w==orig[i] or parity(w)!=p:continue
            radius1+=1;vals=list(orig);vals[i]=w
            if len(gen_group(vals))==6:radius1_conn+=1
    assert radius1==2*n

    out0={'pass':4770,'base':{'vertices':45,'edges':270,'cycle_rank':n,'triangles':270},
      'sign_constraint':{'rank':r,'affine_dimension':sign_dim,'number_of_sign_solutions':sign_solutions,
        'selected_sign_weight':psol.bit_count(),'statement':'triangle holonomy is a transposition iff its S3 sign is odd'},
      'tree_gauge_moduli':{'raw_assignments_per_sign_solution':raw_per_sign,'disconnected_C2_assignments_per_sign_solution':disconnected_per_sign,
        'connected_assignments_total':connected_raw,'connected_vertex_gauge_classes_total':connected_gauge,
        'radius1_same_sign_deformations':radius1,'radius1_connected_deformations':radius1_conn},
      'base_automorphism_quotient':{'Aut_GQ_order':51840,'status':'reduced to the induced finite action on the gauge-moduli/projective parameter space; global orbit enumeration not claimed here'},
      'theorem':'The 270 transposition-holonomy constraints are exactly a binary sign-cocycle affine system. After solving that system, every cotree voltage has three freely selectable lifts of its prescribed parity. This gives an exact complete classification modulo vertex gauge; base-automorphism equivalence is a further finite orbit problem.',
      'boundary':'Exact finite S3 connection/gauge result. The huge moduli count is not a continuum gauge field or physical phase space.'}
    OUT0.write_text(json.dumps(out0,indent=2,sort_keys=True)+'\n')

    # Pass4774: twisted A3 local system over F3 on ALL 270 base edges.
    # In the tree-gauged sign representative, tree parities are zero and cotree
    # parities are psol. D(t)_(u,v)=t_v-(-1)^p t_u.
    epar={e:0 for e in tree}
    for i,e in enumerate(cot):epar[e]=(psol>>i)&1
    D=np.zeros((270,45),dtype=np.int64)
    for row,(u,v) in enumerate(sorted(G.edges())):
        p=epar[tuple(sorted((u,v)))];D[row,v]=1;D[row,u]=(-1 if p==0 else 1)%3
    rd=rank3(D);h0=45-rd;h1=270-rd
    # Every base triangle has odd sign, so a parallel section transported around
    # a triangle satisfies t=-t and hence t=0 over F3: H0 must vanish.
    assert h0==0 and rd==45 and h1==225
    projective_points=(3**h1-1)//2
    if sign_dim==0:
        assert connected_gauge_per_sign==projective_points
        geometry='PG(224,3) point set'
    else:geometry=f'{sign_solutions} copies of nonzero twisted-H1 vectors modulo +/-1'
    out4={'pass':4774,'twisted_local_system':{'field':'F3','sign_monodromy':'A3 exponent is inverted across odd S3 edges',
        'C0_dimension':45,'C1_dimension':270,'rank_twisted_coboundary':rd,'H0_dimension':h0,'H1_dimension':h1},
      'moduli_interpretation':{'sign_affine_dimension':sign_dim,'connected_classes_per_sign_solution':connected_gauge_per_sign,
        'nonzero_vectors_mod_F3_star':projective_points,'geometry_when_sign_unique':geometry},
      'comparison_with_deck_line':{'deck_field':'F2','tangent_field':'F3',
        'nonzero_additive_linear_map_F2_to_F3_exists':False,
        'reason':'an additive homomorphism sends an element of order 2 to an element whose order divides 2; the additive F3 space has no nonzero element of order 2'},
      'theorem':'The finite deformation sector behind the nonunique S3 covers is a sign-twisted F3 graph-cohomology space of dimension 225. When the binary sign solution is unique, connected vertex-gauge classes are exactly the nonzero twisted-H1 vectors modulo F3^*={+/-1}, i.e. the point set of PG(224,3). This sector cannot be linearly identified with the characteristic-two apartment deck line.',
      'boundary':'Finite local-system cohomology only. Projective-space language classifies gauge classes set-theoretically; the further PGSp orbit quotient is not asserted.'}
    OUT4.write_text(json.dumps(out4,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4770':out0,'4774':out4},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
