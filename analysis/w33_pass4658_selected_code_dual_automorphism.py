#!/usr/bin/env python3
"""Pass 4658 — dual enumerator and full automorphism group of [135,16,30]_2.

The proof is intrinsic and fail-closed.  MacWilliams gives C^perp=[135,119,3]
with exactly 270 weight-three words; because C=ker(N^T), these are precisely the
270 columns of the selected incidence matrix and therefore reconstruct the
135_6-270_3 geometry from the code alone.

For Aut(C), derive a graph on the 36 minimum words using their joint Jacobi
profiles against the entire weight-45 shell.  The 630 pairs split intrinsically
as 270+360; the 270 relation is 15-regular.  Under the already proved
minword-to-W33-spread equivariant transport, this graph is literally the
spread overlap-4 SRG(36,15,6,6), whose full automorphism order 51840 was
independently certified.  The 135 coordinate incidence signatures across the
36 minimum words are all distinct, so Aut(C) acts faithfully on this graph.
Thus |Aut(C)|<=51840.  Conversely the explicit PGSp(4,3) action on the selected
135 coordinates has order 51840 and preserves the 270 selected triples, hence
C. Therefore Aut(C)=PGSp(4,3), order 51840.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, build_line_perm, nullspace2, perm_group, transvection_matrix
from w33_pass4587_w33_derived_d4_triality import rank_basis_int, span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4658_SELECTED_CODE_DUAL_AUTOMORPHISM_REGEN.json'

def pmask(mask,p):
    y=0; x=int(mask)
    while x:
        b=x&-x; i=b.bit_length()-1; x^=b; y|=1<<p[i]
    return y

def rank_mod2(M):
    A=np.asarray(M,dtype=np.uint8).copy(); r=0
    for c in range(A.shape[1]):
        q=np.flatnonzero(A[r:,c])
        if len(q)==0: continue
        rr=r+int(q[0]); A[[r,rr]]=A[[rr,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
        if r==A.shape[0]: break
    return r

def main():
    pts,pidx,lines,lidx,_,Astar,_,apartments,_=build_geometry(); Astar=np.asarray(Astar,dtype=np.uint8)
    apartments=sorted(tuple(map(int,a)) for a in apartments); n=40; j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(Astar[:,c]): m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(n) for k in range(i+1,n) if Astar[i,k]])
    V=set(span(B9)); rep=lambda x:min(int(x),int(x)^j)
    def ap_line(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]; assert len(opp)==2
        s=rep(cols[opp[0][0]]^cols[opp[0][1]]); t=rep(cols[opp[1][0]]^cols[opp[1][1]])
        x=0
        for i in ap: x^=cols[i]
        return tuple(sorted((s,t,rep(x))))
    selected=sorted({ap_line(a) for a in apartments}); assert len(selected)==270
    sing=sorted(set().union(*(set(L) for L in selected))); assert len(sing)==135; sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L: N[sidx[x],c]=1
    assert set(map(int,N.sum(1)))=={6} and set(map(int,N.sum(0)))=={3}

    B=nullspace2(N.T); assert len(B)==16
    bm=[]
    for b in B:
        m=0
        for i,z in enumerate(b):
            if int(z): m|=1<<i
        bm.append(m)
    words=[0]
    for b in bm: words += [x^b for x in words]
    W=Counter(w.bit_count() for w in words)
    minimum=sorted(w for w in words if w.bit_count()==30); shell45=sorted(w for w in words if w.bit_count()==45)
    assert len(minimum)==36 and len(shell45)==432

    # Full MacWilliams transform.
    dual={}
    for wt in range(136):
        s=0
        for i,Ai in W.items():
            K=sum((-1)**t*comb(i,t)*comb(135-i,wt-t) for t in range(max(0,wt-(135-i)),min(wt,i)+1))
            s += Ai*K
        assert s%(1<<16)==0; dual[wt]=s//(1<<16)
    assert sum(dual.values())==1<<119
    assert dual[1]==dual[2]==0 and dual[3]==270 and dual[4]==2025 and dual[132]==45
    # C^perp=rowspace(N^T); all 270 columns are distinct weight-three words,
    # and MacWilliams says there are no others.
    colwords=[]
    for c in range(270):
        m=0
        for i in np.flatnonzero(N[:,c]): m|=1<<int(i)
        colwords.append(m)
    assert len(set(colwords))==270 and all(m.bit_count()==3 for m in colwords)

    # Code-intrinsic pair Jacobi relation on the minimum shell.
    pair_classes=defaultdict(list)
    for a,b in itertools.combinations(range(36),2):
        wa,wb=minimum[a],minimum[b]
        sig=Counter(tuple(sorted(((wa&u).bit_count(),(wb&u).bit_count()))) for u in shell45)
        key=tuple(sorted((k,v) for k,v in sig.items()))
        pair_classes[key].append((a,b))
    assert sorted(map(len,pair_classes.values()))==[270,360]
    adjpairs=next(v for v in pair_classes.values() if len(v)==270)
    AJ=np.zeros((36,36),dtype=np.uint8)
    for a,b in adjpairs: AJ[a,b]=AJ[b,a]=1
    assert set(map(int,AJ.sum(1)))=={15}
    # coordinate signatures in the 36 minwords are unique -> faithful action.
    coord_sigs=[]
    for c in range(135): coord_sigs.append(tuple((w>>c)&1 for w in minimum))
    assert len(set(coord_sigs))==135

    # PSp action and exact minword <-> W33 spread transport.
    candidates=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for p in candidates:
        trial=perm_group(gens+[p])
        if len(trial)>len(G): gens.append(p); G=trial
        if len(G)==25920: break
    assert len(G)==25920 and len(gens)==5
    def act_v(x,g): return rep(pmask(rep(x),g))
    def act_word(w,g):
        z=0
        for i in range(135):
            if (w>>i)&1: z |= 1<<sidx[act_v(sing[i],g)]
        return z
    # all 36 W33 spreads.
    bypt=defaultdict(list)
    for li,L in enumerate(lines):
        for p in L: bypt[p].append(li)
    spreads=[]
    def rec(chosen,used):
        if len(used)==40: spreads.append(frozenset(chosen)); return
        p=next(x for x in range(40) if x not in used)
        for li in bypt[p]:
            S=set(lines[li])
            if not (S&used): rec(chosen+[li],used|S)
    rec([],set()); spreads=sorted(set(spreads),key=lambda S:tuple(sorted(S))); assert len(spreads)==36
    def act_spread(S,g): return frozenset(g[i] for i in S)
    w0=minimum[0]; H=[g for g in G if act_word(w0,g)==w0]; assert len(H)==720
    fixed=[S for S in spreads if all(act_spread(S,g)==S for g in H)]; assert len(fixed)==1; S0=fixed[0]
    minidx={w:i for i,w in enumerate(minimum)}; spridx={S:i for i,S in enumerate(spreads)}; transport={}
    for g in G:
        a=minidx[act_word(w0,g)]; b=spridx[act_spread(S0,g)]
        if a in transport: assert transport[a]==b
        transport[a]=b
    assert len(transport)==36 and len(set(transport.values()))==36
    AS=np.zeros((36,36),dtype=np.uint8)
    for a,b in itertools.combinations(range(36),2):
        if len(spreads[a]&spreads[b])==4: AS[a,b]=AS[b,a]=1
    assert set(map(int,AS.sum(1)))=={15}
    for a,b in itertools.combinations(range(36),2): assert AJ[a,b]==AS[transport[a],transport[b]]

    # Independent frozen automorphism count of the spread/double-six graph.
    autcert=json.loads((ROOT/'manuscripts/parts/PART_MCCCXCV_SPREAD_DOUBLE_SIX_AUTOMORPHISM_ORDER_results.json').read_text())
    assert autcert['orbit_stabilizer']['automorphism_order']==51840

    # Explicit PGSp outer similitude acts on selected 135 coordinates and code.
    outer=np.diag([1,2,1,2])%3
    outer_line=build_line_perm(outer,pts,pidx,lines,lidx)
    all_line_gens=gens+[outer_line]
    selected_set=set(selected)
    coord_perms=[]
    for g in all_line_gens:
        cp=tuple(sidx[act_v(x,g)] for x in sing); coord_perms.append(cp)
        assert {tuple(sorted(act_v(x,g) for x in L)) for L in selected}==selected_set
    PG=PermutationGroup([Permutation(list(p)) for p in coord_perms]); assert PG.order()==51840

    out={'pass':4658,
      'code':{'parameters':'[135,16,30]_2','minimum_words':36,'coordinate_minimum_shell_signatures_unique':True},
      'dual':{'parameters':'[135,119,3]_2','weight_enumerator':{str(k):int(v) for k,v in dual.items() if v},'minimum_words':270,'minimum_shell_equals_selected_270_lines':True},
      'intrinsic_Jacobi_graph':{'vertices':36,'pair_class_sizes':[270,360],'chosen_relation_pairs':270,'degree':15,'transport_equals_W33_spread_overlap4_graph':True,'full_graph_automorphism_order':51840},
      'automorphism_group':{'upper_bound':51840,'upper_reason':'faithful action on intrinsic Jacobi graph','explicit_lower_group':'PGSp(4,3)','lower_order':51840,'order':51840,'identification':'Aut(C)=PGSp(4,3)'},
      'theorem':'The code C=[135,16,30]_2 reconstructs the selected geometry from its dual weight-three shell, and its full coordinate automorphism group is exactly PGSp(4,3) of order 51840. The upper bound is code-intrinsic via the 36-minword/weight45 Jacobi graph; the lower bound is an explicit outer-similitude action.',
      'boundary':'Exact binary-code and permutation-group theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(out,indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
