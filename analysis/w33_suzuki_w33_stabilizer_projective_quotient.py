#!/usr/bin/env python3
"""Exact stabilizer quotient for a full W(3,3) inside the 2.Suz tight shell.

This continues w33_suzuki_w33_e6_incidence_tower.py.  The earlier certificate
constructs the 135135-element 2.Suz orbit of full nondegenerate W(3,3)
subspaces in F3^12 and the 27 complementary three-W33 decompositions through a
fixed block U1, whose intersection graph is SRG(27,10,1,5).

Here we compute the actual block stabilizer, rather than identify the 27-vertex
graph only by parameters.

Results:
  * |Stab_{2.Suz}(U1)| = 896690995200 / 135135 = 6635520.
  * Restriction to U1 is all Sp(4,3), order 51840; kernel order 128.
  * The induced action on the 27 complementary decompositions is exactly
    PSp(4,3), order 25920; kernel order 256.
  * The full graph automorphism group has order 51840 (the W(E6) action), but
    exhaustive Schreier scanning of all 2*135135 = 270270 orbit edges finds no
    stabilizer generator in the outer coset.

This distinction matters: Sp(4,3) and W(E6)=PSp(4,3):2 both have order 51840,
but they are different extensions of PSp(4,3).  The Suzuki embedding realizes
the symplectic double cover on the four-dimensional block and only the inner
PSp action on the projective 27-decomposition carrier.  It does NOT realize the
outer E6 involution there.
"""
from __future__ import annotations

from collections import deque
import json
from pathlib import Path
import numpy as np

import w33_suzuki_w33_e6_incidence_tower as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_suzuki_w33_stabilizer_projective_quotient.json"
P = 3
G2SUZ_ORDER = 896_690_995_200
OUTER_GRAPH = (0,1,2,3,4,5,13,19,17,9,10,11,12,6,14,15,20,8,21,7,16,18,24,23,22,25,26)
AUT_BASE = (0,1,4,16,2)


def inv3(M):
    A=np.array(M,dtype=np.int64)%3; n=A.shape[0]
    X=np.concatenate([A,np.eye(n,dtype=np.int64)],axis=1)
    for c in range(n):
        p=next(i for i in range(c,n) if X[i,c])
        if p!=c: X[[c,p]]=X[[p,c]]
        X[c]=X[c]*pow(int(X[c,c]),-1,3)%3
        for i in range(n):
            if i!=c and X[i,c]: X[i]=(X[i]-X[i,c]*X[c])%3
    return X[:,n:]%3


def matkey(M):
    return bytes(np.asarray(M,dtype=np.uint8).ravel())


def perm_comp(p,g):
    # Row-action product: apply p, then g.
    return tuple(g[p[i]] for i in range(len(p)))


def perm_closure(gens, cap=100000):
    ident=tuple(range(len(gens[0])))
    seen={ident}; q=deque([ident])
    while q:
        x=q.popleft()
        for g in gens:
            z=perm_comp(x,g)
            if z not in seen:
                seen.add(z); q.append(z)
                assert len(seen)<=cap
    return seen


def mat_closure(gens, cap=100000):
    I=np.eye(gens[0].shape[0],dtype=np.int64)%3
    seen={matkey(I):I}; q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            z=(x@g)%3; k=matkey(z)
            if k not in seen:
                seen[k]=z; q.append(z)
                assert len(seen)<=cap
    return seen


def greedy_matrix_generators(cands, target):
    gs=[]; order=1
    for g in cands:
        if np.array_equal(g,np.eye(g.shape[0],dtype=np.int64)): continue
        H=mat_closure(gs+[g],cap=max(target,order)+1)
        if len(H)>order:
            gs.append(g); order=len(H)
        if order==target: break
    assert order==target
    return gs, H


def greedy_perm_generators(cands, target):
    gs=[]; order=1
    ident=tuple(range(len(cands[0])))
    for g in cands:
        if g==ident: continue
        H=perm_closure(gs+[g],cap=max(target,order)+1)
        if len(H)>order:
            gs.append(g); order=len(H)
        if order==target: break
    assert order==target
    return gs, H


