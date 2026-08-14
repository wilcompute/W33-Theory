#!/usr/bin/env python3
"""Passes 5090, 5094-5097: the C2 root-direction derivative geometry.

Finite statements only.  The formal identity d(q^4)/dq=4q^3 is interpreted
combinatorially as a root-subgroup coset count; q is not treated as a
continuous physical variable.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
import numpy as np
import networkx as nx
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS5090_5094_5097_ROOT_DERIVATIVE_GEOMETRY.json'

def prime_building(q:int):
    def norm(v):
        for a in v:
            if a%q:
                z=pow(a,-1,q);return tuple((z*x)%q for x in v)
        raise ValueError('zero')
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)}
    def symp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%q
    def span(x,y):
        S=set()
        for a,b in itertools.product(range(q),repeat=2):
            if a or b:S.add(norm(tuple((a*x[i]+b*y[i])%q for i in range(4))))
        return frozenset(pi[z] for z in S)
    nbr=[set() for _ in pts];LS=set()
    for i,j in itertools.combinations(range(len(pts)),2):
        if symp(pts[i],pts[j])==0:
            nbr[i].add(j);nbr[j].add(i);LS.add(span(pts[i],pts[j]))
    lines=sorted(LS,key=lambda s:tuple(sorted(s)))
    pair_line={}
    for l,L in enumerate(lines):
        for a,b in itertools.combinations(sorted(L),2):pair_line[tuple(sorted((a,b)))]=l
    flags=[(p,l) for l,L in enumerate(lines) for p in sorted(L)];fi={f:i for i,f in enumerate(flags)}
    apts=set();oppP=[]
    for p,r in itertools.combinations(range(len(pts)),2):
        if r not in nbr[p]:
            common=sorted(nbr[p]&nbr[r]);assert len(common)==q+1;oppP.append((p,r,common))
            for a,b in itertools.combinations(common,2):apts.add(frozenset((p,r,a,b)))
    apts=sorted(apts,key=lambda s:tuple(sorted(s)));ai={A:i for i,A in enumerate(apts)}
    apt_lines=[];apt_flags=[]
    for S in apts:
        ed=[(a,b) for a,b in itertools.combinations(sorted(S),2) if b in nbr[a]];assert len(ed)==4
        LL=frozenset(pair_line[tuple(sorted(e))] for e in ed);apt_lines.append(LL)
        F=set()
        for a,b in ed:
            l=pair_line[tuple(sorted((a,b)))];F|={fi[(a,l)],fi[(b,l)]}
        apt_flags.append(frozenset(F))
    ail={L:i for i,L in enumerate(apt_lines)}
    lnbr=[set() for _ in lines]
    for i,j in itertools.combinations(range(len(lines)),2):
        if lines[i]&lines[j]:lnbr[i].add(j);lnbr[j].add(i)
    oppL=[]
    for l,m in itertools.combinations(range(len(lines)),2):
        if m not in lnbr[l]:
            common=sorted(lnbr[l]&lnbr[m]);assert len(common)==q+1;oppL.append((l,m,common))
    base=0;support={a for a,F in enumerate(apt_flags) if base in F};assert len(support)==q**4
    active=[]
    for p,r,common in oppP:
        S={ai[frozenset((p,r,common[i],common[j]))] for i,j in itertools.combinations(range(q+1),2)}
        T=frozenset(S&support)
        if T:active.append(T)
    for l,m,common in oppL:
        S={ail[frozenset((l,m,common[i],common[j]))] for i,j in itertools.combinations(range(q+1),2)}
        T=frozenset(S&support)
        if T:active.append(T)
    assert len(active)==4*q**3 and {len(x) for x in active}=={q}
    sl=sorted(support);pos={a:i for i,a in enumerate(sl)}
    G=nx.Graph();G.add_nodes_from(range(len(sl)))
    active_local=[]
    for T in active:
        C=frozenset(pos[a] for a in T);active_local.append(C)
        G.add_edges_from(itertools.combinations(C,2))
    assert set(dict(G.degree()).values())=={4*(q-1)}
    return G,set(active_local)

def root_coset_geometry(q:int):
    I=np.eye(4,dtype=int)%q
    J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],dtype=int)%q
    def E(i,j):
        A=np.zeros((4,4),dtype=int);A[i,j]=1;return A
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    def mm(A,B):return (A@B)%q
    def key(A):return tuple(map(int,A.flat))
    def spok(A):return np.array_equal((A.T@J@A)%q,J)
    roots=[]
    for Z in X:
        H=[(I+t*Z)%q for t in range(q)];assert all(spok(h) for h in H);roots.append(H)
    gens=[H[1] for H in roots];U={key(I):I};Q=deque([I])
    while Q:
        A=Q.popleft()
        for g in gens:
            B=mm(A,g);k=key(B)
            if k not in U:U[k]=B;Q.append(B)
    assert len(U)==q**4
    el=list(U.values());ei={key(A):i for i,A in enumerate(el)};lines=[];families=[]
    for f,H in enumerate(roots):
        seen=set()
        for g in el:
            C=frozenset(ei[key(mm(g,h))] for h in H)
            if C not in seen:seen.add(C);lines.append(C);families.append(f)
        assert len(seen)==q**3
    G=nx.Graph();G.add_nodes_from(range(q**4))
    for C in lines:G.add_edges_from(itertools.combinations(C,2))
    return G,set(lines),families,roots,mm,key,I

def subgroup_census(q,roots,mm,key,I):
    def close(ids):
        gs=[roots[i][1] for i in ids];S={key(I):I};Q=deque([I])
        while Q:
            A=Q.popleft()
            for g in gs:
                B=mm(A,g);k=key(B)
                if k not in S:S[k]=B;Q.append(B)
        return len(S)
    return [close((i,j)) for i,j in itertools.combinations(range(4),2)]

def aut_order_and_family_action(G,lines,families):
    lf={C:f for C,f in zip(sorted(lines,key=lambda z:tuple(sorted(z))),families)}
    # Rebuild family dictionary from the actual coset enumeration order if sorting changed.
    # The caller only needs the order and the fact that all four intrinsic parallel classes are fixed setwise;
    # recover parallel classes as disjoint line partitions.
    LL=list(lines);disj=nx.Graph();disj.add_nodes_from(range(len(LL)))
    for i,j in itertools.combinations(range(len(LL)),2):
        if LL[i].isdisjoint(LL[j]):disj.add_edge(i,j)
    # Parallel classes are cliques of q^3 mutually disjoint lines. For q=3 they are the four size-27 classes.
    classes=[frozenset(c) for c in nx.find_cliques(disj) if len(c)==27]
    classes=list(set(classes));assert len(classes)==4
    line_to_class={LL[i]:k for k,C in enumerate(classes) for i in C}
    n=0;perms=Counter()
    for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter():
        n+=1;p=[]
        for C in classes:
            imgs={line_to_class[frozenset(m[v] for v in LL[i])] for i in C};assert len(imgs)==1;p.append(next(iter(imgs)))
        perms[tuple(p)]+=1
    return n,perms

def main():
    anchors={}
    for q in (2,3):
        GB,LB=prime_building(q);GU,LU,fam,roots,mm,key,I=root_coset_geometry(q)
        gm=nx.algorithms.isomorphism.GraphMatcher(GB,GU);assert gm.is_isomorphic();mp=gm.mapping
        assert {frozenset(mp[v] for v in C) for C in LB}==LU
        anchors[q]={'apartments_through_chamber':q**4,'active_charts':4*q**3,'chart_size':q,
                    'vertex_degree':4*(q-1),'graph_isomorphic_to_root_cosets':True}
        if q==3:
            A=sp.zeros(81)
            for u,v in GU.edges():A[u,v]=A[v,u]=1
            cp=str(sp.factor(A.charpoly().as_expr()))
            shells=[]
            for s in GU:
                d=nx.single_source_shortest_path_length(GU,s);shells.append(tuple(Counter(d.values()).get(i,0) for i in range(4)))
            assert set(shells)=={(1,8,32,40)}
            aut=0
            for _ in nx.algorithms.isomorphism.GraphMatcher(GU,GU).isomorphisms_iter():aut+=1
            assert aut==324
            anchors[q].update({'diameter':3,'shells':[1,8,32,40],'charpoly':cp,'automorphism_group_order':aut,
                               'full_projective_chamber_stabilizer_order':51840//160})
    # Higher root-direction closure: odd characteristic has the C2 commutator profile q^2^4,q^3,q^4.
    curvature={}
    for q in (2,3,5,7):
        _,_,_,roots,mm,key,I=root_coset_geometry(q);vals=sorted(subgroup_census(q,roots,mm,key,I));curvature[q]=vals
    assert curvature[3]==[9,9,9,9,27,81] and curvature[5]==[25,25,25,25,125,625] and curvature[7]==[49,49,49,49,343,2401]
    assert curvature[2]==[4,4,4,4,4,8]
    result={
      '5090':{'status':'THEOREM','statement':'For the C2 building W(3,q), the q^4 apartments through a fixed chamber form the opposite-chamber unipotent cell. Its four positive-root subgroup orbit families contain q^3 active charts each, of size q. Hence A_chamber=4q^3=d(q^4)/dq as a formal root-coset count.','analytic_boundary':'q is a prime power; the derivative notation is formal/combinatorial, not an infinitesimal variation of finite fields.','anchors':anchors},
      '5094':{'status':'EXACT_Q3_GRAPH_THEOREM','graph':'Cay(U,{U_alpha\\{1}: alpha positive})','vertices':81,'root_coset_lines':108,'degree':8,'diameter':3,'shells':[1,8,32,40],'charpoly':anchors[3]['charpoly'],'not_hamming_H43':True},
      '5095':{'status':'ROOT_COMMUTATOR_CURVATURE','odd_q_unordered_pair_generated_orders':'q^2 four times, q^3 once, q^4 once','q2_orders':curvature[2],'q3_orders':curvature[3],'q5_orders':curvature[5],'q7_orders':curvature[7],'interpretation':'First root-direction derivative is flat; second-direction composition is deformed by C2 commutators. Characteristic two has the expected bad-characteristic collapse.'},
      '5096':{'status':'GENERAL_SPLIT_LIE_TYPE_COUNT','statement':'For a split finite Chevalley group with N positive roots and maximal unipotent U, |U|=q^N=deg(St). Each root subgroup has order q, so the total number of positive-root subgroup cosets is N q^(N-1)=d(q^N)/dq.','C2':{'N':4,'value':'4q^3'}},
      '5097':{'status':'EXACT_Q3_AUTOMORPHISM_CLOSURE','derivative_graph_aut_order':324,'PGSp_chamber_stabilizer_order':324,'consequence':'The q=3 first-derivative graph has exactly the full projective chamber-stabilizer symmetry; no larger graph automorphism group occurs.'}
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
