#!/usr/bin/env python3
"""Pass7449-7456: decide whether the 36D characteristic-3 global incidence
quotient is the local 36-spread/double-six permutation module.

Answer: NO.  The central Eisenstein order-three element J fixes the selected
W33 leaf pointwise (hence its 36 spreads pointwise) but acts on the 36D global
Gram-image with Jordan type 1^6 + J_3^10.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
import w33_pass7425_7432_e8_2240_leaf_geometry as leaf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7449_7456_CHAR3_GLOBAL36_VS_SPREADS.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def rank3(M):return leaf.rank_mod(np.asarray(M,dtype=np.int16)%3,3)

def main():
    R=leaf.roots();I={r:i for i,r in enumerate(R)};A2=leaf.enum_a2(R);ai={S:i for i,S in enumerate(A2)}
    rg=[tuple(I[leaf.refl(r,s)] for r in R) for s in leaf.SIMPLES]
    c=tuple(range(240))
    for g in rg:c=comp(g,c)
    J=tuple(range(240))
    for _ in range(10):J=comp(c,J)
    ag=[tuple(ai[frozenset(g[x] for x in S)] for S in A2) for g in rg]
    jA=tuple(ai[frozenset(J[x] for x in S)] for S in A2)
    base=frozenset(i for i,S in enumerate(A2) if frozenset(J[x] for x in S)==S)
    assert len(base)==40 and all(jA[x]==x for x in base)
    leaves=[base];li={base:0};q=deque([base])
    while q:
        X=q.popleft()
        for g in ag:
            Y=frozenset(g[x] for x in X)
            if Y not in li:li[Y]=len(leaves);leaves.append(Y);q.append(Y)
    assert len(leaves)==2240
    masks=[sum(1<<x for x in L) for L in leaves];G=[set() for _ in range(2240)]
    for i in range(2240):
        for j in range(i+1,2240):
            if (masks[i]&masks[j]).bit_count()==13:G[i].add(j);G[j].add(i)
    parity=[None]*2240;parity[0]=0;q=deque([0])
    while q:
        v=q.popleft()
        for w in G[v]:
            if parity[w] is None:parity[w]=1-parity[v];q.append(w)
            else:assert parity[w]!=parity[v]
    L0=[i for i,x in enumerate(parity) if x==0];assert len(L0)==1120
    F=np.zeros((1120,1120),dtype=np.uint8)
    for j,v in enumerate(L0):F[list(leaves[v]),j]=1
    Gram=(F.astype(np.int16)@F.T.astype(np.int16))%3
    assert rank3(Gram)==36
    p=np.asarray(jA,dtype=int);p2=p[p]
    assert np.all(p2[p]==np.arange(1120))
    N1=(Gram[:,p]-Gram)%3
    N2=(Gram[:,p2]+Gram[:,p]+Gram)%3 # (P-I)^2=P^2+P+I in char 3
    r1,r2=rank3(N1),rank3(N2)
    assert (r1,r2)==(20,10)
    # For order-3 unipotence in characteristic 3, if block counts are a,b,c
    # for sizes 1,2,3, then rank N=b+2c and rank N^2=c.
    c3=r2;b2=r1-2*c3;a1=36-2*b2-3*c3
    assert (a1,b2,c3)==(6,0,10)
    assert rank3((Gram[:,p2]+Gram[:,p]+Gram)%3)==10
    fixed_dim=36-r1;assert fixed_dim==16
    # J fixes every W33 point in the base leaf, hence all combinatorially
    # constructed lines and spreads on those points are fixed pointwise as objects.
    out={
      'schema':'w33.pass7449_7456.char3_global36_vs_spreads.v1','status':'PASS','passes':'7449-7456',
      'global_module':'im_F3(F F^T) on 1120 A2 coordinates','dimension':36,
      'central_Eisenstein_J':{'order':3,'fixed_base_W33_points':40,'action_on_local_36_spreads':'identity','rank_J_minus_I_on_global36':r1,'rank_J_minus_I_squared_on_global36':r2,'fixed_dimension_global36':fixed_dim,'Jordan_type':'1^6 + J3^10'},
      'decision':'The global characteristic-3 36-space is NOT isomorphic, as a base-leaf stabilizer module, to the 36-spread/double-six permutation module: the central C3 acts nontrivially on the former and trivially on the latter.',
      'structural_reading':'The 36-space remembers the central Eisenstein C3 killed by the local W(E6) action; its 30-dimensional nontrivial part consists of ten length-3 unipotent blocks.',
      'boundary':'This rules out the tempting 36=36 module identification. It does not yet identify the global36 module with a named indecomposable module for (3 x U4(2)):2.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','dim':36,'J_Jordan':'1^6+J3^10','spread_module_isomorphic':False}))
if __name__=='__main__':main()