def graph_preserved(p,adj):
    n=len(p)
    return all(int(adj[i,j])==int(adj[p[i],p[j]]) for i in range(n) for j in range(n))


def main(write=True):
    A=base.parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m1')
    B=base.parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m2')
    gens=[A,B]; invgens=[inv3(A),inv3(B)]
    U1=base.U1%3; J=base.J%3; I12=np.eye(12,dtype=np.int64)%3
    k0=base.rref_key(U1)

    # Orbit plus Schreier transversal.
    keys=[k0]; subs=[np.array(k0,dtype=np.int64)]
    T=[I12]; Ti=[I12]; index={k0:0}; q=deque([0])
    sample=[]; sample_keys=set()
    while q:
        ix=q.popleft(); S=subs[ix]
        for gi,g in enumerate(gens):
            kz=base.rref_key((S@g)%3); j=index.get(kz)
            Tg=(T[ix]@g)%3
            if j is None:
                j=len(keys); index[kz]=j; keys.append(kz); subs.append(np.array(kz,dtype=np.int64))
                T.append(Tg); Ti.append((invgens[gi]@Ti[ix])%3); q.append(j)
            elif len(sample)<120:
                s=(Tg@Ti[j])%3; sk=matkey(s)
                if sk not in sample_keys and not np.array_equal(s,I12):
                    assert base.rref_key((U1@s)%3)==k0
                    sample_keys.add(sk); sample.append(s)
    assert len(subs)==135135 and len(sample)==120

    # 54 orthogonal partners and 27 complement pairs.
    partner_keys=[]; partners=[]
    for k,S in zip(keys,subs):
        if np.all((U1@J@S.T)%3==0): partner_keys.append(k); partners.append(S)
    assert len(partners)==54
    pindex={k:i for i,k in enumerate(partner_keys)}
    comp=[]
    for V in partners:
        W=base.perp_basis(np.vstack([U1,V])); comp.append(pindex[base.rref_key(W)])
    assert all(comp[comp[i]]==i and comp[i]!=i for i in range(54))
    pairs=[]; pair_of={}
    for i in range(54):
        if i<comp[i]:
            pid=len(pairs); pairs.append((i,comp[i])); pair_of[i]=pair_of[comp[i]]=pid
    assert len(pairs)==27

    # Local Schlaefli/E6 graph from the already certified intersection rule.
    dec=[(partners[a],partners[b]) for a,b in pairs]
    adj=np.zeros((27,27),dtype=np.uint8)
    for i in range(27):
        for j in range(i+1,27):
            Ai,Bi=dec[i]; Aj,Bj=dec[j]
            sig=tuple(sorted([base.intersection_dim(Ai,Aj),base.intersection_dim(Ai,Bj),
                              base.intersection_dim(Bi,Aj),base.intersection_dim(Bi,Bj)]))
            if sig==(2,2,2,2): adj[i,j]=adj[j,i]=1
    assert base.srg_params(adj)==(27,10,1,5)

    def induced27(s):
        p=[]
        for V in partners: p.append(pindex[base.rref_key((V@s)%3)])
        assert sorted(p)==list(range(54))
        return tuple(pair_of[p[a]] for a,b in pairs)

    def restrict4(s):
        M=(U1@s)%3
        R=M[:,:4]%3  # U1 has pivot block I4.
        assert np.array_equal((R@U1)%3,M)
        return R

    # A deterministic small Schreier sample already generates the full linear image
    # and the complete inner projective image.
    restrictions=[restrict4(s) for s in sample]
    perm_sample=[induced27(s) for s in sample]
    rg,sp4=greedy_matrix_generators(restrictions,51840)
    pg,psp=greedy_perm_generators(perm_sample,25920)
    assert len(rg)==3 and len(pg)==2

    J1=(U1@J@U1.T)%3
    assert all(np.array_equal((R@J1@R.T)%3,J1) for R in sp4.values())

    # The full 27-line graph automorphism group is twice the inner PSp image.
    assert OUTER_GRAPH not in psp and graph_preserved(OUTER_GRAPH,adj)
    full_aut=perm_closure(pg+[OUTER_GRAPH],cap=51840)
    assert len(full_aut)==51840
    # AUT_BASE is a base: its image tuple uniquely determines each full graph automorphism.
    assert len({tuple(p[i] for i in AUT_BASE) for p in full_aut})==51840
    inner_sig={tuple(p[i] for i in AUT_BASE) for p in psp}
    full_sig={tuple(p[i] for i in AUT_BASE) for p in full_aut}
    assert len(inner_sig)==25920 and len(full_sig)==51840
    base_reps=[partners[pairs[i][0]] for i in AUT_BASE]

    # Exhaust all Schreier generators.  Because each stabilizer element preserves the
    # intersection graph and AUT_BASE is a base for its full automorphism group, membership
    # of the five-image signature in inner_sig proves membership in the inner PSp action.
    edge_count=0; observed=set()
    for ix,S in enumerate(subs):
        for gi,g in enumerate(gens):
            edge_count+=1
            kz=base.rref_key((S@g)%3); j=index[kz]
            Tg=(T[ix]@g)%3; s=(Tg@Ti[j])%3
            sig=[]
            for V in base_reps:
                h=pindex[base.rref_key((V@s)%3)]; sig.append(pair_of[h])
            sig=tuple(sig); observed.add(sig)
            assert sig in full_sig
            assert sig in inner_sig
    assert edge_count==270270

    stab_order=G2SUZ_ORDER//len(subs)
    assert stab_order==6635520
    assert stab_order%51840==0 and stab_order//51840==128
    assert stab_order%25920==0 and stab_order//25920==256

    out={
      'schema':'w33.suzuki_w33_stabilizer_projective_quotient.v1','status':'PASS',
      'headline':'For a full W33 block U in the 135135-element 2.Suz orbit, Stab(U) has order 6635520. Its restriction to U is the full symplectic double cover Sp(4,3), order 51840, with kernel 128. Its induced action on the 27 complementary three-W33 decompositions is only the inner projective group PSp(4,3), order 25920, with kernel 256. Exhaustive scanning of all 270270 Schreier generators finds none in the outer coset of the 51840-element E6/Schlaefli graph automorphism group.',
      'ambient':{'group':'2.Suz','order':G2SUZ_ORDER,'full_W33_orbit':len(subs)},
      'block_stabilizer':{'order':stab_order},
      'linear_restriction':{'group':'Sp(4,3)','order':len(sp4),'kernel_order':stab_order//len(sp4),
                            'sample_generators_needed':len(rg)},
      'projective_27_action':{'group':'PSp(4,3)','order':len(psp),'kernel_order':stab_order//len(psp),
                              'sample_generators_needed':len(pg)},
      'local_graph':{'vertices':27,'srg':[27,10,1,5],'full_automorphism_order':len(full_aut),
                     'outer_coset_size':len(full_aut)-len(psp),'five_vertex_base':list(AUT_BASE)},
      'exhaustive_schreier':{'orbit_edges_scanned':edge_count,'unique_five_image_signatures_seen':len(observed),
                             'outer_generators_seen':0},
      'extension_firewall':'Sp(4,3) and W(E6)=PSp(4,3):2 both have order 51840 but are different extensions. The Suzuki stabilizer realizes Sp(4,3) linearly and PSp(4,3) projectively; the E6 outer involution is absent from this 2.Suz-induced 27-point action.',
      'boundary':'This is an exact finite-group/permutation statement for the vendored ATLAS representation. It does not identify the absent outer graph involution with a physical operation or assert that enlarging 2.Suz by any particular element is dynamically available.',
      'checks':{'orbit_135135':True,'stabilizer_6635520':True,'linear_image_sp4_51840':True,
                'linear_kernel_128':True,'projective_image_psp4_25920':True,'projective_kernel_256':True,
                'full_graph_aut_51840':True,'all_270270_schreier_inner':True}
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
