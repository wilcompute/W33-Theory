#!/usr/bin/env python3
"""Pass7491: close the outer-S3 theorem on the three 1120-object E8 families.

Rebuild the Pass7441 triad, forget the three type colours, and ask nauty for the full
automorphism group of the 3360-vertex graph.  The theorem target is that the coloured
automorphism group is the even Weyl group D4(2), while the uncoloured graph acquires
the full outer triality S3 and contains an explicit type 3-cycle.
"""
from __future__ import annotations
import json
from collections import deque
from pathlib import Path
import numpy as np
import pynauty
import w33_pass7425_7432_e8_2240_leaf_geometry as leaf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7491_E8_1120_OUTER_TRIALITY.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))

def build():
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
    parity=[None]*2240;parity[0]=0;q=deque([0])
    while q:
        v=q.popleft()
        for w in G[v]:
            if parity[w] is None:parity[w]=1-parity[v];q.append(w)
            else:assert parity[w]!=parity[v]
    L0=[i for i,x in enumerate(parity) if x==0];L1=[i for i,x in enumerate(parity) if x==1]
    p0={v:i for i,v in enumerate(L0)};p1={v:i for i,v in enumerate(L1)}
    F0=np.zeros((1120,1120),dtype=np.uint8);F1=np.zeros((1120,1120),dtype=np.uint8);K=np.zeros((1120,1120),dtype=np.uint8)
    for j,v in enumerate(L0):F0[list(leaves[v]),j]=1
    for j,v in enumerate(L1):F1[list(leaves[v]),j]=1
    for i,v in enumerate(L0):
        for w in G[v]:K[i,p1[w]]=1
    return F0,F1,K

def graph(F0,F1,K,coloured):
    n=3360;adj={i:set() for i in range(n)}
    # blocks: A=0..1119, L0=1120..2239, L1=2240..3359
    for a in range(1120):
        for j in np.flatnonzero(F0[a]):u=a;v=1120+int(j);adj[u].add(v);adj[v].add(u)
        for j in np.flatnonzero(F1[a]):u=a;v=2240+int(j);adj[u].add(v);adj[v].add(u)
    for i in range(1120):
        for j in np.flatnonzero(K[i]):u=1120+i;v=2240+int(j);adj[u].add(v);adj[v].add(u)
    assert {len(x) for x in adj.values()}=={80}
    colouring=None
    if coloured:colouring=[set(range(0,1120)),set(range(1120,2240)),set(range(2240,3360))]
    return pynauty.Graph(number_of_vertices=n,directed=False,adjacency_dict={k:list(v) for k,v in adj.items()},vertex_coloring=colouring)

def type_image(g,t):
    lo=1120*t;S={g[i]//1120 for i in range(lo,lo+1120)};assert len(S)==1;return next(iter(S))

def main():
    F0,F1,K=build();Gc=graph(F0,F1,K,True);Gu=graph(F0,F1,K,False)
    ac=pynauty.autgrp(Gc);au=pynauty.autgrp(Gu)
    sizec=int(round(ac[1]*(10**ac[2])));sizeu=int(round(au[1]*(10**au[2])))
    # nauty generators are explicit permutations on all 3360 vertices.
    type_perms=[];cycle=None;trans=None
    for g in au[0]:
        p=tuple(type_image(g,t) for t in range(3));type_perms.append(p)
        if p in ((1,2,0),(2,0,1)) and cycle is None:cycle=g
        if sorted(p)==[0,1,2] and sum(p[i]==i for i in range(3))==1 and trans is None:trans=g
    assert sizec==174182400
    assert sizeu==6*sizec
    assert cycle is not None and trans is not None
    # Freeze compact witnesses by hashing the 3360-entry permutations and recording the type action.
    import hashlib
    def h(g):return hashlib.sha256(','.join(map(str,g)).encode()).hexdigest()
    cp=tuple(type_image(cycle,t) for t in range(3));tp=tuple(type_image(trans,t) for t in range(3))
    out={'schema':'w33.pass7491.e8_1120_outer_triality.v1','status':'PASS',
      'vertices':3360,'three_types':['A2','leaf_even','leaf_odd'],'degree':80,
      'type_coloured_automorphism_order':sizec,'type_coloured_group':'D4(2)=O8+(2)',
      'uncoloured_automorphism_order':sizeu,'quotient_by_type_preserving':6,
      'outer_type_group':'S3','explicit_type_cycle':cp,'explicit_type_transposition':tp,
      'cycle_permutation_sha256':h(cycle),'transposition_permutation_sha256':h(trans),
      'nauty_generator_count':len(au[0]),'generator_type_actions':[list(x) for x in type_perms],
      'theorem':'The uncoloured 3360-vertex E8 triality-incidence graph has automorphism group D4(2):S3. Its type-preserving subgroup is D4(2), and explicit graph automorphisms realize a 3-cycle and a transposition on the three 1120-object families.',
      'boundary':'This closes the finite outer-triality identification; it does not add a physical triality symmetry to a dynamical model.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','coloured':sizec,'uncoloured':sizeu,'cycle':cp,'transposition':tp}))
if __name__=='__main__':main()
