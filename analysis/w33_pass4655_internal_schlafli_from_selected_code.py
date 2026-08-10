#!/usr/bin/env python3
"""Pass 4655 — reconstruct Schlaefli line/double-six incidence internally.

Use only the W33-derived selected 135_6–270_3 singular-line geometry:
  1. enumerate its binary left-kernel [135,16,30] code and 36 minimum words;
  2. enumerate all 270 maximal singular four-spaces of the protected V8 and
     isolate the unique PSp orbit of size 27;
  3. compare each 15-point nonzero generator shell with each 30-point minimum
     codeword support.

Every intersection is 0 or 6.  Declaring incidence at intersection 0 gives a
27x36 matrix with row degree 16, column degree 12, rank 21 and the exact
Schlaefli-line/double-six Gram identities.  Thus the cubic-surface incidence
carrier is reconstructed internally from the selected geometry and its binary
relation code, before applying any classical labels.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, nullspace2, perm_group, transvection_matrix,
)
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4655_INTERNAL_SCHLAEFLI_FROM_SELECTED_CODE.json'


def rep_action(m,p,j):
    out=0; x=int(m)
    while x:
        b=x&-x; i=b.bit_length()-1; out|=1<<p[i]; x^=b
    return min(out,out^j)


def main():
    pts,pidx,lines,lidx,_,Astar,_,_,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    nb=[set(np.flatnonzero(Astar[i]).tolist()) for i in range(40)]
    apartments=set()
    for u,w in itertools.combinations(range(40),2):
        if Astar[u,w]: continue
        common=sorted(nb[u]&nb[w])
        for a,b in itertools.combinations(common,2):
            if not Astar[a,b]: apartments.add(tuple(sorted((u,w,a,b))))
    apartments=sorted(apartments); assert len(apartments)==1620

    j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if Astar[i,k]]
    B9=rank_basis_int([cols[i]^cols[k] for i,k in edges]); V9=set(span(B9)); assert len(B9)==9 and j in V9
    rep=lambda x:min(int(x),int(x)^j)
    reps={rep(x) for x in V9}
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    singular=sorted(x for x in reps if x and q(x)==0); assert len(singular)==135

    # Maximal singular four-spaces.
    levels={0:{frozenset((0,))}}
    for d in range(4):
        nxt=set()
        for S in levels[d]:
            for v in singular:
                if v in S or any(polar(v,u) for u in S): continue
                T=frozenset(set(S)|{rep(u^v) for u in S})
                if len(T)==1<<(d+1) and all(q(u)==0 for u in T): nxt.add(T)
        levels[d+1]=nxt
    maxgens=list(levels[4]); assert len(maxgens)==270
    gen_lookup={S:i for i,S in enumerate(maxgens)}

    # Selected singular lines from apartments and incidence N.
    def apartment_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]; assert len(opp)==2
        s=rep(cols[opp[0][0]]^cols[opp[0][1]])
        t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        x=0
        for i in ap: x^=cols[i]
        x=rep(x); assert q(s)==q(t)==q(x)==0 and rep(s^t)==x
        return tuple(sorted((s,t,x)))
    fibers=defaultdict(list)
    for ap in apartments: fibers[apartment_line(ap)].append(ap)
    selected_lines=sorted(fibers); assert len(selected_lines)==270
    sidx={x:i for i,x in enumerate(singular)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected_lines):
        for x in L: N[sidx[x],c]=1

    # Exact binary left-kernel code and its 36 minimum words.
    B=nullspace2(N.T); assert len(B)==16
    bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z): m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm: words += [x^b for x in words]
    mins=[x for x in words if x.bit_count()==30]; assert len(mins)==36
    min_supports=[{singular[i] for i in range(135) if (w>>i)&1} for w in mins]

    # PSp generators and orbit decomposition of the 270 maximal generators.
    all_trans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for p in all_trans:
        trial=perm_group(gens+[p])
        if len(trial)>len(G): gens.append(p); G=trial
        if len(G)==25920: break
    assert len(G)==25920
    def act(p,S): return frozenset(rep_action(x,p,j) for x in S)
    unseen=set(range(270)); orbits=[]
    while unseen:
        z=next(iter(unseen)); orb={z}; Q=deque([z])
        while Q:
            i=Q.popleft()
            for p in gens:
                k=gen_lookup[act(p,maxgens[i])]
                if k not in orb: orb.add(k); Q.append(k)
        unseen-=orb; orbits.append(sorted(orb))
    assert sorted(map(len,orbits))==[27,36,36,36,135]
    orb27=next(o for o in orbits if len(o)==27)
    gen27=[set(maxgens[i])-{0} for i in orb27]

    # Internal incidence: zero intersection between 15-point generator shell
    # and 30-point minimum codeword support.
    X=np.zeros((27,36),dtype=np.int64)
    intersection_counts=Counter()
    for i,S in enumerate(gen27):
        for k,T in enumerate(min_supports):
            z=len(S&T); intersection_counts[z]+=1
            if z==0: X[i,k]=1
    assert intersection_counts==Counter({6:540,0:432})
    assert set(map(int,X.sum(1)))=={16} and set(map(int,X.sum(0)))=={12}
    assert np.linalg.matrix_rank(X)==21

    I27=np.eye(27,dtype=np.int64); J27=np.ones((27,27),dtype=np.int64)
    I36=np.eye(36,dtype=np.int64); J36=np.ones((36,36),dtype=np.int64)
    RR=X@X.T; RtR=X.T@X
    A27=((RR-10*I27-6*J27)//2).astype(np.int64)
    A36=((6*I36+6*J36-RtR)//2).astype(np.int64)
    assert set(np.unique(A27))<={0,1} and set(np.unique(A36))<={0,1}
    assert set(map(int,A27.sum(1)))=={10} and set(map(int,A36.sum(1)))=={15}
    assert np.array_equal(RR,10*I27+2*A27+6*J27)
    assert np.array_equal(RtR,6*I36-2*A36+6*J36)
    assert np.array_equal(3*A27@X+X@A36,20*np.ones((27,36),dtype=np.int64))

    adj=Counter(); non=Counter()
    for i,k in itertools.combinations(range(27),2):
        c=int(A27[i]@A27[k]); (adj if A27[i,k] else non)[c]+=1
    assert adj==Counter({1:135}) and non==Counter({5:216})
    ds_inter=Counter(RtR[np.triu_indices(36,1)].tolist())
    assert ds_inter==Counter({6:360,4:270})

    out={
      'pass':4655,
      'inputs':{
        'selected_geometry':'135_6-270_3',
        'binary_relation_code':'[135,16,30]_2',
        'minimum_words':36,
        'degree27_maximal_generator_orbit':27
      },
      'internal_intersection_rule':{
        'generator_nonzero_points':15,
        'minimum_word_support':30,
        'intersection_census':{'0':432,'6':540},
        'incidence':'intersection size 0'
      },
      'reconstructed_matrix':{
        'shape':[27,36],'row_sum':16,'column_sum':12,'rank_Q':21,
        'RRt':'10 I27 + 2 A27 + 6 J27','RtR':'6 I36 - 2 A36 + 6 J36',
        'intertwiner':'3 A27 R + R A36 = 20 J27x36'
      },
      'reconstructed_graphs':{
        'A27':'SRG(27,10,1,5) meeting graph',
        'A36':'SRG(36,15,6,6) double-six graph',
        'A36_offdiag_RtR_census':{'4':270,'6':360}
      },
      'action_level_chain':'Pass4640 identifies the 27 orbit with cubic lines; Pass4651 identifies the 36 minimum words with W33 spreads; Pass4643/4646 identify each spread sheet with the double-six carrier. The zero-intersection rule now reconstructs the same 27x36 incidence directly inside the selected geometry.',
      'theorem':'The selected 135_6-270_3 geometry internally reconstructs the full Schlaefli-line/double-six 27x36 incidence: zero intersection between a degree-27 maximal singular generator and a minimum [135,16,30] codeword is exactly the Schlaefli incidence relation.',
      'boundary':'Finite internal reconstruction theorem; no cubic-surface physics is inferred.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
