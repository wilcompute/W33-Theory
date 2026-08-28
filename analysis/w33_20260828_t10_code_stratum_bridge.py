#!/usr/bin/env python3
"""Exact T(10) carrier inside the existing W33 [36,17,4] code stratum.

Pass3957 already constructed a deterministic maximal [36,17,4] binary code
and observed that its 57 weight-four generators have an intersection-two graph
with components 45+6+6, the 45 component being SRG(45,16,8,4).

This pass identifies that 45-component internally and explicitly as T(10):
* it has exactly ten maximal K9 cliques;
* each vertex lies in exactly two K9s;
* every pair of K9s meets in exactly one vertex;
* mapping each vertex to its two containing K9s is therefore a bijection with
  C(10,2), and adjacency is exactly pair-intersection.

The ten K9s have an additional coordinate meaning. In each K9, two of the 36
binary coordinates occur in all nine weight-four words. The ten resulting
2-coordinate cores are exactly the ten nonsingular pairs {x,x+4}; the
translation vector 4 is singular in the frozen F2^6 quadratic model. Their
union is exactly the 20 coordinates of degree nine in the 57-word selection.

Thus the P1(F9) pair graph T(10) is not merely an abstract SRG that happens to
occur elsewhere: W33 already contains a native exact T(10) carrier in its
code-stratum machinery. What remains unproved is a canonical equivariant map
between the P1(F9)/HJ ten-set and these ten singular-translation fibres.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_20260828_T10_CODE_STRATUM_BRIDGE.json"

def bits(x,n=6):return [(x>>i)&1 for i in range(n)]
def qform(x):
    b=bits(x)
    return (b[0]*b[1]+b[2]*b[3]+b[4]*b[5]+b[4]+b[5])&1
def beta(x,y):return qform(x^y)^qform(x)^qform(y)

def gf2_basis(vals):
    piv={}
    for value in vals:
        x=int(value)
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:
                piv[p]=x
                for pp in list(piv):
                    if pp!=p and ((piv[pp]>>p)&1):piv[pp]^=x
                break
    return [piv[p] for p in sorted(piv,reverse=True)]

def build_selected():
    nons=[x for x in range(1,64) if qform(x)]
    assert len(nons)==36
    base_words=set()
    for label in range(64):
        w=0
        for i,x in enumerate(nons):
            if beta(label,x):w|=1<<i
        base_words.add(w)
    base=gf2_basis(base_words);assert len(base)==6
    w4=[]
    for sup in itertools.combinations(range(36),4):
        w=sum(1<<i for i in sup)
        if all(((w&b).bit_count()&1)==0 for b in base):w4.append(w)
    assert len(w4)==945
    neigh=[set() for _ in w4]
    for i,wi in enumerate(w4):
        for j in range(i+1,len(w4)):
            if ((wi&w4[j]).bit_count()&1)==0:
                neigh[i].add(j);neigh[j].add(i)
    cand=set(range(len(w4)));cl=[]
    while cand:
        v=max(cand,key=lambda x:(len(cand&neigh[x]),-x))
        cl.append(v);cand&=neigh[v]
    assert len(cl)==57
    return nons,[w4[i] for i in cl]

def intersection_graph(words):
    G=[set() for _ in words]
    for i,j in itertools.combinations(range(len(words)),2):
        if (words[i]&words[j]).bit_count()==2:G[i].add(j);G[j].add(i)
    seen=set();comps=[]
    for i in range(len(words)):
        if i in seen:continue
        st=[i];seen.add(i);C=[]
        while st:
            v=st.pop();C.append(v)
            for z in G[v]:
                if z not in seen:seen.add(z);st.append(z)
        comps.append(sorted(C))
    return G,sorted(comps,key=len,reverse=True)

def maximal_cliques(G,V):
    V=set(V);out=[]
    def bk(R,P,X):
        if not P and not X:
            out.append(tuple(sorted(R)));return
        if not P:return
        U=P|X
        u=max(U,key=lambda z:len(P&G[z])) if U else None
        for v in list(P-(G[u] if u is not None else set())):
            bk(R|{v},P&G[v],X&G[v]);P.remove(v);X.add(v)
    bk(set(),set(V),set())
    return sorted(set(out),key=lambda x:(len(x),x))

def params(G,C):
    C=set(C);deg=[len(G[v]&C) for v in C];la=set();mu=set()
    L=sorted(C)
    for ii,i in enumerate(L):
        for j in L[ii+1:]:
            c=len((G[i]&G[j])&C);(la if j in G[i] else mu).add(c)
    return [len(C),sorted(set(deg)),sorted(la),sorted(mu)]

def main():
    nons,sel=build_selected()
    G,comps=intersection_graph(sel)
    assert list(map(len,comps))==[45,6,6]
    C=comps[0];assert params(G,C)==[45,[16],[8],[4]]
    mc=maximal_cliques(G,C)
    hist=Counter(map(len,mc))
    assert hist==Counter({3:120,9:10})
    K9=[x for x in mc if len(x)==9]
    assert len(K9)==10
    containing={v:[] for v in C}
    for ci,K in enumerate(K9):
        for v in K:containing[v].append(ci)
    assert {len(x) for x in containing.values()}=={2}
    ints=Counter(len(set(K9[i])&set(K9[j])) for i,j in itertools.combinations(range(10),2))
    assert ints==Counter({1:45})
    labels={v:tuple(sorted(containing[v])) for v in C}
    assert len(set(labels.values()))==45==len(list(itertools.combinations(range(10),2)))
    for i,j in itertools.combinations(C,2):
        assert (j in G[i])==(len(set(labels[i])&set(labels[j]))==1)

    cores=[]
    for K in K9:
        deg=Counter()
        for v in K:
            for c in range(36):
                if (sel[v]>>c)&1:deg[c]+=1
        core=tuple(sorted(c for c,n in deg.items() if n==9))
        assert len(core)==2
        assert Counter(deg.values())==Counter({1:18,9:2})
        cores.append(core)
    assert len(set(cores))==10
    label_cores=[tuple(sorted((nons[a],nons[b]))) for a,b in cores]
    xors={a^b for a,b in label_cores}
    assert xors=={4} and qform(4)==0
    all_translation_pairs=sorted({tuple(sorted((x,x^4))) for x in nons if qform(x^4)})
    assert sorted(label_cores)==all_translation_pairs and len(all_translation_pairs)==10

    coordinate_degree=Counter(sum((w>>c)&1 for w in sel) for c in range(36))
    assert coordinate_degree==Counter({9:20,3:16})
    high={c for c in range(36) if sum((w>>c)&1 for w in sel)==9}
    core_union={c for z in cores for c in z}
    assert high==core_union and len(high)==20

    out={
      "schema":"w33.20260828.t10-code-stratum-bridge.v1","status":"PASS",
      "source_stratum":"Pass3957 deterministic maximal [36,17,4] binary code",
      "weight4_selection":57,
      "intersection2_components":[45,6,6],
      "component45":{"parameters":[45,16,8,4],"maximal_clique_histogram":dict(sorted(hist.items())),
                     "K9_count":10,"K9_pair_intersections":dict(sorted(ints.items())),
                     "K9s_per_vertex":2,"T10_isomorphism":True,
                     "coordinatization":"vertex -> unordered pair of the two containing K9 cliques"},
      "ten_fibre_coordinate_model":{
        "translation_vector":4,"translation_vector_binary":"000100",
        "translation_vector_singular":True,
        "core_pairs_coordinate_indices":[list(x) for x in sorted(cores)],
        "core_pairs_F2_6_labels":[list(x) for x in sorted(label_cores)],
        "all_pairs_are_x_xor_4":True,
        "core_union_size":20,
        "selected_word_coordinate_degree_profile":{"3":16,"9":20},
        "degree9_coordinates_equal_core_union":True},
      "P1F9_consequence":"The canonical unordered-pair graph on the ten P1(F9) states and this native W33 code-stratum component are both literally T(10). Any bijection of the underlying ten-sets induces a graph isomorphism.",
      "missing_intertwiner":"No canonical equivariant bijection is yet proved between the HJ10/P1(F9) ten states and the ten singular-translation fibres {x,x+4}; the graph bridge is exact but the ten-set bridge is not.",
      "theorem":"The existing W33 [36,17,4] code stratum contains a canonical 45-state T(10): ten maximal K9s coordinatize its vertices by C(10,2), and the ten K9 fibres are exactly the ten nonsingular coordinate pairs under the singular translation x->x+4.",
      "boundary":"This identifies an exact native T(10) graph and ten-fibre structure. It does not undo the GQ(4,2) orbital no-go and does not identify the ten fibres with HJ10 without an equivariant map."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","T10":True,"K9":10,"translation":4,"components":[45,6,6]}))
if __name__=="__main__":main()
