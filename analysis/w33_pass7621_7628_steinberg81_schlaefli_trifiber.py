#!/usr/bin/env python3
"""Pass7621-7628: the 81-suborbit is an S3-fibred Schlaefli 27.

Fix one A2 point in the global 1120-point E8 A2 association scheme.  Its
valency-81 suborbit consists exactly of A2 subsystems sharing one antipodal root
pair with the anchor.  A relation-internal common-neighbour test canonically
partitions the 81 objects into 27 triples.  Each triple contains one extension
through each of the anchor A2's three root lines; orthogonal projection to the
E6 complement is constant on a triple and gives the 27 minuscule weight pairs.
The quotient graph is Schlaefli SRG(27,16,10,8).

The projective-E8 anchor stabilizer acts faithfully on the 81-set with order
311040.  Its quotient on the 27 triples has order 51840=W(E6), while the two
anchor-root reflections generate a kernel S3 acting identically and faithfully
on every 3-fibre.  This is the objectwise S3 x W(E6) realization behind 81=3*27.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7621_7628_STEINBERG81_SCHLAEFLI_TRIFIBER.json'

def canonpm(v):
    for x in v:
        if x!=0:return tuple(v) if x>0 else tuple(-y for y in v)
    return tuple(v)

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();AO,C,lab=E.a2_scheme(R,A2)
    anchor=0; S81=[int(x) for x in np.flatnonzero(lab[anchor]==4)]
    assert len(S81)==81
    # Relation 4 inside the 81-set has 81 exceptional edges with exactly one
    # common neighbour.  They form 27 K3 components.
    sub=lab[np.ix_(S81,S81)]; A4=(sub==4).astype(np.int16); CN=A4@A4
    ex=[(i,j) for i in range(81) for j in range(i+1,81) if A4[i,j] and CN[i,j]==1]
    H=[set() for _ in range(81)]
    for i,j in ex:H[i].add(j);H[j].add(i)
    assert len(ex)==81 and set(map(len,H))=={2}
    seen=set();tri=[]
    for i in range(81):
        if i in seen:continue
        q=[i];seen.add(i);cc=[]
        while q:
            u=q.pop();cc.append(u)
            for v in H[u]:
                if v not in seen:seen.add(v);q.append(v)
        assert len(cc)==3;tri.append(tuple(sorted(cc)))
    assert len(tri)==27

    # The 81 A2s share exactly one of the three antipodal root-pairs of anchor.
    I={r:i for i,r in enumerate(R)};S0=A2[anchor];pairs=[];pset=set()
    for r in S0:
        nr=I[tuple(-z for z in R[r])];P=frozenset((r,nr))
        if P not in pset:pset.add(P);pairs.append(P)
    assert len(pairs)==3
    st=[]
    for a in S81:
        X=A2[anchor]&A2[a];assert len(X)==2 and X in pset;st.append(pairs.index(X))
    assert Counter(st)==Counter({0:27,1:27,2:27})
    assert all(sorted(st[i] for i in T)==[0,1,2] for T in tri)

    # Project to the orthogonal E6 complement.  Every A2 in S81 contributes one
    # opposite minuscule weight pair; each of the 27 canonical triples is exactly
    # one projection fibre.
    alpha,beta=next((a,b) for a,b in itertools.combinations(sorted(S0),2) if E.dot(R[a],R[b])==-4)
    B=sp.Matrix.hstack(sp.Matrix(R[alpha]),sp.Matrix(R[beta]));Gi=(B.T*B).inv()
    def proj(i):
        x=sp.Matrix(R[i]);z=x-B*(Gi*(B.T*x));return canonpm(tuple(sp.simplify(q) for q in z))
    pclass=[]
    for a in S81:
        P={proj(r) for r in A2[a]-A2[anchor]};assert len(P)==1;pclass.append(next(iter(P)))
    pc=Counter(pclass);assert len(pc)==27 and set(pc.values())=={3}
    assert all(len({pclass[i] for i in T})==1 for T in tri)

    # Quotient pair patterns and Schlaefli graph.
    Q=np.zeros((27,27),dtype=np.int8);patterns=Counter()
    for i,j in itertools.combinations(range(27),2):
        pat=Counter(int(sub[a,b]) for a in tri[i] for b in tri[j]);patterns[tuple(sorted(pat.items()))]+=1
        if pat==Counter({2:6,4:3}):Q[i,j]=Q[j,i]=1
    assert patterns==Counter({((2,6),(4,3)):216,((3,6),(4,3)):135})
    assert set(map(int,Q.sum(1)))=={16}
    QQ=Q@Q;la={int(QQ[i,j]) for i,j in itertools.combinations(range(27),2) if Q[i,j]};mu={int(QQ[i,j]) for i,j in itertools.combinations(range(27),2) if not Q[i,j]}
    assert la=={10} and mu=={8}
    ev=Counter(round(float(x),8) for x in np.linalg.eigvalsh(Q.astype(float)))
    assert ev==Counter({-2.0:20,4.0:6,16.0:1})

    # Stabilizer action: faithful order 311040 on 81, order 51840 on 27 fibres.
    PG=PermutationGroup([Permutation(list(p)) for p in ag]);stab=PG.stabilizer(anchor)
    loc={v:i for i,v in enumerate(S81)};blocks=[frozenset(S81[i] for i in T) for T in tri];bi={B:i for i,B in enumerate(blocks)}
    g81=[];g27=[]
    for g in stab.generators:
        arr=g.array_form;g81.append(Permutation([loc[arr[v]] for v in S81]));g27.append(Permutation([bi[frozenset(arr[v] for v in B)] for B in blocks]))
    G81=PermutationGroup(g81);G27=PermutationGroup(g27)
    assert int(stab.order())==int(G81.order())==311040 and int(G27.order())==51840

    # Anchor A2 Weyl reflections give the entire six-element kernel and act the
    # same way on every fibre.
    ai={S:i for i,S in enumerate(A2)}
    def arefl(ridx):
        rp=tuple(I[E.refl(x,R[ridx])] for x in R)
        return tuple(ai[frozenset(rp[x] for x in S)] for S in A2)
    pa,pb=arefl(alpha),arefl(beta);K=PermutationGroup([Permutation(list(pa)),Permutation(list(pb))]);assert int(K.order())==6
    for p in (pa,pb):assert all(bi[frozenset(p[v] for v in B)]==i for i,B in enumerate(blocks))
    def onblock(p,B):
        L=sorted(B);pos={x:i for i,x in enumerate(L)};return tuple(pos[p[x]] for x in L)
    fibre_actions=Counter((onblock(pa,B),onblock(pb,B)) for B in blocks)
    assert len(fibre_actions)==1 and next(iter(fibre_actions.values()))==27

    out={
      'schema':'w33.pass7621_7628.steinberg81_schlaefli_trifiber.v1','status':'PASS','passes':'7621-7628',
      'anchor_stabilizer_order':311040,'anchor_stabilizer_structure':'W(A2) x W(E6) = S3 x W(E6)',
      'suborbit_size':81,'suborbit_characterization':'A2 subsystems sharing exactly one antipodal root pair with the anchor A2',
      'three_anchor_root_lines_counts':[27,27,27],
      'canonical_exceptional_edges':81,'canonical_fibres':27,'fibre_size':3,
      'fibre_rule':'relation-4 edges with one common relation-4 neighbour form 27 K3; each K3 uses all three anchor A1 root lines once',
      'E6_projection':'orthogonal projection of the four nonshared roots is one opposite E6 minuscule weight pair; 27 values each occur three times and exactly equal the K3 fibres',
      'quotient_pair_patterns':{'R2^6_R4^3':216,'R3^6_R4^3':135},
      'Schlaefli':{'parameters':[27,16,10,8],'spectrum':{'16':1,'4':6,'-2':20}},
      'action_on_81_order':311040,'action_on_27_order':51840,'kernel_order':6,'kernel':'S3=W(A2)',
      'kernel_fibre_action':'the same faithful S3 action on every one of the 27 triples',
      'novelty_boundary':'Pass7181 already proved that an 81 A2-charge sector projects 3-to-1 to the 27 E6 minuscule weights. New here is the global 1120-A2-scheme realization: the valency-81 suborbit is that 3-cover, the fibres are recoverable internally as 27 canonical triangles, and the anchor stabilizer realizes S3 x W(E6) objectwise.',
      'theorem':'The q^4=81 suborbit of one E8 A2 point is a canonical S3-fibred lift of the E6 minuscule Schlaefli 27. Thus 81=3*27 is realized by an exact point-stabilizer action, not a numerical factorization.',
      'claim_boundary':'Exact finite E8/E6 association-scheme theorem; it does not identify the 81-dimensional Steinberg representation with this permutation set without an explicit intertwiner.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','fibres':27,'quotient':'SRG(27,16,10,8)','orders':[311040,51840,6]}))
if __name__=='__main__':main()
