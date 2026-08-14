#!/usr/bin/env python3
"""Pass5140 (bonkers): all-q third-order chamber-star intersection law.

In the chamber graph of a generalized quadrangle apartment (an 8-cycle), three
chambers can lie in one apartment only in five dihedral distance patterns.
For W(3,q), successive completion in the generalized-quadrangle incidence
geometry gives q^2, q, or 1 apartments according to that pattern.  We verify
the complete rooted triple census objectwise at q=2,3,4,5, including GF(4).
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5140_ALLQ_TRIPLE_CHAMBER_STAR_LAW.json'

def dist_from_inter(q,w):
    for d in range(1,5):
        if w==q**(4-d):return d
    raise AssertionError((q,w))

def predicted(q,sig):
    return {(1,1,2):q*q,(1,2,3):q,(1,3,4):1,(2,2,4):1,(2,3,3):1}.get(sig,0)

def anchor(q):
    G=build_W(q);S=chamber_stars(G);n=len(S);base=S[0]
    d0=[0]*n
    for i in range(1,n):d0[i]=dist_from_inter(q,(base&S[i]).bit_count())
    hist=Counter();by_sig=defaultdict(Counter)
    for i,j in itertools.combinations(range(1,n),2):
        dij=dist_from_inter(q,(S[i]&S[j]).bit_count())
        sig=tuple(sorted((d0[i],d0[j],dij)))
        t=(base&S[i]&S[j]).bit_count();hist[t]+=1;by_sig[sig][t]+=1
        assert t==predicted(q,sig),(q,sig,t,predicted(q,sig))
    assert all(len(H)==1 for H in by_sig.values())
    return {'q':q,'chambers':n,'fixed_base_triples':sum(hist.values()),
      'triple_intersection_histogram':{str(k):v for k,v in sorted(hist.items())},
      'distance_signatures':{str(sig):{'intersection':next(iter(H)),'count':sum(H.values())} for sig,H in sorted(by_sig.items())}}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5140,'status':'THEOREM_ALL_Q_TRIPLE_CHAMBER_STAR_INTERSECTION_LAW',
      'law':{'(1,1,2)':'q^2','(1,2,3)':'q','(1,3,4)':'1','(2,2,4)':'1','(2,3,3)':'1','all_other_sorted_distance_signatures':'0'},
      'geometric_proof':'An apartment is an induced 8-cycle in the Levi graph. Up to dihedral symmetry, three distinct cycle edges have exactly the five displayed gallery-distance signatures. Conversely each displayed chamber hull embeds in an apartment. Completing the hull to an 8-cycle leaves respectively two, one, or zero independent generalized-quadrangle projection choices, each with q possibilities, giving q^2,q,1. Any other distance triangle cannot embed in C8 and has intersection zero.',
      'anchors':A,
      'q5_histogram_expected':{'0':428320,'1':7500,'5':750,'25':75},
      'connection':'Pass5134 proved pairwise information fails at leader 18. This supplies the exact third-order coefficient |Si cap Sj cap Sk| from pairwise gallery distances alone, enabling a cubic inclusion-exclusion/LP attack without enumerating apartments again.',
      'boundary':'This is the triple-intersection law. Higher parity inclusion-exclusion still contains fourth and higher intersections, so q5 d=625 is not yet claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
