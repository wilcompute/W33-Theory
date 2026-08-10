#!/usr/bin/env python3
"""Pass 4663 (outside box) — the apartment duo bit does not descend to spreads.

Test the most natural group-theoretic coupling between the apartment C2 cover
and the 36 minimum-word/W33-spread carrier.  A representative apartment
stabilizer K has order 16. Against the 36 spread stabilizers its intersection
orders have profile 1^16,4^16,8^4; K fixes no spread, so there is no
PSp-equivariant set map apartments -> spreads (and none from flags -> spreads).

The four order-8 spreads nevertheless define a canonical transported relation.
Across all 1620 apartments it has row degree 4 and column degree 180, but only
135 distinct rows, each repeated twelve times. The row depends exactly on the
selected singular apartment fiber, producing a new 135_4-36_15 incidence.
Thus the relation is blind to both flag choice and the C2 deck sheet. Under the
Pass4658 minword<->spread transport, its four spreads are disjoint from the
eight minimum words containing the same singular coordinate.  The natural duo
signing therefore fails closed rather than producing a spurious binary phase.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,nullspace2,perm_group,transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4663_DUO_SPREAD_COUPLING_OBSTRUCTION_REGEN.json'

def pmask(mask,p):
    y=0;x=int(mask)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8);apartments=sorted(tuple(map(int,a)) for a in apartments)
    n=40;j=(1<<n)-1;cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(n) for k in range(i+1,n) if Astar[i,k]]);V=set(span(B9));rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    B=nullspace2(N.T);bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z):m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm:words += [x^b for x in words]
    minimum=sorted(w for w in words if w.bit_count()==30);assert len(minimum)==36

    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G):gens.append(p);G=trial
        if len(G)==25920:break
    assert len(G)==25920
    def act_v(x,g):return rep(pmask(rep(x),g))
    def act_word(w,g):
        z=0
        for i in range(135):
            if (w>>i)&1:z|=1<<sidx[act_v(sing[i],g)]
        return z
    byp=defaultdict(list)
    for li,L in enumerate(lines):
        for p in L:byp[p].append(li)
    spreads=[]
    def rec(chosen,used):
        if len(used)==40:spreads.append(frozenset(chosen));return
        p=next(x for x in range(40) if x not in used)
        for li in byp[p]:
            S=set(lines[li])
            if not(S&used):rec(chosen+[li],used|S)
    rec([],set());spreads=sorted(set(spreads),key=lambda S:tuple(sorted(S)));assert len(spreads)==36
    sI={S:i for i,S in enumerate(spreads)}
    def actS(S,g):return frozenset(g[i] for i in S)

    # Exact minword -> spread transport.
    mI={w:i for i,w in enumerate(minimum)};w0=minimum[0];Hw=[g for g in G if act_word(w0,g)==w0];assert len(Hw)==720
    fixed=[S for S in spreads if all(actS(S,g)==S for g in Hw)];assert len(fixed)==1;S0=fixed[0]
    tr={}
    for g in G:
        a=mI[act_word(w0,g)];b=sI[actS(S0,g)]
        if a in tr:assert tr[a]==b
        tr[a]=b
    assert len(tr)==36

    ap0=apartments[0];K=[g for g in G if tuple(sorted(g[i] for i in ap0))==ap0];assert len(K)==16
    profile=Counter();special=[]
    for S in spreads:
        z=sum(actS(S,g)==S for g in K);profile[z]+=1
        if z==8:special.append(S)
    assert profile==Counter({1:16,4:16,8:4}) and len(special)==4
    assert not [S for S in spreads if all(actS(S,g)==S for g in K)]

    aI={a:i for i,a in enumerate(apartments)};M=np.zeros((1620,36),dtype=np.uint8);seen={}
    for g in G:
        a=tuple(sorted(g[i] for i in ap0));ai=aI[a];U=frozenset(sI[actS(S,g)] for S in special)
        if ai in seen:assert seen[ai]==U
        seen[ai]=U
    assert len(seen)==1620
    for ai,U in seen.items():
        for s in U:M[ai,s]=1
    assert Counter(map(int,M.sum(1)))==Counter({4:1620}) and Counter(map(int,M.sum(0)))==Counter({180:36})
    rowkeys=Counter(bytes(row) for row in M);assert Counter(rowkeys.values())==Counter({12:135})

    # The 135 row types are exactly apartment singular fibers.
    byfib=defaultdict(set)
    for ai,a in enumerate(apartments):byfib[fib(a)].add(bytes(M[ai]))
    assert len(byfib)==135 and all(len(v)==1 for v in byfib.values())
    Q=np.vstack([np.frombuffer(next(iter(byfib[x])),dtype=np.uint8) for x in sing]);assert Q.shape==(135,36)
    assert Counter(map(int,Q.sum(1)))==Counter({4:135}) and Counter(map(int,Q.sum(0)))==Counter({15:36})

    # It is complementary, not identical, to the 8-spread incidence furnished
    # by the code minimum shell at each selected singular coordinate.
    for i,x in enumerate(sing):
        eight={tr[a] for a,w in enumerate(minimum) if (w>>i)&1};four=set(np.flatnonzero(Q[i]));assert len(eight)==8 and len(four)==4 and not(eight&four)

    out={'pass':4663,'apartment_stabilizer':{'order':16,'spread_stabilizer_intersection_profile':{'1':16,'4':16,'8':4},'fixed_spreads':0,'equivariant_apartment_to_spread_map':False},
      'transported_order8_relation':{'shape':[1620,36],'row_degree':4,'column_degree':180,'distinct_rows':135,'row_multiplicity':12,'factors_through':'selected singular apartment fiber','quotient_incidence':'135_4-36_15'},
      'comparison_to_code_spread_incidence':{'code_row_degree':8,'new_row_degree':4,'rowwise_intersection':0},
      'duo_sign_test':{'deck_sensitive':False,'reason':'the natural stabilizer relation factors through the 135 apartment fiber and is constant on all 12 apartments over that fiber; K fixes no spread so no equivariant set map can push the C2 sheet to a spread sign'},
      'theorem':'The natural apartment/spread coupling fails to induce a nontrivial duo signing on the 36 spread carrier. Instead it produces a deck-blind 135_4-36_15 incidence, rowwise disjoint from the existing 135_8-36_30 code-minimum/spread incidence.',
      'boundary':'Exact finite equivariance obstruction and incidence theorem; no phase/sign physics is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
