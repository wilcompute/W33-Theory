#!/usr/bin/env python3
"""Pass 4595 -- concrete W33 lifts of both D4 half-spinor families.

The 270 maximal singular 4-spaces of the protected O+(8,2) geometry split into
two D4 half-spinor families.  Under PSp(4,3) one family is transitive of degree
135; the other decomposes 27+36+36+36.  This pass gives W33 objects for all of
those pieces instead of using counts as labels.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,deque
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix,norm3
from w33_pass4588_apartment_triality_obstruction_spread_bridge import perm_group,pmask
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4595_CONCRETE_D4_TRIALITY_W33_LIFTS.json'

def rep_builder(Astar):
    j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if Astar[i,k]]
    V=set(span(rank_basis_int([cols[i]^cols[k] for i,k in edges])));assert len(V)==512 and j in V
    rep=lambda x:min(int(x),int(x)^j);q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    return rep,q,polar

def max_generators(singular,rep,q,polar):
    levels={0:{frozenset((0,))}}
    for d in range(4):
        nxt=set()
        for S in levels[d]:
            for v in singular:
                if v in S or any(polar(v,u) for u in S):continue
                T=frozenset(set(S)|{rep(u^v) for u in S})
                if len(T)==1<<(d+1) and all(q(u)==0 for u in T):nxt.add(T)
        levels[d+1]=nxt
    G=sorted(levels[4],key=lambda X:tuple(sorted(X)));assert len(G)==270;return G

def orbit(seed,G,act):return {act(seed,g) for g in G}
def point_perm(M,pts,pidx):
    out=[]
    for p in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(p,dtype=int))%3;out.append(pidx[norm3(tuple(map(int,y)))])
    return tuple(out)
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def pair_group(gens):
    I=(tuple(range(40)),tuple(range(40)));S={I};Q=deque([I])
    while Q:
        a,b=Q.popleft()
        for x,y in gens:
            z=(compose(x,a),compose(y,b))
            if z not in S:S.add(z);Q.append(z)
    return S

def exact_spreads(lines,size):
    byp=defaultdict(list)
    for i,L in enumerate(lines):
        for p in L:byp[p].append(i)
    out=set()
    def go(chosen,used,start=0):
        if len(chosen)==size:
            out.add(tuple(sorted(chosen)));return
        # choose uncovered point with fewest admissible lines
        candpts=[p for p in range(40) if p not in used]
        if not candpts:return
        p=min(candpts,key=lambda z:sum(used.isdisjoint(lines[i]) for i in byp[z]))
        for i in byp[p]:
            L=set(lines[i])
            if used.isdisjoint(L):go(chosen+[i],used|L)
    go([],set());return sorted(out)
def partial8(lines):
    # enumerate pairwise-disjoint 8-line sets; there are exactly 1755.
    dis=[set() for _ in range(40)]
    for i,j in itertools.combinations(range(40),2):
        if set(lines[i]).isdisjoint(lines[j]):dis[i].add(j);dis[j].add(i)
    out=set()
    def rec(chosen,cands):
        if len(chosen)==8:out.add(tuple(chosen));return
        for pos,i in enumerate(sorted(cands)):
            rec(chosen+[i],{j for j in cands if j>i and j in dis[i]})
    rec([],set(range(40)));return sorted(out)
def center_quads(Apoint):
    nb=[set(np.flatnonzero(Apoint[i]).tolist()) for i in range(40)];qs=set()
    for a,b,c in itertools.combinations(range(40),3):
        if Apoint[a,b] or Apoint[a,c] or Apoint[b,c]:continue
        X=frozenset(nb[a]&nb[b]&nb[c])
        if len(X)==4:qs.add(X)
    qs=sorted(qs,key=lambda X:tuple(sorted(X)));qi={q:i for i,q in enumerate(qs)};pair={}
    for i,Q in enumerate(qs):pair[i]=qi[frozenset(set.intersection(*(nb[v] for v in Q)))]
    seen=set();supports=[]
    for i in range(90):
        z=tuple(sorted((i,pair[i])))
        if z in seen:continue
        seen.add(z);supports.append(frozenset(qs[z[0]]|qs[z[1]]))
    supports=sorted(supports,key=lambda X:tuple(sorted(X)));ql=[]
    for C in itertools.combinations(range(45),5):
        U=set();ok=True
        for i in C:
            if U&supports[i]:ok=False;break
            U|=set(supports[i])
        if ok and len(U)==40:ql.append(frozenset(C))
    assert len(ql)==27;return supports,ql

def main():
    pts,pidx,lines,lidx,Apoint,Astar,_,_,_=build_geometry();Apoint=np.asarray(Apoint,dtype=np.uint8);Astar=np.asarray(Astar,dtype=np.uint8)
    rep,q,polar=rep_builder(Astar);singular=sorted(x for x in {rep(x) for x in span(rank_basis_int([sum(int(Astar[r,c])<<r for r in np.flatnonzero(Astar[:,c])) for c in range(40)]))} if x and q(x)==0)
    # safer full protected class extraction from edge span
    cols=[sum(1<<int(r) for r in np.flatnonzero(Astar[:,c])) for c in range(40)];B=rank_basis_int([cols[i]^cols[k] for i,k in itertools.combinations(range(40),2) if Astar[i,k]])
    singular=sorted(x for x in {rep(v) for v in span(B)} if x and q(x)==0);assert len(singular)==135
    MG=max_generators(singular,rep,q,polar)
    # paired PSp action.
    gens=[];PG={(tuple(range(40)),tuple(range(40)))}
    for v in pts:
        M=transvection_matrix(v);gp=point_perm(M,pts,pidx);gl=build_line_perm(M,pts,pidx,lines,lidx)
        trial=pair_group(gens+[(gp,gl)])
        if len(trial)>len(PG):gens.append((gp,gl));PG=trial
        if len(PG)==25920:break
    actX=lambda X,g:frozenset(rep(pmask(x,g[1])) for x in X)
    rem=set(MG);orbits=[]
    while rem:
        X=next(iter(rem));O={actX(X,g) for g in PG};orbits.append(O);rem-=O
    assert sorted(map(len,orbits))==[27,36,36,36,135]
    O135=[O for O in orbits if len(O)==135][0];X=next(iter(O135));H=[g for g in PG if actX(X,g)==X];assert len(H)==192
    P8=partial8(lines);assert len(P8)==1755
    unext=[]
    for S in P8:
        used=set().union(*(set(lines[i]) for i in S));
        if not any(used.isdisjoint(lines[j]) for j in range(40) if j not in S):unext.append(S)
    assert len(unext)==135
    def act_lineset(S,g):return tuple(sorted(g[1][i] for i in S))
    fixed8=[S for S in unext if all(act_lineset(S,g)==S for g in H)];assert len(fixed8)==3
    # each is one H-orbit on lines and has stabilizer H.
    line_orbits=[];remL=set(range(40))
    while remL:
        a=min(remL);O={g[1][a] for g in H};line_orbits.append(O);remL-=O
    assert sorted(map(len,line_orbits))==[8,8,8,16]
    assert {frozenset(S) for S in fixed8}=={frozenset(O) for O in line_orbits if len(O)==8}
    assert all(len([g for g in PG if act_lineset(S,g)==S])==192 for S in fixed8)

    # The 27 orbit is the center-quad/E6 quotient-line G-set.
    supports,qlines=center_quads(Apoint);sidx={S:i for i,S in enumerate(supports)}
    O27=[O for O in orbits if len(O)==27][0];Y=next(iter(O27));HY=[g for g in PG if actX(Y,g)==Y];assert len(HY)==960
    def act_qline(L,g):return frozenset(sidx[frozenset(g[0][p] for p in supports[i])] for i in L)
    fixedql=[L for L in qlines if all(act_qline(L,g)==L for g in HY)];assert len(fixedql)==1

    # The three degree-36 orbits are each the W33 spread G-set (recheck Pass4588).
    spreads=exact_spreads(lines,10);assert len(spreads)==36
    d36=[]
    for O in [O for O in orbits if len(O)==36]:
        Z=next(iter(O));HZ=[g for g in PG if actX(Z,g)==Z];assert len(HZ)==720
        fixed=[S for S in spreads if all(act_lineset(S,g)==S for g in HZ)];assert len(fixed)==1
        d36.append({'orbit_size':36,'stabilizer_order':720,'fixed_W33_spreads':1})
    out={'pass':4595,'half_spinor_PSp_orbits':sorted(map(len,orbits)),
      'transitive_135_family':{'stabilizer_order':192,'fixed_maximal_size8_partial_spreads':3,'fixed_spreads_are_exactly_three_8_line_orbits':True,'line_orbits':[8,8,8,16],
        'each_fixed_partial_spread_stabilizer_order':192,'interpretation':'a half-spinor generator has a concrete three-valued W33 lift by its three maximal 8-line partial spreads'},
      'other_family':{'decomposition':[27,36,36,36],'orbit27':{'stabilizer_order':960,'fixed_center_quad_E6_quotient_lines':1,'G_set_identification':'27 half-spinor orbit = 27 center-quad/E6 quotient lines'},
        'orbit36':d36,'G_set_identification_36':'each degree-36 half-spinor orbit = W33 spread G-set'},
      'partial_spread_census':{'size8_total':1755,'unextendable_maximal':135,'reconfirms_Pass1100':True},
      'theorem':'All 270 D4 half-spinor generators now have concrete W33-derived lifts: the transitive 135 family through triples of maximal size-8 partial spreads, and the other family as 27 center-quad quotient lines plus three 36-spread copies.',
      'boundary':'The three-valued lift of the transitive half-spinor family is genuinely noncanonical under PSp; no physical spinor interpretation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
