#!/usr/bin/env python3
"""Pass7492: identify the 40 marked triples over one double-six with the 40 W33 points.

The Pass4964 transceiver gives the SAME W(E6)=PGSp(4,3) elements as permutations of
27 cubic lines and 40 W33 points.  Fix one double-six.  Its stabilizer has order 1440.
It acts on the 40 objects obtained by choosing one of its two sixers and a 3-subset of
that sixer.  We prove this 40-point action is equivariantly isomorphic to the stabilizer's
natural action on the 40 W33 points, and freeze an explicit bijection.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import networkx as nx
import numpy as np
import w33_pass4964_4965_4967_double_six_spread_transceiver as p
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7492_MARKED_TRIPLE_W33_POINT_EQUIVARIANT.json'

def paired_closure(gens):
    I27=tuple(range(27));I40=tuple(range(40));S={(I27,I40)};Q=deque([(I27,I40)])
    while Q:
        a,b=Q.popleft()
        for x,y in gens:
            z=(p.comp(x,a),p.comp(y,b))
            if z not in S:S.add(z);Q.append(z)
    return S

def build_actions():
    # Copy the canonical Pass4964 finite construction only through the 27-line / 40-point actions.
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if p.Q6(v)==0];nons=[v for v in vecs if p.Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[tuple(si[p.add2(x,v) if p.polar(x,v) else x] for x in sing) for v in nons]
    gp=[];S={tuple(range(27))}
    for g in [p.comp(trans[0],t) for t in trans[1:]]:
        T=p.closure(gp+[g],27)
        if len(T)>len(S):gp.append(g);S=T
        if len(S)==25920:break
    assert len(S)==25920
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    p27=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    l27=[tuple(i for i,P in enumerate(p27) if x in P) for x in qp]
    G27=nx.Graph();G27.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(l27[i])&set(l27[j]):G27.add_edge(i,j)
    C6=sorted({frozenset(c) for c in nx.find_cliques(nx.complement(G27)) if len(c)==6},key=lambda x:tuple(sorted(x)));assert len(C6)==72
    DS=[];halves=[]
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G27.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):
            U=frozenset(A|B)
            if U not in DS:DS.append(U);halves.append((A,B))
    order=sorted(range(36),key=lambda i:tuple(sorted(DS[i])));DS=[DS[i] for i in order];halves=[halves[i] for i in order];di={D:i for i,D in enumerate(DS)}
    # Steiner triples of double-sixes and their 40 fibres.
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    st=sorted(t for t in itertools.combinations(range(36),3) if all(H36.has_edge(*e) for e in itertools.combinations(t,2)) and len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0);assert len(st)==120;sti={t:i for i,t in enumerate(st)}
    DP=[];SP=[]
    for g in gp:
        dp=tuple(di[frozenset(g[x] for x in D)] for D in DS);DP.append(dp)
        SP.append(tuple(sti[tuple(sorted(dp[i] for i in t))] for t in st))
    seen=set();orbits=[]
    for z in itertools.combinations(range(120),2):
        if z in seen:continue
        O={z};seen.add(z);Q=deque([z])
        while Q:
            a=Q.popleft()
            for op in SP:
                c=tuple(sorted((op[a[0]],op[a[1]])))
                if c not in O:O.add(c);seen.add(c);Q.append(c)
        orbits.append(sorted(O))
    R1,R2,R3,R4=sorted(orbits,key=len);assert list(map(len,(R1,R2,R3,R4)))==[120,1620,2160,3240]
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1)
    fibers=sorted([sorted(c) for c in nx.connected_components(FG)]);assert len(fibers)==40
    fi={x:i for i,F in enumerate(fibers) for x in F};fiber_index={frozenset(F):i for i,F in enumerate(fibers)}
    FP=[]
    for op in SP:FP.append(tuple(fiber_index[frozenset(op[x] for x in F)] for F in fibers))
    # Full outer generator and its 40-point action.
    gout=trans[0];dpout=tuple(di[frozenset(gout[x] for x in D)] for D in DS);spout=tuple(sti[tuple(sorted(dpout[i] for i in t))] for t in st);fpout=tuple(fiber_index[frozenset(spout[x] for x in F)] for F in fibers)
    full=paired_closure(list(zip(gp,FP))+[(gout,fpout)]);assert len(full)==51840
    return G27,C6,DS,halves,full

def main():
    G27,C6,DS,halves,full=build_actions();D0=DS[0];A,B=halves[0];assert A|B==D0 and not(A&B)
    stab=[z for z in full if frozenset(z[0][x] for x in D0)==D0];assert len(stab)==1440
    halves0=[frozenset(A),frozenset(B)];mark=[]
    for h,S in enumerate(halves0):
        for T in itertools.combinations(sorted(S),3):mark.append((h,frozenset(T)))
    assert len(mark)==40;mi={x:i for i,x in enumerate(mark)}
    def markperm(g):
        out=[]
        for h,T in mark:
            U=frozenset(g[x] for x in T);H=frozenset(g[x] for x in halves0[h]);hh=halves0.index(H);out.append(mi[(hh,U)])
        return tuple(out)
    actions=[(markperm(g),p40) for g,p40 in stab]
    assert len({a for a,b in actions})==1440 and len({b for a,b in actions})==1440
    # Both actions are transitive.
    assert {a[0] for a,b in actions}==set(range(40)) and {b[0] for a,b in actions}==set(range(40))
    hm=[(a,b) for a,b in actions if a[0]==0];assert len(hm)==36
    fixed=[x for x in range(40) if all(b[x]==x for a,b in hm)];assert len(fixed)==1;p0=fixed[0]
    bridge={}
    for a,b in actions:
        x=a[0];y=b[p0]
        if x in bridge:assert bridge[x]==y
        bridge[x]=y
    assert len(bridge)==40 and len(set(bridge.values()))==40
    assert all(bridge[a[x]]==b[bridge[x]] for a,b in actions for x in range(40))
    # Compare permutation characters element-by-element.
    char_ok=all(sum(i==a[i] for i in range(40))==sum(i==b[i] for i in range(40)) for a,b in actions);assert char_ok
    # What does triple complementation become on W33 points?
    cinv=[]
    for h,T in mark:cinv.append(mi[(h,frozenset(halves0[h]-T))])
    wcinv=[None]*40
    for i,j in enumerate(cinv):wcinv[bridge[i]]=bridge[j]
    assert all(wcinv[wcinv[i]]==i and wcinv[i]!=i for i in range(40))
    # Reconstruct W33 adjacency from the full 40-point action's canonical Steiner fibre graph:
    # the unique orbit size 240 on unordered pairs is the W33 edge relation.
    pair_orbits=[];seen=set()
    for e in itertools.combinations(range(40),2):
        if e in seen:continue
        O={tuple(sorted((b[e[0]],b[e[1]]))) for a,b in actions};seen|=O;pair_orbits.append(O)
    sizes=sorted(map(len,pair_orbits));
    # Stabilizer need not reproduce the full W33 rank-3 action, so only freeze complement-pair orbit size under this subgroup.
    cpairs={tuple(sorted((i,wcinv[i]))) for i in range(40)};assert len(cpairs)==20
    orbit_sizes=sorted(len(O) for O in pair_orbits)
    out={'schema':'w33.pass7492.marked_triple_w33_point_equivariant.v1','status':'PASS',
      'fixed_double_six_index':0,'double_six_stabilizer_order':1440,'marked_triples':40,'W33_points':40,
      'marked_point_stabilizer_order':36,'unique_W33_point_fixed_by_marked_stabilizer':p0,
      'equivariant_bijection_marked_index_to_W33_point':[bridge[i] for i in range(40)],
      'elementwise_permutation_characters_equal':True,
      'triple_complement_involution':{'pairs':20,'transported_W33_permutation':wcinv},
      'stabilizer_pair_orbit_sizes':orbit_sizes,
      'theorem':'For one double-six, its order-1440 stabilizer acts on the 40 marked sixer triples in exactly the same permutation representation as it acts on the 40 W33 points under the Pass4964 W(E6)=PGSp(4,3) transceiver. The displayed bijection is equivariant for all 1440 stabilizer elements.',
      'interpretation':'The 1440=36*40 bundle is not merely numerical: the 40-object fibre over a double-six is a concrete W33 point model for that double-six/spread stabilizer.',
      'boundary':'The map depends on the already-certified equivariant transceiver/gauge choice; no physical state identification is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','stab':1440,'point_stab':36,'fixed_point':p0,'pair_orbits':orbit_sizes}))
if __name__=='__main__':main()
