#!/usr/bin/env python3
"""Passes 4836/4840 — classify the 1080 binary Levi minimum words and their K3,3 bridge.

The [1620,64,96]_2 minimum words are twelvefold repetitions of the 8-cycles of
the GQ(4,2) Levi graph. Project an 8-cycle to its four quotient-line vertices;
these form a 4-cycle in the SRG(27,10,1,5) line graph. Conversely every line
4-cycle lifts uniquely through the four pairwise intersection packets, giving a
Levi 8-cycle. The producer verifies this bijection, the PSp/PGSp orbit structure,
pairwise edge-intersection census, and incidence with the 360 induced K3,3
ternary homology witnesses of Pass4808.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import networkx as nx
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle,compose
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
ROOT=Path(__file__).resolve().parents[1]
OUT36=ROOT/'data/PART_W33_PASS4836_LEVI_MINIMUM_ORBITS.json'
OUT40=ROOT/'data/PART_W33_PASS4840_LEVI_CYCLE_K33_INCIDENCE.json'

def pmask(m,p):
    y=0;x=int(m)
    while x:
        b=x&-x;i=b.bit_length()-1;x^=b;y|=1<<p[i]
    return y

def canon_cycle(C):
    C=list(C);R=list(reversed(C));cand=[]
    for s in range(len(C)):
        cand.append(tuple(C[s:]+C[:s]));cand.append(tuple(R[s:]+R[:s]))
    return min(cand)

def count_k33(G):
    out=[]
    for S in itertools.combinations(range(27),6):
        H=G.subgraph(S)
        if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
            A,B=nx.algorithms.bipartite.sets(H)
            if len(A)==len(B)==3:out.append(frozenset(S))
    return sorted(set(out),key=lambda x:tuple(sorted(x)))

def orbit(seed,gens):
    seen={seed};Q=[seed]
    while Q:
        x=Q.pop()
        for p in gens:
            y=p[x]
            if y not in seen:seen.add(y);Q.append(y)
    return seen

def main():
    D=build_all();B=build_bundle();packets=B['packets'];K5=[frozenset(x) for x in B['K5']];G45=B['G45']
    # Levi graph and all 8-cycles.
    ledges=sorted((p,L) for L,S in enumerate(K5) for p in S);lei={e:i for i,e in enumerate(ledges)}
    Levi=nx.Graph();Levi.add_nodes_from(range(72));Levi.add_edges_from((p,45+L) for p,L in ledges)
    cycles=set()
    for s in range(72):
        def dfs(path):
            if len(path)==8:
                if Levi.has_edge(path[-1],s):cycles.add(canon_cycle(path))
                return
            for v in Levi[path[-1]]:
                if v==s or v in path or v<s:continue
                dfs(path+[v])
        dfs([s])
    cycles=sorted(cycles);assert len(cycles)==1080
    cmasks=[];line4=[]
    for C in cycles:
        m=0
        for a,b in zip(C,C[1:]+C[:1]):
            if a>=45:a,b=b,a
            m|=1<<lei[(a,b-45)]
        cmasks.append(m)
        L=frozenset(v-45 for v in C if v>=45);assert len(L)==4;line4.append(L)
    assert len(set(line4))==1080
    # quotient line graph and exact 4-cycle census.
    qG=nx.Graph();qG.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if K5[i]&K5[j]:qG.add_edge(i,j)
    assert qG.number_of_edges()==135 and set(dict(qG.degree()).values())=={10}
    q4=set()
    for S in itertools.combinations(range(27),4):
        H=qG.subgraph(S)
        if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):q4.add(frozenset(S))
    assert len(q4)==1080 and set(line4)==q4

    # Common PSp/PGSp action on packets and quotient lines, then on cycles via line4 labels.
    pts=D['pts'];wlines=D['lines'];sing=D['selected135'];pidx={p:i for i,p in enumerate(pts)};pgens,PSp,full=build_groups(pts,pidx,wlines);outer=next(g for g in full if g not in PSp);fullgens=list(pgens)+[outer]
    all40=(1<<40)-1;rep=lambda x:min(int(x),int(x)^all40);sidx={int(x):i for i,x in enumerate(sing)};packet_of={s:p for p,T in enumerate(packets) for s in T};kidx={S:i for i,S in enumerate(K5)}
    def packet_perm(g):
        sp=[sidx[rep(pmask(sing[i],g))] for i in range(135)];q=[]
        for T in packets:
            z={packet_of[sp[s]] for s in T};assert len(z)==1;q.append(next(iter(z)))
        return tuple(q)
    pp=[packet_perm(g) for g in fullgens]
    lp=[]
    for p in pp:lp.append(tuple(kidx[frozenset(p[x] for x in S)] for S in K5))
    cindex={S:i for i,S in enumerate(line4)};cperms=[]
    for p in lp:cperms.append(tuple(cindex[frozenset(p[x] for x in S)] for S in line4))
    Op=orbit(0,cperms[:len(pgens)]);Of=orbit(0,cperms);p_orbit=len(Op);f_orbit=len(Of)
    assert 25920%p_orbit==0 and 51840%f_orbit==0

    # Pairwise physical/Levi edge intersection census from one representative; if transitive this is global valency data.
    repm=cmasks[0];inter=Counter((repm&m).bit_count() for m in cmasks[1:])
    # Cell/packet/line incidence of one minimum word.
    C0=cycles[0];pack0={v for v in C0 if v<45};line0={v-45 for v in C0 if v>=45};assert len(pack0)==len(line0)==4

    # Ternary K3,3 witnesses: exact incidence through the projected 4-cycle.
    K33=count_k33(qG);assert len(K33)==360
    containment=Counter(sum(1 for K in K33 if S<=K) for S in line4)
    reverse=Counter(sum(1 for S in q4 if S<=K) for K in K33)
    total_inc=sum(k*v for k,v in containment.items());assert total_inc==sum(k*v for k,v in reverse.items())==360*9

    # Intersection-size relation graphs: test which are SRG, without assuming intersection size is a full orbital.
    srg={}
    for k in sorted(x for x in inter if x>0):
        adj=[set() for _ in range(1080)]
        for i,j in itertools.combinations(range(1080),2):
            if (cmasks[i]&cmasks[j]).bit_count()==k:adj[i].add(j);adj[j].add(i)
        deg={len(a) for a in adj}
        if len(deg)!=1:srg[str(k)]={'regular':False,'degree_set':sorted(deg)};continue
        d=next(iter(deg));lam=set();mu=set()
        for i,j in itertools.combinations(range(1080),2):
            z=len(adj[i]&adj[j]);(lam if j in adj[i] else mu).add(z)
            if len(lam)>1 or len(mu)>1:break
        srg[str(k)]={'regular':True,'degree':d,'strongly_regular':len(lam)==1 and len(mu)==1,'lambda_values':sorted(lam),'mu_values':sorted(mu)}

    out36={'pass':4836,'code':'[1620,64,96]_2','minimum_words':1080,'Levi_8_cycles':1080,'projection_to_27_line_graph':'bijection with the 1080 four-cycles of SRG(27,10,1,5)','PSp':{'orbit_size_of_representative':p_orbit,'stabilizer_order':25920//p_orbit},'PGSp':{'orbit_size_of_representative':f_orbit,'stabilizer_order':51840//f_orbit},'representative_pairwise_shared_Levi_edge_census':dict(sorted(inter.items())),'representative_touches_packets':4,'representative_touches_K6_cells':12,'representative_touches_quotient_lines':4,'theorem':'The 1080 minimum binary Levi codewords are exactly the twelvefold repetitions of Levi 8-cycles, equivalently the 1080 four-cycles of the 27-line Schlaefli graph. The frozen group orbit sizes/stabilizers classify their PSp/PGSp action.','boundary':'Binary minimum-shell orbit theorem only; no identification with ternary homology witnesses is made from counts.'}
    OUT36.write_text(json.dumps(out36,indent=2,sort_keys=True)+'\n')
    out40={'pass':4840,'binary_cycle_count':1080,'ternary_induced_K33_count':360,'K33_to_binary_cycle_incidence':dict(sorted(reverse.items())),'binary_cycle_to_K33_incidence':dict(sorted(containment.items())),'total_incidence':total_inc,'intersection_relation_tests':srg,'theorem':'The exact incidence between the 1080 binary Levi 8-cycles and the 360 induced K3,3 ternary homology witnesses is computed objectwise through their quotient-line supports. Every claimed 3-to-9 relation, if present in the frozen census, is therefore incidence-theoretic rather than the numerical equality 1080=3*360.','boundary':'The K3,3 objects are canonical ternary projective weight-6 witnesses, not asserted to exhaust the full ternary minimum quotient shell.'}
    OUT40.write_text(json.dumps(out40,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4836':out36,'4840':out40},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
