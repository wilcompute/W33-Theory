#!/usr/bin/env python3
"""Pass 4720 (outside box) — exact S5-invariant Petersen edge codes.

Treat one 15-edge Petersen shortcut fiber as a binary edge-symbol block.  Its
cycle space is [15,6,5]_2 and its dual cut space is [15,9,3]_2.  Both are
invariant under the full 120-element Petersen automorphism group S5, hence under
the A5/S5 local actions already established for PSp/PGSp.  The cycle code has
an exact erasure-failure census and corrects every pattern of at most four erased
edge symbols.  Across 27 fibers the direct sum is [405,162,5]_2.

This is local redundancy, not a free network-capacity gain: the cycle-code rate
is 2/5 (cut-code rate 3/5).  The pass therefore certifies erasure recovery and
symmetry-compatible load coding while failing closed on any claim that coding
increases fault-free raw throughput.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4720_PETERSEN_NETWORK_CODE_REGEN.json'

def rref2(A):
    A=np.asarray(A,dtype=np.uint8).copy();r=0;p=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]^=A[r]
        p.append(c);r+=1
    return A,p

def null2(A):
    R,piv=rref2(A);free=[j for j in range(A.shape[1]) if j not in piv];B=[]
    for f in free:
        x=np.zeros(A.shape[1],dtype=np.uint8);x[f]=1
        for i,p in reversed(list(enumerate(piv))):x[p]=int(np.dot(R[i],x)%2)
        B.append(x)
    return B

def span2(B):
    W=[np.zeros(len(B[0]),dtype=np.uint8)] if B else [np.zeros(0,dtype=np.uint8)]
    for b in B:W += [x^b for x in list(W)]
    return W

def main():
    G=nx.petersen_graph();edges=sorted(tuple(sorted(e)) for e in G.edges());eidx={e:i for i,e in enumerate(edges)}
    B=np.zeros((10,15),dtype=np.uint8)
    for j,(u,v) in enumerate(edges):B[u,j]=B[v,j]=1
    rank=len(rref2(B)[1]);assert rank==9
    cycle_basis=null2(B);assert len(cycle_basis)==6;cycle=span2(cycle_basis)
    cut_basis=rref2(B)[0][:rank];cut=span2([x for x in cut_basis])
    ec=Counter(int(x.sum()) for x in cycle);ed=Counter(int(x.sum()) for x in cut)
    assert ec==Counter({0:1,5:12,6:10,8:15,9:20,10:6})
    assert min(k for k in ed if k)>0 and min(k for k in ed if k>0)==3

    # All graph automorphisms preserve both codes; enumerate all 120 directly.
    aut=[]
    for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter():
        p=[]
        for e in edges:p.append(eidx[tuple(sorted((m[e[0]],m[e[1]])))])
        aut.append(tuple(p))
    aut=set(aut);assert len(aut)==120
    cmasks={sum(int(x[i])<<i for i in range(15)) for x in cycle};dmasks={sum(int(x[i])<<i for i in range(15)) for x in cut}
    def pmask(m,p):
        y=0
        for i,j in enumerate(p):
            if (m>>i)&1:y|=1<<j
        return y
    assert all({pmask(w,p) for w in cmasks}==cmasks for p in aut)
    assert all({pmask(w,p) for w in dmasks}==dmasks for p in aut)

    # Erasure decoding of a linear block code is ambiguous exactly when the
    # erased coordinate set contains the support of a nonzero codeword.
    supports=[frozenset(np.flatnonzero(x).tolist()) for x in cycle if x.any()]
    fail=Counter();total=Counter()
    for m in range(1<<15):
        E=frozenset(i for i in range(15) if (m>>i)&1);e=len(E);total[e]+=1
        if any(S<=E for S in supports):fail[e]+=1
    expected={0:0,1:0,2:0,3:0,4:0,5:12,6:130,7:630,8:1755,9:3005,10:3003,11:1365,12:455,13:105,14:15,15:1}
    assert dict(fail)=={k:v for k,v in expected.items() if v}

    out={'pass':4720,
      'local_cycle_code':{'parameters':'[15,6,5]_2','rate':'2/5','weight_enumerator':{str(k):v for k,v in sorted(ec.items())},'minimum_words':12,'minimum_words_are_Petersen_5_cycles':True},
      'local_cut_code':{'parameters':'[15,9,3]_2','rate':'3/5','dual_of_cycle':True},
      'symmetry':{'Petersen_automorphism_order':120,'full_group':'S5','cycle_code_invariant':True,'cut_code_invariant':True,'compatibility':'Pass4687 local PSp image A5 and PGSp image S5 are sub/full actions of this automorphism group'},
      'cycle_erasure_failure_counts':{str(e):{'fail':expected[e],'total':math.comb(15,e)} for e in range(16)},
      'guaranteed_erasure_correction':4,
      'global_27_fiber_direct_sum':{'cycle_parameters':'[405,162,5]_2','cut_parameters':'[405,243,3]_2','PSp_PGSp_invariant':True},
      'throughput_boundary':'The code adds redundancy: raw symbol rates are 2/5 (cycle) or 3/5 (cut). It certifies local erasure recovery/load-symmetry but does not increase fault-free edge capacity.',
      'theorem':'Each Petersen shortcut fiber carries canonical S5-invariant binary cycle/cut codes. The [15,6,5] cycle code corrects every <=4-edge erasure pattern and has the exact failure census above; 27 fibers give a PSp/PGSp-invariant [405,162,5] direct-sum code.',
      'boundary':'Exact finite coding theorem; no physical implementation, throughput improvement, or fault-tolerance threshold is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
