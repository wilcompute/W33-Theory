#!/usr/bin/env python3
"""Pass10677-10684 outside-box: the 27 harmonic states form a rank-27 cyclotomic association scheme.

Let G=C105 additively and H=<79> <= Aut(G), |H|=6.  The H-orbits on G are the
27 relations of the Schurian translation association scheme (G,H); equivalently
they index the spherical/Hecke algebra of C105:C6 with respect to C6.

CRT gives C105 ~= C3 x C5 x C7 and 79 -> (1,-1,2).  Since C6 ~= C2 x C3,
the orbit partition is the direct product of the three local rank-3 schemes:

  * C3 with trivial multiplier: the thin directed C3 scheme;
  * C5 under inversion: the pentagon C5 distance scheme;
  * C7 under <2>: D={1,2,4} and -D={3,5,6}.

D is a (7,3,1) cyclic difference set.  Its seven translates are the seven Fano
lines; the bipartite incidence graph between C7 points and translates of D is
exactly the Heawood graph.  Thus the Fano/Heawood object enters the 105-clock
through its C7 harmonic factor, not through a permutation of the six BT chamber
vertices.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10677_10684_C105_CYCLOTOMIC_ASSOCIATION_SCHEME.json'

def orbits(n,m):
    seen=set();out=[]
    for s in range(n):
        if s in seen: continue
        O=[];x=s
        while x not in O:
            O.append(x);seen.add(x);x=(m*x)%n
        out.append(tuple(O))
    return out

def diffs(D,n):
    return Counter((a-b)%n for a in D for b in D if a!=b)

def main():
    O105=orbits(105,79)
    O3=orbits(3,1); O5=orbits(5,4); O7=orbits(7,2)
    assert len(O105)==27 and len(O3)==len(O5)==len(O7)==3
    assert O3==[(0,),(1,),(2,)]
    assert O5==[(0,),(1,4),(2,3)]
    assert O7==[(0,),(1,2,4),(3,6,5)]
    assert Counter(map(len,O105))==Counter({6:12,3:6,2:6,1:3})
    assert 27==len(O3)*len(O5)*len(O7)

    # Verify CRT product of orbit partitions explicitly.
    def crt_key(x): return (x%3,x%5,x%7)
    products=[]
    for A in O3:
      for B in O5:
       for C in O7:
        S={x for x in range(105) if x%3 in A and x%5 in B and x%7 in C}
        products.append(frozenset(S))
    assert {frozenset(O) for O in O105}==set(products)

    # C7 Singer/Fano difference set.
    D={1,2,4};Dm={3,5,6}
    dd=diffs(D,7)
    assert set(dd)==set(range(1,7)) and set(dd.values())=={1}
    lines={tuple(sorted((x+d)%7 for d in D)) for x in range(7)}
    assert len(lines)==7 and all(len(L)==3 for L in lines)
    # Fano incidence axioms: every point on 3 lines; every pair on one line.
    point_degrees=Counter(p for L in lines for p in L)
    assert set(point_degrees.values())=={3}
    pair_counts=Counter()
    for L in lines:
      a=list(L)
      for i in range(3):
       for j in range(i+1,3): pair_counts[tuple(sorted((a[i],a[j])))]+=1
    assert len(pair_counts)==21 and set(pair_counts.values())=={1}
    # Incidence graph has 14 vertices, 21 edges, degree 3 and girth 6.
    edges=[(p,7+j) for j,L in enumerate(sorted(lines)) for p in L]
    assert len(edges)==21
    deg=Counter(v for e in edges for v in e); assert len(deg)==14 and set(deg.values())=={3}
    # no 4-cycle iff any two points share at most one line, already certified; Fano has triangles only in incidence-free projection, so bipartite girth is 6.

    # Local scheme intersection-number fingerprints p_ij^k.
    def intersection_numbers(n,Os):
      ans={}
      for k,Ok in enumerate(Os):
        d=Ok[0];mat=[]
        for i,Oi in enumerate(Os):
          row=[]
          for j,Oj in enumerate(Os):
            row.append(sum(1 for z in range(n) if z in Oi and (d-z)%n in Oj))
          mat.append(row)
        ans[str(k)]=mat
      return ans

    out={
      'schema':'w33.pass10677_10684.c105_cyclotomic_association_scheme.v1','status':'PASS','passes':'10677-10684','outside_box':True,
      'global_scheme':{
        'translation_group':'C105','multiplier_group':'C6=<79>','rank':27,
        'interpretation':'Schurian cyclotomic translation association scheme / spherical Hecke algebra of C105:C6 relative to C6',
        'relation_valencies':dict(Counter(map(len,O105))),
        'commutative_Bose_Mesner_algebra':True},
      'CRT_tensor_product':{
        'identity':'C105 ~= C3 x C5 x C7','multiplier':'79 -> (1,-1,2)','rank_factorization':'27=3*3*3',
        'local_orbits':{'C3':[list(x) for x in O3],'C5':[list(x) for x in O5],'C7':[list(x) for x in O7]},
        'scheme_identity':'A(C105,C6) ~= A(C3,1) tensor A(C5,< -1 >) tensor A(C7,<2>)'},
      'local_C3':{'name':'thin directed C3 / qutrit phase scheme','valencies':[1,1,1],'intersection_numbers':intersection_numbers(3,O3)},
      'local_C5':{'name':'pentagon C5 distance scheme','valencies':[1,2,2],'relation_1':'steps +/-1','relation_2':'steps +/-2','intersection_numbers':intersection_numbers(5,O5)},
      'local_C7':{
        'name':'Singer/Fano rank-3 cyclotomic scheme','valencies':[1,3,3],
        'difference_set':[1,2,4],'opposite_set':[3,5,6],'difference_multiset_nonzero_counts':{str(k):dd[k] for k in range(1,7)},
        'Fano_lines':[list(x) for x in sorted(lines)],'Fano_points':7,'Fano_lines_count':7,'Fano_incidence_edges':21,
        'incidence_graph':'Heawood graph (14 vertices, 3-regular, bipartite, girth 6)',
        'intersection_numbers':intersection_numbers(7,O7)},
      'theorem':'The 27 normalizer states are the relation classes of a canonical rank-27 cyclotomic association scheme on C105. CRT factors this scheme exactly into a thin C3/qutrit factor, the C5 pentagon distance scheme, and the C7 Singer/Fano scheme. The C7 multiplier orbit {1,2,4} is a (7,3,1) difference set, so its translates are literally the Fano plane and its incidence graph is Heawood.',
      'boundary':'Exact finite-group/association-scheme statement. It locates Fano/Heawood inside the C7 harmonic factor; it does not identify the six Bruhat-Tits chamber vertices with Heawood vertices or claim the H4 weighted quotient equals this Bose-Mesner algebra element.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rank':27,'tensor':'C3-thin x C5-pentagon x C7-Fano','Fano_difference_set':True}))
if __name__=='__main__': main()
