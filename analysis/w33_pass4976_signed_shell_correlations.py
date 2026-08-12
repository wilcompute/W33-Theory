#!/usr/bin/env python3
"""Pass4976 — low-shell correlations from the H36 triangle model.

The 360 coordinates are the edges of the 36-double-six graph H36.  The
nontrivial switching generator sigma from Pass4859 is reconstructed from the E6
root signing.  A graph triangle is in K^perp iff its sigma parity is zero.

This identifies all 1080 weight-three dual words with the non-Steiner H36
triangles, proves that they span the entire 324-dimensional dual code, and uses
that span to reject the artificial Pass4960 degree-seven witness.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4976_SIGNED_SHELL_CORRELATIONS.json'
A={3:1080,4:10530,5:127656,6:2329680,7:37193040}

def Q6(v):
    a,c,d,e,f,g=v; return (a*c+d*e+f+f*g+g)&1
def gf2_rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def main()->int:
    # Cubic 27-line / 36-double-six graph.
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0]
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for X,Y in itertools.combinations(C6,2):
        if X&Y:continue
        H=G.subgraph(X|Y)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):
            DS.add(frozenset(X|Y))
    DS=sorted(DS,key=lambda s:tuple(sorted(s)));assert len(DS)==36
    H=nx.Graph();H.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H.add_edge(i,j)
    E=sorted(tuple(sorted(e)) for e in H.edges());ei={e:i for i,e in enumerate(E)}
    assert len(E)==360
    tri=sorted(t for t in itertools.combinations(range(36),3)
               if all(H.has_edge(*e) for e in itertools.combinations(t,2)))
    steiner=set(t for t in tri if len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    assert (len(tri),len(steiner))==(1200,120)

    # Pass4859 E6 root signing sigma on H36 edges.
    C=np.eye(6,dtype=int)*2
    for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
    def ref(v,i):
        v=np.array(v,dtype=int);m=int(v@C[:,i]);w=v.copy();w[i]-=m;return tuple(map(int,w))
    roots={(1,0,0,0,0,0)};D=deque(roots)
    while D:
        v=D.popleft()
        for i in range(6):
            w=ref(v,i)
            if w not in roots:roots.add(w);D.append(w)
    pos=sorted(v for v in roots if all(x>=0 for x in v));assert len(pos)==36
    ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
    for i,j in itertools.combinations(range(36),2):
        z=int(np.array(pos[i])@C@np.array(pos[j]));ip[(i,j)]=z
        if abs(z)==1:ER.add_edge(i,j)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(H,ER).isomorphisms_iter())
    sigma=np.zeros(360,dtype=np.uint8)
    for e,(a,b) in enumerate(E):
        i,j=sorted((iso[a],iso[b]));sigma[e]=int(ip[(i,j)]<0)

    masks=[];parity_class=Counter()
    for t in tri:
        m=0
        for e in itertools.combinations(t,2):m|=1<<ei[tuple(sorted(e))]
        p=sum(int(sigma[k]) for k in range(360) if (m>>k)&1)&1
        parity_class[('Steiner' if t in steiner else 'nonSteiner',p)]+=1
        if p==0:masks.append(m)
    assert parity_class==Counter({('nonSteiner',0):1080,('Steiner',1):120})
    assert len(masks)==A[3] and gf2_rank(masks)==324

    # Exact pair convolution of the weight-3 shell.
    pair_weight=Counter();multiplicity=Counter()
    for i in range(len(masks)):
        for j in range(i+1,len(masks)):
            x=masks[i]^masks[j];pair_weight[x.bit_count()]+=1;multiplicity[x]+=1
    w4_mult=Counter(v for x,v in multiplicity.items() if x.bit_count()==4)
    w6_mult=Counter(v for x,v in multiplicity.items() if x.bit_count()==6)
    assert pair_weight==Counter({6:569700,4:12960})
    assert w4_mult==Counter({1:6480,2:3240})
    assert w6_mult==Counter({1:569700})
    w4_reachable=sum(w4_mult.values())
    assert w4_reachable==9720 and A[4]-w4_reachable==810

    # Extremal T3 values fix the complete character because shell3 spans K^perp.
    pass4960_fake={3:-1080,4:-1936,5:75316,6:830590,7:-37193040}
    forced_minus={j:(-1 if j%2 else 1)*A[j] for j in A}
    forced_plus={j:A[j] for j in A}
    assert pass4960_fake[3]==-A[3] and pass4960_fake[4]!=forced_minus[4]

    out={
      'pass':4976,'code':'K=[360,36,20]_2',
      'H36_triangle_dual_shell':{
        'H36_edges_coordinates':360,'H36_triangles':1200,'Steiner_triangles_sigma_odd':120,
        'nonSteiner_triangles_sigma_even':1080,'dual_weight3_words':1080,
        'weight3_span_rank':324,'dual_dimension':324,'weight3_shell_spans_full_dual':True},
      'shell3_pair_convolution':{
        'unordered_pairs_weight4':12960,'unordered_pairs_weight6':569700,
        'distinct_weight4_words_reached':9720,'weight4_multiplicity_distribution':{'1':6480,'2':3240},
        'frozen_A4':A[4],'weight4_words_not_reached_by_two_shell3_words':810,
        'distinct_weight6_words_reached':569700,'weight6_multiplicity_distribution':{'1':569700}},
      'extremal_character_lock':{
        'T3_plus_1080_forces':{str(j):forced_plus[j] for j in A},
        'T3_minus_1080_forces':{str(j):forced_minus[j] for j in A},
        'reason':'the 1080 shell-3 words span all 324 dimensions of K^perp; all + signs give the trivial character and all - signs give the weight-parity character'},
      'Pass4960_relaxation_witness':{
        'signed_shell_values':{str(j):pass4960_fake[j] for j in pass4960_fake},
        'realizable_character':False,
        'first_contradiction':'T3=-1080 forces T4=+10530, not -1936'},
      'covering_radius':{'proved_interval':[134,173],'improved_here':False},
      'theorem':'The 1080 non-Steiner H36 triangles are exactly the sigma-even weight-three dual checks and span the full 324-dimensional dual code. Consequently the signed low-shell sums are correlated: in particular T3=+1080 forces Tj=Aj for every shell, while T3=-1080 forces Tj=(-1)^j Aj. This rejects the exact degree-seven relaxation witness used in Pass4960. The shell-3 pair convolution also reaches 9720 of the 10530 weight-four dual words, with multiplicities 1^6480 and 2^3240.',
      'consequence':'The Pass4960 moment functional is genuinely non-character-valued. Future radius work can impose shell-product/character relations rather than independent |Tj| bounds.',
      'boundary':'Rejecting the Pass4960 relaxation witness does not by itself exclude every possible distance-173 coset. The rigorous covering-radius interval remains 134<=rho(K)<=173.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
