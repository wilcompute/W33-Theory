#!/usr/bin/env python3
"""Pass5098-5101: collision-clean root-coset supplement.

5098: q=2,3 chamber-star active-chart hypergraph ~= C2 positive-root cosets.
5099: q=3 derivative graph Aut = U_81 semidirect V4.
5100: general split-Lie positive-root coset derivative law N q^(N-1).
5101: exact C2 second-direction commutator profile in odd characteristic.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
import numpy as np
import networkx as nx
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS5098_5101_ROOT_COSET_SUPPLEMENT.json'

def prime_building(q):
    def norm(v):
        for a in v:
            if a%q:
                z=pow(a,-1,q);return tuple((z*x)%q for x in v)
        raise ValueError
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
    def s(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%q
    def span(x,y):
        S=set()
        for a,b in itertools.product(range(q),repeat=2):
            if a or b:S.add(norm(tuple((a*x[i]+b*y[i])%q for i in range(4))))
        return frozenset(pi[z] for z in S)
    nbr=[set() for _ in pts];LS=set()
    for i,j in itertools.combinations(range(len(pts)),2):
        if s(pts[i],pts[j])==0:nbr[i].add(j);nbr[j].add(i);LS.add(span(pts[i],pts[j]))
    lines=sorted(LS,key=lambda z:tuple(sorted(z)));pair_line={}
    for l,L in enumerate(lines):
        for a,b in itertools.combinations(sorted(L),2):pair_line[tuple(sorted((a,b)))]=l
    flags=[(p,l) for l,L in enumerate(lines) for p in sorted(L)];fi={f:i for i,f in enumerate(flags)}
    A=set();oppP=[]
    for p,r in itertools.combinations(range(len(pts)),2):
        if r not in nbr[p]:
            c=sorted(nbr[p]&nbr[r]);oppP.append((p,r,c))
            for a,b in itertools.combinations(c,2):A.add(frozenset((p,r,a,b)))
    A=sorted(A,key=lambda z:tuple(sorted(z)));ai={a:i for i,a in enumerate(A)};AL=[];AF=[]
    for S in A:
        ed=[e for e in itertools.combinations(sorted(S),2) if e[1] in nbr[e[0]]]
        LL=frozenset(pair_line[tuple(sorted(e))] for e in ed);AL.append(LL);F=set()
        for a,b in ed:
            l=pair_line[tuple(sorted((a,b)))];F|={fi[(a,l)],fi[(b,l)]}
        AF.append(frozenset(F))
    ail={L:i for i,L in enumerate(AL)};ln=[set() for _ in lines]
    for i,j in itertools.combinations(range(len(lines)),2):
        if lines[i]&lines[j]:ln[i].add(j);ln[j].add(i)
    oppL=[]
    for l,m in itertools.combinations(range(len(lines)),2):
        if m not in ln[l]:oppL.append((l,m,sorted(ln[l]&ln[m])))
    support={a for a,F in enumerate(AF) if 0 in F};assert len(support)==q**4;charts=[]
    for p,r,c in oppP:
        T={ai[frozenset((p,r,c[i],c[j]))] for i,j in itertools.combinations(range(q+1),2)}&support
        if T:charts.append(frozenset(T))
    for l,m,c in oppL:
        T={ail[frozenset((l,m,c[i],c[j]))] for i,j in itertools.combinations(range(q+1),2)}&support
        if T:charts.append(frozenset(T))
    assert len(charts)==4*q**3 and {len(x) for x in charts}=={q};sl=sorted(support);pos={a:i for i,a in enumerate(sl)}
    C={frozenset(pos[a] for a in T) for T in charts};G=nx.Graph();G.add_nodes_from(range(q**4))
    for T in C:G.add_edges_from(itertools.combinations(T,2))
    return G,C

def root_cosets(q):
    I=np.eye(4,dtype=int)%q
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    def mm(A,B):return (A@B)%q
    def key(A):return tuple(map(int,A.flat))
    H=[[(I+t*Z)%q for t in range(q)] for Z in X];gens=[h[1] for h in H];U={key(I):I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            b=mm(a,g);k=key(b)
            if k not in U:U[k]=b;Q.append(b)
    assert len(U)==q**4;el=list(U.values());ei={key(a):i for i,a in enumerate(el)};C=set();families=[]
    for f,h in enumerate(H):
        seen=set()
        for g in el:
            c=frozenset(ei[key(mm(g,z))] for z in h)
            if c not in seen:seen.add(c);C.add(c);families.append((c,f))
        assert len(seen)==q**3
    G=nx.Graph();G.add_nodes_from(range(q**4))
    for c in C:G.add_edges_from(itertools.combinations(c,2))
    return G,C,el,H,mm,key,I,families

def perm_comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def perm_inv(p):
    z=[0]*len(p)
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def perm_order(p):
    seen=[0]*len(p);o=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;n=0
            while not seen[j]:seen[j]=1;n+=1;j=p[j]
            o=math.lcm(o,n)
    return o

def main():
    anchors={}
    for q in (2,3):
        B,BC=prime_building(q);U,UC,els,H,mm,key,I,fam=root_cosets(q);gm=nx.algorithms.isomorphism.GraphMatcher(B,U);assert gm.is_isomorphic();m=gm.mapping
        assert {frozenset(m[v] for v in c) for c in BC}==UC
        anchors[q]={'q4_points':q**4,'active_charts':4*q**3,'chart_size':q,'hypergraph_isomorphic':True}
        if q==3:
            aut=[tuple(g[i] for i in range(81)) for g in nx.algorithms.isomorphism.GraphMatcher(U,U).isomorphisms_iter()];assert len(aut)==324
            stab=[g for g in aut if g[0]==0];assert Counter(perm_order(g) for g in stab)==Counter({2:3,1:1})
            ei={key(a):i for i,a in enumerate(els)};left=[]
            for a in els:left.append(tuple(ei[key(mm(a,b))] for b in els))
            LS=set(left)
            assert all(perm_comp(perm_comp(s,L),perm_inv(s)) in LS for s in stab for L in left)
            # The four root-coset parallel classes are intrinsic as the four partitions of U by mutually disjoint q-lines.
            LL=list(UC);D=nx.Graph();D.add_nodes_from(range(len(LL)))
            for i,j in itertools.combinations(range(len(LL)),2):
                if LL[i].isdisjoint(LL[j]):D.add_edge(i,j)
            pcs=list({frozenset(c) for c in nx.find_cliques(D) if len(c)==27});assert len(pcs)==4
            lineclass={LL[i]:k for k,C in enumerate(pcs) for i in C}
            for s in stab:
                image=[]
                for C in pcs:
                    ks={lineclass[frozenset(s[v] for v in LL[i])] for i in C};assert len(ks)==1;image.append(next(iter(ks)))
                assert tuple(image)==(0,1,2,3)
            anchors[q].update({'graph_aut_order':324,'identity_stabilizer':'V4','left_regular_U_order':81,'left_regular_U_normal':True,'aut_structure':'U81 semidirect V4','root_parallel_classes':4,'V4_fixes_each_parallel_class_setwise':True})
    # Symbolic C2 commutator proof.
    def E(i,j):M=sp.zeros(4);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)]
    comm={(i,j):X[i]*X[j]-X[j]*X[i] for i,j in itertools.combinations(range(4),2)}
    nonzero={k:v for k,v in comm.items() if v!=sp.zeros(4)}
    assert nonzero[(0,1)]==X[2] and nonzero[(0,2)]==2*X[3] and len(nonzero)==2
    result={
      '5098':{'status':'THEOREM','statement':'For q=2 and q=3, the fixed-chamber apartment-star active-chart hypergraph is explicitly isomorphic, lines included, to the hypergraph of right cosets of the four positive-root subgroups in the type-C2 maximal unipotent group.','anchors':anchors},
      '5099':{'status':'THEOREM','q':3,'aut_order':324,'structure':'U81 semidirect V4','identity_stabilizer_orders':{'1':1,'2':3},'normal_regular_subgroup':81,'projective_chamber_stabilizer_order':'51840/160=324','root_direction_parallel_classes':4,'V4_action':'fixes each parallel class setwise'},
      '5100':{'status':'THEOREM','statement':'For a split finite Chevalley group with N positive roots, |U|=q^N and each positive-root subgroup has q elements, so the total first root-direction coset count is N q^(N-1), formally d(q^N)/dq. For C2, N=4 and the count is 4q^3.','boundary':'The root-coset identity is general; its identification with apartment-code active charts is certified here only for the W(3,q) rank-two setting at q=2,3.'},
      '5101':{'status':'THEOREM_ODD_CHARACTERISTIC_C2','symbolic_commutators':{'[X0,X1]':'X2','[X0,X2]':'2 X3','all_other_pairs':'0'},'odd_characteristic_pair_closure':'four q^2 pairs, one q^3 pair, one q^4 pair','reason':'<X0,X1> creates X2 then X3; <X0,X2> creates X3; the other four pairs commute. 2 invertible is the odd-characteristic condition.','characteristic2_boundary':'the 2 X3 commutator vanishes, giving the observed collapsed profile.'}
    }
    OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
