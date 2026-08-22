#!/usr/bin/env python3
"""Pass7441-7448: three 1120-object E8 families form a triality incidence triad.

Families:
  A = 1120 E8 A2 root subsystems,
  L+ and L- = the two parity halves of the 2240 Eisenstein W33 leaves.

Every pair of families carries the same degree-40 diameter-4 incidence parameters.
The three centered incidence matrices satisfy a 300-dimensional triality groupoid
law.  External O8+(2) triality is recorded only as a classification target; the
script itself proves the E8 incidence identities.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np
import w33_pass7425_7432_e8_2240_leaf_geometry as leaf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7441_7448_E8_1120_TRIALITY_TRIAD.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def orbit(seed,gens):
    S={seed};q=deque([seed])
    while q:
        x=q.popleft()
        for g in gens:
            y=g[x]
            if y not in S:S.add(y);q.append(y)
    return S

def check_drg(left,right):
    # left/right are adjacency lists indexed 0..1119 on opposite sides.
    assert all(len(x)==40 for x in left) and all(len(x)==40 for x in right)
    dL=[None]*1120;dR=[None]*1120;dL[0]=0;q=deque([(0,0)])
    while q:
        side,x=q.popleft()
        if side==0:
            for y in left[x]:
                if dR[y] is None:dR[y]=dL[x]+1;q.append((1,y))
        else:
            for y in right[x]:
                if dL[y] is None:dL[y]=dR[x]+1;q.append((0,y))
    assert Counter(dL)==Counter({4:729,2:390,0:1})
    assert Counter(dR)==Counter({3:1080,1:40})
    layers={0:{(0,i) for i,d in enumerate(dL) if d==0},
            1:{(1,i) for i,d in enumerate(dR) if d==1},
            2:{(0,i) for i,d in enumerate(dL) if d==2},
            3:{(1,i) for i,d in enumerate(dR) if d==3},
            4:{(0,i) for i,d in enumerate(dL) if d==4}}
    def nb(v):
        s,x=v
        return ({(1,y) for y in left[x]} if s==0 else {(0,y) for y in right[x]})
    rows={}
    for d in range(5):
        z=Counter(tuple(len(nb(v)&layers[e]) for e in range(5)) for v in layers[d])
        assert len(z)==1;rows[d]=next(iter(z))
    assert rows=={0:(0,40,0,0,0),1:(1,0,39,0,0),2:(0,4,0,36,0),
                  3:(0,0,13,0,27),4:(0,0,0,40,0)}
    return rows

def main():
    R=leaf.roots();I={r:i for i,r in enumerate(R)};A2=leaf.enum_a2(R);ai={S:i for i,S in enumerate(A2)}
    rg=[tuple(I[leaf.refl(r,s)] for r in R) for s in leaf.SIMPLES]
    c=tuple(range(240))
    for g in rg:c=comp(g,c)
    J=tuple(range(240))
    for _ in range(10):J=comp(c,J)
    ag=[tuple(ai[frozenset(g[x] for x in S)] for S in A2) for g in rg]
    base=frozenset(i for i,S in enumerate(A2) if frozenset(J[x] for x in S)==S);assert len(base)==40
    leaves=[base];li={base:0};q=deque([base])
    while q:
        X=q.popleft()
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in li:li[Y]=len(leaves);leaves.append(Y);q.append(Y)
    assert len(leaves)==2240
    masks=[sum(1<<x for x in L) for L in leaves]
    G=[set() for _ in range(2240)]
    for i in range(2240):
        for j in range(i+1,2240):
            if (masks[i]&masks[j]).bit_count()==13:G[i].add(j);G[j].add(i)
    assert {len(x) for x in G}=={40}
    parity=[None]*2240;parity[0]=0;q=deque([0])
    while q:
        v=q.popleft()
        for w in G[v]:
            if parity[w] is None:parity[w]=1-parity[v];q.append(w)
            else:assert parity[w]!=parity[v]
    L0=[i for i,x in enumerate(parity) if x==0];L1=[i for i,x in enumerate(parity) if x==1]
    assert len(L0)==len(L1)==1120
    p0={v:i for i,v in enumerate(L0)};p1={v:i for i,v in enumerate(L1)}
    # Simple reflections swap parity; their even products are transitive on all
    # three 1120-object families.
    lg=[tuple(li[frozenset(g[x] for x in leaves[v])] for v in range(2240)) for g in ag]
    evenA=[comp(ag[0],ag[i]) for i in range(1,8)]
    evenL=[comp(lg[0],lg[i]) for i in range(1,8)]
    assert len(orbit(0,evenA))==1120
    assert len(orbit(L0[0],evenL))==1120 and len(orbit(L1[0],evenL))==1120
    # Pairwise incidence matrices.
    F0=np.zeros((1120,1120),dtype=np.uint8);F1=np.zeros((1120,1120),dtype=np.uint8)
    for j,v in enumerate(L0):F0[list(leaves[v]),j]=1
    for j,v in enumerate(L1):F1[list(leaves[v]),j]=1
    K=np.zeros((1120,1120),dtype=np.uint8)
    for i,v in enumerate(L0):
        for w in G[v]:K[i,p1[w]]=1
    for B in (F0,F1,K):
        assert set(map(int,B.sum(0)))=={40} and set(map(int,B.sum(1)))=={40}
        assert leaf.rank_mod(B,2)==300 and leaf.rank_mod(B,3)==266
        gram=B.astype(np.int16)@B.T.astype(np.int16)
        assert set(np.unique(gram))=={0,4,40}
        assert leaf.rank_mod(gram%2,2)==0 and leaf.rank_mod(gram%3,3)==36
    # All three pairwise bipartite geometries have the same DRG array.
    A_L0=[set(np.flatnonzero(F0[a])) for a in range(1120)]
    L0_A=[set(np.flatnonzero(F0[:,j])) for j in range(1120)]
    A_L1=[set(np.flatnonzero(F1[a])) for a in range(1120)]
    L1_A=[set(np.flatnonzero(F1[:,j])) for j in range(1120)]
    L0_L1=[set(np.flatnonzero(K[j])) for j in range(1120)]
    L1_L0=[set(np.flatnonzero(K[:,j])) for j in range(1120)]
    check_drg(A_L0,L0_A);check_drg(A_L1,L1_A);check_drg(L0_L1,L1_L0)
    # Triality composition: a cross-pair has 13 common vertices in the third
    # family exactly when it is incident, and one otherwise.
    X=F1.astype(np.int16)@K.T.astype(np.int16)
    assert np.array_equal(X, np.ones((1120,1120),dtype=np.int16)+12*F0)
    Y=F0.astype(np.int16)@K.astype(np.int16)
    assert np.array_equal(Y, np.ones((1120,1120),dtype=np.int16)+12*F1)
    Z=F0.T.astype(np.int16)@F1.astype(np.int16)
    assert np.array_equal(Z, np.ones((1120,1120),dtype=np.int16)+12*K)
    # Centering yields an exact 300D partial-isometry groupoid.
    # With X_B=B-J/28, the uncentered identities imply X1 X2^T=12 X0.
    # Each centered Gram has eigenvalue 144 on rank 300 and zero elsewhere.
    gram=F0.astype(np.int16)@F0.T.astype(np.int16)
    # rank over R from SRG Gram spectrum: 1600^1 + 144^300.
    assert np.linalg.matrix_rank(gram.astype(float),tol=1e-7)==301
    # The mod-3 half-incidence code has a large hull: k-rank(GG^T)=266-36.
    out={
      'schema':'w33.pass7441_7448.e8_1120_triality_triad.v1','status':'PASS','passes':'7441-7448',
      'three_families':{'A2':1120,'leaf_plus':1120,'leaf_minus':1120},
      'even_Weyl_transitive_on_each_family':True,
      'pairwise_incidence_degree':40,
      'pairwise_distance_regular':'{40,39,36,27;1,4,13,40}',
      'pairwise_matrix_ranks':{'real':301,'F2':300,'F3':266},
      'pairwise_gram_spectrum':'1600^1 144^300 0^819',
      'binary_shadow':'Each 1120x1120 pair-incidence row code has dimension 300 and is self-orthogonal because BB^T=0 mod2.',
      'ternary_shadow':{'code_dimension':266,'gram_rank':36,'hull_dimension':230},
      'triality_composition':['F_minus K^T = J + 12 F_plus','F_plus K = J + 12 F_minus','F_plus^T F_minus = J + 12 K'],
      'centered_triality':'Writing X_B=B-J/28 gives X_minus X_K^T=12 X_plus and cyclic variants; X_B X_B^T=144 P_300. Thus X_B/12 are coherent partial isometries between three 300-dimensional constituents.',
      'third_family_common_neighbor_law':'Across any two distinct families, incident pairs have 13 common neighbors in the third family and nonincident pairs have exactly 1.',
      'external_group_target':'The effective even Weyl group is the D4(2)=O8+(2) group. ATLAS/GAP lists three nonconjugate maximal-subgroup classes of index 1120 and structure (3 x U4(2)):2. The present three-family geometry is therefore the natural triality target, but this certificate does not claim the outer S3 permutation until explicit subgroup-class/fusion maps are frozen.',
      'claim_boundary':'Exact E8 incidence/triality-parameter theorem. The outer triality identification is a tightly constrained next theorem, not silently assumed.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','families':'1120+1120+1120','composition':'J+12B','ranks':'301/300/266'}))
if __name__=='__main__':main()
